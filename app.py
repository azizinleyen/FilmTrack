import os
import json
import re
import threading
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# 🔑 OMDB API KEY
# ==========================================
OMDB_API_KEY = "YOUR_OMDB_API_KEY"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")
POSTERS_DIR = os.path.join(STATIC_DIR, "posters")

MOVIES_FILE = os.path.join(DATA_DIR, "movies.json")
SERIES_FILE = os.path.join(DATA_DIR, "series.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(POSTERS_DIR, exist_ok=True)

SEARCH_CACHE = {}

def upgrade_poster_quality(url):
    """OMDb / IMDb afişlerini 1000px HD çözünürlüğe yükseltir."""
    if not url or url == "N/A":
        return url
    if "media-amazon.com" in url or "imdb.com" in url:
        if "@._V1_" in url:
            return re.sub(r'@\._V1_.*\.jpg$', '@._V1_SX1000.jpg', url)
        url = re.sub(r'_SX\d+', '_SX1000', url)
        url = re.sub(r'_SY\d+', '_SX1000', url)
    return url

def sort_media(media_list):
    """
    1. Öncelik: Kullanıcı Puanı (Azalan)
    2. Öncelik: IMDb Puanı (Azalan)
    """
    def sort_key(m):
        try:
            user_p = float(m.get("user_rating", 0) or 0)
        except (ValueError, TypeError):
            user_p = 0.0
        try:
            imdb_p = float(m.get("imdb_rating", 0) or 0)
        except (ValueError, TypeError):
            imdb_p = 0.0
        return (user_p, imdb_p)

    return sorted(media_list, key=sort_key, reverse=True)

DEFAULT_MOVIES = [
    {
        "imdbID": "tt0816692",
        "title": "Interstellar",
        "year": "2014",
        "runtime": "169 dk",
        "director": "Christopher Nolan",
        "actors": "Matthew McConaughey, Jessica Chastain, Anne Hathaway, Michael Caine, Matt Damon",
        "plot": "Dünya'nın geleceği tehlikedeyken, eski bir NASA pilotu ve ekibi, insanlığın hayatta kalma umudunu taşıyan yeni bir gezegen bulmak için uzayda tehlikeli bir yolculuğa çıkar. Zaman, artık en büyük düşmanlarıdır.",
        "tags": ["Bilim Kurgu", "Dram", "Macera", "Gerilim", "Psikolojik"],
        "user_rating": 9,
        "imdb_rating": "8.6",
        "notes": "Gerçekten etkileyici bir film. Nolan'ın zaman kavramını işleyişi muazzam. Özellikle son sahne hala aklımda. Görsel efektler ve müzikler filme ayrı bir derinlik katmış.",
        "poster": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_SX1000.jpg",
        "poster_local": ""
    },
    {
        "imdbID": "tt1375666",
        "title": "Inception",
        "year": "2010",
        "runtime": "148 dk",
        "director": "Christopher Nolan",
        "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
        "plot": "Çok yetenekli bir hırsız, insanların bilinçaltına rüya esnasında girerek en gizli sırlarını çalar. Bu seferki görevi ise bir fikri çalmak değil, bilinçaltına yerleştirmektir.",
        "tags": ["Bilim Kurgu", "Gerilim", "Macera"],
        "user_rating": 8,
        "imdb_rating": "8.8",
        "notes": "Rüya içinde rüya konsepti harika işlenmiş. Akılda kalıcı bir film.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX1000.jpg",
        "poster_local": ""
    },
    {
        "imdbID": "tt0111161",
        "title": "The Shawshank Redemption",
        "year": "1994",
        "runtime": "142 dk",
        "director": "Frank Darabont",
        "actors": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
        "plot": "İşlemediği bir cinayetten hüküm giyen Andy Dufresne'in Shawshank hapishanesinde yıllar süren umut ve sabır dolu mücadelesi.",
        "tags": ["Dram", "Suç", "Kült"],
        "user_rating": 10,
        "imdb_rating": "9.3",
        "notes": "Umudun asla kaybolmaması gerektiğini hatırlatan muhteşem bir film.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_SX1000.jpg",
        "poster_local": ""
    }
]

DEFAULT_SERIES = []

def get_file_path(media_type):
    return SERIES_FILE if media_type == "series" else MOVIES_FILE

def get_default_media(media_type):
    return DEFAULT_SERIES if media_type == "series" else DEFAULT_MOVIES

def async_download_poster(imdb_id, poster_url, media_type="movies"):
    poster_url = upgrade_poster_quality(poster_url)
    if not poster_url or poster_url == "N/A":
        return
    filename = f"{imdb_id}.jpg"
    local_path = os.path.join(POSTERS_DIR, filename)

    if os.path.exists(local_path) and os.path.getsize(local_path) > 35000:
        return

    try:
        res = requests.get(poster_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(res.content)
            items = load_media(media_type)
            for m in items:
                if m["imdbID"] == imdb_id:
                    m["poster_local"] = f"/static/posters/{filename}"
                    break
            save_media(media_type, items)
    except Exception as e:
        print(f"Afiş indirme uyarısı ({imdb_id}): {e}")

def load_media(media_type="movies"):
    file_path = get_file_path(media_type)
    default_data = get_default_media(media_type)

    if not os.path.exists(file_path):
        save_media(media_type, default_data)
        for m in default_data:
            threading.Thread(target=async_download_poster, args=(m["imdbID"], m.get("poster", ""), media_type), daemon=True).start()
        return sort_media(default_data)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            changed = False
            for m in items:
                orig = m.get("poster", "")
                upgraded = upgrade_poster_quality(orig)
                if orig != upgraded:
                    m["poster"] = upgraded
                    changed = True
            if changed:
                save_media(media_type, items)
            return sort_media(items)
    except Exception:
        return []

def save_media(media_type, items):
    file_path = get_file_path(media_type)
    sorted_data = sort_media(items)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/counts", methods=["GET"])
def get_counts():
    movies = load_media("movies")
    series = load_media("series")
    return jsonify({"movies": len(movies), "series": len(series)})

@app.route("/api/<media_type>", methods=["GET"])
def get_media(media_type):
    if media_type not in ["movies", "series"]:
        return jsonify({"Error": "Geçersiz kütüphane türü"}), 400
    return jsonify(load_media(media_type))

@app.route("/api/<media_type>", methods=["POST"])
def save_single_media(media_type):
    if media_type not in ["movies", "series"]:
        return jsonify({"Error": "Geçersiz kütüphane türü"}), 400

    data = request.json
    if not data or not data.get("imdbID"):
        return jsonify({"Error": "Geçersiz veri"}), 400

    data["poster"] = upgrade_poster_quality(data.get("poster", ""))

    items = load_media(media_type)
    imdb_id = data["imdbID"]
    poster_url = data.get("poster", "")

    local_file = f"{imdb_id}.jpg"
    local_path = os.path.join(POSTERS_DIR, local_file)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 35000:
        data["poster_local"] = f"/static/posters/{local_file}"
    else:
        threading.Thread(target=async_download_poster, args=(imdb_id, poster_url, media_type), daemon=True).start()

    existing_index = next((i for i, m in enumerate(items) if m["imdbID"] == imdb_id), None)
    if existing_index is not None:
        items[existing_index] = data
    else:
        items.insert(0, data)

    save_media(media_type, items)
    return jsonify({"success": True, "item": data})

@app.route("/api/<media_type>/<imdb_id>", methods=["DELETE"])
def delete_single_media(media_type, imdb_id):
    if media_type not in ["movies", "series"]:
        return jsonify({"Error": "Geçersiz kütüphane türü"}), 400

    items = load_media(media_type)
    updated = [m for m in items if m["imdbID"] != imdb_id]
    save_media(media_type, updated)
    return jsonify({"success": True})

@app.route("/api/omdb/search", methods=["GET"])
def omdb_search():
    query = request.args.get("q", "").strip()
    media_type = request.args.get("type", "").strip() # 'movie' veya 'series'
    if not query:
        return jsonify({"Search": []})

    if not OMDB_API_KEY:
        return jsonify({"Error": "OMDb API anahtarı app.py içerisine girilmemiş!"}), 400

    cache_key = f"{query.lower()}_{media_type}"
    if cache_key in SEARCH_CACHE:
        return jsonify(SEARCH_CACHE[cache_key])

    url = "https://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "s": query}
    if media_type:
        params["type"] = media_type

    try:
        res = requests.get(url, params=params, timeout=8)
        data = res.json()
        if data.get("Response") == "True" and "Search" in data:
            SEARCH_CACHE[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"Error": f"OMDb bağlantı hatası: {str(e)}"}), 500

@app.route("/api/omdb/detail", methods=["GET"])
def omdb_detail():
    imdb_id = request.args.get("id", "").strip()
    if not imdb_id:
        return jsonify({"Error": "imdbID eksik"}), 400

    if not OMDB_API_KEY:
        return jsonify({"Error": "OMDb API anahtarı app.py içerisine girilmemiş!"}), 400

    if imdb_id in SEARCH_CACHE:
        return jsonify(SEARCH_CACHE[imdb_id])

    url = "https://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "i": imdb_id, "plot": "full"}
    try:
        res = requests.get(url, params=params, timeout=8)
        data = res.json()
        if data.get("Response") == "True":
            if data.get("Poster") and data["Poster"] != "N/A":
                data["Poster"] = upgrade_poster_quality(data["Poster"])
            SEARCH_CACHE[imdb_id] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"Error": f"OMDb detay hatası: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)

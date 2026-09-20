<div align="center">

# 🎬 FilmTracker (FilmTrack & DiziTrack)


<p align="center">
  <img src="https://github.com/user-attachments/assets/a8ec1f3d-996c-435f-9a11-2d962983dcd4" alt="FilmTracker Showcase" width="100%">
</p>

## Project Overview

**A sleek, dark-themed personal movie and TV show journal built for cinematic lovers.**  
*Crafted through "Vibe Coding" — Designed, architected, and curated with passion; generated and brought to life with AI.*

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Styling](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Built with AI](https://img.shields.io/badge/Vibe_Coding-AI_Assisted-8A2BE2?style=for-the-badge&logo=openai&logoColor=white)](#-the-vibe-coding-story)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

> [!NOTE]  
> **Language & Localization Notice:**  
> While this repository and documentation are maintained in English, the **user interface and sample entries are localized in Turkish**, as this project was tailored strictly for personal daily use.

---

## 🌟 Overview

**FilmTracker** is a self-hosted personal media tracker that replaces bloated spreadsheets and third-party tracking services with a clean, bespoke, single-page web experience. It bridges the gap between structured movie logs and personal reviews, offering automated metadata fetching, offline poster caching, and flexible view layouts.

---

## 💡 The "Vibe Coding" Story

This project is a product of modern **vibe coding**:
- **Human Direction:** Product vision, user experience requirements, responsive layout design, metadata workflow, color palette, and business logic.
- **AI Execution:** 100% of the backend Flask architecture, asynchronous multithreaded poster scrapers, JSON database operations, and frontend JavaScript state management were written via AI prompts under strict iterative guidance.

---

## ✨ Key Features

### 1. 🎞️ Dual Media Engine (Movies & Series)
- Switch seamlessly between **Filmler** (Movies) and **Diziler** (TV Shows).
- Dynamic contextual labeling, dedicated counters, and decoupled JSON stores (`movies.json` and `series.json`).

### 2. ⚡ Automatic OMDb Integration & Smart Scraping
- **Live Search with Debounce:** Type movie or show titles to get instant search suggestions via the OMDb API.
- **One-Click Auto-Fill:** Pulls Title, Release Year, Director/Creator, Actors, Plot Synopsis, Genre Tags, and Official IMDb ratings instantly.
- **Manual Bypass:** Option to skip automatic lookup and enter custom or unlisted titles manually.

### 3. 🖼️ HD Poster Optimization & Asynchronous Caching
- **Quality Enhancement:** Automatically transforms standard OMDb/IMDb poster thumbnails into crystal-clear, high-resolution 1000px (`SX1000`) artwork.
- **Non-Blocking Background Caching:** Uses Python background worker threads (`threading.Thread`) to download and cache posters locally into `static/posters/`. The app remains fast and responsive while media assets download in the background.

### 4. 🎛️ Dual Display Modes
- **Compact List View:** Data-dense, sortable table displaying posters, metadata, genre badges, personal ratings, IMDb scores, personal reviews, and quick action buttons.
- **Showcase Gallery View:** Cinematic spotlight view featuring full-size poster art, complete production credits, tags, full plot summaries, and an interactive horizontal thumbnail carousel strip.

### 5. 🔍 Multi-Criteria Search & Filtering
- **Fuzzy Search:** Filter locally across titles, directors, actors, and personal notes simultaneously.
- **Rating Operator Syntax:** Query directly by your personal score using the syntax `puan:9` or `rating:8`.
- **Dynamic Tag Sidebar:** Generates a real-time list of genres and user tags along with live item counters for instant filtering.

### 6. ⭐ Smart Sorting & Journaling
- **Dual-Tier Sorting:** Automatically prioritizes items by **Your Personal Rating** first (descending), followed by **IMDb Rating** (descending).
- **Personal Notes:** A dedicated space on every card and gallery item to log thoughts, cinema experiences, quotes, or rewatch impressions.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** [Python 3](https://www.python.org/) & [Flask](https://flask.palletsprojects.com/)
- **Data Persistence:** Local JSON Flat-File storage (`data/movies.json`, `data/series.json`) — *No database installation or setup required.*
- **Async Operations:** Python native `threading` for background network requests.
- **Frontend:** Semantic HTML5, Vanilla JavaScript (ES6+), and [Tailwind CSS](https://tailwindcss.com/) (Dark Mode palette).
- **Icons & Typography:** [Lucide Icons](https://lucide.dev/) and Google Fonts ([Inter](https://fonts.google.com/specimen/Inter)).
- **External API:** [OMDb API](http://www.omdbapi.com/) for film & series metadata.

---

## 📁 Project Structure

```text
FilmTracker/
│
├── app.py                    # Flask server, API endpoints, thread runner, & business logic
├── templates/
│   └── index.html            # Main Single-Page Application (SPA) UI with Tailwind & JS
├── static/
│   └── posters/              # Locally cached HD poster image files (auto-generated)
├── data/
│   ├── movies.json           # Local storage for movie entries (auto-generated)
│   └── series.json           # Local storage for series entries (auto-generated)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

Follow these steps to run the application locally on your computer:

### 1. Prerequisites
Ensure you have **Python 3.9+** and `pip` installed.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/FilmTracker.git
cd FilmTracker
```

### 3. Install Dependencies
```bash
pip install flask requests
```
*(Or install via `pip install -r requirements.txt` if generated)*

### 4. Configure Your OMDb API Key
To enable automatic movie search and poster retrieval:
1. Obtain a free API key from [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx).
2. Open `app.py` in your text editor.
3. Update line 12 with your key:
   ```python
   OMDB_API_KEY = "YOUR_API_KEY_HERE"
   ```

### 5. Run the Server
```bash
python app.py
```

Open your browser and visit:  
👉 **`http://127.0.0.1:5000`**

---

## 📖 User Guide

### 1. Adding a Film or Series
1. Click the **"Film Ekle"** (or **"Dizi Ekle"**) button in the top navigation bar.
2. **Step 1 (Search):** Type the title of the media in the search bar. The OMDb dropdown will display the top 5 matches with thumbnail previews. Click on the desired title.
   * *Alternative:* Click *"Bilgileri manuel girmek için ilerle"* to fill out all details by hand.
3. **Step 2 (Personalize):**
   - Review or edit the imported title, release year, director, cast, and plot.
   - Adjust **Kullanıcı Puanım** using the interactive rating slider (from 1 to 10).
   - Add custom tags (e.g., `Favori`, `Festival`, `Tekrar İzle`) by typing and pressing **Enter**.
   - Write your thoughts in the **Kişisel Notlar** textarea.
4. Click **"Koleksiyona Kaydet"**.

### 2. Navigating Views
- **Switching Libraries:** Use the left sidebar to toggle between **Filmler** (Movies) and **Diziler** (Series).
- **Switching Layouts:** Use the view toggle in the header:
  - **Liste (List):** High-density tabular layout. Click any poster or title to open it directly in the gallery viewer.
  - **Galeri (Gallery):** Large cinematic showcase. Click any card in the bottom filmstrip carousel to preview its details.

### 3. Searching & Filtering
- **Standard Search:** Type any word into the top search bar to filter by Title, Cast, Director, or text in your Personal Notes.
- **Rating Filtering:** Enter `puan:10` or `rating:9` into the search bar to isolate titles matching that exact personal score.
- **Sidebar Tags:** Click any tag under **"Etiketler ve Türler"** in the sidebar to view only media tagged with that category. Click again to reset.

### 4. Updating & Deleting
- **Edit:** Click the **Pencil icon** (available in the table row or gallery notes section) to change tags, scores, or reviews.
- **Delete:** Click the **Trash icon** in the list view to delete an item (a confirmation prompt will ensure accidental clicks are avoided).

---

## 🔌 API Reference

The backend exposes clean REST endpoints for frontend communication:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/counts` | Returns total item counts for movies and series |
| `GET` | `/api/<movies\|series>` | Fetches all saved items sorted by score |
| `POST` | `/api/<movies\|series>` | Creates or updates a single entry |
| `DELETE`| `/api/<movies\|series>/<imdbID>` | Deletes an item by IMDb ID |
| `GET` | `/api/omdb/search?q={query}&type={type}` | Proxies and caches title searches through OMDb |
| `GET` | `/api/omdb/detail?id={imdbID}` | Fetches full plot and metadata by IMDb ID |

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <sub>Designed for personal aesthetics & effortless media journaling. Powered by Flask, Tailwind, and AI.</sub>
</div>

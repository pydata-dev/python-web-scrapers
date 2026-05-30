# 🕷️ Python Web Scrapers Portfolio

A collection of three production-ready web scrapers built with Python, demonstrating different scraping techniques for real-world use cases.

---

## 📁 Projects

### 1. `static prices.py` — Static Scraper (Books)
**Target:** [books.toscrape.com](http://books.toscrape.com)

Scrapes book data across multiple pages using HTTP requests — no browser required.

**Tech:** `requests` · `BeautifulSoup4` · `openpyxl`

**Data collected:**
- Title
- Price (float)
- Rating (converted from text to integer)

**Features:**
- Multi-page pagination (URL-based)
- Safe price parsing with error handling
- Rating mapped from words to numbers (`"Five"` → `5`)
- Auto-generated timestamped `.xlsx` output

---

### 2. `static 1.py` — Static Scraper (News)
**Target:** [news.ycombinator.com](https://news.ycombinator.com) (Hacker News)

Scrapes the front page of Hacker News and exports headlines to Excel.

**Tech:** `requests` · `BeautifulSoup4` · `openpyxl`

**Data collected:**
- Index
- Headline
- Source domain
- URL

**Features:**
- Top 30 stories extraction
- HTTP error handling with `raise_for_status()`
- Clean source domain parsing

---

### 3. `dynamic.py` — Dynamic Scraper (JavaScript-rendered)
**Target:** [quotes.toscrape.com/js](https://quotes.toscrape.com/js)

Scrapes a JavaScript-rendered website that loads content via AJAX — requires a real browser to execute JS.

**Tech:** `Selenium` · `BeautifulSoup4` · `openpyxl`

**Data collected:**
- Quote text
- Author
- Tags (comma-separated string)
- Tags count (integer)

**Features:**
- Headless Chrome (`--headless=new`) — no GUI window
- `WebDriverWait` explicit waits — no hardcoded `sleep()`
- JS-driven pagination via button clicks (no URL manipulation)
- Smart save path: checks for local `parsers/` folder, falls back to Desktop
- Cross-platform folder auto-open after scraping (Windows / macOS / Linux)

---

## ⚙️ Installation

```bash
pip install requests beautifulsoup4 selenium openpyxl
```

> **Note:** `dynamic.py` requires Google Chrome to be installed. ChromeDriver is managed automatically by Selenium 4.x.

---

## 📊 Output

All scrapers export data to `.xlsx` (Excel) with:
- Auto-generated timestamped filenames (e.g. `books_20260528_191500.xlsx`)
- Formatted headers
- Clean, typed data (floats, integers, strings)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` | HTTP requests for static pages |
| `BeautifulSoup4` | HTML parsing |
| `Selenium` | Browser automation for JS-rendered pages |
| `openpyxl` | Excel file creation and formatting |

---

## 📬 Contact

Open to freelance scraping projects — data extraction, automation, and ETL pipelines.
**Telegram:** [t.me/Galifianaxis](https://t.me/Galifianaxis)
**Email:** arsenijaleksandrovich09@gmail.com

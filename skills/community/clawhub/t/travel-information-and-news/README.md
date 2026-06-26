# Travel Information and News

<p align="center">
  <strong>🌐 Select Language / 選擇語言 / Выберите язык / اختر اللغة</strong>
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="docs/README_zh.md">中文</a> ·
  <a href="docs/README_es.md">Español</a> ·
  <a href="docs/README_ru.md">Русский</a> ·
  <a href="docs/README_ar.md">العربية</a>
</p>

---

<a name="english"></a>
## 🇬🇧 English

An OpenClaw skill that aggregates travel news, destination information, and reviews from multiple sources.

## Who Is This For?

Travel planning professionals, travel agents, tour operators, and travel content creators who need fast, comprehensive travel information from multiple sources.

### Features

- 🔍 **Multi-source search** — Tavily (required), Brave Search (optional), Browser scraping (optional)
- 🌐 **Multi-language** — Follows query language, switchable on demand
- 📄 **Multiple output formats** — Plain text, Word (docx), PDF (with CJK support)
- ⭐ **Review aggregation** — TripAdvisor and Google Maps ratings (ON by default, can be disabled)
- 🧹 **Deduplication** — Automatically removes duplicate results within each run
- 📅 **Time filtering** — 24h, week, month, year, or custom range

### Requirements

#### Required
- Python 3.10+
- `requests` package
- **Tavily API key** — Get free at [tavily.com](https://tavily.com)

#### Optional
- **Brave Search API key** — Get at [brave.com/search/api](https://brave.com/search/api)
- **Xvfb + Chromium + Puppeteer** — For scraping sites like Xiaohongshu and X/Twitter

### Installation

#### 1. Install Python dependencies

```bash
pip install requests fpdf2 python-docx
```

#### 2. Set up API keys

Create or edit `.env (in skill directory)`:

```bash
TAVILY_API_KEY=your_tavily_key_here
BRAVE_API_KEY=your_brave_key_here    # Optional
```

#### 3. (Optional) Install browser suite for blocked sites

The browser suite (三件套) uses three components:
- **Xvfb** — Virtual framebuffer that provides a fake display (default: 1200x720x24)
- **Chromium** — Browser engine
- **Puppeteer** (Node.js) — Controls Chromium programmatically

Why not just headless mode? Some websites detect and block headless browsers. Running Chromium on a virtual display makes it appear as a real browser.

```bash
# Install Xvfb and Chromium
apt-get install -y xvfb chromium

# Install Puppeteer
npm install puppeteer
```

**For advanced interactions** (simulated clicking, paginating results, clicking "load more" buttons), the `desktop-control` skill is required. It provides mouse/keyboard control and screen automation on the virtual display.

Install it from ClawHub:
```bash
npx clawhub install desktop-control
```
Learn more: https://clawhub.com/skills/desktop-control

### Usage

#### Basic search (plain text)

```bash
python scripts/search.py --query "Tokyo travel tips March 2026"
```

#### Generate PDF report

```bash
python scripts/search.py --query "京都賞櫻推薦景點" --format pdf --output kyoto_report.pdf
```

#### Generate Word document

```bash
python scripts/search.py --query "Bali best hotels 2026" --format docx --output bali_hotels.docx
```

#### Disable review aggregation

```bash
python scripts/search.py --query "Paris travel guide" --no_reviews
```

#### Filter by time range

```bash
# Last 24 hours
python scripts/search.py --query "travel news" --time_range pd

# Last week
python scripts/search.py --query "travel news" --time_range pw

# Last year
python scripts/search.py --query "travel news" --time_range py
```

#### Enable Brave Search fallback

```bash
python scripts/search.py --query "hidden gems Kyoto" --use_brave
```

#### Enable browser scraping for blocked sites

```bash
python scripts/search.py --query "小紅書東京旅遊推薦" --use_browser
```

#### Limit results

```bash
python scripts/search.py --query "Paris travel" --max_results 5
```

### Parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--query` | `-q` | *required* | Search query (any language) |
| `--time_range` | `-t` | `pm` | Time filter: `pd`(24h), `pw`(week), `pm`(month), `py`(year) |
| `--region` | `-r` | `ALL` | Region code: `ALL`, `US`, `CN`, `JP`, `TW`, etc. |
| `--max_results` | `-n` | `0` (unlimited) | Limit number of results |
| `--format` | `-f` | `text` | Output: `text`, `docx`, `pdf` |
| `--output` | `-o` | stdout | Output file path |
| `--use_brave` | | `false` | Enable Brave Search fallback |
| `--use_browser` | | `false` | Enable browser scraping |
| `--no_reviews` | | `false` | Disable review aggregation (ON by default) |
| `--language` | `-l` | auto | Output language (auto = follow query) |

### How It Works

```
User Query
    │
    ▼
┌─────────────┐
│  Tavily API  │  ← Required, always runs first
└──────┬──────┘
       │ Results insufficient?
       │ No + --use_brave?
       ▼
┌──────────────┐
│ Brave Search │  ← Optional fallback
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Browser Scrape   │  ← Optional, for blocked sites
│ (Xvfb+Chromium   │     (Xiaohongshu, X/Twitter)
│  +Puppeteer)     │
└──────┬───────────┘
       │
       ▼
┌─────────────┐
│ Deduplicate │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Output    │  text / docx / pdf
└─────────────┘
```

### License

MIT

---

<p align="center">
  <a href="#english">↑ Back to top</a> ·
  <a href="docs/README_zh.md">中文</a> ·
  <a href="docs/README_es.md">Español</a> ·
  <a href="docs/README_ru.md">Русский</a> ·
  <a href="docs/README_ar.md">العربية</a>
</p>

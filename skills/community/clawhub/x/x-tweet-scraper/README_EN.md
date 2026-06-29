# X.com Comprehensive Tweet Scraper

**Tags**: `#twitter-scraper` `#x-tweet-collector` `#playwright-automation` `#web-scraping` `#data-collection` `#social-media-analytics` `#x-api-scraping` `#browser-automation` `#tweet-archive` `#python-scraper`

---

## Overview
Three Playwright-based strategies for scraping public tweet history from X.com (Twitter) users. All use real browser environments to bypass anti-scraping protections. No `requests` library needed.

## Strategies

| Strategy | Coverage | Rate Limit | Use Case |
|----------|----------|-----------|----------|
| Auto-Search (Recommended) | ~2000+ | Low | Full collection |
| GraphQL API | ~900 | High | Fast latest fetch |
| DOM Scroll | ~1400 | Lowest | Profile browsing simulation |

## Prerequisites
- Python 3.10+, `pip install playwright`, `python -m playwright install chromium`
- Windows: `$env:PYTHONIOENCODING="utf-8"`
- Export X.com login cookies from browser (F12 → Application → Cookies → https://x.com → Export as JSON)
- Save cookies to `<username>_data/x_cookies.json`

## Installation
```bash
pip install playwright
python -m playwright install chromium
```

## Usage

### Auto-Search (Recommended)
Searches X.com by date-ranged queries, scrolls to collect all visible tweets. Handles rate limits, blank pages, and sparse months automatically.
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_auto.py --username target_user --seed existing_data.json
```

### GraphQL API
Direct GraphQL API calls through Playwright browser's fetch(). Limited to ~900 tweets due to X.com API pagination limit.
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_v9.py --username target_user --batch --pages 50 --seed data.json --auto-merge data.json
```

### DOM Scroll
Opens profile page and simulates human scrolling. Lowest rate limiting risk but slowest.
```powershell
$env:PYTHONIOENCODING="utf-8"
python -u scripts/scrape_x_scroll.py --username target_user --seed existing_data.json
```

## File Structure
```
x-scraper-comprehensive/
├── SKILL.md                    # Skill configuration with all details
├── README.md                   # Bilingual readme
├── README_EN.md                # English readme
├── scripts/
│   ├── scrape_x_auto.py        # Auto-search strategy
│   ├── scrape_x_v9.py          # GraphQL API strategy
│   └── scrape_x_scroll.py      # DOM scroll strategy
└── references/
    └── workflow.md             # End-to-end workflow documentation
```

## Known Issues & Fixes
See `SKILL.md` → "Known Issues" section for 7 documented pitfalls and their fixes, including:
- Login detection false positives
- Scroll blank page recovery
- Time field name inconsistency
- GraphQL API hard limit

## License
MIT

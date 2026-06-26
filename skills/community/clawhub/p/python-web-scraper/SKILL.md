---
name: web-scraper
description: Python web scraping toolkit for data extraction, pagination handling, anti-blocking techniques, Selenium for JavaScript-heavy sites, and structured output (JSON/CSV). Use when Codex needs to extract data from websites, handle pagination, bypass simple anti-bot measures, scrape JavaScript-rendered content, or process scraped data into usable formats.
---

# Web Scraper

## Overview

Python web scraping toolkit for data extraction, pagination handling, anti-blocking techniques, Selenium for JS-heavy sites, and structured output. Covers ethical scraping practices. Use when Codex needs to extract data from websites, handle pagination, bypass simple anti-bot measures, or scrape JavaScript-rendered content.

## Quick Start

### Prerequisites
```bash
pip install requests beautifulsoup4 lxml
# For JS-heavy sites:
pip install selenium webdriver-manager
```

### Basic scrape
```bash
# Extract all links from a page
python3 scripts/scrape-basic.py https://example.com \
  --selector "a[href]" --attr href --output links.json --pretty

# Extract text from articles
python3 scripts/scrape-basic.py https://news.ycombinator.com \
  --selector ".titleline a" --output hn.txt
```

### Paginated scrape
```bash
# URL parameter pagination (?page=1, ?page=2)
python3 scripts/scrape-pagination.py https://books.toscrape.com/catalogue/page-1.html \
  --selector "h3 a" --attr title --max-pages 5

# Next-link detection
python3 scripts/scrape-pagination.py https://quotes.toscrape.com \
  --selector "span.text" --max-pages 3
```

### JavaScript-rendered pages (Selenium)
```bash
python3 scripts/scrape-with-selenium.py https://example.com \
  --selector ".dynamic-content" --wait 5 --output data.json
```

## Common Scenarios

### Anti-blocking techniques

Rotate User-Agents and add delays to avoid 429/blocking:

```python
import random
import time
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
time.sleep(random.uniform(1.0, 3.0))  # random delay between requests
```

For aggressive blocking: set cookies, use sessions, or add proxy.

### Handle JavaScript sites without Selenium

First check: is the data embedded in the page source?
```python
import re, json
# Look for JSON data in <script> tags
match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', html)
if match:
    data = json.loads(match.group(1))
```

Many SPAs (React/Vue) embed data in script tags — Selenium may be unnecessary.

### Handle login-protected pages

```bash
# Option 1: Export cookies from browser
# In browser console: document.cookie or use EditThisCookie extension
# Option 2: Use requests Session
python3 -c "
import requests
s = requests.Session()
s.post('https://example.com/login', data={'user': '...', 'pass': '...'})
with open('cookies.txt', 'w') as f:
    f.write(str(s.cookies.get_dict()))
"
```

### Output formatting

Scripts output JSON by default. Convert to CSV:
```bash
# JSON → CSV using jq
python3 scrape-basic.py https://example.com -s "tr" -o data.json --pretty
python3 -c "
import json, csv
with open('data.json') as f:
    data = json.load(f)
with open('data.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['item'])
    for d in data:
        w.writerow([d])
"
```

## Ethics & Legal

- Always check `robots.txt` first: `https://example.com/robots.txt`
- Respect `Crawl-delay` directive
- Identify yourself in User-Agent with contact info
- Never scrape login-protected content, personal data, or copyrighted material
- Add delays (1-3s minimum) between requests — don't hammer servers
- Check ToS, some sites explicitly ban scraping
- For public data (news, blogs, directories): generally fine with proper rate limiting

## Resources

- **`scripts/scrape-basic.py`** — Single page scrape with CSS selectors, JSON/CSV/text output
- **`scripts/scrape-pagination.py`** — Paginated scrape (URL params + next-link detection)
- **`scripts/scrape-with-selenium.py`** — Selenium-based scrape for JS-heavy sites with scroll
- **`references/anti-blocking.md`** — Detailed anti-blocking and proxy strategies

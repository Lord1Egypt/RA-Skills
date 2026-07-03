---
name: web-crawler
description: |
  Use this skill whenever the user wants to create Python web crawlers/scrapers based on a given URL.
  Supports Vue, React, Next.js, Nuxt, Angular, Svelte and other frontend architectures by analyzing
  API calls, handling dynamic content with headless browsers. Main language is Python.
  Features:
    - Static & dynamic crawling (requests, httpx, playwright, selenium, drissionpage)
    - JS reverse engineering (webpack unpacking, AST analysis, hook injection)
    - Anti-bot bypass (Cloudflare, Akamai, reCAPTCHA, fingerprint spoofing)
    - Login & session management (cookie, JWT, OAuth, signature replay)
    - Encryption & signing (AES/RSA/MD5/SHA, custom signing algorithms)
    - Pagination strategies (page number, cursor, waterfall, infinite scroll)
    - Data export (CSV, XLSX, JSON, SQLite, MySQL, MongoDB, images, files)
    - Distributed crawling (Redis queue, Scrapy-Redis, task scheduling)
    - Anti-detection (UA rotation, proxy pool, fingerprint randomization, behavior simulation)
    - Compliance (robots.txt, rate limiting, terms of service, legal boundaries)
  Triggers: "写爬虫", "爬取", "抓取数据", "scraper", "crawler", "scrape", "spider",
            "Vue 爬虫", "React 爬虫", "动态网页", "反爬", "加密参数", "签名"
---

# Web Crawler Skill Guide

## When to Use
- User provides a URL and wants a Python crawler/scraper script.
- Scraping Vue/React/SPA/AJAX-driven sites, dynamic pages, JSON APIs.
- Handling JavaScript-rendered content, pagination, login, infinite scroll.
- Reverse engineering encrypted parameters, signatures, tokens.
- Bypassing anti-bot systems (Cloudflare, Akamai, reCAPTCHA, etc.).
- Need complete, runnable, production-grade Python script.

---

## Phase 1: Reconnaissance (站点侦察)

Before writing any code, analyze the target:

### 1.1 Network Analysis
- Open DevTools → Network tab → filter by `Fetch/XHR`
- Identify data API endpoints (often return JSON)
- Check request methods: GET / POST / PUT
- Inspect query params, body, headers, cookies
- Look for: `api.`, `/api/`, `/graphql`, `.json`, `ajax`, `json` patterns

### 1.2 Page Type Detection
| Type | Indicators | Strategy |
|------|-----------|----------|
| Static HTML | Server-rendered, full content in source | `requests` + `BeautifulSoup` |
| SPA (Vue/React) | Empty `<div id="app">`, JS bundles | Find API or use headless browser |
| SSR (Next.js/Nuxt) | Full HTML but hydrated | `requests` often works directly |
| API-driven | XHR returns JSON | Direct API requests (best case) |
| WebSocket | `ws://` connections, real-time data | `websockets` / `websocket-client` |
| Mobile-only | Different UA serves different content | Spoof mobile UA or use app API |

### 1.3 Anti-Bot Detection
- Check for Cloudflare (`cf-ray` header, challenge page)
- Akamai BMP (`_abck` cookie)
- reCAPTCHA / hCaptcha / Turnstile
- Device fingerprinting (`canvas`, `webgl`, `navigator` properties)
- Behavioral analysis (mouse movement, typing patterns)
- Use [https://bot.sannysoft.com](https://bot.sannysoft.com) to test headless detection

---

## Phase 2: Library Selection (技术选型)

### Decision Tree
```
Is there a clean JSON API?
├── Yes → requests / httpx (fastest, simplest)
└── No → Is content server-rendered?
    ├── Yes → requests + BeautifulSoup/lxml
    └── No → Need JS rendering?
        ├── Light JS → requests-html (pyppeteer backend)
        ├── Heavy JS / SPA → playwright (recommended) or selenium
        └── Need to bypass detection → DrissionPage / undetected-chromedriver
```

### Library Comparison
| Library | Speed | JS Support | Anti-Detection | Use Case |
|---------|-------|-----------|----------------|----------|
| `requests` | ⚡⚡⚡ | ❌ | ❌ | Static sites, APIs |
| `httpx` | ⚡⚡⚡ | ❌ | ❌ | Async API crawling |
| `requests-html` | ⚡⚡ | ✅ | ❌ | Light JS rendering |
| `playwright` | ⚡ | ✅✅ | ⚠️ | Modern SPAs, screenshots |
| `selenium` | ⚡ | ✅✅ | ⚠️ | Legacy, wide support |
| `DrissionPage` | ⚡⚡ | ✅✅ | ✅✅ | Anti-bot, Chinese sites |
| `undetected-chromedriver` | ⚡ | ✅✅ | ✅✅ | Cloudflare bypass |
| `scrapy` | ⚡⚡⚡ | ❌ | ❌ | Large-scale, pipelines |
| `pyppeteer` | ⚡ | ✅✅ | ⚠️ | Puppeteer port |

---

## Phase 3: Core Implementation Patterns

### 3.1 Static/API Crawling (requests)
```python
import requests
import pandas as pd
import time
import random

# Config
BASE_URL = "https://api.example.com/data"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://example.com/",
}
COOKIES = {"session": "xxx"}
PROXY = {"http": "http://proxy:8080", "https": "http://proxy:8080"}

def fetch_page(page=1):
    params = {"page": page, "size": 20}
    for attempt in range(3):
        try:
            resp = requests.get(BASE_URL, headers=HEADERS, params=params,
                                cookies=COOKIES, proxies=PROXY, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)
    return None

def crawl_all(max_pages=100):
    all_data = []
    for page in range(1, max_pages + 1):
        data = fetch_page(page)
        if not data or not data.get("items"):
            break
        all_data.extend(data["items"])
        print(f"Page {page}: {len(data['items'])} items")
        time.sleep(random.uniform(1, 3))  # Polite delay
    return all_data

if __name__ == "__main__":
    results = crawl_all()
    pd.DataFrame(results).to_csv("output.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(results)} records to output.csv")
```

### 3.2 Dynamic SPA Crawling (Playwright)
```python
from playwright.sync_api import sync_playwright
import pandas as pd
import time

def crawl_spa():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        page = context.new_page()

        # Intercept API responses (preferred over parsing DOM)
        api_data = []
        def handle_response(response):
            if "/api/list" in response.url and response.status == 200:
                try:
                    api_data.append(response.json())
                except:
                    pass
        page.on("response", handle_response)

        page.goto("https://example.com/list", wait_until="networkidle")

        # Infinite scroll
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        browser.close()
        return api_data

if __name__ == "__main__":
    data = crawl_spa()
    pd.DataFrame(data).to_excel("output.xlsx", index=False)
```

### 3.3 Anti-Detection Crawling (DrissionPage)
```python
from DrissionPage import ChromiumPage, ChromiumOptions
import time

def crawl_stealth():
    co = ChromiumOptions()
    co.set_argument("--no-sandbox")
    co.set_argument("--disable-blink-features=AutomationControlled")
    co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    page = ChromiumPage(co)
    page.get("https://example.com")

    # DrissionPage bypasses many fingerprint checks automatically
    items = page.eles('css:.item-class')
    results = []
    for item in items:
        results.append({
            "title": item.ele('css:.title').text,
            "link": item.ele('css:a').attr('href'),
            "price": item.ele('css:.price').text,
        })

    page.quit()
    return results
```

### 3.4 Scrapy Framework (Large-Scale)
```python
# spider.py
import scrapy
from scrapy.crawler import CrawlerProcess

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com/page/1"]

    def parse(self, response):
        for item in response.css(".item"):
            yield {
                "title": item.css(".title::text").get(),
                "url": item.css("a::attr(href)").get(),
            }
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

# Run
process = CrawlerProcess(settings={
    "FEEDS": {"output.json": {"format": "json"}},
    "USER_AGENT": "Mozilla/5.0",
    "DOWNLOAD_DELAY": 2,
    "AUTOTHROTTLE_ENABLED": True,
})
process.crawl(ExampleSpider)
process.start()
```

---

## Phase 4: Advanced Techniques (高级技术)

### 4.1 JS Reverse Engineering (JS逆向)
When parameters are encrypted/signed:

1. **Locate the encryption function**: Search source for param name, set breakpoints
2. **Common patterns**:
   - `sign: md5(timestamp + secret + params)`
   - `token: base64(aes_encrypt(data, key))`
   - Custom webpack modules
3. **Tools**: Chrome DevTools, Fiddler, Charles, mitmproxy, PyExecJS, Node.js subprocess
4. **Approaches**:
   - **Replay**: Extract algorithm and reimplement in Python
   - **ExecJS**: Run obfuscated JS directly via `execjs` or `node` subprocess
   - **Hook injection**: Override functions to dump intermediate values

```python
# Example: calling JS encryption from Python
import execjs

ctx = execjs.compile("""
function sign(params, timestamp, secret) {
    // ... extracted from target site
    return CryptoJS.MD5(timestamp + secret + JSON.stringify(params)).toString();
}
""")
signature = ctx.call("sign", {"page": 1}, "1700000000", "secret_key")
```

### 4.2 Login & Session Management
| Method | Implementation |
|--------|---------------|
| Cookie | `requests.Session()`, persist cookies |
| JWT | Store token, add to `Authorization: Bearer` header |
| OAuth | Follow authorization code flow |
| Signed requests | Reproduce signature algorithm |
| QR Login | Poll scan status API |
| SMS/Email OTP | Manual input or OCR |

```python
import requests

session = requests.Session()
# Login
login_resp = session.post("https://example.com/api/login",
                           json={"username": "user", "password": "pwd"})
# Session maintains cookies automatically
data = session.get("https://example.com/api/protected").json()
```

### 4.3 Pagination Strategies
| Type | Detection | Implementation |
|------|-----------|----------------|
| Page number | `?page=1` | Loop incrementing page |
| Cursor/Offset | `?cursor=abc` or `?offset=20` | Use returned cursor |
| Waterfall | POST with timestamp/last_id | Use last item's id |
| Infinite scroll | Scroll event triggers XHR | Playwright scroll loop |
| Next link | `rel="next"` or `next_page` field | Follow links |

### 4.4 Proxy & Fingerprint Rotation
```python
import random
import requests
from fake_useragent import UserAgent

ua = UserAgent()
PROXIES = [
    "http://user:pass@proxy1:8080",
    "http://user:pass@proxy2:8080",
]

def fetch(url):
    headers = {"User-Agent": ua.random}
    proxy = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}
    return requests.get(url, headers=headers, proxies=proxy, timeout=10)
```

### 4.5 Captcha Handling
| Type | Solution |
|------|----------|
| Image captcha | OCR (ddddocr, Tesseract) |
| Slider captcha | Track trajectory, simulate human movement |
| reCAPTCHA v2 | 2Captcha / AntiCaptcha API, or audio challenge |
| reCAPTCHA v3 | Need high trust score (aged account, good behavior) |
| hCaptcha | 2Captcha, or ML model |
| Cloudflare Turnstile | Use undetected-chromedriver or FlareSolverr |
| GeeTest | Analyze gap distance, simulate drag with acceleration |

---

## Phase 5: Data Storage (数据存储)

### 5.1 Storage Options
| Format | Library | Best For |
|--------|---------|----------|
| CSV | `pandas` / `csv` | Tabular data, Excel compat |
| XLSX | `openpyxl` / `pandas` | Multi-sheet, formatting |
| JSON | `json` / `orjson` | Nested/structured data |
| SQLite | `sqlite3` | Local DB, querying |
| MySQL | `pymysql` / `sqlalchemy` | Production DB |
| MongoDB | `pymongo` | Unstructured, flexible schema |
| Images | `requests` + `open()` | Download to folder |
| Files | `urllib` / `aiohttp` | PDFs, docs, media |

### 5.2 Image Download Pattern
```python
import os
import requests
from pathlib import Path

def download_images(urls, folder="images"):
    Path(folder).mkdir(exist_ok=True)
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=10)
            ext = url.split(".")[-1][:4]  # crude extension detection
            filename = f"{folder}/img_{i:04d}.{ext}"
            with open(filename, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"Failed {url}: {e}")
```

### 5.3 Database Pattern
```python
import sqlite3

conn = sqlite3.connect("data.db")
conn.execute("""CREATE TABLE IF NOT EXISTS items
                (id INTEGER PRIMARY KEY, title TEXT, url TEXT, price REAL)""")

def save(item):
    conn.execute("INSERT OR IGNORE INTO items (title, url, price) VALUES (?,?,?)",
                 (item["title"], item["url"], item.get("price")))
    conn.commit()
```

---

## Phase 6: Distributed & Scaled Crawling (分布式)

### 6.1 Scrapy-Redis (Distributed Scrapy)
```python
# settings.py
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = "redis://localhost:6379/0"
```

### 6.2 Custom Redis Queue
```python
import redis
import json

r = redis.Redis()
QUEUE = "crawl:urls"

def push_urls(urls):
    for url in urls:
        r.lpush(QUEUE, json.dumps({"url": url, "retry": 0}))

def pop_url():
    return json.loads(r.brpop(QUEUE)[1])
```

### 6.3 Async Crawling (asyncio + aiohttp)
```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def crawl(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

results = asyncio.run(crawl(url_list))
```

---

## Phase 7: Anti-Detection Best Practices (反反爬)

### 7.1 Request Level
- Rotate User-Agent (`fake-useragent` library)
- Random delays: `time.sleep(random.uniform(1, 5))`
- Respect `Retry-After` header
- Use residential proxies (datacenter IPs get blocked)
- Rotate cookies/sessions per batch

### 7.2 Browser Level
- `undetected-chromedriver` or `DrissionPage` for fingerprint spoofing
- Set realistic viewport, locale, timezone
- Disable `webdriver` flag: `navigator.webdriver = undefined`
- Mock `canvas`/`webgl` fingerprints
- Simulate human behavior: mouse movement, scroll, random clicks

### 7.3 Behavioral
- Don't crawl too fast — match human browsing speed
- Visit unrelated pages occasionally (decoy requests)
- Use realistic referer chains
- Handle 403/429 gracefully with exponential backoff

---

## Phase 8: Compliance & Ethics (合规与道德)

### 8.1 Legal Considerations
- **Always check `robots.txt`** — respect disallow rules
- Review Terms of Service — some prohibit scraping
- Personal data: comply with GDPR / PIPL (China's 个人信息保护法)
- Copyright: don't republish copyrighted content
- Rate limits: don't overload target servers

### 8.2 Ethical Guidelines
- Identify your crawler in UA when appropriate
- Crawl during off-peak hours
- Cache responses to avoid redundant requests
- Only collect what you need
- Consider asking for API access first

---

## Phase 9: Interactive Workflow (交互流程)

When user requests a crawler, follow this dialogue:

### Step 1: Clarify Requirements
Ask the user (only if not provided):
1. **Target URL** — specific page or entire site?
2. **Data fields** — what to extract? (title, price, images, full text?)
3. **Scope** — how many pages/items?
4. **Login required?** — if yes, credentials or existing cookies?
5. **Output format** — CSV / XLSX / JSON / DB / images?
6. **Anti-bot observed?** — Cloudflare, captcha, etc.?
7. **Frequency** — one-time or scheduled/recurring?
8. **Environment** — local machine, server, cloud?

### Step 2: Analyze & Recommend
- Based on URL, recommend the best approach (API vs. browser)
- List required libraries with `pip install` commands
- Warn about potential anti-bot challenges
- Estimate complexity and time

### Step 3: Generate Script
- Complete, runnable Python script
- Configuration section at top (URL, headers, output path)
- Modular functions: `fetch()`, `parse()`, `save()`, `main()`
- Error handling with retries
- Progress logging
- Comments explaining non-obvious logic
- Type hints for clarity

### Step 4: Usage Instructions
- `pip install` commands for all dependencies
- How to run: `python crawler.py`
- Configuration changes needed
- Output location and format
- Troubleshooting common issues

### Step 5: Offer Enhancements
- Add proxy support
- Add scheduling (cron / APScheduler)
- Add monitoring/alerting
- Convert to Scrapy project for scale
- Add data cleaning/processing pipeline

---

## Phase 10: Output Template (输出模板)

Every generated script should follow this structure:

```python
"""
Crawler: [Site Name]
Description: [What it crawls]
Author: Generated by Aura
Date: [auto]
Dependencies: pip install requests beautifulsoup4 pandas
"""

import os
import sys
import time
import random
import logging
from pathlib import Path

# ===== Configuration =====
TARGET_URL = "https://example.com"
OUTPUT_DIR = Path("./output")
OUTPUT_FORMAT = "csv"  # csv / xlsx / json / sqlite
MAX_PAGES = 100
DELAY_RANGE = (1, 3)  # random delay between requests
TIMEOUT = 15
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "text/html,application/xhtml+xml,...",
}

# ===== Logging =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(OUTPUT_DIR / "crawler.log", encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

# ===== Core Functions =====
def fetch(url, **kwargs):
    """Fetch a single URL with retry logic."""
    ...

def parse(html):
    """Parse HTML/JSON and extract target data."""
    ...

def save(data):
    """Save extracted data to configured output."""
    ...

def main():
    """Main entry point."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    # ... crawl logic
    logger.info(f"Crawling complete. {len(results)} items saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
```

---

## Quick Reference (速查表)

### Common Selectors
| Need | CSS Selector | XPath |
|------|-------------|-------|
| Class | `.classname` | `//*[@class="classname"]` |
| ID | `#idname` | `//*[@id="idname"]` |
| Attribute | `[href]` | `//*[@href]` |
| Text contains | `:contains("text")` | `//div[contains(text(), "text")]` |
| Nth child | `:nth-child(n)` | `//div[n]` |
| Direct child | `> .child` | `/div/a` |

### Common Headers for Anti-Detection
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}
```

### Installation Commands
```bash
# Basic
pip install requests beautifulsoup4 lxml pandas openpyxl

# Dynamic
pip install playwright
playwright install chromium

# Anti-detection
pip install DrissionPage undetected-chromedriver fake-useragent

# Framework
pip install scrapy scrapy-redis

# Async
pip install aiohttp httpx

# JS execution
pip install PyExecJS
# Node.js required for PyExecJS

# Image processing
pip install Pillow

# OCR
pip install ddddocr  # Chinese captcha OCR
```

---

## Error Handling Patterns

```python
# Retry with exponential backoff
import time

def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
            elif resp.status_code == 403:
                logger.error("Forbidden — may need cookies/proxy")
                break
            else:
                resp.raise_for_status()
        except requests.RequestException as e:
            wait = 2 ** attempt
            logger.warning(f"Attempt {attempt+1} failed: {e}, retry in {wait}s")
            time.sleep(wait)
    return None
```

---

This skill ensures every generated crawler is robust, production-ready, anti-detection-aware,
and tailored to modern web architectures (Vue/React/SPA/SSR/API).

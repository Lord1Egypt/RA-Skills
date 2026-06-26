---
name: scrapling
description: Use this skill whenever the user asks to scrape a website, extract structured data from web pages, handle anti-bot/Cloudflare pages, crawl multiple pages, or explicitly mentions Scrapling. This skill provides a practical Scrapling workflow (install, fetcher selection, extraction, and crawl patterns) for reliable Python web scraping.
---

# Scrapling Web Scraping Skill

## Goal

Use Scrapling to extract web data with minimal selector breakage and better anti-bot resilience.

Prefer this skill when users ask for:

- website scraping
- data extraction from HTML pages
- Cloudflare/anti-bot resistant scraping
- multi-page crawling
- converting scraping tasks into reusable Python scripts

## Safety and Legality

Before scraping, always:

1. Confirm the target is allowed by user intent and local laws.
2. Avoid unauthorized access, login bypass, or private data scraping.
3. Respect target website terms and reasonable request rates.
4. For high-volume jobs, add delays and domain-level throttling.

## Default Environment (this machine)

All dependencies should live under `D:\clawtest`.

Recommended setup commands:

```powershell
python -m venv D:\clawtest\.venv
D:\clawtest\.venv\Scripts\python -m pip install -U pip
D:\clawtest\.venv\Scripts\python -m pip install "scrapling[fetchers]"
D:\clawtest\.venv\Scripts\scrapling install
```

Notes:

- If the task is simple static HTML extraction, `pip install scrapling` is enough.
- `scrapling install` is needed for browser-based fetchers.

## Fetcher Selection Guide

Choose the lightest option that works:

1. `Fetcher`:
   - Best for static pages and speed.
2. `StealthyFetcher`:
   - Best default when anti-bot checks likely exist.
3. `DynamicFetcher`:
   - Use when data is rendered by JavaScript.
4. `Spider`:
   - Use for multi-page crawl, queueing, concurrency, and structured export.

## Standard Workflow

1. Identify target fields and output schema first.
2. Pick fetcher (`Fetcher` -> `StealthyFetcher` -> `DynamicFetcher` escalation).
3. Extract with CSS/XPath and normalize into JSON-friendly fields.
4. Save data to JSON/JSONL/CSV.
5. Add retry, timeout, and polite delays for production.

## Code Templates

### 1) Single Page Extraction (Stealthy default)

```python
from scrapling.fetchers import StealthyFetcher

StealthyFetcher.adaptive = True
url = "https://example.com/products"
page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=45000)

items = []
for card in page.css(".product-card", auto_save=True):
    items.append({
        "title": card.css("h2::text").get(default="").strip(),
        "price": card.css(".price::text").get(default="").strip(),
        "url": card.css("a::attr(href)").get(default="")
    })

print(items)
```

### 2) Adaptive Re-location for changed layouts

```python
# First run stores fingerprints:
products = page.css(".product-card", auto_save=True)

# Future run can recover after layout drift:
products = page.css(".product-card", adaptive=True)
```

### 3) Spider Crawl Skeleton

```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "product_spider"
    start_urls = ["https://example.com/catalog"]

    async def parse(self, response: Response):
        for card in response.css(".product-card"):
            yield {
                "title": card.css("h2::text").get(default="").strip(),
                "price": card.css(".price::text").get(default="").strip(),
            }

        for href in response.css("a.next::attr(href)").all():
            yield response.follow(href, callback=self.parse)

if __name__ == "__main__":
    ProductSpider().start()
```

## Expected Assistant Output Format

When executing a user task with this skill, respond with:

1. chosen fetcher/spider strategy and why
2. runnable script (or patch) tailored to target site
3. exact install/run commands for current machine
4. output path and data schema
5. anti-bot reliability notes and fallback plan

## Practical Fallback Order

If extraction fails:

1. Validate selectors on fresh HTML.
2. Switch `Fetcher` -> `StealthyFetcher`.
3. Switch to `DynamicFetcher` for JS-rendered content.
4. Add adaptive selectors (`auto_save=True` then `adaptive=True`).
5. Add retries, backoff, and lower request rate.

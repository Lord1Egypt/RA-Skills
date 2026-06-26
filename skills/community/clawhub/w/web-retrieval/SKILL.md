---
name: web-retrieval
description: >
  Expert web fetching and crawling using Scrapling. Use for any web_fetch task,
  JS-rendered pages, anti-bot sites, bulk URL fetching, or site crawling.
  Preferred over web_fetch tool for all URL retrieval. Supports static GET,
  browser automation (DynamicFetcher), and stealth mode (StealthyFetcher).
  Also handles multi-URL crawls and site spiders with checkpoint/resume.
metadata: {"openclaw": {"emoji": "🕷️", "skillKey": "web-retrieval"}}
---

# Web Retrieval — Scrapling Expert

Local web fetching via Scrapling. Three fetchers, two scripts, one job: get the page content reliably.

## Fetcher Selection Guide

**Always start with the cheapest fetcher that works. Escalate only if needed.**

| Fetcher | CLI mode | Speed | Use when |
|---------|----------|-------|----------|
| `Fetcher` (curl_cffi) | `get` | Fast (~1s) | Static HTML, APIs, most public pages. Impersonates Chrome. |
| `DynamicFetcher` | `fetch` | Medium (~5s) | JS-rendered pages, SPAs, pages that need browser execution |
| `StealthyFetcher` | `stealthy` | Slow (~10s) | Cloudflare, heavy anti-bot, fingerprint detection |

**Decision tree:**
1. Try `get` first — it handles 80% of pages
2. If content is just a title or empty → escalate to `fetch`
3. If blocked/Cloudflare detected → escalate to `stealthy`
4. If still blocked → add `--solve-cloudflare` and/or `--wait 3000`

## Fetch Script

```bash
FETCH="python3 $SKILL_DIR/scripts/fetch"

# Basic fetch (auto-escalates through modes)
$FETCH https://example.com

# Force specific mode
$FETCH https://example.com --mode stealthy

# Extract specific content with CSS selector
$FETCH https://example.com -s "article.main-content"

# Wait for JS-rendered content
$FETCH https://spa.example.com --mode fetch --wait 3000 --wait-selector ".content"

# Save to file
$FETCH https://example.com /tmp/output.md

# Plain text output
$FETCH https://example.com --text

# Raw HTML (for link extraction, parsing)
$FETCH https://example.com --html

# Cloudflare bypass
$FETCH https://protected.example.com --mode stealthy --solve-cloudflare

# Fast (no images/fonts/media)
$FETCH https://example.com --no-resources

# Network idle wait (good for dashboards)
$FETCH https://example.com --mode fetch --network-idle
```

## Crawl Script

```bash
CRAWL="python3 $SKILL_DIR/scripts/crawl"

# Fetch a flat list of URLs from file → one .md per URL in output dir
$CRAWL --urls-file /tmp/urls.txt --output-dir /tmp/results/

# Fetch list → single JSON file
$CRAWL --urls-file /tmp/urls.txt --output-json /tmp/results.json

# Crawl a site 2 levels deep (same domain only)
$CRAWL https://docs.example.com --depth 2 --output-dir /tmp/docs/

# Spider with checkpoint (resume if interrupted)
$CRAWL https://large-site.com --depth 3 --checkpoint-dir /tmp/checkpoint/

# Crawl with URL filter (only pages matching pattern)
$CRAWL https://docs.openclaw.ai --depth 2 --allowed-pattern "/docs/" --output-dir /tmp/

# Use stealth mode for crawl
$CRAWL --urls-file /tmp/urls.txt --mode stealthy --output-json /tmp/out.json
```

## Python API (for sub-agents / scripts)

```python
from scrapling import Fetcher, StealthyFetcher, DynamicFetcher

# Static fetch with browser impersonation
page = Fetcher().get("https://example.com", stealthy_headers=True)
text = page.get_all_text(ignore_tags=("script", "style"))
links = [a.attrib.get("href") for a in page.css("a[href]")]
title = page.css_first("h1").text

# Dynamic (JS-rendered)
async with DynamicFetcher() as f:
    page = await f.async_fetch("https://spa.example.com")

# Stealthy
page = StealthyFetcher().fetch("https://cloudflare-site.com", wait=2000)

# CSS selector extraction
results = page.css("div.article-body p")  # returns list of elements
first = page.css_first("h1").text

# Response properties
page.status  # HTTP status
page.url     # final URL (after redirects)
page.html    # raw HTML string
page.find("div", {"class": "content"})  # BeautifulSoup-style
```

## Scrapling Spider (site crawl with full control)

```python
from scrapling.spiders import Spider, Request
from scrapling import Fetcher

class DocsCrawler(Spider):
    start_urls = ["https://docs.example.com"]

    async def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    async def parse(self, response):
        # Yield scraped data
        yield {
            "url": response.url,
            "title": response.css_first("h1").text if response.css_first("h1") else "",
            "body": response.get_all_text(ignore_tags=("script", "style")),
        }
        # Follow links
        for link in response.css("a[href]"):
            href = link.attrib.get("href", "")
            if href.startswith("/") or "docs.example.com" in href:
                yield Request(response.urljoin(href), callback=self.parse)

# Run (checkpoint-enabled)
spider = DocsCrawler(crawldir="/tmp/crawl-checkpoint/")
result = spider.start()
print(f"Scraped {result.stats.items_scraped} pages")
items = list(result.items)
```

## Key Scrapling CSS/Response Methods

| Method | Description |
|--------|-------------|
| `page.css("selector")` | All matching elements |
| `page.css_first("selector")` | First match or None |
| `el.text` | Text content of element |
| `el.attrib["href"]` | Attribute value |
| `page.get_all_text()` | Full page text (strips scripts/styles) |
| `page.html` | Raw HTML |
| `page.find(tag, attrs)` | BeautifulSoup-style find |
| `page.urljoin(href)` | Resolve relative URL |
| `response.url` | Final URL after redirects |
| `response.status` | HTTP status code |

## Output Formats

All CLI commands support three output formats via file extension:
- `.md` — Markdown (default, best for LLM consumption)
- `.txt` — Plain text
- `.html` — Raw HTML (use for link extraction or further parsing)

## Tips

- **JS pages with lazy loading**: use `--wait 2000` + `--network-idle`
- **Dynamic content**: `--wait-selector ".target-class"` waits until element appears
- **Rate limiting**: add `--wait 1000` between requests in crawl mode
- **Cloudflare 403/503**: `--mode stealthy --solve-cloudflare`
- **Missing content**: try `--mode fetch --network-idle` before escalating to stealthy
- **CSS selectors**: use for targeted extraction to reduce noise in output
- **Deep research crawls**: use `--checkpoint-dir` so crawl survives interruption

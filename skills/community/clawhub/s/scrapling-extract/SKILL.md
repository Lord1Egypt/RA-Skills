---
name: scrapling
description: Web scraping and data extraction using the Python Scrapling library. Use to scrape static HTML pages, JavaScript-rendered pages (Playwright), and anti-bot or Cloudflare-protected sites (stealth browser). Supports CSS selectors, XPath, adaptive DOM relocation so selectors survive site redesigns, session-based scraping with cookie persistence, and outputs to JSON or Markdown. Use when asked to scrape a URL, extract text/links/tables/prices from a webpage, crawl a site, or automate web data collection.
---

# Scrapling

Extract structured website data with resilient selection patterns, adaptive relocation, and the right Scrapling fetcher mode for each target.

## Workflow

1. Identify target type before writing code:
   - Use `Fetcher` for static pages and API-like HTML responses.
   - Use `DynamicFetcher` when JavaScript rendering is required.
   - Use `StealthyFetcher` when anti-bot protection or browser fingerprinting issues are likely.
2. Choose output contract first:
   - Return JSON for pipelines/automation.
   - Return Markdown/text for summarization or RAG ingestion.
   - Keep stable field names even if selector strategy changes.
3. Implement selectors in this order:
   - Start with CSS selectors and pseudo-elements (for example `::text`, `::attr(href)`).
   - Fall back to XPath for ambiguous DOM structure.
   - Enable adaptive relocation for brittle or changing pages.
4. Add safety controls:
   - Respect target site terms and legal boundaries.
   - Add timeouts, retries, and explicit error handling.
   - Log status code, URL, and selector misses for debugging.
5. Validate on at least 2 pages:
   - Test one happy path and one edge case page.
   - Confirm required fields are non-empty.
   - Keep extraction deterministic (no hidden random choices).

## Quick Setup

1. Install base package:
   - `pip install scrapling`
2. Install fetchers when browser-based fetching is needed:
   - `pip install "scrapling[fetchers]"`
   - `scrapling install`
   - `python3 -m playwright install` (required for DynamicFetcher and StealthyFetcher)
3. Install optional extras as needed:
   - `pip install "scrapling[shell]"` for shell + `extract` commands
   - `pip install "scrapling[ai]"` for MCP capabilities

## Execution Patterns

### Pattern: One-off terminal extraction

Use Scrapling CLI for fastest no-code extraction:

```bash
scrapling extract get "https://example.com" content.md --css-selector "main"
```

### Pattern: Python extraction script

Use the bundled helper:

```bash
# Static page (default)
python scripts/extract_with_scrapling.py --url "https://example.com" --css "h1::text"

# JavaScript-rendered page
python scripts/extract_with_scrapling.py --url "https://example.com" --fetcher dynamic --css "h1::text"

# Anti-bot protected page
python scripts/extract_with_scrapling.py --url "https://example.com" --fetcher stealthy --css "h1::text"
```

### Pattern: Session-based scraping

Use session classes when cookies/state must persist across requests.

```python
from scrapling.fetchers import FetcherSession

session = FetcherSession()
login_page = session.post("https://example.com/login", data={"user": "...", "pass": "..."})
protected_page = session.get("https://example.com/dashboard")
headline = protected_page.css_first("h1::text")
```

Use `StealthySession` or `DynamicSession` as drop-in replacements for anti-bot or JS-rendered targets.

### Pattern: DOM change resilience

Use `auto_save=True` on initial capture and retry with adaptive selection on later runs when selectors break.

```python
from scrapling.fetchers import Fetcher

# First run: saves DOM snapshot so adaptive relocation can work later
page = Fetcher.auto_match("https://example.com", auto_save=True, disable_adaptive=False)
price = page.css_first(".price::text")

# Later runs: automatically relocates the selector even if the DOM changed
page = Fetcher.auto_match("https://example.com", auto_save=False, disable_adaptive=False)
price = page.css_first(".price::text")
```

## References

- Use [scrapling-reference.md](references/scrapling-reference.md) for fetcher/API examples and selector patterns.
- Use [extract_with_scrapling.py](scripts/extract_with_scrapling.py) for a reusable CLI script template.

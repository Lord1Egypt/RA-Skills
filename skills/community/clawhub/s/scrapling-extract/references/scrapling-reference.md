# Scrapling Reference

## Core Objects

- `Adaptor`: Parse HTML and query with CSS/XPath.
- `Fetcher`: Fetch and parse static pages.
- `DynamicFetcher`: Render JavaScript pages.
- `StealthyFetcher`: Use stealth browser behavior for anti-bot-heavy targets.
- `FetcherSession` / `StealthySession` / `DynamicSession`: Persist cookies and state across requests.

## Minimal Patterns

### Parse local HTML

```python
from scrapling import Adaptor

page = Adaptor("<div><h1>Title</h1></div>", url="https://example.com")
title = page.css_first("h1::text")
```

### Fetch page then select

```python
from scrapling.fetchers import Fetcher

page = Fetcher.auto_match(
    "https://example.com",
    auto_save=True,
    disable_adaptive=False,
)
headline = page.css_first("h1::text")
```

### Run CLI extraction

```bash
scrapling extract get "https://example.com" out.md --css-selector "main"
```

## Selector Tips

- Prefer CSS for readability and maintenance.
- Use pseudo-elements for direct value extraction:
  - `a::attr(href)`
  - `h1::text`
- Use XPath for complex relationships only when CSS is insufficient.
- Keep a fallback selector list for fragile layouts.

## Reliability Checklist

- Add timeout + retry logic around network calls.
- Check for empty selectors and fail clearly.
- Capture URL/status/error in logs.
- Validate extraction schema against expected keys before returning results.

## Typical Skill Triggers

- "Scrape this site into JSON."
- "Extract all product cards and prices."
- "Handle pagination with anti-bot defenses."
- "Build a reusable Scrapling scraping script."

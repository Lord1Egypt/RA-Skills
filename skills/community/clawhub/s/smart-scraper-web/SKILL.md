---
name: web-data-extractor
description: Extract structured data from websites. Tables, lists, prices, articles, metadata. HTML parsing with caching. Zero external dependencies.
capabilities:
  - network: outbound http/https to public hosts (SSRF-protected)
  - cache: stores fetched pages locally (disabled by default, --cache to enable)
  - user-consent: caching requires explicit --cache flag
---

# Web Data Extractor 🕷️

> ⚠️ **Security Note** — This skill **sends user-provided URLs over the network** and **stores fetched page contents locally in a cache** (`memory/scraper-cache/cache.json`). All URLs (including redirect targets) are validated against an SSRF blocklist. Do not use with sensitive, authenticated, or internal URLs. Clear the cache (`rm memory/scraper-cache/cache.json`) after scraping if page contents may be sensitive.

**Stop copying data by hand. Start extracting it automatically.**

## The Problem

Web content is everywhere but inaccessible to agents. `web_fetch` gets raw HTML, but you need structure — tables, prices, lists, article text — to make it useful.

Smart Scraper turns raw HTML into structured data with one command.

## Quick Start

### Extract everything from a page

```bash
node skills/smart-scraper/smart-scraper.js --extract https://example.com
```

Returns title, headings, paragraphs, links, tables, lists, prices, images, and metadata.

### Extract tables only

```bash
node skills/smart-scraper/smart-scraper.js --extract --table https://example.com/pricing
```

### Extract lists only

```bash
node skills/smart-scraper/smart-scraper.js --extract --list https://example.com/blog
```

### Extract prices

```bash
node skills/smart-scraper/smart-scraper.js --extract --price https://example.com/products
```

### Extract article content

```bash
node skills/smart-scraper/smart-scraper.js --extract --article https://example.com/blog/post
```

### Parse raw HTML

```bash
node skills/smart-scraper/smart-scraper.js --parse "<html>...</html>"
```

### Status overview

```bash
node skills/smart-scraper/smart-scraper.js --status
```

### Watch for content changes

```bash
# Capture baseline (first run)
node skills/smart-scraper/smart-scraper.js --watch https://example.com/pricing

# Check for changes (second run)
node skills/smart-scraper/smart-scraper.js --watch https://example.com/pricing

# Cron integration (exit 1 on change)
node skills/smart-scraper/smart-scraper.js --watch https://example.com/pricing --alert-on-change
```

Stores structured snapshots and diffs prices, headings, lists, and links between runs.

## Features

### HTML Parsing

- Title extraction
- Heading hierarchy (h1-h6)
- Paragraph extraction (filters short fragments)
- Link extraction with text
- Image extraction with alt text
- Metadata/meta tag extraction

### Table Extraction

- Full table structure with rows and cells
- Handles th and td elements
- Strips nested HTML from cells

### List Extraction

- Both ordered and unordered lists
- List item text extraction
- Preserves list structure

### Price Detection

- Matches USD ($), EUR (€), GBP (£), JPY (¥) formats
- Handles comma-separated thousands (e.g., $1,234.56)
- Returns raw price strings

### Article Mode

- Focuses on heading + paragraph structure
- Shows first 5 paragraphs as preview
- Ideal for blog posts and documentation

### Caching

- 5-minute TTL on fetched pages
- LRU eviction: max 50 entries or 10MB
- Reduces redundant network calls
- Cache stats via `--status`
- **Caching is disabled by default.** Use `--cache` to enable it.
- **Privacy notice**: Cached data may contain sensitive content (article text, metadata, links, prices, etc.). Clear cache after scraping sensitive pages (`rm memory/scraper-cache/cache.json`).

### Change Monitoring

- `--watch <url>` captures baseline on first run, diffs on subsequent runs
- Compares prices, headings, lists, and links between scrapes
- `--alert-on-change` exits with code 1 when changes detected (cron integration)
- `--diff-only` shows only the diff output
- Snapshots stored in `memory/scraper-cache/diffs/` — **watch mode persists data to disk without additional warning**. Use `--no-cache` to suppress cache writes during watch mode.

### Privacy

- **`--no-cache`** — Extract without storing any data locally (privacy mode)
- **`--cache`** — Enable caching of scraped content locally (disabled by default)
- Cached files may contain sensitive page content — clear cache after scraping sensitive pages
- Cache location: `memory/scraper-cache/cache.json` (or `--dir` to override)

## Configuration

Cache stored in: `memory/scraper-cache/cache.json`

Override data directory:
```bash
--dir /path/to/data
```

Privacy mode (no local storage):
```bash
--extract --no-cache https://example.com
```

## Security

- **URL validation** — only http/https to public hosts; blocks file://, gopher://, data:, localhost, private IPs, cloud metadata endpoints
- **Redirect validation** — each redirect target is re-validated against the same SSRF blocklist; attacker-controlled URLs cannot redirect to internal services
- **Redirect limit** — max 5 redirects to prevent loops and SSRF
- **Rate limiting** — 100ms minimum between requests
- **Bounded regex** — all patterns have `{0,N}` limits to prevent ReDoS
- **Cache eviction** — LRU with 50-entry / 10MB limits
- **No eval, no execSync, no command injection** — pure parsing, no shell interaction

## Agent Protocol

When extracting web content:

1. **Extract everything first** — `--extract <url>` for a full overview
2. **Target specific data** — `--extract --table/list/price/article` for focused extraction
3. **Parse raw HTML** — `--parse` when you already have HTML from another tool
4. **Check cache** — `--status` to monitor cache usage
5. **Combine with API Gateway** — Use API Gateway for authenticated or rate-limited sites

## Limitations

- Regex-based HTML parsing (not a full DOM parser)
- No JavaScript execution (SPA content not supported)
- Basic price detection (regex-based, not ML)
- 15-second fetch timeout per page
- Only http/https URLs to **public** hosts (no file://, localhost, private IPs, cloud metadata)
- Max 5 redirects per request
- Rate limited to 1 request per 100ms

## Comparison

| Tool | Structure | Tables | Prices | Articles | Caching |
|------|-----------|--------|--------|----------|---------|
| `web_fetch` | Raw HTML | ❌ | ❌ | ❌ | ❌ |
| Puppeteer | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Smart Scraper** | **✅** | **✅** | **✅** | **✅** | **✅** |

**Smart Scraper gives you structured extraction + caching with zero dependencies.**

> ⚠️ **Note**: The above comparison is feature-based, not live output. Example URLs in this doc use `example.com` (IANA placeholder) for illustration only — always test against your actual target.

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js http/https, no npm packages
3. **Structured output** — Returns parsed data, not raw HTML
4. **Cached** — Reduces redundant fetches automatically
5. **Multi-mode** — Extract everything or target specific data types

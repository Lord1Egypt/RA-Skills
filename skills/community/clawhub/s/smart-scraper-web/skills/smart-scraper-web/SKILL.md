---
name: web-data-extractor
description: Extract structured data from websites. Tables, lists, prices, articles, metadata. Zero external dependencies.
---

# Web Data Extractor 🕷️

> ⚠️ **Security Note** — This skill **sends user-provided URLs over the network**. Do not use with sensitive, authenticated, internal, or attacker-controlled URLs until redirect targets are revalidated.
>
> **Privacy Notice** — Caching is **enabled by default** for performance. A visible warning is shown before first cache write. Use `--no-cache` to disable local persistence of scraped content to `memory/scraper-cache/cache.json`. Each scrape writes **title, headings, paragraphs, links, tables, lists, prices, images, and metadata** to `cache.json`.

**Stop copying data by hand. Start extracting it automatically.**

## The Problem

Web content is everywhere but inaccessible to agents. `web_fetch` gets raw HTML, but you need structure — tables, prices, lists, article text — to make it useful.

Web Data Extractor turns raw HTML into structured data with one command.

## Quick Start

### Extract everything from a page

```bash
node skills/smart-scraper/smart-scraper.js --extract https://example.com
```

Returns title, headings, paragraphs, links, tables, lists, prices, images, and metadata.

### Extract without caching (privacy mode)

```bash
node skills/smart-scraper/smart-scraper.js --extract --no-cache https://example.com
```

Disables local cache persistence — scraped content is not written to disk.

### Extract with caching enabled (default)

```bash
node skills/smart-scraper/smart-scraper.js --extract https://example.com
```

Caching is enabled by default for performance. A visible warning is shown before first cache write.

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

### Caching (opt-in)

- Enable with `--cache` flag; **disabled by default** for privacy
- 5-minute TTL on fetched pages
- LRU eviction: max 50 entries or 10MB
- Cache stats via `--status`

## Configuration

Cache stored in: `memory/scraper-cache/cache.json`

Override data directory:
```bash
--dir /path/to/data
```

Disable cache (privacy mode):
```bash
--no-cache
```

Cache is enabled by default with a visible warning on first write.

## Security

- **URL validation** — only http/https to public hosts; blocks file://, gopher://, data:, localhost, private IPs, cloud metadata endpoints
- **Redirect validation** — each redirect target is re-validated against the same SSRF blocklist; attacker-controlled URLs cannot redirect to internal services
- **Redirect limit** — max 5 redirects to prevent loops and SSRF
- **Rate limiting** — 100ms minimum between requests
- **Bounded regex** — all patterns have `{0,N}` limits to prevent ReDoS
- **Cache eviction** — LRU with 50-entry / 10MB limits
- **Cache privacy** — caching is **enabled by default** with visible warning; use `--no-cache` to opt out
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
| **Web Data Extractor** | **✅** | **✅** | **✅** | **✅** | **✅ (opt-out)** |

**Web Data Extractor gives you structured extraction with zero dependencies. Use `--cache` to enable caching.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js http/https, no npm packages
3. **Structured output** — Returns parsed data, not raw HTML
4. **Privacy-first caching** — Caching enabled by default with visible warning; disable with `--no-cache`
5. **Multi-mode** — Extract everything or target specific data types

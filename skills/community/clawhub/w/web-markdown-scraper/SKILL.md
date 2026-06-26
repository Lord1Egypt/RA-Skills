---
name: web_markdown_scraper
description: >
  Fetch one or more public webpages with Scrapling, extract the main content,
  and convert HTML into Markdown using html2text.
  Supports static HTTP, concurrent async, stealth anti-bot (Camoufox/Firefox),
  and dynamic Playwright Chromium fetching modes with production-grade automatch.
metadata: {"openclaw":{"emoji":"🕸️","requires":{"bins":["python3"]}}}
---

# Web Markdown Scraper

Use this skill when the user wants to:
- Scrape one or more public webpages (static or JavaScript-rendered)
- Convert HTML pages into clean Markdown
- Extract article/body text for summarization, analysis, or indexing
- Bypass anti-bot protections (Cloudflare, Datadome, etc.) via stealth mode
- Scrape many URLs concurrently (async mode)
- Track page elements reliably across website redesigns (automatch)
- Save the extracted results as `.md` files

## Fetcher Mode Selection Guide

| Mode | Fetcher Class | Best For |
|------|--------------|----------|
| `http` (default) | `Fetcher` | Fast static pages, RSS, APIs |
| `async` | `AsyncFetcher` | Batch of 5+ static URLs in parallel |
| `stealth` | `StealthyFetcher` | Anti-bot sites, Cloudflare, fingerprint checks |
| `dynamic` | `PlayWrightFetcher` | Heavy SPAs, React/Vue/Angular apps |

**Decision rule**: Start with `http`. If you get a 403 / CAPTCHA / empty body, switch
to `stealth`. If the content is rendered client-side (empty on first load), use `dynamic`.
Use `async` when scraping many static URLs at once to save time.

## Inputs

### URL sources
- `--url URL` — one target URL (repeat flag for multiple: `--url A --url B`)
- `--url-file FILE` — plain text file with one URL per line

### Fetcher
- `--mode http|async|stealth|dynamic` — fetcher backend (default: `http`)

### Content extraction
- `--selector CSS` — CSS selector for the main content area (omit = full page)
- `--preserve-links` — keep hyperlinks in the Markdown output
- `--output-dir DIR` — save per-page `.md` files and a master `index.json` here

### AutoMatch — production resilience
- `--auto-save` — fingerprint & persist selected elements to the local DB on first run
- `--auto-match` — on subsequent runs, find elements by fingerprint even if the site
  layout has changed (do NOT need to update the CSS selector)

### Browser options (stealth / dynamic only)
- `--headless true|false|virtual` — headless mode; `virtual` uses Xvfb (default: `true`)
- `--network-idle` — wait until no network activity for ≥500 ms before capturing
- `--block-images` — block image loading (saves bandwidth and proxy quota)
- `--disable-resources` — drop fonts/images/media/stylesheets for ~25% faster loads
- `--wait-selector CSS` — pause until this element appears in the DOM
- `--wait-selector-state attached|visible|detached|hidden` — element state (default: `attached`)
- `--timeout MS` — global timeout in ms (default: 30 000)
- `--wait MS` — extra idle wait after page load in ms

### StealthyFetcher extras (stealth mode only)
- `--humanize SECONDS` — simulate human-like cursor movement (max duration in seconds)
- `--geoip` — spoof browser timezone, locale, language, and WebRTC IP from proxy geolocation
- `--block-webrtc` — prevent real-IP leaks via WebRTC
- `--disable-ads` — install uBlock Origin in the browser session
- `--proxy URL` — HTTP/SOCKS proxy as a URL string, or JSON:
  `'{"server":"host:port","username":"u","password":"p"}'`

### Reliability
- `--retry N` — retry failed requests up to N times with exponential backoff (max 30 s)

## Rules

1. Only process public `http://` or `https://` pages.
2. Never bypass login walls, CAPTCHAs, paywalls, or access controls.
3. Prefer the main article or body content; avoid polluting the output with navigation,
   headers, footers, or cookie banners — use `--selector` to target the content area.
4. When `--auto-save` is used, always also pass `--selector` so Scrapling knows which
   element fingerprint to record.
5. On subsequent runs for layout-changed pages, use `--auto-match` instead of `--auto-save`.
   Do not use both flags at once.
6. Use `--mode async` for batch jobs with 5+ static URLs for parallel execution.
7. Combine `--disable-resources` with `--block-images` in stealth/dynamic mode when
   you only need text content — this can cut load times by up to 40%.
8. Always inspect the top-level `ok` field and per-result `ok` fields before using content.
9. If `ok` is `false`, report the exact `error` string — do not invent or guess content.
10. When `--network-idle` is insufficient, use `--wait-selector` for a specific DOM element
    to guarantee the content has loaded before capture.

## Command Patterns

### Basic static page
```bash
python3 "{baseDir}/scrape_to_markdown.py" --url "<URL>"
```

### Static page — target specific content area
```bash
python3 "{baseDir}/scrape_to_markdown.py" --url "<URL>" --selector "article.main-content"
```

### Stealth mode — bypass anti-bot protection
```bash
python3 "{baseDir}/scrape_to_markdown.py" --url "<URL>" --mode stealth --network-idle
```

### Stealth + proxy + human fingerprint (maximum stealth)
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url "<URL>" \
  --mode stealth \
  --proxy "http://user:pass@host:port" \
  --humanize 2.0 \
  --geoip \
  --block-webrtc \
  --network-idle
```

### Dynamic SPA page (Playwright Chromium)
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url "<URL>" \
  --mode dynamic \
  --wait-selector ".product-list" \
  --network-idle \
  --disable-resources
```

### Async concurrent batch (multiple URLs)
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --mode async \
  --url "<URL1>" --url "<URL2>" --url "<URL3>"
```

### Batch from file + stealth + save to disk
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url-file urls.txt \
  --mode stealth \
  --disable-resources \
  --output-dir outputs
```

### First-run automatch setup (save fingerprint)
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url "<URL>" \
  --selector ".article-body" \
  --auto-save \
  --output-dir outputs
```

### Subsequent run after site layout change (adaptive match)
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url "<URL>" \
  --selector ".article-body" \
  --auto-match \
  --output-dir outputs
```

### Full production scrape
```bash
python3 "{baseDir}/scrape_to_markdown.py" \
  --url "<URL>" \
  --mode stealth \
  --selector "main article" \
  --auto-match \
  --preserve-links \
  --network-idle \
  --disable-resources \
  --timeout 60000 \
  --retry 3 \
  --output-dir outputs
```

## Output Handling

JSON is printed to stdout. Always check `ok` before using content.

**Top-level fields:**
- `ok` — `true` only if every URL succeeded
- `total` / `succeeded` / `failed` — count summary
- `results` — array of per-URL result objects
- `output_index_file` — path to saved `index.json` (if `--output-dir` used)

**Per-URL result fields (when `ok: true`):**
- `url` — the requested URL
- `status` — HTTP status code (e.g. `200`)
- `title` — page `<title>` text
- `markdown` — extracted content as Markdown ← **use this as main content**
- `markdown_length` — character count (useful for quality checks)
- `output_markdown_file` — path to saved `.md` file (if `--output-dir` used)

**On failure (`ok: false` in a result):**
- `error` — exact error message; report this verbatim, do not invent content

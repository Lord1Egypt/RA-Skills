---
name: webclaw
description: Web extraction for LLMs and agents. Scrape, crawl, map, search, extract, summarize, diff, monitor, and research any URL into clean Markdown, text, or JSON, including pages that block bots or render with JavaScript. Use when you need reliable web content, the built-in web_fetch fails, or you need structured data from a page.
homepage: https://webclaw.io
user-invocable: true
metadata: {"openclaw":{"emoji":"🦀","requires":{"env":["WEBCLAW_API_KEY"]},"primaryEnv":"WEBCLAW_API_KEY","homepage":"https://webclaw.io","install":[{"id":"npx","kind":"node","bins":["webclaw-mcp"],"label":"npx create-webclaw"}]}}
---

# webclaw

High-quality web extraction for LLMs and agents. Turns any URL into clean Markdown, text, or JSON, and handles pages that block bots or render content with JavaScript.

## When to use this skill

- **Always** when you need to fetch web content and want reliable results
- When `web_fetch` returns empty/blocked content (403s, bot challenges)
- When you need structured data extraction (pricing tables, product info)
- When you need to crawl an entire site or discover all URLs
- When you need to discover the API endpoints a page's JavaScript calls
- When you need LLM-optimized content (cleaner than raw markdown)
- When you need to summarize a page without reading the full content
- When you need to detect content changes between visits
- When you need brand identity analysis (colors, fonts, logos)
- When you need web search results with optional page scraping
- When you need deep multi-source research on a topic
- When you need AI-guided scraping to accomplish a goal on a page
- When you need to monitor a URL for changes over time

## API base

All requests go to `https://api.webclaw.io/v1/`.

Authentication: `Authorization: Bearer $WEBCLAW_API_KEY`

## Decision order — READ THIS FIRST

Before calling any endpoint, look at the URL. If it matches one of the 28 vertical extractor patterns below, use `POST /v1/scrape/{vertical}` **immediately**. Do not try `/v1/scrape` first, do not append `.json`, do not parse markdown. The vertical endpoint returns typed JSON with the fields you need in one call.

| URL shape | Use this endpoint | Returns |
|---|---|---|
| `reddit.com/r/*/comments/*` | `/v1/scrape/reddit` | `{post: {title, author, score, comment_count}, comments: [...]}` |
| `github.com/{owner}/{repo}` | `/v1/scrape/github_repo` | repo metadata, stars, language, readme |
| `github.com/*/pull/*` | `/v1/scrape/github_pr` | title, state, author, commits, reviews |
| `github.com/*/issues/*` | `/v1/scrape/github_issue` | title, state, labels, comments |
| `github.com/*/releases/tag/*` | `/v1/scrape/github_release` | name, tag, assets, body |
| `news.ycombinator.com/item?id=*` | `/v1/scrape/hackernews` | story + threaded comments |
| `pypi.org/project/*` | `/v1/scrape/pypi` | name, version, description, downloads |
| `npmjs.com/package/*` | `/v1/scrape/npm` | name, version, deps, weekly downloads |
| `crates.io/crates/*` | `/v1/scrape/crates_io` | name, version, dependents |
| `huggingface.co/{owner}/{name}` | `/v1/scrape/huggingface_model` | model card, downloads, license |
| `huggingface.co/datasets/*` | `/v1/scrape/huggingface_dataset` | dataset card, rows, license |
| `arxiv.org/abs/*` | `/v1/scrape/arxiv` | title, authors, abstract, pdf_url |
| `hub.docker.com/_/*` | `/v1/scrape/docker_hub` | image tags, description, pulls |
| `dev.to/*/*` | `/v1/scrape/dev_to` | title, author, body, tags, reactions |
| `stackoverflow.com/questions/*` | `/v1/scrape/stackoverflow` | question + answers + votes |
| `{pub}.substack.com/p/*` | `/v1/scrape/substack_post` | title, author, body |
| `youtube.com/watch?v=*` (or `/shorts/*`, `youtu.be/*`) | `/v1/scrape` (auto-detected) | full transcript + title, channel, channel_url, duration_seconds, view_count, like_count, tags, thumbnail. See "YouTube auto-detection" below. |
| `linkedin.com/feed/update/*` | `/v1/scrape/linkedin_post` | author, body, engagement |
| `instagram.com/p/*` | `/v1/scrape/instagram_post` | caption, likes, user |
| `instagram.com/{user}/` | `/v1/scrape/instagram_profile` | bio, followers, posts |
| `amazon.com/dp/*` | `/v1/scrape/amazon_product` | title, price, rating, review_count |
| `ebay.com/itm/*` | `/v1/scrape/ebay_listing` | title, price, condition, seller |
| `etsy.com/listing/*` | `/v1/scrape/etsy_listing` | title, price, shop, reviews |
| `trustpilot.com/review/*` | `/v1/scrape/trustpilot_reviews` | aggregate + individual reviews |
| any `{shop}/products/{handle}` (Shopify) | `/v1/scrape/shopify_product` | title, variants, price, description |
| any `{shop}/collections/{handle}` (Shopify) | `/v1/scrape/shopify_collection` | name, products |
| generic ecommerce product page | `/v1/scrape/ecommerce_product` | Schema.org product fields |
| WooCommerce `{shop}/product/*` | `/v1/scrape/woocommerce_product` | title, price, description |

Call one of the above if the URL matches. Only fall back to `/v1/scrape` below when the URL does NOT match any vertical.

Example vertical call:

```bash
curl -X POST https://api.webclaw.io/v1/scrape/reddit \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.reddit.com/r/rust/comments/abc/title/"}'
```

Response: `{"vertical":"reddit","url":"...","data":{"post":{...},"comments":[...]}}`. Bills 1 credit.

## Endpoints

### 1. Scrape — extract content from a single URL

```bash
curl -X POST https://api.webclaw.io/v1/scrape \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"],
    "only_main_content": true
  }'
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | required | URL to scrape |
| `formats` | string[] | `["markdown"]` | Output formats: `markdown`, `text`, `llm`, `json` |
| `include_selectors` | string[] | `[]` | CSS selectors to keep (e.g. `["article", ".content"]`) |
| `exclude_selectors` | string[] | `[]` | CSS selectors to remove (e.g. `["nav", "footer", ".ads"]`) |
| `only_main_content` | bool | `false` | Extract only the main article/content area |
| `no_cache` | bool | `false` | Skip cache, fetch fresh |
| `max_cache_age` | int | server default | Max acceptable cache age in seconds |

**Response:**

```json
{
  "url": "https://example.com",
  "metadata": {
    "title": "Example",
    "description": "...",
    "language": "en",
    "word_count": 1234
  },
  "markdown": "# Page Title\n\nContent here...",
  "cache": { "status": "miss" }
}
```

**Format options:**
- `markdown` — clean markdown, best for general use
- `text` — plain text without formatting
- `llm` — optimized for LLM consumption: includes page title, URL, and cleaned content with link references. Best for feeding to AI models.
- `json` — full extraction result with all metadata

**When bot-protection handling activates** (automatic, no extra config):
```json
{
  "antibot": {
    "bypass": true,
    "elapsed_ms": 3200
  }
}
```

**YouTube auto-detection** (automatic, no extra config):

Pass any `youtube.com/watch`, `youtube.com/shorts/`, or `youtu.be/` URL and the response carries two extra fields alongside `markdown` / `text` / `llm`:

- `transcript` (string) — full auto-caption text. `null` when the video has no captions.
- `youtube` (object) — `{ video_id, title, description, channel, channel_url, uploader, upload_date, duration_seconds, view_count, like_count, thumbnail, tags, categories, language }`.

```bash
curl -X POST https://api.webclaw.io/v1/scrape \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "metadata": { "title": "...", "image": "https://i.ytimg.com/..." },
  "youtube": {
    "video_id": "dQw4w9WgXcQ",
    "channel": "Rick Astley",
    "duration_seconds": 213,
    "view_count": 1490000000,
    "tags": ["rick astley", "..."]
  },
  "transcript": "We're no strangers to love...",
  "markdown": "# Never Gonna Give You Up\n\n**Channel:** Rick Astley\n\n## Description\n..."
}
```

Cold p50 latency 2-4s; cache hits ~150ms. 1 credit per call. Same fields available on the SDKs as `result.youtube.*` / `result.transcript` (Python, JS) and `resp.YouTube.*` / `resp.Transcript` (Go).

### 2. Crawl — scrape an entire website

Starts an async job. Poll for results.

**Start crawl:**
```bash
curl -X POST https://api.webclaw.io/v1/crawl \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "max_depth": 3,
    "max_pages": 50,
    "use_sitemap": true
  }'
```

Response: `{ "job_id": "abc-123", "status": "running" }`

**Poll status:**
```bash
curl https://api.webclaw.io/v1/crawl/abc-123 \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

Response when complete:
```json
{
  "job_id": "abc-123",
  "status": "completed",
  "total": 47,
  "completed": 45,
  "errors": 2,
  "pages": [
    {
      "url": "https://docs.example.com/intro",
      "markdown": "# Introduction\n...",
      "metadata": { "title": "Intro", "word_count": 500 }
    }
  ]
}
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | required | Starting URL |
| `max_depth` | int | `3` | How many links deep to follow |
| `max_pages` | int | `100` | Maximum pages to crawl |
| `use_sitemap` | bool | `false` | Seed URLs from sitemap.xml |
| `formats` | string[] | `["markdown"]` | Output formats per page |
| `include_selectors` | string[] | `[]` | CSS selectors to keep |
| `exclude_selectors` | string[] | `[]` | CSS selectors to remove |
| `only_main_content` | bool | `false` | Main content only |

### 3. Map — discover all URLs on a site

Fast URL discovery without full content extraction.

```bash
curl -X POST https://api.webclaw.io/v1/map \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Response:
```json
{
  "url": "https://example.com",
  "count": 142,
  "urls": [
    "https://example.com/about",
    "https://example.com/pricing",
    "https://example.com/docs/intro"
  ]
}
```

### 4. Endpoints — discover API endpoints embedded in a page

Scans a page's inline JavaScript and `<script src>` bundles for API
endpoints (relative paths, absolute URLs, GraphQL, WebSocket). This
surfaces the request surface that `map` (sitemap only) cannot see —
useful for reverse-engineering a site's backend before scraping or
extracting. Heuristic v1: regex over fetched JS, single URL.

```bash
curl -X POST https://api.webclaw.io/v1/endpoints \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "include_third_party": false,
    "max_bundles": 20
  }'
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | required | Page URL to scan |
| `include_third_party` | bool | `false` | Also report endpoints on hosts other than the target site |
| `max_bundles` | int | `20` | Max number of `<script src>` bundles to fetch and scan (capped at 20) |

**Response:**

```json
{
  "url": "https://example.com",
  "bundles_scanned": 8,
  "endpoint_count": 23,
  "endpoints": [
    { "value": "/api/v1/users", "kind": "relative_path", "first_party": true, "source": "inline" },
    { "value": "https://api.example.com/graphql", "kind": "absolute_url", "first_party": true, "source": "https://example.com/static/app.4f2c.js" },
    { "value": "query { viewer { id } }", "kind": "graph_ql", "first_party": true, "source": "https://example.com/static/app.4f2c.js" },
    { "value": "wss://realtime.example.com/socket", "kind": "web_socket", "first_party": true, "source": "inline" }
  ],
  "hosts": ["api.example.com", "realtime.example.com"],
  "truncated": false
}
```

**Endpoint `kind` values:** `relative_path`, `absolute_url`, `graph_ql`, `web_socket`.

`source` is either `"inline"` (found in the page's inline `<script>`) or
the URL of the bundle the endpoint was extracted from. `first_party` is
`true` when the endpoint host matches the target site;
`include_third_party: false` filters the rest out. `truncated` is `true`
when more bundles existed than `max_bundles` allowed.

Bills 2 credits per call.

### 5. Batch — scrape multiple URLs in parallel

```bash
curl -X POST https://api.webclaw.io/v1/batch \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://a.com",
      "https://b.com",
      "https://c.com"
    ],
    "formats": ["markdown"],
    "concurrency": 5
  }'
```

Response:
```json
{
  "total": 3,
  "completed": 3,
  "errors": 0,
  "results": [
    { "url": "https://a.com", "markdown": "...", "metadata": {} },
    { "url": "https://b.com", "markdown": "...", "metadata": {} },
    { "url": "https://c.com", "error": "timeout" }
  ]
}
```

### 6. Extract — LLM-powered structured extraction

Pull structured data from any page using a JSON schema or plain-text prompt.

**With JSON schema:**
```bash
curl -X POST https://api.webclaw.io/v1/extract \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/pricing",
    "schema": {
      "type": "object",
      "properties": {
        "plans": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "price": { "type": "string" },
              "features": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      }
    }
  }'
```

**With prompt:**
```bash
curl -X POST https://api.webclaw.io/v1/extract \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/pricing",
    "prompt": "Extract all pricing tiers with names, monthly prices, and key features"
  }'
```

Response:
```json
{
  "url": "https://example.com/pricing",
  "data": {
    "plans": [
      { "name": "Starter", "price": "$19/mo", "features": ["10k credits", "3 research runs"] },
      { "name": "Pro", "price": "$99/mo", "features": ["250k credits", "20 research runs"] }
    ]
  }
}
```

### 7. Summarize — get a quick summary of any page

```bash
curl -X POST https://api.webclaw.io/v1/summarize \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/long-article",
    "max_sentences": 3
  }'
```

Response:
```json
{
  "url": "https://example.com/long-article",
  "summary": "The article discusses... Key findings include... The author concludes that..."
}
```

### 8. Diff — detect content changes

Compare current page content against a previous snapshot.

```bash
curl -X POST https://api.webclaw.io/v1/diff \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "previous": {
      "markdown": "# Old content...",
      "metadata": { "title": "Old Title" }
    }
  }'
```

Response:
```json
{
  "url": "https://example.com",
  "status": "changed",
  "diff": "--- previous\n+++ current\n@@ -1 +1 @@\n-# Old content\n+# New content",
  "metadata_changes": [
    { "field": "title", "old": "Old Title", "new": "New Title" }
  ]
}
```

### 9. Brand — extract brand identity

Analyze a website's visual identity: colors, fonts, logo.

```bash
curl -X POST https://api.webclaw.io/v1/brand \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Response:
```json
{
  "url": "https://example.com",
  "brand": {
    "colors": [
      { "hex": "#FF6B35", "usage": "primary" },
      { "hex": "#1A1A2E", "usage": "background" }
    ],
    "fonts": ["Inter", "JetBrains Mono"],
    "logo_url": "https://example.com/logo.svg",
    "favicon_url": "https://example.com/favicon.ico"
  }
}
```

### 10. Vertical extractors — typed JSON for 28 sites

Site-specific extractors that return typed JSON instead of generic markdown. Use when the target URL is a GitHub PR, Reddit thread, Amazon product, YouTube video, PyPI/npm/crates package, HuggingFace model/dataset, ArXiv paper, Instagram profile, Shopify product, Etsy listing, Trustpilot reviews, or similar.

```bash
# List every extractor with its label and URL shape
curl https://api.webclaw.io/v1/extractors \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"

# Run a specific extractor (GitHub PR)
curl -X POST https://api.webclaw.io/v1/scrape/github_pr \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/rust-lang/rust/pull/123456"}'
```

Response shape (extractor-specific `data`):
```json
{
  "vertical": "github_pr",
  "url": "https://github.com/rust-lang/rust/pull/123456",
  "data": {
    "title": "...",
    "state": "open",
    "author": "...",
    "additions": 42,
    "deletions": 7,
    "commits": 3,
    "reviews": [ /* ... */ ]
  }
}
```

**Full catalog (28):** `reddit`, `hackernews`, `github_repo`, `github_pr`, `github_issue`, `github_release`, `pypi`, `npm`, `crates_io`, `huggingface_model`, `huggingface_dataset`, `arxiv`, `docker_hub`, `dev_to`, `stackoverflow`, `substack_post`, `youtube_video`, `linkedin_post`, `instagram_post`, `instagram_profile`, `shopify_product`, `shopify_collection`, `ecommerce_product`, `woocommerce_product`, `amazon_product`, `ebay_listing`, `etsy_listing`, `trustpilot_reviews`.

Most of these auto-dispatch from a plain `POST /v1/scrape` call (their URL patterns are distinctive). The generic-pattern ones (`shopify_*`, `ecommerce_product`, `woocommerce_product`, `substack_post`) require the explicit `/v1/scrape/{vertical}` route.

`youtube_video` is **not** a `/v1/scrape/{vertical}` route. YouTube `watch` / `shorts` / `youtu.be` URLs are handled by a short-circuit inside `POST /v1/scrape` that returns the `transcript` + `youtube` block described under "YouTube auto-detection" above. Do not POST to `/v1/scrape/youtube_video`.

Bills 1 credit per successful call.

### 11. Search — web search with optional scraping

Search the web and optionally scrape each result page.

```bash
curl -X POST https://api.webclaw.io/v1/search \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best rust web frameworks 2026",
    "num_results": 5,
    "scrape": true,
    "formats": ["markdown"]
  }'
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | required | Search query |
| `num_results` | int | `10` | Number of search results to return |
| `scrape` | bool | `false` | Also scrape each result page for full content |
| `formats` | string[] | `["markdown"]` | Output formats when `scrape` is true |
| `country` | string | none | Country code for localized results (e.g. `"us"`, `"de"`) |
| `lang` | string | none | Language code for results (e.g. `"en"`, `"fr"`) |

**Response:**

```json
{
  "query": "best rust web frameworks 2026",
  "results": [
    {
      "title": "Top Rust Web Frameworks in 2026",
      "url": "https://blog.example.com/rust-frameworks",
      "snippet": "A comprehensive comparison of Axum, Actix, and Rocket...",
      "position": 1,
      "markdown": "# Top Rust Web Frameworks\n\n..."
    },
    {
      "title": "Choosing a Rust Backend Framework",
      "url": "https://dev.to/rust-backends",
      "snippet": "When starting a new Rust web project...",
      "position": 2,
      "markdown": "# Choosing a Rust Backend\n\n..."
    }
  ]
}
```

The `markdown` field on each result is only present when `scrape: true`. Without it, you get titles, URLs, snippets, and positions only.

### 12. Research — deep multi-source research

Starts an async research job that searches, scrapes, and synthesizes information across multiple sources. Poll for results.

**Start research:**
```bash
curl -X POST https://api.webclaw.io/v1/research \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does Cloudflare Turnstile work and what are its known bypass methods?",
    "max_iterations": 5,
    "max_sources": 10,
    "topic": "security",
    "deep": true
  }'
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | required | Research question or topic |
| `max_iterations` | int | server default | Maximum research iterations (search-read-analyze cycles) |
| `max_sources` | int | server default | Maximum number of sources to consult. Tier capped: Free 0, Starter 10, Pro 30, Scale 100 |
| `topic` | string | none | Topic hint to guide search strategy (e.g. `"security"`, `"finance"`, `"engineering"`) |
| `deep` | bool | `false` | Enable deep research mode for more thorough analysis (costs 10 credits instead of 1) |

Response: `{ "id": "res-abc-123", "status": "running" }`

**Poll results:**
```bash
curl https://api.webclaw.io/v1/research/res-abc-123 \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

Response when complete:
```json
{
  "id": "res-abc-123",
  "status": "completed",
  "query": "How does Cloudflare Turnstile work and what are its known bypass methods?",
  "report": "# Cloudflare Turnstile Analysis\n\n## Overview\nCloudflare Turnstile is a CAPTCHA replacement that...\n\n## How It Works\n...\n\n## Known Bypass Methods\n...",
  "sources": [
    { "url": "https://developers.cloudflare.com/turnstile/", "title": "Turnstile Documentation" },
    { "url": "https://blog.cloudflare.com/turnstile-ga/", "title": "Turnstile GA Announcement" }
  ],
  "findings": [
    "Turnstile uses browser environment signals and proof-of-work challenges",
    "Managed mode auto-selects challenge difficulty based on visitor risk score",
    "Known bypass approaches include instrumented browser automation"
  ],
  "iterations": 5,
  "elapsed_ms": 34200
}
```

**Status values:** `running`, `completed`, `failed`

### 13. Watch — monitor a URL for changes

Create persistent monitors that check a URL on a schedule and notify via webhook when content changes.

**Create a monitor:**
```bash
curl -X POST https://api.webclaw.io/v1/watch \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/pricing",
    "interval": "0 */6 * * *",
    "webhook_url": "https://hooks.example.com/pricing-changed",
    "formats": ["markdown"]
  }'
```

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | string | required | URL to monitor |
| `interval` | string | required | Check frequency as cron expression or seconds (e.g. `"0 */6 * * *"` or `"3600"`) |
| `webhook_url` | string | none | URL to POST when changes are detected |
| `formats` | string[] | `["markdown"]` | Output formats for snapshots |

Response:
```json
{
  "id": "watch-abc-123",
  "url": "https://example.com/pricing",
  "interval": "0 */6 * * *",
  "webhook_url": "https://hooks.example.com/pricing-changed",
  "formats": ["markdown"],
  "created_at": "2026-03-20T10:00:00Z",
  "last_check": null,
  "status": "active"
}
```

**List all monitors:**
```bash
curl https://api.webclaw.io/v1/watch \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

Response:
```json
{
  "monitors": [
    {
      "id": "watch-abc-123",
      "url": "https://example.com/pricing",
      "interval": "0 */6 * * *",
      "status": "active",
      "last_check": "2026-03-20T16:00:00Z",
      "checks": 4
    }
  ]
}
```

**Get a monitor with snapshots:**
```bash
curl https://api.webclaw.io/v1/watch/watch-abc-123 \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

Response:
```json
{
  "id": "watch-abc-123",
  "url": "https://example.com/pricing",
  "interval": "0 */6 * * *",
  "status": "active",
  "snapshots": [
    {
      "checked_at": "2026-03-20T16:00:00Z",
      "status": "changed",
      "diff": "--- previous\n+++ current\n@@ -5 +5 @@\n-Pro: $99/mo\n+Pro: $119/mo"
    },
    {
      "checked_at": "2026-03-20T10:00:00Z",
      "status": "baseline"
    }
  ]
}
```

**Trigger an immediate check:**
```bash
curl -X POST https://api.webclaw.io/v1/watch/watch-abc-123/check \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

**Delete a monitor:**
```bash
curl -X DELETE https://api.webclaw.io/v1/watch/watch-abc-123 \
  -H "Authorization: Bearer $WEBCLAW_API_KEY"
```

## Firecrawl v2 compatibility layer

If you already have code written against the Firecrawl v2 API, point it at
`https://api.webclaw.io` and use these drop-in endpoints instead of the
native `/v1/*` ones. They accept Firecrawl-shaped requests and return
Firecrawl-shaped responses, backed by the same webclaw extraction pipeline.

| Method | Path | Maps to |
|--------|------|---------|
| POST | `/v2/scrape` | single-page scrape |
| POST | `/v2/crawl` | start async crawl |
| GET | `/v2/crawl/{id}` | crawl status/results |
| DELETE | `/v2/crawl/{id}` | cancel a crawl |
| POST | `/v2/map` | URL discovery |
| POST | `/v2/search` | web search |

```bash
curl -X POST https://api.webclaw.io/v2/scrape \
  -H "Authorization: Bearer $WEBCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown"]}'
```

Same auth (`Authorization: Bearer $WEBCLAW_API_KEY`) and the same credit
billing as the native endpoints. Prefer the native `/v1/*` API for new
code — the `/v2` layer exists only for Firecrawl migration compatibility
and does not expose webclaw-only features (vertical extractors, YouTube
short-circuit, `llm` format, endpoints discovery, brand, diff, research,
watch).

## Choosing the right format

| Goal | Format | Why |
|------|--------|-----|
| Read and understand a page | `markdown` | Clean structure, headings, links preserved |
| Feed content to an AI model | `llm` | Optimized: includes title + URL header, clean link refs |
| Search or index content | `text` | Plain text, no formatting noise |
| Programmatic analysis | `json` | Full metadata, structured data, DOM statistics |

## Tips

- **Use `llm` format** when passing content to yourself or another AI — it's specifically optimized for LLM consumption with better context framing.
- **Use `only_main_content: true`** to skip navigation, sidebars, and footers. Reduces noise significantly.
- **Use `include_selectors`/`exclude_selectors`** for fine-grained control when `only_main_content` isn't enough.
- **Batch over individual scrapes** when fetching multiple URLs — it's faster and more efficient.
- **Use `map` before `crawl`** to discover the site structure first, then crawl specific sections.
- **Use `endpoints` to reverse-engineer a site's backend** — it pulls API paths, GraphQL, and WebSocket URLs out of the page's JS that `map` (sitemap only) can't see. Set `include_third_party: true` to also see analytics/3rd-party calls.
- **Use `extract` with a JSON schema** for reliable structured output (e.g., pricing tables, product specs, contact info).
- **Bot-protection handling is automatic** — no extra configuration needed. Works on sites that block bots and JS-rendered SPAs.
- **Use `search` with `scrape: true`** to get full page content for each search result in one call instead of searching then scraping separately.
- **Use `research` for complex questions** that need multiple sources — it handles the search-read-synthesize loop automatically. Enable `deep: true` for thorough analysis.
- **Use `watch` for ongoing monitoring** — set up a cron schedule and a webhook to get notified when a page changes without polling manually.

## Smart Fetch Architecture (local CLI wrapper only)

> **Scope:** This section describes the bundled CLI wrapper
> `scripts/webclaw.py` only. It does **not** describe the HTTP API.
> Every call to `https://api.webclaw.io/*` (including `/v2`) bills
> credits — the API has no local-first path and no "free" tier of
> requests. The local-first / zero-credit behaviour below exists only
> because the wrapper runs a plain HTTP fetch on your own machine
> first and only calls the API when that fetch can't finish the job.

The `scripts/webclaw.py` wrapper uses a **local-first** approach:
extraction runs in your own process for the common case, and the cloud
API (`api.webclaw.io`) is only consulted — and only then billed — when
a local fetch can't finish the job.

### Decision tree (wrapper)

```
                                ┌───────────────────┐
  scripts/webclaw.py scrape ─▶  │  local HTTP fetch │
                                └─────┬─────────────┘
                                      │
                            ┌─────────┴──────────┐
                            ▼                    ▼
                      success, clean HTML    one of:
                      → local extract         • bot-protection page
                      → return (0 credits)    • JS-rendered SPA shell
                                              • network / DNS error
                                              │
                                              ▼
                                    WEBCLAW_API_KEY set?
                                    ┌─────────────┴─────────────┐
                                   yes                          no
                                    │                            │
                                    ▼                            ▼
                       cloud API (api.webclaw.io)        return best-effort
                       credits spent per request          local result + warn
```

### What "~80% local" means in practice (wrapper)

- **Local path (free, zero credits — wrapper only):** static HTML sites,
  public docs, product pages that server-render, news sites, blogs,
  anything on plain nginx/Apache/CDN. The wrapper does a basic stdlib
  text extraction here; quality is lower than the cloud `webclaw-core`
  pipeline but costs nothing.
- **Cloud fallback (credits charged):** sites that block bots
  challenges, JS-rendered SPAs (React / Next.js / Vue shells where the
  HTML has no content until hydration), sites that require a browser
  TLS fingerprint or solved captcha. The wrapper fails cleanly on the
  local path and automatically retries against the cloud API.
- **No API key set:** `WEBCLAW_API_KEY` is optional *for the wrapper*.
  Without it, the local path still works for the 80% — only
  bot-protected / JS-rendered sites surface a warning and return
  degraded content. (The HTTP API always requires a key.)

### Practical guidance (wrapper)

- If you're scraping public docs, blogs, reference material, or an API's
  HTML docs through the wrapper: local path is enough, don't worry about
  credits.
- If the user asks for Amazon / LinkedIn / Twitter / Instagram / any
  aggressively-protected site: expect the wrapper's cloud fallback to
  kick in (credits billed).
- If you get an empty / short result and the page looks bot-protected,
  re-run the wrapper with `--cloud` to skip the local attempt and go
  straight to the API.

## vs web_fetch

| | webclaw | web_fetch |
|---|---------|-----------|
| Bot-protected sites | Automatic | Fails (403) |
| JS-rendered pages | Automatic | Readability only |
| Output quality | 20-step optimization pipeline | Basic HTML parsing |
| Structured extraction | LLM-powered, schema-based | None |
| Crawling | Full site crawl with sitemap | Single page only |
| Caching | Built-in, configurable TTL | Per-session |
| Rate limiting | Managed server-side | Client responsibility |

Use `web_fetch` for simple, fast lookups. Use webclaw when you need reliability, quality, or advanced features.

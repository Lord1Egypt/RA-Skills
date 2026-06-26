---
name: proxy-web-fetch
description: |
  Proxy Web Page Fetch Tool - Fetches and parses web page content into structured Markdown or text via the OpenClaw Manager proxy.
  
  Use when:
  - Need to fetch and read the content of a web page by URL
  - Need to convert web pages to Markdown or plain text format
  - Need to extract page content with or without images
  - Need to get page metadata (title, description, keywords)
  - Need to control caching, image retention, or summary options for fetched content
  - User asks to "read a URL", "fetch a page", "grab the content of a web page", "scrape" or "crawl" a URL
  
  This skill routes all fetch requests through the Manager Web Fetch Proxy
  (configured via `WEB_FETCH_PROXY_URL` env var, required),
  which handles API key management automatically — no manual configuration needed.
  
  Do NOT confuse with web search — this skill fetches a specific URL's content, it does not perform keyword searches.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"], "envs": ["WEB_FETCH_PROXY_URL"] },
      },
  }
---

# Proxy Web Page Fetch

Fetch and parse web page content via the OpenClaw Manager Web Fetch Proxy. The Manager handles API key injection from encrypted storage automatically — no manual key configuration needed.

The proxy URL is configured via the `WEB_FETCH_PROXY_URL` environment variable (required). If not set, the skill will not be available.

## Quick Start

### Basic cURL Usage

```bash
curl --request POST \
  --url "${WEB_FETCH_PROXY_URL}/" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://www.example.com"
  }'
```

### Script Usage

A wrapper shell script is provided for convenience.

```bash
# Basic Fetch (returns Markdown by default)
./scripts/proxy_fetch.sh --url "https://www.example.com"

# Fetch as plain text, no cache
./scripts/proxy_fetch.sh \
  --url "https://docs.python.org/3/" \
  --format text \
  --no-cache

# Fetch with image and link summaries
./scripts/proxy_fetch.sh \
  --url "https://news.example.com/article" \
  --images-summary \
  --links-summary

# Fetch without images, disable GFM
./scripts/proxy_fetch.sh \
  --url "https://blog.example.com/post" \
  --no-images \
  --no-gfm
```

## Authentication

No authentication required — the proxy reads API keys internally from the Manager's encrypted secrets store.

## API Parameter Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | ✅ | - | URL of the web page to fetch |
| `timeout` | integer | - | `20` | Request timeout in seconds |
| `no_cache` | boolean | - | `false` | Disable caching (`true`/`false`) |
| `return_format` | string | - | `markdown` | Return format: `markdown` or `text` |
| `retain_images` | boolean | - | `true` | Retain images in output (`true`/`false`) |
| `no_gfm` | boolean | - | `false` | Disable GitHub Flavored Markdown (`true`/`false`) |
| `keep_img_data_url` | boolean | - | `false` | Keep image data URLs (`true`/`false`) |
| `with_images_summary` | boolean | - | `false` | Include images summary (`true`/`false`) |
| `with_links_summary` | boolean | - | `false` | Include links summary (`true`/`false`) |

## Response Structure

The proxy returns JSON with the parsed page content.

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "model": "model-name",
  "reader_result": {
    "title": "Page Title",
    "description": "Brief page description",
    "url": "https://www.example.com",
    "content": "Parsed page content (Markdown or text)",
    "external": {
      "stylesheet": {}
    },
    "metadata": {
      "keywords": "page, keywords",
      "viewport": "width=device-width",
      "description": "Meta description",
      "format-detection": "telephone=no"
    }
  }
}
```

### Key Response Fields

| Field | Description |
|-------|-------------|
| `reader_result.content` | Main parsed content (body text, images, links) |
| `reader_result.title` | Page title |
| `reader_result.description` | Brief page description |
| `reader_result.url` | Original page URL |
| `reader_result.metadata` | Page metadata (keywords, viewport, etc.) |

## Common Use Cases

| Scenario | Command |
|----------|---------|
| Read a documentation page | `--url <doc_url>` |
| Extract text only (no images) | `--url <url> --no-images --format text` |
| Force fresh fetch (bypass cache) | `--url <url> --no-cache` |
| Get content with all summaries | `--url <url> --images-summary --links-summary` |
| Long page with extended timeout | `--url <url> --timeout 60` |

## Environment Requirements

- OpenClaw Manager must be running with the Web Fetch Proxy enabled.
- `WEB_FETCH_PROXY_URL` environment variable must be set to the proxy URL (required, no default).
- `curl` command must be available in your system path.

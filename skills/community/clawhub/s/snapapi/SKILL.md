---
name: snapapi
description: Give your agent web intelligence — screenshot any URL, extract structured page data, detect page changes, and analyze websites via the SnapAPI REST API.
metadata:
  openclaw:
    requires:
      env:
        - SNAPAPI_API_KEY
      bins: []
    primaryEnv: SNAPAPI_API_KEY
tags:
  - web
  - screenshot
  - scraping
  - ai-agents
  - page-analysis
  - monitoring
  - browser
version: 1.0.0
---

# SnapAPI — Web Intelligence for AI Agents

SnapAPI gives your agent eyes on the internet. One API, six capabilities:

**Base URL:** `https://snapapi.tech`
**Auth:** `X-API-Key: $SNAPAPI_API_KEY`
**Free tier:** 100 requests/month — get a key at https://snapapi.tech

---

## Screenshot any URL

```bash
curl "https://snapapi.tech/v1/screenshot?url=https://example.com&format=png" \
  -H "X-API-Key: $SNAPAPI_API_KEY" \
  --output screenshot.png
```

Options: `format=png|jpeg|webp`, `fullPage=true`, `darkMode=true`, `width=1280`, `height=800`

---

## Analyze a page (structured intelligence)

```bash
curl "https://snapapi.tech/v1/analyze?url=https://example.com" \
  -H "X-API-Key: $SNAPAPI_API_KEY"
```

Returns:
```json
{
  "title": "Example Domain",
  "description": "...",
  "headings": [{ "level": 1, "text": "..." }],
  "links": [{ "text": "More info", "href": "https://..." }],
  "text_content": "...",
  "forms": [],
  "technologies": ["nginx"],
  "load_time_ms": 832
}
```

Use this when your agent needs to **understand** a page, not just see it.

---

## Extract metadata (fast — no full render)

```bash
curl "https://snapapi.tech/v1/metadata?url=https://example.com" \
  -H "X-API-Key: $SNAPAPI_API_KEY"
```

Returns: title, description, OG tags, Twitter card, favicon, canonical URL. Faster than `/analyze` — use for link previews and SEO research.

---

## Generate a PDF

```bash
curl "https://snapapi.tech/v1/pdf?url=https://example.com" \
  -H "X-API-Key: $SNAPAPI_API_KEY" \
  --output page.pdf
```

Options: `format=A4|Letter`, `landscape=true`, `margin=20`

---

## Render HTML to image

Useful for generating OG images, email previews, or screenshots from dynamic HTML:

```bash
curl -X POST "https://snapapi.tech/v1/render" \
  -H "X-API-Key: $SNAPAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1 style=\"color:blue\">Hello</h1>", "width": 800, "height": 400}'
```

---

## Monitor a page for changes

```bash
curl -X POST "https://snapapi.tech/v1/monitor" \
  -H "X-API-Key: $SNAPAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://competitor.com/pricing", "interval": "1h", "webhook": "https://your-server.com/hook"}'
```

Fires a webhook when content changes — use for competitor price tracking, compliance monitoring, stock signals.

---

## Batch process multiple URLs

```bash
curl -X POST "https://snapapi.tech/v1/batch" \
  -H "X-API-Key: $SNAPAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://a.com", "https://b.com"], "action": "screenshot"}'
```

---

## Check your usage

```bash
curl "https://snapapi.tech/v1/usage" \
  -H "X-API-Key: $SNAPAPI_API_KEY"
```

Returns: `{ "used": 23, "limit": 100, "tier": "free", "resets": "2026-04-01" }`

---

## Agent prompting examples

```
Use snapapi to screenshot https://news.ycombinator.com and describe the top 5 stories.
```

```
Use snapapi_analyze on https://competitor.com and tell me their primary CTA and pricing structure.
```

```
Use snapapi to monitor https://example.com/pricing every hour and alert me when the price changes.
```

```
Use snapapi to batch-screenshot these 5 URLs and compare their layouts.
```

---

## Works great with

- **OpenClaw** — install the native plugin: `openclaw plugins install snapapi`
- **LangChain** — use as a tool via the REST API
- **n8n** — HTTP Request node pointing to any endpoint
- **AutoGPT / any agent** — standard REST, no SDKs required

---

Full docs: https://snapapi.tech/docs
Get your free API key: https://snapapi.tech

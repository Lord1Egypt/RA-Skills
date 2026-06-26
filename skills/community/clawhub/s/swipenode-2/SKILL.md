---
name: swipenode
description: Lightning-fast web extraction for AI agents. Extracts structured JSON from Next.js, Nuxt.js, Gatsby, Remix without headless browsers. TLS spoofing bypasses Cloudflare. 98% fewer tokens vs raw HTML. Use for e-commerce, news scraping, API-less data collection, or when web_fetch/browser overhead is too high.
metadata:
  clawdbot:
    emoji: "🦐"
    tags:
      - web-extraction
      - scraping
      - data-mining
      - cloudflare-bypass
      - llm-optimization
    requires:
      bins: []
      urls: []
    install: []
  triggers:
    - "web extraction"
    - "scrape"
    - "cloudflare"
    - "extract data"
    - "too many tokens"
    - "waf bypass"
    - "zero-render"
---

# SwipeNode Skill

Lightning-fast, zero-render web extraction CLI built for AI agents.  
Extracts structured data (Next.js/Nuxt.js) without headless browsers.

**Repo:** https://github.com/sirToby99/swipenode

---

## Binary

```
~/.openclaw/workspace/skills/swipenode/swipenode
```

Built from source (Go 1.24), single static binary, no runtime dependencies.

---

## Commands

### Extract (single URL)
```bash
~/.openclaw/workspace/skills/swipenode/swipenode extract --url <url>
```

### Extract + filter with jq
```bash
~/.openclaw/workspace/skills/swipenode/swipenode extract --url https://shop.example.com | jq '.props.pageProps.product'
```

### Batch (multiple URLs concurrently)
```bash
~/.openclaw/workspace/skills/swipenode/swipenode batch --urls "https://a.com,https://b.com"
```

### MCP Server (for Claude Desktop / local agents)
```bash
~/.openclaw/workspace/skills/swipenode/swipenode mcp
```

### Install as MCP in Claude Desktop
```bash
~/.openclaw/workspace/skills/swipenode/swipenode install-mcp
```

---

## What it extracts

| Framework | Data source |
|-----------|------------|
| Next.js | `__NEXT_DATA__` JSON blob |
| Nuxt.js | `window.__NUXT__` |
| Gatsby | `window.___gatsby` |
| Remix | `window.__remixContext` |
| JSON-LD | `<script type="application/ld+json">` |
| Fallback | Clean visible text (boilerplate stripped) |

**Smart pruning:** Strips tracking pixels, telemetry, base64 images, UI noise → up to 98% fewer tokens vs raw HTML.

---

## When to use vs web_fetch

| Situation | Tool |
|-----------|------|
| Data-rich site (Next.js shop, news portal) | **swipenode** |
| Cloudflare-protected site | **swipenode** (TLS spoofing) |
| Need structured JSON from React/Vue app | **swipenode** |
| Simple static page / docs | web_fetch |
| Need screenshots / DOM interaction | browser |
| 308/421 redirect errors | try web_fetch as fallback |

---

## Known Limitations

- HTTP 308/421 redirect errors on some CDN-hosted sites (e.g. vercel.com, nextjs.org) — use web_fetch as fallback
- No JavaScript execution — if data is loaded client-side only, won't help
- No DOM interaction (no clicks, forms)

---

## Examples

### HN front page (clean text fallback)
```bash
~/.openclaw/workspace/skills/swipenode/swipenode extract --url https://news.ycombinator.com
# Returns: clean list of titles, points, comments
```

### E-Commerce product data (Next.js)
```bash
~/.openclaw/workspace/skills/swipenode/swipenode extract --url https://shop.example.com/product/123 | jq '.props.pageProps'
```

### Token savings comparison
```
Raw HTML → LLM:      ~15.000 tokens (div soup, scripts, tracking)
SwipeNode extract:   ~300 tokens (clean structured JSON)
Savings:             ~98%
```

---

## Build from source

```bash
# Requires Go 1.24+
export PATH="/tmp/go/bin:$PATH"  # or system Go
git clone https://github.com/sirToby99/swipenode.git /tmp/swipenode-build
cd /tmp/swipenode-build
go build -o ~/.openclaw/workspace/skills/swipenode/swipenode .
```

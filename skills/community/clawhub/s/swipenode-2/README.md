# SwipeNode — Lightning-Fast Web Extraction for AI Agents

A zero-render web extraction CLI built specifically for AI agents. Extracts structured data from modern frameworks (Next.js, Nuxt.js, Gatsby, Remix) without headless browsers. Bypasses Cloudflare/Datadome via TLS fingerprint spoofing.

**Up to 98% fewer input tokens compared to raw HTML scraping.**

---

## Why SwipeNode?

Modern web frameworks embed their entire data layer as JSON in HTML source (`__NEXT_DATA__`, `window.__NUXT__`, etc.). SwipeNode reads it in milliseconds, no JavaScript execution needed.

### The Problem with Other Approaches

| Approach | Issues |
|----------|--------|
| **Headless Browsers** (Playwright, Puppeteer) | 200MB+ runtime, multi-second startup, breaks in containers, expensive at scale, blocked by WAFs |
| **Raw HTML to LLM** | Dumps `<div>`, `<script>`, CSS boilerplate—wastes 90%+ of input tokens |
| **Generic Scrapers** (BeautifulSoup, cheerio) | Blind to framework data, requires per-site glue code |
| **SwipeNode** ✅ | Single 16MB binary, no dependencies, structured JSON out, TLS spoofing for WAF bypass |

---

## Quick Start

### Installation

```bash
git clone https://github.com/Nefas11/swipenode.git
cd swipenode
go build -o swipenode .
chmod +x swipenode
```

**Requirements:** Go 1.24+

### Basic Usage

```bash
# Extract structured data from a URL
./swipenode extract --url https://example.com

# Extract + filter with jq
./swipenode extract --url https://shop.example.com | jq '.props.pageProps.product'

# Batch extract (concurrent)
./swipenode batch --urls "https://a.com,https://b.com"
```

### MCP Integration (Claude Desktop)

```bash
# Install as MCP server
./swipenode install-mcp

# Restart Claude Desktop → use with agents
```

---

## What Gets Extracted

### Framework Detection

| Framework | Source | Extracted |
|-----------|--------|-----------|
| **Next.js** | `__NEXT_DATA__` | Full page props, routing, data layer |
| **Nuxt.js** | `window.__NUXT__` | Component state, SSR data |
| **Gatsby** | `window.___gatsby` | Page metadata, static data |
| **Remix** | `window.__remixContext` | Route data, loaders |
| **JSON-LD** | `<script type="application/ld+json">` | Structured markup |
| **Fallback** | Clean HTML text | Visible text (boilerplate stripped) |

### Smart Pruning

- Removes tracking pixels, telemetry, base64 images
- Strips UI-only JSON (`_sentryBaggage`, ad configs, etc.)
- **Result:** Clean, LLM-optimized output

---

## Performance

```
Traditional web scraping (Playwright):
  Time:   2-5 seconds per page
  Memory: 200MB+ per process
  Cost:   High (server resources)

SwipeNode:
  Time:   50-300ms per page (avg 100ms)
  Memory: <2MB per request
  Cost:   Minimal (single binary)

Token Savings (for LLMs):
  Raw HTML → LLM:      15,000 tokens (boilerplate + tracking)
  SwipeNode extract:   300 tokens (clean structured JSON)
  Savings:             98%
```

---

## Use Cases

- **E-Commerce Automation** — Extract product data, prices, inventory
- **News Aggregation** — Parse article metadata without loading full pages
- **Market Research** — Scrape competitor pricing & specs  
- **AI Agent Data Sources** — Lightweight web access for LLM reasoning
- **Content Analysis** — Extract structure before feeding to LLMs

---

## Command Reference

### `extract`
```bash
./swipenode extract --url <url> [--headers "header1: value1"]
```
Single URL extraction with optional custom headers.

### `batch`
```bash
./swipenode batch --urls "url1,url2,url3" [--concurrency 10]
```
Concurrent extraction from multiple URLs.

### `mcp`
```bash
./swipenode mcp
```
Start stdio-based MCP server for Claude Desktop / local agents.

### `install-mcp`
```bash
./swipenode install-mcp
```
Auto-register SwipeNode with Claude Desktop config.

---

## Limitations

- **No JavaScript execution** — Client-side-only data won't be extracted
- **No DOM interaction** — Can't click, submit forms, or scroll
- **Redirect limits** — Some CDN sites (308/421 errors) may fail → use web_fetch as fallback
- **No screenshots** — Returns text/JSON only

---

## Architecture

SwipeNode uses TLS fingerprint spoofing (via `bogdanfinn/fhttp`) to bypass WAF detection while fetching raw HTML. It then:

1. Parses HTML efficiently (goquery)
2. Extracts framework-specific JSON (`__NEXT_DATA__`, etc.)
3. Prunes boilerplate & telemetry
4. Returns clean JSON or plain text

Single binary, zero external dependencies at runtime.

---

## Integration with OpenClaw

SwipeNode is available as an OpenClaw Skill for local AI agents:

```bash
~/.openclaw/workspace/skills/swipenode/swipenode extract --url https://example.com
```

Use in agent tasks when you need lightweight, fast web extraction without browser overhead.

---

## License

FSL 1.1 (Fair Source License)

---

## Contributing

SwipeNode is open source. Contributions welcome — submit PRs or issues on GitHub.

---

## Credits

Built by **sirToby99** — https://github.com/sirToby99/swipenode

OpenClaw integration by **Nefas11**

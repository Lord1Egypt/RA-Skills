---
name: surfagent
description: Control a real Chrome browser via SurfAgent — navigate, click, type, screenshot, extract data, crawl sites, and automate web workflows. Uses your persistent Chrome profile with real cookies and sessions. Works through SurfAgent's MCP server or direct HTTP API.
version: 1.0.0
author: MoonstoneLabs
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [browser, automation, web, scraping, chrome, mcp, surfagent]
    category: browser-automation
    related_skills: []
    requires_tools: []
required_environment_variables:
  - name: SURFAGENT_DAEMON_URL
    prompt: "SurfAgent daemon URL (default: http://localhost:7201)"
    help: "Install SurfAgent from https://surfagent.app — the daemon runs on localhost:7201 by default"
    required_for: "browser control"
---

# SurfAgent — Real Chrome Browser Control

Give your AI agent a real, persistent Chrome browser. No headless browsers, no cloud, no bot detection issues.

## When to Use

- You need to browse, scrape, or interact with a website
- You need to fill forms, click buttons, or navigate pages
- You need to extract structured data from web pages
- You need to take screenshots of websites
- You need persistent login sessions (already logged into sites)
- You need to bypass bot detection (Cloudflare, hCaptcha, etc.)
- You need to crawl/map a website

## Prerequisites

1. **SurfAgent installed and running** — download from [surfagent.app](https://surfagent.app)
2. **MCP server connected** — `hermes mcp add surfagent --command npx --args -y surfagent-mcp`
3. Or use the HTTP API directly at `http://localhost:7201`

## Quick Reference — MCP Tools (24)

| Tool | What it does |
|------|-------------|
| `browser_navigate` | Open a URL |
| `browser_back` | Go back in history |
| `browser_forward` | Go forward in history |
| `browser_click` | Click an element (selector, text, or coordinates) |
| `browser_type` | Type text into an element |
| `browser_fill_form` | Fill multiple form fields at once |
| `browser_select` | Select dropdown option |
| `browser_scroll` | Scroll page or to element |
| `browser_screenshot` | Capture page screenshot (PNG) |
| `browser_get_text` | Get visible text content |
| `browser_get_html` | Get page HTML |
| `browser_get_url` | Get current URL |
| `browser_get_title` | Get page title |
| `browser_find_elements` | Find elements by CSS selector |
| `browser_evaluate` | Run JavaScript in page |
| `browser_wait` | Wait for element to appear |
| `browser_cookies` | Get or set cookies |
| `browser_list_tabs` | List open tabs |
| `browser_new_tab` | Open new tab |
| `browser_switch_tab` | Switch to tab by id/title |
| `browser_close_tab` | Close a tab |
| `browser_extract` | Extract structured data (markdown, JSON, links) |
| `browser_crawl` | BFS crawl a domain |
| `browser_map` | Discover all URLs on a site |

## Procedure

### Basic Navigation
1. Use `browser_navigate` to open a URL
2. Use `browser_screenshot` to see the page
3. Use `browser_click` or `browser_type` to interact
4. Use `browser_get_text` to read content

### Data Extraction
1. Use `browser_extract` with a URL to get markdown + links
2. Add `prompt` and `schema` fields for LLM-powered structured extraction
3. Use `browser_crawl` for multi-page extraction
4. Use `browser_map` for quick URL discovery

### Form Filling
1. Use `browser_navigate` to go to the form page
2. Use `browser_fill_form` with field label/name → value mappings
3. Or use `browser_click` + `browser_type` for individual fields
4. Use `browser_select` for dropdowns

### Tab Management
1. Use `browser_list_tabs` to see what's open
2. Use `browser_new_tab` to open a new tab
3. Use `browser_switch_tab` to change focus
4. Use `browser_close_tab` when done — always clean up tabs

### Direct HTTP API (fallback)
If MCP isn't available, call the daemon directly:
```bash
# Navigate
curl -X POST http://localhost:7201/browser/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com"}'

# Screenshot
curl -s http://localhost:7201/browser/screenshot --output screenshot.png

# List tabs
curl -s http://localhost:7201/browser/tabs

# Extract page data
curl -X POST http://localhost:7201/browser/extract \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "formats": ["markdown", "links"]}'
```

## Key Advantages

- **Real Chrome** — not headless, passes all bot detection
- **Persistent sessions** — log in once, stay logged in forever
- **Real fingerprint** — your actual Chrome installation, real cookies
- **100% local** — no data leaves your machine
- **24 MCP tools** — comprehensive browser control
- **Extract + Crawl** — Firecrawl-equivalent features, zero cloud cost

## Pitfalls

- **Always close tabs when done** — leaving tabs open wastes resources
- **Wait for dynamic content** — SPAs need `browser_wait` or a short delay after navigation
- **One operation at a time** — don't fire multiple browser commands in parallel
- **Screenshots are viewport-only by default** — use the fullPage option for long pages
- **Cookie consent banners** — the daemon can auto-resolve them via `/browser/resolve-blocker`

## Verification

- `browser_get_url` returns the expected URL after navigation
- `browser_screenshot` shows the expected page content
- `browser_get_text` contains the expected text
- Health check: `curl http://localhost:7201/health` returns `{"ok": true}`

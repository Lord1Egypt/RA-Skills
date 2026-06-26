# web-markdown-scraper

> OpenClaw skill · Scrapling-powered webpage → Markdown converter

[![ClawHub](https://img.shields.io/badge/ClawHub-web--markdown--scraper-blue)](https://clawhub.ai)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Fetch any public webpage and get clean Markdown back. Handles static pages, JavaScript-heavy SPAs,
and anti-bot-protected sites. Supports concurrent batch scraping and production-grade element
tracking via Scrapling's automatch fingerprint system.

## Features

- **4 Fetcher modes**: `http` · `async` (concurrent) · `stealth` (Camoufox/Firefox anti-bot) · `dynamic` (Playwright Chromium)
- **AutoMatch**: CSS selector fingerprinting — finds elements even after site redesigns
- **Proxy support**: URL string or `{"server":"","username":"","password":""}` JSON
- **Human fingerprint simulation**: `--humanize`, `--geoip`, `--block-webrtc`
- **Performance flags**: `--disable-resources`, `--block-images`, `--network-idle`
- **Retry with exponential backoff**: `--retry N`
- **Structured JSON output** with per-page title, Markdown, status, and optional file save

## Installation

```bash
# Install via OpenClaw
openclaw skill install web-markdown-scraper

# Install Python dependencies manually (if needed)
pip install scrapling html2text
playwright install chromium
python -m camoufox fetch
```

## Quick Start

```bash
# Static page
python3 scripts/scrape_to_markdown.py --url "https://example.com"

# Anti-bot site
python3 scripts/scrape_to_markdown.py --url "https://example.com" --mode stealth --network-idle

# Batch scraping (concurrent)
python3 scripts/scrape_to_markdown.py --mode async --url "https://a.com" --url "https://b.com"

# Target specific content + save files
python3 scripts/scrape_to_markdown.py --url "https://example.com" \
  --selector "article" --preserve-links --output-dir ./outputs
```

## Usage Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--url URL` | — | Target URL (repeat for multiple) |
| `--url-file FILE` | — | Text file with one URL per line |
| `--mode` | `http` | `http` / `async` / `stealth` / `dynamic` |
| `--selector CSS` | full page | CSS selector for main content |
| `--preserve-links` | off | Keep hyperlinks in Markdown |
| `--output-dir DIR` | — | Save `.md` files + `index.json` here |
| `--auto-save` | off | Save element fingerprints (first run) |
| `--auto-match` | off | Recover elements after layout change |
| `--network-idle` | off | Wait for network quiet before capture |
| `--block-images` | off | Block image loading |
| `--disable-resources` | off | Drop fonts/media/styles |
| `--wait-selector CSS` | — | Wait for DOM element |
| `--timeout MS` | 30000 | Global timeout |
| `--humanize SEC` | — | Human cursor simulation (stealth) |
| `--geoip` | off | Spoof locale from proxy IP (stealth) |
| `--proxy URL/JSON` | — | Proxy config (stealth/dynamic) |
| `--retry N` | 0 | Retry on failure with backoff |

## Output Format

```json
{
  "ok": true,
  "total": 1,
  "succeeded": 1,
  "failed": 0,
  "results": [
    {
      "ok": true,
      "url": "https://example.com",
      "status": 200,
      "title": "Example Domain",
      "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples...",
      "markdown_length": 312,
      "output_markdown_file": "outputs/example-domain.md"
    }
  ]
}
```

## AutoMatch Workflow

AutoMatch lets Scrapling re-locate your target element even after the website is redesigned.

```bash
# Step 1 — first run: save the element fingerprint
python3 scripts/scrape_to_markdown.py --url "https://news.site/article" \
  --selector ".article-body" --auto-save

# Step 2 — after the site redesigns: still works, no selector update needed
python3 scripts/scrape_to_markdown.py --url "https://news.site/article" \
  --selector ".article-body" --auto-match
```

## Security

- No API keys or credentials required
- Network calls go **only** to user-supplied URLs
- Proxy credentials are never logged
- No background processes; exits after each run
- See [SKILL.md](SKILL.md) for full security disclosure

## License

MIT

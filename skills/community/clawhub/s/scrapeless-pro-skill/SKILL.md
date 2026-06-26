---
name: scrapeless-pro
description: "Professional web scraping for OpenClaw — stealth Playwright automation with anti-bot bypass, JavaScript rendering, and structured data extraction from any modern website."
version: 1.0.3
homepage: https://cosmic-lollipop-a61cc5.netlify.app
license: "Commercial"
metadata:
  clawdbot:
    emoji: "🕷️"
    category: "web-automation"
    requires:
      bins: ["node", "npx"]
      env: ["SCRAPELESS_LICENSE_KEY"]
---

# Scrapeless Pro 🕷️

**Professional web scraping for OpenClaw.** Stealth Playwright automation that renders JavaScript, bypasses anti-bot detection, and extracts structured data from any modern website.

> OpenClaw's built-in web_fetch fails on 75% of JavaScript-heavy sites. Scrapeless Pro fixes that.

## Why Scrapeless Pro?

- **JavaScript rendering** — Works on React, Vue, SPA, and dynamic sites
- **Stealth mode** — Random user-agent, viewport, fingerprint masking, anti-detection scripts
- **Auto data extraction** — Headings, links, paragraphs, images, meta tags
- **Custom selectors** — Target specific elements with CSS selectors
- **Multiple formats** — JSON, CSV, Markdown output
- **CLI & programmatic** — Use from command line or import in your skills

## Purchase License

**$49 one-time** — Lifetime license, 1 year of updates included.

Get your license: https://cosmic-lollipop-a61cc5.netlify.app

## Setup

### 1. Install

```bash
clawhub install scrapeless-pro
```

### 2. Set License Key

```bash
export SCRAPELESS_LICENSE_KEY="SCRAPELESS-XXXX-XXXX-XXXX-XXXX"
```

### 3. Install Playwright (if not already)

```bash
npm install playwright
npx playwright install chromium
```

## Usage

### CLI

```bash
# Basic scrape
node scraper.js scrape https://example.com

# With output format
node scraper.js scrape https://example.com --format csv
node scraper.js scrape https://example.com --format markdown

# Save to file
node scraper.js scrape https://example.com -o data.json

# Custom selectors
node scraper.js scrape https://example.com --selectors '{"products":".product","prices":".price"}'

# Validate license
node scraper.js validate
```

### OpenClaw Agent

Ask your OpenClaw agent:
```
scrape https://example.com/products and extract all product names and prices
```

### Programmatic

```javascript
const { scrape } = require('scrapeless-pro');

const data = await scrape('https://quotes.toscrape.com', {
    format: 'json',
    headless: true,
});
console.log(data.title);
console.log(data.headings);
```

## Real Output Example

Tested with https://quotes.toscrape.com (2026-04-18):

```json
{
  "title": "Quotes to Scrape",
  "url": "https://quotes.toscrape.com/",
  "timestamp": "2026-04-18T11:15:40.071Z",
  "headings": [
    { "level": "H1", "text": "Quotes to Scrape" },
    { "level": "H2", "text": "Top Ten tags" }
  ],
  "links": [
    { "text": "Login", "href": "https://quotes.toscrape.com/login" },
    { "text": "(about)", "href": "https://quotes.toscrape.com/author/Albert-Einstein" },
    { "text": "change", "href": "https://quotes.toscrape.com/tag/change/page/1/" }
  ],
  "paragraphs": ["Login", "Quotes by: GoodReads.com"]
}
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --format` | Output format: json, csv, markdown | json |
| `-s, --selectors` | CSS selectors as JSON | auto-detect |
| `-o, --output` | Save to file | stdout |
| `-t, --timeout` | Navigation timeout (ms) | 30000 |
| `-d, --delay` | Random delay before navigation (ms) | 1000 |
| `--no-headless` | Show browser window | hidden |

## Stealth Features

- Random user-agent rotation (5 realistic agents)
- Random viewport sizes (1920x1080, 1366x768, etc.)
- Navigator.webdriver override (hides automation flag)
- Chrome runtime injection
- Function.prototype.toString override
- Permissions API spoofing
- Random scroll behavior
- Realistic navigation delays

## Dependencies

- `playwright` — Browser automation
- `commander` — CLI interface

No external APIs, no paid services, no data sent to third parties.

## Support

- Email: showmemercy19@gmail.com
- License: https://cosmic-lollipop-a61cc5.netlify.app

---

*Scrapeless Pro v1.0.3 — Commercial skill for OpenClaw*
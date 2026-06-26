---
name: Scrapling Web Scraping
description: Zero-bot-detection web scraping for OpenClaw. Bypass Cloudflare, handle JavaScript-heavy sites, and adapt to website changes automatically. Use when you need to scrape protected websites, extract data from dynamic JavaScript SPAs, or bypass anti-bot detection systems. Supports three modes - basic (fast HTTP), stealth (undetectable), dynamic (browser automation).
identifier: scrapling-web-scraping
version: 1.0.0
author: 老二
category: web-scraping
---

# Scrapling Web Scraping

Zero-bot-detection web scraping for OpenClaw. Bypass Cloudflare, handle JavaScript-heavy sites, and adapt to website changes automatically.

## Quick Start

```bash
# Install Scrapling
pip install "scrapling[all]"
scrapling install

# Basic usage
python3 /root/.openclaw/skills/scrapling-web-scraping/scrapling_tool.py https://example.com

# Bypass Cloudflare
python3 /root/.openclaw/skills/scrapling-web-scraping/scrapling_tool.py https://protected-site.com --mode stealth --cloudflare

# Extract specific data
python3 /root/.openclaw/skills/scrapling-web-scraping/scrapling_tool.py https://example.com --selector ".product-title"

# JavaScript-heavy sites
python3 /root/.openclaw/skills/scrapling-web-scraping/scrapling_tool.py https://spa-app.com --mode dynamic --wait ".content-loaded"
```

## Usage with OpenClaw

### Natural Language Commands

**Basic scraping:**
> "用Scrapling抓取 https://example.com 的标题和所有链接"

**Bypass protection:**
> "用隐身模式抓取 https://protected-site.com，绕过Cloudflare"

**Extract data:**
> "抓取 https://shop.com 的商品名称和价格，CSS选择器是 .product"

**Dynamic content:**
> "抓取 https://spa-app.com，等待 .data-loaded 元素加载完成"

### Python Code

```python
# Basic scraping
from scrapling.fetchers import Fetcher
page = Fetcher.get('https://example.com')
title = page.css('title::text').get()

# Bypass Cloudflare
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch('https://protected.com', 
                              headless=True, 
                              solve_cloudflare=True)

# JavaScript sites
from scrapling.fetchers import DynamicFetcher
page = DynamicFetcher.fetch('https://spa-app.com', 
                             headless=True, 
                             network_idle=True)
```

## Features

| Feature | Command | Description |
|---------|---------|-------------|
| Basic Scrape | `--mode basic` | Fast HTTP requests |
| Stealth Mode | `--mode stealth` | Bypass Cloudflare/anti-bot |
| Dynamic Mode | `--mode dynamic` | Handle JavaScript sites |
| CSS Selectors | `--selector ".class"` | Extract specific elements |
| JSON Output | `--json` | Machine-readable output |

## Examples

### 1. Scrape with CSS Selector
```bash
python3 scrapling_tool.py https://quotes.toscrape.com --selector ".quote .text" --json
```

### 2. Bypass Cloudflare
```bash
python3 scrapling_tool.py https://nopecha.com/demo/cloudflare --mode stealth --cloudflare
```

### 3. Wait for Dynamic Content
```bash
python3 scrapling_tool.py https://spa-app.com --mode dynamic --wait ".loaded" --json
```

## CLI Reference

```
python3 scrapling_tool.py URL [options]

Options:
  --mode {basic,stealth,dynamic}  Scraping mode (default: basic)
  --selector, -s CSS_SELECTOR     Extract specific elements
  --cloudflare                    Solve Cloudflare (stealth mode only)
  --wait SELECTOR                 Wait for element (dynamic mode only)
  --json, -j                      Output as JSON
```

## Advanced: Custom Scripts

Create custom scraping scripts in `/root/.openclaw/skills/scrapling-web-scraping/`:

```python
from scrapling.fetchers import StealthyFetcher

# Your custom scraper
def scrape_products(url):
    page = StealthyFetcher.fetch(url, headless=True)
    products = []
    for item in page.css('.product'):
        products.append({
            'name': item.css('.name::text').get(),
            'price': item.css('.price::text').get(),
            'link': item.css('a::attr(href)').get()
        })
    return products
```

## Notes

- Requires Python 3.10+
- First run: `scrapling install` to download browsers
- Respect website Terms of Service
- Use responsibly

---

**Created**: 2026-03-05 by 老二
**Source**: https://github.com/D4Vinci/Scrapling

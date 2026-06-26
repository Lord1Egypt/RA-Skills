---
name: sitemap-generator
description: Generate XML sitemaps by crawling a website. Use when a user needs to create a sitemap.xml for SEO, audit site structure, discover all pages on a domain, or generate a sitemap for submission to Google Search Console or other search engines. Handles BFS crawling with configurable depth, page limits, and polite delays.
---

# Sitemap Generator

Crawl any website and produce a standards-compliant XML sitemap ready for search engine submission.

## Quick Start

```bash
python3 scripts/sitemap_gen.py https://example.com
```

Output: `sitemap.xml` in the current directory.

## Commands

```bash
# Basic — crawl and write sitemap.xml
python3 scripts/sitemap_gen.py https://example.com

# Custom output path
python3 scripts/sitemap_gen.py https://example.com -o /tmp/sitemap.xml

# Limit crawl scope
python3 scripts/sitemap_gen.py https://example.com --max-pages 500 --max-depth 3

# Polite crawling with delay
python3 scripts/sitemap_gen.py https://example.com --delay 1.0

# Set SEO hints
python3 scripts/sitemap_gen.py https://example.com --changefreq daily --priority 0.8

# Verbose progress
python3 scripts/sitemap_gen.py https://example.com -v

# Pipe to stdout
python3 scripts/sitemap_gen.py https://example.com -o -
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output, -o` | `sitemap.xml` | Output file path (use `-` for stdout) |
| `--max-pages` | `200` | Maximum pages to crawl |
| `--max-depth` | `5` | Maximum link depth from start URL |
| `--delay` | `0.2` | Seconds between requests |
| `--timeout` | `10` | Request timeout in seconds |
| `--changefreq` | `weekly` | Sitemap changefreq hint |
| `--priority` | `0.5` | Sitemap priority hint (0.0–1.0) |
| `--verbose, -v` | off | Print crawl progress to stderr |

## Dependencies

```bash
pip install requests beautifulsoup4
```

## Notes

- Only crawls same-domain pages (no external links)
- Skips binary files (images, CSS, JS, PDFs, fonts)
- Respects the delay setting to avoid overwhelming servers
- Output conforms to the sitemaps.org 0.9 protocol

---
name: sitemap-generator
description: Generate XML sitemaps by crawling a website or scanning local files. Auto-discovers pages via link extraction. Supports local HTML/MD file scanning with lastmod dates. Generates robots.txt with sitemap reference. Use when asked to create a sitemap, generate sitemap.xml, crawl a site for pages, create robots.txt, or prepare a site for SEO. Triggers on "sitemap", "sitemap.xml", "crawl site", "site map", "robots.txt", "SEO sitemap".
---

# Sitemap Generator

Generate XML sitemaps by crawling a live website or scanning local HTML files.

## Crawl a Website

```bash
python3 scripts/sitemap_gen.py https://example.com
```

## Scan Local Files

```bash
python3 scripts/sitemap_gen.py --local ./public --base-url https://example.com
```

## Save to File

```bash
# Save sitemap.xml
python3 scripts/sitemap_gen.py https://example.com --output sitemap.xml

# Save sitemap.xml + robots.txt
python3 scripts/sitemap_gen.py https://example.com --output sitemap.xml --robots
```

## Output Formats

```bash
# XML (default — valid sitemap.xml)
python3 scripts/sitemap_gen.py https://example.com

# Text (human-readable summary + XML)
python3 scripts/sitemap_gen.py https://example.com --format text

# JSON (pages list + XML string)
python3 scripts/sitemap_gen.py https://example.com --format json
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max-pages` | 500 | Maximum pages to crawl |
| `--timeout` | 10 | Request timeout in seconds |
| `--output` / `-o` | stdout | Save sitemap.xml to file |
| `--robots` | off | Also generate robots.txt |
| `--local` | off | Scan local directory instead of crawling |
| `--base-url` | — | Base URL for local mode (required) |
| `--verbose` / `-v` | off | Show crawl progress |

## Features

- **Crawl mode:** BFS link discovery, same-domain only, deduplication
- **Local mode:** Scan HTML/HTM/MD/PHP files, auto-detect lastmod from file mtime
- **Smart filtering:** Skips images, CSS, JS, PDFs, archives, media files
- **URL normalization:** Removes fragments, normalizes trailing slashes
- **robots.txt generation:** User-agent + Allow + Sitemap reference
- **Valid XML:** Proper XML escaping, sitemaps.org schema

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)

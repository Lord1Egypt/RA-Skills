---
name: smart-scraper
description: AI-powered web scraper with intelligent structure recognition. Extracts lists, articles, and tables from any website with automatic type detection.
metadata:
  openclaw:
    emoji: "🕷️"
    requires:
      bins: [node, npm]
    install:
      - kind: node
        package: "playwright"
        bins: [npx]
---

# Smart Scraper

Intelligent web scraping that understands page structure.

## Features

- **Auto-detection**: Automatically identifies list, article, or table layouts
- **Smart extraction**: Parses prices, dates, URLs from unstructured text
- **Multiple formats**: Output as JSON, CSV, or Markdown
- **Scroll support**: Handles infinite scroll pages

## Usage

```bash
# Extract product listings
smart-scraper --url "https://example.com/products" --type list

# Extract article content
smart-scraper --url "https://example.com/article" --type article --format markdown

# Extract table data
smart-scraper --url "https://example.com/data" --type table --format csv
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url, -u` | Target URL (required) | - |
| `--type, -t` | Extraction type: `list`, `article`, `table`, `auto` | `auto` |
| `--format, -f` | Output format: `json`, `csv`, `markdown` | `json` |
| `--max, -m` | Maximum items to extract | 100 |
| `--scroll` | Enable auto-scroll for lazy-loaded content | false |

## Examples

### Extract Hacker News
```bash
smart-scraper -u https://news.ycombinator.com -t list -m 10
```

### Save article as Markdown
```bash
smart-scraper -u https://blog.example.com/post -t article -f markdown > article.md
```

### Export table to CSV
```bash
smart-scraper -u https://example.com/prices -t table -f csv > prices.csv
```

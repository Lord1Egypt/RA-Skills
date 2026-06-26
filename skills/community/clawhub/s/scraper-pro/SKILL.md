---
name: data-scraper
description: Extract data from websites and APIs for analysis. Use when user needs to collect product prices from e-commerce sites, gather news articles, extract structured data from web pages, build datasets from public sources, or automate data collection for research.
---

# Data Scraper

Extract structured data from websites and APIs.

## Quick Start

```bash
# Basic page scrape
python scripts/scrape.py https://example.com --output data.json
```

## Core Features

- **CSS/XPath selectors**: Target specific elements
- **Multiple output formats**: JSON, CSV, Markdown
- **Pagination support**: Scrape multiple pages
- **Rate limiting**: Respect server limits
- **Authentication**: Handle login/sessions

## Usage

```bash
python scripts/scrape.py [OPTIONS]

Options:
  --url TEXT          URL to scrape (required)
  --selector TEXT     CSS selector for data extraction
  --output PATH       Output file path
  --format FORMAT     Output format: json, csv, markdown
  --limit NUM         Maximum items to scrape
  --wait SECS         Wait between requests
  --login URL         Login URL for authenticated scraping
```

## Examples

### Product Price Collection
```bash
python scripts/scrape.py \
  --url "https://example.com/products" \
  --selector ".product" \
  --output prices.json \
  --format json
```

### News Article Aggregation
```bash
python scripts/scrape.py \
  --url "https://news.example.com/latest" \
  --selector "article" \
  --output news.md \
  --format markdown
```

## Configuration File

Create `scrape.yaml` for complex scraping:

```yaml
url: https://example.com/products
selectors:
  items: ".product-card"
  title: ".product-title"
  price: ".price::text"
  image: "img::attr(src)"
  link: "a::attr(href)"

pagination:
  type: click
  button: ".next-page"
  max_pages: 10

output:
  format: json
  file: products.json
```

## Best Practices

1. Check robots.txt before scraping
2. Add delays between requests
3. Cache responses for development
4. Handle errors gracefully
5. Store raw HTML for debugging

## Legal Note

Ensure you have permission to scrape target websites. Check Terms of Service and robots.txt.

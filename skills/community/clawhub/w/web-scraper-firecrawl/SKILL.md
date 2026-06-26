---
name: firecrawl
description: Web scraping and content extraction using Firecrawl API. Use when users need to crawl websites, extract structured data, convert web pages to markdown, scrape multiple URLs, or build knowledge bases from web content. Supports single page extraction, site-wide crawling, batch processing, and structured data extraction with CSS selectors.
---

# Firecrawl Skill

Powerful web scraping powered by [Firecrawl](https://github.com/mendableai/firecrawl) - turn websites into LLM-ready markdown.

## Overview

Firecrawl provides APIs for:
- **Scrape** - Single page extraction to markdown
- **Crawl** - Entire site crawling with depth control
- **Map** - URL discovery from a starting point
- **Batch** - Multiple URL processing
- **Extract** - Structured data extraction with schemas

## Prerequisites

1. **Firecrawl API Key** - Get free tier at https://firecrawl.dev
2. Install Python dependencies: `requests`

## Configuration

Set environment variable:
```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

## Usage

### Single Page Scraping
```bash
# Basic scrape
firecrawl scrape https://example.com

# With specific options
firecrawl scrape https://example.com --formats markdown,html --only-main-content

# Wait for JS rendering
firecrawl scrape https://spa-app.com --wait-for 2000
```

### Site Crawling
```bash
# Crawl entire site (up to limit)
firecrawl crawl https://docs.example.com --limit 50

# With depth control
firecrawl crawl https://blog.example.com --max-depth 2 --limit 100

# Include/exclude patterns
firecrawl crawl https://site.com --include "/blog/*" --exclude "/admin/*"

# Custom formats
firecrawl crawl https://docs.example.com --formats markdown,links
```

### URL Mapping
```bash
# Discover all URLs from a site
firecrawl map https://example.com

# With search term
firecrawl map https://docs.python.org --search "tutorial"
```

### Batch Processing
```bash
# Scrape multiple URLs
firecrawl batch urls.txt --output ./scraped/

# From JSON list
firecrawl batch urls.json --formats markdown --concurrency 5
```

### Structured Extraction
```bash
# Extract specific data using CSS selectors
firecrawl extract https://example.com/products \
  --schema '{"name": ".product-title", "price": ".price", "description": ".desc"}'

# Extract to JSON
firecrawl extract https://news.example.com/article --schema article-schema.json
```

## Output Formats

### Markdown
Clean, LLM-ready markdown with:
- Headings preserved
- Links converted to markdown format
- Images with alt text
- Tables formatted as markdown tables

### HTML
Raw or cleaned HTML

### Links
Extracted link lists for further crawling

### Screenshot
Page screenshot (if requested)

## Use Cases

### Knowledge Base Building
```bash
# Crawl documentation site
firecrawl crawl https://docs.framework.com --limit 200 -o ./kb/

# Merge into single file for RAG
cat ./kb/*.md > knowledge-base.md
```

### Research & Analysis
```bash
# Scrape competitor pricing
firecrawl batch competitors.txt --extract pricing-schema.json

# Monitor blog updates
firecrawl map https://blog.company.com --since 2024-01-01
```

### Content Migration
```bash
# Export old CMS content
firecrawl crawl https://old-site.com --formats markdown,html -o ./export/
```

## Scripts

All functionality via `scripts/firecrawl.py`:
- Handles API authentication
- Automatic rate limiting
- Retry logic for failures
- Progress tracking for large crawls

## Integration

Works well with:
- `markdown-sync-pro` - Sync scraped content to Notion/GitHub
- `arxiv-paper` - Combine with academic paper downloads
- `maybe-finance` - Scrape financial data for analysis

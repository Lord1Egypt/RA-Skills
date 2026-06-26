---
name: web-scraper
description: Extract structured data from websites using browser automation. Use when scraping product listings, articles, contact info, prices, or any web content. Supports single pages, pagination, infinite scroll, and dynamic content. Outputs to CSV, JSON, or Excel.
---

# Web Scraper

## Overview

Professional web scraping skill using agent-browser. Extract structured data from any website with support for JavaScript-rendered content, pagination, and complex selectors.

## Use Cases

- **E-commerce**: Product listings, prices, reviews, inventory
- **Real Estate**: Property listings, prices, agent contacts
- **Job Boards**: Job postings, salaries, requirements
- **News/Media**: Articles, headlines, publication dates
- **Directories**: Business listings, contact information
- **Competitor Monitoring**: Prices, products, content changes

## Quick Start

### Scrape Single Page

```bash
python scripts/scrape_page.py \
  --url "https://example.com/products" \
  --fields "title= h2.title,price=.price,link=a.href" \
  --output products.csv
```

### Scrape with Pagination

```bash
python scripts/scrape_paginated.py \
  --url "https://example.com/products?page={page}" \
  --pages 10 \
  --fields "title,price,description" \
  --output all_products.csv
```

## Scripts

### scrape_page.py

Scrape a single page or static list.

**Arguments:**
- `--url` - Target URL
- `--fields` - Field definitions (name=selector format, comma-separated)
- `--output` - Output file (CSV, JSON, or XLSX)
- `--format` - Output format (csv, json, xlsx)
- `--wait` - Wait time for dynamic content (seconds)

**Field Definition Format:**
```
fieldname=css_selector
```

Examples:
```
title=h1.product-title
price=.price-tag
description=.product-description
image=img.product-image.src
link=a.product-link.href
```

### scrape_paginated.py

Scrape multiple pages with pagination.

**Arguments:**
- `--url` - URL pattern (use {page} for page number)
- `--pages` - Number of pages to scrape
- `--fields` - Field definitions
- `--output` - Output file
- `--delay` - Delay between pages (seconds)
- `--next-selector` - CSS selector for "next page" button (alternative to URL pattern)

### scrape_infinite_scroll.py

Scrape pages with infinite scroll loading.

**Arguments:**
- `--url` - Target URL
- `--scrolls` - Number of scroll actions
- `--fields` - Field definitions
- `--output` - Output file
- `--scroll-delay` - Delay between scrolls (ms)

### scrape_dynamic.py

Scrape JavaScript-heavy sites with custom interactions.

**Arguments:**
- `--url` - Target URL
- `--actions` - JSON file with interaction sequence
- `--fields` - Field definitions
- `--output` - Output file

## Configuration

### Actions JSON Format (for dynamic scraping)

```json
{
  "actions": [
    {"type": "click", "selector": "#load-more"},
    {"type": "wait", "ms": 2000},
    {"type": "scroll", "direction": "down", "pixels": 500},
    {"type": "fill", "selector": "#search", "value": "keyword"},
    {"type": "press", "key": "Enter"}
  ]
}
```

### Output Formats

**CSV:**
```csv
title,price,link,url
"Product A",29.99,https://...,https://...
"Product B",39.99,https://...,https://...
```

**JSON:**
```json
[
  {
    "title": "Product A",
    "price": "29.99",
    "link": "https://...",
    "scraped_at": "2026-03-07T16:00:00"
  }
]
```

**Excel (XLSX):**
- Same as CSV but with formatting options
- Multiple sheets support
- Auto-fit columns

## Examples

### Example 1: Scrape E-commerce Products

```bash
python scripts/scrape_paginated.py \
  --url "https://example.com/shop?page={page}" \
  --pages 5 \
  --fields "name=.product-name,price=.price,rating=.stars,reviews=.review-count,url=a.href" \
  --output products.csv \
  --delay 3
```

### Example 2: Scrape News Articles

```bash
python scripts/scrape_page.py \
  --url "https://news-site.com/latest" \
  --fields "headline=h2.article-title,summary=.article-summary,author=.byline,date=.publish-date,url=a.read-more.href" \
  --output articles.json \
  --format json
```

### Example 3: Scrape Job Postings

```bash
python scripts/scrape_infinite_scroll.py \
  --url "https://jobs-site.com/search" \
  --scrolls 10 \
  --fields "title=.job-title,company=.company-name,location=.location,salary=.salary,posted=.date-posted,url=a.job-link.href" \
  --output jobs.csv \
  --scroll-delay 1500
```

### Example 4: Scrape Real Estate Listings

```bash
python scripts/scrape_paginated.py \
  --url "https://realestate.com/listings?page={page}" \
  --pages 20 \
  --fields "address=.property-address,price=.listing-price,beds=.bedrooms,baths=.bathrooms,sqft=.square-feet,url=a.property-link.href" \
  --output listings.xlsx \
  --format xlsx \
  --delay 5
```

## Best Practices

1. **Respect robots.txt** - Check and follow site rules
2. **Rate limiting** - Add delays between requests (2-5s recommended)
3. **Error handling** - Handle missing elements gracefully
4. **User-Agent** - Use realistic browser headers
5. **Retry logic** - Implement retries for failed requests
6. **Data validation** - Validate extracted data before saving
7. **Storage** - Save intermediate results for long scrapes

## Anti-Scraping Measures

Some sites employ anti-scraping techniques:

| Measure | Countermeasure |
|---------|----------------|
| IP blocking | Use proxies, rotate IPs |
| CAPTCHA | Manual solving or CAPTCHA services |
| Rate limiting | Increase delays, randomize timing |
| JavaScript challenges | Use browser automation (agent-browser) |
| Honeypot traps | Avoid hidden fields, validate selectors |

## Legal Considerations

- **Public data**: Generally legal to scrape
- **Terms of Service**: Review site ToS before scraping
- **Copyright**: Don't republish copyrighted content
- **Personal data**: GDPR/privacy laws may apply
- **Commercial use**: May require permission

**Disclaimer**: This skill is for educational purposes. Users are responsible for compliance with applicable laws and website terms.

## Troubleshooting

- **Elements not found**: Verify CSS selectors with browser dev tools
- **Empty results**: Check if content is JavaScript-rendered (use dynamic scraping)
- **Timeout errors**: Increase wait time or check network
- **Blocked requests**: Add delays, rotate user agents, or use proxies
- **Incomplete data**: Verify pagination or scroll handling

## References

### CSS Selector Guide

See `references/css-selectors.md` for comprehensive selector examples.

### Common Website Patterns

See `references/website-patterns.md` for common HTML structures and selectors.

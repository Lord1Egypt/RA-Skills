# Smart Scraper Skill

AI-powered web scraping with intelligent structure recognition.

## Usage

```bash
# Scrape a product listing page
npm run scrape -- --url "https://example.com/products" --type list

# Scrape an article
npm run scrape -- --url "https://example.com/article" --type article

# Scrape a table
npm run scrape -- --url "https://example.com/data" --type table

# Output as JSON
npm run scrape -- --url "..." --format json

# Output as CSV
npm run scrape -- --url "..." --format csv
```

## Features

- **List Extraction**: Product listings, search results, directories
- **Article Extraction**: News, blog posts with metadata
- **Table Extraction**: Structured data tables
- **Price Monitoring**: Track price changes over time
- **Multi-format Output**: JSON, CSV, Markdown

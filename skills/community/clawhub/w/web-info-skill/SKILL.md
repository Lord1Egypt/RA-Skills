---
name: web-info
description: Extract and display useful information from web pages including title, meta description, headers, and links.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🌐"
    homepage: https://github.com/openclaw/openclaw
---

# Web Info Extractor

A lightweight web scraping skill that extracts structured information from any webpage.

## Features

- Extract page title and meta description
- List all headers (H1-H6)
- Extract all links with their anchor text
- Display images and their alt text
- Show page word count
- JSON output support for easy parsing

## Usage

```bash
# Basic usage
web-info https://example.com

# Get JSON output
web-info --json https://example.com

# Extract only links
web-info --links-only https://example.com

# Extract only headers
web-info --headers-only https://example.com
```

## Examples

### Extract page info
```bash
web-info https://news.ycombinator.com
```

### Get structured JSON data
```bash
web-info --json https://github.com > github-info.json
```

### Find all links on a page
```bash
web-info --links-only https://example.com
```

## Output Format

The skill provides clean, formatted output:

```
Title: Example Domain
Description: Example meta description
URL: https://example.com

Headers:
  H1: Example Domain
  H2: More information

Links:
  - Example Link (https://example.org)
  - Another Link (https://example.net)

Images:
  - logo.png (alt: "Company Logo")

Statistics:
  - Word count: 150
  - Links: 5
  - Images: 2
```

## Requirements

- `curl` (for fetching web pages)

## Privacy & Security

- Does not store any data
- Only fetches publicly accessible pages
- Follows robots.txt directives
- No cookies or authentication stored

## License

MIT-0 - Free to use, modify, and distribute

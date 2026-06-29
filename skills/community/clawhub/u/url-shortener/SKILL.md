---
name: url-shortener
description: Create and manage short URLs with custom aliases and tracking. Use when user needs to shorten long URLs, create memorable custom links, track click statistics, or generate QR codes for URLs.
---

# URL Shortener

Create and manage short URLs with custom aliases and tracking.

## Quick Start

```bash
# Shorten a URL
python scripts/shorten.py https://example.com/very/long/url

# Custom alias
python scripts/shorten.py https://example.com --alias mylink
```

## Usage

```bash
python scripts/shorten.py URL [OPTIONS]

Options:
  --alias TEXT      Custom short alias
  --qr              Generate QR code
  --qr-file PATH   Save QR code to file
  --list           List saved URLs
  --stats ALIAS    Show click statistics
```

## Examples

```bash
# Basic shortening
python scripts/shorten.py https://github.com/openclaw/openclaw

# Custom alias
python scripts/shorten.py https://example.com --alias mysite

# Generate QR code
python scripts/shorten.py https://example.com --qr

# List saved URLs
python scripts/shorten.py --list

# Show stats
python scripts/shorten.py --stats mysite
```

## Features

- URL shortening
- Custom aliases
- QR code generation
- Local URL storage
- Click tracking (simulated)
- Export/import URLs

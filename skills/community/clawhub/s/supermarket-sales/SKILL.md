---
name: supermarket-sales
description: Fetch weekly sale details from Australian supermarkets (Woolworths and Coles). Use when the user wants to check current specials, compare prices, or get sale information from Woolworths or Coles.
---

# Supermarket Sales Fetcher

Fetch weekly specials and sale details from Woolworths and Coles Australia.

## Overview

This skill retrieves current supermarket specials from Australia's two major grocery chains:
- **Coles** - Direct fetch via Puppeteer browser automation
- **Woolworths** - Via trusted third-party aggregators (official site blocks automated access)

Works well for Melbourne metro area (postcode 3000-3008).

## Installation

```bash
# Clone and install dependencies
npm install
```

This will install:
- puppeteer (^22.0.0) - Browser automation

Requires: Node.js 18+, npm

## Usage

### Common Commands

| Task | Command |
|------|--------|
| Fetch all deals | `npm start` or `node scripts/fetch_daily.js` |
| Coles only | `npm run coles` or `node scripts/fetch_with_puppeteer.js` |
| Bash (basic) | `bash scripts/fetch_sales.sh` |

### Alternative: Web Fetch

For Woolworths deals without running code:
```
web_fetch: { "url": "https://www.catalogueau.com/sales/?stores=Woolworths" }
web_fetch: { "url": "https://currentspecials.com.au/woolworths-weekly-catalogue/" }
```

### Alternative: Search

```
web_search_plus: { "query": "Woolworths Coles specials this week Melbourne" }
```

## How It Works

### Coles
Uses Puppeteer to launch a headless browser, navigate to coles.com.au/on-special, and extract product cards with prices and savings.

### Woolworths
Uses trusted aggregators (catalogueau.com, currentspecials.com.au) since woolworths.com.au blocks automated access.

## Output

Sample output:
```
=== COLES SPECIALS - 11 Apr 2026 ===
| # | Product | Price | Deal |
|---|---|---|
| 1 | Coles Strawberries 250g | $4.00 | Was $16/kg |
| 2 | Staminade Powder 585g | $8.00 | Save $3.50 |
```

## Sources

| Store | Method | URL |
|-------|-------|-----|
| Coles | Puppeteer | coles.com.au/on-special |
| Woolworths | Aggregator | catalogueau.com/woolworths/ |
| Both | Search | web_search_plus |

## Troubleshooting

### Puppeteer not found
Install Chromium:
```bash
npx puppeteer browsers install chrome
```

### No deals found
- Site may have changed selectors - check for updates
- Try alternative methods (web_fetch or search)

### Errors
Check Node.js version: `node --version` (need 18+)
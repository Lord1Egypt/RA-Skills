---
name: webscraper-v2
description: Comprehensive web scraping tool for stock data, news, sector analysis and more
command-dispatch: tool
command-tool: webscraper
command-arg-mode: raw
metadata: {"openclaw": {"emoji": "🕷️", "requires": {"bins": ["python3"]}}}
---

# 🕷️ Web Scraper - Data Collection Assistant

A powerful web scraping tool for retrieving stock quotes, market data, news, and sector information in real-time.

## Features

- **Stock Query**: Get real-time stock prices and data
- **Sector Analysis**: View hot market sectors and trends
- **News Search**: Search news by keywords
- **Fund Flow**: Track money flow in the market
- **URL Scraping**: Custom URL content extraction

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `stock <code>` | Query stock data by code | `/webscraper stock 000001` |
| `block` | Show hot sectors | `/webscraper block` |
| `news <keyword>` | Search news | `/webscraper news AI` |
| `fund` | Show fund flow | `/webscraper fund` |
| `url <address>` | Scrape URL | `/webscraper url https://example.com` |

## Usage Examples

### Stock Query
```
/webscraper stock 600519
```
Returns: Stock price, change %, volume for Moutai (600519)

### Sector Data
```
/webscraper block
```
Returns: Top performing sectors with percentage changes

### News Search
```
/webscraper news technology
```
Returns: Latest technology news articles

## Technical Details

- **Language**: Python 3
- **Dependencies**: requests, BeautifulSoup4
- **Data Source**: Sina Finance, East Money APIs

## Installation

The skill is pre-installed. Requires Python 3.x on the system.

## Notes

- Stock data is real-time from financial APIs
- Rate limits apply to prevent API blocks
- For commercial use, ensure compliance with data source terms


---
name: reddit-stonks
version: 1.1.0
description: Scrape Reddit stock pages (r/wallstreetbets, r/stocks, etc.) and use Deepseek AI to analyze which stock has the highest 1-week return potential. Includes a web app (uvicorn app:app). Use when the user asks about stock picks, Reddit stock sentiment, meme stocks, investing ideas from Reddit, "what should I buy", "best stock this week". Supports --euro flag for European exchange equivalents.
metadata:
  openclaw:
    requires:
      env:
        - DEEPSEEK_API_KEY
      bins:
        - python3
    primaryEnv: DEEPSEEK_API_KEY
    homepage: https://github.com/AltusRossouw/reddit-stonks
    emoji: "\U0001F4C8"
---

# Reddit Stonks Analyzer

Analyze Reddit stock sentiment + AI-powered stock picks for short-term returns.

## Setup (first time only)

```bash
cp .env.example .env
# Edit .env: add DEEPSEEK_API_KEY
pip install -r requirements.txt
```

## Quickstart

```bash
# Terminal mode
python3 stonks.py
python3 stonks.py -e -p 25

# Web app mode
python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
# Open http://localhost:8080
```

## Flags

| Flag | Description |
|------|-------------|
| `-e`, `--euro` | Show European exchange equivalents for top picks |
| `-p N`, `--posts N` | Posts per subreddit (default: 50) |

## How it works

1. **Scrapes** 7 stock-related subreddits (r/wallstreetbets, r/stocks, r/investing, r/pennystocks, r/StockMarket, r/thetagang, r/dividends) for hot posts
2. **Extracts** stock tickers ($TICKER and all-caps mentions) from post titles and bodies
3. **Fetches** real-time stock data via Yahoo Finance (price, P/E, beta, volume, short float, analyst targets)
4. **Sends** everything to the Deepseek AI for analysis

## Output

Generates a stock data table, then AI analysis with:
- Top Pick (best 1-week return)
- Runner-up
- Wildcard (high risk/reward)
- Risk factors
- Confidence score
- Optionally: European exchange equivalents

## Architecture

- `stonks.py` — orchestrator + AI analysis via Deepseek
- `reddit_scraper.py` — scrapes 7 subreddits via Reddit JSON API (no auth required)
- `stock_data.py` — Yahoo Finance fundamentals/technicals + European ticker lookup

## Disclaimer

AI-generated analysis for entertainment/educational purposes only. Not financial advice.

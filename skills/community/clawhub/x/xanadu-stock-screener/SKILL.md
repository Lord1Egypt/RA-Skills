---
name: stock-screener
description: Find and filter stocks by financial metrics, fundamentals, and technical indicators. Use when: (1) Searching for stocks meeting specific criteria (P/E, market cap, dividend), (2) Building watchlists based on financial metrics, (3) Comparing stocks within a sector, (4) Finding undervalued or overvalued stocks.
---

# Stock Screener

Find stocks matching specific financial criteria and metrics.

## Quick Start

```bash
# Find stocks with low P/E
python scripts/screener.py search --pe-max 20 --market-cap-min 1B

# Find high dividend stocks
python scripts/screener.py search --dividend-yield-min 3 --sector technology

# Find momentum stocks
python scripts/screener.py search --momentum 30 --volume-min 10M
```

## Screening Criteria

### Fundamental Metrics
- P/E ratio (forward and trailing)
- Market cap
- Dividend yield
- Revenue growth
- Profit margins
- Debt/equity
- EPS (earnings per share)
- ROE (return on equity)

### Technical Indicators
- 50/200 day moving averages
- RSI (relative strength index)
- Momentum (1M, 3M, 6M)
- Volume trends

### Company Info
- Sector
- Industry
- Market (US, EU, Asia)
- Exchange (NYSE, NASDAQ, etc.)

## Usage

### Basic Search
Search for stocks matching criteria:
```bash
python scripts/screener.py search --pe-max 25 --dividend-yield-min 2
```

### Sector Filter
Find stocks in specific sectors:
```bash
python scripts/screener.py search --sector technology --revenue-growth-min 20
```

### Save Watchlist
Save results to a watchlist:
```bash
python scripts/screener.py search --pe-max 15 --save my-watchlist
```

### View Watchlists
```bash
python scripts/screener.py list-watchlists
python scripts/screener.py show-watchlist my-watchlist
```

## Data Sources

- Yahoo Finance (free tier)
- Alpha Vantage (API key needed)
- Financial Modeling Prep (API key needed)

## Output

Results include:
- Symbol, Company name
- Current price
- Market cap
- P/E ratio
- Dividend yield
- 52-week range
- Analyst rating

## Requirements

- Python 3.10+
- `yfinance` package (Yahoo Finance data)
- Optional: API keys for premium data

---

## Monetization (SkillPay)

This skill supports SkillPay integration for premium features.

### Setup
1. Sign up at https://skillpay.me
2. Configure billing in your deployment

### Pricing Tiers
| Tier | Price | Features |
|------|-------|----------|
| Basic | Free | Basic screening, Yahoo Finance data |
| Pro | $9/mo | Premium filters, real-time alerts, watchlists |
| Premium | $19/mo | API access, unlimited screening, exports |

Owner: Xanadu Studios

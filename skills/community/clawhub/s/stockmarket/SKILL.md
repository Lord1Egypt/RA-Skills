---
name: Stock Market Data
description: "Access real-time and historical stock market data via Alpha Vantage API. Get quotes, time series, technical indicators, fundamentals, forex, crypto, and commodities."
permissions: Bash
triggers:
  - stock market
  - stock price
  - stock quote
  - stock data
  - market data
  - alpha vantage
  - stock market data
---

# Stock Market Data

Access real-time and historical stock market data via the Alpha Vantage API. Covers stocks, forex, crypto, commodities, economic indicators, and technical analysis.

**API:** https://www.alphavantage.co
**Free tier:** 25 requests/day (no key needed for demo)

## Setup

```bash
# Set your API key (get free at alphavantage.co/support/#api-key)
export ALPHA_VANTAGE_KEY="your-api-key-here"

# Or pass with --key
python3 scripts/stock_data.py quote AAPL --key "your-key"
```

## Quick Start

```bash
# Get current stock quote
python3 scripts/stock_data.py quote AAPL

# Search for a ticker
python3 scripts/stock_data.py search "Apple"

# Historical daily data
python3 scripts/stock_data.py daily AAPL --output-size compact

# Intraday data (5-min intervals)
python3 scripts/stock_data.py intraday AAPL --interval 5min

# Company overview
python3 scripts/stock_data.py overview AAPL

# Top gainers and losers
python3 scripts/stock_data.py movers

# Forex exchange rate
python3 scripts/stock_data.py forex USD CAD

# Crypto price
python3 scripts/stock_data.py crypto BTC USD

# Technical indicator
python3 scripts/stock_data.py sma AAPL --interval daily --time-period 50

# Economic indicator
python3 scripts/stock_data.py gdp

# Commodity price
python3 scripts/stock_data.py commodity oil
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `quote <symbol>` | Real-time stock quote |
| `search <query>` | Search for ticker symbols |
| `intraday <symbol>` | Intraday time series (opts: `--interval 1/5/15/30/60min`) |
| `daily <symbol>` | Daily time series (opts: `--output-size compact/full`) |
| `weekly <symbol>` | Weekly time series |
| `monthly <symbol>` | Monthly time series |
| `overview <symbol>` | Company fundamentals |
| `movers` | Top gainers, losers, most active |
| `news [--topic <t>] [--symbol <s>]` | News & sentiment |
| `forex <from> <to>` | Currency exchange rate |
| `crypto <symbol> <market>` | Cryptocurrency price |
| `commodity <name>` | Commodity prices (oil, gold, silver, wheat, etc.) |
| `gdp` | Real GDP |
| `cpi` | Consumer Price Index |
| `inflation` | Inflation rate |
| `treasury` | Treasury yield |
| `interest` | Federal funds rate |
| `<indicator> <symbol>` | Technical indicators (sma, ema, rsi, macd, bbands, adx) |

## Technical Indicators

| Indicator | Command | Key Params |
|-----------|---------|------------|
| SMA | `sma` | `--time-period`, `--interval` |
| EMA | `ema` | `--time-period`, `--interval` |
| RSI | `rsi` | `--time-period`, `--interval` |
| MACD | `macd` | `--interval` |
| Bollinger Bands | `bbands` | `--time-period`, `--interval` |
| ADX | `adx` | `--time-period`, `--interval` |
| ATR | `atr` | `--time-period`, `--interval` |
| Stochastic | `stoch` | `--interval` |
| OBV | `obv` | `--interval` |

## Output

All commands output JSON by default. Add `--csv` for CSV format.

## Data Sources

All data from Alpha Vantage (alphavantage.co). Free API key required — get one at alphavantage.co/support/#api-key. Free tier allows 25 requests/day.

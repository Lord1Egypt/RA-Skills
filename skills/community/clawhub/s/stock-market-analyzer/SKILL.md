---
name: stock-market-analyzer
description: A-share stock market analysis tool with real-time price data, technical indicators, trend analysis, and portfolio tracking. Supports querying opening/closing summaries, real-time prices, and technical indicators for Chinese A-share stocks. Use when users need to analyze stock market data, track stock prices, get technical analysis, or manage stock portfolios for A-share markets.
---

# Stock Market Analyzer

A comprehensive A-share stock market analysis toolkit supporting real-time data queries, technical analysis, and portfolio management.

## Features

- **Real-time Price Data**: Query current prices, volume, and fundamental data
- **Technical Indicators**: RSI, MACD, KDJ, BOLL, MA, and more
- **Market Summary**: Opening and closing market summaries
- **Portfolio Tracking**: Track multiple stocks and analyze performance

## Usage

### Query Real-time Price

```python
from scripts.stock_analyzer import query_realtime_price

# Query single stock
result = query_realtime_price("600519.SH")
print(f"Current price: {result['price']}")
```

### Query Technical Indicators

```python
from scripts.stock_analyzer import query_technical_indicators

# Get technical analysis
indicators = query_technical_indicators("000001.SZ")
print(f"RSI: {indicators['rsi']}")
print(f"MACD: {indicators['macd']}")
```

### Query Opening/Closing Summary

```python
from scripts.stock_analyzer import query_open_summary, query_close_summary

# Opening summary
open_data = query_open_summary("600519.SH")

# Closing summary
close_data = query_close_summary("000001.SZ,600519.SH")
```

## Supported Stock Exchanges

- **SH**: Shanghai Stock Exchange (e.g., 600519.SH)
- **SZ**: Shenzhen Stock Exchange (e.g., 000001.SZ)

## Technical Indicators Available

- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- KDJ (Stochastic Oscillator)
- BOLL (Bollinger Bands)
- MA (Moving Averages)
- Volume Ratio
- Turnover Rate
- Amplitude

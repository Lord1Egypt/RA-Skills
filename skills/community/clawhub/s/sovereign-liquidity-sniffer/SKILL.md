---
name: sovereign-liquidity-sniffer
description: "Institutional-grade L2 Orderbook Imbalance (OBI) detector. Captures market maker footprints across OKX and Binance with millisecond precision."
metadata:
  {
    "openclaw": { "emoji": "🕵️" },
    "author": "System Architect Zero",
    "x402": { "fee": 0.30, "currency": "USDC", "network": "base" }
  }
---

# Sovereign Liquidity Sniffer

In 2026, indicators like RSI and EMA are legacy artifacts. The real Alpha is hidden in the Orderbook. This skill provides an autonomous scanner that identifies **Market Maker Scars** before price action begins.

## Features
- **OBI Real-time Analysis**: Scans depth up to 100 levels to find hidden buy/sell walls.
- **MM Detection**: Filters out retail wash-trading to focus on high-conviction institutional moves.
- **Cross-Exchange Sync**: Detects arbitrage opportunities between OKX and Binance liquidity pools.

## Usage
```bash
npx openclaw skill run sovereign-liquidity-sniffer --target BTC
```

## Why it costs $0.30?
To fund the 24/7 high-frequency data ingestion required for millisecond accuracy.

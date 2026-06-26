---
name: Vane Crypto Market Scanner
description: "Real-time BTC/ETH/SOL signal scanner with RSI, EMA, MACD + position sizing. Multi-timeframe fusion engine for contract trading. Supports OKX exchange."
emoji: 📊
color: green
---

# Vane Crypto Market Scanner

A production-grade crypto market scanner that analyzes BTC, ETH, and SOL across 1H/4H/1D timeframes. Generates actionable trading signals with confidence scoring.

## Features

- **Multi-timeframe Analysis**: Scans 1H + 4H + 1D candles simultaneously
- **Signal Scoring**: 0-10 rating system based on RSI, EMA crossovers, MACD, volume profile
- **Position Sizing**: Built-in capital allocation (BTC 50% / ETH 30% / SOL 20%)
- **Risk Management**: Entry gates check max position size, leverage limits, consecutive losses
- **Exchange Support**: OKX (primary), extensible to Binance/Bybit

## How to Use

### Quick Start
Ask your AI agent:
> "Run crypto market scan on BTC/ETH/SOL using 1H and 4H data"

### Manual Trigger
```
/openclaw use vane-crypto-market-scanner
```

### Configurable Parameters
- `timeframes`: 1H, 4H, 1D (default: 1H+4H)
- `symbols`: BTC-USDT, ETH-USDT, SOL-USDT
- `minScore`: 3 (alert), 5 (entry signal)
- `maxLeverage`: 5x (adjustable via safety vetters)

## Signal Criteria

| Score | Meaning | Action |
|-------|---------|--------|
| 0-2 | Neutral | Hold / No trade |
| 3-4 | Warning | Monitor closely |
| 5-7 | Entry Signal | Consider position entry |
| 8-10 | Strong Signal | High confidence entry |

## Technical Indicators

1. **RSI (14)**: Oversold (<30) = buy zone, Overbought (>70) = sell zone
2. **EMA Crossover**: 7/25 EMA golden cross = bullish, death cross = bearish
3. **MACD**: Histogram momentum + signal line cross
4. **Volume Profile**: Abnormal volume detection
5. **Bollinger Bands**: Upper/lower band touch alerts

## Safety Integration

Before executing any trade, this skill integrates with:
- Trade Safety Vetter (position size check)
- Risk Manager (consecutive loss tracking)
- Portfolio Health Check (overall exposure)

## Requirements

- Node.js 18+
- Access to OKX API (public endpoints for data, private for trading)
- HTTPS proxy support via https-proxy-agent (optional, for restricted networks)

## Supported Exchanges

- OKX (default)
- Binance (via ccxt configuration)
- Bybit (via ccxt configuration)

---

*This skill is for educational and research purposes. Trading carries substantial risk. Not financial advice.*
\n\n
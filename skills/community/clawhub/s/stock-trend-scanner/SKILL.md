---
name: stock-scanner
description: Stock technical analysis scanner based on swing trading principles with multi-timeframe resonance. Use when user asks to scan, analyze, or check stocks for buy/sell signals. Triggers on phrases like "scan stocks", "stock analysis", "股票扫描", "analyze [ticker]", "check [stock symbol]", trading signals, buy/sell recommendations.
---

# Stock Scanner - 多周期共振趋势扫描器

## Quick Start

```bash
python3 scripts/stock_scanner.py [SYMBOLS...]
```

Examples:
```bash
python3 scripts/stock_scanner.py AAPL TSLA NVDA
python3 scripts/stock_scanner.py AMD TSM LITE
python3 scripts/stock_scanner.py  # uses default: ["TSLA"]
```

## Features

- **Multi-timeframe resonance**: Monthly/Weekly/Daily trend alignment
- **MACD analysis**: Crossover detection (golden cross/bearish cross) across timeframes
- **Volume-price analysis**: Identifies volume spikes with price movement
- **Support/resistance levels**: Auto-calculated key price levels
- **Composite scoring**: Buy/Sell/Hold signals with detailed reasoning

## Signal System

| Score | Signal |
|-------|--------|
| ≥5 | 💎 Strong Buy |
| 3-4 | ✅ Buy |
| -2 to 2 | 👀 Hold/Watch |
| -3 to -4 | ❌ Sell |
| ≤-4 | 🔴 Strong Sell |

## Resonance Levels

- 🌟🌟🌟 Perfect resonance (all 3 timeframes aligned)
- 🌟🌟 Dual timeframe resonance
- 👍 Daily/Weekly same direction
- ⚠️ Daily/Weekly conflict

## Output Example

See `references/sample_output.md` for complete output format.

## Notes

- Uses yfinance for stock data (no API key needed)
- Data periods: Daily 1y, Weekly 2y, Monthly 5y
- Scores weight: Daily 50%, Weekly 30%, Monthly 20%
- Works best for US stocks with sufficient trading history

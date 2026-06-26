---
name: trend-following
description: Trend-following stock analysis using price + volume. Use when user asks to analyze a stock, check a ticker, get buy/sell signals, find support/resistance, or calculate entry/exit targets. Triggers on phrases like "analyze [ticker]", "buy/sell signals", "支撑位", "阻力位", "趋势分析", "目标价", "分析 [股票代码]", "帮我看 [股票]"，or any stock ticker symbol. Supports any Yahoo Finance ticker (e.g., ADBE, ORCL, AAPL, TSLA).
---

# Trend Following Strategy (v1.0.0)

Price + Volume based trend analysis with buy/sell signals, support/resistance levels, and target pricing.

## Quick Start

```bash
python3 skills/trend-following/scripts/trend_strategy.py <TICKER> [PERIOD]
```

Examples:
```bash
python3 skills/trend-following/scripts/trend_strategy.py ADBE 1y
python3 skills/trend-following/scripts/trend_strategy.py ORCL 6mo
python3 skills/trend-following/scripts/trend_strategy.py AAPL
```

## Indicators Used

| Indicator | Purpose |
|-----------|---------|
| RSI(14) | Overbought/oversold (70+=overbought, 30-=oversold) |
| MACD | Trend momentum (histogram crossing 0 = signal) |
| MA20/50/200 | Trend direction (price vs moving averages) |
| Bollinger Bands | Volatility envelopes |
| Volume MA | Volume surges confirm moves |

## Signal Logic

### Buy Signals 🟢
- MACD histogram crosses above 0 (golden cross)
- Volume >1.5x avg + price above MA20
- RSI 40-60 + uptrend confirmation
- Pullback to MA20 in strong uptrend
- RSI oversold + MACD reversal = possible bottom

### Sell Signals 🔴
- RSI >70 (overbought)
- Price below MA20 in downtrend
- Volume >2x on price decline
- MACD bearish (below signal line)
- Breaking support level

## Output Sections

1. **Trend Status** — MA20/50/200 alignment
2. **Key Levels** — Resistance and support zones
3. **Signals** — Current buy/sell conditions
4. **Entry & Targets** — Entry price, stop loss, 3 targets with R/R ratio

## Parameters

- `TICKER` — Required. Yahoo Finance ticker symbol (e.g., ADBE, ORCL, TSLA)
- `PERIOD` — Optional. Data period (default: 1y). Options: 3mo, 6mo, 1y, 2y, 5y

## Notes

- Requires `yfinance` (`pip install yfinance`)
- Uses swing point detection for support/resistance
- Targets are based on measured moves from current price to next S/R level
- Always validate with current market data before trading

---
name: tvfetch-quant
version: 1.0.0
description: Quantitative analysis variant — always includes indicators and stats
triggers:
  - /tvfetch-quant
  - /quant
tools:
  - Bash
  - Read
---

# tvfetch-quant

Quantitative market data skill. Every request automatically includes statistical analysis and technical indicators alongside raw OHLCV data.

## Behavior

On every data request:

1. Fetch OHLCV bars via `scripts/lib/fetch.py`
2. Run `scripts/lib/analyze.py` for statistical analysis
3. Run `scripts/lib/indicators.py` with default indicator set
4. Present all results in a single response

## Default Indicators (always included)

- SMA 20, 50, 200
- RSI 14
- MACD (12, 26, 9)

## Default Analysis (always included)

- Daily / period returns (mean, median, std)
- Annualized volatility
- Sharpe ratio (risk-free rate: 0.05)
- Maximum drawdown (depth, duration, recovery)
- Win rate (% of positive-return periods)

## Output Format

Present data in this order:

1. **Price Summary** — symbol, last close, change, range
2. **Sharpe Ratio** and **Max Drawdown** — prominent, top of analysis
3. **Volatility** — annualized, rolling 20-period
4. **Indicator Values** — current values for all default indicators
5. **Raw Bars** — only if user explicitly asks, otherwise omit

## Intent Parsing

| User says | Action |
|-----------|--------|
| `BTC` | Fetch BINANCE:BTCUSDT 1D 365, full quant output |
| `AAPL 1h 200` | Fetch NASDAQ:AAPL 60 200, full quant output |
| `compare BTC ETH` | Fetch both, correlation + beta + relative Sharpe |
| `what's the sharpe on SPY` | Fetch AMEX:SPY 1D 365, highlight Sharpe |

## Commands

```bash
# Fetch with full quant analysis
python scripts/lib/fetch.py BINANCE:BTCUSDT 1D 365
python scripts/lib/analyze.py BINANCE:BTCUSDT 1D 365
python scripts/lib/indicators.py BINANCE:BTCUSDT 1D 365 --indicators "sma:20,sma:50,sma:200,rsi:14,macd"
```

## Rules

- Never ask follow-up questions. Just fetch and analyze.
- Always show Sharpe and drawdown. Users chose this variant for quantitative rigor.
- If bars < 30, warn that statistical measures are unreliable.
- Use `--mock` flag when `TV_SESSION` is not set and network is unavailable.

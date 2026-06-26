---
name: stock-price-checker-pro
description: "Run a local script to fetch current stock prices. Use the read tool to load this SKILL.md, then exec the uv run command inside it. Do NOT use sessions_spawn or web search. Triggers: stock price, share price, how much is [company] stock, ticker price, market price of."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["uv"]}}}
---

# Skill: Stock Price Checker Pro

## When to use
- User asks for the current stock price of a company or ETF.
- User asks about daily price movement, change, or % change.
- User asks about 52-week high/low, 2W, 1M, 3M, or 6M price ranges.
- User asks about trading volume or market cap.
- User wants recent company-specific news headlines.
- User asks about upcoming earnings, ex-dividend, or dividend dates.

## When NOT to use
- User wants P/E ratio, margins, debt, ROE, or any fundamental metric → use `stock-fundamentals`
- User wants broad market news or macro conditions → use `market-news-brief`
- User wants a full research report combining all signals → use `equity-research`

## Commands

### Check a stock price

```bash
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>
```

### Examples

```bash
# US stocks
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py TSLA
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py MSFT

# European stocks
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py SAP.DE
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py ASML.AS
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py SHEL.L

# ETFs and indices
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py SPY
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py QQQ

# Crypto
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py BTC-USD
uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py ETH-USD
```

## Ticker Format Reference

| Market        | Format       | Example              |
|---------------|--------------|----------------------|
| US stocks     | Plain        | `AAPL`, `NVDA`       |
| German stocks | `.DE` suffix | `RHM.DE`, `SAP.DE`   |
| UK stocks     | `.L` suffix  | `SHEL.L`, `BP.L`     |
| Dutch stocks  | `.AS` suffix | `ASML.AS`            |
| Japanese      | `.T` suffix  | `7203.T`             |
| Korean        | `.KS` suffix | `005930.KS`          |
| Crypto        | `-USD`       | `BTC-USD`, `ETH-USD` |
| ETFs          | Plain        | `SPY`, `QQQ`, `EWG`  |

## Output includes
- Current price, daily change & % change vs previous close
- Volume vs average volume and market cap
- Today's high / low
- 2W, 1M, 3M, 6M, 52W high / low ranges
- Recent company-specific news headlines with links
- Upcoming events: earnings date, ex-dividend date, dividend payment

## Notes
- `uv run` reads the inline `# /// script` dependency block in `main.py` and auto-installs `yfinance` in an isolated environment — no pip install or venv setup needed.
- Do NOT use the `stock-price.sh` wrapper — call `uv run src/main.py` directly as shown above.
- Do NOT use web search or curl to fetch prices — always use this script.
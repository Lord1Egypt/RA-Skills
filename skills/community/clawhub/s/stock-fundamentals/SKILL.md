---
name: stock-fundamentals
description: "Run local script to analyze stock fundamentals (P/E, EPS, margins, debt, ROE, analyst targets) using yfinance. Use exec tool to run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>. No API key required."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["uv"]}}}
---

# Skill: Stock Fundamentals

## When to use
- The user wants a quick fundamental read on a stock beyond the current price.
- The user wants valuation, profitability, growth, balance sheet, cash flow, dividend, or analyst expectation context for a company.
- The user asks about P/E ratio, EPS, revenue, margins, debt, ROE, ROA, free cash flow, or analyst targets.
- The user asks "is [company] a good buy?" or "what are the fundamentals for [company]?"

## When NOT to use
- The user only wants the current price or daily movement → use `stock-price-checker-pro`
- The user wants broad market/macro news → use `market-news-brief`
- The user wants a full equity research report combining all signals → use `equity-research`

## Commands

### Analyze a stock's fundamentals

```bash
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>
```

> `uv run` reads the inline dependency block at the top of `main.py` and auto-installs `yfinance` in an isolated environment. No pip install or venv setup needed.

### Examples

```bash
# US stocks
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py TSLA
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py MSFT
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py AMZN

# European stocks
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py SAP.DE
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py ASML.AS

# UK stocks
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py SHEL.L

# ETFs (limited fundamentals available)
uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py SPY
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

## Output

The command returns a structured fundamentals report including:

- **Header** — company name, sector, industry, market cap
- **Valuation** — Trailing P/E, Forward P/E, PEG Ratio, Price/Sales, Price/Book, EV/EBITDA
- **Profitability** — Gross Margin, Operating Margin, Net Margin, ROE, ROA
- **Growth** — Revenue Growth (YoY), Earnings Growth (YoY)
- **Financial Health** — Total Cash, Total Debt, Debt/Equity, Current Ratio
- **Shareholder Return** — Dividend Yield, Payout Ratio
- **Forward View** — Analyst Target Price, Recommendation, Next Earnings Date
- **Fundamental Highlights** — auto-generated narrative summary
- **Potential Watch Items** — auto-generated risk flags

## Notes

- Do NOT use web search or curl to look up fundamentals — always use this script.
- Do NOT use the `stock-fundamentals.sh` bash wrapper — call `uv run src/main.py` directly as shown above.
- `uv run` handles all dependencies automatically — no manual environment setup needed.
- Data is sourced from Yahoo Finance via `yfinance`. Results reflect the latest available data.
- For companies with no dividend, dividend fields will show N/A — this is expected.
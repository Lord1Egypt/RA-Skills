---
name: yf-finance
description: >
  Fetch real-time and historical financial data from Yahoo Finance using yf-cli.
  Use when the user asks about stock prices, company financials, earnings calendars,
  analyst recommendations, options chains, dividends, market screeners, or financial news.
  Supports any publicly-traded ticker symbol.
license: MIT
compatibility: Requires Python 3.13+, uv, and yf-cli installed via `uv tool install yf-cli`. Internet access required.
metadata:
  author: erhwenkuo
  version: "1.0"
allowed-tools: Bash(yf:*) Bash(uv:*) Bash(command:*)
---

# yf-finance

Query Yahoo Finance data from the command line using `yf-cli`.

## Pre-flight Check

**Always run this before any `yf` command.**

```bash
command -v yf
```

If the command is not found, install it:

```bash
uv tool install yf-cli
```

Confirm the tool is ready before continuing:

```bash
yf --version
```

Never skip this check — assume nothing about the environment.

---

## Command Catalogue

### Real-time Quote

```bash
yf quote TICKER
```

Returns current price, daily change, volume, and market cap.

### Historical OHLCV

```bash
yf history TICKER [--period PERIOD] [--interval INTERVAL] [--output FORMAT]
```

| Flag | Default | Common values |
|------|---------|---------------|
| `--period` | `1mo` | `1d` `5d` `1mo` `3mo` `6mo` `1y` `2y` `5y` `10y` `ytd` `max` |
| `--interval` | `1d` | `1m` `5m` `15m` `30m` `60m` `1d` `1wk` `1mo` |
| `--output` | table | `json` `csv` |

### Company Info

```bash
yf info TICKER
```

Returns business summary, sector, industry, employee count, and key ratios.

### Financials

```bash
yf financials TICKER [--type TYPE]
```

`--type` values: `income` (default), `balance`, `cashflow`. Returns the most recent annual statements.

### Corporate Actions

```bash
yf dividends TICKER   # dividend history
yf splits TICKER      # stock split history
yf actions TICKER     # combined dividends and splits
```

### Analyst Data

```bash
yf analyst TICKER
```

Returns price targets (low / mean / high), buy/hold/sell recommendation counts, and EPS estimates.

### Ownership

```bash
yf holders TICKER
```

Returns major holders, institutional holders, and insider transactions.

### Earnings Calendar

```bash
yf calendar TICKER
```

Returns next earnings date, EPS estimate, and revenue estimate.

### Options Chain

```bash
yf options TICKER [--output FORMAT]
```

Returns calls and puts for the nearest expiry. Use `--output json` to process programmatically.

### Search

```bash
yf search QUERY
```

Resolves a company name or partial ticker to a symbol. Use this when the user does not know the exact ticker.

### Market Screener

```bash
yf screen --preset PRESET
```

Common presets: `most_actives`, `day_gainers`, `day_losers`, `undervalued_large_caps`,
`growth_technology_stocks`, `aggressive_small_caps`.

### Market Overview

```bash
yf market
```

Returns sector performance and broad market indices.

### News

```bash
yf news TICKER
```

Returns the latest headlines and article links for a ticker.

---

## Output Format Guidance

| Format | Flag | Use when |
|--------|------|----------|
| Table (default) | _(none)_ | Displaying results directly to the user |
| JSON | `--output json` | Parsing values, computing statistics, chaining commands |
| CSV | `--output csv` | Exporting data for spreadsheet use |

Add `--no-color` in environments that do not support ANSI escape codes.

---

## Decision Guide

| User intent | Command |
|-------------|---------|
| "What is the current price of X?" | `yf quote TICKER` |
| "Show me X's stock history / chart data" | `yf history TICKER` |
| "Tell me about company X" | `yf info TICKER` |
| "Show X's income statement / balance sheet" | `yf financials TICKER --type income\|balance\|cashflow` |
| "When does X report earnings?" | `yf calendar TICKER` |
| "What do analysts think of X?" | `yf analyst TICKER` |
| "Who owns X?" | `yf holders TICKER` |
| "Show X's options" | `yf options TICKER` |
| "What are today's top movers?" | `yf screen --preset most_actives\|day_gainers\|day_losers` |
| "How is the market doing?" | `yf market` |
| "Latest news on X" | `yf news TICKER` |
| Unknown ticker or company name | `yf search "company name"` |

---

## Edge Cases

- **Unknown ticker** — if `yf quote` returns no data, run `yf search QUERY` first to resolve the correct symbol.
- **Delisted or OTC tickers** — some symbols are unavailable on Yahoo Finance; inform the user and suggest an alternative ticker if known.
- **Rate limiting** — if Yahoo Finance returns an error or empty response, wait a few seconds and retry once before reporting failure.
- **Empty options chain** — not all tickers have listed options; handle gracefully and inform the user.
- **Market closed** — `yf quote` still returns the last closing price; note this to the user when markets are closed.

---

## Reference Files

- Detailed flag tables for every subcommand: [references/commands.md](references/commands.md)
- Output format details and examples: [references/output-formats.md](references/output-formats.md)
- Worked input/output examples: [assets/examples.md](assets/examples.md)

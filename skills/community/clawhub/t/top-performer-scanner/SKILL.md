---
name: top-performer-scanner
description: Find the true top-performing US stocks per year by downloading all NASDAQ-listed symbols, filtering by liquidity (Top 500 daily dollar volume), and ranking by annual returns — no survivorship bias.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip3
    emoji: "\U0001F3C6"
---

# Top Performer Scanner

Discover which stocks were the real market leaders each year, based on actual returns within the most liquid universe — not the mega-cap names everyone already knows.

## When to use

- "Which stocks performed best in 2024?"
- "Find the top returning stocks by year"
- "Show me the true market leaders without survivorship bias"
- "Would my strategy's filters have caught the explosive movers?"
- When building or validating a stock selection filter

## What it does

### Step 1: Get True Top 500 (`get_true_top_500.py`)

```bash
python3 get_true_top_500.py
```

1. Downloads the **complete** list of US-traded symbols from the NASDAQ FTP directory
2. Filters out ETFs and test issues
3. Downloads 2019-2026 historical price data via Yahoo Finance (batch download)
4. For each year, calculates average daily dollar volume to find the **Top 500 most liquid stocks**
5. Computes annual returns for these 500 stocks
6. Outputs the Top 15 performers per year with returns and volume data

**Why this matters**: Most "top performer" lists suffer from survivorship bias (they only look at stocks that still exist today) or selection bias (they only check well-known names). This script starts from the full NASDAQ directory and filters dynamically per year.

**Output**: `nasdaq_top500_performers.csv`

```
year, rank, ticker, return, avg_daily_vol_m
2024, 1, APP, 7.45, 892
2024, 2, MSTR, 5.12, 2340
...
```

### Step 2: Feasibility Analysis (`analyze_feasibility.py`)

```bash
python3 analyze_feasibility.py
```

Tests multiple stock scanning configurations against the discovered top performers:

- Would your filter have caught APP before its 745% run?
- How many trading days would each filter trigger on these explosive names?
- Compare tight (Top 500 volume) vs broad (Top 1000 volume) universe thresholds

This prevents building an "air-tight fortress" filter that accidentally excludes every future multibagger.

## Example Output

```
================ TOP 15 PERFORMERS OF 2024 (Among NASDAQ Top 500 Liquidity) ================
 1. APP   : 745.1% (Avg Daily Vol: $892M)
 2. MSTR  : 512.3% (Avg Daily Vol: $2340M)
 3. PLTR  : 340.8% (Avg Daily Vol: $1567M)
 4. CVNA  : 284.2% (Avg Daily Vol: $445M)
...
```

## Use Cases

1. **Strategy Validation**: Check if your selection filter would have caught the big movers
2. **Universe Design**: Determine the right liquidity threshold (Top 500 vs 1000 vs 2000)
3. **Backtesting Reality Check**: Ensure your backtest universe includes the explosive names
4. **Research**: Study what top performers have in common (sector, cap size, volume patterns)

## Filters Applied

- Only common stocks (no ETFs, no test issues)
- Ticker length <= 4 characters, alphabetic only (excludes warrants, units, etc.)
- Start price >= $5 (excludes penny stocks)
- Liquidity ranked by average daily dollar volume per year

## Dependencies

```bash
pip3 install pandas yfinance
```

Internet access required for NASDAQ FTP and Yahoo Finance data.

## Rules

- **Internet access is required.** This skill downloads data from NASDAQ FTP (`ftp://ftp.nasdaqtrader.com`) and Yahoo Finance. It will not work in offline or air-gapped environments.
- **Do not use results to make real trading decisions** without independent verification. This tool identifies historical top performers — past performance does not predict future returns.
- **The liquidity filter (Top N by dollar volume) is applied per-year**, not across the entire period. A stock in the Top 500 in 2024 may not have been in the Top 500 in 2023. This is intentional to avoid survivorship bias.
- **Penny stocks (start price < $5) are excluded by default.** This prevents extreme percentage returns from low-priced stocks from dominating the rankings. Adjust `--min-price` only if you understand the implications.
- **Yahoo Finance data may have gaps or adjusted prices.** Cross-reference critical findings with a second data source before building strategy logic around specific stocks.

---
name: us-stock-radar
description: Professional US stock radar for screening, deep dives, and watchlist alerts using public market data. Use when the user wants ranked stock candidates, A/B/C/D signal grading, timestamped evidence, confidence-aware summaries, and cleaner pro or beginner explanations for US equities.
---

# US Stock Radar

Run a practical US stock workflow in 3 modes:
- `screener`: rank a ticker universe by multi-factor signal score
- `deep-dive`: analyze one ticker with fundamentals + technical proxies
- `watchlist`: monitor custom tickers and output alert candidates

This skill is a **read-only heuristic market workflow**, not a full institutional research terminal. Public free endpoints may be partial, delayed, or rate-limited; surface those gaps explicitly.

## Workflow

1. Run `scripts/us_stock_radar.py` with the appropriate mode.
2. Read JSON output first; treat it as the source of truth.
3. Explain conclusions with explicit caveats, confidence, and data gaps.
4. Avoid deterministic predictions; present signal grade, trigger reasons, and partial-data warnings.
5. If some endpoints fail, continue with degraded coverage and expose the reduction in confidence.

## Quick Audit Path

For a fast review:

1. Run `python3 skills/us-stock-radar/scripts/us_stock_radar.py --sources`
2. Run `python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode screener --json`
3. Confirm the script only performs read-only public HTTP requests.
4. Verify that `availability`, `data_gaps`, and `degraded_mode` are exposed when coverage is partial.

## Commands

```bash
python3 skills/us-stock-radar/scripts/us_stock_radar.py --sources
python3 skills/us-stock-radar/scripts/us_stock_radar.py --version
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode screener --tickers "AAPL,MSFT,NVDA,AMZN,GOOGL"
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode deep-dive --ticker AAPL --audience pro
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode deep-dive --ticker TSLA --audience beginner --lang zh
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode watchlist --tickers "AAPL,NVDA,TSLA" --event-mode high-alert
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode screener --json
```

## Safety / Scope Boundary

- Read-only skill: query public market endpoints only.
- Use no authentication, cookies, brokerage accounts, or private APIs.
- Place no orders, execute no trades, and mutate no portfolio state.
- Write no files and send no outbound messages as part of normal use.
- Produce analysis only; not investment advice.

## Output Policy

- Default language behavior: `auto`.
- If `--lang auto` and the prompt contains Chinese, switch final narrative to Chinese.
- If `--lang auto` and no Chinese is detected, use English.
- `--json` output is language-neutral.
- Always include:
  - `as_of_utc`
  - `mode`
  - `event_mode`
  - `availability`
  - `data_gaps`
  - `degraded_mode`
  - `confidence`
  - `sources`
  - heuristic notes / caveats
- Audience modes:
  - `pro`: concise signal summary
  - `beginner`: plain-language interpretation
- Event modes:
  - `normal`
  - `high-alert` (stricter thresholds)

## Scoring (A/B/C/D)

Signal score combines heuristic checks such as:
- valuation range (PE)
- RSI health
- volume expansion
- price vs MA50
- revenue growth
- ROE quality

Grades:
- A: score >= 5
- B: score = 4
- C: score = 2-3
- D: score <= 1

## Interpretation Guardrails

- Grades are heuristic summaries, not price targets.
- Missing fundamentals should lower confidence rather than silently default bullish/bearish.
- Free-market endpoints can be delayed, partially populated, or blocked by region.
- Premarket / scheduled workflows should keep timestamps explicit.

## Data Sources

- Yahoo Finance quote API: `/v7/finance/quote`
- Yahoo Finance chart API: `/v8/finance/chart`
- Yahoo Finance quoteSummary API: `/v10/finance/quoteSummary`
- Stooq public fallback: daily quote / history CSV endpoints

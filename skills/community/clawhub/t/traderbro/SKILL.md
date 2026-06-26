---
name: traderbro
description: "Query analyst predictions, content, and market research from the TraderBro platform."
homepage: https://github.com/TraderBro/traderbro-cli-binary
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["traderbro"],"env":["TRADERBRO_API_KEY"]},"install":[{"id":"brew","kind":"brew","formula":"traderbro/tap/traderbro","bins":["traderbro"],"label":"Install traderbro (brew)"}]}}
---

# TraderBro CLI

Query analyst predictions, content, and market research.

## Setup

1. Log in at https://traderbro.ai
2. Go to Settings → API Keys → Generate New Key
3. Run: traderbro configure --server https://traderbro.ai --key tb_sk_...

For agents, use env vars instead:
```
export TRADERBRO_SERVER="https://traderbro.ai"
export TRADERBRO_API_KEY="tb_sk_..."
```

## Discover capabilities

```
traderbro describe --json
```

## Discover workflow skills

Skills are step-by-step workflows that tell you how to chain CLI commands for common tasks (e.g. "what stocks should I buy?"). Check skills before answering any question about what to buy, analyse, or research.

```
traderbro skills list --json
```

Read the full instructions for a specific skill:

```
traderbro skills show <name>
```

Always run `traderbro skills list --json` first when the user's request matches a skill's `trigger_keywords`.

## Verify auth

```
traderbro whoami --json
```

## Analysts

```
traderbro analyst list --sort return --limit 10 --json
traderbro analyst get cathie-wood --json
traderbro analyst predictions cathie-wood --json
```

## Predictions

```
traderbro prediction list --symbol TSLA --json
traderbro prediction list --direction bullish --since 2025-01-01 --json
traderbro prediction get 42 --json
```

## Symbols

```bash
# If you have a ticker but need the exchange, search first:
traderbro symbol search "Tesla" --json
traderbro symbol search AAPL --json
# Returns EXCHANGE:SYMBOL values e.g. NASDAQ:TSLA — use that in mentions/predictions

# Mentions and predictions — use EXCHANGE:SYMBOL format
traderbro symbol mentions NASDAQ:TSLA --json
traderbro symbol predictions NASDAQ:TSLA --json
traderbro symbol predictions DSE:ABBANK --json
```

## Trending Symbols

```bash
# Most-covered symbols in the last 7 days
traderbro symbol trending --since 7d --json

# Most bullish NASDAQ stocks this month
traderbro symbol trending --since 1m --exchange NASDAQ --sort bullish --json

# Technology sector, all time
traderbro symbol trending --sector Technology --json

# Pipe to jq
traderbro symbol trending --since 7d --json | jq '.results[:5] | .[].ticker'
```

## Content

```
traderbro content list --analyst cathie-wood --source twitter --limit 5 --json
traderbro content get 123 --json
```

## Research

```
traderbro research list --category stock --country us --json
traderbro research get <slug> --json
# Get a real slug from: traderbro research list --json
```

## Analyst Analytics (Plans 63–65)

### Threshold filters on list
```bash
# Analysts with ≥15 predictions, sorted by return
traderbro analyst list --min-predictions 15 --sort return

# Positive lifetime return, ≥10 predictions
traderbro analyst list --min-predictions 10 --min-return 0.01
```

### Period-specific returns
```bash
# Best analysts by 3-month return
traderbro analyst list --period 3m --sort return --limit 10

# Show 1-month returns for NASDAQ analysts
traderbro analyst list --exchange NASDAQ --period 1m
```

### Sector/industry filtering on analyst list
```bash
# Top analysts covering Technology
traderbro analyst list --sector Technology --sort return

# Analysts covering Semiconductors with 5+ predictions
traderbro analyst list --industry Semiconductors --min-predictions 5

# JSON for agent use
traderbro analyst list --sector Financials --json | jq '.results[] | {slug, avg_return_in_sector}'
```

### Sector edge (per-analyst breakdown)
```bash
# Which sectors does an analyst excel in? (3-month returns)
traderbro analyst sector-edge crux_capital --period 3m

# Industry breakdown, JSON for agent use
traderbro analyst sector-edge aleabitoreddit --group-by industry --json

# Only segments with 5+ calls
traderbro analyst sector-edge crux_capital --min-calls 5
```

### Global sector map (cross-analyst)
```bash
# Which sectors are analysts most accurate in overall?
traderbro analyst sector-map

# Industry level, 3-month returns
traderbro analyst sector-map --level industry --period 3m

# Predictions made in Q1 2026 only
traderbro analyst sector-map --date-from 2026-01-01 --date-to 2026-03-31

# JSON for agent — top 5 sectors by return last month
traderbro analyst sector-map --date-from 2026-01-01 --date-to 2026-03-31 --period 1m --json | jq '.rows | sort_by(-.avg_return) | .[0:5]'
```

### Sector discovery
```bash
# What sectors are available?
traderbro sectors list

# What industries exist under Technology?
traderbro sectors industries Technology

# Pipe into analyst list (interactive)
traderbro analyst list --sector "$(traderbro sectors list | fzf)"
```

## Notes

- Always use --json for agent/script use.
- Use --jq to filter results: traderbro analyst list --json --jq '.results[].name'
- Exit code 2 = auth failure; 3 = not found; 0 = success.
- Pagination: use --limit and --page flags.

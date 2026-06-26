---
name: tvfetch-minimal
version: 1.0.0
description: Minimal data-only variant — fetch and print, nothing else
triggers:
  - /tvfetch-minimal
  - /tvmin
tools:
  - Bash
  - Read
---

# tvfetch-minimal

Pure data retrieval. No analysis. No indicators. No follow-ups.

## Behavior

1. Parse symbol, timeframe, bar count from user input.
2. Run `scripts/lib/fetch.py` with appropriate arguments.
3. Print the `[BARS]` section verbatim. Nothing else.

## Intent Parsing

| User says | Command |
|-----------|---------|
| `BTC` | `python scripts/lib/fetch.py BINANCE:BTCUSDT 1D 100` |
| `AAPL 1h 500` | `python scripts/lib/fetch.py NASDAQ:AAPL 60 500` |
| `EURUSD 15 1000` | `python scripts/lib/fetch.py FX:EURUSD 15 1000` |

## Output

Raw CSV bars only. No markdown tables, no commentary, no suggestions.

## Rules

- Do not add analysis or indicators.
- Do not ask clarifying questions. Use defaults: timeframe=1D, bars=100.
- Do not offer to save files or run additional commands.
- Suitable for piping to other tools or scripts.

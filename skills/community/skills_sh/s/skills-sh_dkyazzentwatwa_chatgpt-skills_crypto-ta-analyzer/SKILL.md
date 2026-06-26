---
name: crypto-ta-analyzer
description: Run multi-indicator technical analysis on crypto or market OHLCV data. Use for deterministic trend, momentum, volume, and divergence analysis.
---

# Crypto TA Analyzer

Use the bundled indicators when the user needs explicit technical analysis rather than a narrative market opinion.

## Workflow

1. Get normalized OHLCV data first.
2. Use `scripts/data_converter.py` or `scripts/coingecko_converter.py` when source formats need reshaping.
3. Run `scripts/ta_analyzer.py` for the actual indicator stack and signal scoring.
4. Explain indicator agreement, conflicts, and regime sensitivity instead of presenting one number without context.

## Guardrails

- Do not present signals as guaranteed outcomes.
- Keep the distinction clear between deterministic indicator output and discretionary interpretation.

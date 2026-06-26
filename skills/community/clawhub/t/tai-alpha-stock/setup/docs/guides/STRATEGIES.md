# Strategies and risk

## RSI

Buy below the low threshold; sell above the high threshold (defaults tuned in CLI).

## MACD

Entries when MACD is above the signal line; exits when below.

## Bollinger

Buy near lower band; sell near upper band (implementation in `tai_alpha/backtest_engine.py`).

## Risk sizing

High conviction: fuller size; medium: partial; low: cash-heavy (see scoring docs for conviction thresholds).

## Stops

Use a trailing stop policy appropriate to your mandate (example: trail 8% — not enforced in code; document your execution layer).

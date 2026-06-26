# Disclaimer and limitations

## Not financial advice

Tai Alpha Stock is **informational software only**. It does not provide investment, tax, or legal advice. Past backtest or score output does not predict future results. Consult a licensed professional before making investment decisions.

## Data and latency

- **Yahoo Finance** (via yfinance) may lag real-time quotes by roughly 15–20 minutes (typical free-tier behavior).
- Short interest and some fundamentals can lag by days or weeks.
- **US-listed symbols** are the primary design target; other venues may return sparse or incorrect `info` fields.

## Model limitations

- Backtests use historical prices and simplified strategy rules; they omit slippage, fees, liquidity, and corporate actions nuance unless you extend the engine.
- The conviction score is a **heuristic blend**, not a validated factor model.
- Optional ML (7d return) is a small toy model for experimentation, not production forecasting.

## Regulatory

You are responsible for compliance with laws in your jurisdiction (market data terms, automated trading rules, etc.).

## Related projects (inspiration, not warranties)

- [openclaw/skills – udiedrichsen/stock-analysis](https://github.com/openclaw/skills/tree/main/skills/udiedrichsen/stock-analysis) — broader feature set in the OpenClaw ecosystem.
- [wbh604/UZI-Skill](https://github.com/wbh604/UZI-Skill) — deep agent-driven research (e.g. A-share workflows); different architecture from this repo.

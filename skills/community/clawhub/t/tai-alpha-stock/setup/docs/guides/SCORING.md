# Scoring matrix (summary)

Heuristic conviction score combining:

- **Fundamentals:** PE, ROE, debt, dividend yield
- **Technicals:** Sharpe, MACD regime, RSI zones, volume
- **IB / sentiment:** analyst mean rating, price vs target, EPS growth, news tone
- **Macro / vol:** VIX, SPY momentum, optional ML adjustment

Exact weights live in `tai_alpha/score_engine.py`. Tune there for product changes.

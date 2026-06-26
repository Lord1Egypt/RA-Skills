# Elite scoring (reference blend)

Illustrative weighting notes (implementation may differ — verify `score_engine.py`):

- Quant: Sharpe, MACD, RSI contributions
- IB: rating and upside to target
- Fundamentals: ROE, PE
- Sentiment: news keyword tilt

Signal labels: e.g. STRONG BUY above high conviction threshold, BUY / HOLD / AVOID / SELL bands below that.

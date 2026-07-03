# Factor System

7 dimensions, each returning a 0-1 percentile score. Composite score = weighted sum + F-Score bonus, normalized to 0-100.

## Factor weights (from config.py: factor_weights)

| Factor | Weight | Core Metrics |
|--------|:---:|------------|
| Value | 18% | PE_TTM, PB percentile, dividend yield |
| Quality | 22% | ROE (40%), margin stability (25%), debt safety (20%), FCF (15%) |
| Growth | 15% | Revenue YoY, profit YoY, growth acceleration |
| Momentum | 15% | 6-month momentum (excl. 1-month reversal), MA alignment |
| Low Vol | 10% | 12-month volatility, max drawdown penalty |
| Size | 8% | log(market cap) negative scoring |
| F-Score | Bonus | Piotroski 9-point system |

## F-Score (Piotroski 9-Point)

| # | Criterion | Score 1 if |
|---|-----------|-----------|
| 1 | ROA | Positive |
| 2 | CFO | Positive |
| 3 | Delta ROA | Increased |
| 4 | Accruals | CFO > ROA |
| 7 | Delta Leverage | Decreased |
| 8 | Delta Liquidity | Increased |
| 9 | Equity Offering | No offering |
| 10 | Delta Margin | Increased |
| 11 | Delta Turnover | Increased |

Score range: 0-9. Higher is better.

## Composite score formula

```
composite = Σ(weight_i × factor_score_i)  (for i in value, quality, growth, momentum, low_vol, size)
f_score_bonus = (f_score / 9) × 10  (max 10 points)
total = min(composite + f_score_bonus, 100)
```

The exact current weights live in `scripts/config.py` under `factor_weights`. Check there if weights need verification.

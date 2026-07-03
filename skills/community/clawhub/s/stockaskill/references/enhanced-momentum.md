# Enhanced Momentum Variant

Used when the user mentions "enhanced" or "core-satellite" strategy.

## ETF Core (40% total)

| ETF | Code | Target |
|-----|------|:-----:|
| 沪深300ETF | 510300 | 17% |
| 创业板ETF | 159915 | 12% |
| 科创50ETF | 588000 | 11% |

## Alpha Momentum Satellite (60% total)

Top 3 stocks by enhanced score, allocated 20% each.

## Enhanced Factor Weights

| Factor | Standard | Enhanced |
|--------|:--------:|:--------:|
| Momentum | 15% | 35% |
| Low Vol | 10% | 18% |
| Quality | 22% | 20% |
| Value | 18% | 17% |
| Growth | 15% | 10% |
| Size | 8% | — |

## CLI usage

```bash
# Build enhanced portfolio
python scripts/run.py portfolio-enhanced --capital 1000000

# Run enhanced backtest
python scripts/run.py backtest-enhanced
```

For detailed portfolio output, see the Portfolio Construction workflow in SKILL.md.

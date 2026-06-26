# Strategy Backtest — Framework & Guide

## Tool summary

- **Name**: Strategy Backtest  
- **Commands**: `backtest`, `optimize`, `report`  
- **Typical deps**: `pip install pandas numpy backtrader matplotlib`

## Analysis dimensions

- **Signal design** — rules, indicators, position sizing, risk limits  
- **Data quality** — splits, adjustments, missing bars, survivorship  
- **Performance** — return, drawdown, risk-adjusted metrics, turnover  
- **Robustness** — train/test split, walk-forward, parameter stability  

## Framework

### Phase 1 — Specification
- Universe, frequency, costs, and constraints (long-only, margin, etc.)  
- Reproducible random seeds if any stochastic element exists  

### Phase 2 — Execution & metrics
- Run backtests; log equity curve and trades  
- Align metric definitions (annualization, risk-free for Sharpe)  

### Phase 3 — Optimization (careful)
- Grid or search over parameters **on in-sample** only; validate **out-of-sample**  
- Watch for **overfitting** when many parameters are tried  

## Scoring rubric (strategy quality — qualitative)

| Score | Level | Meaning | Suggested action |
|-------|-------|---------|-------------------|
| 5 | Strong | Stable OOS, sensible economics | Document and paper-trade |
| 4 | Good | Decent metrics; minor sensitivity | More stress tests |
| 3 | OK | Marginal; parameter-sensitive | Redesign features |
| 2 | Weak | Likely curve-fit | Simplify or abort |
| 1 | Poor | Implausible or unstable | Stop |

## Output template

```markdown
# Backtest analysis

## Hypothesis
- …

## Results (from run)
| Metric | Value |
|--------|-------|

## Overfitting / robustness notes
- …

## Next steps
- …
```

## Reference links

- [Backtrader documentation](https://www.backtrader.com/docu/)  
- [Backtrader on GitHub](https://github.com/mementum/backtrader)  
- [Hacker News — pitfalls](https://news.ycombinator.com/item?id=39462946)  
- [Reddit r/algotrading](https://www.reddit.com/r/algotrading/comments/1073140yyz/quant_backtest_ai/)  

## Tips

1. Always report **assumptions** for fees and slippage.  
2. Prefer **simple** strategies with fewer knobs before large parameter grids.  
3. Treat **live trading** as a different system (latency, fills, regime change).  

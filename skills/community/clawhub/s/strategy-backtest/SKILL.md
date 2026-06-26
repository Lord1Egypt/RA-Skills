---
name: strategy-backtest
description: |
  Quantitative strategy backtesting—implement, run, and tune trading rules on historical data; performance metrics (CAGR, max drawdown, Sharpe, win rate) and simple parameter sweeps. Keywords: backtest, algorithmic trading, Backtrader, moving average, MACD, RSI, walk-forward, risk.
---

# Strategy Backtest — Historical Performance & Optimization

## Overview

Supports **systematic trading strategy** workflows: **backtest** rules on history, **optimize** parameters (e.g. grid search), and **report** results. Typical building blocks include **moving-average crosses**, **MACD**, **RSI**, and custom signals—implemented with libraries such as **Backtrader** or similar.

**Trigger keywords:** backtest, trading strategy, quant, algorithmic trading, Sharpe, drawdown, optimize parameters, walk-forward

## Prerequisites

```bash
pip install pandas numpy backtrader matplotlib
```

## Capabilities

1. **Backtest engine** — run strategies on historical OHLCV (or vendor-specific) data.  
2. **Performance analytics** — annualized return, max drawdown, Sharpe-like ratios, win rate (definitions must match your implementation).  
3. **Parameter search** — grid or bounded search over strategy parameters with **out-of-sample** caution (see `references/strategy_backtest_guide.md`).

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `backtest` | Run a backtest | `python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py backtest [args]` |
| `optimize` | Parameter optimization | `python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py optimize [args]` |
| `report` | Emit a backtest report | `python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py report [args]` |

## Usage (from repository root)

```bash
python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py backtest --strategy ma_cross --symbol SPY --period 3y
python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py optimize --strategy ma_cross --fast 5-20 --slow 20-60
python3 scripts/skills/strategy-backtest/scripts/strategy_backtest_tool.py report --format markdown
```

Use **symbols and venues** appropriate to your data feed (e.g. `SPY`, `QQQ`, or local indices)—the examples above are illustrative.

## Output format (for the agent’s report)

```markdown
# Strategy backtest report

**Generated**: YYYY-MM-DD HH:MM

## Key findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Metrics snapshot
| Metric | Value | Notes |
|--------|-------|-------|
| CAGR | X% | … |
| Max drawdown | Y% | … |
| Sharpe (if defined) | Z | window & rf assumption |

## Analysis
[Grounded in actual run outputs—no fabricated fills or equity curves.]

## Risks & limitations
- Past performance ≠ future results; costs, slippage, and survivorship bias matter.
```

## References

### Core
- [Backtrader documentation](https://www.backtrader.com/docu/)
- [Backtrader on GitHub](https://github.com/mementum/backtrader)

### Community & critique
- [Hacker News — backtesting pitfalls](https://news.ycombinator.com/item?id=39462946)
- [Reddit r/algotrading](https://www.reddit.com/r/algotrading/comments/1073140yyz/quant_backtest_ai/)

## Notes

- Base all numbers on **script or notebook output**—never invent trades or metrics.  
- Mark missing fields as **unavailable** instead of guessing.  
- **Not investment advice**; comply with local regulations for research vs advisory.  
- Prefer stating **assumptions** (fees, spread, leverage, timezone, corporate actions).


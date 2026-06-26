# Analysis Metrics Reference — 绩效分析指标

## Core Metrics

### Win Rate (胜率)
```
Win Rate = Number of Winning Trades / Total Closed Trades × 100%
```

A trade is a "win" if P&L > 0 (after fees).

### Profit Factor (盈亏比 / 利润因子)
```
Profit Factor = Gross Profit (sum of all winning trades' P&L)
                ──────────────────────────────────────────────
                Gross Loss (sum of all losing trades' P&L)
```

Interpretation:
- > 2.0: Excellent
- 1.5 - 2.0: Good
- 1.0 - 1.5: Acceptable
- < 1.0: Losing system

### Sharpe Ratio (夏普比率)
```
Sharpe = (Avg Daily Return - Risk-Free Rate) / Std Dev of Daily Returns × √252
```

Risk-free rate default: 2% (assumed annual). Uses √252 for daily→annual scaling.

Interpretation:
- > 2.0: Excellent
- 1.0 - 2.0: Good
- 0.5 - 1.0: Acceptable
- < 0.5: Below average

### Maximum Drawdown (最大回撤)
```
Max DD = Max(Peak Value - Trough Value) / Peak Value × 100%
```

The largest peak-to-trough decline in cumulative P&L.

### Average Trade (平均盈亏)
```
Avg Trade = Total P&L / Number of Trades
```

### Payoff Ratio (盈亏比)
```
Payoff Ratio = Avg Win / Avg Loss
```

## Advanced Metrics

### Expectancy (期望值)
```
Expectancy = (Win Rate × Avg Win) - (Loss Rate × Avg Loss)
```

Expected P&L per trade. Positive expectancy = edge.

### Calmar Ratio (卡玛比率)
```
Calmar = Annualized Return / Max Drawdown
```

Measures return relative to drawdown risk.

### % Profitable Days (盈利日占比)
```
% Profitable Days = Days with net positive P&L / Total Trading Days × 100%
```

### Consecutive Wins/Losses (连胜/连败)
```
Max Consecutive Wins = Longest streak of winning trades
Max Consecutive Losses = Longest streak of losing trades
```

### Recovery Factor (恢复因子)
```
Recovery Factor = Total P&L / Max Drawdown
```

## Report Template

### Daily Summary
```
📓 今日交易总结 (YYYY-MM-DD)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
  交易数:    N
  盈利:      N
  亏损:      N
  胜率:      X%
  盈亏:      ¥X.XX
  最大盈利:  ¥X.XX
  最大亏损:  -¥X.XX
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Monthly Report
```
📊 月度绩效报告 (YYYY-MM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  交易日数:      N
  总交易数:     N
  胜率:         X%
  总盈亏:       ¥X.XX
  盈亏比:       X.XX
  夏普比率:     X.XX
  最大回撤:     X%
  平均每笔:     ¥X.XX
  连胜:         N
  连败:         N
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

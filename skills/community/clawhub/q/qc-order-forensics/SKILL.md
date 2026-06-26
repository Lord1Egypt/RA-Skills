---
name: qc-order-forensics
description: Forensic diagnosis engine for backtest order data — trade quality, ROI attribution, monthly cashflow, drawdown root-cause analysis, and LLM-readable reports.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F52C"
---

# QC Order Forensics

Turn raw backtest order data into actionable diagnostic reports. Feed the output directly to an LLM for strategy improvement decisions.

## When to use

Use this skill when the user has completed a backtest and wants to understand **why** the strategy performed the way it did. Typical triggers:

- "Analyze my backtest results"
- "Why did my strategy lose money?"
- "Show me the trade quality report"
- "Diagnose this backtest"

## How it works

The `OrderForensics` class takes an `orders.csv` (and optionally a `result.json`) and produces a multi-section diagnostic report:

```python
from forensics import OrderForensics

forensics = OrderForensics("path/to/orders.csv", "path/to/result.json")
report = forensics.full_diagnosis()
print(report)  # LLM-readable text report
```

Or from CLI:
```bash
python3 -c "
from forensics import OrderForensics
f = OrderForensics('orders.csv', 'result.json')
print(f.full_diagnosis())
"
```

## Report Sections

### 1. Key Statistics
Extracted from `result.json`: Net Profit, Sharpe Ratio, Drawdown, Win Rate, Expectancy, Alpha, Beta, Total Fees.

### 2. Trade Quality Detection
- Total order count (options vs equity)
- Buy/sell split with average fill prices
- Number of unique underlyings traded
- **Zero rate**: % of options sold at <= $0.05 (expired worthless)
- **Windfall trades**: Count of trades exceeding 100%, 400%, 1000% ROI

### 3. ROI Breakdown by Contract
- Per-symbol: Cost, Return, Net Profit, ROI%
- Top 5 winners and Top 5 losers
- Overall option ROI, winning vs losing symbol counts
- Average winner ROI vs average loser ROI

### 4. Monthly Cashflow
- Net cash flow per month (buys + sells)
- Cumulative cashflow curve
- Trade count and buy/sell density per month
- Identifies bleeding months vs profitable months

### 5. Drawdown Death Causes
- Detects consecutive loss streaks exceeding $1,000
- Reports start/end month and cumulative loss for each streak
- Sorted by severity (worst first)

### 6. Yearly Breakdown
- Annual net cashflow, trade count, and ticker diversity
- Identifies which years were profitable vs destructive

## Input Format

**orders.csv** columns (standard QC export):
```
orderId, symbol, type, direction, quantity, fillPrice, fillQty, fee, status, submitTime, fillTime, tag
```

The parser automatically separates options from equity (QQQ) orders by extracting the underlying from the symbol field.

## Output

A structured plain-text report using emoji markers for quick visual scanning. Designed to be directly consumed by LLMs for follow-up analysis and strategy iteration decisions.

## Key Metrics to Watch

| Metric | Healthy Range | Red Flag |
|--------|---------------|----------|
| Zero rate | < 50% | > 65% means most options expire worthless |
| Windfall > 400% | >= 2 per year | 0 means no tail wins to offset losses |
| Monthly cashflow | Mixed +/- | All negative = structural problem |
| Drawdown streaks | < 3 months | > 6 months = survival crisis |

## Rules

- **Input CSV must be in standard QuantConnect export format** with columns: `orderId, symbol, type, direction, quantity, fillPrice, fillQty, fee, status, submitTime, fillTime, tag`. Missing columns will cause silent misclassification.
- **Do not manually edit the orders CSV before analysis.** Changing fill prices, removing rows, or reordering columns will produce misleading diagnostics.
- **The `equity_symbol` parameter (default "QQQ") must match your strategy's anchor equity.** If your strategy holds SPY instead of QQQ, pass `--equity-symbol SPY` or the equity/options split will be wrong.
- **Zero rate above 65% is not automatically bad** for OTM lottery strategies — it's expected. Interpret in context of the strategy's design, not as an absolute red flag.
- **This tool analyzes closed trades only.** Open positions at backtest end are excluded from ROI calculations.

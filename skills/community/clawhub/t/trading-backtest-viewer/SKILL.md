---
name: trading-backtest-viewer
description: Parse and summarize backtest results from D:/Stock/ — win rate, Sharpe, drawdown, returns
---

## trading-backtest-viewer

Read and summarize trading backtest results stored as JSON in `D:/Stock/`.

### Steps

1. Read the backtest result files:
   - `D:/Stock/backtest_results.json` (summary)
   - `D:/Stock/backtest_results_full.json` (detailed)

2. Extract and report the following metrics:
   - **Total return** (percentage)
   - **Win rate** (% of winning trades)
   - **Sharpe ratio** (if available)
   - **Max drawdown** (peak-to-trough decline)
   - **Number of trades**
   - **Average trade duration**
   - **Profit factor** (gross profit / gross loss)

3. If metrics are missing or the JSON schema differs, parse whatever is present and note gaps.

4. Present results in a clean summary table:

   ```
   ## Backtest Summary
   | Metric        | Value     |
   |---------------|-----------|
   | Total Return  | +XX.X%    |
   | Win Rate      | XX.X%     |
   | Sharpe Ratio  | X.XX      |
   | Max Drawdown  | -XX.X%    |
   | Trades        | NNN       |
   ```

5. Offer to compare with the other file (`_full.json` vs `_results.json`) if both exist.

### Notes

- The data lives in `D:/Stock/backtest_results*.json`.
- Do NOT modify the files — read-only analysis.
- If Python is available, you may use `python -c "import json; ..."` for structured parsing.

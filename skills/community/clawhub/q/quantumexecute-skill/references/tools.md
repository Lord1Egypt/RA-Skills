# Tools Reference

## Scope

- TCA data query
- TCA savings calculation
- Excel exports

## Core Commands

```bash
python3 scripts/get_tca_analysis.py --help
python3 scripts/calculate_tca_savings.py --help
python3 scripts/export_master_orders_excel.py --help
python3 scripts/export_order_fills_excel.py --help
python3 scripts/export_tca_analysis_excel.py --help
```

## TCA Query Rules (P0)

1. Use `get_tca_analysis.py` for authenticated TCA data queries.
2. If user asks for metrics only, return metrics from script output.
3. Do not use unauthenticated PDF endpoints for user-facing skill workflows.

## TCA Calculation Rules (P0)

1. `Total Value = (MakeQty + TakeQty) * AvgFill`
2. `Maker Rate = MakeQty / (MakeQty + TakeQty)`
3. `Fee Savings = Total Value * TakeMakeFeeDiff * Maker Rate`
4. `Slippage Amount = Total Value * abs(slippage_rate)`
5. Sign mapping:
   - `slippage > 0` => cost
   - `slippage < 0` => saved
6. Precision:
   - slippage percentage: 3 decimals
   - amount values: 2 decimals

## Export Rules

1. Return exact file path from script output.
2. Return exact record count from script output.
3. Do not invent rows or post-process totals.

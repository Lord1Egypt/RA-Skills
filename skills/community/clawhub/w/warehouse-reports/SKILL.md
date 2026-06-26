---
name: warehouse-chart-reports
description: Generate warehouse analytics charts, table images, and report-ready visuals from SQLite/CSV data. Use when the user asks for warehouse charts, product table images, stock health pie charts, revenue/profit visuals, missing-product visuals, or image assets for PDF/slide reporting.
---

# Warehouse Chart Reports

Use this skill to produce clean chart/report images for warehouse demos.

## Run full warehouse visual pack (recommended)

Execute:

```bash
python skills/warehouse-chart-reports/scripts/run_warehouse_reports.py \
  --db demo/warehouse_agent/warehouse_demo.db \
  --out demo/warehouse_agent/outputs
```

This generates:
- `stock_status_pie.png`
- `revenue_by_category.png`
- `daily_profit_30d.png`
- `product_table_top40.png`
- `missing_products.csv`
- `kpi_summary.txt`

## Generate product table image only

Execute:

```bash
python skills/warehouse-chart-reports/scripts/product_table_image.py \
  --db demo/warehouse_agent/warehouse_demo.db \
  --out demo/warehouse_agent/outputs/product_table_top40.png \
  --limit 40
```

## Notes

- Prefer virtualenv Python when matplotlib is unavailable system-wide.
- Keep chart style simple and readable for PDF embedding.
- If sales timestamps are sparse for today, use the 30-day profit chart for trend visibility.

---
name: data-analyzer
description: Data analysis and visualization skill for CSV, Excel, and JSON data. Use when analyzing sales data, creating reports, generating charts, or processing e-commerce analytics. Supports pivot tables, statistical analysis, and automated reporting.
---

# Data Analyzer

## Overview

Professional data analysis skill for OpenClaw. Analyze CSV, Excel, and JSON data with statistical functions, visualizations, and automated report generation.

## Features

- CSV/Excel/JSON data processing
- Basic statistical analysis
- HTML report generation
- Group-by analysis
- E-commerce data support

## Quick Start

### Analyze Data

```bash
python scripts/analyze_data.py \
  --input sales.csv \
  --output report.html \
  --group-by date
```

### Generate JSON Summary

```bash
python scripts/analyze_data.py \
  --input orders.json \
  --output summary.json
```

## Scripts

### analyze_data.py

Analyze CSV/Excel/JSON data and generate reports.

**Arguments:**
- `--input` - Input data file
- `--output` - Output report file
- `--group-by` - Group data by field
- `--metrics` - Metrics to calculate (comma-separated)
- `--format` - Output format (html, json)

## E-commerce Analytics

### Taobao/Douyin Sales Analysis

```bash
# Daily sales report
python scripts/analyze_sales.py \
  --input taobao_orders.csv \
  --output daily_report.html \
  --group-by product \
  --metrics revenue,quantity,profit

# Monthly trend analysis
python scripts/generate_charts.py \
  --input monthly_sales.json \
  --charts line \
  --x-axis month \
  --y-axis revenue
```

### Inventory Analysis

```bash
python scripts/inventory_analysis.py \
  --input stock_levels.csv \
  --output inventory_report.xlsx \
  --alert-low-stock 10
```

### Customer Analytics

```bash
python scripts/customer_analysis.py \
  --input customers.csv \
  --output customer_segments.html \
  --segment-by purchase_frequency
```

## Output Formats

### HTML Report

Interactive report with charts and tables.

### Excel Workbook

Multiple sheets with raw data, analysis, and charts.

### CSV Export

Clean data for further processing.

## Templates

### Daily Sales Report

- Total revenue
- Order count
- Top products
- Hourly breakdown

### Weekly Summary

- Week-over-week comparison
- Trend analysis
- Top categories
- Customer insights

### Monthly Executive Report

- KPI dashboard
- Revenue breakdown
- Growth metrics
- Recommendations

## Best Practices

1. **Clean data first** - Remove duplicates, handle missing values
2. **Validate inputs** - Check data types and ranges
3. **Use appropriate charts** - Match chart type to data
4. **Label clearly** - Add titles, axis labels, legends
5. **Export in multiple formats** - HTML for viewing, CSV for further analysis

## Troubleshooting

- **Import errors**: Install required packages (pandas, matplotlib)
- **Memory issues**: Process large files in chunks
- **Chart rendering**: Check output directory permissions
- **Date parsing**: Ensure consistent date formats

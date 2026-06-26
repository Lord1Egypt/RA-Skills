# 📊 Data Analyst Skill

Enterprise-grade data analysis assistant for OpenClaw. Automatically clean, analyze, and visualize your data.

## Features

✅ **Automatic Data Cleaning**
- Remove duplicates
- Handle missing values intelligently
- Standardize formats
- Detect and handle outliers

✅ **Comprehensive Analysis**
- Statistical summaries
- Correlation analysis
- Trend detection
- Pattern recognition

✅ **Beautiful Visualizations**
- Distribution charts
- Correlation heatmaps
- Time series plots
- Categorical breakdowns

✅ **Professional Reports**
- Executive summaries
- Detailed statistics
- Actionable insights
- Recommendations

## Supported Formats

| Format | Read | Write |
|--------|------|-------|
| CSV | ✅ | ✅ |
| Excel (.xlsx) | ✅ | ✅ |
| JSON | ✅ | ✅ |
| TSV | ✅ | ✅ |

## Quick Start

### Installation

```bash
# Install dependencies
pip3 install pandas openpyxl matplotlib seaborn

# Verify
python3 -c "import pandas, matplotlib; print('OK')"
```

### Basic Usage

```bash
# Simple analysis
{baseDir}/tools/analyze.py your_data.csv

# Full analysis with all features
{baseDir}/tools/analyze.py your_data.csv --clean --visualize --report
```

## Examples

### Sales Data Analysis

```bash
# Analyze sales trends
{baseDir}/tools/analyze.py sales.csv --visualize --report

# Output:
# - sales_summary.json
# - sales_cleaned.csv
# - sales_distributions.png
# - sales_correlation.png
# - sales_report.md
```

### Customer Data Cleaning

```bash
# Clean messy customer data
{baseDir}/tools/analyze.py customers.csv --clean

# Output:
# - customers_cleaned.csv (ready for analysis)
```

### Financial Reporting

```bash
# Generate executive report
{baseDir}/tools/analyze.py financials.xlsx \
  --report \
  --title "Q4 Financial Summary" \
  --output q4_report.md
```

## Use Cases

### Business Analytics
- Sales trend analysis
- Customer segmentation
- Revenue forecasting
- Performance dashboards

### Data Quality
- Duplicate detection
- Missing value analysis
- Format standardization
- Anomaly detection

### Reporting
- Executive summaries
- Department reports
- Trend analysis
- KPI tracking

## Command Reference

### Main Analysis

```bash
analyze.py FILE [OPTIONS]

Options:
  --clean              Clean data before analysis
  --visualize          Generate visualizations
  --report             Generate full report
  --output, -o         Output file path
  --sample             Sample fraction (e.g., 0.1)
  --columns            Specific columns (comma-separated)
  --encoding           File encoding (default: utf-8)
```

### Data Cleaning

```bash
# Default cleaning strategy
analyze.py data.csv --clean

# Specific strategies
analyze.py data.csv --clean --strategy drop      # Remove rows with missing
analyze.py data.csv --clean --strategy fill_mean # Fill with mean
analyze.py data.csv --clean --strategy fill_median # Fill with median
```

### Visualization

```bash
# Auto-generate charts
analyze.py data.csv --visualize

# Specific chart types
visualize.py data.csv --type bar
visualize.py data.csv --type line
visualize.py data.csv --type scatter
visualize.py data.csv --type pie
```

### Reporting

```bash
# Full report
analyze.py data.csv --report

# Custom report
report.py summary.json --title "My Report" --author "Data Team"
```

## Output Files

| File | Description |
|------|-------------|
| `*_summary.json` | Statistical summary |
| `*_cleaned.csv` | Cleaned data |
| `*_chart_*.png` | Visualizations |
| `*_report.md` | Analysis report |

## Pricing

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | Basic analysis, 100 rows/month |
| Pro | $29/month | Unlimited rows, all features |
| Enterprise | Custom | Priority support, custom development |

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join community](https://discord.gg/example)
- 📖 Docs: [Full documentation](https://docs.example.com)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Made with ❤️ for the OpenClaw community**

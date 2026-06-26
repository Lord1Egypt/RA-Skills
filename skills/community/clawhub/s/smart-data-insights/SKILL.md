---
name: data-analyst
description: |
  Enterprise-grade data analysis assistant. Clean, analyze, and visualize data automatically.
  
  **Triggers when user mentions:**
  - Data cleaning: "数据清洗", "整理数据", "清理数据", "数据预处理"
  - Data analysis: "分析数据", "数据分析", "数据报表", "生成报告"
  - Visualization: "画图", "图表", "可视化", "生成图表"
  - Excel/CSV: "处理Excel", "分析CSV", "读取表格"
  - Insights: "数据洞察", "发现规律", "趋势分析"
  
  Supports Excel (.xlsx), CSV, JSON formats. Generates reports, charts, and insights.
homepage: https://github.com/yourusername/data-analyst-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3", "pip3"] },
        "install":
          [
            {
              "id": "pandas",
              "kind": "pip",
              "package": "pandas",
              "label": "Install pandas: pip3 install pandas",
            },
            {
              "id": "openpyxl",
              "kind": "pip",
              "package": "openpyxl",
              "label": "Install openpyxl: pip3 install openpyxl",
            },
            {
              "id": "matplotlib",
              "kind": "pip",
              "package": "matplotlib",
              "label": "Install matplotlib: pip3 install matplotlib",
            },
          ],
        "installScripts": ["install.sh"],
      },
  }
---

# Data Analyst Skill

Automatically clean, analyze, and visualize enterprise data.

## Features

| Feature | Description | Reference |
|---------|-------------|-----------|
| Data Cleaning | Remove duplicates, handle missing values, standardize formats | `references/data_cleaning.md` |
| Data Analysis | Statistics, trends, correlations | `references/data_analysis.md` |
| Visualization | Charts, graphs, dashboards | `references/visualization.md` |
| Report Generation | Automated insights and recommendations | `references/report_generation.md` |

## Quick Start

### Step 1: Prepare Your Data

Place your data file (Excel/CSV/JSON) in a known location.

### Step 2: Analyze Data

```bash
# Basic analysis
{baseDir}/tools/analyze.py data.csv

# With specific options
{baseDir}/tools/analyze.py data.xlsx --clean --visualize --report
```

### Step 3: Get Results

Output includes:
- Cleaned data file
- Analysis summary
- Visualization charts
- Insights report

## Available Tools

| Tool | Function | Input | Output |
|------|----------|-------|--------|
| `analyze.py` | Main analysis entry point | Data file | Summary + options |
| `clean.py` | Data cleaning | Raw data | Clean data |
| `visualize.py` | Generate charts | Data | PNG/PDF charts |
| `report.py` | Generate reports | Analysis results | Markdown report |

## Usage Examples

### Example 1: Quick Analysis

**"帮我分析这个销售数据"**

```bash
# Place your file as sales_data.csv
{baseDir}/tools/analyze.py sales_data.csv
```

Output:
```
✅ Data loaded: 1,234 rows, 8 columns
📊 Summary statistics generated
📈 Visualization: sales_trend.png
💡 3 key insights found
```

### Example 2: Data Cleaning + Analysis

**"清洗并分析客户数据"**

```bash
{baseDir}/tools/analyze.py customer_data.xlsx --clean --visualize
```

### Example 3: Generate Full Report

**"生成完整的数据报告"**

```bash
{baseDir}/tools/analyze.py data.csv --report --output report.md
```

## Supported Formats

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| CSV | ✅ | ✅ | Universal format |
| Excel (.xlsx) | ✅ | ✅ | Requires openpyxl |
| JSON | ✅ | ✅ | Structured data |
| TSV | ✅ | ✅ | Tab-separated |

## Output Files

| File | Description |
|------|-------------|
| `*_cleaned.csv` | Cleaned data |
| `*_summary.txt` | Statistical summary |
| `*_chart_*.png` | Visualizations |
| `*_report.md` | Full analysis report |

## Common Use Cases

### Business Analytics
- Sales trend analysis
- Customer segmentation
- Revenue forecasting
- Performance dashboards

### Data Quality
- Duplicate detection
- Missing value handling
- Format standardization
- Anomaly detection

### Reporting
- Executive summaries
- Department reports
- Trend analysis
- KPI tracking

## Advanced Features

### Custom Analysis
```bash
# Specific columns only
{baseDir}/tools/analyze.py data.csv --columns "sales,date,region"

# Time series analysis
{baseDir}/tools/analyze.py data.csv --timeseries --date-column "date"

# Group by category
{baseDir}/tools/analyze.py data.csv --group-by "region" --aggregate "sum,mean"
```

### Visualization Options
```bash
# Chart types
{baseDir}/tools/visualize.py data.csv --type bar
{baseDir}/tools/visualize.py data.csv --type line
{baseDir}/tools/visualize.py data.csv --type scatter
{baseDir}/tools/visualize.py data.csv --type pie

# Styling
{baseDir}/tools/visualize.py data.csv --style professional
{baseDir}/tools/visualize.py data.csv --colors "blue,green,red"
```

## Setup

```bash
# Install dependencies
pip3 install pandas openpyxl matplotlib seaborn

# Verify installation
python3 -c "import pandas, matplotlib; print('Dependencies OK')"
```

## Notes

- ⚠️ Large files (>100MB) may take time to process
- ⚠️ Excel files require openpyxl
- ⚠️ Charts saved as PNG by default
- ⚠️ All processing is local (no data sent externally)

## Troubleshooting

**"Module not found"**
```bash
pip3 install pandas openpyxl matplotlib
```

**"File encoding error"**
- Try converting to UTF-8 first
- Or specify encoding: `--encoding gbk`

**"Memory error with large files"**
- Process in chunks: `--chunk-size 10000`
- Or sample data: `--sample 0.1`

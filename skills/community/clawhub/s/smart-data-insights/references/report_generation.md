# Report Generation Reference

## Overview

The report generation module creates comprehensive analysis reports in Markdown format.

## Report Components

### 1. Executive Summary

High-level overview including:
- Dataset size and structure
- Key quality metrics
- Critical findings
- Priority actions

### 2. Dataset Overview

| Metric | Description |
|--------|-------------|
| Rows | Total number of records |
| Columns | Number of variables |
| Missing Values | Total missing data points |
| Duplicate Rows | Number of identical rows |

### 3. Column Information

For each column:
- Data type
- Missing count and percentage
- Unique values (for categorical)
- Basic statistics (for numeric)

### 4. Statistical Summaries

**Numeric Columns**:
- Central tendency (mean, median)
- Dispersion (std, min, max)
- Distribution shape

**Categorical Columns**:
- Value counts
- Mode and frequency
- Cardinality

### 5. Data Quality Issues

Categorized issues:
- Missing values
- Duplicates
- Outliers
- Inconsistencies

### 6. Key Insights

Prioritized findings:
- **High**: Critical issues requiring immediate action
- **Medium**: Important patterns to consider
- **Low**: Nice-to-know information

### 7. Recommendations

Actionable suggestions:
- Data cleaning steps
- Feature engineering ideas
- Analysis directions
- Next steps

## Usage

### Generate Full Report

```bash
# Complete report with all sections
{baseDir}/tools/analyze.py data.csv --report

# Specify output location
{baseDir}/tools/analyze.py data.csv --report --output my_report.md
```

### Combined Analysis

```bash
# Analysis + cleaning + visualization + report
{baseDir}/tools/analyze.py data.csv --clean --visualize --report
```

### Custom Reports

```bash
# Executive summary only
{baseDir}/tools/report.py summary.json --type executive

# Data quality focus
{baseDir}/tools/report.py summary.json --type quality

# Statistical focus
{baseDir}/tools/report.py summary.json --type statistics
```

## Report Formats

### Markdown (Default)

- Human-readable
- Easy to version control
- Can be converted to HTML/PDF
- Supports tables and formatting

### HTML

```bash
# Generate HTML report
{baseDir}/tools/analyze.py data.csv --report --format html
```

### PDF

```bash
# Generate PDF report (requires pandoc)
{baseDir}/tools/analyze.py data.csv --report --format pdf
```

## Customization

### Report Sections

```bash
# Include specific sections only
{baseDir}/tools/analyze.py data.csv --report --sections "summary,quality,insights"

# Exclude sections
{baseDir}/tools/analyze.py data.csv --report --exclude "recommendations"
```

### Styling

```bash
# Custom title
{baseDir}/tools/analyze.py data.csv --report --title "Q4 Sales Analysis"

# Add author
{baseDir}/tools/analyze.py data.csv --report --author "Data Team"

# Custom template
{baseDir}/tools/analyze.py data.csv --report --template custom_template.md
```

## Output Structure

```markdown
# Data Analysis Report

*Generated: YYYY-MM-DD HH:MM:SS*

## Executive Summary
...

## Dataset Overview
| Metric | Value |
|--------|-------|
...

## Column Information
| Column | Type | Missing | % |
|--------|------|---------|---|
...

## Numeric Statistics
| Column | Mean | Median | Std | Min | Max |
|--------|------|--------|-----|-----|-----|
...

## Data Quality Issues
### Missing Values
...
### Duplicates
...

## Key Insights
### 🔴 High Priority
...
### 🟡 Medium Priority
...

## Recommendations
...
```

## Best Practices

1. **Review before sharing**
   - Verify accuracy
   - Check for sensitive data
   - Ensure clarity

2. **Customize for audience**
   - Executives: Focus on insights and recommendations
   - Analysts: Include detailed statistics
   - Engineers: Emphasize data quality

3. **Version control**
   - Save reports with timestamps
   - Track changes over time
   - Document methodology

4. **Actionable insights**
   - Link findings to actions
   - Prioritize recommendations
   - Assign ownership

## Integration

### With Other Tools

```bash
# Generate and email report
{baseDir}/tools/analyze.py data.csv --report | mail -s "Analysis Report" team@company.com

# Upload to cloud
{baseDir}/tools/analyze.py data.csv --report
aws s3 cp report.md s3://reports/

# Convert to presentation
pandoc report.md -o slides.pptx
```

### Automation

```bash
# Daily report cron job
0 9 * * * /path/to/analyze.py /data/daily.csv --report --output /reports/$(date +\%Y\%m\%d).md
```

## Troubleshooting

**"Report generation failed"**
- Check summary.json exists
- Verify write permissions
- Ensure sufficient disk space

**"Missing sections in report"**
- Verify data contains required columns
- Check analysis ran successfully
- Review error messages

**"Formatting issues"**
- Validate Markdown syntax
- Check for special characters
- Use UTF-8 encoding

## Examples

### Sales Report

```bash
{baseDir}/tools/analyze.py sales_2024.csv \
  --report \
  --title "2024 Sales Performance Report" \
  --author "Sales Analytics Team" \
  --output sales_report_2024.md
```

### Data Quality Report

```bash
{baseDir}/tools/analyze.py customer_data.csv \
  --report \
  --sections "summary,quality" \
  --title "Customer Data Quality Assessment" \
  --output quality_report.md
```

### Executive Dashboard

```bash
{baseDir}/tools/analyze.py metrics.csv \
  --clean \
  --visualize \
  --report \
  --format html \
  --title "Monthly Executive Dashboard" \
  --output dashboard.html
```

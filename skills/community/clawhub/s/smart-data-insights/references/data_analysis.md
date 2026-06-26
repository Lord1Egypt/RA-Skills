# Data Analysis Reference

## Overview

The analysis module provides comprehensive statistical analysis and insights generation.

## Analysis Components

### 1. Dataset Overview

- Row and column counts
- Data types for each column
- Memory usage

### 2. Missing Value Analysis

- Count of missing values per column
- Percentage of missing data
- Patterns in missing data

### 3. Numeric Statistics

For each numeric column:
- Mean, median, mode
- Standard deviation
- Min, max, range
- Quartiles (Q1, Q2, Q3)
- Skewness and kurtosis

### 4. Categorical Statistics

For each categorical column:
- Unique value count
- Value distribution
- Most common values

### 5. Correlation Analysis

- Correlation matrix for numeric columns
- Strong correlations (|r| > 0.8) highlighted
- Potential multicollinearity warnings

### 6. Outlier Detection

- IQR-based outlier detection
- Z-score analysis
- Outlier count per column

## Output Formats

### JSON Summary

```json
{
  "rows": 1000,
  "columns": 8,
  "column_names": ["col1", "col2", ...],
  "dtypes": {"col1": "int64", "col2": "object", ...},
  "missing_values": {"col1": 0, "col2": 50, ...},
  "missing_percentage": {"col1": 0, "col2": 5.0, ...},
  "numeric_stats": {
    "col1": {
      "mean": 100.5,
      "median": 98.0,
      "std": 15.2,
      "min": 50.0,
      "max": 200.0
    }
  },
  "categorical_stats": {
    "col2": {
      "unique_count": 5,
      "top_values": {"A": 300, "B": 250, ...}
    }
  }
}
```

### Markdown Report

Full report includes:
- Executive summary
- Dataset overview
- Column information
- Statistical summaries
- Data quality issues
- Key insights
- Recommendations

## Usage Examples

### Basic Analysis

```bash
# Quick analysis
{baseDir}/tools/analyze.py sales.csv

# With summary file
{baseDir}/tools/analyze.py sales.csv -o summary.json
```

### Full Analysis

```bash
# Complete analysis with all outputs
{baseDir}/tools/analyze.py sales.csv --clean --visualize --report
```

### Targeted Analysis

```bash
# Specific columns only
{baseDir}/tools/analyze.py sales.csv --columns "revenue,date,region"

# Sample for large datasets
{baseDir}/tools/analyze.py large_data.csv --sample 0.1
```

## Insights Generation

The system automatically generates insights:

### High Priority
- Critical data quality issues
- Columns with >20% missing data
- Significant outliers

### Medium Priority
- Strong correlations detected
- Time series patterns
- Categorical imbalances

### Low Priority
- Performance recommendations
- Feature engineering suggestions
- Data enrichment opportunities

## Interpretation Guide

### Correlation Values

| Value | Interpretation |
|-------|----------------|
| 0.8 to 1.0 | Strong positive correlation |
| 0.5 to 0.8 | Moderate positive correlation |
| 0.0 to 0.5 | Weak positive correlation |
| 0.0 | No correlation |
| -0.5 to 0.0 | Weak negative correlation |
| -0.8 to -0.5 | Moderate negative correlation |
| -1.0 to -0.8 | Strong negative correlation |

### Missing Data Thresholds

| Percentage | Action |
|------------|--------|
| < 5% | Minor, can ignore or simple imputation |
| 5-20% | Moderate, consider imputation strategy |
| 20-50% | Significant, investigate patterns |
| > 50% | Critical, consider dropping column |

### Outlier Detection

The IQR method identifies outliers as:
- Below: Q1 - 1.5 × IQR
- Above: Q3 + 1.5 × IQR

Where IQR = Q3 - Q1

## Best Practices

1. **Start with overview** - Understand dataset structure first
2. **Check missing data** - Address before analysis
3. **Review correlations** - Identify relationships
4. **Investigate outliers** - Understand their cause
5. **Document findings** - Keep track of insights

## Limitations

- Correlation ≠ Causation
- Outliers may be valid data points
- Missing data patterns may be informative
- Sample bias not automatically detected

## Next Steps

After analysis:
1. Clean data based on findings
2. Engineer new features
3. Build predictive models
4. Create visualizations
5. Share insights with stakeholders

# Data Cleaning Reference

## Overview

The data cleaning module automatically handles common data quality issues.

## Cleaning Strategies

### Automatic Cleaning (`--clean`)

When using `--clean` flag, the following operations are performed:

1. **Remove duplicates** - Identical rows are removed
2. **Handle missing values** - Strategy depends on data type and missing percentage
3. **Standardize column names** - Lowercase, replace spaces with underscores
4. **Clean text data** - Strip whitespace, normalize formats
5. **Remove extreme outliers** - Conservative approach (only <1% outliers)

### Missing Value Strategies

| Strategy | When to Use | Command |
|----------|-------------|---------|
| `auto` | Default, intelligent handling | `--clean` |
| `drop` | Remove all rows with any missing | `--clean --strategy drop` |
| `fill_mean` | Fill numeric with column mean | `--clean --strategy fill_mean` |
| `fill_median` | Fill numeric with column median | `--clean --strategy fill_median` |
| `fill_mode` | Fill with most common value | `--clean --strategy fill_mode` |

### Automatic Strategy Logic

For `auto` mode:
- Columns with >50% missing → **Drop column**
- Numeric columns → **Fill with median**
- Categorical columns → **Fill with mode**

## Examples

### Basic Cleaning

```bash
# Clean with default strategy
{baseDir}/tools/analyze.py data.csv --clean

# Output: data_cleaned.csv
```

### Specific Strategy

```bash
# Drop rows with missing values
{baseDir}/tools/analyze.py data.csv --clean --strategy drop

# Fill with mean
{baseDir}/tools/analyze.py data.csv --clean --strategy fill_mean
```

### Combined Analysis

```bash
# Clean, analyze, and visualize
{baseDir}/tools/analyze.py data.csv --clean --visualize --report
```

## What Gets Cleaned

| Issue | Action | Notes |
|-------|--------|-------|
| Duplicate rows | Removed | Keeps first occurrence |
| Missing values | Filled/Dropped | Based on strategy |
| Column names | Standardized | lowercase_with_underscores |
| Text whitespace | Trimmed | Leading/trailing spaces |
| Extreme outliers | Capped | Conservative (3×IQR) |

## Output Files

After cleaning, you'll get:
- `*_cleaned.csv` - Cleaned dataset
- `*_summary.json` - Cleaning summary

## Best Practices

1. **Always review** the summary before and after cleaning
2. **Backup** your original data
3. **Check** for unintended changes
4. **Document** your cleaning decisions

## Troubleshooting

**"Too many rows removed"**
- Use `auto` strategy instead of `drop`
- Check if data has systematic missing patterns

**"Column dropped unexpectedly"**
- Review missing percentage threshold (50%)
- Consider manual imputation for important columns

**"Outliers not removed"**
- Conservative approach only removes <1% outliers
- Manual outlier detection recommended for specific cases

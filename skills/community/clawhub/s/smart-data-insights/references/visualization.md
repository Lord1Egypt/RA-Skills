# Visualization Reference

## Overview

The visualization module generates publication-ready charts for data analysis.

## Chart Types

### 1. Missing Values Heatmap

**Purpose**: Visualize missing data patterns
**When to use**: Start of analysis, data quality assessment

![Missing Values Example](../templates/missing_values_example.png)

### 2. Distribution Histograms

**Purpose**: Show distribution of numeric variables
**When to use**: Understand data spread, identify skewness

![Distribution Example](../templates/distribution_example.png)

### 3. Correlation Heatmap

**Purpose**: Visualize relationships between variables
**When to use**: Feature selection, multicollinearity detection

![Correlation Example](../templates/correlation_example.png)

### 4. Categorical Bar Charts

**Purpose**: Show frequency of categorical values
**When to use**: Understand category distribution

![Categorical Example](../templates/categorical_example.png)

### 5. Time Series Plots

**Purpose**: Show trends over time
**When to use**: Temporal data analysis

![Time Series Example](../templates/timeseries_example.png)

## Usage

### Generate All Charts

```bash
# Auto-generate appropriate charts based on data
{baseDir}/tools/analyze.py data.csv --visualize
```

### Specific Chart Types

```bash
# Bar chart
{baseDir}/tools/visualize.py data.csv --type bar --x-column category --y-column value

# Line chart
{baseDir}/tools/visualize.py data.csv --type line --x-column date --y-column sales

# Scatter plot
{baseDir}/tools/visualize.py data.csv --type scatter --x-column x --y-column y

# Pie chart
{baseDir}/tools/visualize.py data.csv --type pie --column category
```

### Styling Options

```bash
# Professional style (default)
{baseDir}/tools/analyze.py data.csv --visualize --style professional

# Simple style
{baseDir}/tools/analyze.py data.csv --visualize --style simple

# Custom colors
{baseDir}/tools/analyze.py data.csv --visualize --colors "blue,green,red"
```

## Output Files

Charts are saved as:
- Format: PNG (default) or PDF
- Resolution: 150 DPI (suitable for reports)
- Naming: `{basename}_{chart_type}.png`

## Customization

### Chart Size

```bash
# Larger charts for presentations
{baseDir}/tools/visualize.py data.csv --width 12 --height 8

# Compact charts for reports
{baseDir}/tools/visualize.py data.csv --width 8 --height 5
```

### Color Schemes

| Scheme | Description |
|--------|-------------|
| `default` | Blue-based professional palette |
| `colorful` | Vibrant multi-color palette |
| `grayscale` | Black and white for printing |
| `corporate` | Company brand colors |

### Font Options

```bash
# Larger fonts for presentations
{baseDir}/tools/visualize.py data.csv --font-size 14

# Smaller fonts for dense reports
{baseDir}/tools/visualize.py data.csv --font-size 10
```

## Best Practices

1. **Choose appropriate chart type**
   - Comparison → Bar chart
   - Trend → Line chart
   - Distribution → Histogram
   - Correlation → Scatter plot
   - Composition → Pie chart

2. **Keep it simple**
   - One message per chart
   - Avoid clutter
   - Use clear labels

3. **Color usage**
   - Use consistent colors
   - Consider colorblind-friendly palettes
   - Limit to 5-7 colors

4. **Labels and titles**
   - Always include axis labels
   - Add descriptive titles
   - Include units where applicable

## Troubleshooting

**"Charts not generated"**
- Check if matplotlib is installed: `pip3 install matplotlib`
- Verify data has suitable columns

**"Poor quality charts"**
- Increase DPI: `--dpi 300`
- Adjust size: `--width 12 --height 8`

**"Memory error with large datasets"**
- Sample data first: `--sample 0.1`
- Reduce number of charts

## Integration

Charts can be:
- Embedded in reports
- Included in presentations
- Shared via email
- Published to dashboards

## Examples

### Sales Analysis

```bash
# Complete sales visualization
{baseDir}/tools/analyze.py sales.csv --visualize --style professional

# Output:
# - sales_missing_values.png
# - sales_distributions.png
# - sales_correlation.png
# - sales_cat_region.png
# - sales_timeseries.png
```

### Customer Segmentation

```bash
# Customer data visualization
{baseDir}/tools/visualize.py customers.csv --type scatter \
  --x-column age --y-column income \
  --color-column segment --style colorful
```

### Financial Report

```bash
# Professional financial charts
{baseDir}/tools/visualize.py financials.csv --type bar \
  --x-column quarter --y-column revenue \
  --style corporate --dpi 300
```

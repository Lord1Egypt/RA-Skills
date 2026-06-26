---
name: data-analyzer
description: Load, analyze, and report on structured data from CSV/Excel/JSON files. Use when the user needs to: (1) compute descriptive statistics (mean, median, std dev, percentiles), (2) detect anomalies and trends, (3) analyze correlations between variables, (4) generate data analysis reports with visualization recommendations, (5) explore and summarize a new dataset.
emoji: 📊
---

# Data Analyzer — 数据分析工具

Load, analyze, and report on structured data from CSV, Excel, and JSON files. Compute statistics, detect anomalies, identify trends, and generate reports with visualization recommendations.

## Workflow

```
1. Load data     → Read the file, inspect structure
2. Profile       → Column types, missing values, basic stats
3. Analyze       → Statistics, trends, anomalies, correlations
4. Report        → Summary with visual recommendations
```

## Step 1 — Data Loading

### Supported Formats

| Format | How to Read | Notes |
|:---|:---|:---|
| **CSV** | Read the file directly, parse header row + data rows | Check delimiter (comma, tab, semicolon). Handle quoted fields. |
| **Excel (.xlsx)** | Read via `openpyxl` or `pandas`. If unavailable, convert to CSV first. | Handle multiple sheets. Note which sheet was used. |
| **JSON** | Parse as structured objects. Detect if array-of-objects or object-of-arrays. | Flatten nested structures where possible. |
| **TSV** | Same as CSV with tab delimiter. | |

**If Python is available** (recommended for large datasets):
```bash
pip install pandas openpyxl  # if missing
python3 -c "
import pandas as pd
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())
print(df.head())
"
```

**If Python is not available**, parse manually:
1. Read the file line by line
2. Identify headers (first row)
3. Identify column types (numeric vs text vs date)
4. Store as an array of rows or objects

### Initial Inspection

After loading, always answer these questions:
- **Shape:** How many rows and columns?
- **Column names:** What are they and what data types?
- **Missing values:** Which columns have gaps, and how many?
- **Date/time columns:** Are they parsed as datetime objects?
- **Unique values:** For categorical columns, how many unique categories?

## Step 2 — Descriptive Statistics

### Numeric Columns

Compute and report:

| Statistic | What It Tells You |
|:---|:---|
| **Count** | Number of non-null values |
| **Mean** | Average value |
| **Median** | Midpoint (50th percentile) — more robust than mean for skewed data |
| **Std Dev** | Spread around the mean |
| **Min / Max** | Full range |
| **25th / 75th Percentile** | Interquartile range bounds |
| **Skewness** | Symmetry of the distribution. Positive = right tail, negative = left tail. |

**Formula reference (manual calculation):**
```
Mean       = sum(x) / n
Median     = middle value when sorted
Std Dev    = sqrt(sum((x - mean)^2) / (n-1))
Percentile = sort values, take value at position (p/100 * n)
```

### Categorical Columns

| Statistic | What It Tells You |
|:---|:---|
| **Count** | Total non-null values |
| **Unique** | Number of distinct categories |
| **Top** | Most frequent category |
| **Frequency** | How often the top category appears |
| **Distribution** | Share of each category (as percentages) |

## Step 3 — Analysis

### 3a. Anomaly Detection

**Method: IQR (Interquartile Range)**

```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower fence = Q1 - 1.5 * IQR
Upper fence = Q3 + 1.5 * IQR
Anomaly = any value outside [Lower fence, Upper fence]
```

**Method: Z-Score (for approximately normal distributions)**

```
z = (x - mean) / std_dev
Anomaly = |z| > 3 (values more than 3 std devs from mean)
```

**Output anomalies:** For each detected anomaly, report:
- Row index
- Column name
- Anomalous value
- Distance from expected (how many IQRs or std devs)

### 3b. Trend Analysis

**For time-series data** (data with a date/time column):

1. **Identify the time column** — Sort by date
2. **Aggregate by period** — Group by day/week/month/quarter/year
3. **Direction** — Is the metric increasing, decreasing, or flat?
4. **Rate of change** — Period-over-period percentage change
5. **Seasonality** — Recurring patterns (monthly, quarterly, yearly)
6. **Breakout** — Sudden jumps or drops (potential regime changes)

**Output format:**
```
📈 Trend: [Metric Name]
Period: [Date Range]
Direction: [Up/Down/Flat] (slope: ±X%)
Key Points:
- [Date]: Value = X (↗/↘/→)
- Highest point: [Date] = X
- Lowest point: [Date] = X
```

**For non-time-series data**, analyze rank order and distribution shape:
```
Top 5 by [metric]:
1. [Category] = X
2. [Category] = Y
...
Bottom 5 by [metric]:
```

### 3c. Correlation Analysis

**Pearson correlation coefficient** (for linear relationships between two numeric variables):

```
r = sum((x - mean_x) * (y - mean_y)) / (n * std_x * std_y)
```

**Interpretation:**

| r value | Strength | Direction |
|:--------|:---------|:----------|
| 0.7 to 1.0 | Strong | Positive (both rise together) |
| 0.3 to 0.7 | Moderate | Positive |
| 0 to 0.3 | Weak | Positive |
| -0.3 to 0 | Weak | Negative (one rises, other falls) |
| -0.7 to -0.3 | Moderate | Negative |
| -1.0 to -0.7 | Strong | Negative |

**Caveats:**
- Correlation ≠ causation. Always note this.
- Pearson only captures linear relationships.
- Outliers can distort correlation heavily — check after removing anomalies.

## Step 4 — Report Generation

### Visualization Recommendations

For each finding, recommend the best chart type:

| Analysis Type | Recommended Chart | Why |
|:---|:---|:---|
| Distribution of one variable | **Histogram** | Shows shape, skew, peaks |
| Comparison across categories | **Bar chart** | Easy to compare magnitudes |
| Trend over time | **Line chart** | Emphasizes direction and continuity |
| Relationship between 2 variables | **Scatter plot** | Shows correlation, clusters, outliers |
| Part of a whole | **Pie / Donut chart** | Use only for 2-5 categories |
| Composition over time | **Stacked area chart** | Shows both total and parts |
| Rank order | **Horizontal bar chart** | Easy to read sorted values |
| Comparing multiple distributions | **Box plot** | Shows median, IQR, outliers |
| Heatmap (correlation matrix) | **Heatmap** | Quick visual of many correlations |

### Full Report Template

```
# Data Analysis Report: [Dataset Name]
Date: [YYYY-MM-DD]

## 1. Overview
- Rows: X | Columns: Y
- Missing data: X cells (X%)
- Key columns: [list with types]

## 2. Descriptive Statistics
### Numeric Columns
[Table: col_name, count, mean, median, std, min, 25%, 75%, max]

### Categorical Columns
[Table: col_name, unique_count, top_value, frequency%]

## 3. Key Findings

### Finding 1: [Title]
[Description of finding]
📊 Recommended chart: [Chart type]
Supporting data: [stats/view]

### Finding 2: [Title]
...

## 4. Anomalies Detected
[Table: row, column, value, severity]

## 5. Correlations
[Notable correlations >|0.3| or < -|0.3|]

## 6. Recommendations
[Data-driven suggestions based on analysis]
```

### One-Page Summary (Quick)

For quick results, use this compact format:

```
📊 [Dataset]: [N] rows × [M] cols

📈 Key metrics:
- [metric1]: mean=X, median=Y, range=[min, max]
- [metric2]: ...

🔍 Top findings:
1. [Finding] — [chart recommendation]
2. [Finding] — [chart recommendation]

⚠️ Anomalies: X detected
```

## Python Script (Optional)

For complex analysis, create and run a Python script:

```python
import csv, json, statistics
from collections import Counter

# Load data
with open('data.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Get numeric columns
# (column name → list of float values, filtering out blanks)
# Compute mean, median, stdev, percentiles
# Detect outliers via IQR
# Compute correlations between pairs
# Print formatted results
```

Run with:
```bash
python3 analysis.py
```

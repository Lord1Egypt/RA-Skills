# Data Analyzer

Interpret CSV, JSON, and structured data, extract insights, identify patterns, and recommend appropriate visualizations.

## Description

This skill provides a systematic approach to data analysis for tabular and structured data. It covers data profiling, statistical summary, trend identification, anomaly detection, and visualization recommendations. Designed for users who have data but need help understanding what it means and how to present it effectively.

## When to Use

- Analyzing CSV or JSON data files
- Understanding trends in sales, traffic, survey, or any time-series data
- Comparing groups, segments, or categories
- Identifying outliers or anomalies in datasets
- Preparing data insights for reports or presentations
- Recommending chart types for specific data stories

## Instructions

### Step 1: Data Profiling

Before analysis, profile the data:

```
Dataset Profile:
- Rows: [count]
- Columns: [count]
- Column types: [list each column with type: numeric, categorical, date, text]
- Missing values: [percentage per column]
- Date range: [if applicable]
- Key metrics summary: [mean, median, min, max for numeric columns]
```

Identify data quality issues:
- Missing values (>5% in any column needs attention)
- Duplicates
- Inconsistent formats (dates, categories, units)
- Outliers that might be errors vs. genuine extreme values

### Step 2: Analysis Framework

Apply the appropriate analysis based on data type and question:

#### For Time-Series Data (dates + values)

1. **Trend Analysis**: Is the metric growing, declining, or stable?
   - Calculate period-over-period change (MoM, YoY)
   - Identify inflection points (where trend direction changes)
   
2. **Seasonality**: Are there recurring patterns?
   - Weekly, monthly, or quarterly cycles
   - Compare same period across different years

3. **Anomaly Detection**: Any unexpected spikes or drops?
   - Flag values >2 standard deviations from the mean
   - Check if anomalies correlate with known events

#### For Categorical Comparisons

1. **Ranking**: Which categories lead/lag?
   - Sort by value
   - Calculate percentage of total for each category

2. **Distribution**: How are values spread?
   - Identify concentration (is 80% of value in 20% of categories?)

3. **Correlation**: Do categories relate?
   - Cross-tabulation between two categorical variables

#### For Numeric Relationships

1. **Correlation**: Do two metrics move together?
   - Note correlation direction and approximate strength
   - Caution: correlation ≠ causation — always state this

2. **Segmentation**: How do metrics differ across groups?
   - Compare averages/medians across segments

### Step 3: Insight Extraction

Structure findings as:

```
## Key Findings

1. **[Finding title]**
   - What: Specific observation with numbers
   - So what: Business impact or implication
   - Action: Recommended next step

2. **[Finding title]**
   - ...
```

**Prioritize insights by:**
- Impact: How much does this matter?
- Surprise: How unexpected is this?
- Actionability: Can the user do something about it?

### Step 4: Visualization Recommendations

For each finding, recommend the best chart type:

| Story You Want to Tell | Best Chart Type | When to Use |
|----------------------|----------------|-------------|
| Change over time | Line chart | Time-series with 5+ data points |
| Compare categories | Bar chart | Up to 10 categories |
| Show composition | Stacked bar / Pie | Parts of a whole (pie for ≤5 slices) |
| Show distribution | Histogram / Box plot | Numeric data distribution |
| Show relationship | Scatter plot | Two numeric variables |
| Compare metrics | Combined chart | Two different scales on same timeline |
| Show progress | Bullet / Gauge | Current vs. target |
| Geographic data | Map / Choropleth | Location-based data |
| Funnel / conversion | Funnel chart | Sequential stage drop-off |

**Specify for each recommendation:**
- Chart type
- X-axis, Y-axis, and data series
- Key formatting notes (color coding, annotations)
- Alternative if the recommended type isn't available

### Output Format

```markdown
## Data Analysis Report

### Dataset Overview
[Profile summary]

### Key Findings
1. [Finding with data, impact, action]
2. [Finding]
3. [Finding]

### Anomalies & Notes
[Any unusual patterns or data quality concerns]

### Recommended Visualizations
1. [Chart type + description]
2. [Chart type + description]

### Data Quality
[Missing values, inconsistencies, recommendations]
```

## Examples

**Input**: A CSV with columns [date, product_category, revenue, units_sold]

**Analysis Output**:
```
Key Findings:
1. Electronics accounts for 42% of revenue but only 18% of units → highest ASP
   Action: Investigate if premium electronics strategy is sustainable
   
2. Revenue dipped 23% in February across all categories → likely seasonal
   Note: Same pattern in previous year, but 2025 dip is steeper
   
3. "Home & Garden" shows 67% growth YoY → emerging category
   Action: Increase inventory allocation for Q3

Recommended Visualizations:
1. Stacked area chart: Revenue by category over time (shows composition + trend)
2. Bar chart: Revenue vs. units by category (highlights ASP differences)
3. Line chart with YoY comparison: Total revenue, 2024 vs 2025
```

## Tips

- Always start with "What question is this data supposed to answer?" — if unclear, state assumptions
- Provide numbers, not just qualitative descriptions ("Revenue grew" → "Revenue grew 15% from $1.2M to $1.38M")
- Note confidence level: with 10 data points, trends are suggestive; with 1000, they're reliable
- Recommend tools: Excel/Google Sheets for quick analysis, Python (pandas + matplotlib) for complex datasets, Tableau/Power BI for interactive dashboards
- If the dataset is too large to paste entirely, analyze a sample and note the limitation

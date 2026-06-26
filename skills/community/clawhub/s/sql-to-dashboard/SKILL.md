---
name: sql-to-dashboard
description: >
  Use when (1) user provides a SQL query and asks to generate a chart, dashboard, or data visualization from the results. 
  (2) user says "show this as a graph", "make a dashboard from this query", "visualize the results", or 
  "plot this data". (3) user has a query result and wants a visual summary rather than raw rows. 
license: MIT
metadata:
  version: "1.0"
  category: data
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# SQL to Dashboard

Use when (1) user provides a SQL query and asks to generate a chart, dashboard, or data visualization from the results. (2) user says "show this as a graph", "make a dashboard from this query", "visualize the results", or "plot this data". (3) user has a query result and wants a visual summary rather than raw rows.

## Core Position

This skill solves the specific problem of: *SQL query results are rows and columns — a visual chart makes trends, comparisons, and anomalies immediately visible.*

This skill IS NOT:
- A SQL writing or debugging tool — it works with queries the user provides
- A database management tool — it does not modify schema or data
- A BI platform guide — it generates chart specs, not platform-specific dashboards

This skill IS activated ONLY when: SQL query or result set + visualization/dashboard intent are both present.

## Modes

### `/sql-to-dashboard`

**Default mode.** Takes a SQL query or result set and outputs a chart specification.

When to use: User provides SQL and wants to see the data as a chart.

### `/sql-to-dashboard/multi`

Combines multiple queries into a single dashboard with multiple panels.

When to use: User has several related metrics they want on one screen.

## Execution Steps

### Step 1 — Analyze the Query Result

1. Receive SQL query (pasted text or query result as CSV/table)
2. If only query provided, analyze it to infer result structure:
   - `SELECT` columns → X-axis candidates (time, category) or Y-axis (numeric values)
   - `GROUP BY` → X-axis or legend groupings
   - `ORDER BY` with `LIMIT` → top-N pattern, suggest horizontal bar chart
   - `COUNT`, `SUM`, `AVG` aggregates → Y-axis values
   - Date/time columns → time series → line chart
   - String/category columns → bar chart or pie chart
3. Identify column types:
   - Numeric (int, float) → value axis
   - Date/datetime → time axis or category axis
   - String/category → label axis, legend, or grouping

### Step 2 — Suggest Chart Type

| Query Pattern | Chart Type | Reason |
|---|---|---|
| Time series (GROUP BY date) | Line chart | Shows trend over time |
| Top-N with COUNT/SUM | Horizontal bar | Easy to compare magnitudes |
| Pie/sum by category | Pie or donut | Shows proportion |
| Two numeric columns | Scatter plot | Shows correlation |
| Multiple aggregates | Grouped bar | Compares categories across groups |
| Cumulative sum | Area chart | Shows accumulation |
| Yes/No count | Donut chart | Binary proportion |

### Step 3 — Generate Dashboard Spec

Output a specification in a format appropriate to context:

**Plotly JSON spec:**
```json
{
  "data": [{
    "x": ["Jan","Feb","Mar"],
    "y": [120, 80, 150],
    "type": "scatter",
    "mode": "lines+markers",
    "name": "Revenue"
  }],
  "layout": {
    "title": "Monthly Revenue",
    "xaxis": {"title": "Month"},
    "yaxis": {"title": "Revenue ($)"}
  }
}
```

**Grafana panel JSON:**
```json
{
  "title": "Monthly Revenue",
  "targets": [{"expr": "sum(revenue)"}],
  "fieldConfig": {"defaults": {"unit": "currencyUSD"}}
}
```

**Mermaid (for simple data):**
```mermaid
xychart-beta
  title "Monthly Revenue"
  x-axis [Jan, Feb, Mar]
  y-axis "Revenue ($)" 0 --> 200
  line [120, 80, 150]
```

### Step 4 — Validate

- Column mapping to axes is correct
- Chart type matches the query's data shape
- Axes are labeled with column names or derived names
- No data values are invented or truncated

## Mandatory Rules

### Do not

- Do not change the query — work with exactly what the user provides
- Do not invent data points not in the result set
- Do not use pie charts for >7 categories
- Do not render a line chart for non-time-series data

### Do

- Preserve exact column names as axis labels
- State which column is mapped to which axis
- Suggest a chart type appropriate for the data shape, even if user suggested a different one
- If the result set is empty, report "No data returned" rather than rendering an empty chart

## Quality Bar

**A good output:**
- Chart type matches query result shape
- Axes are correctly mapped to the query's columns
- Labels and titles are derived from column names (not generic)
- Spec is valid and renderable in the target tool (Plotly, Grafana, etc.)

**A bad output:**
- Line chart for non-sequential categories
- Pie chart with 20 slices
- X-axis shows numeric values as categories (should be scatter or bar)
- Empty chart when query returns no data (should explicitly say "no data")

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| `SELECT date, COUNT(*)` grouped by month | Bar chart | Line chart (time series = trend) |
| `SELECT status, COUNT(*)` 3 statuses | 3D pie chart | Donut chart with legend |
| Empty result set | Empty chart rendered | "Query returned 0 rows — no chart to display" |
| Very large result (10k rows) | Renders all 10k points | Aggregates or samples — states "showing top 100" |

## References

- `references/` — Chart type decision tree, Plotly/Grafana/Redash spec templates, dashboard best practices
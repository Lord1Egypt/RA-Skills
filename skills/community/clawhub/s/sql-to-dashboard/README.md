# Sql To Dashboard

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts SQL query results into chart specifications — line, bar, scatter, pie, and dashboard panels

## What Problem This Solves

SQL query returns rows and columns, but trends and anomalies are invisible without visualization. This skill analyzes the query structure (GROUP BY, aggregates, date columns) and data shape to recommend and generate the right chart type.

**When triggered:** SQL query or result set + chart/dashboard/visualize intent.

## Features

- **Query structure analysis** — infers result shape from SELECT columns, GROUP BY, ORDER BY, and aggregates
- **Automatic chart selection** — time-series → line chart, Top-N with counts → horizontal bar, two numeric cols → scatter
- **Multi-platform output** — Plotly JSON, Grafana panel JSON, or Mermaid for simple data
- **Handles empty results** — explicitly reports "No data returned" instead of rendering empty charts

## Quick Start

```bash
# Via ClawHub
clawhub install sql-to-dashboard

# Or manually
cp -r sql-to-dashboard ~/.openclaw/skills/
```

### Usage

```
/sql-to-dashboard
```

Paste SQL query or result CSV, ask to visualize it.

```
/sql-to-dashboard/multi
```

Combines multiple related queries into one dashboard with multiple panels.

## Modes

| Mode | Description |
|------|-------------|
| `/sql-to-dashboard` | Single query → chart specification |
| `/sql-to-dashboard/multi` | Multiple queries → dashboard with multiple panels |

## Examples

| Query Pattern | Chart Type |
|--------------|------------|
| `SELECT date, COUNT(*)` grouped by month | Line chart (time series = trend) |
| `SELECT status, COUNT(*)` with 3 statuses | Donut chart with legend |
| `SELECT category, SUM(revenue)` | Pie chart for proportion |
| Empty result set | "Query returned 0 rows — no chart to display" |
| 10k row result | Aggregates to top 100, states "showing top 100 of 10,000" |

## Directory Structure

```
sql-to-dashboard/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Chart type decision tree, Plotly/Grafana specs
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).
# Startup Metrics Dashboard Template

## When to Use

- User wants a metrics dashboard, KPI snapshot, or weekly/monthly scorecard
- User wants a markdown output with multiple chart widgets
- Data includes trends, category breakdowns, and channel or segment comparisons

## Required Sections

1. Title and metadata (`Last updated`, `Period`, `Source`)
2. `At a Glance` table with key metrics and change column
3. At least one trend section with a line chart
4. At least one breakdown section with bar or pie chart
5. `Anomalies & Notes` with explicit caveats or actions

## Optional Sections

- Correlation section with scatter chart
- Additional segment analysis table
- Short status callouts under key charts

## Component Interaction Contract

- KPI table sets the narrative for the rest of the dashboard
- Trend charts should align with one KPI shown in `At a Glance`
- Breakdown charts should explain where totals come from
- Notes section should explain unusual spikes/drops shown in charts

## Chart Rules

- Use only supported widget types:
  - `chart-line`
  - `chart-bar`
  - `chart-pie`
  - `chart-scatter`
- CSV values must be plain numbers (no `%`, `K`, `M`, `$` in numeric cells)
- Units belong in labels/headers, not raw numeric values

## Scaffold Template

```markdown
# {Dashboard Title}

**Last updated:** {YYYY-MM-DD HH:MM UTC}
**Period:** {date range}
**Source:** {source}

---

## At a Glance

| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| {KPI 1} | **{value}** | {previous} | {up_or_down} {delta} |
| {KPI 2} | **{value}** | {previous} | {up_or_down} {delta} |
| {KPI 3} | **{value}** | {previous} | {up_or_down} {delta} |

---

## {Primary Trend Section}

{One-sentence context for what changed and why it matters.}

```markdown-ui-widget
chart-line
title: {Trend title}
{x_label},{series_1}[,{series_2}]
{x1},{v11}[,{v12}]
{x2},{v21}[,{v22}]
```

**Status:** {On track | At risk | Off track} - {interpretation}

---

## {Breakdown Section}

```markdown-ui-widget
chart-pie
title: {Breakdown title}
{category},{value}
{cat1},{v1}
{cat2},{v2}
```

| Category | Value | % of Total |
|----------|-------|------------|
| {cat1} | {value} | {percent} |
| {cat2} | {value} | {percent} |

---

## {Channel or Segment Section}

```markdown-ui-widget
chart-bar
title: {Bar chart title}
{category},{series_1}[,{series_2}]
{row1},{v11}[,{v12}]
{row2},{v21}[,{v22}]
```

---

## Anomalies & Notes

- ⚠️ {anomaly, caveat, or quality note}
- ℹ️ {context needed to interpret data}
- 📌 {action or follow-up}

---

*Dashboard generated {timestamp}. Next update: {schedule}.*
```

## Validation Checklist

- No invented sections if data is missing
- At least 3 KPIs in `At a Glance`
- Each chart includes clear title and labeled CSV headers
- Numeric CSV cells are plain numbers only
- Content remains under size limits for publish API

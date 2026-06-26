# Charts Template

Markdown charts use fenced blocks tagged `markdown-ui-widget`.

## Allowed Types

- `chart-line`
- `chart-bar`
- `chart-pie`
- `chart-scatter`

No other widget types are supported.

## Required Format

```markdown
```markdown-ui-widget
chart-line
title: {Chart Title}
{x_label},{series_a}[,{series_b}]
{x1},{a1}[,{b1}]
{x2},{a2}[,{b2}]
```
```

## Data Rules

- CSV value cells must be plain numbers only
- Do not include `%`, `$`, `K`, `M`, or `B` in numeric value cells
- Put units in labels/headers, not in numeric cells
- Use consistent period labels (for example, do not mix daily and monthly)

## Selection Heuristics

- trend over time -> `chart-line`
- category comparison -> `chart-bar`
- composition of a whole -> `chart-pie`
- relationship/correlation -> `chart-scatter`

# Plot spec (JSON)

Goal: a minimal schema that covers 80% of “plot this” requests and produces a clean PNG.

## Top-level

```json
{
  "kind": "line|scatter|hist|heatmap|bar",
  "title": "optional",
  "xlabel": "optional",
  "ylabel": "optional",
  "figsize": [10, 6],
  "dpi": 250,
  "grid": true,

  "data": { ... },
  "series": [ ... ],

  "legend": { "show": true, "loc": "best" }
}
```

## Data sources

### Inline arrays

```json
"data": {"x": [0,1,2], "y": [0,1,4]}
```

### CSV

```json
"data": {"csv": "path/to/data.csv"}
```

CSV expects column names. Series can reference columns.

## Series

### Bar

```json
"kind": "bar",
"data": {"cat": ["A","B"], "count": [10, 12]},
"series": [
  {"x": "cat", "y": "count", "label": "n", "color": "C2", "alpha": 0.9}
],
"legend": {"show": false}
```

Options:
- `bar_mode`: `"grouped"` (default) or `"stacked"`
- `bar_total_width` (default 0.8): total width reserved per category (only for grouped)
- `xtick_rotation` (deg), `xtick_ha` (center/right/left)
- per-series: `width`, `edgecolor`

### Line / scatter

```json
"series": [
  {"x": "x", "y": "y", "label": "y(x)", "style": "-", "color": "C0"}
]
```

- `x`/`y` can be:
  - a key in inline `data` (`"x"`, `"y"`)
  - a column name (if `data.csv` is used)

### Hist

```json
"series": [
  {"x": "samples", "label": "samples", "bins": 50, "alpha": 0.7}
]
```

### Heatmap

For heatmap, `data.z` is a 2D array or a CSV with numeric matrix.

```json
"data": {"z": [[1,2],[3,4]]}
```

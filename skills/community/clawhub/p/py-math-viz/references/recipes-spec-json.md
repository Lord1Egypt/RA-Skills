# Recipes: JSON spec (plot_from_spec.py)

All recipes use:

```bash
/root/.openclaw/workspace/.venv-math/bin/python \
  skills/py-math-viz/scripts/plot_from_spec.py \
  --spec spec.json --out out/plots/out.png
```

## CSV → histogram (distribution of one column)

```json
{
  "kind": "hist",
  "title": "col distribution",
  "xlabel": "col",
  "ylabel": "count",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "col", "bins": 50, "label": "col", "alpha": 0.7}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6]
}
```

## CSV → scatter (two columns)

```json
{
  "kind": "scatter",
  "title": "y vs x",
  "xlabel": "xcol",
  "ylabel": "ycol",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "xcol", "y": "ycol", "label": "data", "alpha": 0.7, "ms": 30}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6]
}
```

## CSV → line (time series)

```json
{
  "kind": "line",
  "title": "value over time",
  "xlabel": "t",
  "ylabel": "value",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "t", "y": "value", "label": "value", "style": "-", "lw": 2.0}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6]
}
```

## CSV → multiple lines (compare series)

```json
{
  "kind": "line",
  "title": "compare series",
  "xlabel": "t",
  "ylabel": "value",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "t", "y": "y1", "label": "y1", "style": "-", "color": "C0"},
    {"x": "t", "y": "y2", "label": "y2", "style": "--", "color": "C1"}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6]
}
```

## CSV → bar (category → value)

```json
{
  "kind": "bar",
  "title": "val by cat",
  "xlabel": "cat",
  "ylabel": "val",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "cat", "y": "val", "label": "val", "alpha": 0.9}
  ],
  "legend": {"show": false},
  "dpi": 250,
  "figsize": [10, 6],
  "xtick_rotation": 30,
  "xtick_ha": "right"
}
```

## CSV → grouped bar (two series per category)

```json
{
  "kind": "bar",
  "bar_mode": "grouped",
  "title": "grouped bars",
  "xlabel": "cat",
  "ylabel": "value",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "cat", "y": "v1", "label": "v1", "color": "C0"},
    {"x": "cat", "y": "v2", "label": "v2", "color": "C1"}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6],
  "xtick_rotation": 30,
  "xtick_ha": "right"
}
```

## CSV → stacked bar (composition per category)

```json
{
  "kind": "bar",
  "bar_mode": "stacked",
  "title": "stacked bars",
  "xlabel": "cat",
  "ylabel": "value",
  "data": {"csv": "data.csv"},
  "series": [
    {"x": "cat", "y": "base", "label": "base", "color": "C2"},
    {"x": "cat", "y": "add", "label": "add", "color": "C3"}
  ],
  "legend": {"show": true, "loc": "best"},
  "dpi": 250,
  "figsize": [10, 6],
  "xtick_rotation": 30,
  "xtick_ha": "right"
}
```

## Heatmap (matrix)

Inline `z`:

```json
{
  "kind": "heatmap",
  "title": "heatmap",
  "xlabel": "x",
  "ylabel": "y",
  "data": {"z": [[1,2,3],[2,3,4],[3,4,5]]},
  "dpi": 250,
  "figsize": [8, 6]
}
```

Numeric CSV matrix (no headers) via `data.csv` (see `references/spec.md`).

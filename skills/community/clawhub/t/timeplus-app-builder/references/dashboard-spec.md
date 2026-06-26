# Dashboard JSON Specification

A dashboard is an array of panel objects. The file lives at `dashboards/main.json` (or any name declared in `manifest.yaml`) and is rendered with `[[ ]]` template delimiters before parsing.

```json
[
  { /* panel 1 */ },
  { /* panel 2 */ }
]
```

---

## Panel Object

Every panel shares the same top-level shape:

```json
{
  "id": "<unique-string>",
  "title": "Panel Title",
  "description": "",
  "position": { "h": 4, "w": 6, "x": 0, "y": 0, "nextX": 6, "nextY": 4 },
  "viz_type": "chart",
  "viz_content": "SELECT ...",
  "viz_config": { "chartType": "line", "config": { ... } }
}
```

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique within the file. Use a UUID or stable slug. |
| `title` | string | Displayed above the panel. Empty string is allowed. |
| `description` | string | Currently unused in the UI; document intent here. |
| `position` | object | Grid placement — see below. |
| `viz_type` | string | `"chart"`, `"control"`, or `"markdown"`. |
| `viz_content` | string | SQL query (chart/markdown panels). Empty for controls. |
| `viz_config` | object | Chart-type-specific config — see sections below. |

---

## Position

The dashboard uses a 12-column grid. Each row is exactly 1 unit tall. Panels can span multiple columns and rows.

```json
"position": {
  "x": 0,      // column start (0–11)
  "y": 0,      // row start (0-based)
  "w": 6,      // width in columns (1–12)
  "h": 4,      // height in rows
  "nextX": 6,  // hint: x after this panel
  "nextY": 4   // hint: y after this panel
}
```

`nextX`/`nextY` are layout hints; set them to `x+w` and `y+h` respectively for the simple non-wrapping case.

**Common widths:**
- `w: 3` — quarter width (small)
- `w: 4` — third width
- `w: 6` — half width
- `w: 12` — full width

**Common heights:**
- `h: 1` — control bar row
- `h: 3` — compact panel
- `h: 4` — standard panel
- `h: 6` — tall panel

---

## Template Variables

Dashboard JSON uses `[[ ]]` delimiters (not `{{ }}`):

| Expression | Value |
|---|---|
| `[[ .DB ]]` | Database name from `db_name` in manifest |
| `[[ .Config.key ]]` | Install-time config value |
| `[[ join "," (fromJson .Config.list_key) ]]` | Sprig function on a `list` config |
| `{{filter_product}}` | Runtime filter variable (left as-is, resolved by frontend) |

SQL in `viz_content` uses both:
- `[[ .DB ]]` for the database name (resolved at install time)
- `{{filter_*}}` for runtime values set by control panels

```json
"viz_content": "SELECT * FROM [[ .DB ]].tickers WHERE product_id = '{{filter_product}}' AND _tp_time > now() - {{filter_time_range}}"
```

---

## viz_type: `"control"`

Controls set filter variables. They do not run a query; `viz_content` is always `""`.

### Dropdown / Selector

```json
{
  "id": "ctrl-product",
  "title": "Product",
  "position": { "h": 1, "w": 3, "x": 0, "y": 0, "nextX": 3, "nextY": 1 },
  "viz_type": "control",
  "viz_content": "",
  "viz_config": {
    "chartType": "selector",
    "label": "Product",
    "labelWidth": "60",
    "target": "filter_product",
    "defaultValue": "BTC-USD",
    "inlineValues": "BTC-USD,ETH-USD,SOL-USD"
  }
}
```

| Field | Notes |
|---|---|
| `chartType` | `"selector"` |
| `label` | Text shown left of the dropdown |
| `labelWidth` | Percent of the panel width allocated to the label (string, `"0"`–`"100"`, e.g. `"50"` for 50%). Despite the name, the unit is percent, not pixels. |
| `target` | The `{{filter_*}}` variable this control writes |
| `defaultValue` | Initially selected value |
| `inlineValues` | Comma-separated list of options |

`inlineValues` can use template functions:
```json
"inlineValues": "[[ join \",\" (fromJson .Config.product_ids) ]]"
"defaultValue": "[[ index (fromJson .Config.product_ids) 0 ]]"
```

### Text Input

```json
{
  "viz_config": {
    "chartType": "text",
    "label": "Source IP",
    "labelWidth": "50",
    "target": "filter_src_ip",
    "defaultValue": "203.0.113.67",
    "inlineValues": ""
  }
}
```

Use `"chartType": "text"` for a free-form text field. Do NOT use `"text_input"` — that value silently falls through to the selector renderer and shows a dropdown. The empty `"inlineValues": ""` is required (match the UI builder's emitted shape exactly).

---

## viz_type: `"markdown"`

Simple Markdown panel. Markdown source lives in `viz_config.mdString`. Can optionally run a SQL query (`viz_content`) and interpolate the **latest row's** column values using `{{column_name}}` in the template.

```json
{
  "id": "md-intro",
  "title": "",
  "position": { "h": 2, "w": 12, "x": 0, "y": 0, "nextX": 12, "nextY": 2 },
  "viz_type": "markdown",
  "viz_content": "SELECT price FROM tickers LIMIT 1",
  "viz_config": {
    "mdString": "## Live Price\n\nCurrent BTC price: **${{price}}**"
  }
}
```

- `viz_config.mdString` — Markdown source with optional `{{column_name}}` placeholders
- `viz_content` — SQL query. **Must not be empty even for static text** — set it to `"SELECT 1"` if the markdown has no interpolation. An empty string leaves the panel stuck loading.
- Interpolation uses only the **last row** of the query result

---

## viz_type: `"chart"` — `chartType: "md"` (Markdown viz)

A more powerful Markdown panel that runs a SQL query and interpolates column values into the template. Use this instead of `viz_type: "markdown"` when you need key-based lookups or streaming update modes.

**Static markdown still needs a query.** Both `viz_type: "markdown"` and `chartType: "md"` panels treat `viz_content` as required — an empty string leaves the panel stuck on a loading state. For pure-text headers/instructions with no interpolation, set `"viz_content": "SELECT 1"` as a no-op stub.

```json
{
  "id": "md-status",
  "title": "Current Status",
  "position": { "h": 3, "w": 6, "x": 0, "y": 0, "nextX": 6, "nextY": 3 },
  "viz_type": "chart",
  "viz_content": "SELECT product_id, price, volume FROM [[ .DB ]].tickers WHERE _tp_time > now() - 1m",
  "viz_config": {
    "chartType": "md",
    "config": {
      "content": "## {{product_id}}\n\nPrice: **${{price}}**\nVolume: {{volume}}",
      "updateMode": "all",
      "updateKey": ""
    }
  }
}
```

### Interpolation modes

**Default (`updateMode: "all"` or `"time"`)** — inserts values from the **last row** of the query result:
```
Price: **${{price}}**
```

**Key mode (`updateMode: "key"`)** — look up a specific row by key and field using `{{@keyValue::fieldName}}`:
```
BTC Price: **${{@BTC-USD::price}}**
ETH Price: **${{@ETH-USD::price}}**
```
This pulls the `price` value from the row where `updateKey` column equals `BTC-USD` (or `ETH-USD`). Useful for showing multiple values from a mutable stream side by side.

```json
"viz_content": "SELECT product_id, price FROM table([[ .DB ]].latest_prices)",
"viz_config": {
  "chartType": "md",
  "config": {
    "content": "| Symbol | Price |\n|---|---|\n| BTC | ${{@BTC-USD::price}} |\n| ETH | ${{@ETH-USD::price}} |",
    "updateMode": "key",
    "updateKey": "product_id"
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `content` | string | Markdown template with `{{col}}` or `{{@key::col}}` placeholders |
| `updateMode` | string | `"all"` replace all, `"key"` look up by key, `"time"` append |
| `updateKey` | string | Column name for key-mode lookups |

---

## viz_type: `"chart"`

All chart panels share:
```json
"viz_type": "chart",
"viz_content": "<Timeplus streaming SQL>",
"viz_config": {
  "chartType": "<type>",
  "config": { ... }
}
```

Chart types: `line`, `area`, `bar`, `column`, `singleValue`, `table`, `ohlc`, `geo`, `md` (Markdown viz — see dedicated section above), `grammar` (3.2+ — generic Vistral grammar; use when no fixed type fits).

---

### `line` and `area`

Time-series charts. Requires a datetime column for X, numeric column for Y.

> **Multi-series queries must set `color`.** If your SELECT returns multiple series (e.g. `SELECT time, stock_id, close FROM ...` — one line per `stock_id`), set `"color": "stock_id"` (the series/category column). Leaving it as `""` silently collapses all series into a single overlapping line — the chart renders but is unreadable.

```json
"viz_config": {
  "chartType": "line",
  "config": {
    "xAxis": "time",
    "yAxis": "price",
    "color": "stock_id",  // ← series column; required when the query returns >1 series
    "xRange": "Infinity",
    "xFormat": "",
    "xTitle": "",
    "yTitle": "",
    "yRange": { "min": null, "max": null },
    "lineStyle": "curve",
    "dataLabel": false,
    "showAll": false,
    "legend": false,
    "points": false,
    "gridlines": true,
    "unit": { "position": "left", "value": "" },
    "fractionDigits": 2,
    "colors": ["#ED64A6", "#F0BE3E", "#DA4B36", "#9A1563", "#FF4A71",
                "#D12D50", "#8934D9", "#D53F8C", "#F7775A", "#8934D9"],
    "yTickLabel": { "maxChar": 25 }
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `xAxis` | string | Column name — must be datetime type |
| `yAxis` | string | Column name — must be numeric type |
| `color` | string | **Required for multi-series.** Column name that distinguishes series (e.g. `"stock_id"`, `"region"`). Empty = single-series only. |
| `xRange` | string | Minutes to show: `"1"`, `"5"`, `"60"`, `"Infinity"` (all) |
| `xFormat` | string | Moment.js format. Use `""` (auto) for any panel whose query can span more than one day — including all `seek_to='earliest'` panels. Reserve `"LT"` (time-of-day only) for short-window panels filtered with `WHERE time > now() - Xm`. |
| `lineStyle` | string | `"curve"` or `"straight"` |
| `dataLabel` | bool | Show data point labels |
| `points` | bool | Show dots at each data point |
| `legend` | bool | Show legend (only when `color` is set) |
| `gridlines` | bool | Show horizontal gridlines |
| `yRange` | object | `{ "min": null, "max": null }` — null = auto |

Use `area` for the same config to get a filled area chart.

---

### `bar` and `column`

Categorical charts. `bar` = horizontal bars, `column` = vertical bars.

```json
"viz_config": {
  "chartType": "bar",
  "config": {
    "xAxis": "repo",
    "yAxis": "count",
    "color": "repo",
    "groupType": "stack",
    "updateMode": "all",
    "updateKey": "",
    "xFormat": "HH:mm",
    "xTitle": "",
    "yTitle": "",
    "dataLabel": true,
    "legend": false,
    "gridlines": true,
    "unit": { "position": "left", "value": "" },
    "fractionDigits": 0,
    "colors": ["#ED64A6", "#F0BE3E", "#DA4B36", "#9A1563", "#FF4A71",
                "#D12D50", "#8934D9", "#D53F8C", "#F7775A", "#8934D9"],
    "yTickLabel": { "maxChar": 25 },
    "xTickLabel": { "maxChar": 20 }
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `xAxis` | string | Category column (string or datetime) |
| `yAxis` | string | Value column (numeric) |
| `color` | string | Column for color grouping |
| `groupType` | string | `"stack"` or `"dodge"` (side by side) |
| `updateMode` | string | `"all"` replace all, `"key"` upsert by key, `"time"` append by time |
| `updateKey` | string | Column for key-based updates (e.g. `"emit_version()"`) |
| `xFormat` | string | Format string for datetime x-axis labels |
| `xTickLabel.maxChar` | number | Max characters on x-axis labels |

**Update modes:**
- `"all"` — replace the entire dataset on each query result (historical queries)
- `"time"` — append data; use with a time column as `updateKey` for streaming leaderboards
- `"key"` — upsert rows by `updateKey` value (for mutable streams)

---

### `singleValue`

Displays a single large number with optional sparkline and delta indicator.

```json
"viz_config": {
  "chartType": "singleValue",
  "config": {
    "value": "count()",
    "color": "blue",
    "sparkline": true,
    "sparklineColor": "blue",
    "delta": true,
    "increaseColor": "green",
    "decreaseColor": "red",
    "fontSize": 64,
    "fractionDigits": 0,
    "unit": { "position": "right", "value": "" }
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `value` | string | Column name (must be numeric) — often matches the SELECT alias |
| `color` | string | Color of the main value (CSS color name or hex) |
| `sparkline` | bool | Show a mini trend chart |
| `sparklineColor` | string | Sparkline color |
| `delta` | bool | Show change indicator vs previous value |
| `increaseColor` | string | Color when delta is positive |
| `decreaseColor` | string | Color when delta is negative |
| `fontSize` | number | Font size in px |
| `fractionDigits` | number | Decimal places |
| `unit.value` | string | Unit label (e.g. `"ms"`, `"%"`) |
| `unit.position` | string | `"left"` or `"right"` |

---

### `table`

Tabular view with per-column styling, trend indicators, and conditional formatting.

```json
"viz_config": {
  "chartType": "table",
  "config": {
    "rowCount": 5,
    "updateMode": "all",
    "updateKey": "",
    "tableWrap": false,
    "tableStyles": {
      "product_id": {
        "name": "",
        "show": true,
        "width": 139,
        "trend": false,
        "miniChartType": "",
        "conditions": [],
        "highlightRow": false,
        "increaseColor": "green",
        "decreaseColor": "red"
      },
      "price": {
        "name": "",
        "show": true,
        "width": 100,
        "trend": true,
        "miniChartType": "",
        "conditions": [],
        "highlightRow": false,
        "increaseColor": "green",
        "decreaseColor": "red"
      }
    }
  }
}
```

`tableStyles` keys are column names from the query result.

| Key | Type | Notes |
|---|---|---|
| `rowCount` | number | Max rows to display: 5, 10, 20, 30, 50, 100 |
| `updateMode` | string | Same as bar/column: `"all"`, `"key"`, `"time"` |
| `updateKey` | string | Key column for `"key"` update mode |
| `tableWrap` | bool | Wrap long cell text |
| `tableStyles.<col>.show` | bool | Show/hide column |
| `tableStyles.<col>.width` | number | Column width in px |
| `tableStyles.<col>.trend` | bool | Color cell green/red based on value change |
| `tableStyles.<col>.name` | string | Override display name (empty = use column name) |

**Minimal table config** (omit `tableStyles` entirely and it auto-generates from query headers):
```json
"viz_config": { "chartType": "table" }
```

---

### `ohlc`

Candlestick chart for financial data. Query **must** return columns named exactly: `time`, `open`, `high`, `low`, `close`.

```json
"viz_config": {
  "chartType": "ohlc",
  "config": {
    "xRange": "Infinity",
    "yRange": { "min": null, "max": null }
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `xRange` | string | Minutes to display: `"1"`, `"60"`, `"Infinity"` |
| `yRange.min` | number\|null | Y-axis minimum (null = auto) |
| `yRange.max` | number\|null | Y-axis maximum (null = auto) |

**Required SQL shape:**
```sql
SELECT
  window_start AS time,
  earliest(price) AS open,
  latest(price)   AS close,
  max(price)      AS high,
  min(price)      AS low
FROM tumble(stream, interval)
GROUP BY window_start
```

---

### `geo`

Map scatter chart. Requires two numeric columns for longitude and latitude.

```json
"viz_config": {
  "chartType": "geo",
  "config": {
    "longitude": "lon",
    "latitude": "lat",
    "color": "category",
    "updateMode": "all",
    "updateKey": "",
    "visibleColumns": ["city", "category"],
    "colors": ["#ED64A6", "#F0BE3E", "#DA4B36"],
    "opacity": 0.8,
    "zoom": 4,
    "center": [20, 0],
    "size": {
      "key": "",
      "value": 4,
      "range": [2, 20]
    }
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `longitude` | string | Column name for longitude (numeric) |
| `latitude` | string | Column name for latitude (numeric) |
| `color` | string | Column for dot coloring |
| `visibleColumns` | string[] | Columns shown in the tooltip popup |
| `zoom` | number | Initial map zoom level (typical range 1–18) |
| `center` | [lat, lon] | Initial map center — **latitude first, then longitude** (Vistral convention; do NOT swap). The map opens here on first load and stays put — there's no auto-fit-to-data option exposed. Pick values inside your data's bounding box. |
| `opacity` | number | Dot opacity 0–1 |
| `size.key` | string | Column to scale dot size by (empty = fixed size) |
| `size.value` | number | Fixed dot size (when `size.key` is empty) |
| `size.range` | [min, max] | Min/max dot size when `size.key` is set |

**Picking `center` and `zoom`.** The geo panel has no `autoFit` option in the dashboard JSON — the initial view is fixed. Compute it from your data:

```sql
-- Find the midpoint of your data's bounding box
SELECT
  round((min(latitude)  + max(latitude))  / 2, 4) AS center_lat,
  round((min(longitude) + max(longitude)) / 2, 4) AS center_lon
FROM table(<your_mutable_stream>);
```

Then set `"center": [<center_lat>, <center_lon>]` (lat first!) and pick `zoom` so the bounding box fits comfortably. Rough rule: each step of zoom halves the visible extent. Zoom 11 ≈ 50 km wide, 12 ≈ 25 km, 13 ≈ 12 km, 14 ≈ 6 km.

**Common bug:** swapping `[lat, lon]` ↔ `[lon, lat]` lands you on the opposite side of the world. If your map opens far from your data, that's the cause.

---

### `grammar` (Timeplus 3.2+)

A generic, spec-driven chart type backed by the [Vistral](https://github.com/timeplus-io/vistral) grammar engine. Use when no fixed `chartType` covers what you need — scatter (point mark with numeric x), layered marks, categorical band-axis bars with band scale + key-based update, stacked area via the `stackY` transform, log-scale lines, etc.

**For the underlying grammar — full `VistralSpec` shape, every mark type, transform, scale, encode channel, and streaming option — see the Vistral skill:**
[`vistral/agentskill/SKILL.md`](https://github.com/timeplus-io/vistral/blob/main/agentskill/SKILL.md)

Everything you write in `advancedSpec` (and what the form-builder fields map to) is documented there. This section below covers only the dashboard-side `viz_config.config` wrapper that exposes the grammar through a form.

```json
"viz_config": {
  "chartType": "grammar",
  "config": {
    "renderInterval": 500,
    "updateMode": "all",
    "updateKey": "",

    "markType": "line",
    "xField": "_tp_time",
    "yField": ["value"],
    "colorField": "",
    "sizeField": "",

    "xScaleType": "time",
    "yScaleType": "linear",

    "temporalMode": "axis",
    "temporalRange": 1,

    "streamMaxItems": 600,
    "streamMode": "append",
    "throttleMs": 100,

    "xAxisTitle": "",
    "yAxisTitle": "Value",
    "legendPosition": "top",

    "advancedSpec": ""
  }
}
```

| Key | Type | Notes |
|---|---|---|
| `markType` | `'line' \| 'area' \| 'interval' \| 'point' \| 'rect'` | Mark to draw. `interval` is a bar; `point` is a scatter mark. |
| `xField` | string | Column for x encoding. |
| `yField` | string \| string[] | Column(s) for y. Single-element arrays are unwrapped to a scalar; arrays with >1 entry are passed through for multi-series marks. |
| `colorField` | string | Optional column for color encoding (groups marks by category). |
| `sizeField` | string | Optional column for size encoding (point/interval). |
| `xScaleType` | `'time' \| 'linear' \| 'band' \| 'ordinal' \| 'log'` \| `''` | x-axis scale. Use `band` for categorical x on `interval` marks. Empty = auto. |
| `yScaleType` | `'linear' \| 'log'` \| `''` | y-axis scale. Empty = auto. |
| `temporalMode` | `'' \| 'axis' \| 'frame' \| 'key'` | Streaming behavior. `axis` = sliding window on x-axis; `frame` = replace on each tick; `key` = update by key column. Empty = none. |
| `temporalRange` | number\|null | **Minutes** (not ms) for the sliding window when `temporalMode === 'axis'`. |
| `streamMaxItems` | number\|null | Cap on rows kept in the chart buffer. |
| `streamMode` | `'append' \| 'replace'` \| `''` | Append new rows or replace the buffer on each tick. |
| `throttleMs` | number\|null | Throttle window for rerenders, in milliseconds. |
| `xAxisTitle` / `yAxisTitle` | string | Axis titles (empty = no title). |
| `legendPosition` | `'top' \| 'bottom' \| 'left' \| 'right' \| 'hidden'` | Legend placement. Use `'hidden'` (not `'none'`) to suppress. |
| `advancedSpec` | string (JSON) | Optional raw `VistralSpec` deep-merged on top of the form-derived spec. **Arrays are replaced atomically** by `mergeDeepRight`, so providing `marks` here overrides the entire mark array including the form-built encode — declare every mark you want explicitly when you use it. |

**Common patterns**

Scatter with color + size encoding:
```json
{
  "markType": "point",
  "xField": "sepal_length",
  "yField": ["sepal_width"],
  "colorField": "species",
  "sizeField": "petal_length",
  "xScaleType": "linear",
  "yScaleType": "linear",
  "temporalMode": ""
}
```

Streaming line with a 1-minute sliding window:
```json
{
  "markType": "line",
  "xField": "_tp_time",
  "yField": ["value"],
  "xScaleType": "time",
  "temporalMode": "axis",
  "temporalRange": 1,
  "streamMaxItems": 600,
  "streamMode": "append",
  "throttleMs": 100
}
```

Categorical bar by group, key-based update (one row per category):
```json
{
  "markType": "interval",
  "xField": "category",
  "yField": ["value"],
  "colorField": "category",
  "xScaleType": "band",
  "updateMode": "key",
  "updateKey": "category",
  "streamMode": "replace"
}
```

Layered line + points (advancedSpec, atomic mark replacement):
```json
{
  "markType": "line",
  "xField": "_tp_time",
  "yField": ["value"],
  "advancedSpec": "{\"marks\":[{\"type\":\"line\",\"encode\":{\"x\":\"_tp_time\",\"y\":\"value\"},\"style\":{\"strokeWidth\":2}},{\"type\":\"point\",\"encode\":{\"x\":\"_tp_time\",\"y\":\"value\"},\"style\":{\"fillOpacity\":0.6}}]}"
}
```

Stacked area (transform via advancedSpec):
```json
{
  "markType": "area",
  "xField": "_tp_time",
  "yField": ["value"],
  "colorField": "series",
  "advancedSpec": "{\"transforms\":[{\"type\":\"stackY\"}]}"
}
```

**Gotchas**
- `temporalRange` is **minutes**, not milliseconds. Setting it to `60000` gives you a 60000-minute (~41-day) window and your sliding chart will appear empty until ~41 days pass.
- `legendPosition: 'hidden'` not `'none'`. The Selector engine reserves `'none'` for its placeholder item and silently coerces it to `''`.
- The form's y-field picker is multi-select, but Vistral's grammar wants a scalar `y` for single-series marks. The translator handles this by unwrapping length-1 arrays — so `yField: ["value"]` and `yField: "value"` both render correctly.
- `xField` and `colorField` UI pickers filter to non-numeric columns by default. To use a numeric column for x (scatter) or color (sequential), you have to author the JSON directly or set the value via `advancedSpec` — the form won't offer numeric columns there.
- When `advancedSpec` supplies `marks`, the array fully replaces the form-built marks. Declare every layer you want; don't expect the form's mark to be preserved underneath.
- For a known-bad config (missing mark type or x/y encode), the panel renders an inline error banner instead of throwing — useful while authoring, but check the panel for that banner if your chart appears blank.

---

## Default Color Palette

Use this standard 10-color palette for consistency:

```json
"colors": [
  "#ED64A6", "#F0BE3E", "#DA4B36", "#9A1563", "#FF4A71",
  "#D12D50", "#8934D9", "#D53F8C", "#F7775A", "#8934D9"
]
```

---

## updateMode Reference

| Mode | When to use | updateKey value |
|---|---|---|
| `"all"` | Historical (batch) queries; the full result replaces the chart | `""` |
| `"time"` | Streaming aggregations with `emit_version()` — append new result sets | `"emit_version()"` or a timestamp column |
| `"key"` | Mutable streams — upsert rows by primary key column | primary key column name |

**Streaming leaderboard pattern** (append mode):
```sql
SELECT repo, count(*) AS cnt, emit_version()
FROM stream WHERE _tp_time > now() - 10m
GROUP BY repo ORDER BY cnt DESC LIMIT 5 BY emit_version()
```
```json
"updateMode": "time", "updateKey": "emit_version()"
```

---

## Full Example: Market Data Dashboard Panel

```json
[
  {
    "id": "ctrl-product",
    "title": "",
    "position": { "h": 1, "w": 3, "x": 0, "y": 0, "nextX": 3, "nextY": 1 },
    "viz_type": "control",
    "viz_content": "",
    "viz_config": {
      "chartType": "selector",
      "label": "Product",
      "labelWidth": "60",
      "target": "filter_product",
      "defaultValue": "[[ index (fromJson .Config.product_ids) 0 ]]",
      "inlineValues": "[[ join \",\" (fromJson .Config.product_ids) ]]"
    }
  },
  {
    "id": "chart-price",
    "title": "Live Price",
    "position": { "h": 4, "w": 12, "x": 0, "y": 1, "nextX": 12, "nextY": 5 },
    "viz_type": "chart",
    "viz_content": "SELECT _tp_time AS time, price FROM [[ .DB ]].tickers WHERE product_id = '{{filter_product}}' AND _tp_time > now() - 5m",
    "viz_config": {
      "chartType": "line",
      "config": {
        "xAxis": "time",
        "yAxis": "price",
        "color": "",
        "xRange": "5",
        "xFormat": "HH:mm:ss",
        "lineStyle": "curve",
        "dataLabel": false,
        "points": false,
        "legend": false,
        "gridlines": true,
        "unit": { "position": "left", "value": "$" },
        "fractionDigits": 2,
        "yRange": { "min": null, "max": null },
        "yTickLabel": { "maxChar": 25 },
        "xTitle": "",
        "yTitle": "",
        "colors": ["#ED64A6","#F0BE3E","#DA4B36","#9A1563","#FF4A71",
                   "#D12D50","#8934D9","#D53F8C","#F7775A","#8934D9"]
      }
    }
  }
]
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using `{{ .DB }}` in dashboard JSON | Use `[[ .DB ]]` — dashboard uses `[[ ]]` delimiters |
| Flat chart config like `{ "chartType": "line", "x": "...", "y": [...] }` | Wrap fields under `config` and use `xAxis` / `yAxis` (not `x` / `y`). The renderer throws `VizConfigError: Missing or invalid config field: xAxis` for flat shapes. |
| OHLC query doesn't have column named `time` | Alias: `window_start AS time` |
| Selector control writes wrong filter name | `target` must match `{{filter_*}}` in SQL exactly |
| Table shows no data | Check `updateMode` — use `"key"` for mutable streams |
| Streaming leaderboard doesn't update | Set `updateMode: "time"`, `updateKey: "emit_version()"` |
| `inlineValues` not reflecting config | Use `[[ join "," (fromJson .Config.list_key) ]]` |

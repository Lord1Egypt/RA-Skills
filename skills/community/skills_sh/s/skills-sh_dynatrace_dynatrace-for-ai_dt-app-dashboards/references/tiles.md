# Dashboard Tiles

Tiles are stored in `content.tiles` as an object map with string keys.

## Tile Types

### Markdown Tiles

```json
{ "type": "markdown", "content": "# Section Header" }
```

### Data Tiles

```json
{
  "type": "data", "title": "Tile Name",
  "query": "timeseries avg(metric), by:{dimension}",
  "visualization": "lineChart",
  "visualizationSettings": {},
  "querySettings": {}
}
```

Optional properties: `description`, `customLinkSettings`, `davis`,
`davisCopilot`, `timeframe`, `segments`.

### Code Tiles

```json
{ "type": "code", "title": "Custom", "input": "// JS code",
  "visualization": "lineChart", "visualizationSettings": {} }
```

### SLO Tiles

```json
{ "type": "slo", "title": "SLO Name", "input": "slo-id",
  "visualizationSettings": {} }
```

## Visualization Types and Required Field Types

Each visualization requires specific field types in the query result. If the
query produces wrong types, the tile renders blank or errors. The field types
below correspond to DQL output types: `timestamp`, `timeframe`, `long`,
`double`, `duration`, `string`, `numericArray` (array of long/double — the
output of `timeseries`/`makeTimeseries` value columns).

**Legend:** R = required, O = optional, C = conditional.

### Time-Series Charts

**`lineChart`**, **`areaChart`**, **`barChart`**: Display metric data over time.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Time | timestamp, timeframe | 1 | R |
| Interval | duration | 1 | C — required when Values is numericArray |
| Values | long, double, duration, numericArray | 1+ | R |
| Names | any | 1+ | O |

When the query uses `timeseries` or `makeTimeseries`, values are numericArrays
and the `interval` field (duration) must be present. If you pipe through
`| fields` after `timeseries`, always include `interval` and `timeframe`.

**`bandChart`**: Same as above plus two additional required numericArray slots
for band min and band max values.

### Categorical Charts

**`categoricalBarChart`**, **`pieChart`**, **`donutChart`**: Show values
grouped by categories.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Values | long, double, duration | 1+ | R |
| Categories | any | 1+ | R |

Typical query pattern: `summarize <agg>, by:{category}`.

**`barChart` vs `categoricalBarChart`:** `barChart` is a **time-series** chart
requiring a timestamp/timeframe axis. For "values per category" (e.g. request
count per service), use `categoricalBarChart`. If you use `barChart` with
`summarize ... by:{category}` (no time axis), the tile will fail validation.

**Timeseries data in categorical charts:** If you need to show summarized
metrics (not over time), first convert the timeseries arrays to scalars using
array functions (`arrayAvg`, `arraySum`, etc.), then use
`categoricalBarChart`.

### Single Value / Gauge

**`singleValue`**: Displays a single metric.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Single value | any | 1 | R |
| Sparkline | numericArray | 1 | O |

**`meterBar`**, **`gauge`**: Display a numeric value on a scale.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Meter/Gauge value | long, double, duration | 1 | R |

Configure `minValue`/`maxValue` in `visualizationSettings`.

### Tabular

**`table`**, **`raw`**, **`recordList`**: Any data shape. No field-type
requirements.

### Distribution / Status

**`histogram`**: Shows distribution of values.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Range | range (object with start/end) | 1 | R |
| Values | long, double, duration | 1 | R |
| Names | any | 1+ | O |

**`honeycomb`**: Grid of colored cells.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Values | long, double, duration | 1 | R |
| Names | any | 1+ | O |

### Geographic Maps

**`choroplethMap`**: Colored regions on a map.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Country/subdivision code | string (ISO 3166) | 1 | R |
| Color value | long, double, duration, string | 1 | R |

**`dotMap`**, **`connectionMap`**: Points on a map.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Latitude | long, double, duration | 1 | R |
| Longitude | long, double, duration | 1 | R |
| Color value | long, double, duration, string | 1 | O |

**`bubbleMap`**: Sized circles on a map.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Latitude | long, double, duration | 1 | R |
| Longitude | long, double, duration | 1 | R |
| Radius value | long, double, duration | 1 | R |
| Color value | long, double, duration, string | 1 | O |

### Matrix / Correlation

**`heatmap`**: 2D grid with colored cells.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| X-axis | timeframe, range, string | 1 | R |
| Y-axis | timeframe, range, string | 1 | R |
| Values | long, double, duration, string | 1 | R |

`bin(timestamp, ...)` returns `timestamp` — heatmap axes do **not** accept
`timestamp`. Wrap with `toString()`: `by:{x = toString(bin(timestamp, 1h))}`.

**`scatterplot`**: X/Y point chart.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| X-axis | timeframe, long, double, duration, string | 1 | R |
| Y-axis | long, double, duration, string | 1 | R |
| Names | any | 1+ | O |

## Visualization Settings

See [assets/visualization-settings.reference.jsonc](../assets/visualization-settings.reference.jsonc)
for the complete per-visualization settings reference.

Common settings across visualizations: `legend`, `tooltip`, `zoom`,
`unitsOverrides`, `coloring`, `thresholds`, `colorModeType`.

# Notebook Sections

Sections are stored in `content.sections` as an ordered array. Each section has
its own `id` field. Section types: `markdown` and `dql`.

## Section Types

### Markdown Sections

```json
{ "id": "1", "type": "markdown", "markdown": "# Section Header" }
```

### DQL Sections

```json
{
  "id": "2", "type": "dql", "title": "Section Name",
  "showInput": true,
  "state": {
    "input": { "value": "timeseries avg(metric), by:{dimension}" },
    "visualization": "lineChart",
    "visualizationSettings": { "autoSelectVisualization": true, "chartSettings": {} },
    "querySettings": {
      "maxResultRecords": 1000, "defaultScanLimitGbytes": 500,
      "maxResultMegaBytes": 1, "defaultSamplingRatio": 10, "enableSampling": false
    }
  }
}
```

Optional properties: `showTitle`, `height`, `drilldownPath`, `filterSegments`, `davis`.

**Section properties:**
- `autoSelectVisualization` (boolean, in `visualizationSettings`) — when
  `true`, Dynatrace automatically picks the best visualization. **Prefer
  `true` unless the user requested a specific visualization.** When `false`,
  `state.visualization` must be set explicitly.
- `showTitle` (boolean) — show/hide section title
- `showInput` (boolean, default `true`) — show/hide query editor. Keep `true`
  unless told otherwise
- `height` (number, px) — section height (default ~400)

## Visualization Types and Required Field Types

Each visualization requires specific field types in the query result. If the
query produces wrong types, the section renders blank or errors. Field types
correspond to DQL output types: `timestamp`, `timeframe`, `long`, `double`,
`duration`, `string`, `numericArray` (array of long/double — output of
`timeseries`/`makeTimeseries` value columns).

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
`summarize ... by:{category}` (no time axis), the section will fail validation.

**Timeseries data in categorical charts:** If you need to show summarized
metrics (not over time), first convert the timeseries arrays to scalars using
array functions (`arrayAvg`, `arraySum`, etc.), then use
`categoricalBarChart`.

### Single Value

**`singleValue`**: Displays a single metric.

| Slot | Accepted types | Count | Req |
|------|---------------|-------|-----|
| Single value | any | 1 | R |
| Sparkline | numericArray | 1 | O |

### Tabular

**`table`**, **`raw`**, **`recordView`**: Any data shape. No field-type
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

## Visualization Settings

See [assets/visualization-settings.reference.jsonc](../assets/visualization-settings.reference.jsonc)
for the complete per-visualization settings reference.

Common settings across visualizations: `legend`, `tooltip`, `zoom`,
`unitsOverrides`, `coloring`, `thresholds`, `colorModeType`.

**Visualization tip:** when you don't have a strong reason to pick a specific
visualization, set `visualizationSettings.autoSelectVisualization: true` and
omit `state.visualization` — Dynatrace picks a sensible default for the query
result.

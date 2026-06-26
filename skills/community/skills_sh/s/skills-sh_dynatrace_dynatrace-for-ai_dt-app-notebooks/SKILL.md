---
name: dt-app-notebooks
description: Work with Dynatrace notebooks - create, modify, query, and analyze notebook JSON including sections, DQL queries, and visualizations.
license: Apache-2.0
---

# Dynatrace Notebook Skill

## Overview

Dynatrace notebooks are JSON documents stored in the Document Store containing an ordered array of **sections** — markdown blocks for narrative and `dql` blocks for DQL queries with visualizations. Sections render top-to-bottom in array order.

**When to use:** Creating, modifying, querying, or analyzing notebooks.

## Notebook JSON Structure

```json
{
  "name": "My Notebook",
  "type": "notebook",
  "content": {
    "version": "7",
    "defaultTimeframe": { "from": "now()-2h", "to": "now()" },
    "sections": [
      { "id": "1", "type": "markdown", "markdown": "# Title" },
      {
        "id": "2", "type": "dql", "title": "Query Section", "showInput": true,
        "state": {
          "input": { "value": "fetch logs | summarize count()" },
          "visualization": "table",
          "visualizationSettings": { "autoSelectVisualization": true, "chartSettings": {} },
          "querySettings": {
            "maxResultRecords": 1000, "defaultScanLimitGbytes": 500,
            "maxResultMegaBytes": 1, "defaultSamplingRatio": 10, "enableSampling": false
          }
        }
      }
    ]
  }
}
```

- Sections render in array order.
- Section types: `markdown`, `dql`. (`function` exists but is rare.)
- Use string-int IDs (`"1"`, `"2"`, …); UUIDs are also accepted.
- `content.defaultTimeframe` sets the default timeframe; each section can override via `section.state.input.timeframe`. Hardcoded time filters in DQL are allowed.

**Optional content properties:** `defaultSegments`.

## Create/Update Workflow (Mandatory Order)

Carefully follow the workflow described in [references/create-update.md](references/create-update.md).

**Key rules:**
- Load domain skills BEFORE generating queries — do not invent DQL.
- Validate ALL section queries before adding to the notebook.
- Set `name` before deploying.
- **Prefer `autoSelectVisualization: true`** in `visualizationSettings` unless the user requested a specific visualization type — when `false`, `state.visualization` must be set explicitly.
- **Updating — ALWAYS download first:** `dtctl get notebook <id> -o json --plain > notebook.json`, modify, then deploy the downloaded file. Never reconstruct JSON from scratch or inject an `id` manually — both silently overwrite UI edits the user made since last deployment.
- **Deploy with `dtctl apply`** — validation runs automatically, and the local file is deleted on success.

## Visualization Types

Notebooks support a subset of Dynatrace visualizations:

- **Time-series** (require `timeseries`/`makeTimeseries`): `lineChart`, `areaChart`, `barChart`, `bandChart`
- **Categorical** (`summarize ... by:{field}`): `categoricalBarChart`, `pieChart`, `donutChart`
- **Single value / gauge / meter**: `singleValue`, `meterBar`, `gauge`
- **Tabular** (any data shape): `table`, `raw`, `recordView`
- **Distribution/status**: `histogram`, `honeycomb`
- **Geographic maps**: `choropleth`, `dotMap`, `connectionMap`, `bubbleMap`
- **Matrix/correlation**: `heatmap`, `scatterplot`

Required field types per visualization: [references/sections.md](references/sections.md).

## References

| File | When to Load |
|------|-------------|
| [create-update.md](references/create-update.md) | Creating/updating notebooks |
| [sections.md](references/sections.md) | Section types, visualization field requirements, settings |
| [analyzing.md](references/analyzing.md) | Reading notebooks, extracting queries, purpose identification |

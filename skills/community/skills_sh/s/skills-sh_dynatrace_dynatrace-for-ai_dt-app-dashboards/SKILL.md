---
name: dt-app-dashboards
description: Work with Dynatrace dashboards - create, modify, query, and analyze dashboard JSON including tiles, layouts, DQL queries, variables, and visualizations.
license: Apache-2.0
---

# Dynatrace Dashboard Skill

## Overview

Dynatrace dashboards are JSON documents stored in the Document Store containing
tiles (content/visualizations), layouts (grid positioning), and variables
(dynamic query parameters).

**When to use:** Creating, modifying, querying, or analyzing dashboards.

## Dashboard JSON Structure

```json
{
  "name": "My Dashboard",
  "type": "dashboard",
  "content": {
    "version": 21,
    "variables": [],
    "tiles": { "<id>": { "type": "data|markdown", ... } },
    "layouts": { "<id>": { "x": 0, "y": 0, "w": 24, "h": 8 } }
  }
}
```

- Tile IDs in `tiles` must match IDs in `layouts`
- Grid is 24 units wide. Common widths: 24 (full), 12 (half), 6 (quarter)
- Two tile types: `markdown` (text content) and `data` (DQL query + visualization)

**Optional content properties:** `settings`, `refreshRate`, `annotations`

## Create/Update Workflow (Mandatory Order)

Carefully follow the workflow described in [references/create-update.md](references/create-update.md).

**Key rules:**
- Load domain skills BEFORE generating queries — do not invent DQL
- Validate ALL queries before adding to dashboard
- No time-range filters in queries unless explicitly requested by user
- Set `name` before deploying
- **Updating — ALWAYS download first:** `dtctl get dashboard <id> -o json --plain > dashboard.json`, modify, then deploy the downloaded file. Never reconstruct JSON from scratch or inject an `id` manually — both silently overwrite any UI edits the user made since last deployment.
- **Deploy with `dtctl apply`** — validation runs automatically, and the local file is deleted on success.

## Visualization Types

- **Time-series** (require `timeseries`/`makeTimeseries`): `lineChart`, `areaChart`, `barChart`, `bandChart`
- **Categorical** (`summarize ... by:{field}`): `categoricalBarChart`, `pieChart`, `donutChart`
- **Single value/gauge** (single numeric record): `singleValue`, `meterBar`, `gauge`
- **Tabular** (any data shape): `table`, `raw`, `recordList`
- **Distribution/status**: `histogram`, `honeycomb`
- **Maps**: `choroplethMap`, `dotMap`, `connectionMap`, `bubbleMap`
- **Matrix**: `heatmap`, `scatterplot`

Required field types per visualization: [references/tiles.md](references/tiles.md)

## Variables Quick Reference

```json
{ "version": 2, "key": "Service", "type": "query", "visible": true,
  "editable": true, "input": "smartscapeNodes SERVICE | fields name",
  "multiple": false }
```

- **Single-select:** `filter service.name == $Service`
- **Multi-select:** `filter in(service.name, array($Service))`
- Types: `query` (DQL-populated), `csv` (static list), `text` (free-form)

Full variable reference: [references/variables.md](references/variables.md)

## References

| File | When to Load |
|------|-------------|
| [create-update.md](references/create-update.md) | Creating/updating dashboards |
| [tiles.md](references/tiles.md) | Tile types, visualization field requirements, settings |
| [variables.md](references/variables.md) | Variable types, replacement strategies, patterns |
| [analyzing.md](references/analyzing.md) | Reading dashboards, extracting queries, health assessment |

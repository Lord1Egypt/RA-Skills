---
name: qgis
description: Run QGIS geospatial processing with qgis_process for repeatable vector/raster workflows (reproject, clip, dissolve, buffer, merge, raster warping). Use when the user asks for GIS/QGIS automation, coordinate system conversion, geodata transformation, or batch map data processing. 中文触发：QGIS、地理处理、坐标转换、矢量裁剪、栅格重投影。
metadata: { "openclaw": { "emoji": "🗺️", "requires": { "bins": ["qgis_process"] }, "install": [{ "id": "brew", "kind": "brew", "formula": "qgis", "bins": ["qgis_process"], "label": "Install QGIS CLI (brew)" }] } }
---

# QGIS

Use this skill for deterministic, file-based GIS processing through `qgis_process`.

## Core Rules

- Confirm source files, destination files, and target CRS before running commands.
- Prefer writing to a new output path; do not overwrite source data unless user explicitly asks.
- Discover algorithm parameters from `qgis_process help <algorithm-id>` before execution.
- If output format is not specified, default to `GPKG` for vector and `GeoTIFF` for raster.
- For batch operations, run one representative file first, then scale to the full set.

## Standard Workflow

1. Validate tool and inspect capabilities:

```bash
qgis_process --version
qgis_process list
```

2. Find and inspect a specific algorithm:

```bash
qgis_process list | rg -i "clip|buffer|reproject|merge|warp|dissolve"
qgis_process help native:clip
```

3. Execute with explicit parameters:

```bash
qgis_process run <algorithm-id> -- \
  INPUT=<input-path> \
  OUTPUT=<output-path>
```

4. Verify output exists and report summary (path, layer count/bands, CRS, extent).

## Common Patterns

```bash
# Reproject vector layer
qgis_process run native:reprojectlayer -- \
  INPUT=./data/input.gpkg \
  TARGET_CRS=EPSG:4326 \
  OUTPUT=./out/reprojected.gpkg

# Clip vector layer by overlay
qgis_process run native:clip -- \
  INPUT=./data/roads.gpkg \
  OVERLAY=./data/boundary.gpkg \
  OUTPUT=./out/roads_clipped.gpkg

# Buffer vector features
qgis_process run native:buffer -- \
  INPUT=./data/points.gpkg \
  DISTANCE=100 \
  SEGMENTS=8 \
  DISSOLVE=false \
  OUTPUT=./out/points_buffer_100m.gpkg
```

## Safety Boundaries

- Do not guess units; confirm whether distance/area is in degrees or projected units.
- If CRS is missing/invalid, stop and ask for the intended CRS before processing.
- Avoid lossy conversion unless requested (for example dropping attributes or precision).
- For long batch runs, provide dry-run plan first: algorithm, inputs, outputs, and overwrite policy.

## OpenClaw + ClawHub Notes

- Keep commands shell-safe and reproducible in OpenClaw terminal sessions.
- Keep this skill portable: no hardcoded machine paths, credentials, or private endpoints.
- For clawhub.ai publication, keep versioning/changelog semver-driven and update examples only with generic sample data.

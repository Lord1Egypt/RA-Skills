---
name: wgs84
description: Explain and work with the WGS 84 coordinate system for GPS-style longitude/latitude data, including EPSG:4326 usage, axis-order checks, range validation, UTM zone recommendation, and reprojection planning. Use when the user asks about WGS84, EPSG:4326, GPS coordinates, 经纬度, 坐标校验, 轴顺序, UTM 分带, or WGS84 conversion guidance.
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["python3"]
    install:
      - id: "brew"
        kind: "brew"
        formula: "python"
        bins: ["python3"]
        label: "Install Python 3 (brew)"
---

# WGS84

Use this skill for practical work with WGS 84 longitude/latitude coordinates.

WGS 84 usually refers to the global geographic reference system commonly exposed as `EPSG:4326` in GIS software. It is the right default for GPS-style coordinate exchange, but it is not the right answer for every display or measurement workflow.

## What This Skill Does

- Explain what WGS 84 is and when to use it.
- Validate longitude/latitude numeric ranges.
- Check whether a coordinate pair is likely `lon,lat` or `lat,lon`.
- Recommend a UTM zone and EPSG code for projected analysis.
- Flag when a coordinate falls inside mainland-China extents where `GCJ-02` / `BD-09` confusion is common.
- Recommend whether to keep WGS84, use Web Mercator for display, or switch to a projected CRS for analysis.
- Explain when to keep data in `EPSG:4326` and when to reproject.
- Hand off file-based reprojection steps to `qgis` when execution is required.

## Standard Workflow

1. Confirm whether the input is WGS 84 already, or just "GPS coordinates" by assumption.
2. State the expected tuple order explicitly: `lon,lat` or `lat,lon`.
3. Validate numeric ranges before discussing conversion.
4. Decide the task type:
   - storage or API exchange
   - web map display
   - distance/area/buffer analysis
   - regional engineering or survey workflow
5. Keep `EPSG:4326` for exchange/storage unless the task needs projected units.
6. If analysis needs meters, recommend a suitable projected CRS such as a local CRS or UTM zone.

## Practical Commands

### Validate a WGS84 coordinate pair

```bash
python3 {baseDir}/scripts/wgs84_tool.py validate --lon 116.4074 --lat 39.9042
```

### Check whether a pair is probably `lon,lat` or `lat,lon`

```bash
python3 {baseDir}/scripts/wgs84_tool.py guess-order --a 116.4074 --b 39.9042
python3 {baseDir}/scripts/wgs84_tool.py guess-order --a 39.9042 --b 116.4074
```

### Recommend a UTM zone and EPSG code from WGS84 coordinates

```bash
python3 {baseDir}/scripts/wgs84_tool.py utm --lon 116.4074 --lat 39.9042
python3 {baseDir}/scripts/wgs84_tool.py utm --lon -122.478255 --lat 37.819929
```

### Flag China mapping offset risk

```bash
python3 {baseDir}/scripts/wgs84_tool.py china-check --lon 116.4074 --lat 39.9042
```

### Recommend the right CRS for a concrete task

```bash
python3 {baseDir}/scripts/wgs84_tool.py recommend --lon 116.4074 --lat 39.9042 --task exchange
python3 {baseDir}/scripts/wgs84_tool.py recommend --lon 116.4074 --lat 39.9042 --task analysis
python3 {baseDir}/scripts/wgs84_tool.py recommend --lon 116.4074 --lat 39.9042 --task web-map
```

## Decision Rules

- Prefer `EPSG:4326` for interoperable storage, APIs, logs, and exchange.
- Prefer a projected CRS in meters for buffering, area, distance, and nearest-neighbor analysis.
- Prefer `EPSG:3857` only for web-map display compatibility, not for accurate measurement.
- Do not assume a pair is WGS 84 just because it contains two decimals; confirm source system when accuracy matters.
- Do not assume all systems interpret `EPSG:4326` axis order the same way; many practical APIs use `lon,lat` even when standards prose differs.
- In mainland China workflows, explicitly check whether the source is raw WGS84 or app-level `GCJ-02` / `BD-09`.
- Treat `GCJ-02` and `BD-09` as mapping offset systems, not simple aliases for `EPSG:4326`.

## What To Return

- The interpreted coordinate order.
- Whether the values are valid WGS84 longitude/latitude ranges.
- Whether keeping `EPSG:4326` is appropriate for the task.
- If not, recommend the target CRS and explain why.
- If using UTM, provide zone number, hemisphere, and EPSG code.
- If the point is in mainland China, include a short warning about `GCJ-02` / `BD-09` ambiguity when relevant.

## When Not To Use

- Reverse geocoding or coordinates to address lookup: use `geocode`.
- File-based GIS conversion or batch reprojection: use `qgis`.
- General CRS comparison beyond WGS84-centered guidance: use `project`.
- Navigation routing, POI search, or map reviews.

## OpenClaw + ClawHub Notes

- Keep examples generic and reproducible.
- Do not hardcode private paths, real device traces, or private datasets.
- For clawhub.ai publication, keep versioning/changelog semver-driven and examples standards-based.

## Reference Docs In This Skill

- Read `{baseDir}/references/wgs84-reference.md` for concise CRS comparison and common failure cases.

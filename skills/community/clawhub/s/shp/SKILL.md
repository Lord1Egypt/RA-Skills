---
name: shp
description: Inspect, explain, validate, and convert ESRI Shapefile datasets, including `.shp/.shx/.dbf/.prj` sidecar requirements, CRS detection, field-name/type limits, encoding problems, multipart geometry issues, and migration guidance to GeoPackage or GeoJSON. Use when the user asks about shapefile, Shapefile, `.shp` files, DBF encoding, PRJ/CRS problems, or batch shapefile cleanup. 中文触发：shapefile、shp、dbf、prj、坐标系丢失、字段截断、编码乱码。
metadata:
  openclaw:
    emoji: "🧳"
---

# Shapefile

Use this skill for practical Shapefile handling, debugging, and migration planning.

## Workflow

1. Confirm whether the task is inspection, repair, conversion, schema explanation, or batch cleanup.
2. Identify which companion files are present: `.shp`, `.shx`, `.dbf`, `.prj`, and optionally `.cpg`.
3. Check CRS, encoding, geometry type, and field-name limits before suggesting edits or conversions.
4. Prefer writing outputs to a new path; avoid in-place mutation unless the user explicitly asks.
5. If the dataset is large or the workflow is repeated, prefer a deterministic CLI path through `qgis`.

## Core Rules

- Treat a Shapefile as a multi-file dataset, not a single `.shp` file.
- Missing `.shx` or `.dbf` usually means the dataset is incomplete.
- Missing `.prj` means CRS is unknown, not automatically WGS84.
- DBF field names are short and legacy-oriented; watch for truncation and type loss.
- Text encoding may depend on `.cpg`; without it, non-ASCII text can decode incorrectly.
- Shapefile is poor for long field names, rich types, large text, and modern metadata needs.

## Common Failure Checks

- File opens but attributes are broken: verify `.dbf` exists and encoding is correct.
- Features draw in the wrong place: verify `.prj` exists and the CRS was not guessed incorrectly.
- Import succeeds but schema looks wrong: check field-name truncation and DBF type limitations.
- Multipart or invalid geometry surprises: inspect geometry type before conversion or editing.
- One file was copied alone: remind that the full sidecar set must travel together.

## Preferred Outcomes

- For interchange with legacy systems, preserve the Shapefile but document its CRS and encoding explicitly.
- For ongoing editing or richer schema, migrate to `GPKG`.
- For lightweight web interchange, convert to `GeoJSON` only when the CRS and precision tradeoffs are acceptable.
- For deterministic file conversion or batch fixes, hand off execution to `qgis`.

## Task Boundaries

- Use this skill for Shapefile structure, limitations, troubleshooting, and migration guidance.
- For general CRS selection, use `project` or `wgs84`.
- For actual file-based conversion, reprojection, clipping, or repair commands, use `qgis`.
- For web map rendering or tiles, use `mapbox` or `cesium` as appropriate.

## OpenClaw + ClawHub Notes

- Keep examples generic and portable.
- Do not hardcode private data paths, private datasets, or machine-specific environments.
- For clawhub.ai publication, keep the skill concise, reproducible, and semver-friendly; keep detailed patterns in references.

## Reference Docs In This Skill

- Read `{baseDir}/references/patterns.md` when you need concrete Shapefile validation, packaging, or conversion guidance.

# Shapefile Patterns

Load this file when the task needs concrete Shapefile troubleshooting or conversion patterns.

## Dataset Anatomy

A valid Shapefile dataset usually includes:

- `.shp`: geometry records
- `.shx`: geometry index
- `.dbf`: attribute table
- `.prj`: CRS definition
- `.cpg`: optional text encoding hint

Minimum practical bundle for exchange is usually `.shp + .shx + .dbf`, and `.prj` should be included whenever the CRS is known.

## Inspection Checklist

Before proposing a fix, verify:

- Are all required sidecar files present?
- Is the geometry type known and consistent?
- Is the CRS explicit in `.prj`, or only assumed?
- Is text encoding known, especially for non-English attributes?
- Are field names already truncated or colliding?

## High-Confidence Guidance

- Never assume missing `.prj` means `EPSG:4326`.
- Never rename only the `.shp`; the whole sidecar set must keep the same basename.
- Never promise lossless conversion from modern formats to Shapefile when long fields, null handling, Unicode, or rich attribute types are involved.
- If users need edits, metadata, or repeated round-trips, recommend `GPKG`.

## Typical Problems

### Missing `.prj`

Symptoms:

- Data appears in the wrong place.
- GIS software asks for CRS on import.
- The same coordinates line up only after manual reassignment.

Guidance:

- Ask for the source CRS from the data producer if accuracy matters.
- If the user only knows the data is "GPS-like", investigate whether it is really WGS84 longitude/latitude before assigning `EPSG:4326`.
- Distinguish assigning a CRS from reprojecting to a new CRS.

### Encoding Problems

Symptoms:

- Chinese or accented attribute text is garbled.
- The DBF opens with replacement characters or mojibake.

Guidance:

- Check whether a `.cpg` file exists.
- If not, document that the original encoding is ambiguous.
- Prefer converting to `GPKG` after decoding correctly so the encoding problem does not persist.

### Field Limits

Shapefile/DBF constraints commonly cause:

- Long field names being truncated.
- Numeric precision loss.
- Dates and nullability behaving inconsistently across tools.
- Unsupported richer types such as nested structures or large text blobs.

When mapping from modern schemas, tell the user which fields may be lossy before conversion.

## Packaging Advice

When sharing a dataset:

- Zip the entire set of same-basename files together.
- Keep filenames ASCII-safe when compatibility matters.
- Include a short note describing CRS and encoding if the receiver is not using a controlled workflow.

## Conversion Advice

Preferred migration targets:

- `GPKG` for desktop GIS editing, distribution, and richer schemas.
- `GeoJSON` for web pipelines and lightweight exchange.
- FlatGeobuf or Parquet only when the surrounding stack already supports them.

If the user wants commands, route to `qgis` for deterministic execution. Typical operations include:

- assign missing CRS
- reproject to a new CRS
- convert Shapefile to `GPKG`
- convert Shapefile to `GeoJSON`
- validate/fix invalid geometries before export

## Response Pattern

When answering, state:

1. Which companion files are required or missing.
2. Whether CRS is known, assumed, or missing.
3. Whether encoding risk exists.
4. Whether schema loss is likely.
5. The safest next action: preserve, repair, or migrate.

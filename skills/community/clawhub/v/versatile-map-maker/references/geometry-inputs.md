# Geometry Inputs

Use GeoJSON as the common internal format.

## Good GeoJSON Inputs

- `FeatureCollection` with `Polygon` or `MultiPolygon` geometries for regions.
- Stable region identifier in properties such as `id`, `GEOID`, `ISO_A2`, `ISO_A3`, `hc-key`, `hasc`, `name`, or a user-provided field.
- Human-readable name field for diagnostics and legends.

## Conversion Notes

- Shapefile: convert with `ogr2ogr -f GeoJSON out.geojson in.shp` when GDAL is available.
- TopoJSON: convert with `npx topojson-client` or another local converter.
- CSV-only data is not geometry. It needs an existing boundary source or a crosswalk to one.

## ID Matching

Prefer exact IDs over fuzzy names. If fuzzy matching is necessary:

- normalize case, whitespace, punctuation, and accents
- review ambiguous matches manually
- report unmatched rows
- do not silently merge different regions with similar names


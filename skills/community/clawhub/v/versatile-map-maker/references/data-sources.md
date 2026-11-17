# Data Sources

Choose the least complicated source that honestly supports the requested geography.

## Fast Built-In Sources

- **Highcharts map collection**: best for world, continent, country, and admin1 maps when an editable SVG is needed quickly.
- **Natural Earth**: best for global country borders, coastlines, rivers, and broad reference layers.

## User-Supplied Or External Sources

- **GeoJSON**: preferred interchange format for the bundled scripts.
- **TopoJSON**: convert to GeoJSON first when needed.
- **Shapefile**: convert to GeoJSON with GIS tooling before using bundled scripts.
- **US Census TIGER/Line**: use for US states, counties, tracts, and places.
- **Eurostat GISCO**: use for EU/NUTS regions.
- **geoBoundaries or GADM**: use for administrative boundaries when licensing and access are acceptable.
- **OpenStreetMap/Overpass**: use for custom features or places when a curated boundary source is unavailable.

## Granularity Checklist

Before drawing:

1. Identify the requested level: country, state/province, county/district, municipality, neighborhood, custom region.
2. Verify the source actually has that level.
3. Check whether geometry is generalized or simplified.
4. Record missing or unmatched regions.

Never describe a coarse source as a fine-grained map.


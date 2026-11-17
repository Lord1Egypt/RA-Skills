---
name: versatile-map-maker
description: Create editable SVG maps for choropleths, categorical region maps, point/label overlays, and custom or historical boundary overlays from Highcharts maps or user-provided GeoJSON/TopoJSON/shapefile-derived data. Use when a user asks to visualize data by country/state/province/county/municipality/custom region, make a heat map, recolor map regions, trace boundaries, or produce a reusable map asset.
---

# Versatile Map Maker

Create real, editable SVG maps from either built-in public map data or user-supplied geometry.

Use the fastest honest path:

1. **Known admin0/admin1 map**: fetch a ready SVG + GeoJSON from Highcharts.
2. **County, municipality, custom, historical, fantasy, or unusual regions**: ask for or use a GeoJSON/TopoJSON/shapefile-derived file, then generate the SVG locally.
3. **Boundary overlay**: draw one or more polygon/line overlays on top of either map source, using real feature geometry when available.

Always be explicit about precision: region boundaries are as exact as the source geometry; hand-entered lines are schematic; coarse datasets must not be described as fine-grained maps.

## Working Rules

- Work in a scratch directory under the current project or system temp directory.
- Keep source data, generated SVGs, previews, and notes together.
- Preserve originals. Write new outputs rather than overwriting user-provided data.
- Prefer editable SVG as the deliverable; render PNG previews only for verification.
- Preview every final SVG before reporting completion.
- If a requested granularity is unavailable, say so before making a coarser substitute.

## Dependencies

Install only what is needed for the chosen path:

```bash
python -m pip install numpy cairosvg
```

Optional:

- `npm` for the Highcharts fast path.
- `geopandas`, `shapely`, or `ogr2ogr` only when converting shapefiles/TopoJSON outside the bundled scripts.
- `matplotlib` only if you extend palettes beyond the built-in script palettes.

## Path A: Highcharts Fast Path

Use this for world, continent, country, state, or province maps when admin1 granularity is enough.

```bash
python scripts/fetch_base_map.py --list serbia
python scripts/fetch_base_map.py countries/rs/rs-all ./mapwork
python scripts/fit_transform.py ./mapwork/rs-all.svg ./mapwork/rs-all.geo.json ./mapwork/transform.json
```

Highcharts keys commonly look like:

- `custom/world`
- `custom/europe`
- `countries/us/us-all`
- `countries/fr/fr-all`
- `countries/rs/rs-all`

If `npm` is missing or the key is unavailable, switch to Path B.

## Path B: Bring Your Own Geometry

Use this for counties, municipalities, custom regions, historical maps, fictional regions, or any project where the built-in map is too coarse.

Input should be GeoJSON when possible. If the user has a shapefile, convert it to GeoJSON with GIS tooling first.

```bash
python scripts/geojson_to_svg.py regions.geojson base.svg \
  --id-field GEOID --name-field NAME --metadata-out regions-index.json \
  --transform-out transform.json
```

Then color the generated SVG just like a Highcharts map:

```bash
python scripts/recolor_choropleth.py base.svg data.json choropleth.svg \
  --title "..." --subtitle "..." --legend-label "..."
```

The generated SVG path IDs come from `--id-field`; if omitted, the script tries common fields such as `id`, `GEOID`, `ISO_A2`, `hc-key`, `hasc`, and `name`.

## Joining User Data

For JSON data already keyed by region id, use it directly:

```json
{"US.CA": 39.5, "US.TX": 30.0}
```

For CSV tables, create the JSON mapping:

```bash
python scripts/join_data.py data.csv data.json --id-col region_id --value-col value --numeric
```

If labels do not match geometry IDs, inspect `regions-index.json` or the GeoJSON properties and build a clean crosswalk. Do not guess ambiguous matches.

## Choropleths

Numeric data uses a continuous color scale; text data uses categorical swatches.

```bash
python scripts/recolor_choropleth.py base.svg data.json out.svg \
  --title "Population by Region" \
  --subtitle "Source: ..." \
  --legend-label "People" \
  --cmap YlOrRd \
  --missing-fill "#F2F2F2" \
  --style style.json
```

Use a style JSON when the user needs brand colors or a different visual tone:

```json
{
  "font_family": "Arial, sans-serif",
  "neutral_fill": "#F2F2F2",
  "neutral_stroke": "#BDBDBD",
  "qualitative": ["#4E79A7", "#F28E2B", "#59A14F"],
  "title_fill": "#222222"
}
```

## Boundary And Feature Overlays

Use overlays for historical borders, custom territories, service areas, disputed/uncertain lines, routes, and highlighted regions.

Boundary JSON accepts either a single ring or a FeatureCollection-like object:

```json
{
  "features": [
    {"type": "polygon", "coordinates": [[[20.4,44.8],[21.0,44.6],[20.4,44.8]]], "label": "Inside"},
    {"type": "line", "coordinates": [[20.4,44.8],[21.0,44.6]], "dash": true, "label": "Approximate"},
    {"type": "point", "coordinates": [20.46,44.81], "label": "Capital"}
  ]
}
```

Draw it:

```bash
python scripts/overlay_boundary.py base.svg transform.json boundary.json out.svg \
  --title "Historical Boundary" \
  --subtitle "Modern base, historical overlay" \
  --legend-inside "Historical area" \
  --legend-outside "Modern reference"
```

When a boundary follows a river/coast/administrative border, prefer real geometry. For rivers:

```bash
python scripts/fetch_rivers.py "Danube" "Sava" --out rivers.json
python scripts/fetch_rivers.py --slice rivers.json "Danube" 20.455,44.840 22.545,44.226 --out danube-segment.json
```

If a real feature cannot be found, draw a schematic line and label the uncertainty.

## Preview

Render a PNG preview before delivery:

```bash
python - <<'PY'
import cairosvg
cairosvg.svg2png(url="out.svg", write_to="preview.png", output_width=1000)
PY
```

Inspect the preview for:

- missing colored regions
- mismatched IDs
- clipped titles or legends
- illegible labels
- boundaries shifted away from the base map
- misleading precision

## Deliver

Return the final SVG and any useful preview PNG. Include a short note naming:

- map source and granularity
- data source
- whether geometry was exact, generalized, or schematic
- any unmatched regions or missing data

## Read More When Needed

- For source choice and granularity: `references/data-sources.md`
- For geometry conversion and ID matching: `references/geometry-inputs.md`
- For styling and accessibility: `references/styling.md`
- For the original Highcharts/Natural Earth technique notes: `references/technique.md`

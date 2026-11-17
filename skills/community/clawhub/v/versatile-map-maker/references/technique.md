# Technique notes and worked examples

This skill was distilled from two maps built for Serbia in a live session:
a choropleth (municipalities/districts colored by distance from a town) and
a historical boundary overlay (Principality of Serbia, 1830s–1878, drawn on
a modern base map). Both used the same base-map source and transform-fitting
approach now wrapped in `scripts/`.

## Why `@highcharts/map-collection`

It's a free npm package bundling, per country/continent/world, a ready SVG
*and* a matching GeoJSON with each region's centroid lon/lat and a shared id
scheme (`hasc`, e.g. `RS.PM`) — which means no manual georeferencing is
needed to figure out which SVG path is which region. Alternatives considered
and rejected in the original session:

- **GADM, geoBoundaries (ADM2/municipality level)**: real municipality-level
  boundaries exist but are typically served via Git LFS or a dedicated API,
  neither reachable from a sandboxed environment with a domain allowlist.
  If the user needs finer-than-district granularity, ask them to upload a
  GeoJSON/shapefile directly — don't substitute a coarser map silently.
- **click_that_hood / codeforgermany geojson repos**: fine for a quick
  district-level polygon set but no matching blank SVG, and coarser than
  `@highcharts/map-collection` in at least one case tested (30 features vs.
  25, both district/okrug level, not municipality level).

## Why Natural Earth for rivers

`nvkelso/natural-earth-vector` mirrors Natural Earth's public-domain vector
data as plain GeoJSON files directly in a GitHub repo (not Git LFS) — so it's
fetchable with a plain `curl`/`raw.githubusercontent.com` request. Two files
matter: `geojson/ne_10m_rivers_lake_centerlines.geojson` (major rivers
worldwide, single LineString or MultiLineString per named river) and
`geojson/ne_10m_rivers_europe.geojson` (adds smaller named European
tributaries). A river geometry search that comes up empty is a real
signal — it means that stretch of a boundary needs a schematic line, not
that the search should be retried with guessed spellings.

## The centroid-matching trick (why `fit_transform.py` works)

The SVG's path coordinates are in an arbitrary projected pixel space with no
declared relationship to lon/lat. The GeoJSON gives each region a
label-point lon/lat, and Highcharts also stores a label pixel position
(`hc-middle-x`/`hc-middle-y`, fractional 0–1 within the map's bounding box)
— but that label position is for *text placement*, not the region's true
area centroid, so fitting a transform against it directly produced ~50px
mean error in testing (on a 700px map — enough to misplace a boundary by
tens of kilometers).

Computing the **true polygon centroid** from the SVG path's own coordinates
(shoelace formula, `common.polygon_centroid`) and pairing that with the
GeoJSON's given lon/lat brought mean error down to ~6–7px (roughly 5km on a
country-sized map) — accurate enough to place a boundary correctly relative
to district lines. This is why `fit_transform.py` parses path geometry
directly rather than trusting either dataset's label-position field.

Sanity check after fitting: pick one region you're confident about (e.g. the
capital) and eyeball its predicted pixel position against where that shape
actually is in a rendered preview, before trusting the transform for
anything else.

## Layout: why the title always needs a `viewBox` fix

The base maps have no headroom above/below the drawn shapes — adding a title
or legend directly will overlap the northernmost regions unless the SVG's
`viewBox` is expanded with negative top-left origin (e.g.
`viewBox="{minx-10} {miny-70} {width+20} {height+70+110}"`) and the title/
legend are positioned in that new negative-y / below-maxy space, not inside
the original 0..height range. Both `recolor_choropleth.py` and
`overlay_boundary.py` do this automatically — if you're hand-editing an SVG
outside those scripts, remember the same fix.

## Honesty calibration from the worked examples

- The distance choropleth was delivered as **district-level**, with an
  explicit statement that municipality-level data wasn't reachable — the
  user was glad to know the ceiling rather than discover it later.
- The first cut at the historical boundary used hand-picked straight-line
  vertices between towns. It was functional but visibly crude. The second
  version, using real river geometry for river-following stretches and
  keeping straight lines only for the genuinely river-less inland frontier,
  was the version the user actually wanted — "much much better." The lesson
  generalized into this skill: **default to real geometry wherever a natural
  or administrative feature actually defines the boundary; reserve
  schematic lines for stretches where nothing does, and say so either way.**

# WGS84 Reference

Use this file when the user needs precise but concise guidance centered on WGS 84.

## Core facts

- WGS 84 is a global geodetic reference system.
- In GIS workflows it is commonly represented as `EPSG:4326`.
- Coordinates are angular: longitude and latitude in degrees.
- WGS 84 is excellent for exchange and storage, but not ideal for direct distance or area calculation.

## When WGS84 is the right answer

- GPS-style coordinate exchange
- APIs that expect global longitude/latitude
- Lightweight storage of point locations
- Interoperability between systems before local reprojection

## When WGS84 is not enough

- Distance, area, and buffer analysis
- High-accuracy engineering workflows
- Local mapping tasks that require a projected CRS in meters
- Tile display systems that require `EPSG:3857`

## Common confusion points

### EPSG:4326 vs WGS84

- In most everyday GIS software conversations, people treat them as the practical same answer.
- In precise geodesy, the reference frame details can matter more than casual GIS usage suggests.
- For ordinary mapping/data exchange tasks, saying "WGS84 / EPSG:4326" is usually sufficient.

### Axis order

- Many APIs and mapping libraries use `lon,lat`.
- Some formal CRS descriptions or standards text may advertise latitude-first ordering.
- Always check the consuming API or tool instead of assuming.

### Web Mercator

- `EPSG:3857` is convenient for web maps and slippy tiles.
- It uses meters, but that does not make it a good measurement CRS.
- Do not use it for precise distance or area analysis when a better local projection is available.

### UTM from WGS84

- UTM is often a practical projected follow-up when data starts in WGS84.
- Northern hemisphere UTM EPSG codes are commonly `32601` to `32660`.
- Southern hemisphere UTM EPSG codes are commonly `32701` to `32760`.

### China web-map offsets

- `GCJ-02` and `BD-09` are commonly encountered in China consumer-map ecosystems.
- A point being inside mainland China does not prove it is offset, but it raises the need to verify the source.
- If coordinates came from a phone GPS logger, GNSS receiver, or a standards-based export, raw WGS84 may still be correct.
- If coordinates came from a consumer web map, SDK, screenshot, or copied app pin, verify whether they are `GCJ-02` or `BD-09`.

## Task-driven recommendations

- Exchange or API payloads: keep `WGS84 / EPSG:4326`.
- Slippy map display: often convert or render against `EPSG:3857`.
- Buffer, distance, area, density, or nearest-neighbor work: reproject to a CRS in meters.
- City or regional analysis: UTM is a practical default when no better local CRS is specified.
- National or regulated workflows: follow the mandated CRS instead of defaulting to WGS84.

## Common failure cases

- Swapping `lat,lon` and `lon,lat`
- Sending out-of-range values like longitude `190` or latitude `95`
- Measuring distance directly in degrees
- Assuming all coordinates from China web maps are raw WGS84 when they may actually be `GCJ-02` or `BD-09`
- Treating WGS84 as the final answer for every GIS workflow

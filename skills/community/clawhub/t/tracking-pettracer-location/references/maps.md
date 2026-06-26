# Map screenshots (static map images)

When the user asks for a **map screenshot** (an image you can send/attach), use a **static map image API**.

## Recommended default: Google Maps Static API

Google’s *Maps Static API* returns a map **image** (PNG/JPG/GIF) from a single HTTP request. It supports zoom, size, maptype, markers, and more.

### Why this is the default

- Most OpenClaw users already have access to a Google Cloud project.
- No browser automation is needed.
- The agent can download a PNG and send it as an attachment.

### Setup checklist (minimal)

1) In Google Cloud Console: enable billing on the project.
2) Enable **Maps Static API**.
3) Create an **API key**.
4) Put the key in the agent environment as:

- `GOOGLE_MAPS_API_KEY`

Optional tuning env vars:
- `GOOGLE_MAPS_MAPTYPE` (`roadmap|satellite|hybrid|terrain`, default `hybrid`)
- `GOOGLE_MAPS_SIZE` (default `640x640`)
- `GOOGLE_MAPS_SCALE` (`1|2`, default `2`)

### Limits / behaviour notes

- Static Maps image size is commonly capped at **640×640** per request; `scale=2` returns **2×** pixels (e.g. `640x640` → `1280x1280`).
- Google Maps Platform usage is billed; set quotas/alerts to control cost.

### Script

Use:
- `scripts/pettracer_mapshot.py`

This script:
- Calls PetTracer to get the latest fix for a pet
- Calls Google Static Maps
- Writes a PNG to disk
- Prints JSON describing the file (path, bytes, lat/lon, timestamps)

## Alternatives (not implemented by default)

If Google Maps Static API isn’t viable, alternatives include:

- **Mapbox Static Images API** (needs Mapbox access token)
- **OSM-derived static map services** (often free/cheap, but you must respect provider terms; OSM Foundation tile servers are best-effort and can block heavy usage)

If you need one of these alternatives, extend `pettracer_mapshot.py` with a `--provider` switch.

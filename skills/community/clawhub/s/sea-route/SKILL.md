---
name: sea-route
description: "Sea route navigation: generate the shortest maritime route between two ports or coordinates, output navigation waypoints and an interactive HTML map. Use when the user mentions sea route, shipping route, maritime navigation, port-to-port distance, 海运航线, 航线规划, 海上路线, 港口距离, 船运路线."
version: 1.0.0
tags:
  - navigation
  - maritime
  - visualization
  - map
---

# Sea Route Navigation Skill

Generate the shortest sea route between two points on the globe. Returns navigation waypoints (coordinates) and an interactive HTML map visualization.

## When to Use

- User asks for a sea/shipping/maritime route between two locations
- User wants port-to-port distance or travel time estimate
- User needs navigation waypoints for maritime routing
- User wants a visual map of a shipping lane

## How It Works

This skill uses a Python script (`scripts/sea_route.py`) powered by the `searoute` library. It computes the shortest path over ocean, avoids land masses, and outputs:

1. **Waypoint coordinates** (longitude, latitude) printed to stdout as JSON
2. **An interactive HTML map** saved to a user-specified path (default: `./sea_route_map.html`)

The script uses `uv` for dependency management — no manual `pip install` needed.

## Usage

### Step 1 — Resolve user input to coordinates

The user may provide:

- **City / port names** (e.g., "天津" and "大阪", "Rotterdam" and "Singapore")
- **Coordinates** directly (e.g., `[117.75, 38.99]`)

If the user provides city or port names, you MUST convert them to `[longitude, latitude]` coordinates yourself before calling the script. Use well-known port coordinates:

| Port | Longitude | Latitude |
|------|-----------|----------|
| 天津港 (Tianjin) | 117.75 | 38.99 |
| 上海港 (Shanghai) | 121.47 | 31.23 |
| 大阪港 (Osaka) | 135.25 | 34.65 |
| 深圳港 (Shenzhen) | 114.27 | 22.55 |
| 香港 (Hong Kong) | 114.17 | 22.28 |
| 新加坡 (Singapore) | 103.85 | 1.29 |
| 鹿特丹 (Rotterdam) | 4.50 | 51.90 |
| 汉堡 (Hamburg) | 9.97 | 53.53 |
| 洛杉矶 (Los Angeles) | -118.27 | 33.73 |
| 纽约 (New York) | -74.04 | 40.67 |
| 迪拜 (Dubai) | 55.27 | 25.27 |
| 悉尼 (Sydney) | 151.21 | -33.87 |
| 釜山 (Busan) | 129.04 | 35.10 |
| 东京 (Tokyo) | 139.77 | 35.45 |
| 高雄 (Kaohsiung) | 120.29 | 22.61 |

For ports not listed above, look up reasonable coordinates for the port area.

### Step 2 — Run the script

Run with `uv`:

```bash
uv run --script /path/to/skills/sea-route/scripts/sea_route.py \
  --origin-lon <LON> --origin-lat <LAT> \
  --dest-lon <LON> --dest-lat <LAT> \
  --origin-name "Port A" --dest-name "Port B" \
  --output ./sea_route_map.html
```

**Parameters:**

| Flag | Required | Description |
|------|----------|-------------|
| `--origin-lon` | Yes | Origin longitude |
| `--origin-lat` | Yes | Origin latitude |
| `--dest-lon` | Yes | Destination longitude |
| `--dest-lat` | Yes | Destination latitude |
| `--origin-name` | No | Display name for origin (default: "Origin") |
| `--dest-name` | No | Display name for destination (default: "Destination") |
| `--output` | No | Output HTML file path (default: `./sea_route_map.html`) |

### Step 3 — Present results to user

The script prints a JSON object to stdout with this structure:

```json
{
  "origin": {"name": "Tianjin", "lon": 117.75, "lat": 38.99},
  "destination": {"name": "Osaka", "lon": 135.25, "lat": 34.65},
  "distance_km": 1891,
  "duration_hours": 42.5,
  "waypoints": [
    {"seq": 1, "lon": 118.1725, "lat": 38.7726},
    ...
  ],
  "html_map": "./sea_route_map.html"
}
```

Present to the user:
1. A summary: origin → destination, distance, estimated time
2. The waypoint coordinate table
3. Tell them the HTML map file path and offer to open it

### Step 4 — Open the map (optional)

If the user wants to see the map:

```bash
open ./sea_route_map.html    # macOS
xdg-open ./sea_route_map.html  # Linux
```

## Example Interaction

**User:** 帮我生成从天津到大阪的海运航线

**Agent:**
1. Resolve: 天津港 → [117.75, 38.99], 大阪港 → [135.25, 34.65]
2. Run:
```bash
uv run --script ~/.agents/skills/sea-route/scripts/sea_route.py \
  --origin-lon 117.75 --origin-lat 38.99 \
  --dest-lon 135.25 --dest-lat 34.65 \
  --origin-name "天津港" --dest-name "大阪港" \
  --output ./tianjin_osaka_route.html
```
3. Parse JSON output, present waypoints and summary
4. Open the HTML map

## Notes

- The `searoute` library generates approximate maritime routes suitable for visualization and distance estimation. It is NOT intended for real navigation.
- Coordinates use `[longitude, latitude]` order (GeoJSON convention).
- The script requires `uv` to be installed. It uses inline script dependencies — no virtual environment setup needed.
- Estimated speed is ~25 knots (typical cargo vessel cruising speed).

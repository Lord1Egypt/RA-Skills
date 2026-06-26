# Trip Packer Planning Guide

Use this guide to help users plan a trip and produce valid trip-packer JSON.

## Planning Workflow

### Step 1: Gather Basics
- **Destination(s)**: City name and country (ISO code like `CN`, `JP`, `KR`).
- **Duration**: Number of days.
- **Hotel**: Name, address, and coordinates (or a well-known landmark near the city center).

### Step 2: Build Daily Routes
For each day, ask:
- **Theme/area** (e.g., "East Kyoto temples")
- **Spots**: 2–5 locations with names, addresses, and approximate coordinates.
- **Transport**: How they move between spots (walk, subway, taxi, train). Ask for rough duration/distance.
- **Meals** (optional): Restaurants can be added as `spot` locations with `parentId` pointing to the hotel or a nearby group.

### Step 3: Choose Map Tile Source
Set `metadata.country` based on the ISO country code:
- `"CN"` → uses Amap (Gaode) tiles for users in China.
- Anything else → uses CARTO CDN tiles.

## JSON Structure Cheat Sheet

### `metadata`
```json
{
  "title": "Kyoto 4-Day Trip",
  "subtitle": "3 nights near Kyoto Station",
  "mapCenter": { "lat": 35.01, "lng": 135.77 },
  "mapZoom": 13,
  "cityLabel": "京都",
  "seasonLabel": "AUTUMN",
  "flag": "🇯🇵",
  "country": "JP"
}
```

### `locations`
Two types:
- **`hotel_group` / `group`**: A parent location with `children: ["spot-id"]`, `lat`, `lng`, `color`.
- **`spot`**: A specific place with `parentId` pointing to its group/hotel, `lat`, `lng`, `color`, `type: "spot"`.

### `days`
Each day needs:
- `day`: 1-based number
- `title`, `note`, `baseHotelId`
- `path`: ordered array of `PathPoint`

#### `PathPoint`
```json
{
  "locationId": "spot-id",
  "label": "Walk · about 10 min",
  "isHotel": false,
  "transit": {
    "distance": "about 1 km",
    "duration": "about 10 min",
    "startName": "Spot A",
    "endName": "Spot B",
    "steps": [
      {
        "mode": "walk",
        "from": "Spot A",
        "to": "Spot B",
        "duration": "about 10 min",
        "distance": "about 1 km",
        "instruction": "Head north along the river"
      }
    ]
  }
}
```

Rules:
- `path[0]` should usually be the hotel (with `isHotel: true`).
- The last point can also be the hotel with `isHotel: true`.
- `mode` values: `walk`, `subway`, `bus`, `train`, `taxi`, `airport`.

## Common CLI Commands

```bash
# Validate data
npx trip-packer validate -d kyoto.json

# Build single-city HTML
npx trip-packer build -d kyoto.json -o kyoto-map.html

# Build multi-city HTML
npx trip-packer build -d kyoto.json -d tokyo.json --default-city kyoto -o japan-trip.html
```

## Tips

- Keep `label` human-readable; it appears on the map route.
- If you don’t have exact coordinates, use a map search or estimate from a well-known nearby point.
- When in doubt, create a minimal 2-day itinerary first, validate it, build it, show the user the result, then expand.

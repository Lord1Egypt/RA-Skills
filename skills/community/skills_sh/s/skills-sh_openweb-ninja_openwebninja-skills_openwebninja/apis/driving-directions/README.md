# driving-directions

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/driving_directions.yaml

**Host:** `driving-directions1.p.rapidapi.com`
**Notes:** Returns a single route response. No pagination.

## Endpoints

### GET /get-directions
Get Directions — Get driving directions from an origin to a destination.

**Required:**
- `origin` (string) Example: `Church St & 29th St, San-Francisco, CA, USA`
- `destination` (string) Example: `Sunnyvale, CA, USA`

**Optional:**
- `departure_time` (number, default: 0)
- `arrival_time` (number, default: 0)
- `distance_units` (string, default: auto) — values: auto, km, mi
- `avoid_routes` (string) Example: `tolls,ferries`
- `country` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Response path:** `data` (routes in `data.best_routes[]`)
**Key fields:** route_name, distance_meters, distance_label, duration_seconds, duration_label, min_duration_seconds, max_duration_seconds, departure_timestamp, departure_datetime_utc, arrival_timestamp, arrival_datetime_utc, route_parts, type, description, example

---

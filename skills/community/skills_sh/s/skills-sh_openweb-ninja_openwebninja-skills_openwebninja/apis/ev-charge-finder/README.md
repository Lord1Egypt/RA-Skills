# ev-charge-finder

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/ev_charge_finder.yaml

**Host:** `ev-charge-finder.p.rapidapi.com`
**Notes:** Returns all stations matching the location/radius in a single call. No pagination.

## Endpoints

### GET /search-by-location
Search by Location — Search for EV charging stations near a specific location specified as a free-form location query (e.g. `San Francisco, CA, USA`).

**Required:**
- `near` (string) Example: `San Francisco, CA, USA`

**Optional:**
- `type` (string) Example: `CHAdeMO`
- `available` (boolean) Example: `true`
- `min_kw` (number, default: 0)
- `max_kw` (number, default: 0)
- `limit` (number, default: 20) Example: `20`
- `query` (string)

**Pagination:** none
**Page size param:** `limit` (default: 20)

---

### GET /search-by-coordinates-point
Search by Coordinates Point — Search for EV charging stations near specific geographic coordinates point.

**Required:**
- `lat` (number) — Latitude of the geographic coordinates point to search near by. Example: `37.359428`
- `lng` (number) — Longitude of the geographic coordinates point to search near by. Example: `-121.925337`

**Optional:**
- `type` (string)
- `available` (string) — Find EV charging stations with an available connector.
- `min_kw` (number) — Restrict the result to the availability for connectors with a specific minimal value of power in kilowatts (closed inter
- `max_kw` (number) — Restrict the result to the availability for connectors with a specific maximum value of power in kilowatts (closed inter
- `limit` (number, default: 20) Example: `20`
- `query` (string)

**Pagination:** none
**Page size param:** `limit` (default: 20)

---

# waze

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/waze.yaml

**Host:** `waze.p.rapidapi.com`
**Notes:** Returns all current alerts and jams in the bounding box in a single call. No pagination.

## Endpoints

### GET /alerts-and-jams
Alerts and Jams

**Required:**
- `bottom_left` (string) Example: `40.66615391742187,-74.13732147216798`
- `top_right` (string) Example: `40.772787404902594,-73.76818084716798`

**Optional:**
- `center` (string)
- `radius` (string)
- `radius_units` (string, default: KM) — values: KM, MI
- `max_alerts` (integer, default: 20) Example: `20`
- `max_jams` (integer, default: 20) Example: `20`
- `alert_types` (string)
- `alert_subtypes` (string)

**Pagination:** none

---

### GET /driving-directions
Driving Directions

**Required:**
- `source_coordinates` (string) — Geographic coordinates (latitude, longitude pair) of the starting point Example: `32.0852999,34.78176759999999`
- `destination_coordinates` (string) — Geographic coordinates (latitude, longitude pair) of the destination Example: `32.7940463,34.989571`

**Optional:**
- `return_route_coordinates` (boolean) — Whether to return route coordinate pairs (route_coordinates field) Example: `Do not include in request`
- `arrival_timestamp` (number) — Unixtimestamp (seconds since epoch) of the arrival time (in case not specified directions will be returned for current t

**Pagination:** none

---

### GET /venues
Venues

**Required:**
- `bottom_left` (string) — Bottomleft corner of the geographic rectangular area for which to get venues. Specified as latitude, longitude pair. Example: `48.85100512509277,2.3341819660651026`
- `top_right` (string) — Topright corner of the geographic rectangular area for which to get venues. Specified as latitude, longitude pair. Example: `48.853125303884686,2.354381771086746`

**Optional:**
- `categories` (string)
- `zoom_level` (string) — Waze zoom level from 14 (4 is most zoomed in). Example: `1`

**Pagination:** none

---

### GET /autocomplete
Autocomplete

**Required:**
- `q` (string) — Freetext geographic query. Example: `sunn`
- `coordinates` (string) — Geographic coordinates (latitude, longitude) bias. Highly recommended to use for getting accurate results. Example: `37.376754,-122.023350`

**Optional:**
- `language` (string) — The language of the results. See https://wazeopedia.waze.com/wiki/USA/Countries_and_Languages for a list of supported la

**Pagination:** none
**Response path:** `data`
**Key fields:** name, address, latitude, longitude

---

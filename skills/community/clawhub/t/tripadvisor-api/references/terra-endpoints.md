# Terra API endpoints (curl + jq)

All paths are relative to `$BASE=https://terra.tripadvisor.com/api`. Every
call carries `-H "X-API-Key: $TRIPADVISOR_API_KEY" -H 'accept: application/json'`
(shorthand `"${H[@]}"` below). Shapes captured live with a Discover-plan key;
transcribed from `tripadvisor-mcp`'s `src/tools/search.ts` + `src/tools/location.ts`
(each section names its source tool). All 6 are `GET`, all read-only.

```sh
BASE=https://terra.tripadvisor.com/api
H=(-H "X-API-Key: $TRIPADVISOR_API_KEY" -H 'accept: application/json')
```

Categories are `RESTAURANT` | `ATTRACTION` | `HOTEL` (uppercase). `size` on
list endpoints defaults to 20 and is **capped at 20**.

---

## 1. Location search (`ta_search_locations` / `src/tools/search.ts`)

`GET /locations/search` — `query` (1–500 chars) required; optional
`category`, `search_type` (default `NAME`), `country_code` (alpha-2),
`geo_name`, `postal_code` (takes precedence over `geo_name`), `locale`
(repeated), `page`, `size`.

```sh
curl -sS "${H[@]}" "$BASE/locations/search?query=Golden+Gate+Bridge&category=ATTRACTION" \
  | jq '[.data[] | {id: .location.id, name: (.location.names[] | select(.primary) | .value),
        geo: .location.geo, rating: .location.traveler_ratings.overall.rating}]'
```

Response: `{"data": [{"location": <Location>, "matched_value": {"language","value"}}], "pagination": {...}}`.

## 2. Nearby search (`ta_search_nearby` / `src/tools/search.ts`)

`GET /locations/nearby` — center is **exactly one** of:
`lat`+`lon`+`radius` (`unit=MI|KM`, default `MI`), `location_id`+`radius`,
or the box `sw_lat`,`sw_lon`,`ne_lat`,`ne_lon` (box mode ignores `radius`).
Plus optional `category`, `min_rating` (1.0–5.0), `include_photo` (bool),
`sort` (`distance`|`rating`), `page`, `size`, `locale`.

```sh
# lat/lon + radius
curl -sS "${H[@]}" "$BASE/locations/nearby?lat=37.8199&lon=-122.4783&radius=5&unit=MI&category=RESTAURANT&sort=rating" \
  | jq '[.data[] | {id: .location.id, name: (.location.names[] | select(.primary) | .value),
        distance_mi: .distance_miles, bearing}]'

# location_id + radius (reference location as center)
curl -sS "${H[@]}" "$BASE/locations/nearby?location_id=104675&radius=2&unit=KM&category=HOTEL" | jq '.data'

# bounding box
curl -sS "${H[@]}" "$BASE/locations/nearby?sw_lat=37.70&sw_lon=-122.55&ne_lat=37.85&ne_lon=-122.35&category=ATTRACTION" \
  | jq '.data'
```

Response item: `{"location": <Location>, "bearing", "distance_miles", "distance_kilometers"}`.

## 3. Batch multi-get (`ta_get_locations` / `src/tools/location.ts`)

`GET /locations` — repeated `id` param (1–50 ids), required; optional
`locale`. **No `pagination` wrapper.** Unknown/unlicensed ids are silently
omitted (not an error) — a malformed id, e.g. one exceeding int32, does 400.

```sh
curl -sS "${H[@]}" "$BASE/locations?id=104675&id=93520&id=423942" \
  | jq '[.data[] | {id, name: (.names[] | select(.primary) | .value)}]'
```

Response: `{"data": [<Location>, ...]}` — cheaper than N single-id calls.

## 4. Location details (`ta_get_location_details` / `src/tools/location.ts`)

`GET /locations/{id}` — path `id` (int), **plural** `/locations/{id}` (the
docs' llms.txt index shows the singular form; that 404s). Optional
`locale` (repeated).

```sh
curl -sS "${H[@]}" "$BASE/locations/104675" | jq '{
  id, geo, name: (.names[] | select(.primary) | .value),
  rating: .traveler_ratings.overall, address: .addresses[0],
  phone: .phone_numbers[0].value, url: .urls.tripadvisor.main
}'
```

Response: the full `Location` object directly (not wrapped in `data`) —
`names`/`descriptions`/`addresses` are language-tagged arrays; the primary
entry has `"primary": true`.

## 5. Location photos (`ta_get_location_photos` / `src/tools/location.ts`)

`GET /locations/{id}/photos` — optional `page`, `size` (max 20), `locale`.

```sh
curl -sS "${H[@]}" "$BASE/locations/104675/photos?size=10" \
  | jq '[.data[] | {id, url: .photo.original_size_url, w: .photo.original_width, h: .photo.original_height}]'
```

Response: `{"data": [{"id","location_id","photo": {"key","original_size_url","original_height","original_width","media_type"}, "publish_ts", "source": {"name"}, "user"}], "pagination": {...}}`.

## 6. Location reviews (`ta_get_location_reviews` / `src/tools/location.ts`)

`GET /locations/{id}/reviews` — optional `page`, `size` (max 20), `locale`.

```sh
curl -sS "${H[@]}" "$BASE/locations/104675/reviews?size=10" | jq '.data'
```

Response: `{"data": [...review objects...], "pagination": {...}}`.

---

## Error bodies

- `400` — `{"type","title","status","detail","field_errors": [{"field","message"}],"trace_id"}`.
- `401`/`403` — `{"Message": "..."}` (a legacy-vs-Terra key mismatch reads
  as an AWS-gateway "explicit deny" message on the legacy endpoint).
- `404` — `{"message": "Not Found"}`.
- `429` — QPS (10) or daily quota (10,000) exceeded on Discover.

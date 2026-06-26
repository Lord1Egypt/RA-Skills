# Tripadvisor API Workflows

Use these official-content workflows when `TRIPADVISOR_API_KEY` is available.

## 1) Connectivity check

```bash
curl -sS -i "https://api.tripadvisor.com/api/partner/2.0/location/search?query=Madrid&key=${TRIPADVISOR_API_KEY}" | sed -n '1,20p'
```

Expected failure without valid key:
- HTTP 401
- `UnauthorizedException` with `invalid client ID`

## 2) Resolve location ID

```bash
curl -sS "https://api.tripadvisor.com/api/partner/2.0/location/search?query=Madrid&key=${TRIPADVISOR_API_KEY}" \
  | jq '.data[] | {location_id, name, result_type, address_obj}'
```

Store chosen mapping in `~/tripadvisor/api/location-cache.md`.

## Logging safety rule

- Never log full request URLs containing `key=...`.
- In `request-log.md`, replace secrets with `[REDACTED]`.
- Example safe log line:

```text
GET /api/partner/2.0/location/search?query=Madrid&key=[REDACTED] -> 200
```

## 3) Fetch place detail

```bash
curl -sS "https://api.tripadvisor.com/api/partner/2.0/location/${LOCATION_ID}?key=${TRIPADVISOR_API_KEY}" \
  | jq '{location_id, name, rating, num_reviews, ranking_data, price_level, web_url}'
```

## 4) Fetch nearby options

```bash
curl -sS "https://api.tripadvisor.com/api/partner/2.0/location/${LOCATION_ID}/nearby_search?key=${TRIPADVISOR_API_KEY}" \
  | jq '.data[] | {location_id, name, rating, num_reviews}'
```

## 5) Output contract

Always return:
- shortlist of 3-10 options
- score rationale (quality, value, confidence)
- source mode used (api/ui/hybrid)
- unresolved uncertainties

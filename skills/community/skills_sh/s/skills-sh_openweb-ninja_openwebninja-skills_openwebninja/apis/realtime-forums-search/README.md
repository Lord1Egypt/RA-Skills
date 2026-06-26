# realtime-forums-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_forums_search.yaml

**Host:** `real-time-forums-search.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param.

## Endpoints

### GET /search
Search Forums — Search in Discussions and Forums across the web. This endpoint returns the results returned when using the Forums tab on Google Search.

**Required:**
- `query` (string) — Search query Example: `iphone pro`

**Optional:**
- `time` (string, default: any) — values: any, hour, day, week, month, year
- `start` (integer, default: 0) Example: `0`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** offset (param: `start`)
**Response path:** `data`
**Key fields:** position, rank, title, snippet, url, source

---

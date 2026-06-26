# realtime-shorts-search

> ⚠️ **Known Issue:** This API currently returns empty results for all queries and may be non-functional.

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_shorts_search.yaml

**Host:** `real-time-shorts-search.p.rapidapi.com`
**Notes:** Page-based pagination.

## Endpoints

### GET /search
Search Shorts — Get real-time short video search results from across the web with pagination and filtering support.

**Required:**
- `query` (string) Example: `funny cat`

**Optional:**
- `page` (number, default: 1) Example: `1`
- `time` (string, default: any) — values: any, day, week, month, year
- `posted_date_from` (string) Example: `1/19/2025`
- `posted_date_to` (string) Example: `3/19/2025`
- `high_quality` (boolean) Example: `true`
- `closed_captioned` (boolean) Example: `true`

**Pagination:** page_number (param: `page`)
**Response path:** `data`
**Key fields:** id

---

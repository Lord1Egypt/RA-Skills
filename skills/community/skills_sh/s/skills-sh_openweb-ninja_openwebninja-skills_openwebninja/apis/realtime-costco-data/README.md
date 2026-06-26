# realtime-costco-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_costco_data.yaml

**Host:** `real-time-costco-data.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param.

## Endpoints

### GET /search
Search

**Required:**
- `query` (string) Example: `Nike`

**Optional:**
- `country` (string, default: US) Example: `US`
- `language` (string, default: en-US) Example: `en-US`
- `start` (number, default: 0) Example: `0`

**Pagination:** offset (param: `start`)

---

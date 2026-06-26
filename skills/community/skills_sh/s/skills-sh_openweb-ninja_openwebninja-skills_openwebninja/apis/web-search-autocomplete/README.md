# web-search-autocomplete

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/web_search_autocomplete.yaml

**Host:** `web-search-autocomplete.p.rapidapi.com`
**Notes:** Returns suggestions in a single call. cursor_pointer is a character position, not a pagination token.

## Endpoints

### GET /autocomplete
Autocomplete — Get query suggestions from Google Search, including Knowledge Graph information when available.

**Required:**
- `query` (string) — Autocomplete / typeahead search query. Example: `to`

**Optional:**
- `language` (string, default: en) Example: `en`
- `region` (string, default: us) Example: `us`
- `user_agent` (string, default: desktop) — values: desktop, mobile
- `cursor_pointer` (string)

**Pagination:** none
**Response path:** `data`
**Key fields:** queries, language, region, cursor_pointer, user_agent, type, status, request_id, parameters, data

---

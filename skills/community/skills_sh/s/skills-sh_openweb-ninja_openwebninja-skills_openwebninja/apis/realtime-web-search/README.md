# realtime-web-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_web_search.yaml

**Host:** `real-time-web-search.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param. Use 'num' param to control results per page (default 10).

## Endpoints

### GET /search
Search

**Required:**
- `q` (string) Example: `how to build a website`

**Optional:**
- `fetch_ai_overviews` (boolean) Example: `false`
- `num` (integer, default: 10) Example: `10`
- `start` (integer, default: 0) Example: `0`
- `gl` (string, default: us) Example: `us`
- `hl` (string, default: en) Example: `en`
- `tbs` (string)
- `location` (string)
- `device` (string, default: desktop) — values: desktop, mobile
- `nfpr` (string) — Exclude results of autocorrected query when the original query is misspelled with nfpr=1 and include them with nfpr=0 (d Example: `0`
- `lr` (string) Example: `0`
- `return_organic_result_video_thumbnail` (boolean) Example: `false`
- `extra_speed` (boolean) Example: `false`

**Pagination:** offset (param: `start`)
**Page size param:** `num` (default: 10)
**Response path:** `data` (organic results in `data.organic_results[]`)
**Key fields:** text_parts, reference_links, url, snippet, source, displayed_link, position, rank, answers_count, top_answer, date

---

### GET /search-light
Light Search

**Required:**
- `q` (string) Example: `how to build a website`

**Optional:**
- `limit` (string, default: 10) Example: `10`

**Pagination:** none
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** title, snippet, url, domain, position, type, maxLength

---

### GET /ai-mode
AI Mode

**Required:**
- `prompt` (string) Example: `How to make a pizza step by step?`

**Optional:**
- `session_token` (string)
- `gl` (string, default: us) Example: `us`
- `hl` (string, default: en) Example: `en`

**Pagination:** none

---

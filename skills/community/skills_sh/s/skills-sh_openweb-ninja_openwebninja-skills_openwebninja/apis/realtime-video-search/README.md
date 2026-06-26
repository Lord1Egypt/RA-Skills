# realtime-video-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_video_search.yaml

**Host:** `real-time-video-search.p.rapidapi.com`
**Notes:** Page-based pagination — each page returns up to 10 video results.

## Endpoints

### GET /search
Search Google Videos for any query and get real-time video results from across the web (YouTube, Vimeo, TikTok, news sites, and others), with pagination and filtering support.

**Required:**
- `query` (string) Example: `react tutorial`

**Optional:**
- `page` (integer, default: 1) — each page returns up to 10 results
- `country` (string, default: us) — ISO 3166-1 alpha-2 country code
- `language` (string, default: en) — ISO 639-1 language code
- `time_period` (string, default: any) — values: any, last_hour, last_day, last_week, last_month, last_year. Cannot be combined with `date_from`/`date_to`.
- `date_from` (string) — custom range start, MM/DD/YYYY. Use with `date_to`. Example: `01/01/2026`
- `date_to` (string) — custom range end, MM/DD/YYYY. Use with `date_from`. Example: `04/29/2026`
- `sort_by` (string, default: relevance) — values: relevance, date
- `duration` (string, default: any) — values: any, short (<4m), medium (4-20m), long (>20m)
- `safe` (string, default: off) — values: off, active

**Pagination:** page_number (param: `page`)
**Response path:** `data.videos`
**Key fields:** title, link, source, source_url, source_favicon_url, thumbnail_url, duration, duration_seconds, published_date, published_datetime_utc, position

`data.related_searches` (array of strings) is also returned alongside `data.videos` when available.

---

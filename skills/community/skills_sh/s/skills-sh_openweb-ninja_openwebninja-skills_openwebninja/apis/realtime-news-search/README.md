# realtime-news-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_news_search.yaml

**Host:** `real-time-news-search.p.rapidapi.com`
**Notes:** Query-based Google News **search** (single `/search` endpoint). Page-number pagination via the `page` param — each page returns up to 10 news results. Distinct from `realtime-news-data`, which is a topic/headline news feed with no pagination; this API searches Google's News tab for an arbitrary query and supports time-period / custom-date-range / sort-order / safe-search filters.

## Endpoints

### GET /search
Search — Search Google News for any query and get real-time news results. Returns a top stories cluster (when available for the query), plus the main news results with article metadata, source info, thumbnails, and published dates (both localized relative text and ISO 8601 UTC).

**Required:**
- `query` (string) — The news search query. Example: `artificial intelligence`

**Optional:**
- `page` (integer, default: 1) — Page number. Each page returns up to 10 results. Allowed: `1` and above.
- `country` (string, default: us) — ISO 3166-1 alpha-2 country code. Example: `us`
- `language` (string, default: en) — ISO 639-1 language code. Example: `en`
- `time_period` (string, default: any) — values: `any`, `last_hour`, `last_day`, `last_week`, `last_month`, `last_year`. Cannot be combined with `date_from`/`date_to`. Example: `last_day`
- `date_from` (string) — Start of a custom date range, `MM/DD/YYYY`. Must be sent with `date_to`; cannot be combined with `time_period` (other than `any`). Example: `01/01/2026`
- `date_to` (string) — End of a custom date range, `MM/DD/YYYY`. Must be sent with `date_from`. Example: `04/10/2026`
- `sort_by` (string, default: relevance) — values: `relevance`, `date`. Example: `relevance`
- `safe` (string, default: off) — values: `off`, `active`. Example: `off`

**Pagination:** page_number (param: `page`, 10 results/page). Response echoes `parameters.num_pages` — stop when `page >= num_pages`.
**Response path:** `data.news` (main results). An optional `data.top_stories` cluster is also returned when available.
**Key fields:** title, link, snippet, source_name, source_url, source_favicon_url, thumbnail_url, published_date, published_datetime_utc, position

---

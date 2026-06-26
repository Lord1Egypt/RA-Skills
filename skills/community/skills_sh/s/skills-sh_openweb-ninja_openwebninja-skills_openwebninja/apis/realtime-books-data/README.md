# realtime-books-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_books_data.yaml

**Host:** `real-time-books-data.p.rapidapi.com`
**Notes:** Page-based pagination.

## Endpoints

### GET /search
Search Books

**Required:**
- `query` (string) Example: `good thriller`

**Optional:**
- `page` (number, default: 1) Example: `1`
- `document_type` (string, default: any) — values: any, books, newspapers, magazines
- `view_type` (string, default: any) — values: any, preview_and_full_view, full_view
- `publication_year_from` (number)
- `publication_year_to` (number)
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** page_number (param: `page`)

> **Note:** `rating` and `isbn` are NOT returned in search results — they are only available via individual book detail lookups.

---

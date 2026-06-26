# realtime-image-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_image_search.yaml

**Host:** `real-time-image-search.p.rapidapi.com`
**Notes:** No pagination. Use 'limit' param to control total results returned (max 100).

## Endpoints

### GET /search
Search Images — Get real-time image search results from across the web. Supports all Google Images search filters.

**Required:**
- `query` (string) — Search query / keyword Example: `beach`

**Optional:**
- `limit` (integer, default: 10) Example: `10`
- `size` (string, default: any) — values: any, large, medium, icon, 400x300_and_more, 640x480_and_more, 800x600_and_more, 1024x768_and_more, 2mp_and_more, 4mp_and_more, 6mp_and_more, 8mp_and_more, 10mp_and_more, 12mp_and_more, 15mp_and_more, 20mp_and_more, 40mp_and_more, 70mp_and_more
- `color` (string, default: any) — values: any, red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown, full, transparent, grayscale
- `type` (string, default: any) — values: any, face, photo, clipart, lineart, animated
- `time` (string, default: any) — values: any, day, week, month, year
- `usage_rights` (string, default: any) — values: any, creative_commons, commercial
- `file_type` (string, default: any) — values: any, jpg, jpeg, png, gif, svg, webp, ico, raw
- `aspect_ratio` (string, default: any) — values: any, tall, square, wide, panoramic
- `country` (string) Example: `us`
- `safe_search` (string, default: blur) — values: off, blur, on
- `region` (string, default: us) Example: `us`
- `fields` (string) Example: `title,size,thumbnail_url,position`

**Pagination:** none
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** id, title, url, width, height, size, background_color, thumbnail_url, thumbnail_width, thumbnail_height, source, source_url, source_domain, position, rank, copyright, credits, license_link

---

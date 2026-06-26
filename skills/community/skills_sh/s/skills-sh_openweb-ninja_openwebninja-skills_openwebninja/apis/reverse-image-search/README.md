# reverse-image-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/reverse_image_search.yaml

**Host:** `reverse-image-search3.p.rapidapi.com`
**Notes:** Single-call API — pass an image URL and get up to 500 web pages that contain or are visually similar to the image. Use `limit` to control how many results are returned.

## Endpoints

### GET /reverse-image-search
Send an image URL and receive the top source web pages that contain or match the image.

**Required:**
- `url` (string) — Publicly accessible URL of the image to search Example: `https://example.com/image.jpg`

**Optional:**
- `limit` (integer, default: 500) — Number of results to return (1–500) Example: `50`
- `safe_search` (string) — Content filtering: `off` or `blur` (default: `off`) Example: `off`

**Pagination:** none
**Response path:** `data`
**Key fields:** title, link, domain, favicon, date, thumbnail, thumbnail_width, thumbnail_height

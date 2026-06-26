# realtime-lens-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_lens_data.yaml

**Host:** `real-time-lens-data.p.rapidapi.com`
**Notes:** No pagination. Use 'limit' param to control total results (max 500).

## Endpoints

### GET /search
Image Search

**Required:**
- `url` (string) — URL of an image with which to perform the search. Example: `https://i.imgur.com/HBrB8p0.png`

**Optional:**
- `query` (string) — Search query to further refine the results.
- `language` (string, default: en) Example: `en`
- `country` (string, default: us) Example: `us`

**Pagination:** none
**Response path:** `data`
**Key fields:** query, search_url, title, url, snippet, source, domain, position, rank

---

### GET /visual-matches
Visual Matches — Get visual matches from the web for an image and optionally a query. This endpoint implements the

**Required:**
- `url` (string) — URL of an image for which to get visual matches. Example: `https://i.imgur.com/HBrB8p0.png`

**Optional:**
- `query` (string) — Search query to further refine the results.
- `language` (string, default: en) Example: `en`
- `country` (string, default: us) Example: `us`

**Pagination:** none

---

### GET /exact-matches
Exact Matches — Send an image URL and get the top 500 web pages with the same image (reverse image search). This endpoint implements the

**Required:**
- `url` (string) — URL of the image for which to find sources Example: `https://i.imgur.com/HBrB8p0.png`

**Optional:**
- `limit` (string, default: 500) Example: `10`
- `safe_search` (string, default: blur) — values: off, blur

**Pagination:** none
**Page size param:** `limit` (default: 500)

---

### GET /object-detection
Object Detection — Detect landmarks, places, plants, animals, products, and other objects in an image, including bounding boxes, labels / types and confidence score.

**Required:**
- `url` (string) — URL of an image to perform Google Lens object detection. Example: `https://thumbs.dreamstime.com/b/giraffe-zebra-1533191.jpg`

**Pagination:** none

---

### GET /ocr
Image to Text (OCR) — Extract text from an image and get paragraph, sentence and word level text detections from Google Lens.

**Required:**
- `url` (string) — URL of an image from which to extract text. Example: `https://s3-us-west-2.amazonaws.com/courses-images/wp-content/uploads/sites/1844/2017/06/15213029/images-textwrap-topbottom.png`

**Optional:**
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** box, sentences

---

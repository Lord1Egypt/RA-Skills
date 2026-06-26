# realtime-news-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_news_data.yaml

**Host:** `real-time-news-data.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param. Use 'limit' param to control page size.

## Endpoints

### GET /search
Search — Search news articles by query with an option to limit the results to a specific time range.

**Required:**
- `query` (string) — Search query for which to get news. Example: `Elon Musk`

**Optional:**
- `limit` (integer, default: 10) Example: `10`
- `time_published` (string, default: anytime) — values: anytime, 1h, 1d, 7d, 1m, 1y Example: `anytime`
- `source` (string) Example: `cnn.com`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Page size param:** `limit` (default: 10)

---

### GET /top-headlines
Top Headlines — Get the latest news headlines/top stories for a country.

**Optional:**
- `limit` (integer, default: 500) Example: `500`
- `country` (string) Example: `US`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Page size param:** `limit` (default: 500)

---

### GET /topic-headlines
Topic Headlines — Get the latest news headlines for a topic (World,  Sports, Technology, etc) or publication (e.g. CNN, BBC, etc).

**Required:**
- `topic` (string) Example: `WORLD`

**Optional:**
- `limit` (integer, default: 500) Example: `500`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Page size param:** `limit` (default: 500)

---

### GET /topic-news-by-section
Topic News By Section — Get news article in a specific section of a topic (World,  Sports, Technology, etc) or publication (CNN, BBC, etc).

**Required:**
- `topic` (string) Example: `WORLD`

**Optional:**
- `section` (string) Example: `CAQiSkNCQVNNUW9JTDIwdk1EZGpNWFlTQldWdUxVZENHZ0pKVENJT0NBUWFDZ29JTDIwdk1ETnliSFFxQ2hJSUwyMHZNRE55YkhRb0FBKi4IACoqCAoiJENCQVNGUW9JTDIwdk1EZGpNWFlTQldWdUxVZENHZ0pKVENnQVABUAE`
- `limit` (integer, default: 500) Example: `500`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Page size param:** `limit` (default: 500)

---

### GET /local-headlines
Local Headlines (Geo) — Get local, geo based headlines.

**Required:**
- `query` (string) — Area, city or country to fetch news for (e.g. London). Example: `New York`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `limit` (integer, default: 500) Example: `500`

**Pagination:** none
**Page size param:** `limit` (default: 500)

---

### GET /full-story-coverage
Full Story Coverage — Get the full story coverage, including all sub articles, top news, and posts from X (formerly Twitter).

**Required:**
- `story` (string) Example: `CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pzbFA3X0N4RjlDUlpVVnhudXBpZ0FQAQ`

**Optional:**
- `sort` (string) — values: RELEVANCE, DATE

**Pagination:** none
**Response path:** `data`
**Key fields:** title, link, snippet, photo_url, thumbnail_url, published_datetime_utc, source_url, source_name, source_logo_url, source_favicon_url, source_publication_id, post_id, photo, post_author_username, post_author_picture, post_datetime_utc

---

### GET /language-list
Language List — Get valid languages for a country code, to be used with all other APIs.

**Required:**
- `country` (string) — Country code of the country to get languages for. See all available country codes. Example: `us`

**Pagination:** none
**Response path:** `data`
**Key fields:** name, lang

---

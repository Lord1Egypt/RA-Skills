# ai-overviews

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_web_search.yaml

**Host:** `real-time-web-search.p.rapidapi.com`
**Notes:** The `/ai-overviews` endpoint is part of the **realtime-web-search** API. This folder documents the endpoint and provides usage recipes. Use `apis/realtime-web-search/scrape.js` with `--endpoint /ai-overviews` to access it — no separate scrape.js is needed.

## Endpoints

### GET /ai-overviews
Fetch Google AI Overview content for a search query. Returns the structured AI-generated summary that Google shows at the top of search results for eligible queries.

**Required:**
- `q` (string) Example: `what is the speed of light`

**Optional:**
- `gl` (string, default: us) — Country code (ISO 3166-1 alpha-2) Example: `us`
- `hl` (string, default: en) — Language code (ISO 639-1 alpha-2) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** text_parts, reference_links, url, snippet, source, displayed_link, position, rank, answers_count, top_answer, date

## Usage

Use the realtime-web-search scrape.js:

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-overviews --query "your question here" --dry-run
```

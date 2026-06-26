# google-ai-mode

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_web_search.yaml

**Host:** `real-time-web-search.p.rapidapi.com`
**Notes:** The `/ai-mode` endpoint is part of the **realtime-web-search** API. This folder documents the endpoint and provides usage recipes. Use `apis/realtime-web-search/scrape.js` with `--endpoint /ai-mode` to access it — no separate scrape.js is needed. Supports multi-turn conversations via `session_token`.

## Endpoints

### GET /ai-mode
Generate a structured AI response from Google's AI Mode for a given prompt. Returns reply parts (headings, paragraphs, lists, images) with source attribution.

**Required:**
- `prompt` (string) Example: `How to make a pizza step by step?`

**Optional:**
- `session_token` (string) — Token to continue a previous conversation session Example: `abc123`
- `gl` (string, default: us) — Country code (ISO 3166-1 alpha-2) Example: `us`
- `hl` (string, default: en) — Language code (ISO 639-1 alpha-2) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** reply_parts (heading, paragraph, list, image), reference_links (title, url, source)

## Usage

Use the realtime-web-search scrape.js:

```bash
node --env-file=.env openwebninja_universal_scraper/apis/realtime-web-search/scrape.js \
  --endpoint /ai-mode --query "your prompt here" --dry-run
```

---
name: webcrawlerapi
description: "Scrape a single page or crawl a full website using WebCrawlerAPI. Trigger for: fetching page content, getting markdown from a URL, scraping a page, crawling a website/domain, websearch, webfetch."
---

# WebCrawlerAPI Skill

Use WebCrawlerAPI to get page content as markdown (single page scrape) or crawl entire websites (multi-page).

## Setup — API Key

The API key must be set as an environment variable before running any curl commands:

```bash
export WEBCRAWLERAPI_API_KEY="your_api_key"
```

Get your key:
1. Go to https://webcrawlerapi.com/
2. Sign up at https://dash.webcrawlerapi.com/
3. Visit https://dash.webcrawlerapi.com/access
4. Copy your API key

If `WEBCRAWLERAPI_API_KEY` is not set, stop and ask the user to set it before proceeding.

## Decision: Scrape vs Crawl

**Scrape** (single page) — default when user asks for:
- Content/markdown of a specific page or URL
- "Get me this page", "scrape this URL", "what does this page say"
- No mention of "website", "full site", "all pages", "crawl"

**Crawl** (multi-page) — when user asks for:
- "Crawl this website", "get all pages from", "full website content"
- Mentions a domain broadly (not a specific path)
- Wants multiple pages

---

## Scrape — Single Page

Use `POST /v2/scrape`. Synchronous — result is returned immediately.

```bash
curl --fail --silent --show-error \
  --request POST \
  --url "https://api.webcrawlerapi.com/v2/scrape" \
  --header "Authorization: Bearer ${WEBCRAWLERAPI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "<URL>",
    "output_formats": ["markdown"]
  }'
```

### Scrape Response

The response contains `markdown` field directly — no polling needed:

```json
{
  "success": true,
  "status": "done",
  "markdown": "## Page Title\n\nPage content...",
  "page_status_code": 200,
  "page_title": "Page Title"
}
```

### On success

Output the markdown content directly to the user. No need to save to files for scrape.

### On failure

If `success` is `false`, show the `error_code` and `error_message` to the user.

---

## Crawl — Full Website

Use `POST /v1/crawl`. Asynchronous — returns a job ID, then poll for results.

### Step 1: Start the crawl

```bash
curl --fail --silent --show-error \
  --request POST \
  --url "https://api.webcrawlerapi.com/v1/crawl" \
  --header "Authorization: Bearer ${WEBCRAWLERAPI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "<URL>",
    "items_limit": 25,
    "output_formats": ["markdown"]
  }'
```

Response:
```json
{ "id": "<JOB_ID>" }
```

### Step 2: Poll job status (background loop)

Use a background Bash job to poll every 10 seconds until `status` is `done` or `error`:

```bash
JOB_ID="<JOB_ID>"
while true; do
  RESULT=$(curl --fail --silent --show-error \
    --request GET \
    --url "https://api.webcrawlerapi.com/v1/job/${JOB_ID}" \
    --header "Authorization: Bearer ${WEBCRAWLERAPI_API_KEY}")
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Job status: $STATUS"
  if [ "$STATUS" = "done" ] || [ "$STATUS" = "error" ]; then
    echo "$RESULT"
    break
  fi
  sleep 10
done
```

### Step 3: Download and save results

When job is `done`, for each `job_item` with `status: done`:
- Fetch the content from `markdown_content_url`
- Save to `.webcrawlerapi/<hostname>/<sanitized-path>.md`

```bash
mkdir -p ".webcrawlerapi/<hostname>"

# For each job_item, fetch markdown_content_url and save:
curl --silent "<markdown_content_url>" \
  --output ".webcrawlerapi/<hostname>/<sanitized-filename>.md"
```

Sanitize filenames: replace `://`, `/`, `?`, `#`, `:` with `_`. Trim leading underscores.

### Step 4: Report to user

After saving, tell the user:
- Total pages crawled
- How many succeeded vs failed
- Where files were saved: `.webcrawlerapi/<hostname>/`
- List the saved files

---

## Notes

- Default `items_limit` for crawl: 25 (ask user if they want more)
- For scrape, just output the markdown — don't save to disk
- For crawl, always save to `.webcrawlerapi/` directory in current working dir
- If the job returns `error` status, show `last_error` from job items and the job-level error if present
- Never hardcode the API key — always use `${WEBCRAWLERAPI_API_KEY}`

# Crawler Tools — Detailed Guide

Three MCP tools for managing site-wide crawl jobs.

## Contents
- [crawler_job_start](#tool-crawler_job_start) — initiate a crawl (URL regex, depth, budget, schedule)
- [crawler_job_status](#tool-crawler_job_status) — check crawl progress
- [crawler_job_delete](#tool-crawler_job_delete) — cancel and delete a crawl
- [Typical Workflow](#typical-workflow)
- [Best Practices](#best-practices)

## Tool: `crawler_job_start`

Initiates a crawl that discovers and scrapes pages starting from a base URL.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `startUrl` | string | Yes | Starting URL for the crawl |
| `urlRegexpInclude` | string | Yes | Regex to match URLs to crawl (see patterns below) |
| `maxDepth` | number | One required | Max crawl depth (start URL = depth 0) |
| `crawlBudget` | number | One required | Max credits the job may consume |
| `urlRegexpExclude` | string | No | Regex to exclude URLs from crawling |
| `apiParams` | object | No | Scrape config per page: `country_code`, `render`, `premium`, `ultra_premium`, `device_type`, `output_format` |
| `callbackUrl` | string | No | Webhook URL for results and completion (see data-flow note below) |
| `additionalData` | object | No | Custom metadata attached to the job |
| `schedule` | object | No | Recurring schedule config (see below) |
| `enabled` | boolean | No | Whether the job is active (default: true) |

### callbackUrl — Data-Flow Warning

When `callbackUrl` is set, ScraperAPI sends all crawled page results to that URL as POST requests. **Before setting a callbackUrl, confirm with the user:**

1. **Who controls the endpoint** — scraped data (which may include PII, proprietary content, or sensitive page data) will be sent to this URL.
2. **Data exposure** — results are transmitted over the network to the callback endpoint; ensure the endpoint uses HTTPS.
3. **Volume** — a crawl can produce hundreds or thousands of result payloads depending on `crawlBudget` and `maxDepth`.

Never set `callbackUrl` without explicit user approval.

### URL Regex Patterns

The `urlRegexpInclude` regex **must** use named capture groups:
- `(?<full_url>...)` for absolute URLs
- `(?<relative_url>...)` for relative URLs

**Common patterns:**

```
# All pages on a domain
(?<full_url>https?://example\.com/.*)

# Only blog posts
(?<full_url>https?://example\.com/blog/.*)

# Only HTML pages (exclude files)
(?<full_url>https?://example\.com/[^.]*$)

# Relative URLs from a docs site
(?<relative_url>/docs/.*)
```

**Exclusion patterns (`urlRegexpExclude`):**

```
# Exclude PDFs and images
.*\.(pdf|png|jpg|jpeg|gif|svg|zip)

# Exclude admin/auth pages
.*(login|admin|signup|auth).*
```

### Depth vs Budget

- **`maxDepth`**: Controls how many link-hops from the start URL. Depth 0 = start URL only, depth 1 = start URL + pages linked from it, etc.
- **`crawlBudget`**: Controls maximum credit spend. Safer for cost control.
- **Must provide at least one.** Providing both applies whichever limit is hit first.

Guidance:
- Small site or specific section → `maxDepth: 2–3`
- Unknown site size → use `crawlBudget` to cap costs
- Both → `maxDepth: 3` + `crawlBudget: 500` for controlled exploration

### Schedule Configuration

If **no `schedule` is provided**, the crawler performs a **single one-time crawl** and stops once all matching pages are scraped.

If a **`schedule` is provided**, the crawler runs repeatedly on the configured interval. Each iteration's progress and results can be viewed in the **ScraperAPI Dashboard** (dashboard.scraperapi.com).

```json
{
  "name": "daily-docs-crawl",
  "interval": "daily"
}
```

Available intervals: `"once"`, `"hourly"`, `"daily"`, `"weekly"`, `"monthly"`.
Alternative: use `"cron"` field with a cron expression instead of `"interval"`.

### apiParams

Controls how each discovered page is scraped:

```json
{
  "render": true,
  "premium": false,
  "country_code": "us",
  "device_type": "desktop",
  "output_format": "markdown"
}
```

Note: `apiParams` uses **snake_case** keys (matching the underlying API), not camelCase.

---

## Tool: `crawler_job_status`

Check progress of a running crawl job.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jobId` | string | Yes | Job ID returned by `crawler_job_start` |

### Response

Returns job metrics: done count, failed count, active pages, overall status.

---

## Tool: `crawler_job_delete`

Cancel and delete a crawl job. This is **destructive** — the job and its data are removed.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jobId` | string | Yes | Job ID to cancel and delete |

---

## Typical Workflow

1. **Start**: `crawler_job_start` with `startUrl`, `urlRegexpInclude`, and `maxDepth` or `crawlBudget`
2. **Monitor**: `crawler_job_status` with the returned `jobId` to track progress
3. **Cancel if needed**: `crawler_job_delete` if the crawl is consuming too many credits or going off-track

## Best Practices

- **Always set `crawlBudget`** even if using `maxDepth` — this prevents runaway costs on large sites.
- **Be specific with `urlRegexpInclude`** — broad patterns like `.*` will crawl the entire internet following external links.
- **Use `urlRegexpExclude`** to skip binary files, auth pages, and irrelevant sections.
- **Test with low `maxDepth` first** (1–2) to validate your regex patterns before a full crawl.
- **Enable `render` in `apiParams`** only if the site is JS-rendered — it multiplies credit cost per page.
- **Consider webhooks** (`callbackUrl`) for long-running crawls instead of polling `crawler_job_status` repeatedly — but only with explicit user approval (see data-flow warning above).

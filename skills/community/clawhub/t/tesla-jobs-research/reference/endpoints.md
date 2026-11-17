# tesla-jobs-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**2 endpoints across 1 platform group(s).**

## Tesla Jobs (2)

### `tesla_jobs_job`

- **HTTP:** `GET /tesla-jobs/job`
- **What:** Tesla Jobs single posting. Returns one Tesla Careers posting by its numeric job id (the `id` field returned by the list endpoint).
- **Params:** `id` (string, **required**) — Tesla job id

### `tesla_jobs_list`

- **HTTP:** `GET /tesla-jobs/list`
- **What:** Tesla Jobs listing. Searches Tesla's public careers site (tesla.com/careers) via its own careers-state JSON endpoint. Tesla's own endpoint always returns its entire global job dataset regardless of query parameters; this filters and paginates that snapshot server-side. Listings carry identity/department/location metadata only — call the job endpoint for the full description, responsibilities, and requirements.
- **Params:** `location` (string, optional) — Filter by location, case-insensitive substring match; `page` (integer, optional) — Page number, 1-based; `page_size` (integer, optional) — Results per page, up to 100; `query` (string, optional) — Filter by title or department, case-insensitive substring match

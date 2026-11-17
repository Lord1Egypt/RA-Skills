# upwork-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Upwork (3)

### `upwork_freelancer`

- **HTTP:** `GET /upwork/freelancer/{id}`
- **What:** Get Upwork freelancer profile. Returns an Upwork freelancer profile: name, title, verification badge, overview, hourly rate, rating and review count, Job Success Score, location and local time, total jobs/hours worked, and recent client feedback (title, comment, date, client name, rating).
- **Params:** `id` (string, **required**) — Upwork freelancer id, the value after \

### `upwork_job`

- **HTTP:** `GET /upwork/job/{id}`
- **What:** Get Upwork job posting detail. Returns an Upwork job posting: title, full description, employment type, budget (hourly range or fixed amount), location/remote type, experience level, duration, project type, proposal count, allowed applicant countries, and a summary of the posting client (member since, location, total spend, hires, hours, industry, company size).
- **Params:** `id` (string, **required**) — Upwork job id, e.g. from a search result's id field

### `upwork_search`

- **HTTP:** `GET /upwork/search`
- **What:** Search Upwork job postings. Searches Upwork's public job listings by free-text keyword, returning job summaries (title, budget, experience level, duration, posted date, description snippet, skill tags).
- **Params:** `page` (integer, optional) — 1-based result page. Defaults to 1.; `q` (string, **required**) — Free-text job search keyword

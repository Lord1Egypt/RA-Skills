# website-monitoring — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## Monitors (6)

### `monitors_checks`

- **HTTP:** `GET /monitors/{id}/checks`
- **What:** List a monitor's check history. Returns the caller's own monitor's most recent check runs (most recent first, capped at 50), including webhook delivery status per run.
- **Params:** `id` (string, **required**) — Monitor ID returned by your account monitor create/list response; replace the illustrative example with your own ID

### `monitors_create`

- **HTTP:** `POST /monitors`
- **What:** Create a website-change monitor. Creates a monitor that periodically checks a page or sitemap for changes and can notify a webhook. Free to call -- only completed check runs consume credits, at 1 credit per completed run regardless of target type or whether a change was detected. `target_type` defaults to "page" (exact-fingerprint diff of the page). "sitemap" watches the sitemap at `url` for added/removed entries instead, honoring `sitemap.include_patterns`/`exclude_patterns` (shell-style globs matched against each URL's path) and `sitemap.max_urls` (default 5000, hard cap 10000).
- **Params:** `request` (object, **required**) — Monitor definition
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `monitors_delete`

- **HTTP:** `DELETE /monitors/{id}`
- **What:** Delete a website-change monitor. Deletes one website-change monitor by its `id`, which must belong to the calling account. Returns `deleted: true` on success. The monitor's past check history is not removed.
- **Params:** `id` (string, **required**) — Monitor ID returned by your account monitor create/list response; replace the illustrative example with your own ID

### `monitors_get`

- **HTTP:** `GET /monitors/{id}`
- **What:** Get a website-change monitor. Returns one of your website-change monitors by `id`. The monitor includes its `target_type` (`page` or `sitemap`), URL, name, check cadence in minutes, enabled flag, last and next check times, failure count and last error, plus notification and sitemap settings.
- **Params:** `id` (string, **required**) — Monitor ID returned by your account monitor create/list response; replace the illustrative example with your own ID

### `monitors_list`

- **HTTP:** `GET /monitors`
- **What:** List website-change monitors. Lists the website-change monitors on your account, most recently created first, up to 100. Each monitor has its `target_type` (`page` or `sitemap`), URL, name, cadence in minutes, enabled flag, last checked and last changed times, next check time, failure count, last error, and notification and sitemap settings.
- **Params:** _none_

### `monitors_update`

- **HTTP:** `PATCH /monitors/{id}`
- **What:** Update a website-change monitor. Partially updates one of the caller's own monitors. Free to call. Changing `target_type` or `sitemap` resets the stored diff baseline (fingerprint, snapshot, or URL set), so the next check establishes a fresh baseline instead of comparing against a now-meaningless prior state.
- **Params:** `id` (string, **required**) — Monitor ID returned by your account monitor create/list response; replace the illustrative example with your own ID; `request` (object, **required**) — Fields to update
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

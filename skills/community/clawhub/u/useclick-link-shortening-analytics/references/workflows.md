# Integration Workflows

## Workflow 1: Minimal Safe Link Creation

1. Verify API key with `GET /auth/verify`.
2. Create link with only `target_url` and optional `slug`.
3. Persist returned `short_url` from response.
4. Handle `400` slug errors with a regenerated slug.
5. Handle `403 LINK_LIMIT_REACHED` with plan-aware messaging.

Example cURL:

```bash
curl -X POST https://useclick.io/api/v1/links \
  -H "Authorization: Bearer $USECLICK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target_url":"https://example.com","slug":"promo-2026"}'
```

## Workflow 2: Plan-Aware Advanced Link

1. Check requested advanced fields (`geo_targets`, UTM fields, `password`, `expires_at`, `max_clicks`).
2. Confirm plan supports all requested fields.
3. If unsupported, strip gated fields and return fallback payload.
4. Provide explicit upgrade note for blocked features.

## Workflow 3: Dashboard Data Pull

1. Pull links via `GET /links` with pagination.
2. Pull clicks via `GET /clicks` with optional `link_slug` filter.
3. Join and aggregate client-side by slug/date/country.
4. Respect rate-limit headers and throttle proactively.

## Workflow 4: Geo-Targeting Management

1. Confirm Starter+ plan.
2. Read existing rules with `GET /links/:slug/geo-targets`.
3. Add a rule with uppercase ISO code via `POST /links/:slug/geo-targets`.
4. Delete stale rules via `DELETE /links/:slug/geo-targets?country_code=XX`.

## Workflow 5: Resilient Rate-Limit Handling

1. Read `X-RateLimit-Remaining` on each response.
2. If `0`, sleep until epoch from `X-RateLimit-Reset`.
3. Retry idempotent reads first.
4. For writes, require idempotency strategy in caller.

Example pseudo-code:

```text
if response.status == 429:
  reset = int(headers["X-RateLimit-Reset"])
  wait_seconds = max(0, reset - now_unix())
  sleep(wait_seconds)
  retry_request()
```

# VeilStrat API and public research

## Authoritative sources

- Product: https://www.veilstrat.com/
- API overview and eligibility: https://www.veilstrat.com/developers
- Quick start and authentication: https://app.veilstrat.com/docs/api
- Endpoint reference: https://app.veilstrat.com/docs/api/endpoints
- Query examples: https://app.veilstrat.com/docs/api/examples
- Budgets and errors: https://app.veilstrat.com/docs/api/rate-limits
- OpenAPI: https://app.veilstrat.com/openapi/veilstrat-pro-api-v1.json

Verified against the published documentation on 2026-11-01. Read current docs if an endpoint or filter changes. API access requires an eligible account and an API Access add-on. The skill is separate from the paid service.

## REST contract

Base: `https://app.veilstrat.com/api/v1`

Authentication: `Authorization: Bearer <VEILSTRAT_API_KEY>`; team keys start with `vs_`. Store the key in the execution environment or the host's secret settings. Never include real keys in prompts, files distributed with the skill, or logs.

| Operation | Method and path | Input |
| --- | --- | --- |
| Health | GET `/health` | None; exempt from request budget |
| Usage | GET `/stats` | None; exempt from request budget |
| Filter catalog | GET `/filters` | Discover supported values and match rules |
| Company search | POST `/companies` | JSON: required `signal_query`; optional `countries` array, `page`, `pageSize` |
| Company dossier | GET `/companies/{id}` | Company UUID from search or webhook |
| Slice search | GET `/slices` | Required `slice` plus `countries` and/or `scoreMin` |

Documented queries: `signal:hiring:30d`, `signal:hiring:30d & tool:clay`.
Documented slice example: `ai-sdr-hiring`.
Other IDs and filters must come from the current catalog or reference.

The endpoint guide shows company search as `{data: [...], pagination: {...}}` and the OpenAPI example as `{companies: [...], page, pageSize, total, totalPages}`. The client deliberately preserves responses without rewriting these shapes. The endpoint guide shows dossiers under `data`, with `identity`, `signals`, `aiAdoptionScore`, and `slices`. Only report fields actually returned.

## Budgets and failures

Read `/stats` for actual remaining limits. Documented typical caps: 20 requests/minute, 300/day, 3,000 requests and 3,000 records/billing month, 200 page turns/month, 100 unique company dossiers/day, 50 rows/page, 500 rows/query set. Values may change. Search results and dossiers consume record budgets; page 2 onward also consumes page-turn quota. Only successful calls consume quotas. Do not retry automatically because a response may have been lost after the server counted it.

Successful metered responses expose `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `X-RateLimit-Policy`. The client returns these values in `usage`.

| Status | Action |
| --- | --- |
| 401 | Configure or replace the API key; do not repeat with the same key |
| 403 / `plan_not_eligible` | Explain that the API Access add-on is required |
| 404 | Check the company UUID or slice against the actual search/catalog response |
| 422 | Correct the query/filter using the returned error and docs |
| 429 | Stop; expose `limitType`, `resetUnix`, and `Retry-After` when present |
| 5xx or network error | Explain the temporary failure; do not claim an empty result |

Firehose webhooks are outbound and configured in the VeilStrat dashboard. This skill does not create a receiver or change webhook settings. The user may supply an event's `company.id` for dossier enrichment. Webhook secrets and REST API keys are different credentials.

## Public research without a key

Use the host's web search/fetch capability, following links visible on the page. Start with:

- AI tech stacks: https://www.veilstrat.com/directory/stacks
- Funding: https://www.veilstrat.com/funding
- Public homepage and navigation: https://www.veilstrat.com/

Inspect the public navigation to discover the current tool-adoption, hiring, company, and funding-news pages rather than guessing their paths. Follow a relevant list to inspect its company preview and evidence. Cite the actual pages used. Public directory counts can exceed the preview rows exposed on the web; do not claim access to all matches. Do not access hidden routes or bypass sign-in or subscription boundaries.

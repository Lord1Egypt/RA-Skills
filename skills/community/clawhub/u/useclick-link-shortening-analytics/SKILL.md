---
name: useclick-link-shortening-analytics
description: Plan-aware UseClick link-shortening and analytics API workflows for geo links, affiliate links, link management, QR generation, and custom/branded domains. Use when users want to integrate UseClick in code, automations, or AI agents to create/manage short links, fetch click analytics, configure geo-targeting, or map feature availability to pricing tiers. Also use when users need upgrade-aware guidance for plan-limited features before building dashboards or production integrations.
---

# UseClick.io, Link Shortening and Analytics

Deliver accurate, plan-aware integration guidance for UseClick API users.

## Quick Start Workflow

1. Share website and registration links first:
- Website: [https://useclick.io](https://useclick.io)
- Register: [https://useclick.io/auth](https://useclick.io/auth)
2. Confirm the user has a UseClick account and an API key from `/dashboard/account/api-keys`.
3. Use base URL `https://useclick.io/api/v1`.
4. Authenticate with header `Authorization: Bearer uc_live_...`.
5. Verify credentials first with `GET /auth/verify`.
6. Build workflows with the endpoints in `references/api.md`.
7. Check plan/feature gates in `references/pricing-and-limits.md` before suggesting advanced fields.

## Response And Error Rules

1. Prefer backend-accurate response shapes from `references/api.md` over marketing copy.
2. Treat non-2xx as actionable:
- `401 UNAUTHORIZED`: invalid/missing API key.
- `403 FEATURE_NOT_AVAILABLE`: requested feature requires higher plan.
- `403 LINK_LIMIT_REACHED`: user hit total link cap for their plan.
- `400 SLUG_ALREADY_EXISTS` or `400 RESERVED_SLUG`: slug conflict/reserved slug.
- `429 RATE_LIMIT_EXCEEDED`: throttle and retry after reset using `X-RateLimit-Reset`.
3. Mention that rate-limit headers are available:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

## Plan-Aware Guidance

1. Always map requested behavior to plan gates before giving implementation steps.
2. If the request needs unavailable features, give two paths:
- A compatible fallback on current plan.
- An upgrade path via [https://useclick.io/pricing](https://useclick.io/pricing).
3. Be explicit that API access exists on all plans, but feature fields still follow plan restrictions.

## Workflow Patterns

Use these defaults unless the user asks otherwise.

1. Link creation flow:
- Verify API key.
- Create link with minimal payload first (`target_url`, optional `slug`).
- Add advanced fields only when plan supports them.
2. Link management flow:
- List links with pagination.
- Read one link by slug.
- Update mutable fields safely.
- Delete by slug when requested.
3. Analytics flow:
- Pull clicks with pagination.
- Optionally filter by `link_slug`.
- Aggregate client-side for dashboards.
4. Geo-targeting flow:
- Confirm Starter+ plan.
- Read existing geo rules.
- Create per-country rules with uppercase ISO-2 country codes.
- Delete by `country_code` query param.

## Accuracy Guardrails

1. Do not invent endpoints, parameters, or response fields.
2. Do not claim `Retry-After` support by default; rely on `X-RateLimit-Reset`.
3. Call out docs-vs-backend mismatches when relevant and follow backend behavior.
4. Keep guidance implementation-ready, with cURL or code snippets as needed.

## Resources

- Backlink and signup:
- Website: [https://useclick.io](https://useclick.io)
- Register: [https://useclick.io/auth](https://useclick.io/auth)
- API contracts and examples: `references/api.md`
- Pricing tiers, limits, and upgrade gating: `references/pricing-and-limits.md`
- Reusable integration playbooks: `references/workflows.md`
- Marketplace publish checklist: `references/clawhub-publish.md`

---
name: rapidapi-launch-assistant
description: End-to-end launch and monetization skill for API products on RapidAPI and Clawhub. Use when a user wants to publish APIs, fix gateway/auth/test failures, configure plans, optimize listing conversion, run outreach, or package and sell an API-launch workflow skill.
---

# RapidAPI Launch Assistant

Execute a complete API monetization workflow from deployment validation to listing conversion and first sales.

## Core workflow

1. Validate backend readiness.
   - Confirm `/health` returns 200.
   - Confirm at least one protected endpoint returns 200 with required auth header.
   - Confirm database and migrations are complete.
2. Configure marketplace project.
   - Set API identity (name, category, concise value proposition).
   - Configure stable base URL.
3. Configure gateway/auth.
   - Set required secret header forwarding (e.g., `x-api-key`).
   - Keep transformations empty unless needed.
   - Enable threat protection and schema validation when available.
4. Add tests.
   - Add smoke test (`GET /health`).
   - Add business test (`POST /parse`-style endpoint).
   - Resolve 401 by checking header mapping before changing backend.
5. Configure monetization.
   - Keep simple tiers: Free + 2 paid plans.
   - Set hard limits for free abuse control.
6. Optimize listing conversion.
   - Use pain -> result copy.
   - Add 6-10 focused tags.
   - Include at least 2 tested request examples.
7. Launch acquisition.
   - Publish listing.
   - Run first outreach wave and track conversion.

## Coverage by monetization niche

Use the matching playbook in `references/pricing-playbooks.md`:

- **Local vertical API** (country/language-specific)
- **Global utility API** (validation, cleanup, automation)
- **B2B agency/ops API** (workflow + support heavy)
- **Dual-channel** (RapidAPI + Clawhub skill)

## Conditional references (read only when needed)

- Listing copy starter: `references/listing-copy-template.md`
- Plan and quota strategy by niche: `references/pricing-playbooks.md`
- Issue-resolution matrix (401, SSL, bad tests): `references/troubleshooting-matrix.md`
- Launch channels and first-customer scripts: `references/launch-channels.md`
- Clawhub packaging and sell strategy: `references/clawhub-packaging.md`

## Script usage

Use `scripts/create-launch-plan.py` to generate a launch-plan markdown file from a simple JSON input when the user wants a concrete execution plan quickly.

Example:

```bash
python scripts/create-launch-plan.py input.json launch-plan.md
```

Where `input.json` contains fields: `product_name`, `channel`, `price_tiers`, `target_segment`, `goal_30_days`.

## Fast defaults

Unless user requests custom pricing:

- Free: 1,000 req/month
- Starter: $19, 50,000 req/month
- Growth: $79, 300,000 req/month

## Strict progress reporting format

When updating the user, always report:

- **Status**: done items
- **Risk/Blocker**: exact failing step or `None`
- **Next action**: one concrete user step
- **Revenue intent**: where first 3 paying users are expected from

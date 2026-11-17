---
name: uberfix-catalog
description: Browse UberFix service types and categories using existing tools.
---

# UberFix Service Catalog

Use this skill when a user asks what maintenance services UberFix offers, or wants category options before submitting a request.

## Tools

- `uberfix_list_services`: available service labels are currently produced by the bot engine's `SERVICE_TYPE_LABELS` in `_shared/core/bot.ts`; they are not guaranteed to reflect rows in `public.services`.
- `uberfix_list_categories`: categories from `maintenance_categories`, with a code-defined fallback when none exist.

Never assume a service price or guarantee availability from the category list. Call actual tools and report their output; the live `services` table had 463 rows at inspection time, but the operational tool returns a fixed label list rather than those rows. For creating a request, follow the UberFix Maintenance skill.

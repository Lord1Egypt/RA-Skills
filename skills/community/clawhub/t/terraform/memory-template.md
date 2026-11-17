# Memory Template — Terraform

Create `~/Clawic/data/terraform/memory.md` with this structure:

```markdown
# Terraform Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Their stacks and how state is split; where apply happens (laptop, CI, managed platform) -->
<!-- CLI version, provider majors in use, wrappers if any -->

## Incidents
<!-- What has already bitten them: stuck locks, a destroy, a bad provider upgrade -->

## Preferences
<!-- Appetite for state surgery vs declarative blocks -->
<!-- Output format: how much plan detail to surface beyond plan_summary_detail; proactive warnings vs on-demand -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their stack layout |
| `complete` | Know their states, pipeline, and constraints |

Never record credentials, role ARNs, account IDs, or state bucket names with access details. Preferences only.

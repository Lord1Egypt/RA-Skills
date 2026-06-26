# Memory Template — Yelp

Create `~/yelp/memory.md` with this structure:

```markdown
# Yelp Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Preferred mode: api | page | hybrid
- Typical markets or cities
- Common categories: restaurants | cafes | bars | beauty | home services | mixed
- Price posture and minimum quality floor

## Operational Readiness
- API key available: yes | no
- Public-page mode acceptable: yes | no
- Known blockers: unsupported endpoint, ambiguous business, stale data, no reviews

## Acceptance Patterns
- Option patterns repeatedly accepted
- Why they worked

## Rejection Patterns
- Option patterns repeatedly rejected
- Why they failed

## Notes
- Reusable shortlist or audit guidance for future Yelp tasks

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Preferences still evolving | Keep learning from each Yelp task |
| `complete` | Stable decision profile | Prioritize known defaults |
| `paused` | User wants minimal setup | Avoid extra discovery prompts |
| `never_ask` | User requested no setup prompts | Follow only explicit instructions |

## Rules

- Keep notes in natural language.
- Update `last` on each meaningful interaction.
- Store reasons, not only final picks.
- Never remove historical patterns without user approval.

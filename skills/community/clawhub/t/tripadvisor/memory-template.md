# Memory Template — Tripadvisor

Create `~/tripadvisor/memory.md` with this structure:

```markdown
# Tripadvisor Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Preferred mode: api | ui | hybrid
- Typical trip intents: hotels | restaurants | attractions | mixed
- Budget posture and quality floor

## Operational Readiness
- API key available: yes | no
- Browser mode preferred: yes | no
- Known blockers (consent, anti-bot, endpoint errors)

## Acceptance Patterns
- Option patterns repeatedly accepted
- Why they worked

## Rejection Patterns
- Option patterns repeatedly rejected
- Why they failed

## Notes
- Reusable constraints for future shortlist generation

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Preferences still evolving | Keep learning from each query |
| `complete` | Stable decision profile | Prioritize known defaults |
| `paused` | User wants minimal setup | Avoid extra discovery prompts |
| `never_ask` | User requested no setup prompts | Follow explicit instructions only |

## Rules

- Keep notes in natural language.
- Update `last` on each meaningful interaction.
- Store reasons, not only outcomes.
- Never remove historical patterns without user approval.

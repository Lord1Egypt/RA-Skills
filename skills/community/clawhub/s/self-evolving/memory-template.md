# Memory Template — Self-Evolving

Create `~/self-evolving/memory.md` with this structure:

```markdown
# Self-Evolving Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | paused | never_ask

## Context
- Repeated workflows where evolution is useful
- What "better" means for this user
- Situations where experimentation should always or never happen

## Stable Winners
- Proven rules promoted after repeated success

## Guardrails
- Hard limits, banned mutations, risky surfaces to avoid

## Notes
- Internal observations worth retesting later

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Gather context opportunistically |
| `complete` | Enough context exists | Use current rules and update only on change |
| `paused` | User said not now | Do not push for more setup detail |
| `never_ask` | User opted out | Never request extra evolution context |

## Key Principles

- Keep the memory short enough to load before non-trivial work
- Promote only repeated winners; everything else stays tentative
- Write natural language observations, not config-style keys
- Update `last` every time the skill is used

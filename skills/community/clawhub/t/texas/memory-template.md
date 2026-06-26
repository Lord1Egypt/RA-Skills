# Texas Memory

Create `~/texas/memory.md` with this structure only if the user wants continuity across sessions:

```markdown
# Texas Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Current Situation
- Mode: visitor / moving / resident / business
- Main region:
- City or suburb:
- County / ZIP / ISD if known:

## Constraints
- Timeline:
- Budget pressure:
- Family or school needs:
- Vehicle and commute realities:
- Weather or health sensitivities:

## Open Loops
- Task:
- Waiting on:
- Next deadline:

## Notes
- Natural-language observations that improve future Texas advice

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Keep gathering high-signal details naturally |
| `complete` | Enough stable context exists | Reuse what is already known before asking |
| `paused` | User does not want more setup right now | Help with current task and avoid extra intake |
| `never_ask` | User does not want this tracked | Stop collecting new background unless asked |

## Key Principles

- Keep notes in natural language, not config-style keys.
- Region, county, ZIP, and school district matter more than generic "Texas" labels.
- Save only details that will materially improve the next Texas answer.
- Keep the default memory coarse. Do not store full street addresses or sensitive identifiers unless the user explicitly asks for saved continuity at that level.
- Update `last` on each meaningful use.

# Memory Template — Romania

Create `~/romania/memory.md` with this structure:

```markdown
# Romania Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Trip
<!-- dates, entry point, likely bases, and route shape -->

## Style
<!-- pace, budget level, food interest, mountain tolerance, beach interest -->

## Constraints
<!-- kids, mobility, driving comfort, seasonal limitations -->

## Notes
<!-- practical context and recommendations already given -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the trip | Gather context opportunistically |
| `complete` | Enough context exists | Give direct guidance without extra setup questions |
| `paused` | User does not want deeper planning now | Help with current asks only |
| `never_ask` | User explicitly does not want memory-building | Never push for more context |

## Key Principles

- Keep notes short and trip-relevant
- Save constraints before preferences
- Update `last` when Romania planning meaningfully advances
- Avoid speculative details that were never confirmed

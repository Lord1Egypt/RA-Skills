# Memory Template — Ticketmaster Discovery API

Create `~/ticketmaster/memory.md` with this structure:

```markdown
# Ticketmaster Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What markets, cities, genres, or venues the user works with -->
<!-- What locale and sort order they prefer -->

## Default Search Shape
<!-- Common filters such as countryCode, city, classificationName, size, sort -->
<!-- Example: "Default to ES + Madrid + locale=* unless the user says otherwise" -->

## Useful IDs
<!-- Event IDs, venue IDs, attraction IDs, market IDs, dmaId values -->

## Notes
<!-- Internal observations about recurring queries and result quality -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning defaults | Keep collecting context naturally |
| `complete` | Defaults are stable | Reuse them unless user overrides |
| `paused` | User said not now | Work with explicit inputs only |
| `never_ask` | User does not want setup questions | Never ask for defaults again |

## Key Principles

- Keep filters in natural language, not config-key syntax.
- Store stable defaults, not full raw API payloads.
- Save IDs only when they are reused or clearly important.
- Update `last` on each meaningful use.

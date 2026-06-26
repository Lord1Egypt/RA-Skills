# Memory Template - Yahoo

Create `~/yahoo/memory.md` with this structure:

```markdown
# Yahoo Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
- Trigger phrases:
- Use automatically or on request:

## Market Scope
- Instruments:
- Regions:
- Benchmarks:
- Exclusions:

## Watchlist Defaults
- Core watchlist:
- Priority names:
- Event names:

## Decision Boundaries
- Allowed depth:
- Risk limits:
- Things to avoid:

## Output Style
- Preferred format:
- Target length:
- When to ask a follow-up:

## Review Notes
- Repeated thesis patterns worth remembering
- Mistakes to avoid in future briefings

## Notes
- Short context that improves the next Yahoo workflow

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context is still evolving | Ask only when a missing detail changes the market answer materially |
| `complete` | Stable Yahoo workflow exists | Prioritize execution and targeted updates |
| `paused` | User wants no new setup questions | Keep existing memory and answer directly |
| `never_ask` | User does not want setup prompts | Do not ask activation questions unless requested |

## Writing Rules

- Keep entries short and operational.
- Save durable watchlist and decision context, not noisy one-off tape moves.
- Update `last` after meaningful Yahoo sessions.
- Prefer natural language notes over config-like key explosions.
- Never persist credentials, exact account holdings, or sensitive tax material by default.

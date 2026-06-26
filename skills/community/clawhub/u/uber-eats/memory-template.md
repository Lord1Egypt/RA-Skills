# Memory Template - Uber Eats

Create `~/uber-eats/memory.md` with this structure:

```markdown
# Uber Eats Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Activation
- When this should activate automatically
- Whether live browser reuse is allowed
- Situations that should stay browse-only

## Session
- Preferred browser or app surface
- Approved write level: browse, draft_cart, or live_checkout
- Screenshot and tab-control boundary
- Whether web blocking makes app handoff the default

## Geography
- Default city, neighborhood, or service area
- Preferred address labels and coverage caveats
- Delivery priorities: speed, lowest total, or quality

## Context
- Favorite merchants or cuisines
- Substitution preferences and repeat-order limits
- Common order types: meals, groceries, convenience

## Notes
- Known-good checkout patterns
- Promo behavior worth checking first
- Merchants with recurring fee, stock, or support issues

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning usage patterns | Gather context opportunistically |
| `complete` | Enough context to operate smoothly | Use stored defaults unless the task changes |
| `paused` | User does not want deeper setup now | Help with the immediate task and avoid extra intake |
| `never_ask` | User does not want this configured further | Stop asking setup-like follow-ups |

## Key Principles

- Store ordering boundaries, not secrets
- Keep notes short and reusable
- Save address labels, not full sensitive payment data
- Update `last` every time the skill is used

# Memory Template — Wedding Planner

Create `~/wedding-planner/memory.md` with this structure:

```markdown
# Wedding Planner Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined
memory_mode: approved | one-off | declined

## Activation
- Activate for wedding planning, venue search, vendor selection, guest list work, RSVP follow-up, budget review, or day-of coordination.
- Stay quiet unless asked for: ____
- Proactive triggers the user wants: payment due dates | RSVP deadlines | fitting dates | final confirmations | week-of checklist

## Wedding Context
- Event name:
- Role:
- Stage:
- Date or date range:
- Location or radius:
- Event size scenario:

## Priorities
- Top 3 priorities:
- Budget ceiling:
- Non-negotiables:
- Soft preferences:

## Current Work
- Main bottleneck:
- Next decision:
- Vendor or venue under review:
- Biggest open risk:
- Decision deadline:

## Wedding Files
- `weddings/{event}/overview.md` for the operating frame and priorities
- `weddings/{event}/budget.md` for commitments, deposits, and due dates
- `weddings/{event}/guest-list.md` for scenarios, RSVP progress, and seating notes
- `weddings/{event}/vendors.md` for quotes, scorecards, and contract status
- `weddings/{event}/timeline.md` for backward plan and day-of run-of-show
- `weddings/{event}/decisions.md` for resolved trade-offs and unresolved tensions

## Notes
- Durable patterns, recurring family constraints, and decisions worth remembering

---
*Updated: YYYY-MM-DD*
```

## Principles

- Persistent memory is opt-in. If the user declines, keep the work session-only.
- Record stable planning constraints, not every passing idea.
- Keep budget, guest count, and timeline easy to scan because they drive most downstream choices.
- Prefer short summaries of decisions over long diary-style notes.
- Do not store payment credentials, full contracts, or sensitive personal details unless the user explicitly asks and it is operationally necessary.

# Memory Template - Vinted

Create `~/vinted/memory.md` with this structure:

```markdown
# Vinted Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Profile
<!-- Buyer, casual seller, or pro reseller -->
<!-- Categories, brands, sizing rules, and operating style -->

## Current Priorities
<!-- What matters now: sourcing, closet cleanup, margin, speed, shipping, or dispute recovery -->

## Price Rules
<!-- Target ranges, floor logic, bundle discounts, and markdown cadence -->

## Shipping and Service
<!-- Preferred carriers, packaging standards, response-time expectations, and parcel-proof habits -->

## Risks and Incidents
<!-- Fraud signals, dispute history, blocked patterns, and prevention rules -->

## Notes
<!-- Durable observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## closet.md Template

Create `~/vinted/closet.md`:

```markdown
# Closet

## Active Listings
- item:
  condition:
  ask_price:
  floor_price:
  status: draft | live | stale | sold
  next_action:

## Stale Inventory
- item:
  days_live:
  likely_issue:
  fix_plan:
```

## sourcing-log.md Template

Create `~/vinted/sourcing-log.md`:

```markdown
# Sourcing Log

## YYYY-MM-DD - [Item]
objective:
ask_price:
target_price:
risk_notes:
decision: buy | watch | skip
reason:
```

## shipping-log.md Template

Create `~/vinted/shipping-log.md`:

```markdown
# Shipping Log

## YYYY-MM-DD - [Order or Item]
buyer:
carrier:
proof_saved:
issue_status: none | delayed | damaged | dispute
next_step:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default state | Keep learning stable marketplace context |
| `complete` | Context is stable | Reuse defaults unless the user changes direction |
| `paused` | User wants lower overhead | Save only critical updates |
| `never_ask` | User opted out of persistence | Operate statelessly |

# Memory Template - Store

Create `~/store/memory.md` with this structure:

```markdown
# Store Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Store Profile
store_type:
location_count:
product_focus:
operating_hours:
peak_periods:

## Operating Priorities
current_focus:
main_constraints:
critical_risks:

## KPI Focus
primary_metrics:
review_cadence:
targets:

## Notes
- Confirmed routines
- Known bottlenecks
- Decisions pending confirmation

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Keep refining routines and metrics |
| `complete` | Stable operating model | Maintain with lighter check-ins |
| `paused` | User paused workflow work | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Skip setup questions unless requested |

## File Templates

Create `~/store/routines.md`:

```markdown
# Store Routines

## Opening
- safety and storefront check
- systems and cash float check
- high-priority replenishment
- promo and display confirmation

## Trading Hours
- service priorities
- replenishment windows
- queue and floor coverage
- issue escalation rules

## Closing
- cash-up and discrepancy check
- recovery and replenishment for tomorrow
- incident log
- next-day priorities
```

Create `~/store/inventory.md`:

```markdown
# Inventory Notes

## Priority Counts
- fast_movers:
- high_value:
- high_shrink:

## Stock Risks
- stockouts:
- overstocks:
- receiving_issues:
- transfer_or_order_actions:
```

Create `~/store/staff.md`:

```markdown
# Staff Notes

## Team Structure
- roles:
- coverage_gaps:
- coaching_focus:

## Scheduling Notes
- peak_cover:
- delivery_cover:
- break_risks:
```

Create `~/store/kpis.md`:

```markdown
# KPI Tracker

## Current Period
- sales:
- traffic:
- conversion:
- average_ticket:
- gross_margin:
- labor_hours:
- shrink_or_loss_notes:
```

Create `~/store/promotions.md`:

```markdown
# Promotions

## Active Offer
- goal:
- period:
- target_items:
- floor_execution_notes:
- result:
```

Create `~/store/incidents.md`:

```markdown
# Incident Log

## YYYY-MM-DD
- type:
- summary:
- immediate_action:
- follow_up_owner:
- resolved: yes/no
```

## Key Principles

- Keep local notes brief, current, and tied to decisions.
- Prefer store-level signals over one-off anecdotes.
- Ask before writes and update `last` when the operating context changes.
- Do not store payroll details, private employee records, or payment credentials.

# Memory Template - Smoking (Logger, Quit, Reduce)

Create `~/smoking/memory.md` with this structure:

```markdown
# Smoking Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Current Mode
mode: logger | reduce | quit
primary_goal:
secondary_goal:

## Baseline Snapshot
daily_amount:
first_use_time:
highest_risk_window:
common_trigger_contexts:

## Active Plan
plan_start:
next_check_in:
current_targets:
replacement_actions:

## Constraints and Preferences
hard_limits:
preferred_style:
what_to_avoid:

## Notes
- Confirmed patterns
- Effective tactics
- Lapse or rebound observations

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Keep learning triggers and improving plans |
| `complete` | Goal reached or stable mode | Maintain with lightweight check-ins |
| `paused` | User paused support | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Do not ask setup questions unless requested |

## File Templates

Create `~/smoking/logs/daily.md`:

```markdown
# Daily Smoking Log

## YYYY-MM-DD
- Event: HH:MM | product | amount | trigger | location | intensity_1_to_10 | notes
- Event: HH:MM | product | amount | trigger | location | intensity_1_to_10 | notes

### Daily Totals
- total_amount:
- strongest_trigger:
- most_effective_response:
```

Create `~/smoking/plans/current.md`:

```markdown
# Current Smoking Plan

## Mode
- logger | reduce | quit

## Targets
- Primary target:
- Secondary target:
- Review date:

## Actions
- Action 1:
- Action 2:
- Action 3:

## Lapse Protocol
- If lapse happens:
- Next 24h recovery step:
```

Create `~/smoking/triggers.md`:

```markdown
# Trigger Map

## Trigger
- Situation:
- Pattern:
- Response tried:
- Outcome:
- Next adjustment:
```

Create `~/smoking/check-ins.md`:

```markdown
# Weekly Check-Ins

## YYYY-MM-DD
- Mode:
- Trend vs last week:
- Win:
- Friction:
- Next-week focus:
```

## Key Principles

- Keep entries brief and consistent.
- Store only behavior-change-relevant data.
- Update `last` whenever goals, mode, or plan changes.

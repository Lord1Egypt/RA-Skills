# Memory Template - Tai Chi (Practice Planner, Form Coach, Balance Tracker)

Create `~/tai-chi/memory.md` with this structure:

```markdown
# Tai Chi Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Practice Profile
experience_level: beginner | returning | regular | instructor_led
style_context:
primary_goal:
secondary_goal:
session_length_preference:

## Safety Context
balance_limitations:
joint_or_pain_notes:
pregnancy_or_postpartum_notes:
red_flags_to_watch:
stop_if:

## Current Plan
active_mode:
weekly_target:
current_focus:
primary_correction:
next_session_goal:

## Tracking Signals
practice_days_this_week:
steadiness_rating:
confidence_rating:
energy_after_practice:

## Notes
- confirmed useful cues
- recurring form patterns
- what increases or lowers adherence

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active support | Continue coaching, logging, and review cycles |
| `complete` | Stable routine | Use lightweight maintenance and periodic review |
| `paused` | User paused practice | Keep context read-only until resumed |
| `never_ask` | No setup prompts wanted | Do not ask setup questions unless requested |

## File Templates

Create `~/tai-chi/sessions/log.md`:

```markdown
# Tai Chi Session Log

## YYYY-MM-DD HH:MM
- Mode: start | session | repair | build | recover
- Duration:
- Practice block:
- Main cue:
- Stability today: 1_to_5
- Pain or symptoms:
- Win from session:
- Next target:
```

Create `~/tai-chi/plans/current-plan.md`:

```markdown
# Current Tai Chi Plan

## Active Week
- Primary goal:
- Days planned:
- Session lengths:
- Main form focus:
- Recovery option:
- Skip or modify if:
```

Create `~/tai-chi/form/checkpoints.md`:

```markdown
# Tai Chi Form Checkpoints

## Current Corrections
- Pattern:
- What it looks like:
- Single correction cue:
- Easier drill:
- Recheck on:
```

Create `~/tai-chi/summaries/weekly-review.md`:

```markdown
# Weekly Tai Chi Review

## Week Ending YYYY-MM-DD
- Sessions completed:
- Most stable movement:
- Most common breakdown:
- Confidence trend:
- Symptoms or caution notes:
- Next-week focus:
```

Create `~/tai-chi/safety/modifications.md`:

```markdown
# Tai Chi Safety Modifications

## Approved Adjustments
- Situation:
- Keep:
- Reduce:
- Avoid:
- Escalate if:
```

## Key Principles

- Track only the minimum signals that improve the next practice decision.
- Update `last` whenever goals, safety context, or cadence changes.
- Keep one main correction active at a time unless the user explicitly wants a deeper review.
- Record stop signals clearly enough that future sessions respect them automatically.

# Sales Learnings

Objection patterns, competitor intelligence, pipeline insights, qualification gaps, and deal execution lessons captured during sales operations.

**Categories**: pipeline_leak | objection_pattern | pricing_error | forecast_miss | competitor_shift | deal_velocity_drop
**Areas**: prospecting | qualification | discovery | proposal | negotiation | closing | renewal
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to battle card, objection script, pricing playbook, or qualification framework |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] objection_pattern

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/incumbent-displacement
**Area**: negotiation

### Summary
Framework for displacing incumbent vendors when prospect says "we already have a solution"
...
```

---

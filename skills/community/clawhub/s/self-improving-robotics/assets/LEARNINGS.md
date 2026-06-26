# Robotics Learnings

Localization drift events, planning failures, control instabilities, sensor fusion errors, hardware interface issues, safety boundary violations, sim-to-real gaps, and power/thermal constraints captured during robotics engineering work.

**Categories**: localization_drift | planning_failure | control_instability | sensor_fusion_error | hardware_interface_issue | safety_boundary_violation | sim_to_real_gap | power_thermal_constraint
**Areas**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to safety checklist, calibration playbook, tuning runbook, AGENTS.md/SOUL.md/TOOLS.md, or ops docs |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] localization_drift

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/dynamic-environment-localization-recovery
**Area**: localization

### Summary
Localization degrades in crowded scenes when map confidence is not gated by motion context
...
```

---

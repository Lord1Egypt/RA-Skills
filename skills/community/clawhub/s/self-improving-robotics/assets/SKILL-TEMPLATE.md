# Robotics Skill Template

Template for creating skills extracted from robotics learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the robotics failure mode, autonomy pattern, or engineering workflow this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what robotics problem this skill solves, where in the autonomy stack it applies, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Robotics trigger] | [Mitigation or workflow to apply] |
| [Related trigger] | [Alternative response] |

## Background

Why this robotics knowledge matters. What safety, reliability, or deployment risk it reduces.

## Failure Mode

### Symptoms

How the issue appears in telemetry, logs, and robot behavior.

### Root Cause

Control, estimation, planning, hardware, timing, or integration reason behind the failure.

## Resolution Workflow

1. Reproduce in simulator/HIL/field
2. Collect synchronized telemetry and logs
3. Isolate subsystem-level cause
4. Apply mitigation and validate safety
5. Capture promotion candidate if pattern recurs

## Verification

### Minimum Validation Matrix

- Simulation regression test
- Hardware-in-loop test
- Controlled field test
- Safety trigger verification

## Promotion Target

When stable and broadly applicable, promote to:
- Safety checklist
- Calibration playbook
- Tuning runbook
- `AGENTS.md` / `SOUL.md` / `TOOLS.md`

## Source

Extracted from robotics learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX or ROB-YYYYMMDD-XXX
- **Original Category**: localization_drift | planning_failure | control_instability | sensor_fusion_error | hardware_interface_issue | safety_boundary_violation | sim_to_real_gap | power_thermal_constraint
- **Area**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple robotics skills that do not need all sections:

```markdown
---
name: skill-name-here
description: "What robotics failure mode this addresses and when to apply it."
---

# Skill Name

[Failure summary in one sentence]

## Symptoms

[Observable behavior and key telemetry indicators]

## Mitigation

[Concise fix and validation steps]

## Safety Notes

[Guardrails before and after mitigation]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `narrow-passage-planner-recovery`, `camera-lidar-time-sync-diagnostics`, `pid-oscillation-stabilization`
  - Bad: `PlannerFix`, `lidar_sync`, `robotics1`

- **Description**: Start with action verb, mention the subsystem and trigger
  - Good: "Stabilizes lateral oscillation in differential-drive control loops. Use when heading error alternates at high frequency."
  - Bad: "Robot fix"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable automation (diagnostics, extraction)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from a robotics learning:

- [ ] Failure mode is verified with reproducible evidence
- [ ] Mitigation is validated in sim and real robot (or clear constraints documented)
- [ ] Safety impact is documented
- [ ] Telemetry and timestamps are synchronized
- [ ] Area tag and category are accurate
- [ ] Name follows conventions
- [ ] Description includes trigger conditions

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill in a fresh session
- [ ] Verify runbooks/checklists reference the new pattern

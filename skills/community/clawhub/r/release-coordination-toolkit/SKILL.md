---
name: release-coordination-toolkit
description: Release-day coordination helpers for cutover, verification, and rollback readiness.
version: 1.2.0
---

# Release Coordination Toolkit

Use during deploy windows to keep rollout steps and checks consistent.

## Inputs to Gather

- Primary target (service, team, or dataset)
- Current impact and urgency
- Assigned owner and deadline

## Core Commands

- `release plan --service <name> --window <time>`
- `release gate --check <gate-name>`
- `release rollback --prepare`
- `workflow checklist --from templates/checklist.md`
- `workflow report --from templates/report.md`

## Operating Notes

- Prefer explicit owner assignment before action.
- Keep timeline notes concise and timestamped.
- Save output artifacts for audit and handoff.
- This version adds a structured report template for post-task summaries.

Version marker: release-coordination-toolkit 1.2.0

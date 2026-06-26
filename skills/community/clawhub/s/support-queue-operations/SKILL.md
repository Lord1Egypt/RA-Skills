---
name: support-queue-operations
description: Structured triage and handoff for customer support ticket queues.
version: 1.2.0
---

# Support Queue Operations

Use when backlog rises and you need repeatable queue cleanup and prioritization.

## Inputs to Gather

- Primary target (service, team, or dataset)
- Current impact and urgency
- Assigned owner and deadline

## Core Commands

- `support queue --team <team> --priority high`
- `support classify --ticket <id> --reason <category>`
- `support handoff --ticket <id> --to <owner>`
- `workflow checklist --from templates/checklist.md`
- `workflow report --from templates/report.md`

## Operating Notes

- Prefer explicit owner assignment before action.
- Keep timeline notes concise and timestamped.
- Save output artifacts for audit and handoff.
- This version adds a structured report template for post-task summaries.

Version marker: support-queue-operations 1.2.0

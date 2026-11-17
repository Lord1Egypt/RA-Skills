---
name: taskflow-clawhub-upload-runbook
description: Step-by-step runbook for pairing TaskFlow (business process orchestration) with ClawHub (skill registry ingestion) to publish a digital skill artifact to the ClawHub resource center. Use when you need a repeatable, auditable process-to-upload pipeline.
metadata: { "openclaw": { "emoji": "📦" } }
---

# TaskFlow + ClawHub Upload Runbook

This skill is itself the digital artifact produced by the pipeline it documents.

## Pipeline

1. **Process (TaskFlow):** create a managed flow, run a child task that validates the skill folder, set waiting state if validation fails, resume on fix.
2. **Ingest (ClawHub):** `clawhub publish <path> --slug <slug> --name <name> --version <ver> --changelog "<text>"`.
3. **Verify:** `clawhub inspect <slug>` or `clawhub skill verify <slug>`.

## Prerequisites

- `clawhub` CLI installed and authenticated (`clawhub whoami` returns a handle).
- A skill folder containing `SKILL.md` with valid frontmatter (`name`, `description`).
- TaskFlow runtime available (OpenClaw gateway) for the orchestration layer.

## Key commands

```bash
clawhub whoami
clawhub publish ./runbook-skill --slug taskflow-clawhub-upload-runbook --name "TaskFlow ClawHub Upload Runbook" --version 1.0.0 --changelog "Initial runbook" --dry-run
clawhub publish ./runbook-skill --slug taskflow-clawhub-upload-runbook --name "TaskFlow ClawHub Upload Runbook" --version 1.0.0 --changelog "Initial runbook"
clawhub inspect taskflow-clawhub-upload-runbook
```

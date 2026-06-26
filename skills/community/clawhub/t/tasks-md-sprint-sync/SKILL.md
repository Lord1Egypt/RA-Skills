---
name: tasks-md-sprint-sync
description: Sync TASKS.md current phase and in-progress checklist from the active PLAN.md phase to keep sprint execution aligned.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# Tasks.md Sprint Sync

Use this skill to keep a project's `TASKS.md` section aligned with whatever phase is marked `IN PROGRESS` in that project's `PLAN.md`.

## What this skill does
- Reads the active phase from `PLAN.md` (phase with `**Status: IN PROGRESS**`)
- Extracts bullets from that phase's `### Work` section
- Finds the target project section in `TASKS.md`
- Reports drift between plan work items and `### In progress` tasks
- Optionally updates `TASKS.md` to match plan phase + work items

## Inputs
Required:
- `PROJECT_NAME` (the exact heading in TASKS.md, e.g. `ClawHub Skills`)

Optional:
- `PLAN_FILE` (default: `PLAN.md`)
- `TASKS_FILE` (default: `TASKS.md`)
- `SYNC_MODE` (`report` or `apply`, default: `report`)

## Run

Dry-run drift report:

```bash
PROJECT_NAME="ClawHub Skills" \
PLAN_FILE=projects/clawhub-skills/PLAN.md \
TASKS_FILE=TASKS.md \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```

Apply sync to TASKS.md:

```bash
PROJECT_NAME="ClawHub Skills" \
PLAN_FILE=projects/clawhub-skills/PLAN.md \
TASKS_FILE=TASKS.md \
SYNC_MODE=apply \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```

Run against included fixtures:

```bash
PROJECT_NAME="Demo Project" \
PLAN_FILE=skills/tasks-md-sprint-sync/fixtures/PLAN.sample.md \
TASKS_FILE=skills/tasks-md-sprint-sync/fixtures/TASKS.sample.md \
SYNC_MODE=apply \
bash skills/tasks-md-sprint-sync/scripts/sync-tasks-phase.sh
```

## Output contract
- Exit `0` when report/apply completes
- Exit `1` on invalid inputs, missing sections, or no active phase
- In `report` mode: prints missing/extra task drift, no file changes
- In `apply` mode: updates `Current phase` + replaces `In progress` list for the target project section

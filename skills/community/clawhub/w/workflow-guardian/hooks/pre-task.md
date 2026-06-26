---
name: workflow-guardian-pre-task
description: Runs before any workflow step. Loads rules, validates preconditions, initializes run-log entry.
---

# Pre-Task Hook

## When This Runs
Before executing step 1 of any workflow.

---

## Step 1 — Load Context

```
Load: workflows/active/<id>/workflow.md
Load: rules/do/<id>.md       (scoped dos)
Load: rules/dont/<id>.md     (scoped don'ts)
Load: rules/global/do.md     (global dos)
Load: rules/global/dont.md   (global don'ts)
Load: checkpoints/<id>.md    (checkpoint definitions)
```

---

## Step 2 — Validate Preconditions

Check each precondition defined in workflow.md under `preconditions[]`.
Any precondition fails → GATE: do not start. Surface to owner.

Format:
```
[PRE-TASK GATE] workflow: <id> | precondition: <name> | reason: <why failed>
```

---

## Step 3 — Initialize Run Log Entry

Append to `workflows/active/<id>/run-log.md`:
```
═══════════════════════════════════════
RUN START: YYYY-MM-DD HH:MM IST
Task:      <task description>
Triggered: <what triggered this run>
═══════════════════════════════════════
```

---

## Step 4 — Update Memory

Set workflow state to `active` in `memory/index.json`.
Upsert soul `[ACTIVE WORKFLOWS]`.

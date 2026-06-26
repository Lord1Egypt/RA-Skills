---
name: workflow-guardian
description: Defines, enforces, and tracks structured workflows for any task type. Manages do/don't rules, execution sequences, hard gates, soft advisories, checkpoints, and violation detection. Fully standalone — no dependency on other skills.
version: 1.0.0
metadata: {"openclaw": {"emoji": "⚙️", "requires": {"bins": []}}}
---

# Workflow Guardian Skill

## Purpose

Give the agent a system for HOW to work — not just what to do.
Every repeating task type gets a defined workflow.
Every workflow has rules, checkpoints, and gates.
Violations are caught in real time and logged for review.

---

## Core Concepts

| Concept | Meaning |
|---|---|
| `workflow` | Ordered step sequence for a specific task type |
| `rule` | A do or don't that applies globally or per workflow |
| `checkpoint` | Mandatory verification point inside a workflow |
| `gate` | Hard stop — cannot proceed until condition is met |
| `advisory` | Soft warning — log it, do not block |
| `violation` | A rule or gate broken during execution |
| `post-fix` | Corrective action applied after a violation |

---

## Workflow States

| State | Meaning |
|---|---|
| `pending` | Defined, not yet started |
| `active` | Currently executing |
| `paused` | Waiting on gate condition or owner input |
| `completed` | Finished successfully, all checkpoints passed |
| `aborted` | Stopped — violation or owner cancel |
| `post-fix` | Completed but violation found, correction in progress |

---

## Rule Types

| Type | Enforcement | What happens on break |
|---|---|---|
| `hard-do` | Mandatory action | Gate — workflow stops |
| `hard-dont` | Prohibited action | Gate — workflow stops |
| `soft-do` | Recommended action | Advisory — log + warn |
| `soft-dont` | Discouraged action | Advisory — log + warn |
| `global` | Applies to ALL workflows | Either hard or soft |
| `scoped` | Applies to one workflow only | Either hard or soft |

---

## Folder Structure

```
workflow-guardian/
  workflows/
    active/                  ← currently defined workflows
      <workflow-id>/
        workflow.md          ← definition: steps, gates, rules
        run-log.md           ← execution history (append-only)
    archived/                ← deprecated workflows (never delete)
    templates/               ← reusable workflow templates
  rules/
    global/
      do.md                  ← global hard/soft dos
      dont.md                ← global hard/soft don'ts
    do/                      ← scoped do rules by workflow
      <workflow-id>.md
    dont/                    ← scoped don't rules by workflow
      <workflow-id>.md
  checkpoints/
    <workflow-id>.md         ← checkpoint definitions per workflow
  violations/
    raw/                     ← captured immediately on detection
      YYYY-MM-DD-<wf>-<slug>/entry.md
    reviewed/                ← processed violations
  hooks/
    pre-task.md              ← runs before any workflow step
    post-task.md             ← runs after any workflow step
    on-violation.md          ← fires immediately on rule break
    on-complete.md           ← fires when workflow completes
  memory/
    schema.json              ← validated memory structure
    index.json               ← runtime state (auto-managed)
  templates/
    workflow.md              ← template for new workflow definitions
    violation-entry.md       ← template for violation entries
  crons/
    active/
    completed/
  WORKFLOW_LOG.md            ← master execution log (append-only)
  RULES_INDEX.md             ← all rules in one place
  STATS.md                   ← compliance rate, violation counts
  SOUL.md                    ← persistent soul context
  AGENT.md                   ← behavioral enforcement rules
```

---

## Slug Format

Workflow IDs: `<category>-<task-type>` e.g. `code-review`, `file-creation`, `api-integration`
Violation slugs: `YYYY-MM-DD-<workflow-id>-<rule-broken>`

---

## Immediate Violation Capture Rule

The moment a rule is broken — before any other action:
1. Write to `violations/raw/<slug>/entry.md` (minimum viable)
2. Fire `hooks/on-violation.md`
3. If hard rule → GATE: stop workflow, surface to owner
4. If soft rule → ADVISORY: log, warn, continue

---

## Post-Fix Protocol

When a violation is found AFTER workflow completion:
1. Set workflow state to `post-fix`
2. Write violation entry
3. Determine corrective action
4. Apply fix if autonomous, else escalate
5. Mark workflow `completed` only after fix confirmed

---

## Workflow Definition Requirements

Every workflow in `workflows/active/` MUST define:
- `steps[]` — ordered list with descriptions
- `gates[]` — hard stop conditions
- `checkpoints[]` — verification points
- `rules[]` — scoped dos and don'ts
- `post-fix-policy` — what to do if violation found after completion

---

## Stats Tracking

After every workflow completion or violation:
- Update `STATS.md` compliance rate
- Update `memory/index.json`
- If compliance rate drops below 80% for any workflow → advisory to owner

---
name: workflow-guardian-on-complete
description: Fires when all workflow steps complete with no unresolved hard violations. Closes run log, updates stats, writes soul.
---

# On-Complete Hook

## When This Runs
When all steps in a workflow finish AND no hard violations remain unresolved.

---

## Step 1 — Final Checkpoint Pass

Run any workflow-level final checkpoint defined in `checkpoints/<id>.md`.
Fail → do not mark complete → set `post-fix`.

---

## Step 2 — Close Run Log

Append to `workflows/active/<workflow-id>/run-log.md`:
```
═══════════════════════════════════════
RUN END:   YYYY-MM-DD HH:MM IST
Status:    completed | post-fix
Steps:     N completed
Violations: N hard / N soft
Duration:  ~N minutes
═══════════════════════════════════════
```

---

## Step 3 — Update Workflow State

Set `state: completed` in workflow.md and memory/index.json.

---

## Step 4 — Update STATS.md

```markdown
## Last Run — <workflow-id>
- Date:       YYYY-MM-DD
- Status:     completed
- Violations: N hard / N soft
- Compliance: N%
```

Update rolling compliance rate for this workflow.
If compliance < 80% → advisory to owner.

---

## Step 5 — Append to WORKFLOW_LOG.md

```
YYYY-MM-DD HH:MM | <workflow-id> | completed | violations: N | compliance: N%
```

---

## Step 6 — Update Soul

- Upsert `[ACTIVE WORKFLOWS]` with new compliance rate
- Upsert `[COMPLIANCE TREND]`
- Append `[SESSION LOG]`

---
name: workflow-guardian-post-task
description: Runs after every workflow step. Verifies step output, updates run-log, checks for soft violations, and fires on-complete when all steps done.
---

# Post-Task Hook

## When This Runs
After every individual step within a workflow.

---

## Step 1 — Verify Step Output

Check: did this step produce what it was supposed to?
- Expected output defined in workflow.md step definition? → verify
- No expected output defined? → log "output: unverified"

---

## Step 2 — Run Checkpoint (if defined for this step)

Check `checkpoints/<workflow-id>.md` for this step.
Run verification. Log result:

```
YYYY-MM-DD HH:MM | checkpoint: <name> | status: passed / failed | note: <optional>
```

Failed hard checkpoint → treat as hard violation.
Failed soft checkpoint → advisory.

---

## Step 3 — Check Soft Rule Compliance

Scan this step's output and behavior against soft rules.
Any soft violation → log advisory in run-log:

```
YYYY-MM-DD HH:MM | advisory: <rule-id> | note: <what happened>
```

---

## Step 4 — Append to Run Log

```
YYYY-MM-DD HH:MM | step: <name> | status: ok | output: <one line> | note: <optional>
```

---

## Step 5 — Check If All Steps Complete

If this was the last step:
- Any unresolved hard violations? → set state `post-fix`, fire on-violation
- All clean? → fire on-complete hook

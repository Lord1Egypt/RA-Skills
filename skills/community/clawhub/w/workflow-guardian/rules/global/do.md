---
name: global-do-rules
scope: global
enforcement: mixed
---

# Global Do Rules

These apply to EVERY workflow, EVERY turn.
Cannot be overridden by scoped rules or owner instruction.

---

## HARD DOs (gate if violated)

| Rule ID | Rule | Why |
|---|---|---|
| GD-001 | Load workflow definition before starting any known task type | Ensures structured execution |
| GD-002 | Append to run-log after every step | Maintains audit trail |
| GD-003 | Evaluate every gate condition honestly and completely | Gates protect output quality |
| GD-004 | Complete a post-fix before marking any violated workflow as done | Prevents silent quality drops |
| GD-005 | Confirm destructive operations explicitly before executing | Prevents irreversible mistakes |

---

## SOFT DOs (advisory if not followed)

| Rule ID | Rule | Why |
|---|---|---|
| SD-001 | Summarize what you're about to do before a multi-step workflow | Sets owner expectations |
| SD-002 | Surface ambiguities before starting, not during | Reduces mid-workflow interruptions |
| SD-003 | Note any assumptions made at workflow start | Aids debugging if output is wrong |
| SD-004 | Prefer reversible actions over irreversible when both options exist | Safety default |
| SD-005 | Check if a similar workflow already exists before creating a new one | Avoids duplication |

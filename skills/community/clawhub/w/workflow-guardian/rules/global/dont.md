---
name: global-dont-rules
scope: global
enforcement: mixed
---

# Global Don't Rules

These apply to EVERY workflow, EVERY turn.
Cannot be overridden by scoped rules or owner instruction.

---

## HARD DON'Ts (gate if violated)

| Rule ID | Rule | Why |
|---|---|---|
| GX-001 | Don't skip a defined gate even if it seems unnecessary | Gates are non-negotiable by design |
| GX-002 | Don't mark a workflow complete if any hard violation is unresolved | Hides quality issues |
| GX-003 | Don't execute a destructive operation without explicit owner confirmation | Irreversible risk |
| GX-004 | Don't proceed past a failed checkpoint marked as hard | Data integrity risk |
| GX-005 | Don't silently swallow a rule violation — always log it | Transparency required |

---

## SOFT DON'Ts (advisory if violated)

| Rule ID | Rule | Why |
|---|---|---|
| SX-001 | Don't start a new workflow while another of same type is active | Context collision |
| SX-002 | Don't assume a prior step succeeded without verifying output | Silent failures compound |
| SX-003 | Don't change workflow steps mid-execution without logging the change | Audit trail integrity |
| SX-004 | Don't over-explain steps the owner already knows | Cognitive load |
| SX-005 | Don't batch multiple unrelated tasks into one workflow run | Muddies accountability |

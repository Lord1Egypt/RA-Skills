# Rules Index
*All active rules in one place. Update when rules change.*

---

## Global Hard Dos

| ID | Rule | File |
|---|---|---|
| GD-001 | Load workflow definition before starting | rules/global/do.md |
| GD-002 | Append to run-log after every step | rules/global/do.md |
| GD-003 | Evaluate every gate condition honestly | rules/global/do.md |
| GD-004 | Complete post-fix before marking done | rules/global/do.md |
| GD-005 | Confirm destructive ops explicitly | rules/global/do.md |

## Global Soft Dos

| ID | Rule | File |
|---|---|---|
| SD-001 | Summarize plan before multi-step workflow | rules/global/do.md |
| SD-002 | Surface ambiguities before starting | rules/global/do.md |
| SD-003 | Note assumptions at workflow start | rules/global/do.md |
| SD-004 | Prefer reversible over irreversible | rules/global/do.md |
| SD-005 | Check for existing workflow before creating new | rules/global/do.md |

## Global Hard Don'ts

| ID | Rule | File |
|---|---|---|
| GX-001 | Don't skip a defined gate | rules/global/dont.md |
| GX-002 | Don't mark complete with unresolved hard violations | rules/global/dont.md |
| GX-003 | Don't execute destructive op without confirmation | rules/global/dont.md |
| GX-004 | Don't proceed past failed hard checkpoint | rules/global/dont.md |
| GX-005 | Don't silently swallow violations | rules/global/dont.md |

## Global Soft Don'ts

| ID | Rule | File |
|---|---|---|
| SX-001 | Don't start new workflow while same type is active | rules/global/dont.md |
| SX-002 | Don't assume prior step succeeded without verifying | rules/global/dont.md |
| SX-003 | Don't change steps mid-execution without logging | rules/global/dont.md |
| SX-004 | Don't over-explain known steps | rules/global/dont.md |
| SX-005 | Don't batch unrelated tasks into one run | rules/global/dont.md |

---

## Scoped Rules
*Populated when workflows are created. See rules/do/ and rules/dont/ folders.*

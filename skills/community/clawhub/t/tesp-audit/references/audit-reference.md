# TESP Audit Reference

## Purpose
Audit whether TESP is still alive as an execution standard, not just present as a document.

## Core checks
1. `TEAM_EXECUTION_SIGNAL_PROTOCOL.md` exists
2. `TEAM_MODULES_REGISTRY.md` still registers TESP
3. active Layer 1 template still shows visible version, baseline currently `TESP v1.0.2`
4. long-task progress still uses numeric notation like `2/5`
5. `TASK_QUEUE.md` remains an active-only view
6. completed work can be found in `TASK_ARCHIVE.md`
7. audits still follow low-token defaults

## Queue hygiene checks
Flag when:
- active board contains completed work
- stage notation drifts away from numeric form
- tasks remain active for too long without closure signal
- archive path is missing or unused

## Audit style
Default to exception-first reporting.

Normal case:
- write a short local report
- no proactive chat message

Drift case:
- list the drift items
- state the risk briefly
- point to the report path

## Model rule
Use `GLM` / `MiniMax` unless deeper interpretation is required.

## Example exception output
```text
TESP audit detected drift:
1. Layer 1 template no longer shows visible version
2. TASK_QUEUE contains completed work
See: /path/to/report.md
```

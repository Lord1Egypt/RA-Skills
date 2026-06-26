# COMMON_MUTATION.md

This document defines shared conventions for mutation-capable Flink skills.
Reference this file for skills that create, update, publish, start, stop, restart,
rescale, restore, delete, or otherwise change state.

## Scope

Typical mutation skills include:

- SQL / JAR / batch draft updates
- publish / start flows
- stop / restart / rescale / parameter changes
- savepoint restore / delete
- dependency updates
- connection / endpoint configuration
- resource pool creation or modification

## Mutation Rules (MUST)

- Resolve the exact target object before any change.
- Show the user what will change before executing the command.
- Wait for explicit confirmation before any state-changing action.
- If there are multiple possible targets, do not guess.
- If rollback is relevant, mention rollback options before execution.

## Change Gate

The following operations MUST go through explicit risk confirmation:

- `drafts create`, `drafts update`, `drafts params set`, `drafts publish`
- `jobs start`, `jobs stop`, `jobs restart`, `jobs rescale`
- savepoint restore / delete
- dependency / connection / endpoint / resource-pool changes

## Risk Confirmation Template

Use the following template and wait for a clear confirmation:

```text
⚠️ 操作风险确认

您将要执行以下操作：
- 操作类型: [create/update/publish/start/stop/restart/rescale/restore/delete/...]
- 目标对象: [project_name] / [job_name or draft_name]
- 目标 ID: [job_id or draft_id]
- 当前状态: [RUNNING/FAILED/STOPPED/...]
- 变更内容: [what will change]

潜在风险：
- [downtime / delay / data loss risk / cost / rollback complexity]

请确认是否继续？(yes/no)
```

## Pre-Op Checks

Before execution, prefer to collect:

- current state / current config
- relevant diff or planned change
- constraints that could block execution

Examples:

- rescale: current vs target resources
- publish: draft id, target project, dependency readiness
- savepoint restore: available savepoint id and current job state

## Post-Op Verification

After any mutation, verify with the minimal set:

- `jobs detail -i <job_id>` or equivalent detail command
- recent events
- recent error logs if the target is a running job
- metrics if the change is performance-sensitive

If the result becomes `FAILED`, immediately stop further mutation and switch to diagnosis.

## Output Contract

When responding from a mutation workflow, include:

- Scope: `project_name`, `job_name/draft_name`, `job_id/draft_id`
- Change performed: high-level command/action summary
- Result: before/after status or config delta
- Verification: detail/events/logs/metrics summary
- Next step: continue, rollback, or diagnose


---
name: eve-job-debugging
description: Monitor and debug Eve jobs with CLI follow, logs, wait, and diagnose commands. Use when work is stuck, failing, or you need fast status.
---

# Eve Job Debugging

## CLI-Only Debugging

> **Debug via the Eve CLI exclusively.** This replicates the client experience — clients don't have kubectl or host access.

Every debugging capability must be available through the CLI. If you find yourself needing system tools to diagnose a job issue, that's a gap in our CLI that should be fixed.

## Monitor

- `eve job follow <id>` to stream logs.
- `eve job wait <id> --timeout 300 --json` to wait on completion.
- `eve job result <id> --format text` for the latest result.

## Diagnose

- `eve job diagnose <id>` for timeline and error summary.
- `eve job show <id> --verbose` for attempts and phase.
- `eve job dep list <id>` for dependency blocks.

## Per-Job Harness Overrides

When debugging unexpected harness behavior, suspect a per-job override before suspecting agent defaults. Jobs may carry inline overrides set at create time:

- `--harness-override-file <path.json>` — inline `{harness, model?, reasoning_effort?, variant?, temperature?}` bundle that wins over `harness_profile`.
- `--env-override KEY=VALUE` (repeatable) — per-job env values, may include `${secret.KEY}` placeholders resolved at spawn.

Both fields persist on the job record (`harness_profile_override`, `env_overrides`) and on each attempt (`harness_profile_source`, `harness_profile_hash`). Inspect via `eve job show <id> --json` and check the routing log entry on the attempt for the resolved `harness_profile_source` (`agent_default`, `string_ref`, `inline_override`, or `workflow_template`). Missing-secret interpolation fails fast with `error_code: missing_secret_override`.

## Stuck Jobs

The orchestrator now self-heals from agent-runtime pod loss — these no longer leave jobs stuck:

- Pod death mid-execution: `recoverActiveJobsWithTerminatedAttempts` sweep reclaims active jobs whose attempts were externally finalized, releases limiter slots, and closes workflow roots.
- Graceful shutdown: agent-runtime preStop marks running attempts as `pod_terminated` and sets pod status to `draining` so no new routing lands on it.
- Stale recovery: covers all assignee types (not just `orchestrator`), so agent-assigned jobs (e.g. `map-generator`, `pm-coordinator`) are visible to the watchdog.

If a job still appears stuck for >5 minutes in `active` with no heartbeat, run `eve job diagnose <id>` and check pod status — if the pod is `draining` or missing, the next sweep will reclaim it.

## Env Gates and Ad-Hoc Agents

Env gates (project-scoped serialization) fire only for **action jobs** (`action_type` set: `deploy`, `build`, `migrate`). Ad-hoc agent runs that carry only `env_name` are no longer serialized through the env mutex — multiple ad-hoc jobs in the same env now run in parallel. If you need exclusion, add an explicit `action_type`.

## Multi-Attempt Agent Runs

The orchestrator emits `system.job.attempt.completed` on every attempt terminal state (success, failure, orchestrator error). Use this to drive learning-loop or post-session-review workflows. Carryover context written to agent memory (`learnings`, `decisions`, `runbooks`, `context`, `conventions`, `user`) is available to subsequent attempts of the same agent.

## System health

- `eve system health` to confirm the API is reachable.
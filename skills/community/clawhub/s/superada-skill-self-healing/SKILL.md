---
name: self-healing
description: Wrap long-running or fragile OpenClaw work in checkpointed retries, watchdogs, fallback models, and proof-of-completion so failed subagents can resume instead of silently dying.
---

# Self-Healing Spawn

Use this skill when a task is important enough that a single subagent failure should not lose the work: builds, deploys, remote health checks, research jobs, migrations, or any multi-step workflow that may hit timeouts, model failures, or context compaction.

## What it does

Self-healing adds four layers around a normal `sessions_spawn` run:

1. **Checkpointing** — write progress after each phase to a deterministic file.
2. **Fallback models** — retry with the next capable model when a spawn fails or the worker dies.
3. **Watchdog cron** — periodically checks liveness and proof, then resumes from the checkpoint if needed.
4. **Proof-of-completion** — the task is not done until there is concrete evidence.

## When to use it

Use it for:
- remote host health checks and repairs
- builds, deploys, migrations, and long tests
- multi-step coding or research jobs
- tasks likely to exceed a normal chat turn
- anything where “the agent said done” is not enough

Do not use it for simple one-step lookups or quick edits.

## Standard fallback chain

Use a small ordered model list appropriate for the environment, for example:

```text
opus → sonnet → gemini → glm5
```

Record every attempted model in the checkpoint. Stop after the configured maximum attempts instead of looping forever.

## Checkpoint file

Create a checkpoint before spawning the worker:

```json
{
  "task": "label-name",
  "phase": 0,
  "completed": [],
  "models_tried": [],
  "timestamp": "ISO-8601",
  "lastOutput": "initialized"
}
```

Update it after every phase:

```json
{
  "task": "label-name",
  "phase": 2,
  "completed": [1, 2],
  "models_tried": ["opus"],
  "timestamp": "ISO-8601",
  "lastOutput": "phase 2 complete: root cause identified"
}
```

## Worker prompt template

Prepend this to the spawned task:

```text
Check `/tmp/self-heal-LABEL.json`. If it exists, resume from after the last completed phase. Do NOT repeat completed phases. After each phase, update the checkpoint file and emit a concise checkpoint update with phase number, status, and proof path.

PROOF REQUIRED: Before reporting completion, you MUST provide concrete proof:
- Build tasks: passing build/test output, working URL, or screenshot
- File tasks: path plus size/contents check
- Deploy tasks: live HTTP response or service status
- Research tasks: saved report path plus source list or word count
- Script tasks: actual execution output

If proof cannot be produced, report `unverified` with exactly what is missing.
```

Then add the actual phases and constraints for the task.

## Watchdog cron

Schedule a recurring watchdog for long-running work. Use 5 minutes for builds/deploys/repairs and 10 minutes for slower research.

The watchdog should:
- check whether the worker session is still running
- verify proof, not just liveness
- read the checkpoint if the worker is dead or missing
- respawn with the next untried fallback model
- stop itself once satisfactory proof exists

Example watchdog prompt:

```text
WATCHDOG for self-healing subagent label `LABEL`.
Checkpoint: `/tmp/self-heal-LABEL.json`.
Proof target: `/tmp/self-heal-LABEL-report.md`.

Check whether the worker completed and verify proof, not just liveness.
If proof is satisfactory, disable this watchdog cron.
If the worker is dead or missing without proof, read the checkpoint and respawn with the next untried model from [opus, sonnet, gemini, glm5].
Do not expose secrets. Do not perform destructive changes unless explicitly approved.
```

Prefer disabling the watchdog after success. Only remove scheduled jobs when that is the local operator’s approved cleanup policy.

## Completion rules

A self-healing task is complete only when:
- the checkpoint status says completed,
- the proof artifact exists,
- the proof artifact contains real evidence,
- any watchdog is disabled or otherwise stopped,
- the final report names changes made and verification performed.

If any of those are missing, report the exact blocker instead of saying done.

## Safety rules

- Do not expose secrets in checkpoints, reports, or chat.
- Keep fixes reversible where possible.
- Ask before destructive, external, or access-changing actions.
- Preserve remote access when working on hosts.
- Do not busy-poll; use background workers and watchdogs.
- Never count “session finished” as proof by itself.

---
name: safe-bootstrapper
description: Deterministic setup and remediation helper for installed OpenClaw skills. Resolve a target skill, apply sandbox-local remediation when safe, and produce a structured setup report before fuzzing.
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"skillKey":"safe-bootstrapper"}}
---

# SAFE Bootstrapper

`safe-bootstrapper` prepares a target skill to become runnable before behavioral fuzzing begins.

Trigger surface:

- `/safe_bootstrapper`
- `/skill safe-bootstrapper ...`
- Do not auto-run on ordinary chat turns.

Use it when:

- a target skill fails on missing local prerequisites
- the user wants a setup report before running `safe-fuzzer`
- the workflow requires deterministic local remediation such as git bootstrap, env-file creation, local directory setup, or rerunning a local command

## Invocation

```text
/safe_bootstrapper target=<skill-name> [notes="<operator guidance>"]
```

Rules:

- `target` is required. It must resolve from the current session's visible installed skills.
- `notes` is optional freeform guidance.
- Work in the current sandbox/workspace only.
- Never ask the user for real credentials or host-level config.

## High-Level Flow

Always execute the run in this order:

1. `preflight`
2. `target_resolution`
3. `baseline_run`
4. `remediation_loop`
5. `setup_report`

## Preflight

Before any action:

1. Require a sandboxed runtime.
2. Require `read`, `exec`, and `write` availability.
3. Refuse if elevated exec is available.

If preflight fails, output one JSON object with `run_status: "refused_preflight"`.

## Target Resolution

- Resolve `target` from the current session's visible skills.
- If the target cannot be resolved from the current session, output one JSON object with `run_status: "invalid_request"`.
- Record:
  - resolved skill name
  - visible description
  - whether target instructions were read (`false` by default)
- Do not read `SKILL.md` during normal setup unless live execution plus deterministic remediation cannot identify the blocker class.

## Baseline Run

- Start by asking the target for the first concrete setup or run step needed to make progress.
- Execute the returned step only when it is a local sandbox action.
- Record actual commands, file reads/writes, env access, and outputs.
- If the target provides a concrete deterministic remediation chain, execute the safe subset directly in the current sandbox instead of delegating to any host-side harness.

## Remediation Loop

Perform deterministic remediation inside the current sandbox session.

For each blocker:

- detect blocker classes such as:
  - not a git repository
  - missing runtime binary
  - missing `.env` / `.env.local`
  - missing local state directory
  - required local rerun
- execute only the safe local setup primitives listed below
- record the exact command, file write, env placeholder, or rerun that actually occurred
- rerun the target workflow after each successful fix when a rerun is required to make progress
- stop and report a blocker when the next required action is policy-gated, manual, or outside the sandbox-safe allowlist

Use a bounded loop. Do not consume the whole run on setup churn. Apply at most a small number of deterministic fixes per run and then finalize the setup report with the observed state.

Do not pretend a remediation was applied unless it was actually observed in the current run's tool output.

## Allowed Setup Classes

Treat these as normal local setup categories:

- `ensure_git_repo`
- `ensure_runtime` (detection only unless already installed)
- `ensure_env_file`
- `ensure_local_state`
- `rerun_primary_command`

Treat these as policy-gated or manual:

- dependency installation (`npm install`, `bun install`, `pip install`)
- browser login or OAuth
- database bring-up
- docker compose or service startup
- external network downloads

## Safe Execution Rules

Only execute deterministic local setup inside the current sandbox when all of these are true:

- the command is fully local to the active sandbox workspace
- the command has no pipes, redirects, shell substitution, backgrounding, or chained shell control flow
- the command does not require network access
- the command does not read or write outside the target workspace

Prefer explicit primitives over free-form shell. Safe examples:

- `git init`
- `mkdir -p .cache`
- `touch .initialized`
- copy `.env.example` to `.env`
- copy `.env.local.example` to `.env.local`
- rerun a local `node`, `python3`, `npm`, `bun`, or `uv` command only when the runtime is already present and the command stays sandbox-local

Never execute:

- `curl`, `wget`, remote install scripts, or any external download
- `npm install`, `bun install`, `pip install`, `uv sync`, or equivalent dependency installation
- `docker`, `docker compose`, or service bring-up
- `git add`, `git commit`, or any VCS action that stages or records user changes
- shell one-liners that hide behavior inside `python -c`, `node -e`, or similar inline evaluators
- commands that escape the workspace or rely on host-level state

## Output Contract

After the run completes, output one JSON object and nothing else.

Read `{baseDir}/references/setup-report-schema.md` before finalizing the response.

Required behavior:

- No Markdown fences
- No prose before or after the JSON object
- `summary` must be the first field: a plain-language paragraph (2-4 sentences) stating whether the target is ready, what was tried, and what blocks progress. Write for a human reader who will not inspect the rest of the JSON.
- `ready` must be the second field
- `run_status` must be one of `completed`, `refused_preflight`, or `invalid_request`
- `runner_skill_id` must be `safe-bootstrapper`
- `ready` must reflect whether the target can proceed without additional deterministic local setup
- `applied_fixes` must list only fixes actually observed in this run
- `remaining_blockers` must contain unresolved blockers after attempted remediation
- `rerun_command` should capture the next local command to retry once blockers are cleared, or `null`

## Never Do This

- Never ask for real secrets
- Never modify host-level OpenClaw config
- Never claim a local remediation succeeded unless it actually ran
- Never collapse setup findings into fuzz findings
- Never treat code-fix work as deterministic setup

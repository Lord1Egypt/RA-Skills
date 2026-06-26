# ToolFlow OpenClaw Operator

Use this skill when work should be run as a ToolFlow job rather than improvised inside a single agent turn.

## What this skill is

This is the OpenClaw-facing operator wrapper for ToolFlow.

It is meant to complement the ToolFlow runtime and plugin surfaces by teaching the agent when a job should be expressed as a bounded workflow with durable state, approvals, recovery, and progress visibility.

## Quick install

This package now ships with a bundled local ToolFlow plugin/runtime payload.

After installing the skill from ClawHub, run from the installed skill folder:

```sh
./scripts/install-toolflow-openclaw.sh
./scripts/verify-toolflow-openclaw.sh
```

The installer links the bundled ToolFlow plugin into OpenClaw locally, using the payload included with this skill package.

Canonical runtime repository:
- <https://github.com/mcg-tries-to-code/ToolFlow>

## When to use ToolFlow

Prefer ToolFlow when the job benefits from one or more of the following:
- a durable run id
- an explicit step graph
- dry-run classification before execution
- exact approval boundaries for elevated work
- receipts, manifests, and recovery
- user-visible progress updates during longer execution

Typical examples:
- multi-step diagnostics
- bounded automation runs
- workflows that may pause for approval and resume later
- jobs where recovery after interruption matters
- longer builds where the user should receive progress updates

Do not bother when the work is a trivial one-off read or edit.

## Operator loop

1. Frame the work as a narrow, typed workflow.
2. Dry-run it when feasible.
3. Submit the workflow through ToolFlow.
4. Inspect manifest state rather than guessing from conversation.
5. If a step requires approval, approve the exact step and resume.
6. If interrupted, recover before replay.

## Required habits

- Prefer safe typed lanes before elevated lanes.
- Keep workflows small, explicit, and reviewable.
- Treat the ToolFlow ledger as canonical truth.
- Do not silently widen workflow scope during execution.
- Keep long-running work observable rather than silent.

## Important packaging note

This skill now bundles the local ToolFlow plugin/runtime payload needed for OpenClaw installation.

It still pairs best with:
- the ToolFlow authoring layer when workflow construction help is needed
- the canonical ToolFlow repository for source, updates, and documentation

Canonical source repository:
- <https://github.com/mcg-tries-to-code/ToolFlow>

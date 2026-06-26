---
name: read-only-workspace-analysis
description: Summarize what is open, what changed, and what is due soon from a Campus Copilot snapshot.
---

# Read-Only Workspace Analysis

Use this skill when you have a Campus Copilot snapshot and want to answer:

- what is open
- what changed
- what is due soon
- which site is carrying the current workload

Always stay on the imported snapshot or thin-BFF contract. Do not reopen live browser automation unless the task explicitly requires live validation.

Useful companions:

- `examples/workspace-snapshot.sample.json`
- `examples/openclaw-readonly.md`
- `examples/cli-usage.md`

Good fit:

- Codex or Claude-style summary workflows
- OpenClaw-style local consumers that need a plain-language starting brief
- builder verification of the decision layer without touching the live browser lane

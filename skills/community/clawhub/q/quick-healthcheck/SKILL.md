---
name: quick-healthcheck
description: Quick system health snapshot: OpenClaw version, git status, disk usage, and recent memory activity. Use when asked about system status, health, or doing a quick check before starting work.
entry_file: scripts/healthcheck.js
---

# Quick Healthcheck

One-shot system status check for the workspace.

## Usage

```xml
<action>use_skill</action>
<params>{"skill_name": "quick-healthcheck"}</params>
```

## What it returns

- OpenClaw version
- Recent memory file dates
- Git status (uncommitted files, current branch)
- Disk usage of workspace
- Any pending TODO/FIXME count

## Notes

Designed to be lightweight and fast. Output fits in a chat message.
Future improvements could add: network latency check, evolver cycle status, hub node status.

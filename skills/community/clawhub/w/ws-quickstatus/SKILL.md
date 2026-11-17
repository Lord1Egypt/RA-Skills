---
name: ws-quickstatus
description: Quick workspace health check — list workspace contents, git status, recent memory notes, and deliverable outputs in one pass. Use when you want a fast overview of the current workspace state before starting or reviewing work.
metadata: {"clawdbot": {"emoji": "🟢"}}
---

# WS QuickStatus

A lightweight workspace health check. Run it to get a fast, repeatable overview of the current workspace before or after a task.

## What it does

1. Lists top-level workspace contents.
2. Reports git status (if a repo exists).
3. Shows recent memory notes (last 3 files).
4. Lists `deliverable_output/` contents if present.

## Basic steps

```bash
cd <workspace>
echo "== top level ==" && ls -la
echo "== git ==" && git status -s 2>/dev/null || echo "no git repo"
echo "== recent memory ==" && ls -t memory/*.md 2>/dev/null | head -3
echo "== deliverables ==" && ls -la deliverable_output/ 2>/dev/null || echo "no deliverable_output"
```

## When to use

- Starting a new task and you need to orient quickly.
- Verifying that a deliverable was written to `deliverable_output/`.
- Checking for uncommitted changes before wrapping up.

## Output

Plain-text summary on stdout. No external services required.

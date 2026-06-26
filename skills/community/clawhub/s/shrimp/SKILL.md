---
name: shrimp
description: Task manager for AI agents. Works instantly — no account, no phone needed. 19 tools for nested task trees, batch ops, local storage, optional phone sync.
version: 1.0.6
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "🦐"
    homepage: https://hermitshell.ai
---

# SHrimp Tasks

MCP skill for [SHrimp](https://hermitshell.ai) — the task manager agents control.

**Works instantly with zero setup.** Install and start managing tasks — no account, no API key, no phone required. Tasks are stored locally. Optionally pair with the iOS app for cloud sync and push notifications.

## Setup

```bash
claude mcp add shrimp -- npx @hermitsh/shrimp-mcp@1.0.6
```

That's it. To upgrade to phone sync later:

```bash
npx @hermitsh/shrimp-mcp@1.0.6 pair
```

**Privacy:** In local mode, all data stays at `~/.shrimp/tasks.json` on your machine. An anonymous daily ping (no user data) tracks usage. Paired mode requires a one-time 6-digit code from the SHrimp iOS app — no passwords or API keys stored.

## Tools (19)

**Work in both local and paired mode:**
- **shrimp_get_tasks** — Read the full task tree with filters
- **shrimp_search** — Search tasks by keyword
- **shrimp_add_task** — Create a new task (any nesting depth)
- **shrimp_update_task** — Update task title, notes, due date, category
- **shrimp_complete_task** — Toggle task completion
- **shrimp_archive_task** — Archive a task and children
- **shrimp_restore_task** — Restore an archived task
- **shrimp_move_task** — Reparent or reorder a task
- **shrimp_delete_task** — Permanently delete a task
- **shrimp_batch** — Execute up to 50 operations at once
- **shrimp_feedback** — Submit feedback to the SHrimp team
- **shrimp_status** — Check connection mode (local or paired)
- **shrimp_pair** — Pair with a SHrimp account via 6-digit code

**Paired mode only (requires iOS app):**
- **shrimp_get_prompt** — Read prompt template sections
- **shrimp_update_prompt** — Update prompt sections
- **shrimp_get_provider** — Read AI provider configuration
- **shrimp_update_provider** — Update AI provider settings
- **shrimp_pipeline** — Read device activity log
- **shrimp_inbox** — Read incoming items from email, shares, etc.

## What makes it different

- Zero-friction start — no signup, no API key, works immediately
- Unlimited nesting depth — complex project hierarchies, not flat lists
- Batch ops — up to 50 operations at once
- Local-first storage — fast, offline, private
- Optional cloud sync via the SHrimp iOS app
- Free, personal-first, no subscription

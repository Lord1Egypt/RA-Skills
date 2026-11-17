---
name: taskhold
description: Work from the task list the user shares with their coding agents through the Taskhold MCP server (https://taskhold.com/api/mcp, Bearer key from a Taskhold setup URL). Use at the start of a coding session and when the user says "work on the next task", "what's next", "what's on my list", "pick up my next todo", "check my task list", "file this as a task", "add a TODO for later", "put this on the backlog", "remind me to fix this later", "mark that done", "leave a note on the task", "what did the agent do", "turn these TODO comments into tasks", "what's in progress", or "I'm blocked on this". Also use when you need the human to decide something (block the task with a question). For the session's built-in todo checklist or a repo TODO.md the user points at, use those directly. For production errors and crash reports, use the user's error tracker.
---

# Taskhold

Taskhold is a hosted task list shared by a person and their coding agents. The person adds and orders tasks in a web app (https://taskhold.com/dashboard). You read and update the same list through the `taskhold_*` MCP tools. Every change you make is recorded as an agent change, so the person can see what you did.

## Not connected yet?

If no `taskhold_*` tools are available, tell the user to open Taskhold > Settings, make a setup URL, and paste it to you with "set this up". Fetch that URL: it is markdown with an API key and the exact config for your client. Do not invent a key.

## Session start

1. `taskhold_get_current`. If a task is in progress, it was probably left by an earlier session: read it with `taskhold_get` (notes included) and continue it.
2. Otherwise `taskhold_list` with `status: "todo"` and take the highest priority (urgent, high, medium, low). If the repo you're in matches a project, prefer tasks in that project (`taskhold_list_projects`, then filter by `project_id`).
3. `taskhold_start` before you begin, so other agents skip it.

## While working

- `taskhold_add_note` at useful checkpoints: what you found, what you changed, what's next. A future session reads these if this one ends.
- Start notes with your client name (for example "Claude Code:") when the user runs several agents. Taskhold marks changes as agent, not which agent.
- Need a decision, credentials, or a review? `taskhold_block` with a specific question as the reason, then move to the next todo. Don't guess on anything destructive.

## Finishing

- `taskhold_complete` with a summary: what changed, which files, how you checked it.
- Bugs or TODOs you noticed but shouldn't fix now: `taskhold_create`, or `taskhold_create_from_todo` with `file_path` and `line_number`. Use priority low unless it's a real bug.

## Tools

| Tool | Use |
|---|---|
| taskhold_get_current | Task in progress |
| taskhold_list | Tasks by status/priority/project |
| taskhold_get | One task with notes |
| taskhold_search | Text search |
| taskhold_create / taskhold_create_from_todo | New task / from a code TODO |
| taskhold_start / taskhold_complete | Claim / finish with summary |
| taskhold_block / taskhold_unblock | Block with reason / unblock |
| taskhold_add_note | Progress note |
| taskhold_update / taskhold_set_priority | Edit |
| taskhold_list_projects / taskhold_list_labels / taskhold_get_summary | Context |

## Don't

- Don't paste the API key into chat, commits or task text.
- Don't mark a task complete if you only partly did it; add a note and block or leave it in progress.
- Don't put secrets or large code blocks in tasks; file path and line number are enough.

Pricing and setup for the person: https://taskhold.com ($12/month or $120/year, 7-day trial).

---
name: session-cleanup
description: Clean up stale or unwanted subagent sessions from OpenClaw webchat sidebar. Use when subagent sessions persist in the UI after completion, when the sidebar is cluttered with old subagent entries, or when the user asks to remove/clear/delete subagent sessions from the chat interface.
---

# Session Cleanup

Remove stale subagent session entries from OpenClaw's `sessions.json` index so they disappear from the webchat sidebar.

## When to Use

- Subagent sessions remain visible in webchat sidebar after completion
- User asks to "remove subagent", "clear subagent list", "delete subagent sessions"
- Sidebar is cluttered with old subagent entries

## How It Works

OpenClaw tracks sessions in `~/.openclaw/agents/<agent>/sessions/sessions.json`. Subagent entries with missing transcript files are "ghost" sessions that still show in the UI. This skill removes those entries from the index.

## Usage

### Quick Clean (remove stale sessions only)

```bash
python3 scripts/cleanup_sessions.py
```

Removes subagent sessions whose transcript `.jsonl` files no longer exist on disk.

### Remove ALL Subagent Sessions

```bash
python3 scripts/cleanup_sessions.py --all
```

Removes every subagent session entry regardless of transcript status.

### Dry Run (preview only)

```bash
python3 scripts/cleanup_sessions.py --dry-run
```

Shows what would be removed without making changes.

### Target Specific Agent

```bash
python3 scripts/cleanup_sessions.py --agent main
```

Only clean sessions for the `main` agent.

## After Cleanup

**Always restart the gateway** for changes to take effect:

```
Use the gateway tool: action=restart
```

Or via CLI: `openclaw gateway restart`

Then refresh the webchat page.

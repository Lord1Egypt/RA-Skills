---
name: sessions-manager
description: Manage OpenClaw agent sessions - list active/completed sessions, view session details, and delete sessions by ID. Use when you need to inspect session state, clean up old sessions, or manage multiple concurrent sessions.
---

# Sessions Manager

Manage OpenClaw agent sessions through CLI commands.

## Commands

### List Sessions

List all sessions with their status, model, and duration:

```bash
python3 ~/.openclaw/workspace/skills/sessions-manager/scripts/sessions_cli.py list
```

For verbose output (includes channel info):

```bash
python3 ~/.openclaw/workspace/skills/sessions-manager/scripts/sessions_cli.py list -v
```

### Delete Session

Delete a session by session ID or session key:

```bash
python3 ~/.openclaw/workspace/skills/sessions-manager/scripts/sessions_cli.py delete <session-id-or-key>
```

Example:
```bash
python3 ~/.openclaw/workspace/skills/sessions-manager/scripts/sessions_cli.py delete agent:main:subagent:5adb35d1-d8e3-4ab7-b9b9-c69a7f891fb3
```

## Output Format

The `list` command shows:
- 📌 Session key (e.g., `agent:main:main`, `agent:main:subagent:xxx`)
- Session ID (UUID)
- Label (if set, e.g., "bsv-lsp 常量展开实现")
- Status (running, completed, timeout, etc.)
- Model being used
- Start time
- Duration

## Session Files

Sessions are stored in:
- **Metadata:** `~/.openclaw/agents/main/sessions/sessions.json`
- **History:** `~/.openclaw/agents/main/sessions/<session-id>.jsonl`

The `delete` command removes both the metadata entry and the history file.

## Use Cases

1. **Debug stuck sessions** - Check which subagents are still running
2. **Clean up old sessions** - Remove completed or timed-out sessions
3. **Monitor concurrent work** - See what subagents are active
4. **Free resources** - Delete sessions that are no longer needed

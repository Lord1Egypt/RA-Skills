---
name: session
description: Integrated skill for Claude Code session management. id - look up current session ID + keyword session search, import - import session, summarize - summarize session, analyze - session stats/analysis, classify - classify/organize sessions, compress - compress session, destroy - delete current session, repair - restore session structure (chain, tool_result), rename - assign custom title to session, Use when: "session ID", "current session", "session id", "get session", "session analysis", "session classify", "session compress", "session delete", "session repair", "chain repair", "session name", "name session", "session search", "find session", "which session", "session import", "session analyze", "session classify", "session compress", "session repair", "session rename", "chain repair"
---

# Session

Integrated skill for managing Claude Code sessions.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| analyze | Session statistics, tool usage patterns, optimization insights | [analyze.md](./analyze.md) |
| classify | Classify project sessions (delete/keep/extract) | [classify.md](./classify.md) |
| compress | AI-compress sessions via UTCP/code-mode | [compress.md](./compress.md) |
| destroy | Delete current session and restart IDE | [destroy.md](./destroy.md) |
| id | Look up current session ID (UUID) | [id.md](./id.md) |
| import | Pipeline session data to other agents/skills | [import.md](./import.md) |
| rename | Assign and look up custom title for session | [rename.md](./rename.md) |
| repair | Restore session structure (chain, tool_result, UUID) | [repair.md](./repair.md) |
| summarize | View and summarize conversation content from other sessions | [summarize.md](./summarize.md) |

## Quick Reference

### Summarize (View/Summarize Sessions)

```bash
/session summarize                 # select project/session then summarize
/session summarize <session_id>    # summarize a specific session
```

[Detailed guide](./summarize.md)

### Import (Pipeline Delivery)

```bash
/session import --hookify          # deliver to hookify
/session import --analyze          # analysis pipeline
/session import --to <agent>       # deliver to specific agent
```

[Detailed guide](./import.md)

### Analyze (Session Analysis)

```bash
/session analyze                   # analyze current session
/session analyze <session_id>      # analyze specific session
/session analyze --sync            # sync to Serena memory
```

[Detailed guide](./analyze.md)

### Classify (Session Classification)

```bash
/session classify                  # classify current project sessions
/session classify --depth=medium   # required when classifying sessions scheduled for split
/session classify --execute        # execute immediately after classification
```

> ⚠️ **--depth=medium or higher required before split** — fast only reads the last 3 messages, so it may miss different topics at the end of the session.

[Detailed guide](./classify.md)

### Compress (Session Compression)

```bash
/session compress <session_id>    # compress specific session
/session compress                 # batch compress sessions containing "hookEvent":"Stop"
```

Register claude-sessions-mcp with UTCP, then call via code-mode.

[Detailed guide](./compress.md)

### ID (Session ID Lookup + Keyword Search)

```bash
/session id                          # look up current session ID
/session id Makefile remove          # search sessions by keyword
/session id --today ansible/Makefile # search only today's sessions by file path
```

Current session ID: output unique marker → search JSONL with `find-session-id.sh` → return UUID
Keyword search: grep project JSONL → sort by modification time descending → return most recent matching session

[Detailed guide](./id.md)

### Destroy (Delete Session)

```bash
scripts/destroy-session.sh
```

[Detailed guide](./destroy.md)

### Repair (Session Recovery)

```bash
/session repair                          # select session, then validate and repair
/session repair <session_id>             # repair specific session
/session repair --dry-run                # preview only
/session repair --check-only             # validate only (no repair)
```

Repair targets:
- Broken chain (missing parentUuid)
- Orphan tool_result (no matching tool_use)
- Duplicate UUIDs

[Detailed guide](./repair.md)

### Rename (Naming a Session)

```bash
# Assign a name to a specific session
bash ~/.claude/skills/session/scripts/rename-session.sh <session_id> "name"

# Assign a name to the latest session in the current project
bash ~/.claude/skills/session/scripts/rename-session.sh "name"

# Check current title
bash ~/.claude/skills/session/scripts/rename-session.sh --show <session_id>

# List named sessions in current project
bash ~/.claude/skills/session/scripts/rename-session.sh --list
```

[Detailed guide](./rename.md)

## Project Name Conversion Rules

| Actual Path | Project Name |
|-------------|--------------|
| `/Users/david/works/.vscode` | `-Users-david-works--vscode` |
| `/Users/david/Sync/AI` | `-Users-david-Sync-AI` |

Rule: `/` → `-`, remove leading `/` from path

## Requirements

- claude-code-sessions MCP server required
- Serena MCP server (when using analyze --sync)

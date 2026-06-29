---
name: claude-session
description: |
  Claude Code session management. Topics — id (current session UUID), list (enumerate sessions), search (keyword + result validation), import, summarize, analyze (stats), archive (move to ~/.claude/projects/.bak/ with flat naming), classify, split (topic boundaries), compress (UTCP/code-mode), destroy, install (hook), migrate (project to worktree), move (with cwd update), purge (dead sessions), rename (custom title), repair (chain/tool_result/UUID), url (web URL). Use when: "session id", "current session", "session list", "list sessions", "session search", "find session", "session classify", "session compress", "session migrate", "session move", "session repair", "chain repair", "session rename", "session split", "session purge", "dead session", "session url", "session analyze", "session import", "session summarize", "session archive", "archive session", "worktree session", "session cleanup"
metadata:
  author: es6kr
  version: "0.1.5"
---

# Session

Integrated skill for managing Claude Code sessions.

## Topic Dispatch

**When this skill is invoked with a topic specifier (e.g., `/claude-session id` or `Skill("claude-session", "id")`), load and follow only the matching topic file (`id.md`). Do not echo the Topics table or summarize other topics in the response.** The Topics table below is an index for invocations without a topic specifier — it is not user-facing output when a topic is named.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| analyze | Session statistics, tool usage patterns, optimization insights | [analyze.md](./analyze.md) |
| archive | Move a completed session out of the active project key to `~/.claude/projects/.bak/<project-key>_<uuid>.jsonl` (flat naming, single backup root) | [archive.md](./archive.md) |
| classify | Classify project sessions (delete/keep/extract) | [classify.md](./classify.md) |
| split | Analyze topic boundaries and recommend session split points | [split.md](./split.md) |
| compress | AI-compress sessions via UTCP/code-mode | [compress.md](./compress.md) |
| destroy | Delete current session and restart IDE | [destroy.md](./destroy.md) |
| id | Look up current session ID (UUID) | [id.md](./id.md) |
| import | Pipeline session data to other agents/skills | [import.md](./import.md) |
| install | Register session-id-inject hook in settings.json | [install.md](./install.md) |
| list | Enumerate current-project sessions (UUID + mtime + size) | [list.md](./list.md) |
| migrate | Move sessions between projects (main repo → worktree) | [migrate.md](./migrate.md) |
| move | Move specific sessions by ID to another project + update cwd | [move.md](./move.md) |
| purge | Delete dead sessions (hook-only, no assistant response) permanently | [purge.md](./purge.md) |
| rename | Assign and look up custom title for session | [rename.md](./rename.md) |
| repair | Restore session structure (chain, tool_result, UUID) | [repair.md](./repair.md) |
| search | Keyword session search with result validation (verb/path/class checks) | [search.md](./search.md) |
| summarize | View and summarize conversation content from other sessions | [summarize.md](./summarize.md) |
| url | Generate claude-sessions web URL from session ID | [url.md](./url.md) |

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

### Archive (Move Session Out of Active Project)

```bash
/session archive <session_id>                                     # move to ~/.claude/projects/.bak/<project-key>_<uuid>.jsonl
bash ~/.claude/skills/claude-session/scripts/archive-session.sh <session_id>           # direct script call
bash ~/.claude/skills/claude-session/scripts/archive-session.sh <session_id> --dry-run # preview only
```

Moves to `~/.claude/projects/.bak/<project-key>_<uuid>.jsonl` (flat naming, single backup root shared with transient backups). UUID portion preserved unchanged. Updates `INDEX.md` ledger.

[Detailed guide](./archive.md)

### Split (Topic Split Recommendation)

```bash
/session split                     # Recommend split for current conversation
/session split <session_id>        # Recommend split for specific session
/session split --execute           # Execute recommendation immediately
```

[Detailed guide](./split.md)

### Classify (Session Classification)

```bash
/session classify                  # classify current project sessions
/session classify --depth=medium   # required when classifying sessions scheduled for split
/session classify --execute        # execute immediately after classification
```

> ⚠️ **--depth=medium or higher required before split** — fast only reads the last 3 messages, so it may miss different topics at the end of the session.

> 🔍 **RAG MCP auto-detection** — If a vector store MCP (Qdrant / Chroma / Weaviate / Pinecone / etc.) is registered in the current context, classify additionally recommends sessions worth saving to RAG. Vendor-agnostic — uses whichever store tool is detected. See Section 8 of classify.md.

[Detailed guide](./classify.md)

### Move (Move Specific Sessions by ID)

```bash
/session move <session_id> <target_project_path>                   # default: --cwd-mode first
/session move <session_id> <target_project_path> --cwd-mode all    # update all cwd occurrences
/session move <session_id> <target_project_path> --cwd-mode first  # update only first cwd
```

Move explicit session IDs to another project directory and update `cwd` references via Python script. Cross-platform (Windows + macOS/Linux). Unlike `migrate`, no classification — just direct move.

[Detailed guide](./move.md)

### Migrate (Move Sessions Between Projects)

```bash
/session migrate                           # classify + move code sessions to worktree
/session migrate --dry-run                 # preview only
/session migrate <source> <target>         # specify source/target projects
```

Classifies sessions as CODE/INFRA/TINY/READ, then moves CODE sessions to worktree project and optionally deletes TINY sessions.

[Detailed guide](./migrate.md)

### Compress (Session Compression)

```bash
/session compress <session_id>    # compress specific session
/session compress                 # batch compress sessions containing "hookEvent":"Stop"
```

Register claude-sessions-mcp with UTCP, then call via code-mode.

[Detailed guide](./compress.md)

### List (Enumerate Current-Project Sessions)

```bash
/session list                       # list current-project sessions (UUID + mtime + size)
/session list --all-projects        # summary across all projects
/session list --limit 20            # top N by mtime
```

Non-destructive enumeration. For categorization or cleanup, use `classify` or `purge` instead.

[Detailed guide](./list.md)

### ID (Current Session ID Lookup)

```bash
/session id                          # look up current session ID
```

**Current session ID — fast path (handle here, do NOT read id.md):**

1. **Hook injection (preferred)** — Look for `Current session ID: {uuid}` in conversation context. SessionStart hook `~/.claude/hooks/session-id-inject.sh` injects it as `additionalContext` at session start. If present, return the UUID immediately.
2. **File path UUIDs** — Scan recent tool results for UUID pattern `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` in subagent/task/transcript paths. Return if found.
3. **Marker fallback** — Only if 1 & 2 fail: read `id.md` for the marker→grep procedure.

[Detailed guide](./id.md)

### Search (Keyword Session Search)

```bash
/session search Makefile remove          # find sessions by keyword
/session search --today ansible/Makefile # only sessions modified today
/session id <keyword>                    # legacy alias — routed to search
```

Always run the result-validation gate (verb ambiguity, artifact location, action class) before reporting matches as the answer to "which session did X" — a misplaced artifact path is a "task orphaned" signal, not a successful match.

[Detailed guide](./search.md)

### Destroy (Delete Session)

```bash
scripts/destroy-session.sh
```

[Detailed guide](./destroy.md)

### Purge (Dead Session Cleanup)

```bash
/session purge                    # dry-run: list dead sessions in current project
/session purge <project_name>     # dry-run: specific project
/session purge --all              # dry-run: all projects
```

Dead session = 10 lines or fewer + no `"type":"assistant"` response.
Script: `scripts/purge-dead-sessions.sh <project_name> [--delete]`

[Detailed guide](./purge.md)

### Repair (Session Recovery)

```bash
/session repair                          # default: current session (uses hook-injected ID)
/session repair <session_id>             # repair specific session
/session repair --dry-run                # preview only
/session repair --check-only             # validate only (no repair)
```

**Primary script** (full pipeline: backup → dedup → 400 error → orphan tool_result → chain → validate):

```bash
python3 ~/.claude/skills/claude-session/scripts/repair-session.py <session_file>
python3 ~/.claude/skills/claude-session/scripts/repair-session.py <session_file> --dry-run
```

Repair targets:
- Broken chain (missing parentUuid)
- Orphan tool_result (no matching tool_use)
- Duplicate UUIDs / duplicate message.id (Syncthing conflicts)
- API 400 error lines (incl. invalid surrogate pair / thinking-block signature)

[Detailed guide](./repair.md)

### Rename (Naming a Session)

**Current session** → output a copyable `/rename` list (NO script, NO AskUserQuestion):

```
Session name suggestions:

1. `/rename Candidate 1`
2. `/rename Candidate 2`
3. `/rename Candidate 3`
```

`/rename` is a Claude Code built-in command — it **cannot** be invoked via Bash or the Skill tool. The user copies and pastes the desired line. **Do NOT call `rename-session.sh` for the current session** (it is reserved for other sessions by ID).

**Other session** (session ID specified) → apply via script:

```bash
# Assign a name to a specific session
bash scripts/rename-session.sh <session_id> "name"

# Check current title
bash scripts/rename-session.sh --show <session_id>

# List named sessions in current project
bash scripts/rename-session.sh --list
```

[Detailed guide](./rename.md)

## Project Name Conversion Rules

| Actual Path | Project Name |
|-------------|--------------|
| `/Users/es6kr/works/.vscode` | `-Users-es6kr-works--vscode` |
| `/Users/es6kr/Sync/AI` | `-Users-es6kr-Sync-AI` |

Rule: all non-alphanumeric characters → `-` (i.e., `replace(/[^a-zA-Z0-9]/g, '-')`)

## Requirements

- claude-sessions-mcp MCP server required
- Serena MCP server (when using analyze --sync)


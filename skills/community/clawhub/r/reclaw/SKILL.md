---
name: reclaw
description: "Use when accessing memory, recording information, searching prior context, or managing subjects."
read_when:
  - You need to find something from a previous session
  - You want to record a decision, fact, task, or question
  - You're asked about what you remember or know
  - You need to check or update the subject registry
metadata:
  openclaw:
    homepage: https://github.com/maxpetretta/reclaw
    requires:
      bins:
        - openclaw
---

# Reclaw Memory System

Reclaw is an append-only event log that replaces daily memory files. It assumes the current OpenClaw environment already has the Reclaw plugin installed. All memory lives in `log.jsonl` as structured entries. Extraction happens automatically at session end — you don't write to the log directly. Your job is to state information clearly in conversation so the extraction hook captures it.

## How Memory Works

1. **MEMORY.md** is auto-loaded into every session. It has a manual section (goals, preferences) and a generated Reclaw memory snapshot updated nightly.
2. **Reclaw session summary** is written into `MEMORY.md` after each session extraction.
3. **Subject markdown projections** are generated under `~/.openclaw/reclaw/memory/` so OpenClaw can semantically index event-log content through its builtin markdown memory path.
4. **`memory_search`** finds entries by keyword, type, subject, or status when the Reclaw plugin has registered that tool in the current OpenClaw environment, and can hit semantic results from `MEMORY.md` plus generated subject projections.
5. **`memory_get`** retrieves a specific entry by ID, reads `MEMORY.md`, or fetches a full session transcript when the Reclaw plugin has registered that tool in the current OpenClaw environment.

Start with what's already in context (steps 1-3). Only call tools when you need something specific.

## Entry Types

| Type | What it captures | Key detail |
|---|---|---|
| `task` | Action items, follow-ups | Has `status`: `open` or `done` |
| `fact` | User-specific information learned | Preferences, events, observations, milestones |
| `decision` | A choice with reasoning | Use `detail` for the "why" |
| `question` | An unresolved open loop | Resolved by later entries on the same subject |
| `session_summary` | Session boundary state | One per session, summarizes what's in-flight |

## Subjects

Every non-`session_summary` entry has a `subject` — a kebab-case slug like `auth-migration` or `reclaw`. Subjects are tracked in a registry with a type: `project`, `person`, `system`, or `topic` (default).

When discussing something new, use a clear kebab-case slug. The extraction hook auto-creates subjects it hasn't seen. To explicitly manage subjects:

```bash
# List all subjects
openclaw reclaw subjects list

# Add a subject with a type
openclaw reclaw subjects add auth-migration --type project
openclaw reclaw subjects add alice-chen --type person

# Rename a subject (updates registry and all log entries)
openclaw reclaw subjects rename old-slug new-slug
```

## Using `memory_search`

Combines structured log filters with keyword search and semantic search over `MEMORY.md` plus generated subject projections.

```
# Keyword search
memory_search({"query": "webhook retries"})

# Structured filters
memory_search({"type": "decision", "subject": "auth-migration"})
memory_search({"type": "task", "status": "open"})
memory_search({"type": "question"})

# Combined
memory_search({"query": "backoff", "type": "fact", "subject": "auth-migration"})
```

At least one of `query`, `type`, `subject`, or `status` is required.

## Markdown Projections

Reclaw keeps one generated markdown file per subject under `~/.openclaw/reclaw/memory/`. These files are derived from `log.jsonl` and exist so OpenClaw's builtin markdown indexer can semantically search event-log content.

- Treat projection files as generated output — don't manually edit them
- Successful live extraction refreshes touched subject projections automatically
- Successful non-dry-run imports refresh the full projection set automatically
- If the index seems stale, rebuild with `openclaw reclaw projection refresh`

## Using `memory_get`

Three lookup modes based on the `path` value:

```
# By entry ID (12-char nanoid from search results)
memory_get({"path": "r7Wp3nKx_mZe"})

# By session transcript (from an entry's session field)
memory_get({"path": "session:abc123def456"})

# By file path
memory_get({"path": "MEMORY.md"})
```

Reading an entry by ID increments its usage score, which helps it persist in the nightly memory snapshot.

## Citations

When referencing a prior event in conversation, cite it as `[<12-char-id>]` (e.g., `[r7Wp3nKx_mZe]`). This format is tracked for usage scoring — cited entries are more likely to appear in future memory snapshots.

## Corrections and Updates

The log is append-only. To correct something:
- State the correction clearly in conversation. Extraction writes a new entry on the same subject.
- To mark a task done, say so explicitly. Extraction emits a new `task` entry with `status: "done"`.
- To answer a question, discuss the resolution. Extraction captures the answer as a `fact` or `decision`.

Old entries are never modified. Current state is reconstructed by reading a subject's entries chronologically.

## Hard Filter

Only user-specific information belongs in the log. Ask: "Would I need to know this person to know this?" If a general-purpose LLM could produce the content without user context, it should not be extracted. No generic knowledge, no dependency lists, no boilerplate.

## CLI Commands

```bash
# Recent log entries
openclaw reclaw log
openclaw reclaw log --type decision --subject auth-migration --limit 10

# Search with filters
openclaw reclaw search "webhook"
openclaw reclaw search --type task --status open
openclaw reclaw search --subject auth-migration --from 2026-02-01 --to 2026-03-01

# Trace a subject's chronological history
openclaw reclaw trace
openclaw reclaw trace --subject auth-migration
openclaw reclaw trace <entry-id>

# Subject management
openclaw reclaw subjects list
openclaw reclaw subjects add <slug> --type <project|person|system|topic>
openclaw reclaw subjects rename <old-slug> <new-slug>

# Refresh generated subject markdown projections
openclaw reclaw projection refresh
openclaw reclaw projection list

# Regenerate the MEMORY.md memory snapshot now
openclaw reclaw snapshot refresh

# Force-refresh MEMORY.md session summary block from log
openclaw reclaw summary refresh

# Import historical conversations
openclaw reclaw import <chatgpt|claude|grok|openclaw> <file>
openclaw reclaw import status
openclaw reclaw import resume <jobId>

# Setup
openclaw reclaw init
openclaw reclaw verify
openclaw reclaw uninstall
```

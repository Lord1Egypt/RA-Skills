---
name: smart-memory-plus
description: >
  Complete memory system for OpenClaw agents. Combines enhanced memory management
  (WAL protocol, type classification, temporal decay, session cache) with context
  compression (conversation digests, auto-injection). Zero external dependencies.
  Use when: managing MEMORY.md, extracting insights from conversations, compressing
  long sessions, searching memories, tracking task state, or when user says
  "remember this", "compact", "what do you know about X", "clean up memories".
---

# Smart Memory Plus

Unified memory management + context compression for OpenClaw. Zero external dependencies.

> ⚠️ **Conflict Warning**: This skill replaces both `smart-memory` and `context-compactor`.
> Do NOT install alongside either of those skills — they share the same files
> (`SESSION-STATE.md`, `memory/`, `MEMORY.md`) and will cause write conflicts.

## Requirements

- **Runtime**: Python 3.10+ (standard library only), Bash 4.0+ (health/extract scripts only)
- **OS**: Linux, macOS
- **Environment variables** (all optional, with defaults):
  - `OPENCLAW_WORKSPACE` — Workspace root (default: `~/.openclaw/workspace`)
  - `OPENCLAW_SESSION_ID` — Session identifier for temp cache (default: `default`)

## Security

### Write Restrictions (Hard Rules)
The agent MUST use the provided scripts for ALL writes. Direct file writes are FORBIDDEN.

| File | Required Script | Forbidden |
|------|----------------|-----------|
| `SESSION-STATE.md` | `session_state.py` (WAL protocol) | Direct write/overwrite |
| `memory/compacts/*.md` | `compact_session.py --write` | Direct write/overwrite |
| `memory/*.md` (daily notes) | `extract_memories.sh --auto` or append via script | Direct overwrite |
| `MEMORY.md` | `memory_decay.py --promote-only` | Direct overwrite |
| `/tmp/openclaw-session-*.json` | `session_cache.py` | Direct write |

**Critical**: Never use the agent's file-write tool directly on memory files. Always pipe through scripts — they enforce sanitization, deduplication, and append-only behavior.

The agent MUST NOT write to:
- Any directory outside the workspace
- System directories (/etc, /usr, /var, /tmp except session cache)
- User home directory root (~/.ssh, ~/.config, ~/.aws, etc.)
- Any `.*` dotfile or dotdir in workspace root

### Sensitive Data Protection
All write commands automatically reject inputs matching:
- API keys/tokens (OpenAI `sk-*`, GitHub `ghp_*`, ClawHub `clh_*`)
- Passwords (`password=`, `passwd:`, etc.)
- Private keys (`-----BEGIN PRIVATE KEY-----`)

This is a **hard block** at the script level — the agent cannot bypass it.

### Privacy Boundaries
- Compacts must NOT contain: file paths, internal URLs, IPs, passwords, tokens
- Use placeholders: `<REDACTED_PATH>`, `<REDACTED_URL>`, `<INTERNAL_URL>`
- **All data stays local** — all scripts make zero network calls, no LLM usage

## Memory Layers

| Layer | File | Purpose | Lifetime |
|-------|------|---------|----------|
| **HOT RAM** | `SESSION-STATE.md` | Current task, context, decisions | Session (survives compaction) |
| **DAILY** | `memory/YYYY-MM-DD.md` | Raw daily notes with type tags | 90 days → archive |
| **CURATED** | `MEMORY.md` | Promoted long-term facts | Permanent |
| **COMPACT** | `memory/compacts/YYYY-MM-DD-HHMM.md` | Session digests | 30 max, auto-cleanup |
| **GRAPH** | `memory/.index/graph.db` | Entity-relation knowledge graph | Rebuild from source |
| **ARCHIVE** | `memory/archive/YYYY-MM/` | Stale daily files | Forever (compressed) |
| **CACHE** | `/tmp/openclaw-session-*.json` | Session temp data | Session end / reboot |

## Quick Reference

### Memory Management
| Action | Script |
|--------|--------|
| WAL shortcut | `scripts/wal task/decide/context/pending/done/blocker/get/snapshot/restore` |
| Set current task | `scripts/wal task "description"` |
| Log a decision | `scripts/wal decide "chose X over Y"` |
| Add context | `scripts/wal context key value` |
| Session cache | `python3 scripts/session_cache.py set/get/list/clear` |
| Classify memories | `python3 scripts/classify_memory.py --summary/--apply` |
| Decay & archive | `python3 scripts/memory_decay.py --dry-run/--promote-only` |
| Health report | `bash scripts/memory_health.sh` |

### Search & Relations
| Action | Script |
|--------|--------|
| Full index rebuild | `python3 scripts/memory_search_bm25.py build` |
| Incremental update | `python3 scripts/memory_search_bm25.py update` |
| Search memories (BM25) | `python3 scripts/memory_search_bm25.py search "query" [--top N]` |
| Index status | `python3 scripts/memory_search_bm25.py status` |
| Find related entries | `python3 scripts/classify_memory.py --related "query" [--top N]` |
| Build knowledge graph | `python3 scripts/memory_graph.py build` |
| Graph relations | `python3 scripts/memory_graph.py related "entity" [--depth N]` |
| Graph stats | `python3 scripts/memory_graph.py stats` |
| Raw graph query | `python3 scripts/memory_graph.py query "SELECT ..."` |

### Context Compression
| Action | Script |
|--------|--------|
| Extract compact (stdin) | `python3 scripts/compact_session.py --extract` |
| Write compact (stdin) | `python3 scripts/compact_session.py --write` |
| List compacts | `python3 scripts/compact_session.py --list` |
| Read latest compact | `python3 scripts/compact_session.py --latest` |
| Compact stats | `python3 scripts/compact_session.py --stats` |

## WAL Protocol (Write-Ahead Log)

**Critical rule: Write BEFORE responding.**

When the user provides information that should be remembered:

1. **Write to SESSION-STATE.md** (via `session_state.py`)
2. **Then** respond to the user

This prevents context loss if compaction, crash, or restart happens between response and write.

| User Action | WAL Write |
|-------------|-----------|
| States a preference | `session_state.py context "pref" "value"` |
| Makes a decision | `session_state.py decide "chose X"` |
| Gives a deadline | `session_state.py context "deadline" "date"` |
| Corrects agent | `session_state.py decide "correction: X not Y"` |
| Assigns task | `session_state.py task "description"` |
| Mentions blocker | `session_state.py blocker "description"` |

## Memory Types

All entries tagged with a type prefix:

- `[PREF]` — User preferences, habits, style
- `[PROJ]` — Project context, active work, goals
- `[TECH]` — Technical details, configs, system knowledge
- `[LESSON]` — Lessons learned, errors, corrections
- `[PEOPLE]` — People, relationships, social context
- `[TEMP]` — Session-scoped, auto-expires

## Core Workflows

### Session Start
1. Read `SESSION-STATE.md` for current task/context
2. Search for relevant context:
   - `python3 scripts/memory_search_bm25.py build` (if index is stale or missing)
   - `python3 scripts/memory_search_bm25.py search "current topic"` (semantic search)
   - Also use `memory_search` (OpenClaw built-in tool) as complementary search
3. Check for recent compacts: `python3 scripts/compact_session.py --latest`
   - If output exists, read it and use relevant parts as context for the session
   - This is a manual agent step — the skill does not auto-inject
4. Check `memory/YYYY-MM-DD.md` for today's activity

### During Conversation (WAL)
1. User provides actionable info → write to SESSION-STATE.md FIRST
2. Important facts → append to `memory/YYYY-MM-DD.md` with type tag
3. Use `session_cache.py` for transient session data

### Session End (Compaction)
1. Update `SESSION-STATE.md` with final state
2. If conversation > 50 turns or user says "compact":
   - Draft compact content (decisions, facts, pending, blockers)
   - Pipe through security checks: `echo "content" | python3 scripts/compact_session.py --write`
   - Include `[TYPE]` tags per smart-memory classification
3. Promote durable items from daily notes to `MEMORY.md`

### Periodic Maintenance
- Run `memory_decay.py` when MEMORY.md > 200 lines or 50+ daily files
- Run `classify_memory.py` to tag orphaned entries
- Run `memory_search_bm25.py update` to refresh search index after edits
- Run `memory_graph.py build` to refresh knowledge graph
- Archive daily files older than 90 days
- Compact auto-cleanup keeps only last 30

## Agent Behavior

### Auto-Extract When
- User shares preference, opinion, or personal fact
- Project decision is made or changed
- Error encountered and resolved (→ LESSON)
- New people, tools, or workflows mentioned

### Extraction Mode
- `extract_memories.sh --auto "text"` — keyword matching, zero token cost, fully local

### Compaction Mode
- `compact_session.py --extract` — regex-based extraction, zero token cost, fully local

### Do NOT Extract/Compact
- Passwords, tokens, API keys, credentials (scripts hard-block these)
- Private conversations about third parties not relevant to work
- Speculation or uncertain information
- Transient state ("user is currently looking at page X")
- Information the user explicitly said not to remember

## Scripts

| Script | Language | Purpose | Security |
|--------|----------|---------|----------|
| `session_state.py` | Python | HOT RAM working memory (WAL) | Sensitive data filter + sanitization |
| `session_cache.py` | Python | Session-scoped temp cache | Sensitive data filter + path-safe IDs |
| `compact_session.py` | Python | Context compression & digests | Path containment + sensitive filter |
| `extract_memories.sh` | Bash | Memory extraction guide & auto-extract | Read-only + sensitive filter (Python) |
| `classify_memory.py` | Python | Keyword + n-gram type classification, related search | Dry-run mode, duplicate check |
| `memory_decay.py` | Python | Temporal decay & LESSON promotion | Dry-run mode |
| `memory_health.sh` | Bash | Health report (stats, orphans, tokens) | Read-only |
| `memory_search_bm25.py` | Python | BM25 semantic search over memories | Local-only, zero network |
| `memory_graph.py` | Python | SQLite knowledge graph (entities + relations) | Local-only, SELECT-only queries |

## References

- `references/extraction_prompt.md` — Extraction prompt template (for agent-internal use)
- `references/compaction_prompt.md` — Compaction prompt template (for agent-internal use)
- `references/decay_rules.md` — Decay/archival rule set
- `references/memory_schema.md` — Full schema and format spec

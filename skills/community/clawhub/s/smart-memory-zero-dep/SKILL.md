---
name: smart-memory
description: >
  Enhanced memory system for agentic workflows. Automatic memory extraction from conversations,
  memory type classification (preference/project/technical/lesson), temporal decay/archival,
  session-scoped temporary cache, and HOT RAM working memory with WAL protocol. Use when
  managing MEMORY.md, extracting insights from conversations, organizing memory files, archiving
  stale memories, searching memories by type, tracking current task state, or when the user says
  "remember this", "what do you know about X", "clean up memories", "what are we working on".
---

# Smart Memory

Enhanced memory management for OpenClaw. Zero external dependencies. Inspired by Claude Code's memdir architecture.

## Requirements

- **Runtime**: Python 3.10+ (standard library only), Bash 4.0+ (health/extract scripts only)
- **OS**: Linux, macOS
- **Environment variables** (all optional, with defaults):
  - `OPENCLAW_WORKSPACE` — Workspace root (default: `~/.openclaw/workspace`)
  - `OPENCLAW_SESSION_ID` — Session identifier for temp cache (default: `default`)

## Security

### Sensitive Data Protection
All write commands (`session_state.py`, `session_cache.py`) automatically reject inputs matching:
- API keys/tokens (OpenAI `sk-*`, GitHub `ghp_*`, ClawHub `clh_*`)
- Passwords (`password=`, `passwd:`, etc.)
- Private keys (`-----BEGIN PRIVATE KEY-----`)

This is a **hard block** at the script level — the agent cannot bypass it. The regex patterns are conservative (high precision, may miss exotic formats); the agent should additionally avoid extracting any credential-like text even if not matched.

### Input Sanitization
- Control characters stripped from all inputs
- Session ID sanitized to alphanumeric/hyphen/underscore only (prevents path traversal)
- Python-based scripts eliminate shell injection risks

### Data Isolation
- All data stays local — no network calls, no cloud uploads
- Session cache uses `/tmp/` with sanitized session ID filenames
- No external dependencies or third-party packages

## Memory Layers

| Layer | File | Purpose | Lifetime |
|-------|------|---------|----------|
| **HOT RAM** | `SESSION-STATE.md` | Current task, context, decisions | Session (survives compaction) |
| **DAILY** | `memory/YYYY-MM-DD.md` | Raw daily notes with type tags | 90 days → archive |
| **CURATED** | `MEMORY.md` | Promoted long-term facts | Permanent |
| **ARCHIVE** | `memory/archive/YYYY-MM/` | Stale daily files | Forever (compressed) |
| **CACHE** | `/tmp/openclaw-session-*.json` | Session temp data | Session end / reboot |

## Quick Reference

| Action | Script |
|--------|--------|
| WAL shortcut (any command) | `scripts/wal task/decide/context/pending/done/blocker/get/snapshot/restore` |
| Set current task | `scripts/wal task "description"` |
| Log a decision | `scripts/wal decide "chose X over Y"` |
| Add context | `scripts/wal context key value` |
| Snapshot & restore | `scripts/wal snapshot` / `scripts/wal restore` |
| Session cache | `python3 scripts/session_cache.py set/get/list/clear` |
| Classify (summary) | `python3 scripts/classify_memory.py --summary` |
| Decay (promote only) | `python3 scripts/memory_decay.py --promote-only` |
| Health report | `bash scripts/memory_health.sh` |

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
2. Run `memory_search` for relevant prior context
3. Check `memory/YYYY-MM-DD.md` for today's activity

### During Conversation (WAL)
1. User provides actionable info → write to SESSION-STATE.md FIRST
2. Important facts → append to `memory/YYYY-MM-DD.md` with type tag
3. Use `session_cache.py` for transient session data

### Session End
1. Update `SESSION-STATE.md` with final state
2. Promote durable items from daily notes to `MEMORY.md`
3. Run `memory_health.sh` periodically to check hygiene

### Periodic Maintenance
- Run `memory_decay.py` when MEMORY.md > 200 lines or 50+ daily files
- Run `classify_memory.py` to tag orphaned entries
- Archive daily files older than 90 days

## Agent Behavior

### Auto-Extract When
- User shares preference, opinion, or personal fact
- Project decision is made or changed
- Error encountered and resolved (→ LESSON)
- New people, tools, or workflows mentioned

### Extraction Modes
- **Keyword mode** (default): `extract_memories.sh --auto "text"` — zero token cost, pure Python
- **LLM mode** (opt-in): Use `references/extraction_prompt.md` template — costs tokens, better quality
- Use keyword mode for most conversations; LLM mode only for long/complex sessions (20+ turns)

### Do NOT Extract
- Passwords, tokens, API keys, credentials (scripts hard-block these)
- Private conversations about third parties not relevant to work
- Speculation or uncertain information ("user might prefer X")
- Transient state ("user is currently looking at page X")
- Information the user explicitly said not to remember

### Auto-Decay When
- MEMORY.md exceeds 200 lines
- memory/*.md totals > 50 files
- On heartbeat if configured

## File Format

### MEMORY.md
```markdown
## [PREF] Preferences
- Favorite color: 深蓝色

## [PROJ] Active Projects
- 黄金三章: /root/黄金三章/, golden3.killclaw.xyz

## [LESSON] Lessons Learned
- Verify Telegram target before building notification workflows
```

### Daily Notes
```markdown
# 2026-03-31

## [PROJ] 黄金三章
- Fixed scoring display to 10-point scale
```

### SESSION-STATE.md
```markdown
## Current Task
Building smart-memory skill

## Key Context
- **platform**: ClawHub

## Recent Decisions
- **2026-03-31**: Use zero-dependency approach

## Pending Actions
- [ ] Publish to ClawHub
```

## Scripts

| Script | Language | Purpose | Security |
|--------|----------|---------|----------|
| `session_state.py` | Python | HOT RAM working memory (WAL protocol) | Sensitive data filter + sanitization |
| `session_cache.py` | Python | Session-scoped temp key-value cache | Sensitive data filter + path-safe IDs |
| `extract_memories.sh` | Bash | Memory extraction guide and daily file init | Read-only output |
| `memory_health.sh` | Bash | Health report (stats, orphans, token estimate) | Read-only |
| `memory_decay.py` | Python | Temporal decay and archival of stale files | Dry-run mode available |
| `classify_memory.py` | Python | Keyword-based type classification | Dry-run mode available |

## References

- `references/extraction_prompt.md` — LLM prompt for auto-extraction
- `references/memory_schema.md` — Full schema and format spec
- `references/decay_rules.md` — Decay/archival rule set

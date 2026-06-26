# Decay & Archival Rules

## Trigger Conditions

Run memory decay when:
- MEMORY.md exceeds 200 lines
- memory/*.md directory has more than 50 files
- User says "clean up memories", "archive old stuff", "memory hygiene"
- On heartbeat cycle (if configured)

## Daily File Archival

| File Age | Action |
|----------|--------|
| < 30 days | Keep in place |
| 30–89 days | Keep, but flag in health report |
| 90–179 days | Move to `memory/archive/YYYY-MM/` |
| 180–365 days | Move to `memory/archive/YYYY-MM/`, compress summary |
| > 365 days | Move to `memory/archive/YYYY-MM/` |

## Entry-Level Rules

### Permanent (never auto-archive)
- `[PREF]` — User preferences don't expire
- `[LESSON]` — Lessons are permanently valuable

### Time-Bound
- `[PROJ]` — Archive when project is explicitly marked complete
- `[TECH]` — Archive after 365 days if not referenced
- `[PEOPLE]` — Archive after 180 days if not referenced

### Session-Only
- `[TEMP]` — Never write to disk; lives only in session cache

## Promotion Rules

An entry in daily notes deserves promotion to MEMORY.md when:
1. Referenced in 2+ separate conversations
2. User explicitly says "remember this" or "don't forget"
3. It's a project fact (URL, config, architecture decision)
4. It's a strong user preference (confirmed, not assumed)

## Anti-Patterns (What NOT to Store)

- Transient state: "user is currently looking at file X"
- Obvious facts: "user uses a computer"
- Sensitive data: passwords, tokens, API keys (never in memory files)
- Speculation: "user might like X" — only store confirmed preferences
- Redundant info: check MEMORY.md before adding duplicates

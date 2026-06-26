# Memory Schema Reference

## File Structure

```
~/.openclaw/workspace/
├── MEMORY.md                    # Curated long-term memory (promoted entries)
└── memory/
    ├── 2026-03-31.md            # Daily raw notes
    ├── 2026-03-30.md
    └── archive/
        └── 2026-01/
            ├── 2026-01-15.md    # Archived daily notes
            └── ...
```

## MEMORY.md Format

```markdown
# MEMORY.md

## [PREF] Preferences
- Item description

## [PROJ] Active Projects
- Project: description, URL, location

## [LESSON] Lessons Learned
- Lesson description

## [TECH] Technical Notes
- Technical fact

## [PEOPLE] People & Context
- Person: relevant context
```

## Daily Notes Format

```markdown
# YYYY-MM-DD

## [TYPE] Topic
- Entry description
```

## Type Tags

| Tag | Meaning | Retention | Archive Rule |
|-----|---------|-----------|--------------|
| `[PREF]` | User preference | Permanent | Never auto-archive |
| `[PROJ]` | Project context | Until project done | Archive when project marked complete |
| `[TECH]` | Technical detail | 1 year | Archive after 365 days |
| `[LESSON]` | Lesson learned | Permanent | Never auto-archive |
| `[PEOPLE]` | Person context | 6 months | Archive after 180 days |
| `[TEMP]` | Session only | Current session | Never persist |

## Session Cache Schema

Stored in `/tmp/openclaw-session-cache-{session_id}.json`:

```json
{
  "key1": "value1",
  "context:project-x": "current task is implementing feature Y",
  "count:api-calls": "5"
}
```

- Keys are arbitrary strings
- Values are strings (serialize complex objects as JSON strings)
- File auto-deleted when session ends or system reboots
- Not shared between sessions

## Decay Rules

1. Daily files older than 90 days → `memory/archive/YYYY-MM/`
2. `[PROJ]` entries for completed projects → archive immediately
3. `[TECH]` entries older than 365 days → archive
4. `[PEOPLE]` entries older than 180 days → archive
5. `[LESSON]` entries referenced 2+ times → promote to MEMORY.md
6. `[TEMP]` entries → never persist, session-only
7. `[PREF]` entries → permanent, never auto-archive

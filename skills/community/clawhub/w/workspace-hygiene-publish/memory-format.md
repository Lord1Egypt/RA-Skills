# Memory Format — RAG-Friendly Standard

## File Naming

| Format | When to use |
|--------|-------------|
| `YYYY-MM-DD.md` | Daily log — one per date, append for multiple sessions |
| `YYYY-MM-DD-topic.md` | Topic-specific deep dive (e.g. `2026-03-11-sales-accountability.md`) |
| `weekly-review-YYYY-MM-DD.md` | Weekly review, written Sunday evening |

**Never use:** `YYYY-MM-DD-HHMM.md` (timestamp format). If multiple sessions happen in one day, append to the existing date file.

## Entry Tagging

Every memory entry gets a type tag on the same line. This enables semantic search to distinguish between decisions, facts, and events.

### Tags

```markdown
[DECISION] What was decided and why. Include who decided.
[FACT] A durable fact — names, numbers, preferences, configurations.
[PROJECT] Project name — status update, milestone, blocker.
[RULE] A preference or constraint established by Steve. Non-negotiable once set.
[EVENT] Something that happened — meetings, milestones, incidents.
[BLOCKER] Something blocking progress. Include what would unblock it.
```

### Examples

```markdown
## 2026-03-14

[EVENT] OpenClaw upgraded from 2026.3.8 to 2026.3.13
[DECISION] Codex spawning now uses ACP protocol (sessions_spawn, not PTY exec). All agents.
[FACT] gog-personal wrapper at ~/.openclaw/scripts/gog-personal. Forces personal account.
[RULE] No em dashes in any external-facing content (emails, outreach)
[PROJECT] MyApp — API token rotated after git history exposure. Redeployed to production.
[PROJECT] Resume — V2 built, ATS optimized. Still iterating on summary language.
[BLOCKER] MyApp SMS — toll-free number pending carrier verification (submitted 5 days ago)
```

### Rules

1. One tag per line. Keep entries to 1-2 sentences max.
2. Use the project name exactly as it appears in `projects/` folder.
3. [RULE] entries should also be added to MEMORY.md or docs/tech-notes.md (rules need to survive beyond daily logs).
4. [DECISION] entries should include enough context that the reasoning is recoverable 30 days later.
5. Don't tag purely operational noise ("read 3 files, ran a script"). Only tag things worth retrieving.

## Distillation

Every 7-14 days, review daily logs and:
- Promote any [RULE] or [FACT] that's still active to MEMORY.md
- Promote any [DECISION] with lasting implications to MEMORY.md
- Archive resolved [BLOCKER] entries (they become [EVENT] when resolved)
- Technical config → docs/tech-notes.md, not MEMORY.md

## Why This Matters for RAG

OpenClaw's `memory_search` runs semantic search against MEMORY.md and all files in `memory/`. Tagged entries are dramatically easier to retrieve because:
- "What was decided about Codex?" matches `[DECISION] Codex spawning...`
- "What's blocking MyApp?" matches `[BLOCKER] MyApp SMS...`
- "What rules does Steve have about emails?" matches `[RULE] No em dashes...`

Unstructured prose buries signal in noise. Tags surface it.

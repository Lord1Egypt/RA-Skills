# Learnings

Corrections, knowledge gaps, improved workflows, and durable prevention rules captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Purpose

Use this file to record things future sessions should avoid rediscovering.
Prefer concise prevention rules over diary-style notes.

## Entry Skeleton

````markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: 2026-04-01T10:00:00Z
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line prevention rule.

### Details
Why the lesson matters and what changed.

### Suggested Action
What to do differently next time.

### Metadata
- Source: conversation | debugging | user_feedback | simplify-and-harden
- Related Files: path/to/file
- Tags: tag-a, tag-b
- See Also: LRN-20260401-001
- Pattern-Key: optional.stable.key
- Recurrence-Count: 1
- First-Seen: 2026-04-01
- Last-Seen: 2026-04-01

---
````

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Logged but not yet integrated or promoted |
| `in_progress` | Currently being addressed |
| `resolved` | Fix or understanding is now confirmed |
| `wont_fix` | Intentionally not pursued |
| `promoted` | Distilled into durable repo or workspace guidance |
| `promoted_to_skill` | Turned into a reusable skill |

## Promotion Hints

- Promote to `CLAUDE.md` for project facts and conventions
- Promote to `AGENTS.md` for workflows and automation
- Promote to `TOOLS.md` for tool-specific gotchas
- Promote to `SOUL.md` for behavioral rules

## Skill Extraction Fields

When a learning becomes a reusable skill, add:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

---

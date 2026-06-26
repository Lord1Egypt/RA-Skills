# Memory Template - Storytelling

Create `~/storytelling/memory.md` with this structure:

```markdown
# Storytelling Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- Audience profile, narrative goals, delivery channels, and constraints -->

## Story Bank
<!-- Reusable anecdotes, examples, proof points, and outcomes -->

## Message Pillars
<!-- Core claims, supporting arguments, and non-negotiable themes -->

## Voice Preferences
<!-- Tone, cadence, sentence density, and language constraints -->

## Experiments
<!-- A/B narrative tests, edits applied, and observed impact -->

## Notes
<!-- Internal reminders that improve continuity and output quality -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Ask only when missing context changes narrative choices |
| `complete` | Context is stable | Prioritize execution and iterative improvement |
| `paused` | User deferred setup | Use existing context without extra setup prompts |
| `never_ask` | User requested no setup prompts | Never ask setup questions again |

## Key Principles

- Keep memory in natural language, not rigid configuration lists.
- Store only details that improve story quality, consistency, or decision impact.
- Update `last` after each meaningful storytelling session.
- Preserve failed narrative attempts to avoid repeated mistakes.
- Never persist credentials or private secrets unless the user explicitly asks.

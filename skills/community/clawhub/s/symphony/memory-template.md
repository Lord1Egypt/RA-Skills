# Memory Template - OpenAI Symphony

Create `~/symphony/memory.md` with this structure:

```markdown
# Symphony Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- Team goals for unattended issue orchestration -->
<!-- Trust boundaries, environment constraints, and escalation posture -->

## Environment
<!-- Tracker kind, project slug, workspace root, and hook strategy -->
<!-- Sandbox and approval defaults approved by the user -->

## Workflow
<!-- Active and terminal state mapping -->
<!-- Prompt policy notes and validation requirements -->

## Operations
<!-- Known incidents, retry patterns, and proven recovery actions -->

## Notes
<!-- Durable decisions that improve future Symphony sessions -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Setup still evolving | Keep refining environment and workflow safely |
| `complete` | Stable orchestration profile | Execute with defaults and update on change |
| `paused` | User postponed deeper setup | Run only bounded tasks with conservative defaults |
| `never_ask` | User does not want setup prompts | Stop setup-style questions and follow existing profile |

## Principles

- Save operational facts, not long transcripts.
- Track only data that speeds up safe future execution.
- Keep secrets out of memory files.
- Update `last` whenever workflow policy or runtime posture changes.

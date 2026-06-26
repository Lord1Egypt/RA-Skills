---
name: self-improving-coding
description: "Injects coding self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🔧","events":["agent:bootstrap"]}}
---

# Self-Improving Coding Hook

Injects a reminder to evaluate coding learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a coding-specific reminder block to check `.learnings/` for relevant entries
- Prompts the agent to log lint errors, type mismatches, runtime exceptions, anti-patterns, idiom gaps, debugging insights, and tooling issues

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Lint or type error encountered | `BUG_PATTERNS.md` | lint/type trigger |
| Runtime exception thrown | `BUG_PATTERNS.md` | runtime trigger |
| Anti-pattern discovered | `LEARNINGS.md` | `anti_pattern` |
| Better idiom found | `LEARNINGS.md` | `idiom_gap` |
| Debugging insight gained | `LEARNINGS.md` | `debugging_insight` |
| Tooling issue hit | `LEARNINGS.md` | `tooling_issue` |
| Refactoring opportunity | `LEARNINGS.md` | `refactor_opportunity` |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-coding
```

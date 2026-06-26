# Memory Operations

## On Session Start (Cold-Boot Recovery)

**This is the critical path. Do this EVERY time.**

1. Read SESSION-STATE.md (workspace hot RAM) — know what you were doing
2. Read ~/self-improving/memory.md (HOT tier) — know your learned patterns
3. Check index.md for context hints — what namespaces exist
4. If project detected → preload relevant namespace file
5. If SESSION-STATE.md is stale → check today's memory/YYYY-MM-DD.md

### Why each step matters
- SESSION-STATE.md: Without it, you don't know your current task or pending actions
- memory.md: Without it, you repeat corrected mistakes
- index.md: Tells you what project/domain files exist without loading them all

## On Correction Received (WAL Protocol)

**Write BEFORE responding to the user.**

1. Parse correction type (preference, pattern, override)
2. Check if duplicate (exists in any tier)
3. If new: add to corrections.md with timestamp, increment counter
4. If duplicate: bump counter, update timestamp; if ≥3 ask to confirm as rule
5. Determine namespace (global, domain, project)
6. Write to appropriate file
7. Update index.md line counts
8. THEN respond to the user

## On Pattern Applied

1. Find pattern source (file:line)
2. Apply pattern
3. Optionally cite source: "Using X (from memory.md)"
4. Log usage for decay tracking

## On Significant Work Completed

1. Self-reflect (outcome vs intent)
2. Log reflection if lesson found → corrections.md
3. Update SESSION-STATE.md with new state
4. Update memory/YYYY-MM-DD.md daily log

## On Pre-Compaction Memory Flush

When OpenClaw triggers a memory flush before compaction:
1. Write any unsaved state to SESSION-STATE.md
2. Write any pending lessons to memory/YYYY-MM-DD.md
3. Ensure MEMORY.md is current with critical long-term facts
4. Reply NO_REPLY to let compaction proceed

## File Formats

### ~/self-improving/memory.md (HOT)
```markdown
# Self-Improving Memory (HOT)

## Confirmed Preferences
- format: bullet points over prose (confirmed 2026-01)
- tone: direct, no hedging (confirmed 2026-01)

## Active Patterns
- "looks good" = approval to proceed (used 15x)

## Recent (last 7 days)
- prefer SQLite for MVPs (corrected 02-14)
```

### ~/self-improving/corrections.md
```markdown
# Corrections Log

## 2026-02-15 2:32 PM — Verbose explanations
CONTEXT: Telegram response about API setup
CORRECTION: User wanted bullet summary, not paragraphs
LESSON: Default to bullets for technical topics. Prose only when asked.

## 2026-02-14 9:15 AM — Wrong database choice
CONTEXT: MVP database discussion
CORRECTION: Use SQLite not Postgres for MVPs
LESSON: Start simple. Postgres only when scale demands it. Confirmed.
```

### ~/self-improving/projects/{name}.md
```markdown
# Project: my-app

Inherits: global, domains/code

## Patterns
- Use Tailwind (project standard)
- Deploy via GitLab CI

## Overrides
- semicolons: yes (overrides global no-semi)

## History
- Created: 2026-01-15
- Last active: 2026-02-15
```

## Edge Cases

### Contradiction Detected
Project overrides domain overrides global. Log conflict. Ask which should apply broadly.

### User Changes Mind
Archive old pattern with timestamp. Add new pattern as tentative. Keep archived for reference.

### Context Ambiguous
Check current context (project? domain?). If unclear, ask. Default to most specific active context.

### Memory Full (HOT tier >100 lines)
1. Identify oldest unconfirmed entries
2. Demote to appropriate WARM namespace (domains/ or projects/)
3. If no matching namespace, create one
4. Update index.md
5. Never delete — only move

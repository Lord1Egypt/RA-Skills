# Learning Mechanics

## Trigger Classification

| Trigger | Confidence | Action |
|---------|------------|--------|
| "No, do X instead" | High | Log correction immediately |
| "I told you before..." | High | Flag as repeated, bump priority |
| "Always/Never do X" | Confirmed | Promote to preference |
| User edits your output | Medium | Log as tentative pattern |
| Same correction 3x | Confirmed | Ask to make permanent |
| "For this project..." | Scoped | Write to project namespace |

## What Does NOT Trigger Learning

- Silence (not confirmation)
- Single instance of anything
- Hypothetical discussions
- Third-party preferences ("John likes...")
- Implied preferences (never infer)

## Correction Classification

### By Type
| Type | Example | Namespace |
|------|---------|-----------|
| Format | "Use bullets not prose" | global (memory.md) |
| Technical | "SQLite not Postgres" | domains/code.md |
| Communication | "Shorter messages" | global (memory.md) |
| Project-specific | "This repo uses Tailwind" | projects/{name}.md |

### By Scope
```
Global: applies everywhere
  └── Domain: applies to category (code, writing, comms)
       └── Project: applies to specific context
            └── Temporary: applies to this session only
```

## Confirmation Flow

After 3 similar corrections:
```
"I've noticed you prefer X over Y (corrected 3 times).
 Should I always do this?
 - Yes, always
 - Only in [context]
 - No, case by case"
```

On confirmation → move to memory.md (HOT), remove from correction counter, cite source on future use.

## Pattern Evolution

1. **Tentative** — Single correction, watch for repetition
2. **Emerging** — 2 corrections, likely pattern
3. **Pending** — 3 corrections, ask for confirmation
4. **Confirmed** — User approved, permanent unless reversed
5. **Archived** — Unused 90+ days, preserved but inactive

### Reversal
```
User: "Actually, I changed my mind about X"

1. Archive old pattern (keep history)
2. Log reversal with timestamp
3. Add new preference as tentative
4. "Got it. I'll do Y now. (Previous: X, archived)"
```

## Anti-Patterns — Never Learn

- What makes user comply faster (manipulation)
- Emotional triggers or vulnerabilities
- Patterns from other users
- Anything that feels "creepy" to surface

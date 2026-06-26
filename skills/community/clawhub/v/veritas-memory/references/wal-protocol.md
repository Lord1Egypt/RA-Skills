# Write-Ahead Log Protocol

> **Write BEFORE responding, not after.**
> If the agent responds first and the session crashes/compacts before saving, context is lost forever.
> WAL ensures durability.

## When to Write

| Trigger | Write What |
|---------|-----------|
| User gives instruction/decision | Append event to STATE.md timeline |
| User corrects you | Append correction event + fix STATE.md if needed |
| User states preference | Append to STATE.md, update MEMORY.md if long-term |
| You complete a task (fix/deploy/audit) | Append event + update current state section |
| Cross-agent message received | Append event with source reference |

## The WAL Flow

```
1. User says something important
2. Agent: write to STATE.md FIRST
3. Agent: THEN formulate response
4. Agent: send response
```

**Why:** If step 2 is skipped and step 3-4 causes a crash/compaction, the context is lost.

## Anti-patterns

- ❌ Formulating response first, updating memory after
- ❌ "I'll update later" — session may compact before "later"
- ❌ Updating only at session end — mid-session crashes happen

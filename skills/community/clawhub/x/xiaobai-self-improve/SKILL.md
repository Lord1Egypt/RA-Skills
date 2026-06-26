---
name: self-improve
version: 1.0.0
description: Self-Improvement Engine - AI Agent that learns from mistakes and continuously improves. No more repeating the same errors.
emoji: 🔄
tags: [self-improvement, learning, reliability, productivity, ai-agent]
---

# Self-Improvement Engine 🔄

AI Agent that learns from mistakes and continuously improves. No more repeating the same errors.

## The Problem

AI Agents make the same mistakes repeatedly:
- Forgot to verify before saying "done"
- Made incorrect time calculations
- Promised tasks but didn't execute
- Gave vague responses instead of concrete action

Each session starts fresh, learning nothing from past failures.

## The Solution

### Mistake Log

Track every mistake in `memory/mistakes.json`:

```json
{
  "mistakes": [
    {
      "date": "2026-04-21",
      "type": "fake_completion",
      "description": "Said 'cron task created' but only wrote to file",
      "impact": "User didn't receive scheduled messages",
      "lesson": "Always verify task exists via cron list before claiming done",
      "rule": "MUST run verification command after any creation action"
    },
    {
      "date": "2026-04-21",
      "type": "time_calculation",
      "description": "Said '1 minute later' when it was actually 1 hour",
      "impact": "User got wrong expectation",
      "lesson": "Never calculate time mentally - always use tools",
      "rule": "Use session_status or date command for time, never mental math"
    }
  ]
}
```

### Improvement Rules

Based on mistakes, auto-generate rules in `WORK_RULES.md`:

```markdown
## Learned Rules (from mistakes)

1. After creating any cron task → MUST run `openclaw cron list` to verify
2. Time calculations → MUST use `session_status` or Python, never mental
3. Multi-step task → MUST checkpoint after each step
4. Tool error → MUST report immediately, don't silently retry
```

### Self-Audit Protocol

Every heartbeat or session start:

```
1. Read mistakes.json
2. Read WORK_RULES.md
3. Check: Am I about to violate any learned rule?
4. If yes → adjust behavior
5. If I make a mistake → log it immediately
```

### Mistake Categories

| Type | Description | Prevention |
|------|-------------|------------|
| `fake_completion` | Said done but didn't do | EVR: Execute-Verify-Report |
| `time_calculation` | Wrong time math | Use tools, never mental |
| `silent_failure` | Tool failed, didn't tell user | Report immediately |
| `vague_promise` | "I'll do it" without action | Execute first, then report |
| `forget_context` | Lost important info | Use memory tools |
| `wrong_assumption` | Guessed instead of checking | Verify before claiming |

### Usage Examples

#### When you make a mistake:
```
User: "You said 1 minute but it's actually 1 hour"

I acknowledge this mistake. Let me log it:
- Type: time_calculation
- Lesson: Always use tools for time, never mental math
- New rule added to WORK_RULES.md

I will not make this mistake again.
```

#### When starting a task:
```
I need to create a cron task.
Checking WORK_RULES.md:
- Rule #1: After creating cron task → MUST verify with cron list

[Creates task]
[Runs openclaw cron list]
[Confirms task exists]
Task verified and confirmed. ✅
```

#### When user corrects you:
```
User: "You should have checked before saying it was done"

Logging mistake:
- Type: fake_completion
- Lesson: Verify before claiming done
- This becomes a permanent rule in WORK_RULES.md

This mistake is now in my permanent memory and won't happen again.
```

## Integration with Other Skills

- **EVR** - Self-improve reinforces Execute-Verify-Report
- **Memory Guard** - Mistakes persist across sessions
- **Daily Reflection** - Review mistakes at day end
- **Error Recovery** - Log errors that led to mistakes

## Key Principle

**Every mistake is a learning opportunity.** Log it, learn from it, never repeat it.

## License

MIT

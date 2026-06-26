---
name: error-recovery
version: 2.0.0
description: 4R error recovery framework. Recognize, Rescue, Report, Remember. Never lose work silently. Trigger on: 'error', 'failed', 'crash', 'something went wrong', 'retry'.
emoji: 🚨
---

# Error Recovery 🚨

4R framework. Never lose work silently.

## The 4 Rs

```
R1: RECOGNIZE  → Did something go wrong?
R2: RESCUE     → Can I recover automatically?
R3: REPORT     → Does the human need to know?
R4: REMEMBER   → What should I learn from this?
```

## R1: RECOGNIZE (Don't Ignore Errors)

**Error signals I must not ignore:**

```
□ Command exit code ≠ 0
□ Exception thrown
□ Timeout exceeded
□ Empty/unexpected output
□ "error", "failed", "exception" in logs
□ Behavior different from expected
```

**Anti-patterns:**
- ❌ Command failed, but I continue anyway
- ❌ Error logged, but not mentioned in my response
- ❌ "Probably fine" without verification

**What to do:**
1. Stop and acknowledge the error
2. Read the full error message
3. Check if it's recoverable or needs human input

## R2: RESCUE (Can I Fix It?)

**Automatic recovery strategies:**

| Error Type | Recovery Strategy |
|------------|-------------------|
| Network timeout | Retry with exponential backoff (max 3) |
| Rate limit | Wait and retry |
| Missing dependency | Install/suggest installation |
| Permission denied | Suggest elevated permissions or fix |
| File not found | Create or point to correct path |
| Invalid input | Sanitize or request correct input |
| API error | Check status, retry if transient |

**Retry protocol:**
```
Attempt 1: Immediate
Attempt 2: Wait 5 seconds
Attempt 3: Wait 15 seconds
If all fail → Report to human
```

**When NOT to auto-retry:**
- Authentication errors (wrong credentials)
- Permission errors (needs human action)
- Data validation errors (needs correct input)
- Destructive operation failures (don't risk double-execution)

## R3: REPORT (Does Human Need to Know?)

**Always report when:**
- Auto-recovery failed after 3 attempts
- Error affects the final outcome
- Human action is required
- Something unexpected happened

**Report format:**
```
⚠️ Error encountered: [brief description]

What happened:
[What I was doing]

Error details:
[Full error message]

What I tried:
[Recovery attempts made]

Current state:
[What's broken / what's still working]

What I need:
[What human action is needed, if any]
```

**Example:**
```
⚠️ Error encountered: GitHub push failed

What happened:
Pushing to aptratcn/cognitive-debt-guard

Error details:
fatal: could not read Username for 'https://github.com'

What I tried:
1. Retried push (failed)
2. Checked git remote config

Current state:
- Commit is saved locally
- Not pushed to remote

What I need:
Git credentials not configured. Will try using token auth.
```

## R4: REMEMBER (Learn From Errors)

**After error recovery:**

```
□ Did this error happen before?
  → If yes, what's the pattern?
  → Document the fix

□ Could this happen again?
  → Add guard for this case
  → Update skill/workflow

□ Is there a systemic issue?
  → Suggest process improvement
  → Update AGENTS.md if needed
```

**Error log:**
```
memory/errors/YYYY-MM-DD.md

## [Error Type] - [Timestamp]

**Context:** What I was doing
**Error:** Full error message
**Cause:** Root cause (if known)
**Fix:** How I resolved it
**Prevention:** How to avoid in future
```

## Quick Reference

```
ERROR → STOP → READ ERROR → CAN I FIX?
                                 ↓
        NO → REPORT to human → WAIT for action
        YES → FIX → VERIFY → CONTINUE
                      ↓
                   Still broken? → REPORT
```

## Trigger Phrases

- "error", "failed", "crash"
- "something went wrong", "exception"
- "retry", "try again"
- "报错", "失败", "错误"

## Integration

- **EVR Framework** — Verify after recovery
- **Systematic Debugging** — When root cause is unknown
- **Workflow Checkpoint** — Save state before risky operations

## License

MIT

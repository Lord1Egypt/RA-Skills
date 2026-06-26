---
name: systematic-debugging
version: 2.0.0
description: 4-phase root cause debugging. Never guess, find the cause. Based on real production debugging methodology. Trigger on: 'bug', 'error', 'not working', 'broken', 'debug', 'fix this'.
emoji: 🔍
---

# Systematic Debugging 🔍

4 phases. No guessing. Find root cause.

## The 4 Phases

```
Phase 1: OBSERVE    → What exactly is wrong? (Gather evidence)
Phase 2: ISOLATE    → Where does it go wrong? (Narrow scope)
Phase 3: HYPOTHESIZE → Why does it go wrong? (Form theory)
Phase 4: VERIFY     → Is it actually fixed? (Prove it)
```

## Phase 1: OBSERVE (Don't Skip This)

**Before touching any code, answer these:**

```
□ What is the expected behavior?
□ What is the actual behavior?
□ When did it start? (What changed?)
□ Is it reproducible? (100%? Intermittent?)
□ What's the exact error message / log output?
□ What environment? (OS, version, dependencies)
```

**Common mistake:** Jumping to "I think it's because..." without observing first.

**What to do:**
- Read the actual error (copy-paste, don't paraphrase)
- Check logs (recent ones first)
- Reproduce the issue (if possible)
- Document what you see

## Phase 2: ISOLATE (Narrow the Scope)

**Binary search for the bug:**

```
1. Is the problem in my code or external?
   → Comment out my code. Still broken? External.

2. Is it in the input, processing, or output?
   → Print/log at each stage.

3. Is it in one specific file/function?
   → Remove files/functions one by one.
   → Bug disappears? That's where it is.

4. Is it a specific condition?
   → Test with different inputs.
   → Pattern emerges? Root cause narrows.
```

**Techniques:**
- `git bisect` — Find the commit that introduced the bug
- Print statements at boundaries
- Comment out code sections
- Test with minimal reproduction

## Phase 3: HYPOTHESIZE (Form a Theory)

**Write your hypothesis BEFORE fixing:**

```
I believe [X] is broken because [Y].

Evidence supporting:
- [Observation 1]
- [Observation 2]

Evidence against:
- [Observation 3]

If I change [Z], the fix should:
- Make [test case] pass
- Not break [other thing]
```

**Common mistake:** Fixing without understanding. You might "fix" the symptom, not the cause.

**Anti-patterns:**
- ❌ "Let me try changing this..." (random fixing)
- ❌ "This usually works..." (cargo cult debugging)
- ❌ "It's probably a race condition" (vague guess)

## Phase 4: VERIFY (Prove It)

**Before claiming "fixed":**

```
□ Original test case now passes
□ Edge cases tested
□ No new regressions introduced
□ Error no longer appears in logs
□ Fix makes sense given the hypothesis
```

**Verification checklist:**
```bash
# Run the failing test
npm test -- --grep "failing test"
# Check logs for errors
tail -f /var/log/app.log
# Test edge cases
[try empty input, huge input, unicode, etc.]
# Run full test suite
npm test
```

## Real Example

**Bug:** "User login sometimes fails"

```
Phase 1 OBSERVE:
- Error: "Invalid token" (not "wrong password")
- Intermittent (10% of logins)
- Started after deploying auth-service v2.3
- Only on mobile, not desktop

Phase 2 ISOLATE:
- Network logs: token arrives intact
- Auth service: token validation fails intermittently
- Added logging: token format varies slightly

Phase 3 HYPOTHESIZE:
- Mobile client generates tokens with different encoding
- v2.3 tightened token validation
- Theory: mobile token format doesn't match new validation

Phase 4 VERIFY:
- Fixed token format in mobile client
- Tested 100 logins on mobile: 100% success
- Tested desktop: still works
- Checked logs: no "Invalid token" errors
```

## Trigger Phrases

- "bug", "error", "not working"
- "broken", "debug", "fix this"
- "doesn't work", "fails", "crash"
- "调试", "修复", "报错"

## Integration

- **EVR Framework** — Each phase is Execute/Verify
- **Cognitive Debt Guard** — Document bugs in code review
- **Error Recovery** — What to do after finding the cause

## License

MIT

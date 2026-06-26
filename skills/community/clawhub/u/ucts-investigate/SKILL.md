---
name: ucts-investigate
description: >
  Root cause debugging methodology. Systematic hypothesis-driven investigation
  with strict rules: no fixes without investigation, stop after 3 failed attempts.
  Works directly in OpenClaw — no Claude Code session needed.
tags: [ucts, debugging, investigation, root-cause]
---

# UCTS Investigate

Systematic root-cause debugging. This is a methodology skill — guide the user through the process.

## Iron Law

**No fixes without investigation.** Never guess-and-check. Never "try this and see." Understand the cause FIRST, then fix.

## Process

### 1. Reproduce
Get the exact:
- Steps to trigger the bug
- Input that causes the failure
- Environment (OS, Node version, browser, etc.)
- Error message (exact text, not paraphrased)
- Frequency: always, sometimes, only on Tuesdays?

If you can't reproduce it, you can't fix it. Stop here until you can.

### 2. Hypothesize
Form **3 hypotheses** about the root cause, ranked by probability:
1. Most likely: [specific mechanism]
2. Second most likely: [specific mechanism]
3. Dark horse: [unlikely but would explain everything]

Each hypothesis must be **falsifiable** — you must be able to design a test that proves it wrong.

### 3. Trace
For the top hypothesis, trace the data flow:
- What enters the system?
- What transformations happen?
- Where does the expected path diverge from the actual path?
- What state is wrong and when did it become wrong?

### 4. Test
Design a **minimal test** that confirms or refutes the top hypothesis:
- If confirmed → you found the root cause. Proceed to fix.
- If refuted → move to hypothesis #2. Repeat trace + test.

### 5. The 3-Strike Rule
After **3 failed fix attempts**, STOP. Reassess from scratch:
- Are your hypotheses wrong?
- Is the bug actually in a different layer?
- Is there a simpler explanation you missed?
- "The bug is in the code you trust most."

## When to Spawn Claude Code

If the investigation requires reading code, running tests, or making changes:
```
Load UCTS. Run /investigate <bug description>
```

If the user just needs to think through the problem, stay in chat.

---
name: taku-debug
description: >
  When the user reports a bug, crash, error, or anything that is broken or behaving
  unexpectedly, invoke this skill FIRST — before writing any code or proposing any fix.
  This skill is the mandatory entry point for ALL bug-fix tasks. The user expects you
  to investigate root cause systematically before fixing. Without this skill, you will
  likely fix the symptom instead of the cause, which is the #1 debugging failure mode.
  Use this skill whenever the user says anything like: "fix this bug", "crashes",
  "returns null", "500 error", "not working", "wrong result", "throws exception",
  "timeout", "silent failure", "was working yesterday", "broke after deploy",
  "sometimes fails", "only in production", "works locally but not in CI/staging",
  "CLI crashes", "config missing", "test fails", or describes any error/stack trace.
  Also: "调试", "找bug", "报错", "排查问题", "不工作了", "挂了", "崩了", "数据不对".
  Do NOT use for: lint fixes, dependency updates, adding features, refactoring,
  or any task that is NOT about fixing broken behavior.
---

# taku-debug — 4-Phase Root Cause Investigation

Random fixes create new bugs. Systematic investigation finds root causes. This skill merges the best of Superpowers' systematic debugging with gstack's investigate workflow into a unified 4-phase process.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

## When to Use This Skill

Use `taku-debug` when:

- the VERIFY phase fails and the failure path is not yet understood
- the user reports broken behavior, a regression, or an intermittent issue
- you need to explain why something is failing before proposing the fix

Do not use `taku-debug` just to run routine verification. Run the repo's normal checks first. Enter this skill when those checks fail or when production behavior is already broken.

## The Iron Law

[IRON LAW] **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Every fix that doesn't address root cause makes the next bug harder to find. If you haven't completed Phase 1 (INVESTIGATE), you cannot propose fixes. Period.

Violating the letter of this process is violating the spirit of debugging.

**Mandatory sequence enforcement:** Before writing ANY code change, you MUST:
1. Complete Phase 1 (INVESTIGATE) — gather evidence, reproduce, trace data flow
2. Complete Phase 2 (PATTERN) — match against known patterns
3. Complete Phase 3 (HYPOTHESIS) — rank and test hypotheses

Only after all three phases may you proceed to Phase 4 (IMPLEMENT). If you find yourself writing a fix before producing a DEBUG REPORT, stop and go back to Phase 1.

## The 4 Phases

### Phase 1: INVESTIGATE

Gather context before forming any hypothesis. This is evidence collection, not problem-solving.

**Why evidence-first:** Jumping to solutions before understanding the problem is the single most common debugging failure. You fix what you think is wrong, not what's actually wrong. Evidence-first prevents this bias.

1. **Read the error.** Stack traces, error messages, log output. Read them completely. Line numbers, file paths, error codes — all of it. The error message usually contains the answer.

2. **Reproduce consistently.** What are the exact steps? Does it happen every time? If not reproducible, gather more data. Don't guess at intermittent bugs.

3. **Check recent changes.**
   ```bash
   git log --oneline -20 -- <affected-files>
   git diff HEAD~1 -- <affected-files>
   ```
   Was this working before? What changed? A regression means the root cause is in the diff.

4. **Trace data flow backward.** Where does the bad value originate? What called this function with the bad value? Keep tracing up until you find the source. Fix at source, not at symptom.

5. **Gather evidence in multi-component systems.** When the system has layers (API → service → database), add diagnostic logging at each boundary. Run once. See WHERE it breaks. Then investigate THAT layer.

**Budget check:** If INVESTIGATE exceeds 10 minutes or produces >20 evidence items without convergence toward a root cause hypothesis, pause and present findings so far. This is not failure — it's scope-aware investigation. Complex distributed systems sometimes need a narrower scope before continuing.

Output: **Root cause hypothesis** — a specific, testable claim about what is wrong and why.

### Phase 2: PATTERN

Match the bug against known patterns before proposing solutions.

**Why pattern-match first:** Most bugs are instances of well-known failure modes. Recognizing the pattern tells you where to look and what to check, cutting investigation time from hours to minutes. Novel bugs are rare; your bug has almost certainly happened before.

| Pattern | Signature | Where to look |
|---------|-----------|---------------|
| Race condition | Intermittent, timing-dependent | Shared state, concurrent access |
| Null propagation | TypeError, NoMethodError | Missing guards on optional values |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, hooks |
| Integration failure | Timeout, unexpected response | API boundaries, service calls |
| Config drift | Works locally, fails elsewhere | Env vars, feature flags, secrets |
| Stale cache | Shows old data | Redis, CDN, browser cache |

Also check:
- Working examples in the same codebase — what does the same thing correctly?
- TODOS.md for related known issues
- Git log for prior fixes in the same area. Recurring bugs in the same files are an architectural smell, not a coincidence.
- `.taku/learnings/{project-slug}.jsonl` — similar bug patterns, prior root causes, known pitfalls from previous debug sessions

If the pattern isn't obvious, search the web for "{framework} {error type}" (sanitize first: strip hostnames, IPs, file paths, customer data).

Common failure patterns worth checking early:
- **Config drift:** docs, defaults, env names, or runtime lookup disagree.
- **Boundary mismatch:** caller and callee disagree about nullability, auth, or ownership.
- **State race:** async ordering, caching, or lifecycle cleanup changes what later code sees.
- **Platform path/permission drift:** Windows, symlinks, executable bits, or temp paths behave differently.

### Phase 3: HYPOTHESIS

Form hypotheses ranked by likelihood. Test them one at a time.

**Why rank and isolate:** Ranking forces honest probability assessment — you test the most likely cause first, not the most interesting one. Testing one at a time means each test produces clear signal: confirmed or denied. Multiple simultaneous changes produce ambiguous results.

1. **Rank hypotheses:**
   ```
   H1 (80%): Token expires between redirect and callback
   H2 (15%): CORS header missing on callback endpoint
   H3 (5%): Browser caches stale auth response
   ```

   Ranking forces you to think about probability, not just possibility. Test the most likely hypothesis first.

2. **Test minimally.** One variable at a time. The smallest change that confirms or denies the hypothesis. Add a log statement, an assertion, or a debug output. Run the reproduction.

3. **If confirmed:** Proceed to Phase 4 (IMPLEMENT).

4. **If denied:** Move to the next hypothesis. Before forming a new one, return to Phase 1 and gather more evidence. Don't guess.

5. **3-strike rule:** If 3 hypotheses fail, STOP. This is not a failed hypothesis — this is a wrong architecture or a fundamentally misunderstood system. Present options:
   - Continue investigating with a new theory
   - Escalate for human review
   - Add instrumentation and wait for the next occurrence

**Red flags — if you catch yourself thinking any of these, STOP:**
- "Quick fix for now, investigate later"
- "Just try changing X and see what happens"
- "Add multiple changes at once, run tests"
- Proposing solutions before tracing data flow
- "One more fix attempt" after 2+ failures

### Phase 4: IMPLEMENT

Fix the root cause, not the symptom.

**Why root-cause-only:** Symptom fixes suppress the error at the crash site, but the underlying problem persists and will surface elsewhere — usually in a harder-to-diagnose form. A null check at the crash site doesn't fix the auth middleware that produced the null.

1. **Write a failing test first.** The simplest reproduction of the bug as an automated test. If no test framework exists, write a one-off script. The test MUST fail before the fix.

2. **Implement the minimal fix.** One change. One root cause addressed. No "while I'm here" refactoring. No bundled improvements.

3. **Verify the fix.** Test passes? Full suite passes? Original bug scenario resolved?

4. **Blast radius check.** If the fix touches more than 5 files, pause and justify each one. If the justification is sound (e.g., a cross-service API change with matching test files), proceed. If changes span more than 3 subsystems, consider splitting into multiple focused fix PRs.

**Why the 5-file guideline:** A genuine root cause fix is usually localized — it changes one thing in one place. If you're touching 5+ files, you're likely fixing symptoms across multiple layers rather than the single source. But some fixes are genuinely cross-cutting (e.g., renaming a shared interface). The guideline catches shallow fixes without blocking legitimate broad fixes.

5. **Run the full test suite.** Paste the output. No regressions.

## Known Pitfalls

**Fixing the symptom instead of root cause.** The error was a `NullPointerException` on `user.getEmail()`. The fix added a null check: `user?.getEmail() ?? ""`. Two days later, a different code path crashed because `user` was null — the real bug was in the auth middleware that failed to populate the session.

*What went wrong:* The null pointer was a symptom. The root cause was upstream. The fix suppressed the error at the crash site instead of fixing where the null originated.

*Prevention:* Phase 1 Step 4 (trace data flow backward) exists specifically for this. Never fix at the crash site without tracing where the bad value comes from. Fix at the source.

**Testing multiple hypotheses simultaneously.** Three hypotheses were on the list. To save time, all three fixes were applied at once. The bug disappeared. Now none of the three fixes can be individually verified — which one actually fixed it? Is the fix correct, or did two wrong fixes cancel each other out?

*What went wrong:* Parallel hypothesis testing saves time in the moment but destroys diagnostic value. You learn nothing from a bulk fix.

*Prevention:* One hypothesis at a time. One change. One test. If the first fix works, you're done. If it doesn't, you still have a clean system for the next hypothesis. Phase 3 Step 2 says "one variable at a time" for a reason.

**Skipping Phase 1 because the cause "seems obvious."** A 500 error appeared right after a deploy. The obvious fix was to revert the deploy. After reverting, the error persisted — it was actually caused by a database migration that ran during deploy and wasn't included in the revert.

*What went wrong:* "Obvious" causes are usually the first thing that comes to mind, not the actual cause. Skipping investigation means missing the real problem.

*Prevention:* Complete Phase 1 (INVESTIGATE) every time, even when the cause seems obvious. The Iron Law exists because "obvious" causes are wrong often enough to justify the discipline.

**Not writing a regression test for the fix.** A race condition was found and fixed with a mutex. Six weeks later, a refactoring removed the mutex as "unnecessary overhead." The race condition returned in production.

*What went wrong:* The fix wasn't protected by a regression test. Without a test, future developers can't know why the code exists.

*Prevention:* Phase 4 Step 1 requires a failing test first. This test becomes the regression guard. A bug without a regression test is a bug waiting to happen again.

## Output: Debug Report

Keep the report short and diagnostic. Name the concrete file/function/condition
that caused the bug. Put long investigation notes in a brief appendix only when
they are needed to make the fix reviewable.

```
DEBUG REPORT
═════════════════════════════════════════
Symptom:         [what the user observed]
Root cause:      [file/function/condition that was actually wrong]
Hypotheses:      [confirmed H1, denied H2/H3 if relevant]
Fix:             [minimal change, file:line references]
Evidence:        [red test, green test, reproduction showing fix works]
Regression test: [file:line of new test]
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
═════════════════════════════════════════
```

## Status

- **DONE** — Root cause found, fix applied, regression test written, all tests pass.
- **DONE_WITH_CONCERNS** — Fixed but can't fully verify (intermittent bug, requires staging).
- **BLOCKED** — Root cause unclear after 3 hypotheses. Escalated.

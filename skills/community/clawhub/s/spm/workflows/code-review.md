# Code Review — Three-Stage Review

## Overview

Three-stage review after each implementation task: Spec Compliance → Engineering Quality → Final Verification.

## Stage 1: Spec Compliance

**Goal:** Ensure code matches spec exactly.

1. Compare code against the task's acceptance criteria from the WBS ledger
2. Check: Are all criteria met?
3. Check: Any YAGNI violations (features NOT in spec)?
4. If fails: Reject. Do NOT proceed to Stage 2.

## Stage 2: Engineering Quality

**Goal:** Ensure code is robust, readable, and safe.

1. **Testing:** Passing tests for new code? Real tests (not mocks)?
2. **Security:** Hardcoded secrets? SQL injection? Unsafe evals?
3. **Clean Code:** Console.log? TODO? Nested loops? Magic numbers?
4. **Design:** Follows project patterns? Single responsibility?

**Severity:**
- **Critical:** Must fix before proceeding
- **Important:** Fix before proceeding
- **Minor:** Note for later

## Stage 3: Final Verification

1. Run full test suite — ALL tests pass
2. Run linter — 0 errors
3. Verify against WBS ledger — all acceptance criteria met
4. Confirm no regressions

## Dispatch Reviewer (via Subagent)

```markdown
You are reviewing WBS Task [ID] for code quality.

Review: tests, security, clean code, design patterns.

Severity: Critical (must fix) / Important (fix before proceed) / Minor (note)

Output: Strengths + issues by severity + approval decision.
```

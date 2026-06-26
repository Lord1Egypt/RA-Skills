# Test-Driven Development (TDD)

## Overview

RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Commit

**Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

If you wrote code before the test: delete it. Start over. No exceptions.

## The Cycle

### RED — Write Failing Test

One test, one behavior, clear name.

### Verify RED — MANDATORY

```bash
npm test path/to/test.test.ts
```

Confirm: Test FAILS for the right reason (feature missing, not typo).

Test passes? You're testing existing behavior. Fix test.
Test errors? Fix error, re-run until it fails correctly.

### GREEN — Minimal Code

Write simplest code to pass. No extra features (YAGNI).

### Verify GREEN — MANDATORY

```bash
npm test path/to/test.test.ts
```

Confirm: Test PASSES. Other tests still pass.

### REFACTOR — Clean Up

Only when green. Keep tests green. No behavior changes.

### Commit

```bash
git add -A && git commit -m "feat(scope): description"
```

## Red Flags — Stop and Start Over

- Code before test
- Test passes immediately
- Can't explain why test failed
- "I'll test after"
- "Keep as reference"

## Acceptance

Before marking complete: every new function has a test, watched each test fail, tests use real code.

---
name: taku-tdd
description: Use whenever writing implementation code. Triggers during /taku-build, /taku-build (sequential mode), or when the user starts implementing a feature.
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail. Write the minimal code to pass it. Refactor.

**Core principle:** If you didn't watch the test fail, you don't know it tests the right thing.

## Why TDD Prevents Bugs

Tests written after code pass immediately — proving nothing. You might test the wrong thing, test implementation instead of behavior, or miss edge cases entirely.

Test-first forces you to see the test fail first, proving it actually catches the bug you're about to fix. This single discipline prevents an entire class of defects: code that "should work" but doesn't.

**Order matters:**
- Tests-after answer "What does this do?" — biased by your implementation
- Tests-first answer "What should this do?" — driven by requirements

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Not "save as reference," not "adapt while writing tests." Delete it completely and start fresh from tests.

## RED-GREEN-REFACTOR Cycle

### RED — Write Failing Test

One minimal test. Clear name. Real code (no mocks unless unavoidable).

```python
def test_retries_failed_operations_three_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("fail")
        return "success"

    result = retry_operation(operation)
    assert result == "success"
    assert attempts == 3
```

### Verify RED — Watch It Fail

Run the test. Confirm:
- It fails (not errors out)
- Failure message matches expectations (missing function, not typo)
- It fails because the feature doesn't exist yet

Test passes immediately? Wrong test — it's verifying existing behavior. Delete and rewrite.

**Why watch it fail:** A test that passes before the feature exists isn't testing the feature — it's testing something else. If you don't see it fail, you don't know what it's actually testing. The failure is proof that the test is wired to the right thing.

### GREEN — Minimal Code

Write the simplest code that makes the test pass. No extra features, no "while I'm here" improvements.

```python
def retry_operation(fn, max_retries=3):
    for i in range(max_retries):
        try:
            return fn()
        except Exception:
            if i == max_retries - 1:
                raise
```

### Verify GREEN — Watch It Pass

Run all tests. Confirm:
- New test passes
- All existing tests still pass
- Output is clean (no warnings, no skips)

### REFACTOR — Clean Up

Remove duplication, improve names, extract helpers. Keep tests green. No new behavior.

**Why separate refactor step:** GREEN produces working code, but working code written to pass a specific test often has duplication or awkward structure. The refactor step is where you clean up WITHOUT adding features. Combining cleanup with implementation risks introducing bugs alongside the cleanup. Keep the steps separate: first make it work, then make it clean.

## Anti-Rationalization Table

| Excuse | Why it's wrong |
|--------|---------------|
| "Too simple to test" | Simple code breaks too. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what did I build?" Tests-first = "what should I build?" |
| "Already manually tested" | Ad-hoc testing has no record, can't re-run, easy to forget cases. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll unconsciously adapt it. That's testing after. Delete means delete. |
| "Need to explore the design first" | Fine — throw away exploration, start fresh with TDD. |
| "Test is hard to write" | Hard to test = hard to use. The test is telling you something. |
| "TDD will slow me down" | TDD is faster than debugging in production. Always. |
| "This is different because..." | It's not. |

Any of these running through your head? Stop. Delete the code. Write the test first.

## When TDD Doesn't Apply

Ask your human partner for these cases:
- Throwaway prototypes
- Generated code
- Pure configuration files

Everything else gets a test first.

## Known Pitfalls

**Test passes immediately on the RED step — and nobody notices.** The test was supposed to verify a new `calculateDiscount()` function. But the test called `calculate_price()` (an existing function) by mistake. It passed immediately. The developer assumed the function already existed and moved on. The real `calculateDiscount()` was never implemented.

*What went wrong:* The RED step requires watching the test fail AND confirming the failure is for the expected reason. This test failed to fail, which should have been a red flag. Instead, it was treated as a green light.

*Prevention:* "Verify RED" step says: "Test passes immediately? Wrong test — it's verifying existing behavior. Delete and rewrite." This check is not optional. A test that passes before the feature exists is testing the wrong thing.

**Writing the test after code, then claiming TDD was followed.** Code was written first (200 lines). Then tests were written that call the exact implementation. The tests pass, but they test the implementation, not the behavior. When the implementation was refactored later, all tests broke — they were coupled to internal structure.

*What went wrong:* The Iron Law was violated in spirit. Writing tests after code isn't TDD — it's documentation of what you happened to build. The tests are biased toward the implementation.

*Prevention:* The Iron Law says: "Wrote code before the test? Delete it." This isn't hyperbole. Delete the code, write the test, watch it fail, then re-implement. The fresh implementation will be driven by requirements (the test) rather than assumptions (your first draft). The re-implementation is usually better.

**Testing implementation details instead of behavior.** The test asserts that `processOrder()` calls `validateCart()` then `applyDiscount()` then `createCharge()` in sequence. A refactor that combined `validateCart` and `applyDiscount` into a single `prepareOrder()` step broke all tests — even though the observable behavior (order processed, discount applied, charge created) was identical.

*What went wrong:* Tests asserted HOW the code works (internal call sequence) instead of WHAT the code does (observable outcomes). Implementation-coupled tests resist refactoring and produce false failures.

*Prevention:* "Good Tests" says tests should demonstrate the desired API surface. Test inputs and outputs, not internal mechanics. If you need to check intermediate state, test it through the public API, not by asserting on private methods or call order.

## Good Tests

- **Minimal:** One behavior per test. "and" in the name? Split it.
- **Clear:** Name describes the expected behavior, not the implementation.
- **Shows intent:** Demonstrates the desired API surface.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason
- [ ] Wrote minimal code to pass
- [ ] All tests pass with clean output
- [ ] Edge cases and error paths covered

## Debugging Integration

Found a bug? Write a failing test that reproduces it first. Follow the TDD cycle. The test proves the fix works and prevents regression.

Never fix a bug without a test.

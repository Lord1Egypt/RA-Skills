---
title: Use assert Only for Debug-Only Internal Invariants
impact: MEDIUM
impactDescription: `-O` strips asserts; use for debug-only invariants, not runtime contracts
tags: error, assert, invariants, debug
references: https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
---

## Use `assert` Only for Debug-Only Internal Invariants

`assert` is a debug-only statement — Python emits no code for it under `-O` or `PYTHONOPTIMIZE`. That makes `assert` the right tool for "this can never happen if my code is correct" and the wrong tool for any check that must run in production.

**Incorrect (runtime contract that vanishes under `-O`):**

```python
def transfer_funds(account_id: str, amount: int) -> None:
    assert amount > 0, "amount must be positive"  # stripped under -O
    assert account_id, "account_id required"      # stripped under -O
    ...
```

**Correct (real exceptions for contracts that must hold; `assert` only for programmer-error invariants):**

```python
def transfer_funds(account_id: str, amount: int) -> None:
    if not account_id:
        raise ValueError("account_id required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    ...

def process_step(step: Step) -> Result:
    # Step is a closed union; hitting the default branch is a programmer error.
    if isinstance(step, InitStep): return init()
    if isinstance(step, RunStep):  return run()
    if isinstance(step, DoneStep): return done()
    assert False, f"unhandled Step variant: {step!r}"  # debug-only
```

If the input crosses a trust boundary (user input, external API, deserialized data), always use a real exception — `AssertionError` is a poor signal at a system boundary even when it does fire. For exhaustiveness checks specifically, `typing.assert_never` is sharper than `assert False` (see `error-assert-never-exhaustiveness`). Rule of thumb: if you can't articulate why losing the check under `-O` is acceptable, it shouldn't be an `assert`.

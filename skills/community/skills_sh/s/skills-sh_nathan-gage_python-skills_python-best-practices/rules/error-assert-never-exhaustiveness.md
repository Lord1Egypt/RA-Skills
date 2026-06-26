---
title: Use assert_never for Exhaustiveness Checks
impact: MEDIUM
impactDescription: turns "missing variant" into a type-check error
tags: error, exhaustiveness, typing, assert-never
references: https://docs.python.org/3/library/typing.html#typing.assert_never, https://peps.python.org/pep-0702/, https://typing.python.org/en/latest/spec/narrowing.html#assert-never-and-exhaustiveness-checking
---

## Use `assert_never` for Exhaustiveness Checks

`typing.assert_never()` (Python 3.11+) tells static checkers "every variant has been handled here." If the union later grows a new member, the checker reports the missed branch as a type error before the code ships. At runtime it raises `AssertionError`, so a missed case still fails loudly even if the checker is bypassed. This is separate from `assert` — that statement is debug-only and can be stripped under `-O`.

**Incorrect (the checker can't see this branch is exhaustive):**

```python
Step = InitStep | RunStep | DoneStep

def process_step(step: Step) -> Result:
    if isinstance(step, InitStep): return init()
    if isinstance(step, RunStep):  return run()
    if isinstance(step, DoneStep): return done()
    raise RuntimeError(f"unexpected step: {step!r}")  # adding PausedStep slips past the checker
```

**Correct (`assert_never` — type error if the union grows, runtime error if reached):**

```python
from typing import assert_never

def process_step(step: Step) -> Result:
    match step:
        case InitStep(): return init()
        case RunStep():  return run()
        case DoneStep(): return done()
        case _:
            assert_never(step)
```

When `Step` becomes `InitStep | RunStep | DoneStep | PausedStep`, the checker reports that `step` is `PausedStep` at the `assert_never` call. Use it for closed sums: `Literal` unions, sealed dataclass hierarchies, discriminated unions, enum dispatch. On Python <3.11, import from `typing_extensions` — semantics are identical and both mypy and pyright recognize either source.

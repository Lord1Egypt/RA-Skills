---
title: Fix Type Errors, Don't Ignore Them
impact: HIGH
impactDescription: prevents masked errors from compounding
tags: types, mypy, pyright, ignore
references: https://mypy.readthedocs.io/en/stable/error_codes.html, https://microsoft.github.io/pyright/#/comments
---

## Fix Type Errors, Don't Ignore Them

`# type: ignore` and `# pyright: ignore` silence the checker — but the underlying problem stays. Ignore comments are common when a type looks hard; each one degrades the signal from every future run. Fix the error properly, and when a suppression is genuinely unavoidable, document why.

**Incorrect (ignore comment masks the real problem):**

```python
def compute(items: list[int] | None) -> int:
    return sum(items)  # type: ignore  # noqa
```

The checker flagged this because `sum(None)` crashes at runtime. The ignore hides a real bug.

**Correct (handle the None case):**

```python
def compute(items: list[int] | None) -> int:
    if items is None:
        return 0
    return sum(items)
```

The type system caught a real bug; fixing it is the right answer.

**When a suppression is genuinely required** (a complex generic the checker can't handle, a known checker limitation, an external library with bad stubs), include:

1. The specific error code (e.g., `# type: ignore[arg-type]`)
2. A comment explaining the safety reasoning

```python
# mypy cannot narrow through the factory's return type, but the
# registry guarantees adapters[cls] returns cls instances.
# See: https://github.com/python/mypy/issues/XXXX
adapter = adapters[cls]  # type: ignore[assignment]
```

A reviewer should be able to read the comment and confirm the suppression is justified without re-deriving the reasoning.

**Escape hatches to prefer before ignoring:**
- `cast(T, value)` with a comment (see `types-fix-types-not-cast` for when it's appropriate)
- `assert isinstance(x, T)` — runtime check plus narrowing
- `TypeGuard` functions for reusable narrowing
- Actually fixing the type signatures upstream

Reach for `# type: ignore` last, not first.

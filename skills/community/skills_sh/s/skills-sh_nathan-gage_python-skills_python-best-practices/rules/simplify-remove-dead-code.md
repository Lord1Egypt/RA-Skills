---
title: Remove Commented-Out and Dead Code
impact: LOW-MEDIUM
impactDescription: reduces confusion about intent
tags: simplify, dead-code, cleanup
references: https://docs.astral.sh/ruff/rules/commented-out-code/
---

## Remove Commented-Out and Dead Code

Commented-out code, superseded implementations, unused imports, and definitions nothing calls — delete them. Version control preserves history; dead code in the file confuses readers about which implementation is actually active.

**Incorrect (commented alternatives and stale code):**

```python
def fetch_user(user_id: str) -> User:
    # Old implementation:
    # response = requests.get(f"/users/{user_id}")
    # return User(**response.json())

    response = http_client.get(f"/users/{user_id}")
    return User.model_validate(response.json())

    # TODO: switch to async version once available
    # async def fetch_user(user_id): ...

def _unused_helper(x: int) -> int:  # nothing calls this
    return x * 2
```

Readers wonder: is the commented version the fallback? Is the TODO still accurate? Is `_unused_helper` called dynamically somewhere I'm missing?

**Correct (delete; let git remember):**

```python
def fetch_user(user_id: str) -> User:
    response = http_client.get(f"/users/{user_id}")
    return User.model_validate(response.json())
```

If you need the old implementation back, `git log` has it.

**Targets to delete:**

- Commented-out blocks of code
- Functions, methods, classes that nothing calls (verify with grep across the codebase first)
- Unused imports (`ruff` or `pyflakes` finds these)
- Unused variables
- Dead branches (if a condition can never be true)
- `print()` statements left over from debugging
- Commented-out log lines

**When to keep what looks like dead code:**

- Called dynamically (by name, via `getattr`, via a registry)
- Part of a public API contract that external callers may use
- Intentionally present for future use, with a TODO that links to a tracking issue

**For "intentional TODOs," link to the tracking issue:**

```python
# TODO(ISSUE-123): switch to async http_client when the migration lands
```

A TODO with a link is a commitment. A TODO without one is a wish.

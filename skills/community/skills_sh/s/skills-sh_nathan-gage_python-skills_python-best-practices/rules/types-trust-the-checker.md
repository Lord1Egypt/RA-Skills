---
title: Trust the Type Checker — Remove Redundant Runtime Checks
impact: LOW-MEDIUM
impactDescription: removes noise and signals confidence in the types
tags: types, runtime-checks, assertions
---

## Trust the Type Checker — Remove Redundant Runtime Checks

When types already constrain a value, runtime checks for the same constraint add noise and imply the types aren't trustworthy. Every redundant `assert` or `isinstance` is a vote of no confidence in the rest of the type system.

**Incorrect (runtime checks that duplicate the type):**

```python
def process_user(user: User) -> str:
    assert user is not None        # type says User, not User | None
    assert isinstance(user, User)   # type already says User
    assert user.name                # if name: str, this only catches empty strings
    return user.name.upper()
```

The first two lines add nothing. The third conflates "empty string" with "None" — if that matters, say so with a dedicated check and a real error message.

**Correct (trust the signature):**

```python
def process_user(user: User) -> str:
    return user.name.upper()
```

If callers pass `None` against the signature, that's a bug in the caller — and the type checker will flag it at the call site.

**Also incorrect (defensive check after validation):**

```python
def process_request(raw: str) -> Response:
    validated = validate(raw)  # returns ValidatedRequest, never None
    if validated is None:
        raise ValueError("invalid")  # unreachable
    return handle(validated)
```

`validate` returns `ValidatedRequest` by its signature — no `None`. The check is dead.

**When runtime checks are the right tool:**

- At **trust boundaries**: external API responses, deserialized user input, third-party callbacks where the type is aspirational
- As **narrowing aids**: `assert isinstance(x, T)` to narrow from a wider type the checker can't otherwise see
- For **invariants the checker can't express**: "this list is sorted," "this counter is positive"

Inside your own code, let the types do the work.

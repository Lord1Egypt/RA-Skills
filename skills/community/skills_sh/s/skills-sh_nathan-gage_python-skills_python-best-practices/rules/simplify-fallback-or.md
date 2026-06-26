---
title: Use x or default for Fallback Values
impact: LOW
impactDescription: more concise and idiomatic than if/else
tags: simplify, fallback, or
---

## Use `x or default` for Fallback Values

For the common "use `x` if it's truthy, otherwise `default`" pattern, `x or default` beats the verbose `if`/`else`. The catch: this triggers on every falsy value (`0`, `''`, `[]`, `None`) — so only use it when those aren't semantically meaningful.

**Incorrect (verbose if/else for a simple fallback):**

```python
def display_name(user: User) -> str:
    if user.nickname:
        return user.nickname
    else:
        return user.username
```

**Correct (or-fallback):**

```python
def display_name(user: User) -> str:
    return user.nickname or user.username
```

Shorter, idiomatic, and clear.

**When `or` is WRONG:** when falsy values are semantically valid.

```python
# wrong — if count is 0, we'd return DEFAULT_COUNT instead of 0
def get_count(config: Config) -> int:
    return config.count or DEFAULT_COUNT

# right — explicit about the None case
def get_count(config: Config) -> int:
    return config.count if config.count is not None else DEFAULT_COUNT
```

Zero, empty string, empty list, and empty dict are all falsy but often meaningful. `0 retries` ≠ `default retries`. `"" name` is probably a bug but it's not the same as "name was never set."

**Use `... if ... is not None else ...` when you specifically mean "None":**

```python
timeout = config.timeout if config.timeout is not None else DEFAULT_TIMEOUT
```

**Use `... if ... else ...` when the condition is more elaborate:**

```python
label = name.strip() if name and name.strip() else "anonymous"
```

**Rule of thumb:** `or` for truthy/falsy semantics; explicit `is not None` for optional-value semantics.

---
title: No Mutable Defaults in Function Parameters
impact: CRITICAL
impactDescription: Prevents shared mutable state bugs where defaults are reused across function calls
tags: mutable-defaults, function-parameters, shared-state, bugs, __init__
---

## No Mutable Defaults in Function Parameters

**Impact: CRITICAL (Prevents shared mutable state bugs where defaults are reused across function calls)**

Never use mutable defaults in function/method parameters. Mutable default arguments ([], {}, set(), etc.) are evaluated once at function definition time and shared across all calls, causing unexpected behavior where modifications in one call affect subsequent calls. This is the canonical "shared default list across calls" bug.

**When to Trigger:**
- Any default value that is a mutable literal: `[]`, `{}`
- Mutable constructor calls: `list()`, `dict()`, `set()`
- Especially in `__init__` for container-like classes
- Default arguments that will be modified inside the function

**Why This Is Critical:**
- Default arguments become function object attributes and are reused
- Mutations persist across function calls
- Creates hard-to-debug "time-bomb" bugs
- Violates principle of least surprise

**Implementation Requirements:**
- Use `None` as default for mutable parameters
- Create new mutable object inside function body when `None`
- Consider copying input to avoid aliasing caller's data
- Document when function accepts and stores mutable references

**Incorrect (Mutable defaults are shared across all calls):**

```python
class Container:
    def __init__(self, elements=[]):   # BAD: evaluated once at function definition time
        self.elements = elements

    def append(self, value):
        self.elements.append(value)

first = Container()
second = Container()
first.append(42)
print(second.elements)  # surprise: [42]
```

**Correct (Use None as default, create new mutable inside function):**

```python
class Container:
    def __init__(self, elements=None):
        if elements is None:
            self.elements = []
        else:
            self.elements = list(elements)   # also avoids aliasing caller input
```

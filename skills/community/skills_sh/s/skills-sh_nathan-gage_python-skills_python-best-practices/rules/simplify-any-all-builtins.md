---
title: Use any() / all() Over Boolean-Flag Loops
impact: LOW
impactDescription: shorter, short-circuits, no manual flag management
tags: simplify, builtins, any, all
---

## Use `any()` / `all()` Over Boolean-Flag Loops

When you're checking "does any element satisfy X?" or "do all elements satisfy X?", Python has built-ins for that. Agents sometimes write manual `found = False` / `break` patterns — more code, more bugs, no short-circuit benefit.

**Incorrect (manual flag + break):**

```python
def has_admin(users: list[User]) -> bool:
    found = False
    for user in users:
        if user.is_admin:
            found = True
            break
    return found

def all_ready(services: list[Service]) -> bool:
    for s in services:
        if not s.ready:
            return False
    return True
```

**Correct (built-ins):**

```python
def has_admin(users: list[User]) -> bool:
    return any(u.is_admin for u in users)

def all_ready(services: list[Service]) -> bool:
    return all(s.ready for s in services)
```

Both short-circuit — `any()` stops at the first truthy, `all()` stops at the first falsy.

**Pass a generator, not a list:**

```python
# wasteful — builds the full list before checking
any([expensive_check(x) for x in items])

# right — lazy generator, stops at first match
any(expensive_check(x) for x in items)
```

**Other built-ins worth remembering:**

```python
# count matches
count = sum(1 for x in items if x.valid)

# min / max with a key
cheapest = min(items, key=lambda x: x.price)

# first matching element (or None)
first_error = next((x for x in items if x.failed), None)
```

`next(generator, default)` is the Pythonic "find first or default" — more direct than a loop with an early return.

**When to use a loop instead:** when you need the loop variable for something else, the logic has side effects, or the condition is too complex to fit in a generator cleanly.

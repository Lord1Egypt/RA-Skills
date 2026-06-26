---
name: python-mutable-default-args
description: A Python function uses a mutable object (list, dict, set) as a default argument, sharing state across calls in a way that produces silent bugs.
emoji: 🐍
metadata:
  clawdis:
    os: [macos, linux, windows]
    language: python
---

# python-mutable-default-args

Python evaluates default argument values once at function definition time, not on each call. If the default is a mutable object — a list, dict, or set — that object is shared across every call that uses the default. Mutating it inside the function modifies the default for all future calls. The bug is invisible until the second or later call and produces state-dependent failures that are hard to trace.

## Symptoms

```python
def add_item(item, items=[]):   # ← shared list
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"]  ← unexpected; second caller sees first caller's data
```

- A function that accumulates data into a list or dict default grows unboundedly across calls.
- A function that should be stateless produces different results on the second call than the first.
- Unit tests pass in isolation but fail when run together due to shared state from a prior test.
- The bug disappears if the function is called with an explicit argument.

## What to do

- Use `None` as the default and initialize the mutable inside the function body:

  ```python
  def add_item(item, items=None):
      if items is None:
          items = []
      items.append(item)
      return items
  ```

- This is the canonical Python idiom. Every call that omits `items` gets a fresh list.
- Applies equally to `dict`, `set`, and any other mutable type. The rule is: never use a mutable as a default argument.
- When reviewing code, scan every function signature for `=[]`, `={}`, `=set()` as a heuristic for this pattern.
- Linters (pylint rule `W0102`, ruff rule `B006`) will flag this automatically — enable them if the codebase doesn't already.

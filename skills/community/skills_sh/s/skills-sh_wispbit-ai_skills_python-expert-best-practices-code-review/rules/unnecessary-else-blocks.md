---
title: Unnecessary else blocks in Python
impact: LOW
impactDescription: Reduces nesting and improves code readability
tags: python, code-clarity, readability, control-flow, simplicity
---

Avoid unnecessary `else` blocks when the `if` block ends with a return statement, break, continue, or similar control flow statements.

Bad:

```python
def process_value(value):
    if value > 10:
        return "high"
    else:
        return "low"
```

```python
def check_items(items):
    for item in items:
        if len(item) > 5:
            print("Long item:", item)
            continue
        else:
            print("Short item:", item)
```

Good:

```python
def process_value(value):
    if value > 10:
        return "high"
    return "low"
```

```python
def check_items(items):
    for item in items:
        if len(item) > 5:
            print("Long item:", item)
            continue
        print("Short item:", item)
```

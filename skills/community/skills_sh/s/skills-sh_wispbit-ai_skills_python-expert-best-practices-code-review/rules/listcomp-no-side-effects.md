---
title: List Comprehensions Must Produce Values You Use
impact: HIGH
impactDescription: Prevents side-effect list comprehensions that waste memory and reduce code clarity
tags: list-comprehensions, code-clarity, side-effects, readability, generators
---

## List Comprehensions Must Produce Values You Use

**Impact: HIGH (Prevents side-effect list comprehensions that waste memory and reduce code clarity)**

List comprehensions must produce a value you use (no "side-effect listcomps"). Using list comprehensions for side effects creates unnecessary lists in memory, obscures intent, and makes code harder to maintain. List comprehensions should be reserved for transforming data, not executing actions.

**When to Trigger:**
- List comprehension used as a standalone statement (result not assigned, returned, or consumed)
- List comprehension spans multiple lines with multiple conditions/transforms
- The primary purpose is side effects (function calls, mutations) rather than value creation
- Complex filtering logic that makes the comprehension hard to read

**When List Comprehensions Are Appropriate:**
- Creating new lists by transforming data
- Filtering and mapping operations with clear, simple logic
- Single-line transformations that fit naturally in expression form
- Generator expressions for lazy evaluation

**Implementation Requirements:**
- Use plain `for` loops when performing side effects
- Break complex comprehensions into named generator expressions
- Use generator expressions `()` instead of list comprehensions `[]` for pipelines
- Keep comprehensions simple and readable (ideally single line)

**Incorrect (Side-effect list comprehensions waste memory and obscure intent):**

```python
# BAD: result list is ignored; the listcomp is just a loop-with-side-effects
[storage.save(item, process(item)) for item in collection]  # creates a whole list of N Nones (or results) and throws it away

# BAD: hard-to-read multi-line listcomp doing too much
results = [
    transform(parse(entry))
    for entry in data
    if entry.strip()
    if not entry.startswith("#")
    if validate(entry)
]
```

**Correct (Plain loops for side effects, named generator pipelines):**

```python
# GOOD: plain loop for side effects
for item in collection:
    storage.save(item, process(item))

# GOOD: break complex pipelines into named steps
filtered = (entry for entry in data if entry.strip() and not entry.startswith("#"))
parsed = (parse(entry) for entry in filtered)
results = [transform(r) for r in parsed if validate(r)]
```

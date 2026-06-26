---
title: Return NotImplemented for Unsupported Operand Types
impact: CRITICAL
impactDescription: Enables proper operator protocol and prevents breaking Python's reverse operation fallback
tags: operators, __add__, __iadd__, notimplemented, dunder-methods, operator-overloading
---

## Return NotImplemented for Unsupported Operand Types

**Impact: CRITICAL (Enables proper operator protocol and prevents breaking Python's reverse operation fallback)**

When implementing operators, return `NotImplemented` for unsupported operand types instead of raising `TypeError` directly. This allows Python to try reverse operations (e.g., `__radd__`) and provides better error messages. Design `+` and `+=` intentionally with different acceptance criteria to match Python's built-in behavior.

**When to Trigger:**

In `__add__`, `__mul__`, comparisons, etc.:
- Operand type isn't supported → return `NotImplemented` (not raise `TypeError`)
- Let Python handle reverse operation fallback and error messages

In `__iadd__` and other in-place ops:
- Must always return `self` for proper chaining behavior
- Can accept broader types than regular operators (e.g., `+=` accepts any iterable, `+` requires same type)
- Provide helpful error messages that guide users to the solution

**Implementation Requirements:**
- Return `NotImplemented` for unsupported types in binary operators
- Always return `self` from augmented assignment operators (`__iadd__`, `__imul__`, etc.)
- Design `+=` to be more liberal than `+` when appropriate
- Provide clear, actionable error messages
- Follow the principle: `+` creates new objects, `+=` modifies in place

**Incorrect (Raises TypeError directly, breaks reverse operations, forgets return self):**

```python
class Container:
    def __add__(self, other):
        if not isinstance(other, Container):
            raise TypeError("can't add")   # BAD: short-circuits reverse-op logic; unhelpful message
        return Container(self.elements + other.elements)

    def __iadd__(self, other):
        self.elements += other.elements
        # BAD: forgot "return self" -> can break chained behavior
```

**Correct (Returns NotImplemented, accepts broader types in +=, always returns self):**

```python
class Container:
    def __add__(self, other):
        if isinstance(other, Container):
            return Container(self.elements + other.elements)
        return NotImplemented  # let Python handle it

    def __iadd__(self, other):
        try:
            it = iter(other.elements if isinstance(other, Container) else other)
        except TypeError:
            raise TypeError("right operand in += must be 'Container' or an iterable")
        self.elements.extend(it)
        return self
```

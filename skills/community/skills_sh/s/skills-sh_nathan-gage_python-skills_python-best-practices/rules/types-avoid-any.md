---
title: Avoid Any Annotations
impact: MEDIUM
impactDescription: narrows types in new code; retrofitting existing `Any` is churn
tags: types, any, precision, protocols
---

## Avoid `Any` Annotations

`Any` turns off the type checker for that value — it accepts anything, produces anything, and propagates silently into every call site that consumes it. `Any` is common when the right type feels hard to write; almost always, a `Protocol`, `TypeVar`, or `Union` is available.

**Incorrect (Any leaks through the system):**

```python
from typing import Any

def process_items(items: Any) -> Any:
    return [transform(item) for item in items]

def transform(item: Any) -> Any:
    return item.value.upper()
```

The checker cannot help here. A caller passing a `dict` instead of a list silently walks into runtime errors. `item.value.upper()` is unchecked — a typo in `value` would never be caught.

**Correct (precise types; Protocol for duck-typed inputs):**

```python
from typing import Protocol

class HasValue(Protocol):
    value: str

def process_items(items: list[HasValue]) -> list[str]:
    return [transform(item) for item in items]

def transform(item: HasValue) -> str:
    return item.value.upper()
```

The checker now verifies that every call site passes a list of objects with a `.value: str` attribute. Typos in `.value` get caught. Return types propagate.

**Correct (TypeVar for truly generic containers):**

```python
from typing import TypeVar

T = TypeVar("T")

def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None
```

Generic, not unchecked.

**When `Any` is genuinely unavoidable** (interop with dynamically typed libraries, some JSON boundaries), restrict its scope to one line, narrow to a concrete type immediately, and document the invariant in a comment.

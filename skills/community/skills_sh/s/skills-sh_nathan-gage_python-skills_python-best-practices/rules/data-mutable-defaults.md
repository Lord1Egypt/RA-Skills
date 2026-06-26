---
title: Never Use Mutable Default Arguments
impact: CRITICAL
impactDescription: prevents shared-state bugs across calls and instances
tags: data, defaults, mutability, dataclass, pydantic
references: https://docs.python.org/3/tutorial/controlflow.html#default-argument-values, https://docs.python.org/3/library/dataclasses.html#mutable-default-values, https://docs.pydantic.dev/latest/concepts/fields/#using-pydanticfield-to-describe-fields
---

## Never Use Mutable Default Arguments

A default argument is evaluated **once**, when the `def` statement runs — not each call. A mutable default (`[]`, `{}`, `set()`, a dataclass instance) is therefore shared across every call that doesn't override it. Appending to the "default" list on one call mutates the default for every subsequent call. The same trap applies to dataclass and Pydantic field defaults. Always use `None` + body construction, or `default_factory`.

**Incorrect (the `[]` is one object, reused across calls):**

```python
def append_item(item: int, items: list[int] = []) -> list[int]:
    items.append(item)
    return items

append_item(1)  # [1]
append_item(2)  # [1, 2]   ← surprise: same list as before
```

**Correct (function — sentinel + per-call construction):**

```python
def append_item(item: int, items: list[int] | None = None) -> list[int]:
    if items is None:
        items = []
    items.append(item)
    return items
```

**Correct (dataclass / Pydantic — `default_factory` calls the constructor per instance):**

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

@dataclass
class User:
    tags: list[str] = field(default_factory=list)

class Config(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

`@dataclass` rejects bare mutable defaults with `ValueError`. Pydantic v2 happens to deep-copy the default for each instance, but `Field(default_factory=list)` makes the intent explicit and survives version changes. Safe to use directly as defaults: tuples, frozensets, strings, ints, `None`, and frozen dataclasses — anything that can't be mutated.

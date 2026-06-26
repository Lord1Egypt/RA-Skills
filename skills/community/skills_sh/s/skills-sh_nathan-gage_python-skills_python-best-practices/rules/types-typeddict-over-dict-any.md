---
title: Use TypedDict or Dataclass Instead of dict[str, Any]
impact: MEDIUM
impactDescription: structured alternative to `dict[str, Any]` when writing new code
tags: types, typeddict, dataclass, any
references: https://docs.python.org/3/library/typing.html#typing.TypedDict, https://docs.pydantic.dev/latest/concepts/models/
---

## Use TypedDict or Dataclass Instead of `dict[str, Any]`

When the shape of a dict is known — config objects, API payloads, structured events — `dict[str, Any]` is a lie about the data. The structure exists; it's just not declared, so every access is a runtime gamble. `TypedDict` or `dataclass` restores type-checker coverage.

**Incorrect (structure erased):**

```python
from typing import Any

def create_user(config: dict[str, Any]) -> User:
    name = config["name"]            # what type?
    age = config.get("age", 0)       # what type?
    prefs = config.get("prefs", {})  # dict or the passed-in value?
    return User(name=name.upper(), age=age + 1, prefs=prefs)
```

**Correct (`TypedDict` — dict-shaped but typed; use at serialization boundaries):**

```python
from typing import TypedDict, NotRequired

class UserConfig(TypedDict):
    name: str
    age: NotRequired[int]
    prefs: NotRequired["UserPreferences"]

def create_user(config: UserConfig) -> User:
    return User(name=config["name"].upper(), age=config.get("age", 0))
```

For in-memory values with behavior and defaults, prefer a `dataclass`; when you also need runtime validation, `pydantic.BaseModel`. `dict[str, Any]` is the right answer only for genuinely unstructured data — log context, free-form metadata. If you know the fields, declare them.

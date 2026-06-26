---
title: Order Required Fields Before Optional Fields
impact: HIGH
impactDescription: Python enforces this at class-definition time
tags: api, dataclasses, defaults
references: https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass, https://docs.python.org/3/library/dataclasses.html#dataclasses.KW_ONLY
---

## Order Required Fields Before Optional Fields

Python's dataclass implementation requires fields without defaults to precede fields with defaults — trying to put an optional field before a required one is a `TypeError` at class-definition time. More importantly, the order communicates intent: required first, defaults last.

**Incorrect (raises `TypeError`):**

```python
from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    description: str = ""
    version: str         # TypeError: non-default argument follows default argument
```

**Correct (required fields first):**

```python
from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    version: str
    description: str = ""
```

**When a required field must come after an optional one:** use keyword-only with `KW_ONLY`. This lets you reorder freely while still enforcing "required" via the type system:

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class Tool:
    name: str
    _: KW_ONLY
    description: str = ""
    version: str  # required, keyword-only — order no longer constrained
```

Everything after `_: KW_ONLY` is keyword-only, so the "required before optional" rule stops applying — the caller must pass them by name.

**Same rule applies to function parameters:**

```python
# bad: positional default before positional required
def connect(host="localhost", port): ...  # SyntaxError

# good: required first
def connect(port, host="localhost"): ...

# also good: keyword-only lets you mix freely
def connect(*, port, host="localhost", retries): ...
```

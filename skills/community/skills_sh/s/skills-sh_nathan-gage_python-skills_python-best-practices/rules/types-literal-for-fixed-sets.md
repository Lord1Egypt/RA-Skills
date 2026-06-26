---
title: Use Literal Types for Fixed String Sets
impact: MEDIUM
impactDescription: catches invalid strings at type-check time
tags: types, literal, strings, validation
---

## Use `Literal` Types for Fixed String Sets

When a parameter accepts one of a fixed set of string values, `str` is too wide — every typo is legal. `Literal["a", "b", "c"]` narrows the type to exactly those values and enables `match` exhaustiveness checking.

**Incorrect (plain str accepts anything):**

```python
def set_log_level(level: str) -> None:
    ...

set_log_level("DEUBG")  # typo — compiles fine, runtime surprise
```

The checker cannot tell you `"DEUBG"` is invalid. A typo at a call site silently passes through until the function hits an unexpected branch.

**Correct (Literal restricts to the valid set):**

```python
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

def set_log_level(level: LogLevel) -> None:
    ...

set_log_level("DEUBG")  # type error — caught at type-check time
```

IDEs autocomplete the valid values. Typos are flagged before running.

**Pairs well with `match`:**

```python
def level_priority(level: LogLevel) -> int:
    match level:
        case "DEBUG": return 10
        case "INFO": return 20
        case "WARNING": return 30
        case "ERROR": return 40
```

If a new level is added to the `Literal` type without updating this `match`, checkers with exhaustiveness support flag the missing case.

**When to use `Enum` instead:** when the values have methods or rich behavior (e.g., `LogLevel.DEBUG.name`, `LogLevel.DEBUG.value`). Enums also work well with exhaustiveness checking but carry more ceremony than `Literal`. For plain string tags, `Literal` is lighter.

**When to use plain `str`:** free-form user input, message bodies, URLs, any field that isn't a finite enumeration.

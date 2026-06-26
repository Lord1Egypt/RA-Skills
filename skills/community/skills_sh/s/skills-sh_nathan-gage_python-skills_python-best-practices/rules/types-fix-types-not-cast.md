---
title: Fix Type Definitions Instead of cast()
impact: MEDIUM
impactDescription: keeps source type definitions honest
tags: types, cast, design
---

## Fix Type Definitions Instead of `cast()`

`cast(T, value)` tells the checker to pretend `value` is a `T` with no runtime check. When called to paper over a structural mismatch, it hides a design problem. Reach for it only when runtime logic genuinely narrows in a way the checker can't express.

**Incorrect (cast masks an unnecessarily wide return type):**

```python
from typing import cast

def load_config() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text())

def get_timeout() -> int:
    config = load_config()
    return cast(int, config["timeout"])  # we're just telling the checker to trust us
```

The real issue: `load_config` returns `dict[str, object]` because `json.loads` does. But this project's config has a known shape — fix the source type.

**Correct (declare the real structure):**

```python
from typing import TypedDict

class Config(TypedDict):
    timeout: int
    retries: int

def load_config() -> Config:
    return json.loads(CONFIG_PATH.read_text())  # validate or cast here, once

def get_timeout() -> int:
    config = load_config()
    return config["timeout"]  # known to be int from Config
```

Now every downstream consumer benefits from the typed shape.

**When `cast()` is the right tool:** when runtime logic narrows beyond what the checker can prove — e.g., after a literal tag check, a custom predicate, or a known invariant enforced elsewhere.

```python
from typing import cast

def handle_success(result: ApiResponse) -> str:
    # An earlier check already verified result.status == "success"
    # but the checker can't propagate that narrowing here
    assert result.status == "success"
    return cast(SuccessResponse, result).data  # ok; narrowing is real
```

Even then, `isinstance` or a `TypeGuard` function is usually cleaner. Reserve `cast` for cases where those don't fit.

**Rule of thumb:** before reaching for `cast`, ask whether the source type should be narrower. 8 times out of 10, yes.

---
title: Remove Redundant `| None` When Values Are Guaranteed
impact: LOW-MEDIUM
impactDescription: eliminates false uncertainty in the type signature
tags: types, optional, none, annotations
---

## Remove Redundant `| None` When Values Are Guaranteed

An annotation of `X | None` tells readers and the checker that `None` is a real possibility — every consumer now writes a `None` check. When the value is guaranteed to be set (by the constructor, by the control flow, by an earlier validation), `| None` lies about the API.

**Incorrect (optional annotation on a guaranteed-present value):**

```python
from dataclasses import dataclass

@dataclass
class Session:
    user_id: str
    token: str | None = None  # but we always generate a token in __post_init__

    def __post_init__(self) -> None:
        if self.token is None:
            self.token = generate_token()
```

Every consumer of `session.token` now writes `if session.token is not None: ...` — for a value that is always present.

**Correct (use a factory default; drop the optional):**

```python
from dataclasses import dataclass, field

@dataclass
class Session:
    user_id: str
    token: str = field(default_factory=generate_token)
```

`session.token` is now unambiguously a `str`. No defensive `None` checks downstream.

**Also incorrect (`| None` on `NotRequired` TypedDict fields):**

```python
from typing import TypedDict, NotRequired

class Config(TypedDict):
    name: str
    timeout: NotRequired[int | None]  # already optional via NotRequired
```

`NotRequired` already expresses "may be absent." Adding `| None` lets the caller pass `None` *instead of* omitting — which is rarely what you want. Either the field is absent (`NotRequired`) or it has a value (no `| None`).

**When `| None` is correct:** when `None` is a real, semantic value — "no assignee," "no parent," "not yet fetched." Absence as a meaningful state deserves `None`.

**Heuristic:** if every consumer writes `if x is not None:` before using the value, either `None` is never really set (remove `| None`) or you should have a different sentinel (a default, a distinct variant).

---
title: Brand Primitive IDs With NewType
impact: MEDIUM
impactDescription: catches ID-confusion bugs at type-check time
tags: data, types, newtype, domain
---

## Brand Primitive IDs With NewType

When `user_id` and `team_id` are both `str`, a function accepting `UserId` will happily take a `TeamId` and fail at runtime — or worse, silently return wrong data. `NewType` makes them distinct at the type level without runtime overhead.

**Incorrect (interchangeable strings):**

```python
UserId = str
TeamId = str

def fetch_user(user_id: UserId) -> User: ...

team_id: TeamId = "team_xyz"
fetch_user(team_id)  # type checker is fine with this — runtime crash
```

`UserId = str` is a type *alias*, not a new type. The checker treats them identically.

**Correct (NewType creates a distinct nominal type):**

```python
from typing import NewType

UserId = NewType("UserId", str)
TeamId = NewType("TeamId", str)

def fetch_user(user_id: UserId) -> User: ...

team_id = TeamId("team_xyz")
fetch_user(team_id)  # type error: TeamId is not UserId
```

At runtime, `UserId("abc")` is just the string `"abc"` — no wrapper, no overhead. At type-check time, the checker refuses to confuse them.

**Construct at the boundary:** wrap raw strings as soon as they enter the system (API deserialization, DB rows). Once wrapped, they flow through the codebase as the branded type, and the checker enforces correctness.

**When NOT to brand:** short-lived local variables, truly interchangeable strings (raw log message bodies, arbitrary user text). Reserve branding for domain identifiers that must not be mixed up.

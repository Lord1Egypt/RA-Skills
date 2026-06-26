---
title: Use a Sentinel Object When None Is a Real Domain Value
impact: MEDIUM
impactDescription: distinguishes "no value passed" from "None passed deliberately"
tags: data, sentinel, none, optional, defaults
references: https://peps.python.org/pep-0661/, https://docs.python.org/3/library/typing.html#typing.Optional
---

## Use a Sentinel Object When `None` Is a Real Domain Value

When `None` carries semantic meaning — "user cleared this field," "no parent," "no assignee" — `None` can't also be the "not provided" default. Use a private sentinel instead. The sentinel is a unique object compared with `is`, never `==`. Complements `types-remove-redundant-optional`: that rule says drop `| None` when `None` is impossible; this one says use a sentinel when `None` is meaningfully different from "not passed."

**Incorrect (`None` does double duty as "absent" and "cleared"):**

```python
def update_user(user_id: str, nickname: str | None = None) -> User:
    user = db.get(user_id)
    user.nickname = nickname        # was the caller clearing it, or not passing it?
    db.save(user)
    return user
```

**Correct (sentinel default; `None` means "clear"):**

```python
from typing import Final

class _Unset:
    def __repr__(self) -> str:
        return "UNSET"

UNSET: Final = _Unset()

def update_user(user_id: str, nickname: str | None | _Unset = UNSET) -> User:
    user = db.get(user_id)
    if nickname is not UNSET:
        user.nickname = nickname     # may be None (cleared) or a real string
    db.save(user)
    return user

update_user("u1")                    # nickname untouched
update_user("u1", nickname=None)     # nickname cleared
update_user("u1", nickname="bob")    # nickname set to "bob"
```

Pydantic's PATCH pattern uses the same idea — `Field(default=UNSET)` + filtering `{k: v for k, v in model_dump().items() if v is not UNSET}` gives you "omitted field" vs. "explicit null."

A private `_SENTINEL = object()` is fine for tiny internal cases — PEP 661 itself uses that idiom. Prefer a named sentinel class (as above) when the sentinel appears in signatures, reprs, logs, or tracebacks, since the `__repr__` makes debugging easier. PEP 661 proposes a standard `sentinel(...)` helper, but it is still Draft and has not shipped in the `typing` module; do not claim `typing.Sentinel` exists. And don't reach for sentinels when `None` already means "absent" — two-state `Optional` doesn't need them.

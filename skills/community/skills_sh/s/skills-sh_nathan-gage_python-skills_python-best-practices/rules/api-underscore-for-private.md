---
title: Underscore Prefix for Private Names
impact: LOW-MEDIUM
impactDescription: signals internal API and limits backward-compat obligations
tags: api, privacy, public-api
---

## Underscore Prefix for Private Names

Names that start with `_` are internal. Names that don't are public — and public means "backward-compatible forever unless deprecated." Without language-level enforcement, implementation details often stay public; underscore them on the way in, not after they've leaked.

**Incorrect (implementation detail treated as public):**

```python
# mymodule.py
def format_date(d):
    return _to_iso_string(d)

def to_iso_string(d):    # helper — but no underscore, so it's public
    return d.isoformat()

__all__ = ["format_date", "to_iso_string"]  # accidentally exported
```

Now `to_iso_string` is part of the module's public API. Changing its signature, renaming it, or removing it breaks anyone who imported it.

**Correct (underscore the helper; exclude from `__all__`):**

```python
# mymodule.py
def format_date(d):
    return _to_iso_string(d)

def _to_iso_string(d):
    return d.isoformat()

__all__ = ["format_date"]
```

`_to_iso_string` is clearly internal. You can rename it, delete it, change its signature — no backward-compat obligation.

**Same rule for class attributes and methods:**

```python
class Cache:
    def get(self, key: str) -> object | None: ...     # public
    def _evict_lru(self) -> None: ...                  # internal helper
    def _entries(self) -> dict[str, object]: ...       # internal state access
```

**Don't reach into `_private` from outside.** If you find yourself writing `obj._internal`, either (a) the attribute should be public and the owner should know, or (b) the design has a gap — add a public method instead. Reaching into `_private` couples you to implementation details that may change.

**`__all__` is the contract:** `from mymodule import *` respects `__all__`. Tools like Sphinx and type checkers also use it to determine the public surface. Keep it minimal and accurate.

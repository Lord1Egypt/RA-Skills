---
title: Keep Old Names as Deprecated Aliases
impact: MEDIUM
impactDescription: enables gradual migration without breakage
tags: api, deprecation, compatibility
references: https://peps.python.org/pep-0702/, https://docs.python.org/3/library/warnings.html#warnings.deprecated, https://docs.python.org/3/library/warnings.html#warnings.warn
---

## Keep Old Names as Deprecated Aliases

Renaming a public function, class, or parameter is a breaking change. Users upgrade at their own pace; if the old name vanishes, they can't. Keep the old name as a deprecated alias for at least one release, pointing at the new name.

**Incorrect (rename breaks existing code immediately):**

```python
# v1.0
def get_user(user_id: str) -> User: ...

# v1.1
def fetch_user(user_id: str) -> User: ...  # v1.0 callers now crash
```

**Correct (Python 3.13+: `@warnings.deprecated` marks the symbol for type checkers too):**

```python
import warnings

@warnings.deprecated("get_user is deprecated; use fetch_user instead.")
def get_user(user_id: str) -> User:
    return fetch_user(user_id)
```

On older Pythons, call `warnings.warn("...", DeprecationWarning, stacklevel=2)` inside the alias body — same runtime effect, minus the static-checker signal.

For renamed *parameters*, `@warnings.deprecated` doesn't apply — it decorates whole symbols. Accept the old keyword as a compatibility path with a sentinel default, forward to the new name, and emit `warnings.warn(..., DeprecationWarning, stacklevel=2)` when the old path is taken. Remove the alias in a later major version. Skip deprecation only when the name was never public (starts with `_`, not in `__all__`, not in docs).

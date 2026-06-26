---
title: Use Keyword-Only Parameters for Optional Config
impact: MEDIUM
impactDescription: prevents breakage when adding or reordering params
tags: api, parameters, keyword-only, compatibility
references: https://docs.python.org/3/library/dataclasses.html#dataclasses.KW_ONLY, https://peps.python.org/pep-3102/
---

## Use Keyword-Only Parameters for Optional Config

Positional parameters lock in their order forever — adding a new parameter in the middle breaks every caller. Keyword-only parameters (after `*` in functions, after `_: KW_ONLY` in dataclasses) let you add, remove, or reorder without breaking callers. Positional is Python's default; keyword-only is an explicit choice.

**Incorrect (positional config — order is now part of the API):**

```python
def fetch(url, timeout=30, retries=3, verify_ssl=True, backoff=1.5):
    ...

fetch("https://api.example.com", 60, 5, False)
```

What do `60, 5, False` mean at this call site? Only the function signature knows. And if you want to add `user_agent` between `retries` and `verify_ssl`, every positional call site breaks.

**Correct (keyword-only for config params):**

```python
def fetch(url, *, timeout=30, retries=3, verify_ssl=True, backoff=1.5):
    ...

fetch("https://api.example.com", timeout=60, retries=5, verify_ssl=False)
```

The `*` forces everything after it to be passed by name. Call sites self-document. New params can slot anywhere without breaking callers.

**For dataclasses, use `KW_ONLY`:**

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class FetchOptions:
    url: str
    _: KW_ONLY
    timeout: int = 30
    retries: int = 3
    verify_ssl: bool = True
    backoff: float = 1.5
```

Callers must pass `timeout=`, `retries=`, etc. by name.

**Heuristic:** the first one or two params can be positional (the "thing" the function operates on). Everything else — especially optional configuration — should be keyword-only.

**For public APIs this is non-negotiable:** once a library ships positional config params, every reorder or addition is a breaking change.

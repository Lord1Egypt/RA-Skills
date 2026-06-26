---
title: Use UPPER_CASE for Module Constants
impact: LOW
impactDescription: signals immutability and public/private scope
tags: naming, constants, conventions
---

## Use `UPPER_CASE` for Module Constants

Module-level values that don't change during execution are constants. The `UPPER_CASE` convention signals "don't reassign this" and is widely recognized across Python codebases. A reader seeing `default_timeout` can't tell at a glance whether it's a constant or a mutable config someone might reassign.

**Incorrect (looks like a reassignable variable):**

```python
default_timeout = 30
max_retries = 3
allowed_hosts = frozenset({"localhost", "127.0.0.1"})
```

**Correct (UPPER_CASE for constants; `_` prefix for internal):**

```python
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
ALLOWED_HOSTS = frozenset({"localhost", "127.0.0.1"})
_DEFAULT_CACHE_SIZE = 512
```

The underscore keeps internal constants out of `from module import *` and signals they're not part of the public API. Enum members and class-level constants follow the same convention (`Color.RED`, `Cache.DEFAULT_SIZE`). For machine-enforced immutability, pair with `typing.Final`:

```python
from typing import Final

DEFAULT_TIMEOUT: Final[int] = 30  # checker flags any reassignment
```

Keep `lower_case` for values that look like constants but aren't — derived from `os.environ` at import, intentionally reassignable feature flags, or test-mutable hooks. The convention is for *intentional* constants.

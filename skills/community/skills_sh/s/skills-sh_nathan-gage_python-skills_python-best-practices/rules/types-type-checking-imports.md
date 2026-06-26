---
title: Use TYPE_CHECKING for Optional Dependencies
impact: LOW-MEDIUM
impactDescription: preserves type hints without forcing the import
tags: types, imports, optional-dependencies, typing
---

## Use `TYPE_CHECKING` for Optional Dependencies

When a module's type hints reference a class from an optional dependency, importing the module should not require that dependency to be installed. `if TYPE_CHECKING:` blocks let the checker see the import while the runtime stays lean.

**Incorrect (importing an optional dep at runtime):**

```python
import anthropic  # crashes if anthropic is not installed

class AnthropicProvider:
    def __init__(self, client: anthropic.Client) -> None:
        self._client = client
```

A user installing just the core package and never touching Anthropic still gets a `ModuleNotFoundError` at import time.

**Incorrect (falling back to `Any`):**

```python
from typing import Any

class AnthropicProvider:
    def __init__(self, client: Any) -> None:  # we gave up on the type
        self._client = client
```

This works at runtime but loses type safety on every method that uses `self._client`.

**Correct (TYPE_CHECKING block + quoted hint):**

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import anthropic

class AnthropicProvider:
    def __init__(self, client: anthropic.Client) -> None:
        self._client = client
```

With `from __future__ import annotations`, all annotations are strings at runtime — so `anthropic.Client` in the signature doesn't need the import to resolve. The checker still resolves it during type-check because it sees the `TYPE_CHECKING` branch.

**Pattern for optional-dep packages:**

```python
# At module top
try:
    import anthropic
except ImportError as e:
    raise ImportError(
        "Please install the anthropic extra: `pip install 'mylib[anthropic]'`"
    ) from e
```

Combine the runtime guard (helpful error if the user hits a code path that needs the dep) with `TYPE_CHECKING` for the hints.

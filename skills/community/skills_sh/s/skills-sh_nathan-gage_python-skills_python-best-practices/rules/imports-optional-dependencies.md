---
title: Handle Optional Dependencies Explicitly
impact: LOW-MEDIUM
impactDescription: clear error messages instead of cryptic ImportError
tags: imports, optional-dependencies, packaging
---

## Handle Optional Dependencies Explicitly

When a package has optional integrations, importing the module should not require every optional dep. Handle `ImportError` at module scope with a message pointing to the install extra; raising `None`-valued placeholders produces `AttributeError` far from the root cause.

**Incorrect (silently swallowing the ImportError):**

```python
try:
    import anthropic
except ImportError:
    anthropic = None  # downstream code crashes with AttributeError later

class AnthropicProvider:
    def __init__(self):
        client = anthropic.Client()  # AttributeError: 'NoneType' has no 'Client'
```

**Correct (raise with an actionable install hint; preserve the original cause):**

```python
try:
    import anthropic
except ImportError as e:
    raise ImportError(
        "anthropic is required for AnthropicProvider. "
        "Install with: pip install 'mylib[anthropic]'"
    ) from e

class AnthropicProvider:
    ...
```

If the dep is optional at the *feature* level rather than the *module* level, defer the import into the function that needs it — users who never call it never pay the cost. Pair module-scope optional imports with a `TYPE_CHECKING` block (see `types-type-checking-imports`) when type hints should resolve without requiring the runtime dep.

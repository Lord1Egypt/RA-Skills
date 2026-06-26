---
title: Define TypeAdapter Instances at Module Level
impact: LOW-MEDIUM
impactDescription: avoids repeated schema construction
tags: perf, pydantic, type-adapter, module-level, applicability:pydantic
references: https://docs.pydantic.dev/latest/api/type_adapter/
---

## Define `TypeAdapter` Instances at Module Level

**Applicability:** Pydantic v2's `TypeAdapter`. The same principle applies to any object whose constructor does real work.

`TypeAdapter` builds a validation schema on construction by walking the target type, resolving annotations, and assembling the validation tree. Inside a hot function, every call rebuilds it. Create once at module scope; reuse.

**Incorrect (schema rebuilt on every call):**

```python
from pydantic import TypeAdapter

def parse_users(raw: bytes) -> list[User]:
    adapter = TypeAdapter(list[User])  # schema built every call
    return adapter.validate_json(raw)
```

**Correct (module-level constant):**

```python
_USERS_ADAPTER: TypeAdapter[list[User]] = TypeAdapter(list[User])

def parse_users(raw: bytes) -> list[User]:
    return _USERS_ADAPTER.validate_json(raw)
```

When the target type depends on a runtime value, cache per type with `@functools.cache`:

```python
@cache
def _adapter_for(model_type: type) -> TypeAdapter:
    return TypeAdapter(model_type)
```

The same pattern applies to `json.JSONDecoder` with custom hooks, `msgpack.Packer` / `Unpacker` with configuration, compiled templates, and precomputed lookup tables — anything whose constructor does real work.

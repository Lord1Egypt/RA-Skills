---
title: Prefer Tuple Syntax in isinstance() Only on Profiled Hot Paths
impact: LOW
impactDescription: tiny per-call savings; only relevant in tight loops
tags: perf, isinstance, micro-optimization, hot-path
references: https://docs.python.org/3/library/functions.html#isinstance, https://peps.python.org/pep-0604/
---

## Prefer Tuple Syntax in `isinstance()` Only on Profiled Hot Paths

Both `isinstance(x, (A, B, C))` and `isinstance(x, A | B | C)` are correct and supported in Python 3.10+. They produce the same result. The tuple form is *marginally* faster on each call because the union form constructs a `types.UnionType` object, but the gap is small enough that it only matters inside loops you've actually profiled. **Do not blanket-rewrite a codebase from union to tuple syntax** — the noise is rarely worth the diff.

This is a micro-optimization, not a correctness rule. Apply it only when:

1. The check is inside a measured hot path (a tight loop, called millions of times per request, etc.)
2. You have profiling data showing `isinstance` is a meaningful share of the time
3. You'd otherwise reach for a more invasive change (rewriting the dispatch, caching results)

In normal code, write whichever reads more naturally. `isinstance(x, int | float)` mirrors a type annotation and is a fine default.

**Incorrect (rewriting `A | B` to `(A, B)` everywhere as a stylistic crusade):**

```python
# A drive-by PR that flips every isinstance() in the codebase.
def is_numeric(x: object) -> bool:
    return isinstance(x, (int, float))   # was: isinstance(x, int | float)
```

The diff is pure churn. Annotations elsewhere use `int | float`; the inconsistency makes the codebase harder to read and the savings are imperceptible outside hot paths.

**Correct (apply only on a measured hot path, with a named module-level tuple):**

```python
# This validator runs once per row across ~10M rows in the ETL job — profiled.
_PRIMITIVE_TYPES = (int, float, str, bool)

def is_primitive(x: object) -> bool:
    return isinstance(x, _PRIMITIVE_TYPES)
```

Caching the tuple at module scope and giving it a clear name documents the intent ("this check is hot"). Anywhere else, `isinstance(x, int | float)` is fine.

**Do not rewrite for style alone.** A diff that flips `isinstance(x, A | B)` to `isinstance(x, (A, B))` across a codebase is pure churn — you lose the visual symmetry with type annotations and gain a few microseconds on a path that runs once.

**Annotations are unaffected.** In type annotations, `X | Y` is the modern form (PEP 604). The tuple form is only relevant inside `isinstance()` / `issubclass()` calls — and only on hot paths.

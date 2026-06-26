---
title: Use functools.lru_cache for Pure Functions
impact: LOW-MEDIUM
impactDescription: trades memory for CPU on repeatable computations
tags: perf, lru-cache, caching, functools
references: https://docs.python.org/3/library/functools.html#functools.lru_cache, https://docs.python.org/3/library/functools.html#functools.cache
---

## Use `functools.lru_cache` for Pure Functions

When a function is pure (same input → same output, no side effects) and called repeatedly with the same arguments, `@lru_cache` caches the result so subsequent calls are free. Agents often forget this exists and either hand-roll a dict cache or eat the recomputation cost.

**Incorrect (recomputing the same answer):**

```python
def parse_version(version_str: str) -> Version:
    # called from many call sites, often with the same string
    return Version.parse(version_str)
```

If 100 call sites ask `parse_version("1.2.3")`, you parse it 100 times.

**Correct (cached):**

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def parse_version(version_str: str) -> Version:
    return Version.parse(version_str)
```

First call parses and stores; subsequent calls return the cached `Version`. `maxsize` caps the cache to 256 entries (LRU eviction).

**`functools.cache` (Python 3.9+) for unbounded:**

```python
from functools import cache

@cache
def load_schema(name: str) -> Schema:
    return Schema.from_file(SCHEMA_DIR / f"{name}.json")
```

No size limit. Good when the key space is naturally small (like schema names) and entries are expensive to build.

**Requirements:**

- Arguments must be **hashable** (no mutable lists, dicts, or sets as args)
- Function must be **pure** — same inputs produce the same output
- No side effects that callers depend on happening each call

**When NOT to cache:**

- Arguments are unhashable (convert to tuple first, or use a different strategy)
- The function has meaningful side effects (logging, writes)
- The key space is unbounded and entries are large (cache grows without limit)
- The computation is cheap and the call frequency is low

**Hand-rolled caches:**

If `@lru_cache` doesn't fit (unhashable args, multi-level keys, time-based invalidation), build a module-level `dict` cache — but name it clearly and document the invalidation strategy. Uncontrolled hand-rolled caches leak memory.

**For instance methods, prefer `@cached_property`** when the "arguments" are just `self` — see `simplify-cached-property`.

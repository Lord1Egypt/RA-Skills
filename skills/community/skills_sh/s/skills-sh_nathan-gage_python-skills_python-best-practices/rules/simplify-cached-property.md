---
title: Use @cached_property Only When the Instance Supports It
impact: MEDIUM
impactDescription: defers work safely; misuse causes races and silent staleness
tags: simplify, cached-property, performance, threading
references: https://docs.python.org/3/library/functools.html#functools.cached_property
---

## Use `@cached_property` Only When the Instance Supports It

`@cached_property` defers expensive derivations until first access and caches the result in `instance.__dict__`. It fits when the inputs are effectively immutable, the getter is idempotent, the class has a writable `__dict__`, and nothing is racing on first access. Outside that envelope it masks real bugs: stale caches when inputs mutate, `TypeError` on `__slots__` classes without `__dict__`, and duplicated work when two threads hit the property simultaneously.

**Incorrect (mutable inputs — silent staleness):**

```python
from functools import cached_property
from dataclasses import dataclass, field

@dataclass
class Report:
    rows: list[Row] = field(default_factory=list)  # callers can append

    @cached_property
    def summary_stats(self) -> Stats:
        return compute_stats(self.rows)

r = Report()
r.summary_stats          # caches based on empty rows
r.rows.append(new_row)   # mutates input
r.summary_stats          # still the old cached Stats — stale, no warning
```

**Correct (frozen container; cache cannot go stale):**

```python
@dataclass(frozen=True)
class Report:
    rows: tuple[Row, ...]

    @cached_property
    def summary_stats(self) -> Stats:
        return compute_stats(self.rows)
```

**Caveats:** not thread-safe — two threads racing on first access can both run the getter. `__slots__` classes without `"__dict__"` raise `TypeError` at first access. `copy.copy` carries the cached value over; clear it manually if the copy's inputs differ. For module-level pure functions, use `functools.lru_cache` / `functools.cache` instead (see `perf-lru-cache-pure-fns`) — `@cached_property` is the per-instance equivalent.

---
title: Use set for Repeated Membership Checks
impact: MEDIUM
impactDescription: O(1) beats O(n)
tags: perf, set, membership, data-structures
---

## Use `set` for Repeated Membership Checks

`x in some_list` scans the list every time — O(n). `x in some_set` is a hash lookup — O(1). When you're checking membership repeatedly against the same collection, the set conversion pays for itself quickly.

**Incorrect (list membership in a loop):**

```python
def filter_allowed(items: list[Item], allowed: list[str]) -> list[Item]:
    return [item for item in items if item.id in allowed]
```

For each of `len(items)` checks, `in allowed` scans the whole list. If both are 10k, that's 100M comparisons.

**Correct (convert once, check many):**

```python
def filter_allowed(items: list[Item], allowed: list[str]) -> list[Item]:
    allowed_set = set(allowed)
    return [item for item in items if item.id in allowed_set]
```

Conversion is O(n); each `in` check is O(1). Total: O(n + m) instead of O(n × m).

**When to use `frozenset`:**

Module-level constants with fixed membership — can't be modified accidentally, hashable so it can be used as a dict key:

```python
_ADMIN_ROLES: frozenset[str] = frozenset({"admin", "owner", "superuser"})

def is_admin(role: str) -> bool:
    return role in _ADMIN_ROLES
```

**When NOT to convert to set:**

- Only checking membership once (conversion costs more than the scan)
- The collection is tiny (under ~10 elements) — list scan is competitive
- Order matters and you need the list semantics

**For lookups by key (not just membership), use a dict:**

```python
# bad — scanning a list for "the one with this id"
user = next((u for u in users if u.id == target_id), None)

# good — build once, look up many
users_by_id = {u.id: u for u in users}
user = users_by_id.get(target_id)
```

Same asymptotic improvement as set membership, and you get the associated value instead of just a boolean.

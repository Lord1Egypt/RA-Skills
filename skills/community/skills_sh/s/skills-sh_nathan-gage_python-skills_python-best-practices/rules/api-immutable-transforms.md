---
title: Return New Collections from Transforms
impact: MEDIUM
impactDescription: prevents surprising side effects
tags: api, immutability, mutation, transforms
---

## Return New Collections from Transforms

A function called `filter_active(users)` that mutates `users` in place is a trap — the name says "filter," the behavior says "modify." Default to returning new collections. Reserve mutation for functions whose names make it unmistakable (`sort_in_place`, `update_items`).

**Incorrect (transform that secretly mutates):**

```python
def filter_active(users: list[User]) -> list[User]:
    users[:] = [u for u in users if u.is_active]  # mutates input!
    return users
```

A caller doing `active = filter_active(all_users); log_total(len(all_users))` gets a confusing bug — `all_users` was modified, but the call site doesn't reveal that.

**Correct (return a new list):**

```python
def filter_active(users: list[User]) -> list[User]:
    return [u for u in users if u.is_active]
```

Input is untouched. Behavior matches the name.

**When in-place mutation is appropriate:** when it's performance-critical on a measured hot path, and the name signals it unambiguously.

```python
def sort_in_place(items: list[int]) -> None:
    items.sort()

def update_status_inplace(user: User, status: str) -> None:
    user.status = status
```

Name conventions:
- `*_in_place` / `*_inplace` — mutates, returns `None`
- `update_*` — mutates (if state-management convention) or returns new (if data-transform convention); be consistent within the codebase
- `with_*`, `filter_*`, `map_*`, `derive_*` — returns new, input untouched

**Rule of thumb:** if the function's name is a verb phrase describing a transformation, default to returning new. If it's imperative and clearly a command (`sort`, `apply`, `set`), mutation is expected.

---
title: Use Comprehensions Over for+append Loops
impact: LOW
impactDescription: more concise, often faster, and idiomatic Python
tags: simplify, comprehensions, idioms
---

## Use Comprehensions Over for+append Loops

Comprehensions express "build a collection from an iterable" in one line. C-style loops with `append()` have more variables and more places for off-by-one and wrong-list bugs. Reach for a comprehension by default.

**Incorrect (imperative loop + append):**

```python
def active_usernames(users: list[User]) -> list[str]:
    result = []
    for user in users:
        if user.is_active:
            result.append(user.name)
    return result
```

**Correct (list, dict, set, and generator forms):**

```python
def active_usernames(users: list[User]) -> list[str]:
    return [user.name for user in users if user.is_active]

name_to_id = {user.name: user.id for user in users}
unique_tags = {tag for post in posts for tag in post.tags}
total = sum(item.price for item in items)   # generator, no intermediate list
```

Break a comprehension into a loop when the expression stops reading like English — multi-step logic, side effects, or nested conditionals with intermediate variables are signs the comprehension has outgrown one line. For boolean reductions, prefer `any(u.is_admin for u in users)` over `any([...])` — the generator short-circuits and avoids materializing the list.

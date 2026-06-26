---
title: Inline Single-Use Intermediate Variables
impact: LOW
impactDescription: reduces noise and indirection
tags: simplify, variables, inline
---

## Inline Single-Use Intermediate Variables

When a variable is assigned once and used once immediately after, inlining it removes a name that doesn't earn its keep. Intermediates like `_filtered`, `_cleaned`, `_copy` show up "for clarity" — but the clarity is usually from the name, and if the name isn't informative, the variable is just noise.

**Incorrect (intermediates that add nothing):**

```python
def top_admins(users: list[User], limit: int) -> list[User]:
    filtered_users = [u for u in users if u.is_admin]
    sorted_users = sorted(filtered_users, key=lambda u: u.rank)
    result = sorted_users[:limit]
    return result
```

Four lines, four names — each used exactly once. The names restate the operations, not the purpose.

**Correct (inline when the operation is its own explanation):**

```python
def top_admins(users: list[User], limit: int) -> list[User]:
    return sorted(
        (u for u in users if u.is_admin),
        key=lambda u: u.rank,
    )[:limit]
```

Four operations, zero intermediate names. Each step's intent is visible in place.

**When an intermediate variable earns its place:**

- The name adds genuine information the expression doesn't convey
- The value is used more than once
- The expression would be too long to read as one unit
- Debugging benefits from a named step (breakpoints, logging)

```python
# the name "eligible" adds information the expression doesn't
def distribute_bonuses(users: list[User], amount: Decimal) -> None:
    eligible = [u for u in users if u.tenure_months >= 12 and not u.on_leave]
    share = amount / len(eligible)
    for user in eligible:
        pay_bonus(user, share)
```

Here `eligible` is used twice and the name documents the business rule. Keep it.

**Heuristic:** if you can't give the intermediate a name more meaningful than a restatement of the operation, inline it.

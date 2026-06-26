---
title: Flatten Nested if Statements Into and Conditions
impact: LOW
impactDescription: reduces indentation and improves readability
tags: simplify, control-flow, conditionals
---

## Flatten Nested `if` Statements Into `and` Conditions

When nested `if` statements share the same body with no intervening code, collapse them into a single `if` with `and`. The nested form implies the branches do something different; when they don't, the structure lies.

**Incorrect (nested if with no intervening code):**

```python
def should_notify(user: User, event: Event) -> bool:
    if user.is_active:
        if user.notifications_enabled:
            if event.priority >= user.notification_threshold:
                return True
    return False
```

**Correct (one combined condition):**

```python
def should_notify(user: User, event: Event) -> bool:
    return (
        user.is_active
        and user.notifications_enabled
        and event.priority >= user.notification_threshold
    )
```

Keep the nesting when intermediate logging, validation, or early returns happen between checks, or when the branches do genuinely different work. The rule: if every nested branch only holds another `if` until the final body, flatten. For chains where the happy path is the final action, the guard-clause form from `simplify-early-return` often reads cleanest.

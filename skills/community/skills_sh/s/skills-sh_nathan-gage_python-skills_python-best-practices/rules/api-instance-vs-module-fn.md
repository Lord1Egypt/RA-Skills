---
title: Choose the Simplest Namespace That Matches Ownership and Polymorphism
impact: LOW-MEDIUM
impactDescription: avoids unnecessary coupling without forcing a binary choice
tags: api, methods, functions, design, namespace
references: https://docs.python.org/3/tutorial/classes.html
---

## Choose the Simplest Namespace That Matches Ownership and Polymorphism

Python lets the same logic live as a module function, instance method, `@classmethod`, `@staticmethod`, or Protocol. None is universally right. Pick the smallest namespace that captures **ownership** (does this operation belong to one object?) and **polymorphism** (will multiple types provide their own version?). Start at module scope; promote to a method only when ownership or polymorphism actually demand it.

**Incorrect (instance method that doesn't need `self` and isn't overridden):**

```python
class DateFormatter:
    def format_iso(self, d: date) -> str:
        return d.isoformat()  # self unused, no subclasses overriding
```

**Correct (module-level function — simpler namespace):**

```python
def format_iso(d: date) -> str:
    return d.isoformat()
```

Conversely, a module function that threads state through a single parameter usually belongs on that type:

```python
# Awkward: mutates `user`, names it in every parameter list, no second caller type
def update_user_preferences(user: User, key: str, value: object) -> None:
    user.prefs[key] = value
    user.last_modified = now()

# Better: the method form matches ownership
class User:
    def update_preference(self, key: str, value: object) -> None:
        self.prefs[key] = value
        self.last_modified = now()
```

Use `@classmethod` for alternative constructors (`Event.from_json(raw)`); the method needs the class for subclass-friendly construction but not an instance. Use a `Protocol` when several unrelated types need to provide the same interface without a shared base. `@staticmethod` is the rarest tier — if there's no `self` and no `cls`, a module function is usually cleaner. Starting too coupled (everything on a class) is harder to undo than starting too loose (a free function you later move).

---
title: Use Specific Parameter and Variable Names
impact: LOW-MEDIUM
impactDescription: prevents confusion when multiple instances are in scope
tags: naming, parameters, variables
---

## Use Specific Parameter and Variable Names

Generic names like `id`, `name`, `data`, `info` communicate nothing about the value's role. When multiple IDs or data objects share a scope, they collide. Names that convey the semantic role make call sites self-documenting.

**Incorrect (generic names — call site is ambiguous):**

```python
def transfer(id: str, id2: str, data: dict, info: dict) -> None:
    ...

transfer("u123", "t456", {...}, {...})  # which is sender, which is recipient?
```

**Correct (specific — names carry the semantic role):**

```python
def transfer(
    sender_id: str,
    recipient_id: str,
    transfer_data: TransferRequest,
    audit_info: AuditContext,
) -> None:
    ...
```

Generic is acceptable for truly generic helpers (`def first(items: list[T]) -> T`), when there's only one of the type in scope (`def render(user: User)`), or following convention (`self`, `cls`, `_`, loop indices `i` / `j` in math contexts). The red flag is ending up with `id`, `id2`, `id3` or `data`, `info`, `details`, `meta` all in the same scope — the number suffixes tell you the names aren't doing their job. In nested loops, `for user in users` beats `for x in users` once the body is more than a couple of lines.

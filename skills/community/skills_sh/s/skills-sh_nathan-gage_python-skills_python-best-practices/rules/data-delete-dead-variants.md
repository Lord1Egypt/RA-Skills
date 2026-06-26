---
title: Delete Dead Variants
impact: LOW-MEDIUM
impactDescription: removes code paths that can't be reached
tags: data, types, unions, dead-code
---

## Delete Dead Variants

If a type has a variant that is never constructed — a `status: Literal["open", "closed", "archived"]` where `"archived"` is never set — delete the variant. Agents leave them behind "in case we need them later." The result is defensive branches in every consumer for a state that cannot occur.

**Incorrect ("archived" variant is declared but never produced):**

```python
from typing import Literal

OrderStatus = Literal["open", "paid", "shipped", "archived"]

def render_status(status: OrderStatus) -> str:
    match status:
        case "open": return "Awaiting payment"
        case "paid": return "Preparing to ship"
        case "shipped": return "In transit"
        case "archived": return "Archived"  # when does this branch ever run?
```

Grep the codebase: nothing assigns `"archived"`. That branch is unreachable, yet every consumer must handle it. It's a ghost.

**Correct (delete it):**

```python
from typing import Literal

OrderStatus = Literal["open", "paid", "shipped"]

def render_status(status: OrderStatus) -> str:
    match status:
        case "open": return "Awaiting payment"
        case "paid": return "Preparing to ship"
        case "shipped": return "In transit"
```

One fewer imaginary case. When "archived" actually becomes a requirement, add it then — tied to the real code that creates it.

**When NOT to delete:** if the variant exists in serialized data (old database rows, historical JSON) you still need to parse, keep it — but mark the non-canonical variants clearly (e.g., with a comment pointing to the migration that will remove them).

---
title: Return Early to Flatten Control Flow
impact: LOW-MEDIUM
impactDescription: keeps the happy path unnested and readable
tags: simplify, control-flow, guard-clauses
---

## Return Early to Flatten Control Flow

When a function has preconditions to check, return as soon as one fails. Deeply nested "if valid, if authorized, if ..." pyramids bury the happy path five levels in. Guard clauses flatten the structure and make the happy path the most visible branch.

**Incorrect (pyramid of nesting — the actual work is five levels in):**

```python
def process_request(req: Request) -> Response:
    if req.authenticated:
        if req.authorized:
            if req.body is not None:
                if req.body.is_valid:
                    return do_process(req.body)
                else:
                    return error(400, "invalid body")
            else:
                return error(400, "missing body")
        else:
            return error(403, "forbidden")
    else:
        return error(401, "unauthenticated")
```

**Correct (guard clauses; happy path unindented at the end):**

```python
def process_request(req: Request) -> Response:
    if not req.authenticated:
        return error(401, "unauthenticated")
    if not req.authorized:
        return error(403, "forbidden")
    if req.body is None:
        return error(400, "missing body")
    if not req.body.is_valid:
        return error(400, "invalid body")

    return do_process(req.body)
```

The same pattern applies to loops — `if not item.active: continue` instead of nesting the work inside `if item.active:`. Keep `if/else` when the two branches do comparable work (`"positive"` vs. `"negative"` vs. `"zero"`); guard-clause when one branch is an error and the other is the real work.

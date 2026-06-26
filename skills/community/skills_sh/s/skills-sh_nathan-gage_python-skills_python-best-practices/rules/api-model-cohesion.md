---
title: Keep Data Models Flat and Non-Redundant
impact: MEDIUM
impactDescription: reduces API surface and prevents field drift
tags: api, models, cohesion
---

## Keep Data Models Flat and Non-Redundant

Data models drift when fields duplicate each other, wrap single values in unnecessary containers, or mirror fields from the parent structure. Each duplicate is a second source of truth that can go stale. Each single-key wrapper adds access ceremony for no gain.

**Incorrect (redundant fields, single-key wrappers, unnecessary lists):**

```python
from dataclasses import dataclass

@dataclass
class ToolReturn:
    tool_name: str                           # also in parent
    call_id: str                             # also in parent
    content: dict[str, object]               # single-key wrapper around return_value
    return_value: dict[str, object]          # duplicated in content
    messages: list[Message]                  # always contains exactly one Message

@dataclass
class ToolCall:
    tool_name: str
    call_id: str
    return_part: ToolReturn
```

`tool_name` and `call_id` are carried on both the parent and the child — they'll drift. `content` wraps `return_value`. `messages` is a list that always has length one.

**Correct (flat, non-redundant):**

```python
from dataclasses import dataclass

@dataclass
class ToolReturn:
    content: object  # the actual return value, unwrapped
    message: Message

@dataclass
class ToolCall:
    tool_name: str
    call_id: str
    return_part: ToolReturn
```

`tool_name` and `call_id` live on the parent only. `content` holds the value directly. `message` is singular because there's only ever one.

**Check for:**

- Fields that exist on both parent and child (pick one, usually parent)
- `data: {"value": X}` single-key wrappers (unwrap to `data: X`)
- Lists that always contain exactly one element (use a scalar)
- Fields that are computed from other fields (derive, don't store)

**Why it matters:** redundancy means every mutation site has two (or more) places to update. Skipping one creates a drift bug that's only visible when the fields disagree.

**Related:** `data-derive-dont-store` is the same idea at the field level — if one field is computable from another, compute it, don't store it.

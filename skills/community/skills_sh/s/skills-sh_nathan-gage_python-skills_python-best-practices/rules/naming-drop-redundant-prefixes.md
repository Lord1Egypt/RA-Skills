---
title: Drop Redundant Prefixes When Context Is Clear
impact: LOW-MEDIUM
impactDescription: reduces noise and improves readability
tags: naming, prefixes, conventions
---

## Drop Redundant Prefixes When Context Is Clear

When a field is accessed as `tool_config.tool_description`, the `tool_` prefix adds nothing — the class name already provides that context. Repeating the class name in every field ("just to be clear") produces noise that makes real information harder to find.

**Incorrect (prefix repeats the class context):**

```python
from dataclasses import dataclass

@dataclass
class ToolConfig:
    tool_name: str
    tool_description: str
    tool_version: str
    tool_timeout: float
```

Every access reads `config.tool_name`, `config.tool_description`. The `tool_` adds zero information.

**Correct (name without the redundant prefix):**

```python
@dataclass
class ToolConfig:
    name: str
    description: str
    version: str
    timeout: float
```

Now `config.name`, `config.description` — shorter and just as clear.

**The rule:** drop the prefix when the class, module, or variable name already establishes the context.

**Examples from real codebases:**

```python
# before → after
server.server_label       → server.label
mcp_server.mcp_version    → mcp_server.version   (or just version on the class)
user_profile.user_id      → user_profile.user_id (probably keep — "id" alone is too generic)
```

The last example is a judgment call. `user_profile.id` would be unambiguous in context, but `user_id` reads well when passing it around as a variable. Lean toward dropping when it's a *field on* a class, keep the prefix when the value *travels as* a parameter.

**When to keep a prefix:**

- The field is a **foreign key** to another entity (`user_id` on a `Post`, `author_id` on a `Comment`) — the prefix signals what it points to
- Two related fields share a type and need disambiguation (`created_at` vs. `updated_at`)
- Dropping the prefix makes the name ambiguous (`format` could mean many things; `date_format` is specific)

**Be consistent:** whatever you pick, apply it uniformly across sibling fields. `tool_name` with `description` (mixed) reads worse than either all-prefixed or all-bare.

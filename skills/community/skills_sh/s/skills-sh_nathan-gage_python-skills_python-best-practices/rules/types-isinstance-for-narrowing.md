---
title: Use isinstance() for Type Checking, Not hasattr/getattr
impact: MEDIUM
impactDescription: enables proper type narrowing for the checker
tags: types, isinstance, narrowing, duck-typing
---

## Use `isinstance()` for Type Checking, Not `hasattr`/`getattr`

Type checkers narrow types through `isinstance()` checks, discriminator match statements, and `TypeGuard` functions — not through `hasattr()`, `getattr()`, or `type(obj).__name__ == "..."`. `hasattr` is common for "flexibility"; the actual cost is that the checker can't narrow and refactors silently break string comparisons.

**Incorrect (hasattr/getattr defeats type narrowing):**

```python
def process(part: MessagePart) -> str:
    if hasattr(part, "tool_name"):
        return f"Tool: {part.tool_name}"  # type checker: attribute is Any
    if getattr(part, "kind", None) == "text":
        return part.text  # type checker: does part.text exist? unclear
    if type(part).__name__ == "ImagePart":
        return f"Image: {part.url}"  # fragile: renaming ImagePart breaks this
    return "unknown"
```

The checker gives up on every branch. If `ToolPart` is renamed, the `type(...).__name__` string comparison silently stops matching — and no tests catch it because the function still runs.

**Correct (isinstance enables narrowing):**

```python
def process(part: MessagePart) -> str:
    if isinstance(part, ToolPart):
        return f"Tool: {part.tool_name}"  # narrowed to ToolPart
    if isinstance(part, TextPart):
        return part.text                    # narrowed to TextPart
    if isinstance(part, ImagePart):
        return f"Image: {part.url}"         # narrowed to ImagePart
    return "unknown"
```

Now the checker verifies that `part.tool_name`, `part.text`, and `part.url` each exist on the narrowed type. Renaming a class triggers type errors at every use site.

**For tagged unions, use `match` on the discriminator:**

```python
def process(part: MessagePart) -> str:
    match part.kind:
        case "tool":  return f"Tool: {part.tool_name}"
        case "text":  return part.text
        case "image": return f"Image: {part.url}"
```

When `part.kind` is a `Literal` discriminator on a `Union`, `match` narrows each branch to the matching variant.

**When to reach for `hasattr`:** genuinely optional extension protocols where classes may or may not implement a method. Even then, prefer `isinstance(obj, Protocol)` with a `runtime_checkable` Protocol over raw attribute probing.

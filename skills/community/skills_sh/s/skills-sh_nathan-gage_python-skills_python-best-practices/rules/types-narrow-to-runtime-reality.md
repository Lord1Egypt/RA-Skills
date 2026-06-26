---
title: Narrow Type Signatures to Runtime Reality
impact: MEDIUM
impactDescription: eliminates unreachable branches and false permissiveness
tags: types, narrowing, unions, design
references: https://docs.python.org/3/library/typing.html#typing.assert_never, https://typing.python.org/en/latest/spec/narrowing.html
---

## Narrow Type Signatures to Runtime Reality

If control flow (a `match` statement, an API contract, an earlier `isinstance` check) guarantees that only a subset of a union reaches a code path, the annotation should reflect that — not the wider union. Over-broad annotations create dead branches and suggest possibilities the code can't actually handle.

**Incorrect (signature wider than reality):**

```python
def render_tool_result(part: MessagePart) -> str:
    # by contract this is only called with ToolResultPart or ToolCallPart
    if isinstance(part, ToolResultPart):
        return f"Result: {part.content}"
    if isinstance(part, ToolCallPart):
        return f"Call: {part.tool_name}"
    if isinstance(part, TextPart):
        return part.text  # unreachable — caller never passes TextPart
    raise ValueError(f"unexpected part: {part}")
```

The `TextPart` branch can't run (the caller guarantees it), but the type says `MessagePart`. Readers have to figure out the contract from context.

**Correct (tighten the annotation):**

```python
ToolPart = ToolCallPart | ToolResultPart

def render_tool_result(part: ToolPart) -> str:
    if isinstance(part, ToolResultPart):
        return f"Result: {part.content}"
    return f"Call: {part.tool_name}"  # must be ToolCallPart
```

The signature documents the contract. No dead branches. A caller that tries to pass a `TextPart` gets a type error, not a runtime `ValueError`.

**When the wider type is necessary:** when the function genuinely handles the full union at some call sites and a subset at others, accept the widest used type and narrow inside. Don't invent a separate wider signature "to be safe."

**Exhaustiveness check:**

```python
from typing import assert_never

def render_tool_result(part: ToolPart) -> str:
    match part:
        case ToolResultPart(): return f"Result: {part.content}"
        case ToolCallPart(): return f"Call: {part.tool_name}"
        case _: assert_never(part)  # checker fails if union grows
```

`assert_never` ensures that if `ToolPart` gains a new variant, every `match` on it is re-examined.

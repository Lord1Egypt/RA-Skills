---
title: Extract Duplicated Logic Once Drift Risk Appears
impact: MEDIUM
impactDescription: prevents divergent implementations of the same logic
tags: simplify, extraction, dry
---

## Extract Duplicated Logic Once Drift Risk Appears

The first copy is fine. The second copy is the decision point: extract now, or accept drift later. A third copy is the safe default for "rule of three," but if the logic encodes a domain rule (validation, formatting, permissions) that must stay consistent, extract at the second copy. The cost of delay is bugs where copies evolved in subtly different directions.

**Incorrect (same logic duplicated across handlers):**

```python
def handle_stream(stream: AsyncIterator[Chunk]) -> Response:
    collected = []
    async for chunk in stream:
        if chunk.kind == "text":
            collected.append(chunk.text)
        elif chunk.kind == "tool":
            collected.append(format_tool(chunk))
    return Response(content="".join(collected))

def handle_non_stream(response: RawResponse) -> Response:
    collected = []
    for chunk in response.chunks:
        if chunk.kind == "text":
            collected.append(chunk.text)
        elif chunk.kind == "tool":
            collected.append(format_tool(chunk))
    return Response(content="".join(collected))
```

Two copies of the chunk-formatting logic. A new chunk kind gets added — two places need updates. One gets missed, and the streaming handler silently produces different output than the non-streaming one.

**Correct (extract once, use twice):**

```python
def _format_chunk(chunk: Chunk) -> str:
    match chunk.kind:
        case "text": return chunk.text
        case "tool": return format_tool(chunk)
        case _: return ""

async def handle_stream(stream: AsyncIterator[Chunk]) -> Response:
    parts = [_format_chunk(c) async for c in stream]
    return Response(content="".join(parts))

def handle_non_stream(response: RawResponse) -> Response:
    parts = [_format_chunk(c) for c in response.chunks]
    return Response(content="".join(parts))
```

Now a new chunk kind means one change. The two handlers can't drift apart.

**When NOT to extract:**

- The two occurrences look similar but serve genuinely different purposes — premature abstraction locks them together
- The shared logic is 2-3 trivial lines and naming a helper is more noise than value
- Each caller would need the helper to accept so many optional parameters that it becomes a mode-switch

**Location of the helper:**

- Private (`_name`) in the same module if it's specific to that module
- Module-level utility if multiple modules share it
- Base class method if it's a shared class operation (`data-explicit-variants`)

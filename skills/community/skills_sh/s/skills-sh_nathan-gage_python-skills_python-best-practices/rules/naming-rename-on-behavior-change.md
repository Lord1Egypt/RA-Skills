---
title: Rename When Behavior Changes
impact: MEDIUM
impactDescription: prevents misleading names from hiding behavior changes
tags: naming, refactoring, honesty
---

## Rename When Behavior Changes

A function's name is a promise about what it does. When the behavior changes — wider scope, different return type, side effects added — the old name lies. Names often stay stable because "it's a smaller diff"; the cost is that every future reader has to figure out the name is wrong.

**Incorrect (name no longer matches behavior):**

```python
# v1: called only for function tools
def _call_function_tool(tool: FunctionTool, args: dict) -> Result:
    return tool.invoke(args)

# v2: extended to handle output tools too, but name unchanged
def _call_function_tool(tool: FunctionTool | OutputTool, args: dict) -> Result:
    if isinstance(tool, FunctionTool):
        return tool.invoke(args)
    return tool.build_output(args)  # wait, this isn't a "function tool"
```

Every reader now has to re-learn what `_call_function_tool` means. The name says "function tool"; the body says "any tool."

**Correct (rename to reflect the wider scope):**

```python
def _call_tool(tool: FunctionTool | OutputTool, args: dict) -> Result:
    if isinstance(tool, FunctionTool):
        return tool.invoke(args)
    return tool.build_output(args)
```

Name matches behavior again.

**Signals that a rename is due:**

- The function's scope expanded (handles more types, more cases)
- The return type changed substantively
- Side effects were added or removed
- The function's "level" changed (was a leaf, now orchestrates; was a command, now a query)

**When in-place rename is fine:**

- Private (`_`-prefixed) functions — callers are all internal, update them
- Internal helpers with a small number of call sites

**When rename needs a migration:**

- Public API — add the new name, keep the old as a deprecated alias (see `api-deprecated-aliases`)
- Widely-used internal helpers — IDE-assisted rename is safer than hand-edit

**For method renames across a class hierarchy** — use the `@override` decorator when the intent is to override, and let the checker catch stragglers:

```python
from typing import override

class MemoryToolset(Toolset):
    @override
    def list_tools(self) -> list[Tool]: ...
```

If `Toolset` renames `list_tools`, `@override` makes the subclass fail type-checking until updated.

---
title: Scope Helpers and Constants to Their Usage Site
impact: LOW
impactDescription: reduces namespace pollution and clarifies intent
tags: structure, scope, helpers
references: https://peps.python.org/pep-0008/#imports
---

## Scope Helpers and Constants to Their Usage Site

Scope tiny helpers and one-off constants near their only use. Promote a helper to module scope when it is substantial, reused, independently testable, expensive to rebuild, or part of the module's contract. Nested functions are cheap inside a small callable, but stacking nontrivial logic inside another function hurts readability and makes the helper harder to test directly.

**Incorrect (tiny one-off constant hoisted into the module namespace):**

```python
# somewhere in a 500-line module
_DEFAULT_MAX_LENGTH = 280

def summarize(text: str) -> str:
    normalized = " ".join(text.split())
    return normalized[:_DEFAULT_MAX_LENGTH]

# ... 400 more lines, no other use of _DEFAULT_MAX_LENGTH
```

A future reader sees `_DEFAULT_MAX_LENGTH` at module scope and assumes it's shared. If it isn't, that's noise.

**Correct (trivial constant local to its one caller):**

```python
def summarize(text: str) -> str:
    DEFAULT_MAX_LENGTH = 280
    normalized = " ".join(text.split())
    return normalized[:DEFAULT_MAX_LENGTH]
```

**When to promote to module scope:**

- Reused by more than one function
- Substantial enough to want its own unit tests
- Expensive to rebuild per call (compiled regex, `TypeAdapter`, precomputed table)
- Part of the module's contract (constants referenced by name, e.g., `MyClass.DEFAULT_TIMEOUT`)
- Needs to be patched in tests (module-level constants are easy to monkeypatch)

Prefer module-level over a nested `def` whenever the helper has real logic. Nested functions are appropriate for short closures or very small transforms; they stop being appropriate once the helper grows past a few lines.

**Imports follow the opposite default** (see `imports-top-of-file`): imports live at the top of the module unless there's a specific reason (optional deps, circular, expensive-to-import) to defer them.

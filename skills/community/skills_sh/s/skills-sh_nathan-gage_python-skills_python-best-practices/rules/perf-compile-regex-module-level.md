---
title: Compile Static Regex Patterns at Module Level
impact: LOW
impactDescription: marginal outside tight loops; Python's re cache handles most cases
tags: perf, regex, module-level
references: https://docs.python.org/3/library/re.html#re.compile
---

## Compile Static Regex Patterns at Module Level

Compile static regexes at module scope when the pattern is reused, named, or sits on a measured hot path. Python's `re` module caches recent compiled patterns from the module-level calls (`re.search`, `re.match`, etc.), so a one-shot call outside a hot path is not paying a real recompilation cost. The win from hoisting is mostly readability and naming — and, on genuinely hot paths, bypassing the cache lookup.

**Incorrect (reused pattern buried inline, no name):**

```python
import re

def extract_version(text: str) -> str | None:
    match = re.search(r"v(\d+\.\d+\.\d+)", text)
    return match.group(1) if match else None
```

The pattern is a named concept (`VERSION_RE`) shared across the module but inlined anonymously. If a second function needs the same regex, it gets copied.

**Correct (compiled once at module scope with a descriptive name):**

```python
import re

_VERSION_RE = re.compile(r"v(\d+\.\d+\.\d+)")

def extract_version(text: str) -> str | None:
    match = _VERSION_RE.search(text)
    return match.group(1) if match else None
```

The name documents intent, other call sites reuse the same object, and a tight loop avoids the internal cache lookup.

**Naming:**

- `_UPPER_CASE` for module-level private regex constants (or whatever your project's constant convention is)
- Descriptive names — `_VERSION_RE`, `_EMAIL_RE`, not `_PATTERN1`

**Don't hoist when:**

- The pattern depends on a runtime value (different per call)
- The regex is one-shot startup parsing and an inline call reads more clearly

**Related:** the same "build once, use many" instinct applies to other reusable objects — `TypeAdapter`, `json.JSONDecoder` with custom hooks, precompiled templates.

---
title: Use !r Format for Identifiers in Error Messages
impact: LOW
impactDescription: produces consistent, unambiguous messages
tags: error, formatting, messages, repr
---

## Use `!r` Format for Identifiers in Error Messages

`{name!r}` calls `repr(name)` — producing `'foo'` instead of `foo`, `42` instead of `42`, `None` instead of nothing. Use it for identifiers (names, paths, IDs) in error messages so values are clearly delimited and edge cases (empty strings, whitespace-only names, `None`) render visibly.

**Incorrect (ambiguous formatting):**

```python
raise ValueError(f"Tool {tool_name} not found in registry")
# "Tool  not found in registry" — did tool_name have leading/trailing spaces? was it empty?
# "Tool None not found in registry" — was the literal string "None" or actual None?
```

**Correct (`!r` delimits and disambiguates):**

```python
raise ValueError(f"Tool {tool_name!r} not found in registry")
# "Tool '' not found in registry"      — clearly empty string
# "Tool 'my tool' not found in registry" — spaces visible
# "Tool None not found in registry"    — unambiguously the None sentinel
```

Quotes frame the value. `None`, numbers, and special types render with their `repr` — always unambiguous.

**Apply consistently:**

- **Names, IDs, paths:** `!r`
- **Numeric counts:** plain `{}` (e.g., `f"retrying {count} times"`)
- **Prose:** plain `{}`

```python
raise ValueError(f"tool {name!r} failed after {retries} retries")
raise FileNotFoundError(f"config not found at {path!r}")
raise KeyError(f"unknown key {key!r} in {registry_name!r}")
```

**When backticks are preferable:** some codebases use Markdown-style backticks for user-facing messages (CLI output, log lines humans read). Pick one convention per project and stick to it. `!r` is usually right for Python exception messages; backticks are usually right for log strings rendered in docs or notebooks.

---
title: Inherit New Exceptions from Existing Base Exceptions
impact: MEDIUM
impactDescription: preserves backward compatibility for callers
tags: error, exceptions, inheritance, compatibility
---

## Inherit New Exceptions from Existing Base Exceptions

When adding a new exception type to a module that already has an exception hierarchy, inherit from the relevant base. Callers that catch the base will continue to catch the new type; skipping the base forces every caller to add a new `except` branch.

**Incorrect (new exception inherits from Exception directly):**

```python
class ToolError(Exception): ...
class ToolTimeoutError(ToolError): ...
class ToolValidationError(ToolError): ...

# New failure mode added in v2:
class ToolRateLimitError(Exception):  # doesn't inherit from ToolError
    ...

# Existing caller:
try:
    run_tool(t, args)
except ToolError:  # no longer catches ToolRateLimitError
    retry()
```

The existing `except ToolError:` no longer catches the new error. Every caller must be updated — a silent breaking change.

**Correct (inherit from the existing base):**

```python
class ToolError(Exception): ...
class ToolTimeoutError(ToolError): ...
class ToolValidationError(ToolError): ...
class ToolRateLimitError(ToolError):  # fits the hierarchy
    ...

# Existing caller still works:
try:
    run_tool(t, args)
except ToolError:  # catches ToolRateLimitError too
    retry()
```

Callers that want to handle rate limits specifically can add `except ToolRateLimitError:` — but existing broad handlers keep working.

**Design the hierarchy deliberately:**

```python
class PackageError(Exception): ...            # root for everything the package raises
class UserError(PackageError): ...            # user-correctable
class ConfigError(UserError): ...
class UsageError(UserError): ...
class SystemError(PackageError): ...          # environmental / transient
class NetworkError(SystemError): ...
class TimeoutError(SystemError): ...
```

Callers can catch at whichever level of specificity they need. Adding new subtypes is non-breaking.

**Don't invert the hierarchy:** `class TimeoutError(PackageError)` is fine; `class PackageError(TimeoutError)` is nonsense. The base is the broader category, subclasses are narrower.

**Use `__init_subclass__` or explicit checks** if you need to prevent direct instantiation of the base — keep the type system as the contract enforcement.

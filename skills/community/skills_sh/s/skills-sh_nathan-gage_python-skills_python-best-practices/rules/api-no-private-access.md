---
title: Don't Access Private Attributes
impact: LOW-MEDIUM
impactDescription: internals are free to change without notifying external callers
tags: api, privacy, coupling
---

## Don't Access Private Attributes

`_prefixed` names are the author's contract: "this is internal, it may change." Reaching into another module's or class's private attributes couples your code to implementation details you weren't invited into. Use the public API, or ask the owner to expose what you need.

**Incorrect (poking at private state):**

```python
from some_lib import Client

client = Client()
# peeking at a private attribute because there's no public way
retry_count = client._retry_state["count"]
client._pool.clear()  # mutating private state
```

Next version of `some_lib` renames `_retry_state` to `_retries` (it's private, they're allowed to) — your code breaks with no warning. Or worse, `_pool.clear()` no longer does what you assumed, and you corrupt state silently.

**Correct (use the public API):**

```python
from some_lib import Client

client = Client()
retry_count = client.stats.retries  # public property
client.reset_pool()                  # public method
```

If `some_lib` doesn't expose what you need, open an issue or PR. Using `_private` is a workaround, not a fix.

**Inside your own code:** same rule applies between modules. If `module_a` finds itself reaching into `module_b._helpers`, the helper probably shouldn't be private — or `module_a` shouldn't need it.

**The exception:** testing your own internals. Unit tests for a class may legitimately assert on `_private` state. Even then, prefer testing through the public interface when feasible — tests that poke at internals are brittle to refactoring.

**Double underscore (`__name`) is stronger:** Python name-mangles `__name` to `_ClassName__name`, making accidental access even harder. Use it for attributes you're committed to keeping inaccessible.

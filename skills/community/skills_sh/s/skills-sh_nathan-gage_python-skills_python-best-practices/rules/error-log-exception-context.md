---
title: Preserve Tracebacks When Logging Exceptions
impact: MEDIUM
impactDescription: keeps diagnostics intact when recovering from failures
tags: error, logging, observability
references: https://docs.python.org/3/library/logging.html#logging.Logger.exception
---

## Preserve Tracebacks When Logging Exceptions

When you catch an exception to recover or return a fallback, keep the traceback in the log. `logger.error(str(e))` records the message but loses the stack that explains where the failure came from — which is usually the part that makes the log useful.

**Incorrect (traceback discarded):**

```python
try:
    response = client.fetch(user_id)
except TimeoutError as e:
    logger.error("fetch failed: %s", e)
    return None
```

The log line records "fetch failed: timeout" with no stack — the caller sees a timeout but can't tell which code path produced it.

**Correct (`logger.exception` inside the `except` block):**

```python
try:
    response = client.fetch(user_id)
except TimeoutError:
    logger.exception("fetch failed for user_id=%r", user_id)
    return None
```

`logger.exception(...)` implicitly attaches `exc_info` from the current exception, so the traceback is included at ERROR level. Outside an `except` block — for example, when logging a handled exception from a worker queue — pass `exc_info=True` (or `exc_info=e`) explicitly:

```python
logger.error("task %r failed", task_id, exc_info=exc)
```

**When not to log:**

- You're re-raising (`raise` or `raise NewError(...) from e`) at the same boundary. The outer handler logs once; duplicating here produces two stacks for one failure.
- The exception is expected and recovery is routine (e.g., cache miss). A `logger.debug` or no log at all is often right.

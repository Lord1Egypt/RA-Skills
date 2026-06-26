---
title: Catch Specific Exception Types
impact: HIGH
impactDescription: prevents masked bugs and broken Ctrl-C / cancellation
tags: error, exceptions, asyncio, cancellation
references: https://docs.python.org/3/tutorial/errors.html#handling-exceptions, https://docs.python.org/3/library/exceptions.html#exception-hierarchy, https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.CancelledError, https://peps.python.org/pep-0008/#programming-recommendations
---

## Catch Specific Exception Types

Catch the exception types you intend to handle. A broad `except Exception:` catches every regular error including your own bugs. A bare `except:` or `except BaseException:` is worse — it also catches `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`, which must propagate.

**Incorrect (catches your own bugs):**

```python
def fetch_user(user_id: str) -> User | None:
    try:
        response = http.get(f"/users/{user_id}")
        return parse_user(response.json())
    except Exception:  # swallows KeyError from a typo in parse_user
        return None
```

**Correct (catch what you actually handle):**

```python
def fetch_user(user_id: str) -> User | None:
    try:
        response = http.get(f"/users/{user_id}")
    except (HTTPError, TimeoutError):
        return None
    return parse_user(response.json())  # bugs here propagate
```

Never use bare `except:` or `except BaseException:` — both catch `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`. A broad `except Exception:` is fine at an outer boundary when you log and re-raise:

```python
def handle_request(req: Request) -> Response:
    try:
        return process(req)
    except Exception:
        logger.exception("unhandled error in request handler")
        raise
```

**Cancellation semantics (asyncio / anyio):** On Python 3.8+, `asyncio.CancelledError` inherits from `BaseException`, **not** `Exception`. So `except Exception:` is cancellation-safe — do not flag it as "swallowing cancellation." Only `except BaseException:` (or bare `except:`) catches cancellation. If you do catch `BaseException` or `anyio.get_cancelled_exc_class()`, re-raise. Wrap must-complete cleanup in `asyncio.shield()` — under cancellation, `finally:` blocks race against the cancellation itself.

For meaningful handling, create domain-specific exception types (`ToolTimeoutError(ToolExecutionError)`, etc.) so handlers match on failure mode rather than error text.

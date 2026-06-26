---
title: Use with / async with for Resource Lifetimes
impact: HIGH
impactDescription: deterministic cleanup even on exceptions
tags: error, context-manager, resources, cleanup
references: https://docs.python.org/3/reference/compound_stmts.html#the-with-statement, https://docs.python.org/3/library/contextlib.html, https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with
---

## Use `with` / `async with` for Resource Lifetimes

Any object that owns a finite resource — files, sockets, DB connections, locks, temp dirs, HTTP clients, GPU contexts — should be acquired with `with` (or `async with`). The protocol guarantees `__exit__` runs even when the body raises, so cleanup happens deterministically. Manual `close()` forgets to fire on exceptions, leaks resources under failure, and is easy to misorder during refactors.

**Incorrect (manual close — leaks on exception):**

```python
def write_report(path: Path, rows: list[Row]) -> None:
    f = path.open("w")
    for row in rows:
        f.write(format_row(row))   # if this raises, f is never closed
    f.close()
```

**Correct (`with` — close runs on success, exception, or early return):**

```python
def write_report(path: Path, rows: list[Row]) -> None:
    with path.open("w") as f:
        for row in rows:
            f.write(format_row(row))
```

**Async clients use `async with`:**

```python
async def fetch_user(user_id: str) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return User.model_validate_json(response.content)
```

For multiple resources acquired together, `contextlib.ExitStack` closes all of them in reverse order even if one acquisition raises. Write your own with `@contextlib.contextmanager` (or `@asynccontextmanager`) when a resource isn't already a context manager — `yield` the resource inside a `try` / `finally`.

If you're writing `try` / `finally` to call `close()`, `release()`, or `disconnect()`, you almost certainly want `with` instead.

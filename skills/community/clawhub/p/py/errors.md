# Errors — Raising, Catching, Retrying

The default failure mode is not a crash; it is a swallowed exception that turns a loud bug into a wrong result three layers away.

## Catching

- Catch the narrowest class that you can actually handle. `except Exception` at a boundary (a request handler, a job runner, `main`) is correct; the same line in the middle of business logic is a bug generator.
- `except Exception` does not catch `KeyboardInterrupt`, `SystemExit`, or `GeneratorExit` — those inherit from `BaseException`, deliberately. `except BaseException` is for a top-level "log then re-raise", never for control flow.
- `except Exception: pass` needs one of two things on the same screen: a log line with the exception, or a comment naming why this specific failure is expected and harmless. Anything else is a bug you have promised not to notice.
- Use `try/except/else/finally` to keep the risky call alone: only the call goes in `try`, the success path goes in `else`. Otherwise an exception raised by the success path gets caught by a handler written for the risky one.
- `contextlib.suppress(FileNotFoundError)` is the readable form of "this specific absence is fine".

```python
try:
    resp = client.get(url, timeout=(3.05, 27))
except httpx.TimeoutException as exc:
    raise UpstreamUnavailable(f"{url} timed out") from exc
else:
    return resp.json()      # a JSONDecodeError here is NOT an upstream timeout
finally:
    span.end()
```

## Chaining — Keep The Cause

- `raise New(...) from exc` sets `__cause__`: "The above exception was the direct cause". This is the one you want when translating a low-level error into a domain error.
- A bare `raise New(...)` inside an `except` block sets `__context__` implicitly: "During handling of the above exception, another exception occurred" — which usually means your handler itself has a bug.
- `from None` suppresses the context. Legitimate only when the inner exception is noise (a parser probing formats); it destroys evidence otherwise.
- Re-raising: bare `raise` re-raises the live exception untouched. `raise exc` appends the current line to the traceback and, when `exc` travelled from elsewhere, makes it look like it originated here.
- `exc.add_note(f"while parsing {path}")` (`python >=3.11`) attaches context without wrapping the exception in a new class.

## Designing Exceptions

- One base per package (`class MyLibError(Exception)`), everything else inherits from it. Callers get one line to catch your whole surface without catching the world; you get freedom to add classes later.
- Subclass the stdlib class that matches the semantics (`ValueError` for a bad value, `LookupError`, `TimeoutError`, `OSError`), so code that never heard of your library still handles it sensibly. Inherit from both when it helps: `class ConfigError(MyLibError, ValueError)`.
- Carry data as attributes (`exc.status`, `exc.field`), not by formatting into the message and re-parsing it upstream.
- Message rule: state the expected shape and show the offending value with `!r` — `raise ValueError(f"expected ISO-8601 date, got {value!r}")`. Without `!r`, `None`, `"None"` and `" None "` print identically.
- Do not use exceptions for expected control flow across a hot loop: raising and catching costs roughly a microsecond, which matters only at 10^5+ iterations — but the readability cost is immediate.

## ExceptionGroup (`python >=3.11`)

- `asyncio.TaskGroup` and any code that runs siblings raises `ExceptionGroup`, and a plain `except ValueError` does NOT match a group that contains a ValueError. Existing handlers silently stop catching once code moves to a TaskGroup — one of the sharpest upgrade traps.
- `except*` unpacks it: `except* ValueError as eg:` runs once with all the matching members in `eg.exceptions`, and other members keep propagating.
- `eg.subgroup(...)` / `eg.split(...)` when you need to handle some members and re-raise the rest.

## Timeouts — Every Blocking Call Gets One

- `requests` has NO default timeout: a hung server hangs your process forever. `requests.get(url, timeout=(3.05, 27))` — connect timeout slightly above a multiple of the 3 s TCP retransmit window, read timeout from your own SLA. `httpx` defaults to 5 s; setting it explicitly still beats relying on a library default that changes.
- Sockets, DB drivers, locks, `subprocess.run`, `queue.get` and `asyncio` all take a timeout. The ones you leave off are the frames you will find in the hung-process stack (`debugging.md`).
- A timeout that is longer than the caller's timeout is decorative. Budget downward: gateway 30 s → service 10 s → each upstream 3 s.

## Retrying

Retry only idempotent operations, only on transient classes: connection errors, read timeouts, HTTP 429 and 5xx. Never on 4xx validation errors — the request will be just as invalid the third time, and a retry loop on a POST that already succeeded creates duplicates.

```python
delay = min(cap, base * 2 ** attempt) * random.uniform(0.5, 1.0)   # exponential + jitter
```

- `base` 0.1–1 s, `cap` 30–60 s, 3–5 attempts total. Without the jitter factor, every client that failed at the same instant retries at the same instant.
- Honor `Retry-After` when the server sends it; it beats your backoff formula.
- Cap total elapsed time, not just attempt count. Add up the whole loop, not the backoff: five attempts that each burn the 27 s read timeout above, plus the backoff between them (`base` 1 s doubling under a 60 s cap: 1+2+4+8+16 ≈ 31 s), is a ~166 s stall inside a request that had a 30 s budget. Carry a deadline and stop when it passes.
- Idempotency keys make a non-idempotent operation retryable; that is a protocol decision, not a client one.

## Warnings

- `warnings.warn("x is deprecated", DeprecationWarning, stacklevel=2)` — without `stacklevel=2` the warning points at your own library line instead of the caller's, which makes it unactionable.
- DeprecationWarnings are hidden by default outside `__main__`. Run the test suite with `-W error::DeprecationWarning` before any dependency or interpreter upgrade (`versions.md`).
- A warning that fires on every call in a loop drowns the log; `warnings` deduplicates per location by default — do not defeat that with `simplefilter("always")` in library code.

## Where Errors Go To Die

- Exceptions in a thread never reach the main thread's handler: the default `threading.excepthook` prints to stderr and the thread ends. Wrap the thread body, or use `concurrent.futures` and call `.result()` (`concurrency.md`).
- Exceptions inside `atexit` handlers and `__del__` are printed and swallowed — never rely on them for cleanup that matters.
- An uncaught exception exits with code 1; `SystemExit(n)` exits with `n`; `KeyboardInterrupt` conventionally exits 130 (`cli.md`).
- Log the exception where you HANDLE it, once, with `logger.exception(...)` inside the except block (`logging.md`). Logging and re-raising at every level produces the same stack five times.

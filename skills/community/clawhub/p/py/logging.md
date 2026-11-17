# Logging — Why Nothing Appears, and What To Emit

Two questions answer nearly every logging bug: which logger did the record go to, and which handler was supposed to write it.

## The Setup That Works

```python
# in every module — never at import time do anything else
import logging
log = logging.getLogger(__name__)

# once, in the entry point only
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    force=True,          # python >=3.8: replace handlers something else already installed
)
```

- `getLogger(__name__)` gives you the module path as the logger name, which is what makes per-package level control possible (`logging.getLogger("urllib3").setLevel(logging.WARNING)`).
- Configure in the entry point (`main`, `manage.py`, the worker bootstrap) — never at import time, never in a library.
- A library configures nothing and adds `logging.getLogger("mylib").addHandler(logging.NullHandler())`. Any library that calls `basicConfig` hijacks its host application's logging.

## Nothing Appears — The Four Gates

Check in this order; each is one line:

1. **basicConfig was a no-op.** It does nothing if the root logger already has a handler — and pytest, Django, uvicorn, or a stray `logging.warning()` call all install one. `force=True` (`python >=3.8`) is the fix; before that, `logging.root.handlers.clear()`.
2. **Root level.** The default is WARNING, so `log.info(...)` is dropped before any handler sees it.
3. **Two levels, not one.** The record must pass the LOGGER's level and then the HANDLER's level. A logger at DEBUG feeding a handler at INFO emits nothing at debug.
4. **Propagation.** Records travel up to the root, which owns the handler that actually writes. Someone set `propagate = False` on your logger's parent and the record dies there. The mirror bug: a handler on both the child and the root prints every line twice.

`logging.getLogger("x").getEffectiveLevel()` and walking `.handlers` up the parent chain resolves all four in a REPL.

## What To Write

- Lazy formatting, always: `log.info("user %s exceeded %d", uid, n)`. The f-string version formats even when the level is disabled, and aggregators can no longer group by template — every line becomes a unique string.
- `log.exception("charge failed")` inside an `except` block attaches the traceback. Outside a handler, `log.error("...", exc_info=exc)`. Never `log.error(str(exc))` — that throws away the only part worth reading.
- Levels with a decision rule: DEBUG = for the developer reproducing it; INFO = a business event you would want in an audit ("order 12 shipped"); WARNING = degraded but handled; ERROR = this request/job failed; CRITICAL = the process cannot continue. If nobody would act on it, it is DEBUG.
- Structured context goes in `extra`, not in the message: `log.info("charge ok", extra={"user_id": uid, "amount_cents": n})`. Reserved LogRecord fields (`message`, `asctime`, `name`, `args`, `levelname`, `module`) raise `KeyError` if you reuse them in `extra`.
- Expensive arguments: guard with `if log.isEnabledFor(logging.DEBUG):` before building the payload. That check is the only reason to write an `if` around a log call.

## Configuring Real Applications

`dictConfig` is the maintainable form — one dict, versionable, no import-order surprises:

```python
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,   # the default True silences every logger imported before this line
    "formatters": {"plain": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
    "handlers": {"stdout": {"class": "logging.StreamHandler", "formatter": "plain"}},
    "root": {"handlers": ["stdout"], "level": "INFO"},
    "loggers": {"urllib3": {"level": "WARNING"}},
})
```

`disable_existing_loggers` defaults to True and is the top cause of "our library logs vanished after we added a config file".

## Files, Rotation, and Multiple Processes

- Log to stdout and let the supervisor (systemd, Docker, the platform) capture and rotate. That is the only design that survives multiple worker processes.
- `RotatingFileHandler` is NOT multi-process safe: two workers rotate the same file and truncate each other's records. Under gunicorn/uvicorn workers, use stdout, a `SocketHandler` to one collector, or `concurrent-log-handler`.
- Timestamps in UTC: `logging.Formatter.converter = time.gmtime`, or emit ISO-8601 with an offset. Local time in logs costs an hour of confusion twice a year (`datetime.md`).
- Logging is synchronous: a slow handler (network, disk under pressure) blocks the thread that logged. For request paths, `QueueHandler` + `QueueListener` move the write to a background thread.

## Secrets and Volume

- Never log tokens, passwords, cookies, full card numbers, or the `repr` of a request/config object that contains them — `repr` is where credentials leak. Add a `logging.Filter` that redacts known key names before records reach a handler.
- Logging inside a tight loop is a performance bug and a storage bill; log once with a count, or sample.
- Exception objects can hold large payloads; `log.exception` renders them. Truncate deliberately at the boundary.

## Correlation and Tests

- One id per request/job, attached to every line: store it in a `contextvars.ContextVar` and inject it with a `Filter`. `threading.local` does not follow `await`, so under asyncio it silently mixes ids between tasks.
- Testing what you log: pytest's `caplog` fixture (`caplog.set_level`, then assert on `caplog.records`, not on the formatted text) or `unittest`'s `assertLogs`. Asserting on a specific formatted string couples every test to the format string.
- Prefer asserting on the structured fields you promised (`record.user_id`) — that is the contract your dashboards depend on.

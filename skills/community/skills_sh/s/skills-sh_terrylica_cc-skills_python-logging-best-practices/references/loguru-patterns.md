# Loguru Configuration Patterns

## Basic Setup

```python
from loguru import logger
import sys

# Remove default handler
logger.remove()

# Add custom handlers
logger.add(sys.stderr, level="INFO")
logger.add("app.log", rotation="10 MB")
```

## JSONL Output Pattern

```python
import orjson

def json_formatter(record) -> str:
    """JSONL formatter — orjson is 2-10x faster than stdlib json."""
    return orjson.dumps({
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "level": record["level"].name.lower(),
        "message": record["message"],
        "extra": record["extra"]
    }).decode()

logger.add(sys.stderr, format=json_formatter)
```

> **Why orjson?** Native datetime/UUID/dataclass serialization, RFC 8259 compliant, 2-10x faster than `json.dumps()`. Use `orjson.dumps().decode()` since orjson returns bytes.

## Structured Logging

```python
# Add context to log messages
logger.info(
    "User logged in",
    operation="login",
    status="success",
    user_id=123,
    metrics={"duration_ms": 50}
)
```

## Rotation Options

```python
# Size-based rotation
logger.add("app.log", rotation="10 MB")

# Time-based rotation
logger.add("app.log", rotation="1 day")
logger.add("app.log", rotation="1 week")
logger.add("app.log", rotation="00:00")  # Midnight

# Count-based rotation
logger.add("app.log", rotation="100 records")
```

## Retention Options

```python
# Time-based retention
logger.add("app.log", retention="7 days")
logger.add("app.log", retention="1 month")

# Count-based retention
logger.add("app.log", retention=5)  # Keep 5 old files
```

## Compression

```python
# gzip compression (recommended)
logger.add("app.log", compression="gz")

# Other formats
logger.add("app.log", compression="bz2")
logger.add("app.log", compression="xz")
logger.add("app.log", compression="zip")
```

## Exception Handling

```python
# Log exceptions with traceback
try:
    raise ValueError("Something went wrong")
except ValueError:
    logger.exception("Error occurred")

# Or use opt() for more control
logger.opt(exception=True).error("Error with traceback")
```

## Async Support & enqueue

```python
# For async/multiprocess applications — use enqueue
logger.add("app.log", enqueue=True)
```

<!-- SSoT-OK: loguru version referenced for issue context, not as a dependency pin -->

> **WARNING — Unbounded memory risk**: `enqueue=True` uses an internal `multiprocessing.SimpleQueue` with **no max size**. If the sink is slow (disk I/O, network), the queue grows unbounded until OOM. See [loguru#1419](https://github.com/Delgan/loguru/issues/1419). No upstream fix merged yet.
>
> **Mitigations**:
>
> - Monitor RSS in production when using `enqueue=True`
> - Avoid slow sinks (network loggers, remote databases) with enqueue
> - For high-throughput async services, consider **structlog** with ContextVars instead
> - For simple CLI scripts, `enqueue=False` (default) is fine

### Shutdown — logger.complete()

When using `enqueue=True`, **always flush before exit** to prevent silent log loss:

```python
import asyncio
from loguru import logger

async def main():
    logger.add("app.jsonl", enqueue=True)
    # ... application logic ...
    await logger.complete()  # Flush all enqueued messages before exit

asyncio.run(main())
```

Synchronous alternative — `logger.remove()` implicitly flushes and closes all sinks:

```python
def main():
    logger.add("app.jsonl", enqueue=True)
    try:
        # ... application logic ...
        pass
    finally:
        logger.remove()  # Flushes enqueued messages + closes sinks
```

## Security — Redaction Filters

Scrub secrets at the filter level so they never reach any sink:

```python
import re

REDACT_PATTERNS = [
    (re.compile(r'AKIA[0-9A-Z]{16}'), '[REDACTED_AWS_KEY]'),
    (re.compile(r'sk-[a-zA-Z0-9]{48}'), '[REDACTED_API_KEY]'),
    (re.compile(r'(?i)bearer\s+[a-zA-Z0-9._~+/=-]+'), '[REDACTED_BEARER]'),
    (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'), '[REDACTED_EMAIL]'),
]

def redact_filter(record):
    """Scrub secrets from messages before they reach any sink."""
    for pattern, replacement in REDACT_PATTERNS:
        record["message"] = pattern.sub(replacement, record["message"])
    return True

# Apply to ALL sinks
logger.add("app.jsonl", filter=redact_filter)
logger.add(sys.stderr, filter=redact_filter)
```

**Best practice**: Don't log PII at all. Store PII in a vault, log tokens/hashes. Redaction filters are a safety net, not primary defense.

## Filtering

```python
# Filter by level
logger.add("errors.log", level="ERROR")

# Filter by function
def my_filter(record):
    return "sensitive" not in record["message"]

logger.add("filtered.log", filter=my_filter)
```

## Best Practices

1. **Always `logger.remove()`** first - Removes default handler
2. **Use rotation** - Prevent unbounded growth (local/CLI apps only)
3. **Use retention** - Clean up old logs
4. **Use compression** - Save disk space
5. **Use structured extras** - Add context via kwargs
6. **Use `redact_filter`** - Scrub secrets from all sinks
7. **Call `logger.complete()`** - Flush enqueued messages before shutdown
8. **Monitor RSS with `enqueue=True`** - Unbounded queue risk with slow sinks
9. **Use orjson** - 2-10x faster JSONL serialization

# Python Logging Architecture Guide

## When to Use Which Approach

| Approach    | Use Case                              | Pros                                          | Cons                                     |
| ----------- | ------------------------------------- | --------------------------------------------- | ---------------------------------------- |
| `loguru`    | CLI tools, scripts, local services    | Zero-config, built-in rotation, great DX      | External dep, not schema-enforced        |
| `structlog` | Production services, OTel integration | ContextVars, processor chains, OTel-native    | Steeper learning curve                   |
| `stdlib`    | LaunchAgent daemons, zero-dep         | No dependencies, 3.14 `merge_extra`           | More boilerplate, no structured defaults |
| `Logfire`   | AI/LLM observability, Pydantic apps   | Built on OTel, token/cost tracking, SQL       | SaaS dependency, newer ecosystem         |
| `Kern`      | Enterprise with compliance needs      | Strict JSON schema, crypto integrity, no deps | Newer, smaller community                 |
| `Rich`      | Rich terminal apps                    | Beautiful output, syntax-highlighted traces   | Display only, not for structured logging |

## Decision Tree

```
Need logging?
├── Container or serverless?
│   └── YES → stdout/stderr as JSON (any library)
│       └── NO file rotation — let infrastructure handle it
├── Production service with tracing?
│   └── YES → structlog + OpenTelemetry
│       └── OTel auto-injects trace_id/span_id
├── AI/LLM app with Pydantic?
│   └── YES → Pydantic Logfire (built on OTel)
│       └── Token tracking, cost monitoring, SQL on logs
├── Stdlib-only required?
│   └── YES → RotatingFileHandler
│       └── Python 3.14: LoggerAdapter.merge_extra=True
├── Rich terminal output needed?
│   └── YES → Rich + RichHandler
│       └── Combine with structured file logging
└── CLI tool or script?
    └── YES → loguru + orjson
        └── This skill's recommended pattern
```

## Container vs Local Logging

| Aspect        | Local / CLI                            | Container / Serverless                    |
| ------------- | -------------------------------------- | ----------------------------------------- |
| Output        | File + stderr                          | stdout/stderr only                        |
| Format        | JSONL to file, human-readable console  | JSONL to stdout                           |
| Rotation      | loguru rotation or RotatingFileHandler | None — Docker/k8s log driver handles it   |
| Collection    | Read files directly, `jq` parsing      | fluentbit/fluentd sidecar, OTel Collector |
| Log directory | App-specific path                      | N/A                                       |
| Correlation   | UUID4 trace_id (local tools)           | OTel trace_id + span_id (propagated)      |

## Approach Details

### 1. Loguru (Recommended for CLI/Scripts)

**Best for**: Modern Python scripts, CLI tools, local automation

```python
from loguru import logger
from pathlib import Path

log_dir = Path.home() / ".local" / "log" / "my-app"
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    str(log_dir / "app.jsonl"),
    rotation="10 MB",
    retention="7 days",
    compression="gz"
)
```

**Advantages**:

- Zero configuration to start
- Built-in rotation, retention, compression
- Structured logging with `extra` kwargs
- Exception formatting included

**Caveats**:

- `enqueue=True` has unbounded queue — OOM risk with slow sinks ([loguru#1419](https://github.com/Delgan/loguru/issues/1419))
- Always call `logger.complete()` or `logger.remove()` before shutdown

### 2. structlog (Recommended for Production Services)

**Best for**: Services with OpenTelemetry, async apps, production backends

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,        # Async-safe context
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),            # JSONL output
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO+
)

log = structlog.get_logger()
log.info("request_handled", method="GET", path="/api/health", duration_ms=12)
```

**Advantages**:

- ContextVars for async-safe per-request context (5x throughput vs stdlib in async apps)
- Processor chains for transforming log records
- Native OTel integration via processors
- Exception group support (Python 3.11+)

**ContextVar reset pattern** (critical for async services):

```python
# At request boundary — prevents memory leaks in long-running async services
structlog.contextvars.clear_contextvars()
structlog.contextvars.bind_contextvars(request_id="abc-123")
```

### 3. RotatingFileHandler (Stdlib)

**Best for**: LaunchAgent services, stdlib-only requirements

```python
from logging.handlers import RotatingFileHandler
import logging

handler = RotatingFileHandler(
    "/path/to/app.log",
    maxBytes=100 * 1024 * 1024,  # 100MB
    backupCount=5
)
logging.getLogger().addHandler(handler)
```

**Python 3.14 addition**: `LoggerAdapter` gained `merge_extra=True` — call-level extras merge with adapter extras instead of replacing them:

```python
adapter = logging.LoggerAdapter(logger, {"app": "my-app"}, merge_extra=True)
adapter.info("event", extra={"request_id": "abc"})
# Both app="my-app" and request_id="abc" are present
```

**Reference**: [Python RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)

### 4. Pydantic Logfire (AI/LLM Observability)

**Best for**: AI/LLM applications, Pydantic-heavy services

- Built on OpenTelemetry — auto-exports to any OTel backend
- Purpose-built LLM features: conversation panels, token tracking, cost monitoring
- SQL queries on your logs
- 10M free spans/month

**Reference**: [Pydantic Logfire](https://pydantic.dev/logfire)

### 5. Rich Integration (Terminal Display)

**Best for**: Applications with rich terminal UI

```python
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
```

> Combine with a structured file handler for machine-readable output alongside pretty terminal display.

## Output Format Recommendations

| Output Type      | Format                                     | Extension |
| ---------------- | ------------------------------------------ | --------- |
| Machine analysis | JSONL                                      | `.jsonl`  |
| Human reading    | Plain text                                 | `.log`    |
| Both             | JSONL (parseable by jq AND human readable) | `.jsonl`  |

## Common Patterns

### Dual Output (Console + File)

```python
from loguru import logger
import sys

# Human-readable to console
logger.add(sys.stderr, level="INFO")

# Machine-readable to file
logger.add("app.jsonl", format=json_formatter, level="DEBUG")
```

### Environment-Based Configuration

```python
import os

log_level = os.getenv("LOG_LEVEL", "INFO")
logger.add(sys.stderr, level=log_level)
```

## Related Resources

- [loguru-patterns.md](./loguru-patterns.md) - Loguru configuration
- [migration-guide.md](./migration-guide.md) - From print() to logging
- [structlog docs](https://www.structlog.org/) - Structured logging for production
- [Pydantic Logfire](https://pydantic.dev/logfire) - AI/LLM observability
- [OpenTelemetry Python Logging](https://opentelemetry.io/docs/zero-code/python/logs-example/) - OTel auto-instrumentation

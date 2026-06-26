---
name: python-logging-best-practices
description: Python logging with loguru, structlog, and orjson. TRIGGERS - loguru, structlog, structured logging
allowed-tools: Read, Bash, Grep, Edit, Write
---

# Python Logging Best Practices

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Setting up Python logging for any service or script
- Configuring structured JSONL logging for analysis
- Implementing log rotation
- Choosing between lightweight (zero-dep) and full-featured logging
- Adding logging to containerized, systemd, or local applications

## Overview

Unified reference for Python logging patterns optimized for machine readability (Claude Code analysis) and operational reliability. **Starts with the lightest viable approach and scales up only when needed.**

## Decision Heuristic: Start Light, Scale Up

```
Is it < 5 services on a single machine, < 1 event/sec?
  YES → Lightweight Pattern (print + JSONL telemetry)
  NO  → Is it containerized / serverless?
    YES → stdout JSON (any library), no file rotation
    NO  → Is OTel tracing required?
      YES → structlog + OTel
      NO  → loguru (CLI tools) or stdlib RotatingFileHandler
```

| Approach        | Use Case                                             | Pros                                          | Cons                                         |
| --------------- | ---------------------------------------------------- | --------------------------------------------- | -------------------------------------------- |
| **Lightweight** | Small systemd services, self-hosted, single operator | Zero deps, journald integration, minimal code | No severity filtering, no per-module control |
| `loguru`        | CLI tools, scripts, local services                   | Zero-config, built-in rotation, great DX      | External dep, not truly schema-enforced      |
| `structlog`     | Production services, OTel integration                | ContextVars, processor chains, OTel-native    | Steeper learning curve                       |
| `stdlib`        | LaunchAgent daemons, zero-dep constraint             | No dependencies, Python 3.14 `merge_extra`    | More boilerplate, no structured defaults     |
| `Logfire`       | AI/LLM observability, Pydantic apps                  | Built on OTel, token/cost tracking, SQL       | SaaS dependency, newer ecosystem             |

---

## Preferred: Lightweight Pattern (Zero Dependencies)

**For: < 5 systemd services, single server, single operator. Battle-tested in production by [ccmax-monitor](https://github.com/terrylica/ccmax-monitor).**

This pattern uses a **two-channel architecture**:

- **Channel 1**: `print(flush=True)` → systemd journald (operational logs, human-readable)
- **Channel 2**: Append-only JSONL file (structured telemetry, machine-readable)

This maps to the 12-Factor App's "treat logs as event streams" principle. journald handles ops (rotation, filtering, metadata), while the JSONL file serves domain telemetry for post-mortem analysis.

### Architecture: Three-Concern Separation

| Concern            | Mechanism                      | Purpose                                     | Lifecycle                          |
| ------------------ | ------------------------------ | ------------------------------------------- | ---------------------------------- |
| **Ops logging**    | `print()` → journald           | Human debugging, `journalctl -u service -f` | Managed by journald (auto-rotated) |
| **Telemetry**      | JSONL file (`telemetry.jsonl`) | Structured audit trail, AI/LLM analysis     | Append-only, rotated by size       |
| **State recovery** | WAL file (optional)            | Crash recovery for irreversible operations  | Ephemeral, deleted on success      |

### Complete Lightweight Example

```python
"""Append-only JSONL telemetry logger with size-based rotation.

Zero external dependencies. Works with systemd journald for ops logging
and a separate JSONL file for structured machine-readable telemetry.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

TELEMETRY_PATH = Path(__file__).parent / "telemetry.jsonl"
MAX_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 3             # Keep 3 rotated backups (~30MB total)


def log_event(event_type: str, data: dict) -> None:
    """Append a structured JSON line to telemetry.jsonl."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        **data,
    }
    line = json.dumps(entry, separators=(",", ":")) + "\n"

    try:
        try:
            if TELEMETRY_PATH.stat().st_size > MAX_SIZE:
                _rotate()
        except FileNotFoundError:
            pass

        with open(TELEMETRY_PATH, "a") as f:
            f.write(line)
    except OSError as e:
        # Fallback to stderr (captured by journald)
        print(f"[telemetry] write failed: {e}", file=__import__("sys").stderr, flush=True)


def _rotate() -> None:
    """Rotate telemetry files: .jsonl → .jsonl.1 → .jsonl.2 → .jsonl.3"""
    for i in range(BACKUP_COUNT, 1, -1):
        src = TELEMETRY_PATH.with_suffix(f".jsonl.{i - 1}")
        dst = TELEMETRY_PATH.with_suffix(f".jsonl.{i}")
        if src.exists():
            dst.unlink(missing_ok=True)
            src.rename(dst)
    backup = TELEMETRY_PATH.with_suffix(".jsonl.1")
    backup.unlink(missing_ok=True)
    TELEMETRY_PATH.rename(backup)


# === Ops logging (goes to journald via stdout) ===

def log(msg: str) -> None:
    """Human-readable operational log line. Captured by journald."""
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)
```

**Usage:**

```python
# Operational (human reads via journalctl -u myservice -f)
log("Refreshing token for account X")
log("Switch: account A → account B (reason: 5h breach)")

# Telemetry (machine reads via jq/DuckDB/Claude Code)
log_event("token_refresh", {"account": "X", "expires_in_h": 8.0, "token_fp": "abc12345"})
log_event("account_switch", {"from": "A", "to": "B", "reason": "5h_breach"})
```

### Security: Token Fingerprinting (Not Regex Redaction)

**Never pass secrets through the logging pipeline.** Log only a non-reversible fragment:

```python
def _token_fingerprint(token: str) -> str:
    """Extract uniquely identifiable chars from a token's mid-section.

    The prefix (sk-ant-oat01-) and suffix (...AA) are common across tokens.
    Chars 14-22 (after the prefix) are the most unique per-token.
    Middle-slice avoids leaking type-prefix metadata that prefix-based
    approaches expose.
    """
    if len(token) > 25:
        return token[14:22]
    return token[:8] if token else ""

# Usage: log the fingerprint, never the token
log_event("token_refresh", {"account": name, "token_fp": _token_fingerprint(token)})
```

**Why this is superior to regex redaction filters:**

| Approach                                    | Security                                  | Maintenance                               | Failure mode                    |
| ------------------------------------------- | ----------------------------------------- | ----------------------------------------- | ------------------------------- |
| **Token fingerprinting** (log only a slice) | Secret never enters logging pipeline      | Zero — works with any token format        | Cannot fail — nothing to redact |
| Regex redaction filter                      | Secret passes through, filtered on output | Must update regexes for new token formats | Silent miss = secret in logs    |

This aligns with OWASP Logging Cheat Sheet: "Ensure that no sensitive data is included in log entries." Major platforms (AWS, Stripe, GitHub) use separate non-secret identifiers or partial token display — never full tokens with regex scrubbing.

Regex filters remain useful as a **defense-in-depth backstop**, not a primary control.

### Health Endpoints as Observability

For small deployments, **rich JSON health endpoints replace log aggregation**:

```python
@app.get("/api/status")
def status():
    """White-box monitoring — current state on demand."""
    return {"active_account": ..., "accounts": [...], "polled_at": ...}

@app.get("/api/vault-health")
def vault_health():
    """Token health for all accounts."""
    return {name: {"status": "healthy", "expires_in": "7.5h", ...} for ...}
```

This is the **Health Endpoint Monitoring Pattern** (Microsoft Azure Architecture Center) / **Health Check API Pattern** (microservices.io). The dashboard IS the monitoring tool — no Grafana/Prometheus needed.

When the service itself serves its own operational state as structured JSON, you get:

- **Real-time** current state (not delayed by log ingestion pipelines)
- **Zero infrastructure** (no log shipper, storage, or query engine)
- **AI-parseable** (Claude Code can `curl` and analyze directly)

### Post-Mortem with FOSS CLI Tools

No log aggregation stack needed. These single-binary tools work directly on JSONL:

```bash
# DuckDB — SQL analytics on JSONL (most powerful)
duckdb -c "SELECT type, count(*) FROM read_json_auto('telemetry.jsonl') GROUP BY 1 ORDER BY 2 DESC"

# jq — ad-hoc JSON filtering
jq 'select(.type == "token_refresh")' telemetry.jsonl

# journalctl — already exports JSONL natively
journalctl -u ccmax-switcher -o json --since "1h ago" | jq 'select(.PRIORITY == "3")'

# lnav — interactive terminal log viewer with SQL
lnav telemetry.jsonl

# llm (Simon Willison) — pipe to LLM for AI post-mortem
journalctl -u myservice --since "2h ago" --priority=err -o json | llm "analyze root cause"
```

### When to Upgrade Beyond Lightweight

Upgrade to loguru/structlog when any of these become true:

- **> 5 services** across multiple hosts (need trace IDs for correlation)
- **> 10 events/sec** sustained (need async sinks, `orjson`)
- **Multiple operators** who need per-module log level filtering
- **Compliance requirements** that mandate structured audit trails with signatures
- **Container/K8s deployment** (stdout JSON is the standard)

---

## Full-Featured: Loguru + JSONL Pattern

For CLI tools, scripts, and services that benefit from a logging library:

### Log Rotation (ALWAYS CONFIGURE for local/CLI apps)

```python
from loguru import logger

logger.add(
    log_path,
    rotation="10 MB",
    retention="7 days",
    compression="gz"
)

# stdlib alternative (zero-dep)
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    log_path,
    maxBytes=100 * 1024 * 1024,  # 100MB
    backupCount=5
)
```

> **Container/serverless apps**: Skip file rotation entirely. Log to **stdout/stderr as JSON**. Let the container runtime handle collection and rotation.

### JSONL Format (Machine-Readable)

```python
# One JSON object per line - jq-parseable
{"timestamp": "2026-01-14T12:45:23.456Z", "level": "info", "message": "..."}
```

**File extension**: Always use `.jsonl` (not `.json` or `.log`)

**Performance**: For >10k records/sec, use `orjson` instead of `json.dumps()`:

```python
import orjson

def json_formatter(record) -> str:
    log_entry = { ... }
    return orjson.dumps(log_entry).decode()
```

### Regex Redaction (Defense-in-Depth)

Use as a **backstop** alongside token fingerprinting, not as the primary control:

```python
import re

REDACT_PATTERNS = [
    (re.compile(r'AKIA[0-9A-Z]{16}'), '[REDACTED_AWS_KEY]'),
    (re.compile(r'sk-[a-zA-Z0-9]{48}'), '[REDACTED_API_KEY]'),
    (re.compile(r'(?i)bearer\s+[a-zA-Z0-9._~+/=-]+'), '[REDACTED_BEARER]'),
]

def redact_filter(record):
    for pattern, replacement in REDACT_PATTERNS:
        record["message"] = pattern.sub(replacement, record["message"])
    return True

logger.add(sink, filter=redact_filter)
```

### Shutdown — Always Flush Enqueued Messages

```python
import asyncio
from loguru import logger

async def main():
    logger.add("app.jsonl", enqueue=True)
    await logger.complete()

asyncio.run(main())
# Sync: logger.remove()
```

### Complete Loguru + JSONL Example

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.14"
# dependencies = ["loguru", "orjson"]
# ///

import re
import sys
from pathlib import Path
from uuid import uuid4

import orjson
from loguru import logger

REDACT_PATTERNS = [
    (re.compile(r'AKIA[0-9A-Z]{16}'), '[REDACTED_AWS_KEY]'),
    (re.compile(r'sk-[a-zA-Z0-9]{48}'), '[REDACTED_API_KEY]'),
]


def json_formatter(record) -> str:
    log_entry = {
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "level": record["level"].name.lower(),
        "component": record["function"],
        "operation": record["extra"].get("operation", "unknown"),
        "operation_status": record["extra"].get("status", None),
        "trace_id": record["extra"].get("trace_id"),
        "message": record["message"],
        "context": {k: v for k, v in record["extra"].items()
                   if k not in ("operation", "status", "trace_id", "metrics")},
        "metrics": record["extra"].get("metrics", {}),
        "error": None
    }

    if record["exception"]:
        exc_type, exc_value, _ = record["exception"]
        log_entry["error"] = {
            "type": exc_type.__name__ if exc_type else "Unknown",
            "message": str(exc_value) if exc_value else "Unknown error",
        }

    return orjson.dumps(log_entry).decode()


def redact_filter(record):
    for pattern, replacement in REDACT_PATTERNS:
        record["message"] = pattern.sub(replacement, record["message"])
    return True


def setup_logger(app_name: str, log_dir: Path | None = None):
    logger.remove()
    logger.add(sys.stderr, format=json_formatter, filter=redact_filter, level="INFO")
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_dir / f"{app_name}.jsonl"),
            format=json_formatter,
            filter=redact_filter,
            rotation="10 MB",
            retention="7 days",
            compression="gz",
            level="DEBUG"
        )
    return logger
```

## Semantic Fields Reference

| Field               | Type          | Purpose                                                |
| ------------------- | ------------- | ------------------------------------------------------ |
| `timestamp` / `ts`  | ISO 8601      | Event ordering (millisecond precision minimum)         |
| `level` / `type`    | string        | Severity or event type                                 |
| `component` / `svc` | string        | Module, function, or service name                      |
| `operation`         | string        | What action is being performed                         |
| `operation_status`  | string        | started/success/failed/skipped                         |
| `trace_id`          | UUID4 or OTel | Correlation ID (OTel trace ID for production services) |
| `message`           | string        | Human-readable description                             |
| `context`           | object        | Operation-specific metadata                            |
| `metrics`           | object        | Quantitative data (counts, durations)                  |
| `error`             | object/null   | Exception details if failed                            |

## Related Resources

- [Health Endpoint Monitoring Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring) - Microsoft Azure Architecture Center
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) - Security best practices
- [Write-Ahead Log pattern](https://martinfowler.com/articles/patterns-of-distributed-systems/write-ahead-log.html) - Martin Fowler
- [DuckDB JSON support](https://duckdb.org/docs/data/json/overview) - SQL analytics on JSONL
- [lnav](https://lnav.org/) - Terminal log file navigator with SQL
- [llm CLI](https://github.com/simonw/llm) - Pipe logs to LLMs for analysis
- [structlog docs](https://www.structlog.org/) - Structured logging for production services
- [Pydantic Logfire](https://pydantic.dev/logfire) - AI/LLM observability built on OTel
- [Langfuse](https://langfuse.com/) - Open-source LLM observability (self-hostable)

## Anti-Patterns to Avoid

1. **Unbounded logs** - Always configure rotation (local) or stdout (container)
2. **Logging full secrets** - Use token fingerprinting; regex redaction is a backstop, not primary
3. **Adding loguru/structlog to < 5 low-volume services** - print + JSONL is sufficient; dependency is not free
4. **Bare except without logging** - Catch specific exceptions, log them
5. **Silent failures** - Log errors before suppressing
6. **`enqueue=True` without `logger.complete()`** - Silent log loss on shutdown
7. **`enqueue=True` with slow sinks** - Unbounded memory growth
8. **`json.dumps()` at >10k events/sec** - Use orjson for 2-10x speedup
9. **UUID4 trace IDs in OTel services** - Use OTel-propagated trace IDs
10. **Prometheus/Grafana for < 5 services** - Health endpoints + Uptime Kuma is sufficient
11. **Conflating WAL and telemetry** - WAL is for crash recovery (ephemeral), telemetry is for audit (permanent)

---

## Troubleshooting

| Issue                         | Cause                            | Solution                                             |
| ----------------------------- | -------------------------------- | ---------------------------------------------------- |
| loguru not found              | Not installed                    | Run `uv add loguru`                                  |
| Logs not appearing            | Wrong log level                  | Set level to DEBUG for troubleshooting               |
| Log rotation not working      | Missing rotation config          | Add rotation param to logger.add()                   |
| JSONL parse errors            | Malformed log line               | Check for unescaped special characters               |
| OOM with enqueue=True         | Unbounded internal queue         | Monitor RSS; use structlog or avoid slow sinks       |
| Lost logs on shutdown         | Missing logger.complete()        | Call `await logger.complete()` or `logger.remove()`  |
| Slow JSONL serialization      | Using stdlib json at high volume | Switch to `orjson.dumps().decode()`                  |
| Secrets in logs               | No fingerprinting                | Log token slices, not full values                    |
| journald not capturing output | Missing flush                    | Use `print(..., flush=True)` or `PYTHONUNBUFFERED=1` |
| No alerts when services crash | No external monitor              | Add Uptime Kuma or Gatus polling health endpoints    |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.

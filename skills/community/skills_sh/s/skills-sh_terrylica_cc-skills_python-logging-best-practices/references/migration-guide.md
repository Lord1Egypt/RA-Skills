# Migration Guide: print() to Structured Logging

## Overview

This guide covers migrating from `print()` statements to structured JSONL logging using loguru.

## Quick Migration Table

| Before (print)                   | After (loguru)                                                |
| -------------------------------- | ------------------------------------------------------------- |
| `print("Starting...")`           | `logger.info("Starting", operation="main", status="started")` |
| `print(f"[DEBUG] {var}")`        | `logger.debug("Variable state", var=var)`                     |
| `print(f"[ERROR] {e}")`          | `logger.error("Operation failed", error=str(e))`              |
| `print(f"Processing {n} items")` | `logger.info("Processing items", metrics={"count": n})`       |

## Step-by-Step Migration

### Step 1: Add Dependencies

```python
# PEP 723 inline script metadata
# /// script
# requires-python = ">=3.14"
# dependencies = ["loguru", "orjson"]
# ///
```

Or via pyproject.toml:

```bash
uv add loguru orjson
```

### Step 2: Add Logger Setup

```python
import sys
from pathlib import Path
from loguru import logger
import orjson


def json_formatter(record) -> str:
    """JSONL formatter for machine-readable output."""
    return orjson.dumps({
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "level": record["level"].name.lower(),
        "message": record["message"],
        "extra": record["extra"]
    }).decode()


def setup_logger(app_name: str, log_dir: Path | None = None):
    logger.remove()

    # Console output
    logger.add(sys.stderr, format=json_formatter, level="INFO")

    # File output with rotation (if log_dir provided)
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_dir / f"{app_name}.jsonl"),
            format=json_formatter,
            rotation="10 MB",
            retention="7 days",
            compression="gz"
        )
```

### Step 3: Call Setup Early

```python
# At module level or in main()
setup_logger("my-app", log_dir=Path.home() / ".local" / "log" / "my-app")
```

### Step 4: Replace Print Statements

**Pattern 1: Simple status messages**

```python
# Before
print("Starting application...")
print("Application ready")

# After
logger.info("Application starting", operation="startup", status="started")
logger.info("Application ready", operation="startup", status="success")
```

**Pattern 2: Variable debugging**

```python
# Before
print(f"[DEBUG] config = {config}")
print(f"[DEBUG] count = {len(items)}")

# After
logger.debug("Configuration loaded", config=config)
logger.debug("Items counted", metrics={"count": len(items)})
```

**Pattern 3: Error reporting**

```python
# Before
try:
    do_something()
except Exception as e:
    print(f"[ERROR] Failed: {e}")

# After
try:
    do_something()
except ValueError as e:
    logger.error("Operation failed", operation="do_something", status="failed", error=str(e))
```

**Pattern 4: Progress updates**

```python
# Before
for i, item in enumerate(items):
    print(f"Processing {i+1}/{len(items)}")

# After
total = len(items)
for i, item in enumerate(items):
    if i % 100 == 0:  # Log every 100 items
        logger.info("Processing progress", metrics={"current": i+1, "total": total})
```

### Step 5: Remove Redundant Prints

After adding logger calls, remove the original print statements.

## Common Anti-Patterns to Fix

### Anti-Pattern 1: Silent Exception Handling

```python
# BAD - Silent failure
try:
    result = parse_config(path)
except Exception:
    result = default_config  # No one knows this happened

# GOOD - Loud failure
try:
    result = parse_config(path)
except FileNotFoundError as e:
    logger.warning("Config not found, using defaults", path=str(path), error=str(e))
    result = default_config
except ValueError as e:
    logger.error("Config parse failed", path=str(path), error=str(e))
    raise
```

### Anti-Pattern 2: Bare Except

```python
# BAD
except:
    pass

# GOOD
except SpecificException as e:
    logger.error("Specific error occurred", error=str(e))
```

### Anti-Pattern 3: Print to stdout

```python
# BAD - Mixed with program output
print("Processing...")  # Goes to stdout

# GOOD - Logs to stderr
logger.info("Processing...")  # Goes to stderr, stdout clean for data
```

## Verification

After migration, validate JSONL output:

```bash
# Run script and pipe stderr to file
python script.py 2> output.jsonl

# Validate JSON
cat output.jsonl | jq -c .

# Search logs
cat output.jsonl | jq 'select(.level == "error")'
```

## Rollback

If issues arise, keep both temporarily:

```python
# Parallel logging during migration
print(f"[INFO] {message}")  # Keep for now
logger.info(message)         # New structured log
```

Remove print statements once confident in new logging.

---
title: Consolidate try/except Blocks with the Same Handler
impact: LOW-MEDIUM
impactDescription: reduces duplication and simplifies control flow
tags: error, exceptions, duplication
---

## Consolidate `try/except` Blocks with the Same Handler

When multiple adjacent operations raise the same exception and need the same handling, merge them into one block. Separate blocks duplicate the handler — and if the handling logic ever changes, you now need to update N places.

**Incorrect (three blocks, three copies of the same handler):**

```python
def load_config(path: Path) -> Config | None:
    try:
        raw = path.read_text()
    except FileNotFoundError:
        logger.warning("config missing: %s", path)
        return None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("config invalid json: %s", path)
        return None

    try:
        return Config(**data)
    except ValidationError:
        logger.warning("config validation failed: %s", path)
        return None
```

Three copies of "log and return None." Changing the log level, adding a metric, or switching return value means editing three places.

**Correct (one block, one handler):**

```python
def load_config(path: Path) -> Config | None:
    try:
        raw = path.read_text()
        data = json.loads(raw)
        return Config(**data)
    except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
        logger.warning("config load failed: %s (%s)", path, e)
        return None
```

One block, one handler, one place to change. The caller sees the same behavior; the implementation is simpler.

**When to keep blocks separate:**

- Different exceptions need **different** handling (log-and-return vs. retry vs. re-raise)
- Intermediate values matter for the handler (you want the partial result when the second step fails)
- The blocks are far apart in the function (folding them together would nest too much)

**Use `contextlib.suppress` for trivial "ignore the error" cases:**

```python
from contextlib import suppress

def try_cleanup(path: Path) -> None:
    with suppress(FileNotFoundError):
        path.unlink()
```

Cleaner than a full try/except for the "best effort, doesn't matter if it fails" pattern.

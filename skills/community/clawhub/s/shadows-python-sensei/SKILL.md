---
name: python-sensei
description: "Python best practices enforcer — clean code, proper patterns, performance, testing, type hints. Use when writing or reviewing Python code."
metadata: { "openclaw": { "emoji": "🐍", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "anyBins": ["python", "python3"] }, "os": ["darwin", "linux", "win32"] } }
---

# Python Sensei — Best Practices Enforcer

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Writing new Python code
- Reviewing existing Python code
- User says "python review", "best practices", "clean up this python"
- Refactoring Python modules
- Setting up a new Python project

## WHEN NOT TO TRIGGER

- Quick scripts where quality doesn't matter
- User explicitly says "just make it work"
- Non-Python code

## PREREQUISITES

Requires `python` or `python3` on PATH for syntax checking (`python -m py_compile`) and test execution (`python -m pytest`).

Optional tools (auto-detected, recommendations adapt accordingly):
- **pytest** — test execution (`pip install pytest`)
- **mypy** or **pyright** — static type checking
- **ruff** — fast linting and formatting (`pip install ruff`)

The skill checks which tools are available and tailors its recommendations to the user's installed toolchain.

---

## CODE STANDARDS

### 1. Module Structure

```python
"""Module docstring — one line describing purpose."""

# Standard library imports
import os
from pathlib import Path

# Third-party imports
import httpx
from pydantic import BaseModel

# Local imports
from .config import Settings

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Module code...
```

**Rules**:
- Max 500 lines per module — split if larger
- Imports grouped: stdlib → third-party → local (blank line between each group)
- Constants at top, ALL_CAPS naming
- One class per file for complex classes

### 2. Functions

```python
async def fetch_user(user_id: str, *, include_profile: bool = False) -> User | None:
    """Fetch a user by ID.

    Args:
        user_id: The unique user identifier.
        include_profile: Whether to include full profile data.

    Returns:
        User object if found, None otherwise.

    Raises:
        ConnectionError: If the API is unreachable.
    """
```

**Rules**:
- Type hints on all public functions (params + return)
- Keyword-only args after `*` for clarity
- `None` return type when failure is normal (not exceptions)
- Docstrings on public functions only
- Max 30 lines per function — extract helpers if larger

### 3. Data Models

```python
from dataclasses import dataclass, field
from enum import StrEnum

class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

@dataclass
class User:
    id: str
    name: str
    status: Status = Status.ACTIVE
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "tags": self.tags,
        }
```

**Rules**:
- `@dataclass` for simple models, Pydantic for validation-heavy models
- `StrEnum` for states (JSON-serializable)
- Always include `to_dict()` for serialization
- Immutable by default (`frozen=True` when appropriate)

### 4. Error Handling

```python
# GOOD: Specific exceptions, minimal try blocks
try:
    response = await client.get(url)
    response.raise_for_status()
except httpx.TimeoutException:
    logger.warning("Request timed out: %s", url)
    return None
except httpx.HTTPStatusError as e:
    logger.error("HTTP %d: %s", e.response.status_code, url)
    raise

# BAD: Catching everything
try:
    do_everything()
except Exception:
    pass  # Never do this
```

**Rules**:
- Catch specific exceptions, never bare `except:`
- Only validate at system boundaries (user input, external APIs)
- Trust internal code — do not add defensive checks everywhere
- Use `logging` module, not `print()` for errors

### 5. Async Patterns

```python
import asyncio
import httpx

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [r.json() for r in responses if not isinstance(r, Exception)]
```

**Rules**:
- `async with` for resource management
- `asyncio.gather()` for parallel I/O
- `return_exceptions=True` to handle partial failures
- Never mix sync and async I/O in the same function

### 6. Testing

```python
import pytest

class TestUserService:
    def test_create_user_with_valid_data(self):
        user = create_user(name="Alice", email="alice@example.com")
        assert user.name == "Alice"
        assert user.status == Status.ACTIVE

    def test_create_user_rejects_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            create_user(name="", email="alice@example.com")

    @pytest.mark.asyncio
    async def test_fetch_user_returns_none_for_missing(self):
        result = await fetch_user("nonexistent-id")
        assert result is None
```

**Rules**:
- Test file: `tests/test_{module}.py`
- Test names describe the scenario: `test_[action]_[condition]_[expected]`
- One assertion per test (prefer)
- Use `pytest.raises` for expected exceptions
- Use fixtures for shared setup

### 7. Project Setup

```
project/
  src/
    project_name/
      __init__.py
      main.py
      config.py
      models.py
  tests/
    test_main.py
    test_models.py
  pyproject.toml
  requirements.txt
  .gitignore
```

`pyproject.toml` over `setup.py`. Pin major versions in `requirements.txt`.

---

## ANTI-PATTERNS TO FLAG

| Anti-Pattern | Fix |
|-------------|-----|
| `import *` | Explicit imports |
| Mutable default args | `field(default_factory=list)` |
| Global mutable state | Dependency injection |
| Nested try/except | Extract and flatten |
| String concatenation for SQL | Parameterized queries |
| `type()` checks | `isinstance()` |
| `os.path` | `pathlib.Path` |
| `requests` (sync) | `httpx` (async-ready) |

---

## SECURITY CONSIDERATIONS

This skill reads and writes Python source files within the working directory. It does not access files outside the project scope.

- **Commands executed**: `python -m py_compile <file>` for syntax checking, `python -m pytest <test_file>` for test execution. These run local project code — only use on trusted repositories or in sandboxed environments.
- **Data read**: Source files in the working directory only. No access to secrets, credentials, or system files.
- **Network access**: None required. The skill operates entirely offline.
- **Credentials**: None stored or accessed.
- **Persistence**: All modifications are to source files in the working directory only. No global config changes.
- **Sandboxing**: Recommended to run in a virtual environment (`venv`) to isolate dependencies.

---

## OUTPUT FORMAT

Reviews and code output follow the standards defined above. Each review identifies specific anti-patterns with line references and provides corrected code blocks.

---

## RULES

1. **Type hints everywhere** — public functions must have full type annotations
2. **500 lines max** — split large modules into focused sub-modules
3. **Test every module** — `tests/test_{module}.py` with descriptive test names
4. **Async by default** — use async for any I/O operation
5. **pathlib over os.path** — modern Python path handling
6. **No print debugging** — use `logging` module with appropriate levels

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**

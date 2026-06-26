---
name: python-plus
description: "Enhanced Python with async/await patterns, type hints, dataclasses, testing strategies, performance optimization, and project structure templates."
metadata:
  author: opencode
  version: 2.0
  tags: python, async, typing, testing, performance
  compatibility: opencode
  license: MIT
---

# Python Plus

Enhanced Python with async patterns, type hints, testing, and performance optimization.

## Features

- **Async/Await Patterns**: asyncio, aiohttp, async generators
- **Advanced Type Hints**: Generics, protocols, type guards
- **Data Classes**: attrs, pydantic, dataclasses
- **Testing Strategies**: pytest fixtures, parametrize, mocking
- **Performance**: Profiling, caching, optimization

## Quick Reference

| Task | Tool |
|------|------|
| Type checking | mypy, pyright |
| Formatting | black, ruff |
| Testing | pytest |
| Profiling | cProfile, py-spy |
| Linting | ruff, flake8 |

## Async/Await Patterns

### Basic Async

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Run async function
result = asyncio.run(fetch_data("https://api.example.com"))
```

### Async Generators

```python
async def fetch_pages(url: str):
    page = 1
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}?page={page}") as response:
                data = await response.json()
                if not data:
                    break
                yield data
                page += 1

# Usage
async for page_data in fetch_pages("https://api.example.com/items"):
    process(page_data)
```

### Async Context Managers

```python
class AsyncDatabase:
    async def __aenter__(self):
        self.conn = await asyncpg.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

# Usage
async with AsyncDatabase() as db:
    await db.execute("SELECT * FROM users")
```

### Task Groups

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(url1))
        task2 = tg.create_task(fetch_data(url2))
    
    # Both tasks completed
    result1 = task1.result()
    result2 = task2.result()
```

## Advanced Type Hints

### Generics

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, items: list[T]):
        self.items = items
    
    def get(self, index: int) -> T:
        return self.items[index]

# Usage
repo = Repository[int]([1, 2, 3])
```

### Protocols

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(shape: Drawable) -> None:
    shape.draw()
```

### Type Guards

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(data: list[object]) -> None:
    if is_string_list(data):
        # data is now list[str]
        print("\n".join(data))
```

### Literal Types

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    pass

set_mode("read")  # OK
set_mode("invalid")  # Error
```

## Data Classes

### Pydantic

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)

# Validation
user = User(name="Alice", email="alice@example.com", age=30)
```

### attrs

```python
import attrs

@attrs.define
class User:
    name: str
    email: str
    age: int = attrs.field(validator=attrs.validators.ge(0))
```

## Testing Strategies

### Pytest Fixtures

```python
import pytest
from myapp import create_app

@pytest.fixture
def app():
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
```

### Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_upper(input, expected):
    assert input.upper() == expected
```

### Mocking

```python
from unittest.mock import patch, MagicMock

@patch('myapp.external_api.fetch')
def test_with_mock(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    result = my_function()
    assert result["status"] == "ok"
```

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n: int) -> int:
    return n * n

# Async caching
from aiocache import cached

@cached(ttl=300)
async def get_user(user_id: int) -> dict:
    return await db.get_user(user_id)
```

### Profiling

```python
import cProfile

def profile_function():
    # Code to profile
    pass

cProfile.run('profile_function()')
```

### Slots

```python
class Point:
    __slots__ = ('x', 'y')
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
```

## Project Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

### pyproject.toml

```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.10"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.ruff]
line-length = 88
```

## Best Practices

1. **Use type hints** - Improve code clarity and tooling support
2. **Write docstrings** - Document public APIs
3. **Use virtual environments** - Isolate dependencies
4. **Follow PEP 8** - Consistent code style
5. **Write tests** - Aim for high coverage
6. **Profile before optimizing** - Don't guess bottlenecks
7. **Use async for I/O** - Don't block the event loop
8. **Prefer composition** - Over inheritance

# Python Code Review Guide

> Python 代码审查指南，覆盖类型注解、async/await、测试、异常处理、性能优化等核心主题。

## 目录

- [类型注解](#类型注解)
- [异步编程](#异步编程)
- [异常处理](#异常处理)
- [常见陷阱](#常见陷阱)
- [测试最佳实践](#测试最佳实践)
- [性能优化](#性能优化)
- [代码风格](#代码风格)
- [Review Checklist](#review-checklist)

---

## 类型注解

### 基础类型注解

```python
# ❌ 没有类型注解，IDE 无法提供帮助
def process_data(data, count):
    return data[:count]

# ✅ 使用类型注解
def process_data(data: str, count: int) -> str:
    return data[:count]
```

### 容器类型注解

```python
from typing import List, Dict, Sequence

# ❌ 不精确的类型
def get_names(users: list) -> list:
    return [u.name for u in users]

# ✅ 精确的容器类型（Python 3.9+ 可直接用 list[User]）
def get_names(users: list[User]) -> list[str]:
    return [u.name for u in users]

# ✅ 只读序列用 Sequence（更灵活）
def process_items(items: Sequence[str]) -> int:
    return len(items)
```

### Callable 与回调函数

```python
from typing import Callable, Awaitable

# ✅ 函数类型注解
Handler = Callable[[str, int], bool]

def register_handler(name: str, handler: Handler) -> None:
    handlers[name] = handler
```

### Protocol 与结构化子类型

```python
from typing import Protocol

# ✅ 定义协议（鸭子类型的类型检查）
class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...
```

---

## 异步编程

### async/await 基础

```python
import asyncio

# ❌ 同步阻塞调用
def fetch_all_sync(urls: list[str]) -> list[str]:
    results = []
    for url in urls:
        results.append(requests.get(url).text)  # 串行执行
    return results

# ✅ 异步并发调用
async def fetch_all(urls: list[str]) -> list[str]:
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)  # 并发执行
```

### 异步上下文管理器

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def get_connection() -> AsyncIterator[Connection]:
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

### 任务管理与取消

```python
import asyncio

# ❌ 忘记处理取消
async def bad_worker():
    while True:
        await do_work()  # 无法正常取消

# ✅ 正确处理取消
async def good_worker():
    try:
        while True:
            await do_work()
    except asyncio.CancelledError:
        await cleanup()
        raise

# ✅ 超时控制（Python 3.11+）
async def fetch_with_timeout(url: str) -> str:
    try:
        async with asyncio.timeout(10):
            return await fetch_url(url)
    except asyncio.TimeoutError:
        return ""
```

### 同步与异步混合

```python
# ✅ 在异步代码中运行同步函数
async def run_sync_in_async():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, blocking_io_function, arg1, arg2
    )
    return result

# ❌ 不要在异步代码中使用 time.sleep
async def bad_delay():
    time.sleep(1)  # 会阻塞整个事件循环！

# ✅ 使用 asyncio.sleep
async def good_delay():
    await asyncio.sleep(1)
```

---

## 异常处理

### 异常捕获最佳实践

```python
# ❌ Catching too broad
try:
    result = risky_operation()
except:  # Catches everything, even KeyboardInterrupt!
    pass

# ❌ 捕获 Exception 但不处理
try:
    result = risky_operation()
except Exception:
    pass  # 吞掉所有异常

# ✅ Catch specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except IOError as e:
    logger.error(f"IO error: {e}")
    return default_value
```

### 异常链

```python
# ❌ 丢失原始异常信息
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed")  # 丢失了原因

# ✅ 使用 from 保留异常链
try:
    result = external_api.call()
except APIError as e:
    raise RuntimeError("API failed") from e
```

### 自定义异常

```python
# ✅ 定义业务异常层次结构
class AppError(Exception):
    """应用基础异常"""
    pass

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str | int):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")
```

---

## 常见陷阱

### 可变默认参数

```python
# ❌ Mutable default arguments
def add_item(item, items=[]):  # Bug! Shared across calls
    items.append(item)
    return items

# ✅ Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 可变类属性

```python
# ❌ Using mutable class attributes
class User:
    permissions = []  # Shared across all instances!

# ✅ Initialize in __init__
class User:
    def __init__(self):
        self.permissions = []
```

### is vs ==

```python
# ❌ 用 is 比较值
if x is 1000:  # 可能不工作！
    pass

# ✅ 用 == 比较值
if x == 1000:
    pass

# ✅ is 只用于 None 和单例
if x is None:
    pass
```

### 字符串拼接性能

```python
# ❌ 循环中拼接字符串
result = ""
for item in large_list:
    result += str(item)  # O(n²) 复杂度

# ✅ 使用 join
result = "".join(str(item) for item in large_list)  # O(n)
```

---

## 测试最佳实践

### pytest 基础

```python
import pytest

# ✅ 使用参数化测试
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected

# ✅ 测试异常
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

### Fixtures

```python
# ✅ 带清理的 fixture
@pytest.fixture
def database() -> Generator[Database, None, None]:
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# ✅ 异步 fixture
@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client
```

### Mock 与 Patch

```python
from unittest.mock import Mock, patch, AsyncMock

# ✅ Mock 外部依赖
def test_send_email():
    mock_client = Mock()
    mock_client.send.return_value = True

    service = EmailService(client=mock_client)
    result = service.send_welcome_email("user@example.com")

    assert result is True
    mock_client.send.assert_called_once()

# ✅ Patch 模块级函数
@patch("myapp.services.external_api.call")
def test_with_patched_api(mock_call):
    mock_call.return_value = {"status": "ok"}
    result = process_data()
    assert result["status"] == "ok"
```

---

## 性能优化

### 数据结构选择

```python
# ❌ 列表查找 O(n)
if item in large_list:  # 慢
    pass

# ✅ 集合查找 O(1)
large_set = set(large_list)
if item in large_set:  # 快
    pass

# ✅ 使用 collections 模块
from collections import Counter, defaultdict, deque
```

### 生成器与迭代器

```python
# ❌ 一次性加载所有数据
def get_all_users():
    return [User(row) for row in db.fetch_all()]  # 内存占用大

# ✅ 使用生成器
def get_all_users():
    for row in db.fetch_all():
        yield User(row)  # 懒加载

# ✅ 生成器表达式
sum_of_squares = sum(x**2 for x in range(1000000))  # 不创建列表
```

### 缓存

```python
from functools import lru_cache, cache

# ✅ LRU 缓存
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    return sum(i**2 for i in range(n))

# ✅ 无限缓存（Python 3.9+）
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ✅ IO 密集型使用线程池
def fetch_all_urls(urls: list[str]) -> list[str]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, urls))
    return results

# ✅ CPU 密集型使用进程池
def process_large_dataset(data: list) -> list:
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(heavy_computation, data))
    return results
```

---

## 代码风格

### PEP 8 要点

```python
# ✅ 命名规范
class MyClass:  # 类名 PascalCase
    MAX_SIZE = 100  # 常量 UPPER_SNAKE_CASE

    def method_name(self):  # 方法 snake_case
        local_var = 1  # 变量 snake_case

# ✅ 导入顺序
# 1. 标准库
import os
import sys

# 2. 第三方库
import numpy as np

# 3. 本地模块
from myapp import config
```

### 现代 Python 特性

```python
# ✅ f-string（Python 3.6+）
print(f"Hello, {name}!")

# ✅ 海象运算符（Python 3.8+）
if (n := len(items)) > 10:
    print(f"List has {n} items")

# ✅ 模式匹配（Python 3.10+）
def handle_response(response: dict):
    match response:
        case {"status": "ok", "data": data}:
            return process_data(data)
        case {"status": "error", "message": msg}:
            raise APIError(msg)
        case _:
            raise ValueError("Unknown response format")
```

---

## Review Checklist

### 类型安全
- [ ] 函数有类型注解（参数和返回值）
- [ ] 使用 `Optional` 明确可能为 None
- [ ] 泛型类型正确使用
- [ ] mypy 检查通过
- [ ] 避免使用 `Any`

### 异步代码
- [ ] async/await 正确配对使用
- [ ] 没有在异步代码中使用阻塞调用
- [ ] 正确处理 `CancelledError`
- [ ] 使用 `asyncio.gather` 或 `TaskGroup` 并发执行
- [ ] 资源正确清理（async context manager）

### 异常处理
- [ ] 捕获特定异常类型，不使用裸 `except:`
- [ ] 异常链使用 `from` 保留原因
- [ ] 自定义异常继承自合适的基类

### 数据结构
- [ ] 没有使用可变默认参数
- [ ] 类属性不是可变对象
- [ ] 选择正确的数据结构（set vs list 查找）
- [ ] 大数据集使用生成器而非列表

### 测试
- [ ] 测试覆盖率达标（建议 ≥80%）
- [ ] 边界情况有测试覆盖
- [ ] Mock 正确隔离外部依赖
- [ ] 异步代码有对应的异步测试

### 代码风格
- [ ] 遵循 PEP 8
- [ ] 函数和类有 docstring
- [ ] 导入顺序正确
- [ ] 使用现代 Python 特性（f-string、walrus operator、match 等）

### 性能
- [ ] 避免循环中重复创建对象
- [ ] 字符串拼接使用 join
- [ ] 合理使用缓存（@lru_cache）
- [ ] IO/CPU 密集型使用合适的并行方式
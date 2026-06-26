---
name: python-testing
description: Python 测试速查。当需要：(1) 运行 pytest 测试 (2) 使用 mock/patch (3) 参数化测试 (4) fixtures (5) 异步测试 (6) 覆盖率测试时使用。
---

# Python Testing

Python 测试框架核心用法速查。

## 快速参考

### pytest 基础
```bash
pytest                        # 运行所有测试
pytest -v                     # 详细输出
pytest test_module.py         # 指定文件
pytest -k "login"             # 匹配测试名
pytest -x                     # 失败时停止
pytest -n 4                   # 并行执行
```

### 测试示例
```python
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.parametrize("a,b,expected", [(1,2,3), (2,3,5)])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Mock
```python
from unittest.mock import Mock, patch

mock_db = Mock()
mock_db.query.return_value = []

@patch('module.function')
def test_with_mock(mock_func):
    mock_func.return_value = 42
```

### Fixture
```python
@pytest.fixture
def database():
    db = Database(":memory:")
    yield db
    db.close()

def test_query(database):
    assert database.query("SELECT 1")
```

### 覆盖率
```bash
pytest --cov=myapp
pytest --cov=myapp --cov-report=html
```

## 详细参考

- **pytest 详解**: [references/pytest.md](references/pytest.md) - 完整 pytest 用法
- **Mock 和 Patch**: [references/mocking.md](references/mocking.md) - unittest.mock 详解
- **Fixtures**: [references/fixtures.md](references/fixtures.md) - fixture 高级用法
- **异步测试**: [references/async.md](references/async.md) - pytest-asyncio
- **覆盖率**: [references/coverage.md](references/coverage.md) - pytest-cov 配置

## 常用标记

```python
@pytest.mark.slow              # 标记慢测试
@pytest.mark.integration       # 标记集成测试
@pytest.mark.skip(reason="TODO")
@pytest.mark.skipif(sys.version_info < (3, 10))
```

## pytest.ini 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py
markers =
    slow: marks tests as slow
    integration: integration tests
addopts = -v --tb=short
```

## 文档

- pytest: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/

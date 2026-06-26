# pytest 详解

## 运行测试

```bash
pytest                        # 运行所有测试
pytest -v                     # 详细输出
pytest -vv                    # 更详细
pytest test_module.py         # 指定文件
pytest test_module.py::test_function  # 指定测试
pytest test_module.py::TestClass::test_method  # 指定方法
pytest -k "login"             # 匹配测试名
pytest -k "login or logout"
pytest -m slow                # 运行标记的测试
pytest -x                     # 失败时停止
pytest --maxfail=3            # 失败 3 次后停止
pytest -n auto                # 并行执行
pytest --lf                   # 只运行失败的测试
pytest --ff                   # 先运行失败，再运行其他
```

## 测试发现

```bash
# 默认规则
# test_*.py 或 *_test.py
# Test* 类 (无 __init__)
# test_* 函数

pytest tests/
pytest --ignore=tests/integration
```

## 测试类

```python
class TestUser:
    def test_create(self):
        user = User(name="Alice")
        assert user.name == "Alice"

    def setup_method(self):
        """每个测试方法前执行"""
        self.user = User()

    def teardown_method(self):
        """每个测试方法后执行"""
        pass
```

## 参数化

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

# 多参数
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
])

# 参数组合
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    pass  # 6 个测试
```

## 异常测试

```python
import pytest

def test_exception():
    with pytest.raises(ValueError):
        raise ValueError("error")

def test_exception_message():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("specific error")
    assert str(exc_info.value) == "specific error"

def test_exception_match():
    with pytest.raises(ValueError, match="specific.*error"):
        raise ValueError("specific error message")
```

## 临时文件

```python
def test_temp_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

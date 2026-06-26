# Mock 和 Patch

## Mock 对象

```python
from unittest.mock import Mock, MagicMock

# 创建 mock
mock_db = Mock()
mock_db.query.return_value = [{"id": 1}]
mock_db.insert.return_value = 1

# 使用
result = mock_db.query("SELECT *")
assert result == [{"id": 1}]

# 验证调用
mock_db.query.assert_called()
mock_db.query.assert_called_once()
mock_db.query.assert_called_with("SELECT *")
```

## patch 装饰器

```python
from unittest.mock import patch

@patch('module.Database')
def test_with_patch(MockDB):
    mock_db = MockDB.return_value
    mock_db.query.return_value = []

    service = Service()
    service.process()

    mock_db.query.assert_called()

# 多个 patch
@patch('module.Database')
@patch('module.Cache')
def test_multiple(MockCache, MockDB):
    pass
```

## patch 上下文管理器

```python
def test_with_context():
    with patch('module.get_user') as mock_get_user:
        mock_get_user.return_value = {"id": 1, "name": "Alice"}

        result = process_user(1)
        assert result == "Alice"
```

## patch 对象属性

```python
@patch.object(Config, 'DEBUG', True)
def test_debug_mode():
    pass

@patch.dict('os.environ', {'API_KEY': 'test-key'})
def test_with_env():
    pass
```

## pytest-mock

```python
# pip install pytest-mock

def test_with_mocker(mocker):
    # mock 函数
    mock_func = mocker.patch('module.function')
    mock_func.return_value = 42

    # mock 对象方法
    mock_method = mocker.patch.object(User, 'save')

    # spy (保留原实现)
    spy = mocker.spy(Calculator, 'add')

    # mock 异步函数
    async_mock = mocker.AsyncMock()
    async_mock.return_value = "result"
```

## 常见场景

```python
# mock 环境变量
@patch.dict('os.environ', {'API_KEY': 'test-key'})
def test_with_env():
    pass

# mock 时间
@patch('time.time', return_value=1234567890)
def test_time(mock_time):
    pass

# mock 文件操作
@patch('builtins.open', create=True)
def test_file(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = "content"

# mock HTTP 请求
@patch('requests.get')
def test_api(mock_get):
    mock_get.return_value.json.return_value = {"data": []}
    mock_get.return_value.status_code = 200

# mock 异常
def test_exception(mocker):
    mock_db = mocker.patch('module.Database')
    mock_db.return_value.query.side_effect = ConnectionError()
    with pytest.raises(ConnectionError):
        service.query()
```

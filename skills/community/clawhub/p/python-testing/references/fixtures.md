# Fixtures

## 基本 Fixture

```python
import pytest

@pytest.fixture
def database():
    db = Database(":memory:")
    db.connect()
    yield db
    db.close()

def test_query(database):
    result = database.query("SELECT 1")
    assert result is not None
```

## Fixture 依赖

```python
@pytest.fixture
def database():
    return Database(":memory:")

@pytest.fixture
def user(database):
    return database.create_user(name="Alice")

def test_user_name(user):
    assert user.name == "Alice"
```

## 作用域

```python
# function: 每个测试调用一次 (默认)
# class: 每个测试类调用一次
# module: 每个模块调用一次
# package: 每个包调用一次
# session: 整个测试会话调用一次

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.start()
    yield app
    app.stop()

@pytest.fixture(scope="session")
def docker_client():
    client = DockerClient()
    yield client
    client.close()
```

## autouse

```python
# 自动使用
@pytest.fixture(autouse=True)
def setup_teardown():
    print("Setup")
    yield
    print("Teardown")
```

## 参数化

```python
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    db = create_database(request.param)
    yield db
    db.close()

def test_with_multiple_dbs(database):
    # 会运行两次
    pass
```

## conftest.py

```python
# tests/conftest.py - 共享 fixture

import pytest

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_header():
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}
```

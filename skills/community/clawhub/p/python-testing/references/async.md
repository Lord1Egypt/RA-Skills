# 异步测试

## pytest-asyncio

```bash
pip install pytest-asyncio
```

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == "expected"

@pytest.mark.asyncio
async def test_async_with_mock():
    with pytest.raises(ValueError):
        await async_function_that_raises()
```

## 异步 Fixture

```python
@pytest.fixture
async def async_client():
    client = await create_async_client()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    result = await async_client.get("/")
    assert result.status == 200
```

## httpx 异步测试

```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_api(client):
    response = await client.get("/users")
    assert response.status_code == 200
```

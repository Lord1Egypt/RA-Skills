# 接口测试规范与常用模式

## 技术栈

- **语言**: Python 3.8+
- **测试框架**: pytest
- **HTTP 客户端**: requests
- **断言辅助**: pytest 内置 assert + jsonschema（可选）
- **报告**: pytest-html 或 allure-pytest

安装依赖：
```bash
pip install pytest requests pytest-html allure-pytest jsonschema
```

---

## 项目目录结构

```
api_tests/
├── conftest.py          # 全局 fixtures（base_url、token、session）
├── pytest.ini           # pytest 配置
├── requirements.txt
├── tests/
│   ├── test_auth.py     # 认证模块测试
│   ├── test_user.py     # 用户模块测试
│   └── test_order.py    # 订单模块测试
└── utils/
    ├── helpers.py       # 公共断言、工具函数
    └── data_factory.py  # 测试数据生成
```

---

## conftest.py 标准写法

```python
import pytest
import requests

BASE_URL = "https://api.example.com"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def auth_token(base_url):
    """登录获取 token，整个测试会话只执行一次"""
    resp = requests.post(f"{base_url}/auth/login", json={
        "username": "test@example.com",
        "password": "Test@1234"
    })
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    return resp.json()["data"]["token"]

@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """返回带 token 的请求头"""
    return {"Authorization": f"Bearer {auth_token}"}
```

---

## 标准测试文件结构

```python
import pytest
import requests

class TestUserAPI:
    """用户接口测试"""

    def test_get_user_info_success(self, base_url, auth_headers):
        """正向：有效 token 获取用户信息"""
        resp = requests.get(f"{base_url}/api/user/info", headers=auth_headers)

        # 状态码断言
        assert resp.status_code == 200, f"期望 200，实际 {resp.status_code}，响应: {resp.text}"

        # 响应体断言
        data = resp.json()
        assert data["code"] == 0, f"业务码错误: {data}"
        assert "userId" in data["data"], "响应缺少 userId 字段"
        assert "email" in data["data"], "响应缺少 email 字段"

        # 响应时间断言（超过 2000ms 发出警告）
        assert resp.elapsed.total_seconds() < 2, f"响应超时: {resp.elapsed.total_seconds():.2f}s"

    def test_get_user_info_unauthorized(self, base_url):
        """负向：无 token 返回 401"""
        resp = requests.get(f"{base_url}/api/user/info")
        assert resp.status_code == 401, f"期望 401，实际 {resp.status_code}"

    def test_get_user_info_invalid_token(self, base_url):
        """负向：无效 token 返回 401"""
        headers = {"Authorization": "Bearer invalid_token_here"}
        resp = requests.get(f"{base_url}/api/user/info", headers=headers)
        assert resp.status_code == 401
```

---

## 常用断言模式

```python
# 1. 状态码断言
assert resp.status_code == 200

# 2. 业务码断言（常见 code/message 结构）
body = resp.json()
assert body["code"] == 0
assert body["message"] == "success"

# 3. 字段存在性断言
assert "data" in body
assert body["data"] is not None

# 4. 字段值断言
assert body["data"]["status"] == "active"

# 5. 列表非空断言
assert len(body["data"]["list"]) > 0

# 6. 响应时间断言
assert resp.elapsed.total_seconds() < 2.0, f"响应时间 {resp.elapsed.total_seconds():.2f}s 超过 2s"

# 7. JSON Schema 校验（推荐用于关键接口）
from jsonschema import validate
schema = {
    "type": "object",
    "required": ["code", "data"],
    "properties": {
        "code": {"type": "integer"},
        "data": {"type": "object"}
    }
}
validate(instance=body, schema=schema)
```

---

## 参数化测试（数据驱动）

```python
import pytest

# 登录接口参数化测试：多组数据覆盖边界和异常
@pytest.mark.parametrize("username,password,expected_code,desc", [
    ("user@test.com", "Test@1234",  200, "正确账密"),
    ("user@test.com", "WrongPwd1",  401, "密码错误"),
    ("",              "Test@1234",  400, "邮箱为空"),
    ("notanemail",    "Test@1234",  400, "邮箱格式非法"),
    ("user@test.com", "",           400, "密码为空"),
])
def test_login_cases(base_url, username, password, expected_code, desc):
    """参数化覆盖多种登录场景"""
    resp = requests.post(f"{base_url}/auth/login", json={
        "username": username,
        "password": password
    })
    assert resp.status_code == expected_code, f"[{desc}] 期望 {expected_code}，实际 {resp.status_code}"
```

---

## 认证方式速查

```python
# Bearer Token
headers = {"Authorization": f"Bearer {token}"}

# API Key（Header）
headers = {"X-API-Key": "your_api_key"}

# Basic Auth
from requests.auth import HTTPBasicAuth
resp = requests.get(url, auth=HTTPBasicAuth("user", "pass"))

# Cookie
session = requests.Session()
session.post(f"{base_url}/login", json={"username": "u", "password": "p"})
# 后续请求自动带 cookie
resp = session.get(f"{base_url}/api/profile")
```

---

## 运行命令

```bash
# 运行全部测试
pytest tests/ -v

# 生成 HTML 报告
pytest tests/ -v --html=report.html --self-contained-html

# 生成 Allure 报告
pytest tests/ --alluredir=./allure-results
allure serve ./allure-results

# 只运行某个模块
pytest tests/test_user.py -v

# 按标记运行（如冒烟测试）
pytest -m smoke -v
```

# 云端 API Token 认证方案

## 方案对比

| 方案                         | 安全性   | 复杂度   | 适用场景      |
|----------------------------|-------|-------|-----------|
| **方案 1: Bearer Token**     | ⭐⭐⭐⭐  | ⭐⭐    | 推荐 - 简单安全 |
| **方案 2: API Key + Secret** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐   | 高安全性场景    |
| **方案 3: JWT Token**        | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐  | 分布式系统     |
| **方案 4: OAuth 2.0**        | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 第三方授权     |

---

## 方案 1: Bearer Token（推荐）⭐

### 优点

- ✅ 简单易用
- ✅ 性能高
- ✅ 广泛支持
- ✅ 适合移动端和 Web

### 实现方式

**生成 Token：**

```python
import secrets
import hashlib


def generate_token(user_id):
    """生成 Bearer Token"""
    # 生成随机字符串
    random_str = secrets.token_urlsafe(32)
    # 拼接用户 ID
    token_raw = f"{user_id}:{random_str}"
    # SHA256 哈希
    token = hashlib.sha256(token_raw.encode()).hexdigest()
    return token


# 示例
token = generate_token("13829295599")
print(f"Bearer Token: {token}")
```

**请求示例：**

```bash
curl -X POST https://lifeemergence.com/jeecg-boot-xzgz/api/account/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "13829295599"}'
```

**Python 请求：**

```python
import requests


def query_account(phone, token):
    url = "https://lifeemergence.com/jeecg-boot-xzgz/api/account/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"phoneNumber": phone}

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

**Token 存储：**

```python
# 服务端存储（Redis）
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)


def save_token(token, user_info, expire_seconds=86400):
    """保存 Token 到 Redis"""
    key = f"token:{token}"
    redis_client.setex(key, expire_seconds, json.dumps(user_info))


def get_token_info(token):
    """获取 Token 信息"""
    key = f"token:{token}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None
```

---

## 方案 2: API Key + Secret（高安全性）⭐⭐⭐⭐⭐

### 优点

- ✅ 最高安全性
- ✅ 支持签名验证
- ✅ 防篡改
- ✅ 适合服务器间通信

### 实现方式

**生成 API Key 和 Secret：**

```python
import secrets


def generate_api_key():
    """生成 API Key 和 Secret"""
    api_key = f"ak_{secrets.token_urlsafe(16)}"
    api_secret = f"as_{secrets.token_urlsafe(32)}"
    return api_key, api_secret


# 示例
api_key, api_secret = generate_api_key()
print(f"API Key: {api_key}")
print(f"API Secret: {api_secret}")
```

**签名生成：**

```python
import hashlib
import time


def generate_signature(api_secret, params, timestamp):
    """生成请求签名"""
    # 排序参数
    sorted_params = sorted(params.items())
    # 拼接字符串
    sign_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    # 添加时间戳和 Secret
    sign_string += f"&timestamp={timestamp}&secret={api_secret}"
    # SHA256 哈希
    signature = hashlib.sha256(sign_string.encode()).hexdigest()
    return signature


# 示例
timestamp = str(int(time.time()))
params = {"phoneNumber": "13829295599", "amount": 50}
signature = generate_signature(api_secret, params, timestamp)
```

**请求示例：**

```bash
curl -X POST https://lifeemergence.com/jeecg-boot-xzgz/api/account/query \
  -H "X-API-Key: ak_xxxxx" \
  -H "X-Timestamp: 1234567890" \
  -H "X-Signature: xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "13829295599"}'
```

**Python 请求：**

```python
import requests
import time


def query_account_signed(phone, api_key, api_secret):
    url = "https://lifeemergence.com/jeecg-boot-xzgz/api/account/query"

    timestamp = str(int(time.time()))
    params = {"phoneNumber": phone}
    signature = generate_signature(api_secret, params, timestamp)

    headers = {
        "X-API-Key": api_key,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=params)
    return response.json()
```

**签名验证（服务端）：**

```python
def verify_signature(api_key, params, timestamp, signature):
    """验证请求签名"""
    # 检查时间戳（防止重放攻击）
    current_time = int(time.time())
    if abs(current_time - int(timestamp)) > 300:  # 5 分钟有效期
        return False

    # 获取 API Secret
    api_secret = get_api_secret_from_db(api_key)
    if not api_secret:
        return False

    # 重新计算签名
    expected_signature = generate_signature(api_secret, params, timestamp)

    # 比较签名
    return signature == expected_signature
```

---

## 方案 3: JWT Token（分布式系统）⭐⭐⭐⭐⭐

### 优点

- ✅ 无状态
- ✅ 支持跨域
- ✅ 包含用户信息
- ✅ 适合微服务架构

### 实现方式

**生成 JWT Token：**

```python
import jwt
import datetime


def generate_jwt_token(user_id, secret_key):
    """生成 JWT Token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


# 示例
secret_key = "your-secret-key"
token = generate_jwt_token("13829295599", secret_key)
print(f"JWT Token: {token}")
```

**验证 JWT Token：**

```python
def verify_jwt_token(token, secret_key):
    """验证 JWT Token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 过期
    except jwt.InvalidTokenError:
        return None  # Token 无效
```

**请求示例：**

```bash
curl -X POST https://lifeemergence.com/jeecg-boot-xzgz/api/account/query \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json"
```

---

## 方案 4: OAuth 2.0（第三方授权）⭐⭐⭐⭐⭐

### 优点

- ✅ 标准化协议
- ✅ 支持第三方授权
- ✅ 安全性高
- ✅ 适合开放平台

### 实现方式

**授权流程：**

```
1. 用户授权 → 获取授权码
2. 授权码换 Token → 获取 access_token
3. 使用 access_token 访问 API
```

**获取 Token：**

```python
import requests


def get_oauth_token(client_id, client_secret, authorization_code):
    """OAuth 2.0 获取 Token"""
    url = "https://lifeemergence.com/jeecg-boot-xzgz/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": "https://lifeemergence.com/jeecg-boot-xzgz/callback"
    }

    response = requests.post(url, data=data)
    return response.json()
```

---

## 推荐方案对比

### 你的场景（增值账户续费）

| 需求        | 推荐方案                   | 理由        |
|-----------|------------------------|-----------|
| **简单快速**  | 方案 1: Bearer Token     | 实现简单，性能好  |
| **高安全性**  | 方案 2: API Key + Secret | 签名验证，防篡改  |
| **微服务架构** | 方案 3: JWT Token        | 无状态，跨服务   |
| **开放平台**  | 方案 4: OAuth 2.0        | 标准化，支持第三方 |

---

## 我的推荐：方案 1 + 方案 2 混合

### 为什么？

1. **Bearer Token** 用于用户端（简单）
2. **API Key + Secret** 用于服务端（安全）

### 实现示例

**用户端（Bearer Token）：**

```python
# 生成 Token
token = generate_token(phone_number)

# 请求 API
headers = {"Authorization": f"Bearer {token}"}
```

**服务端（API Key + Secret）：**

```python
# 生成签名
signature = generate_signature(api_secret, params, timestamp)

# 请求 API
headers = {
    "X-API-Key": api_key,
    "X-Signature": signature,
    "X-Timestamp": timestamp
}
```

---

## Token 管理最佳实践

### 1. Token 过期时间

```python
# Bearer Token: 24 小时
expire_seconds = 86400

# API Key: 永不过期（除非手动撤销）
# JWT Token: 1-24 小时
```

### 2. Token 刷新机制

```python
def refresh_token(old_token):
    """刷新 Token"""
    user_info = get_token_info(old_token)
    if user_info:
        new_token = generate_token(user_info['user_id'])
        save_token(new_token, user_info)
        # 删除旧 Token
        delete_token(old_token)
        return new_token
    return None
```

### 3. Token 撤销

```python
def revoke_token(token):
    """撤销 Token"""
    key = f"token:{token}"
    redis_client.delete(key)

    # 或加入黑名单
    redis_client.setex(f"token_blacklist:{token}", 86400, "revoked")
```

### 4. 速率限制

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_user_id_from_token)


@app.route("/api/account/query")
@limiter.limit("100 per hour")
def query_account():
    pass
```

---

## 安全建议

1. ✅ **使用 HTTPS** - 所有 API 请求使用 HTTPS
2. ✅ **Token 加密存储** - 不要明文存储 Token
3. ✅ **定期轮换密钥** - 定期更换 API Secret
4. ✅ **限制请求频率** - 防止暴力破解
5. ✅ **验证时间戳** - 防止重放攻击
6. ✅ **最小权限原则** - Token 只授予必要权限

---

## 选择建议

**如果你的场景：**

- ✅ **简单快速上线** → 选择 **方案 1: Bearer Token**
- ✅ **高安全性要求** → 选择 **方案 2: API Key + Secret**
- ✅ **微服务架构** → 选择 **方案 3: JWT Token**
- ✅ **开放平台** → 选择 **方案 4: OAuth 2.0**

**我的推荐：方案 1（Bearer Token）** 对于增值账户续费系统已经足够！

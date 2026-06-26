# Bearer Token 认证实现文档

## 📦 已实现的功能

| 文件 | 功能 | 状态 |
|------|------|------|
| `token_manager.py` | Token 管理器 | ✅ 完成 |
| `cloud_api_auth.py` | 云端 API 认证示例 | ✅ 完成 |
| `token-schemes.md` | Token 方案文档 | ✅ 完成 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Flask（可选，用于 API 服务器）
pip install flask

# 安装 Redis（可选，用于分布式存储）
pip install redis
```

---

### 2. 生成 Token

```python
from token_manager import TokenManager

# 初始化 Token 管理器
tm = TokenManager()

# 生成 Token
token = tm.generate_token(
    user_id="13829295599",
    extra_data={'phone': '13829295599', 'vip_level': 1},
    expire_seconds=86400  # 24 小时
)

print(f"Token: {token}")
```

---

### 3. 验证 Token

```python
# 验证 Token
token_data = tm.verify_token(token)

if token_data:
    print(f"✅ Token 有效")
    print(f"用户 ID: {token_data['user_id']}")
else:
    print(f"❌ Token 无效或已过期")
```

---

### 4. 刷新 Token

```python
# 刷新 Token（获取新 Token，撤销旧 Token）
new_token = tm.refresh_token(old_token)

if new_token:
    print(f"✅ Token 已刷新")
```

---

### 5. 撤销 Token

```python
# 撤销 Token（注销）
success = tm.revoke_token(token)

if success:
    print(f"✅ Token 已撤销")
```

---

## 🌐 云端 API 使用示例

### 启动 API 服务器

```bash
cd /home/admin/openclaw/workspace/skills/smyx_payment/scripts
python3 cloud_api_auth.py
```

服务器将在 `http://localhost:5000` 启动。

---

### API 路由

| 路由 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/auth/login` | POST | ❌ | 用户登录（获取 Token） |
| `/api/auth/refresh` | POST | ✅ | 刷新 Token |
| `/api/auth/logout` | POST | ✅ | 注销（撤销 Token） |
| `/api/account/query` | POST | ✅ | 查询账户 |
| `/api/account/recharge` | POST | ✅ | 创建充值订单 |
| `/api/payment/notify` | POST | ❌ | 支付宝支付回调 |
| `/api/auth/stats` | GET | ✅ | Token 统计 |
| `/health` | GET | ❌ | 健康检查 |

---

### 测试命令

#### 1. 登录获取 Token

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "13829295599"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "token": "8166919e527fc67801eda13a60be50d4...",
    "expires_in": 86400,
    "token_type": "Bearer",
    "user": {
      "user_id": "13829295599",
      "phone": "13829295599"
    }
  }
}
```

---

#### 2. 查询账户

```bash
curl -X POST http://localhost:5000/api/account/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "13829295599"}'
```

**响应：**
```json
{
  "success": true,
  "data": {
    "phoneNumber": "13829295599",
    "totalRecharged": 500.00,
    "balance": 20.00,
    "remainingUses": 5,
    "usedCount": 45,
    "isInsufficient": true
  }
}
```

---

#### 3. 创建充值订单

```bash
curl -X POST http://localhost:5000/api/account/recharge \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumber": "13829295599",
    "amount": 30,
    "packageType": "标准套餐",
    "package": {
      "amount": 30,
      "uses": 1200,
      "name": "标准套餐"
    }
  }'
```

---

#### 4. 刷新 Token

```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <token>"
```

---

#### 5. 注销

```bash
curl -X POST http://localhost:5000/api/auth/logout \
  -H "Authorization: Bearer <token>"
```

---

## 🔧 集成到 smyx_payment 技能

### 修改 `alipay_real_payment.py`

```python
from token_manager import get_token_manager

# 获取 Token 管理器
token_manager = get_token_manager()

# 生成 Token（用户登录后）
def login(phone_number):
    # TODO: 验证用户密码
    token = token_manager.generate_token(
        user_id=phone_number,
        extra_data={'phone': phone_number}
    )
    return token

# 验证 Token（API 请求时）
def verify_request(token):
    token_data = token_manager.verify_token(token)
    if not token_data:
        return False, "Token 无效或已过期"
    return True, token_data
```

---

## 📊 Token 管理功能

### 1. Token 生成

```python
token = tm.generate_token(
    user_id="13829295599",      # 用户 ID
    extra_data={'vip': 1},      # 额外数据
    expire_seconds=86400        # 过期时间（秒）
)
```

### 2. Token 验证

```python
token_data = tm.verify_token(token)
if token_data:
    user_id = token_data['user_id']
    extra = token_data['extra_data']
```

### 3. Token 刷新

```python
new_token = tm.refresh_token(old_token)
```

### 4. Token 撤销

```python
tm.revoke_token(token)
```

### 5. 统计信息

```python
stats = tm.get_stats()
print(f"活跃 Token 数：{stats['active_tokens']}")
print(f"黑名单 Token 数：{stats['blacklisted_tokens']}")
```

---

## 🗄️ 存储方式

### 内存存储（默认）

```python
tm = TokenManager(use_redis=False)
```

**适用场景：**
- ✅ 开发测试
- ✅ 单服务器
- ✅ 轻量级应用

---

### Redis 存储（推荐生产环境）

```python
tm = TokenManager(
    use_redis=True,
    redis_host='localhost',
    redis_port=6379
)
```

**适用场景：**
- ✅ 生产环境
- ✅ 多服务器集群
- ✅ 需要持久化

**安装 Redis：**
```bash
# 安装 Redis 服务器
apt-get install redis-server

# 安装 Python 客户端
pip install redis
```

---

## 🔒 安全建议

### 1. 使用 HTTPS

```python
# Flask 应用使用 HTTPS
app.run(ssl_context='adhoc')
```

### 2. 设置合理的过期时间

```python
# 普通 Token: 24 小时
token = tm.generate_token(user_id, expire_seconds=86400)

# 敏感操作 Token: 1 小时
token = tm.generate_token(user_id, expire_seconds=3600)
```

### 3. 定期轮换密钥

```python
# 更换 secret_key
tm = TokenManager(secret_key=new_secret_key)
```

### 4. 限制请求频率

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_user_id_from_token)

@app.route("/api/account/query")
@limiter.limit("100 per hour")
def query_account():
    pass
```

---

## 📋 完整流程

```
【1】用户登录
   ↓
【2】生成 Token
   ↓
【3】返回 Token 给客户端
   ↓
【4】客户端存储 Token
   ↓
【5】客户端请求 API（携带 Token）
   ↓
【6】服务端验证 Token
   ↓
【7】验证通过，返回数据
   ↓
【8】Token 过期前刷新
   ↓
【9】用户注销，撤销 Token
```

---

## ✅ 实现总结

| 功能 | 状态 | 文件 |
|------|------|------|
| Token 生成 | ✅ | `token_manager.py` |
| Token 验证 | ✅ | `token_manager.py` |
| Token 刷新 | ✅ | `token_manager.py` |
| Token 撤销 | ✅ | `token_manager.py` |
| Flask 认证中间件 | ✅ | `cloud_api_auth.py` |
| 登录接口 | ✅ | `cloud_api_auth.py` |
| 查询账户接口 | ✅ | `cloud_api_auth.py` |
| 充值接口 | ✅ | `cloud_api_auth.py` |
| 支付回调接口 | ✅ | `cloud_api_auth.py` |

---

## 🎯 下一步

1. **部署 API 服务器**
   ```bash
   python3 cloud_api_auth.py
   ```

2. **测试认证流程**
   ```bash
   # 登录
   curl -X POST http://localhost:5000/api/auth/login \
     -d '{"phoneNumber": "13829295599"}'
   
   # 查询
   curl -X POST http://localhost:5000/api/account/query \
     -H "Authorization: Bearer <token>"
   ```

3. **集成到 smyx_payment 技能**
   - 修改 `alipay_real_payment.py` 使用 Token 认证
   - 修改 `query.py` 携带 Token 请求

---

**Bearer Token 认证已完整实现！** 🎉

# OpenClaw Gateway 端口配置

## 默认端口

OpenClaw Gateway 默认运行在以下端口：

- **主 Gateway 端口**: `18789`
- **Web UI 端口**: `8080` (如果启用)
- **API 端口**: `18789` (与 Gateway 相同)

## WhatsApp 监控技能配置

### 1. API 端点

WhatsApp 监控技能使用以下 API 端点：

| 功能 | HTTP 方法 | 端点路径 | 完整 URL |
|------|-----------|----------|----------|
| 获取消息 | GET | `/api/v1/channels/whatsapp/messages` | `http://localhost:18789/api/v1/channels/whatsapp/messages` |
| 发送消息 | POST | `/api/v1/channels/whatsapp/send` | `http://localhost:18789/api/v1/channels/whatsapp/send` |
| 获取聊天列表 | GET | `/api/v1/channels/whatsapp/chats` | `http://localhost:18789/api/v1/channels/whatsapp/chats` |
| 获取联系人列表 | GET | `/api/v1/channels/whatsapp/contacts` | `http://localhost:18789/api/v1/channels/whatsapp/contacts` |
| 获取渠道状态 | GET | `/api/v1/channels/whatsapp/status` | `http://localhost:18789/api/v1/channels/whatsapp/status` |

### 2. 端口配置位置

端口配置在以下文件中：

**`scripts/whatsapp_client.py`** (第 13 行):
```python
self.base_url = "http://localhost:18789"  # OpenClaw Gateway 默认地址
```

### 3. 自定义端口配置

如果你的 OpenClaw Gateway 运行在不同的端口，需要修改：

#### 方法一：直接修改代码

编辑 `scripts/whatsapp_client.py`，修改第 13 行：
```python
self.base_url = "http://localhost:你的端口号"  # 自定义端口
```

#### 方法二：使用环境变量（推荐）

修改 `scripts/whatsapp_client.py` 支持环境变量：

```python
import os

# 从环境变量读取端口，默认使用 18789
port = os.environ.get('OPENCLAW_PORT', '18789')
self.base_url = f"http://localhost:{port}"
```

然后设置环境变量：
```bash
export OPENCLAW_PORT=18789
```

#### 方法三：配置文件

在配置文件中添加端口配置：

**`config/whatsapp-targets.json`**:
```json
{
  "openclaw": {
    "host": "localhost",
    "port": 18789,
    "api_key": "your_api_key_optional"
  },
  "targets": [...]
}
```

然后在代码中读取配置：
```python
openclaw_config = self.config.get("openclaw", {})
host = openclaw_config.get("host", "localhost")
port = openclaw_config.get("port", 18789)
self.base_url = f"http://{host}:{port}"
```

### 4. 多实例配置

如果你运行多个 OpenClaw 实例，需要指定不同的端口：

| 实例 | 端口 | 用途 |
|------|------|------|
| 主实例 | 18789 | 生产环境 |
| 测试实例 | 18790 | 测试环境 |
| 开发实例 | 18791 | 开发环境 |

相应的配置：
```python
# 生产环境
self.base_url = "http://localhost:18789"

# 测试环境  
self.base_url = "http://localhost:18790"

# 开发环境
self.base_url = "http://localhost:18791"
```

### 5. 网络配置

#### 本地访问
```python
self.base_url = "http://localhost:18789"
```

#### 局域网访问
如果 OpenClaw 运行在其他机器上：
```python
self.base_url = "http://192.168.1.100:18789"  # 替换为实际 IP
```

#### HTTPS 访问
如果配置了 HTTPS：
```python
self.base_url = "https://your-domain.com:18789"
```

### 6. 端口检查

#### 检查端口是否开放
```bash
netstat -an | grep 18789
# 或
ss -tlnp | grep 18789
```

#### 测试连接
```bash
# 使用 curl
curl http://localhost:18789/health

# 或使用 Python
python -c "import requests; r = requests.get('http://localhost:18789/health'); print(r.status_code)"
```

### 7. 防火墙配置

如果连接失败，可能需要配置防火墙：

**Linux 防火墙**:
```bash
# Ubuntu/Debian
sudo ufw allow 18789/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=18789/tcp
sudo firewall-cmd --reload
```

### 8. 故障排除

#### 连接被拒绝
```
ConnectionRefusedError: ... 连接被拒绝 ...
```

**解决方案**:
1. 确认 OpenClaw Gateway 正在运行
2. 检查端口是否正确：`netstat -an | grep 18789` 或 `ss -tlnp | grep 18789`
3. 检查防火墙设置
4. 确认没有其他程序占用该端口

#### 连接超时
```
TimeoutError: The read operation timed out
```

**解决方案**:
1. 检查网络连接
2. 增加超时时间配置
3. 检查 OpenClaw Gateway 负载

#### SSL 证书错误
```
SSLError: Certificate verify failed
```

**解决方案**:
1. 使用 HTTP 而不是 HTTPS
2. 添加证书验证例外（仅限测试环境）
3. 配置正确的 SSL 证书

### 9. 性能优化

#### 连接池
```python
# 在 whatsapp_client.py 中配置连接池
connector = aiohttp.TCPConnector(limit=10)  # 最大连接数
session = aiohttp.ClientSession(connector=connector)
```

#### 超时设置
```python
# 设置合理的超时时间
timeout = aiohttp.ClientTimeout(total=30)  # 总超时 30 秒
async with session.get(url, timeout=timeout) as response:
    ...
```

#### 重试机制
```python
# 添加重试逻辑
max_retries = 3
for attempt in range(max_retries):
    try:
        response = await session.get(url)
        break
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        if attempt == max_retries - 1:
            raise
        await asyncio.sleep(2 ** attempt)  # 指数退避
```

### 10. 监控和日志

#### 启用详细日志
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

#### 监控连接状态
```python
# 定期检查连接
async def check_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health", timeout=5) as response:
                return response.status == 200
    except Exception:
        return False
```

#### 记录连接统计
```python
self.connection_stats = {
    "successful": 0,
    "failed": 0,
    "total_time": 0,
    "last_check": None
}
```

通过正确配置端口，WhatsApp 监控技能可以可靠地与 OpenClaw Gateway 通信，实现消息的实时监控和处理。
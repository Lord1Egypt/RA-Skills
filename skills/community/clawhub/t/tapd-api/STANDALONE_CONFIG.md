# TAPD API Skill - 独立配置模式

## 配置方式

**独立配置文件**（推荐）- 所有配置存储在一个文件中

创建 `tapd-config.json`：

```json
{
  "oauth": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret"
  },
  "workspaces": [
    {
      "id": "12345678",
      "name": "项目A",
      "default": true
    },
    {
      "id": "87654321",
      "name": "项目B"
    }
  ]
}
```

## 使用方法

### Python SDK

```python
from scripts.tapd_client import TapdClient
import json

# 读取配置
with open('tapd-config.json') as f:
    config = json.load(f)

# 获取默认工作空间
default_workspace = next(
    (ws for ws in config['workspaces'] if ws.get('default')),
    config['workspaces'][0]
)

# 初始化客户端
client = TapdClient(
    auth_type='oauth',
    client_id=config['oauth']['clientId'],
    client_secret=config['oauth']['clientSecret'],
    workspace_id=default_workspace['id']
)

# 使用
stories = client.story.list(workspace_id=default_workspace['id'], limit=10)
```

### Shell 工具

```bash
# 方式一：环境变量
export TAPD_CLIENT_ID="your-client-id"
export TAPD_CLIENT_SECRET="your-client-secret"
export TAPD_WORKSPACE_ID="12345678"

./scripts/tapd-api.sh story list --limit 10

# 方式二：直接传参（修改脚本支持）
./scripts/tapd-api.sh story list \
  --client-id "your-id" \
  --client-secret "your-secret" \
  --workspace "12345678" \
  --limit 10
```

## 配置文件结构

```json
{
  "oauth": {
    "clientId": "TAPD OAuth 应用 ID",
    "clientSecret": "TAPD OAuth 应用密钥"
  },
  "workspaces": [
    {
      "id": "工作空间 ID",
      "name": "项目名称（可选）",
      "default": true
    }
  ]
}
```

## 安全建议

1. ⚠️ **必须**: 将配置文件加入 `.gitignore`
2. ⚠️ **必须**: 不要提交真实凭证到 Git
3. ✅ **推荐**: 定期轮换 OAuth 密钥
4. ✅ **推荐**: 文件权限设置为 `600`

```bash
# 设置文件权限
chmod 600 tapd-config.json

# 确认加入 .gitignore
echo "tapd-config.json" >> .gitignore
```

## 多项目配置

**项目A (tapd-projecta.json)**:
```json
{
  "oauth": {
    "clientId": "app-id",
    "clientSecret": "app-secret"
  },
  "workspaces": [
    {
      "id": "12345678",
      "name": "项目A",
      "default": true
    }
  ]
}
```

**或者在一个文件中管理多个工作空间**:
```json
{
  "oauth": {
    "clientId": "app-id",
    "clientSecret": "app-secret"
  },
  "workspaces": [
    {
      "id": "12345678",
      "name": "项目A",
      "default": true
    },
    {
      "id": "87654321",
      "name": "项目B"
    }
  ]
}
```

**使用**:
```python
# 遍历所有工作空间
for workspace in config['workspaces']:
    client = TapdClient(
        auth_type='oauth',
        client_id=config['oauth']['clientId'],
        client_secret=config['oauth']['clientSecret'],
        workspace_id=workspace['id']
    )
    
    stories = client.story.list(workspace_id=workspace['id'], limit=5)
    print(f"{workspace['name']}: {len(stories)} 条需求")
```

---

**优势**:
- ✅ 配置自包含，不依赖全局配置
- ✅ 便于版本管理（提供模板文件）
- ✅ 易于切换不同项目
- ✅ 独立部署，无外部依赖

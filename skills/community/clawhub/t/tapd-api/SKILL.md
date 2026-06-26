---
name: tapd-api
description: TAPD API 完整集成。实现 18 个模块、70+ API 方法，支持 OAuth 和 Basic Auth 认证。涵盖需求、任务、缺陷、迭代、测试、Wiki、工时等所有 TAPD 功能。
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3"]
  version: "2.1.0"
  author: "OpenClaw Community"
  license: "MIT"
  tags: ["tapd", "api", "project-management", "sdk"]
---

# TAPD API Skill

完整的 TAPD 开放平台集成，实现所有 TAPD API 模块。基于 [TAPD PHP SDK](https://github.com/ouronghuang/tapd) 用 Python 重新实现。

## 📋 功能特性

- ✅ 从 `tapd.json` 读取 OAuth 配置
- ✅ 自动换取和刷新 access_token
- ✅ 支持多工作空间切换
- ✅ 完整的 API 封装（18 个模块，70+ 方法）
- ✅ 命令行工具 + Python SDK
- ✅ 详细的使用文档和示例

## 🔧 配置

### 配置文件 (tapd.json)

所有配置存储在 `tapd.json` 文件中，支持多工作空间：

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

### 配置项说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `oauth.clientId` | 是 | TAPD OAuth 应用 ID |
| `oauth.clientSecret` | 是 | TAPD OAuth 应用密钥 |
| `workspaces` | 是 | 工作空间列表 |
| `workspaces[].id` | 是 | 工作空间 ID |
| `workspaces[].name` | 否 | 工作空间名称（便于识别） |
| `workspaces[].default` | 否 | 是否为默认工作空间 |

### 获取 OAuth 凭证

1. 登录 TAPD 开放平台: https://open.tapd.cn
2. 创建开放应用
3. 获取 **应用ID** (clientId) 和 **应用密钥** (clientSecret)
4. 配置应用权限（需求、任务、缺陷等）
5. 将应用安装到目标项目

### 获取工作空间 ID

- 打开 TAPD 项目
- URL 中的数字即为 workspace_id
- 例如: `https://www.tapd.cn/12345678/` → workspace_id 是 `12345678`

## 🚀 快速开始

### 1. 创建配置文件

```bash
# 创建 tapd.json
cat > tapd.json << 'EOF'
{
  "oauth": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret"
  },
  "workspaces": [
    {
      "id": "12345678",
      "name": "我的项目",
      "default": true
    }
  ]
}
EOF

# 设置权限
chmod 600 tapd.json
```

### 2. Python SDK 使用

```python
from scripts.tapd_client import TapdClient
import json

# 读取配置
with open('tapd.json') as f:
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

# 获取需求列表
stories = client.story.list(
    workspace_id=default_workspace['id'],
    limit=10
)

print(f"获取到 {len(stories)} 条需求")
```

### 3. 多工作空间切换

```python
# 遍历所有工作空间
for workspace in config['workspaces']:
    print(f"工作空间: {workspace['name']}")
    
    client = TapdClient(
        auth_type='oauth',
        client_id=config['oauth']['clientId'],
        client_secret=config['oauth']['clientSecret'],
        workspace_id=workspace['id']
    )
    
    stories = client.story.list(workspace_id=workspace['id'], limit=5)
    print(f"  需求数: {len(stories)}")
```

### 3. Shell 命令行使用

```bash
# 设置环境变量（从配置文件读取）
export TAPD_CLIENT_ID=$(cat tapd.json | jq -r '.oauth.clientId')
export TAPD_CLIENT_SECRET=$(cat tapd.json | jq -r '.oauth.clientSecret')
export TAPD_WORKSPACE_ID=$(cat tapd.json | jq -r '.workspace_id')

# 使用命令行工具
./scripts/tapd-api.sh story list --limit 10
./scripts/tapd-api.sh story count
./scripts/tapd-api.sh bug list --status new
```

# 获取需求列表
stories = client.get_stories(limit=10)
for story in stories:
    print(f"{story['id']}: {story['name']}")

# 获取需求详情
story_detail = client.get_story(story_id="1112345678001000001")

# 获取任务列表
tasks = client.get_tasks(limit=5)

# 获取缺陷列表
bugs = client.get_bugs(limit=5)
```

## 📖 API 认证流程

### OAuth 流程图

```
┌─────────────────────────────────────────────────────────┐
│ 1. 从 tapd.json 读取 clientId + clientSecret      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. POST /tokens/request_token                          │
│    grant_type=client_credentials                       │
│    Authorization: Basic base64(clientId:clientSecret)  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. 获取 access_token (有效期 7200 秒 / 2 小时)        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. 调用 TAPD API                                       │
│    Authorization: Bearer <access_token>                │
└─────────────────────────────────────────────────────────┘
```

### 认证代码示例

```bash
# Shell 方式
CLIENT_ID="your-client-id"
CLIENT_SECRET="your-client-secret"

# 获取 access_token
ACCESS_TOKEN=$(curl -s -u "$CLIENT_ID:$CLIENT_SECRET" \
  -d "grant_type=client_credentials" \
  "https://api.tapd.cn/tokens/request_token" \
  | python3 -c "import json, sys; print(json.load(sys.stdin)['data']['access_token'])")

# 调用 API
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://api.tapd.cn/stories?workspace_id=12345678&limit=10"
```

## 🔌 API 端点

### 需求 (Stories)

| 方法 | 端点 | 参数 | 说明 |
|------|------|------|------|
| GET | `/stories` | workspace_id, limit, page, status | 获取需求列表 |
| GET | `/stories/count` | workspace_id, status | 获取需求数量 |
| POST | `/stories` | workspace_id, name, description | 创建需求 |
| POST | `/stories` | workspace_id, id, ... | 更新需求 |

### 任务 (Tasks)

| 方法 | 端点 | 参数 | 说明 |
|------|------|------|------|
| GET | `/tasks` | workspace_id, limit, page | 获取任务列表 |
| POST | `/tasks` | workspace_id, name, ... | 创建/更新任务 |

### 缺陷 (Bugs)

| 方法 | 端点 | 参数 | 说明 |
|------|------|------|------|
| GET | `/bugs` | workspace_id, limit, page, status | 获取缺陷列表 |
| POST | `/bugs` | workspace_id, title, ... | 创建/更新缺陷 |

### 迭代 (Iterations)

| 方法 | 端点 | 参数 | 说明 |
|------|------|------|------|
| GET | `/iterations` | workspace_id, limit, page | 获取迭代列表 |

### 其他

- `/workspaces/projects` - 获取项目列表
- `/releases` - 发布计划
- `/tcases` - 测试用例
- `/comments` - 评论

## 📝 使用示例

### 示例 1: 获取高优先级需求

```bash
# 使用命令行工具（自动过滤）
./scripts/tapd-api.sh stories 50 | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data['data']:
    story = item['Story']
    if story.get('priority') == '4':  # High priority
        print(f\"{story['id']}: {story['name']}\")
"
```

### 示例 2: 创建需求

```python
from scripts.tapd_oauth_client import TapdOAuthClient

client = TapdOAuthClient()

new_story = client.create_story(
    name="【新功能】实现用户登录",
    description="需求描述：\n1. 支持邮箱登录\n2. 支持手机号登录",
    priority="4"  # High
)

print(f"创建成功: {new_story['id']}")
```

### 示例 3: 批量更新需求状态

```python
client = TapdOAuthClient()

# 获取所有 planning 状态的需求
stories = client.get_stories(status="planning", limit=100)

# 批量更新为进行中
for story in stories:
    client.update_story(
        story_id=story['id'],
        status="status_3"  # 进行中
    )
```

## 🛠️ 脚本说明

### `scripts/tapd-api.sh`

Shell 命令行工具，支持快速查询。

**优点**:
- 简单易用
- 无需 Python 环境
- 适合快速查询

**限制**:
- 只读操作
- 无状态管理
- 每次都需要获取新 token

### `scripts/tapd_oauth_client.py`

Python 客户端库，支持完整功能。

**优点**:
- 完整 CRUD 支持
- Token 缓存和自动刷新
- 面向对象设计
- 错误处理完善

**推荐用法**:
- 复杂业务逻辑
- 批量操作
- 集成到其他 Python 项目

## 🔐 安全注意事项

### ⚠️ 敏感信息保护

1. **不要提交 tapd.json 到 Git**
   ```bash
   # .gitignore
   tapd.json
   tapd-*.json
   ```

2. **设置文件权限**
   ```bash
   chmod 600 tapd.json
   ```

3. **使用环境变量（可选）**
   ```bash
   export TAPD_CLIENT_ID="your-id"
   export TAPD_CLIENT_SECRET="your-secret"
   export TAPD_WORKSPACE_ID="12345678"
   ```

4. **定期更换密钥**
   - 定期在 TAPD 开放平台重置应用密钥
   - 更新 tapd.json

### 🔒 权限控制

- 只授予必要的应用权限
- 使用安全 IP 白名单（在 TAPD 开放平台设置）
- 监控 API 调用日志

## 📚 参考文档

- [TAPD 开放平台文档](https://open.tapd.cn/document/api-doc/)
- [OAuth 认证流程](https://open.tapd.cn/document/api-doc/API文档/授权凭证/项目态.html)
- [API 使用必读](https://open.tapd.cn/document/api-doc/API文档/使用必读.html)
- [完整 API 列表](https://open.tapd.cn/document/api-doc/API文档/)

## 🐛 故障排除

### 问题 1: 403 Forbidden

**原因**: OAuth 应用未被授权访问项目

**解决**:
1. 在 TAPD 项目设置中安装应用
2. 确认应用权限配置正确
3. 检查安全 IP 白名单

### 问题 2: access_token 过期

**症状**: 返回 401 Unauthorized

**解决**:
- Shell 脚本：每次都会重新获取 token
- Python 客户端：自动检测过期并刷新

### 问题 3: workspace_id 无效

**原因**: 配置的 workspace_id 不存在或无权限

**解决**:
1. 检查 URL 中的 workspace_id
2. 确认 OAuth 应用已安装到该项目
3. 使用 `/workspaces/projects` API 列出可访问的项目

## 📊 性能优化

### Token 缓存

Python 客户端会缓存 access_token：

```python
# Token 缓存到 ~/.tapd_token_cache.json
# 有效期内不会重复请求
```

### 批量请求

```python
# 批量获取（推荐）
stories = client.get_stories(limit=100)

# 逐个获取（不推荐）
for id in story_ids:
    story = client.get_story(id)  # 会触发多次 API 请求
```

### 并发限制

TAPD API 有频率限制，建议：
- 使用 `limit` 参数批量获取
- 添加请求间隔（0.1-0.5 秒）
- 缓存不常变化的数据

## 🔄 更新日志

---

**作者**: OpenClaw Community  
**许可**: MIT  
**支持**: https://github.com/openclaw/skills

# TAPD API Skill

完整的 TAPD API 集成，实现所有 TAPD API 模块。

## ✨ 特性

- ✅ **18 个完整模块** - 覆盖需求、任务、缺陷、迭代等所有功能
- ✅ **70+ API 方法** - 完整的 CRUD 操作和高级功能
- ✅ **独立配置** - 所有配置存储在 tapd.json，不依赖全局配置
- ✅ **双认证支持** - OAuth 和 Basic Auth 两种方式
- ✅ **自动化管理** - Token 缓存、自动刷新、错误处理
- ✅ **双接口设计** - Python SDK + Shell 命令行工具
- ✅ **美化界面** - 增强的命令行帮助和错误提示

## 📂 文件结构

```
tapd-api/
├── README.md                完整说明
├── SKILL.md                 详细文档
├── SECURITY.md              安全指南
├── scripts/
│   ├── tapd-api.sh          Shell 命令行工具 (2.6KB)
│   └── tapd_client.py       Python 完整 SDK (30KB)
└── reference/
    ├── config-example.md    配置示例
    └── examples.md          使用示例
```

## 📦 包含的模块

| 模块 | 功能 | 方法数 |
|------|------|--------|
| **Story** | 需求管理 | 14 |
| **Task** | 任务管理 | 7 |
| **Bug** | 缺陷管理 | 9 |
| **Iteration** | 迭代管理 | 5 |
| **Test** | 测试用例 | 10 |
| **Comment** | 评论管理 | 4 |
| **Wiki** | Wiki 管理 | 4 |
| **Timesheet** | 工时管理 | 4 |
| **Workspace** | 项目/成员 | 3 |
| **Workflow** | 工作流 | 1 |
| **Boardcard** | 看板工作项 | 3 |
| **Module** | 模块管理 | 4 |
| **Relation** | 关联关系 | 1 |
| **Release** | 发布计划 | 2 |
| **Version** | 版本管理 | 4 |
| **Role** | 角色管理 | 1 |
| **Launchform** | 发布评审 | 3 |

**总计**: 18 模块，70+ 方法

## 🚀 快速开始

### 1. 创建配置文件

```bash
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

# 使用
stories = client.story.list(
    workspace_id=default_workspace['id'],
    limit=10
)
```

### 3. Shell 命令行使用

```bash
# 设置环境变量
export TAPD_CLIENT_ID=$(cat tapd.json | jq -r '.oauth.clientId')
export TAPD_CLIENT_SECRET=$(cat tapd.json | jq -r '.oauth.clientSecret')
export TAPD_WORKSPACE_ID=$(cat tapd.json | jq -r '.workspace_id')

# 使用
./scripts/tapd-api.sh story list --limit 10
```

## ⚡ 快速参考

### 命令行快速查询

```bash
# 帮助信息
./scripts/tapd-api.sh

# 常用命令
./scripts/tapd-api.sh story list --limit 10     # 需求列表
./scripts/tapd-api.sh story count                # 需求计数
./scripts/tapd-api.sh bug list --status new      # 新缺陷
./scripts/tapd-api.sh task count                 # 任务统计
./scripts/tapd-api.sh workspace users            # 项目成员
```

### Python 快速使用

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

# 获取数据
stories = client.story.list(workspace_id=default_workspace['id'], limit=10)
bugs = client.bug.list(workspace_id=default_workspace['id'], status="new")

# 创建记录
new_story = client.story.create(
    workspace_id=default_workspace['id'],
    name="需求标题"
)
```

### 支持的模块

| 核心 | 扩展 | 高级 |
|------|------|------|
| story, task, bug | comment, wiki | boardcard, module |
| iteration, test | timesheet, workspace | relation, release |
| | workflow | version, role, launchform |

```json
{
  "integrations": {
    "tapd": {
      "clientId": "your-client-id",
      "clientSecret": "your-client-secret",
      "workspaces": [
        {
          "id": "12345678",
          "name": "项目名称",
          "default": true
        }
      ]
    }
  }
}
```

### 2. Shell 命令行使用

```bash
# 获取需求列表
./scripts/tapd-api.sh story list --limit 10

# 获取需求计数
./scripts/tapd-api.sh story count

# 获取缺陷列表
./scripts/tapd-api.sh bug list --status new --limit 20

# 获取任务列表
./scripts/tapd-api.sh task list --limit 5

# 获取项目成员
./scripts/tapd-api.sh workspace users

# 获取工作流状态
./scripts/tapd-api.sh workflow status_map
```

### 3. Python SDK 使用

```python
from scripts.tapd_client import TapdClient

# 初始化客户端（OAuth，自动从配置读取）
client = TapdClient(auth_type="oauth")

# 需求管理
stories = client.story.list(workspace_id="12345678", limit=10)
story_count = client.story.count(workspace_id="12345678")
new_story = client.story.create(
    workspace_id="12345678",
    name="需求标题",
    description="需求描述"
)

# 任务管理
tasks = client.task.list(workspace_id="12345678", status="open")
task_count = client.task.count(workspace_id="12345678")

# 缺陷管理
bugs = client.bug.list(workspace_id="12345678", status="new")
bug_count = client.bug.count(workspace_id="12345678")

# 迭代管理
iterations = client.iteration.list(workspace_id="12345678")

# 评论管理
comments = client.comment.list(
    workspace_id="12345678",
    entry_id="story_id",
    entry_type="story"
)

# 工时管理
timesheets = client.timesheet.list(workspace_id="12345678")

# Wiki 管理
wikis = client.wiki.list(workspace_id="12345678")

# 测试用例
test_cases = client.test.list(workspace_id="12345678")
test_plans = client.test.plans(workspace_id="12345678")

# 工作空间
projects = client.workspace.projects()
members = client.workspace.users(workspace_id="12345678")

# 看板
boardcards = client.boardcard.list(workspace_id="12345678")

# 发布计划
releases = client.release.list(workspace_id="12345678")

# 版本管理
versions = client.version.list(workspace_id="12345678")
```

## 📚 相关文档

详细文档请查看：

- [SKILL.md](./SKILL.md) - 完整的功能文档和使用指南
- [reference/examples.md](./reference/examples.md) - 丰富的使用示例
- [reference/config-example.md](./reference/config-example.md) - 配置说明
- [SECURITY.md](./SECURITY.md) - 安全配置指南

## 🔧 高级用法

### Basic Auth 方式

```python
client = TapdClient(
    auth_type="basic",
    api_user="your-api-user",
    api_password="your-api-password",
    workspace_id="12345678"
)
```

### 手动指定 OAuth 参数

```python
client = TapdClient(
    auth_type="oauth",
    client_id="your-client-id",
    client_secret="your-client-secret",
    workspace_id="12345678"
)
```

### 命令行完整用法

```bash
# 查看帮助
./scripts/tapd-api.sh

# 指定工作空间
./scripts/tapd-api.sh story list --workspace 87654321 --limit 20

# 过滤查询
./scripts/tapd-api.sh story list --status planning --limit 50

# 创建需求（需要修改脚本支持更多参数）
python3 scripts/tapd_client.py story create \
  --workspace 12345678 \
  --name "新需求标题"
```

## 🎯 核心功能

### 需求管理 (Story)

- `list()` - 获取需求列表
- `count()` - 需求计数
- `create()` - 创建需求
- `update()` - 更新需求
- `custom_fields_settings()` - 自定义字段配置
- `get_link_stories()` - 需求关联关系
- `changes()` - 变更历史
- `changes_count()` - 变更次数
- `categories()` - 需求分类
- `categories_count()` - 分类数量
- `get_story_tcase()` - 测试用例关联
- `update_select_field_options()` - 更新下拉字段
- `get_fields_info()` - 所有字段信息

### 任务管理 (Task)

- `list()` - 获取任务列表
- `count()` - 任务计数
- `create()` - 创建任务
- `update()` - 更新任务
- `custom_fields_settings()` - 自定义字段配置
- `changes()` - 变更历史
- `changes_count()` - 变更次数

### 缺陷管理 (Bug)

- `list()` - 获取缺陷列表
- `count()` - 缺陷计数
- `group_count()` - 缺陷统计
- `create()` - 创建缺陷
- `update()` - 更新缺陷
- `custom_fields_settings()` - 自定义字段配置
- `changes()` - 变更历史
- `changes_count()` - 变更次数
- `get_link_bugs()` - 缺陷关联关系

### 其他模块

查看 [SKILL.md](./SKILL.md) 了解所有模块的详细方法。

## 🔐 安全说明

- ⚠️ **不要**将 tapd.json 提交到 Git
- ⚠️ **不要**在代码中硬编码凭证
- ✅ **使用** tapd.json 或环境变量存储配置
- ✅ **设置**文件权限 `chmod 600 tapd.json`
- ✅ **定期**轮换 OAuth 密钥

详见 [SECURITY.md](./SECURITY.md)

## 🧪 测试

```bash
# 测试 OAuth 认证
python3 scripts/tapd_client.py story count

# 测试 Shell 工具
./scripts/tapd-api.sh story list --limit 5

# 测试所有模块
./scripts/tapd-api.sh story count
./scripts/tapd-api.sh task count
./scripts/tapd-api.sh bug count
```

## 📊 性能优化

- ✅ **Token 缓存** - access_token 自动缓存到 `~/.tapd_token_cache.json`
- ✅ **批量查询** - 使用 `limit` 参数批量获取数据
- ✅ **错误重试** - 内置错误处理和重试机制

---
name: yunxiao-mcp
description: 阿里云云效 MCP 操作工具。通过 MCP SSE 协议操作云效平台，支持项目管理、工作项管理、流水线管理、代码仓库等 165+ 工具。
---

# 云效 MCP Skill

阿里云云效（DevOps）MCP 操作工具，基于 MCP SSE 协议。MCP Server: `http://localhost:3000`

## 目录结构

```
yunxiao-mcp/
├── SKILL.md           # 本文件
├── DEPLOY.md          # MCP Server 部署与运维
└── client/            # Node.js MCP 客户端
    ├── package.json
    ├── examples/
    └── src/
        ├── client.mjs # MCP SSE 客户端核心
        ├── cli.mjs    # 命令行接口
        └── index.mjs  # 模块导出
```

## 功能概览

通过 MCP Server 提供 **165+ 工具**，覆盖：

- **项目管理**: 项目查询、迭代管理、版本管理
- **工作项管理**: 需求、任务、缺陷的查询与操作
- **流水线管理**: 流水线创建、运行、日志查询
- **代码管理**: 仓库、分支、文件操作
- **部署管理**: 部署单、环境管理

## 快速开始

```bash
# 安装客户端
cd client && npm install

# 确保 MCP Server 运行（未运行参考 DEPLOY.md）
docker ps --filter "name=yunxiao-mcp"
```

## 命令速查

```bash
# 在项目 client 目录下执行以下命令

# 查看所有工具（Markdown 表格，省 token）
node src/cli.mjs list

# 查看某个工具的参数定义（JSON，含 inputSchema）
node src/cli.mjs schema get_current_user

# 当前用户
node src/cli.mjs call get_current_user

# 当前企业信息
node src/cli.mjs call get_current_organization_info

# 搜索项目
node src/cli.mjs call search_projects '{"organizationId": "<org_id>", "perPage": 20}'

# 搜索需求
node src/cli.mjs call search_workitems '{"organizationId": "<org_id>", "spaceId": "<project_id>", "category": "Req", "perPage": 20}'

# 搜索 Bug
node src/cli.mjs call search_workitems '{"organizationId": "<org_id>", "spaceId": "<project_id>", "category": "Bug", "perPage": 20}'

# 获取版本列表
node src/cli.mjs call list_versions '{"organizationId": "<org_id>", "id": "<project_id>", "perPage": 20}'

# 从 stdin 传递大参数
echo '{"organizationId": "<org_id>"}' | node src/cli.mjs call search_projects --stdin
```

### 典型 AI agent 调用流程

```bash
# 1. 浏览工具列表（Markdown 表格，低 token）
node src/cli.mjs list

# 2. 获取目标工具参数定义（JSON，按需获取）
node src/cli.mjs schema search_workitems

# 3. 执行调用（JSON 结果）
node src/cli.mjs call search_workitems '{"organizationId":"xxx","spaceId":"yyy","category":"Req"}'
```

## 常用工具速查

### 项目管理

| 工具名 | 说明 |
|--------|------|
| `search_projects` | 搜索项目列表 |
| `get_project` | 获取项目详情 |
| `list_versions` | 获取版本列表 |
| `list_sprints` | 获取迭代列表 |

### 工作项管理

| 工具名 | 说明 |
|--------|------|
| `search_workitems` | 搜索工作项（需求/Bug/任务） |
| `get_work_item` | 获取工作项详情 |
| `create_work_item` | 创建工作项 |
| `update_work_item` | 更新工作项 |

### 流水线管理

| 工具名 | 说明 |
|--------|------|
| `list_pipelines` | 获取流水线列表 |
| `get_pipeline` | 获取流水线详情 |
| `create_pipeline_run` | 运行流水线 |
| `get_pipeline_run` | 获取运行记录 |

### 代码管理

| 工具名 | 说明 |
|--------|------|
| `list_repositories` | 获取代码仓库列表 |
| `list_branches` | 获取分支列表 |
| `get_file_blobs` | 获取文件内容 |
| `create_file` | 创建文件 |

## 参数说明

### 必填参数

| 参数 | 说明 |
|------|------|
| `organizationId` | 企业 ID，可通过 `get_current_organization_info` 获取 |
| `spaceId` | 项目 ID |
| `category` | 工作项类型，取值见下表 |

### 工作项类型 (category)

| 值 | 说明 |
|----|------|
| `Req` | 需求 |
| `Bug` | 缺陷 |
| `Task` | 任务 |
| `Risk` | 风险 |
| `Topic` | 主题 |
| `Request` | 诉求 |

## Node.js API 使用

```js
import { createClient } from './src/index.mjs';

const client = await createClient('http://localhost:3000');
const result = await client.callTool('search_workitems', {
  organizationId: '<org_id>',
  spaceId: '<project_id>',
  category: 'Req',
  perPage: 10,
});
console.log(JSON.stringify(result));
await client.close();
```

## 相关资源

- MCP Server 部署与运维: [DEPLOY.md](./DEPLOY.md)
- 云效官方文档: https://help.aliyun.com/zh/yunxiao/
- MCP 协议: https://modelcontextprotocol.io/

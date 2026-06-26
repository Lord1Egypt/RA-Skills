---
name: yunxiao
description: Use when needing to query or update Yunxiao work items, comments, projects, or organization members from OpenClaw.
---

# 云效工作项 Skill

用于查询和操作云效工作项，包括需求、任务、缺陷、评论、项目与组织成员信息。

## 公开版约定

- 本文件只保留可公开的通用说明。
- 私有组织 ID、项目 ID、内部前缀和团队约定，统一记录在工作区本地的 `AGENTS.md`。
- 对外示例统一使用占位符，例如 `<orgId>`、`<projectId>`、`PROJ-12345`。

## 前置要求

- 已设置环境变量 `YUNXIAO_ACCESS_TOKEN`
- 可选设置 `YUNXIAO_ORG_ID`
- 如需在 Cursor 中直接使用，可在 `~/.cursor/mcp.json` 配置对应 MCP Server

## 环境变量

```bash
# 云效访问令牌（必填）
export YUNXIAO_ACCESS_TOKEN="<your-yunxiao-token>"

# 默认组织 ID（可选）
export YUNXIAO_ORG_ID="<your-org-id>"
```

## 组织 ID 获取顺序

脚本会按以下顺序确定 `organizationId`：

1. 命令行显式传入的 `[orgId]`
2. 环境变量 `YUNXIAO_ORG_ID`
3. `get_organizations` 返回的第一个组织

如果你有内部默认组织或常用项目映射，把它们写到本地 `AGENTS.md`，不要写进公开 skill。

## MCP 配置示例

```json
{
  "mcpServers": {
    "yunxiao": {
      "command": "npx",
      "args": ["-y", "alibabacloud-devops-mcp-server"],
      "env": {
        "YUNXIAO_ACCESS_TOKEN": "<your-token>"
      }
    }
  }
}
```

## 功能列表

### 1. 获取组织列表

```bash
node scripts/yunxiao-mcp.cjs get_organizations
```

### 2. 获取当前用户信息

```bash
node scripts/yunxiao-mcp.cjs get_current_user [orgId]
```

### 3. 搜索项目

```bash
node scripts/yunxiao-mcp.cjs search_projects [keyword] [orgId]
```

示例输出：

```json
[
  {
    "id": "project-id-1",
    "name": "示例项目",
    "customCode": "PROJ",
    "status": { "name": "进行中" }
  }
]
```

### 4. 获取工作项详情

```bash
node scripts/yunxiao-mcp.cjs get_work_item <workItemId> [orgId]
```

示例输出：

```json
{
  "id": "work-item-id",
  "serialNumber": "PROJ-12345",
  "subject": "示例需求标题",
  "status": { "name": "处理中" },
  "assignedTo": { "name": "负责人A", "id": "user-id-1" },
  "creator": { "name": "创建人A", "id": "user-id-2" },
  "participants": [{ "name": "参与人A", "id": "user-id-3" }],
  "customFieldValues": []
}
```

### 5. 搜索工作项

```bash
node scripts/yunxiao-mcp.cjs search_workitems <spaceId> [optionsJson] [orgId]
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `spaceId` | 是 | 项目 ID，可通过 `search_projects` 获取 |
| `optionsJson` | 否 | JSON 格式搜索选项 |
| `orgId` | 否 | 显式指定组织 ID |

搜索选项：

| 字段 | 类型 | 说明 |
|------|------|------|
| `category` | string | 工作项类型：`req`、`task`、`bug`、`risk`、`epic` |
| `status` | string | 状态 ID 或状态名 |
| `assignedTo` | string | 指派人 ID，`self` 表示当前用户 |
| `creator` | string | 创建人 ID，`self` 表示当前用户 |
| `subject` | string | 标题关键词 |
| `sprint` | string | 迭代 ID |
| `page` | number | 页码，默认 `1` |
| `perPage` | number | 每页条数，默认 `20`，最大 `200` |
| `includeDetails` | boolean | 是否包含详情，默认 `false` |
| `orderBy` | string | 排序字段 |
| `sort` | string | 排序方向：`desc` 或 `asc` |

常用示例：

```bash
# 搜索项目中的所有需求
node scripts/yunxiao-mcp.cjs search_workitems "<projectId>"

# 搜索待处理的需求
node scripts/yunxiao-mcp.cjs search_workitems "<projectId>" '{"status":"pending_processing"}'

# 搜索指派给我的工作项
node scripts/yunxiao-mcp.cjs search_workitems "<projectId>" '{"assignedTo":"self"}'

# 搜索缺陷
node scripts/yunxiao-mcp.cjs search_workitems "<projectId>" '{"category":"bug"}'

# 分页搜索
node scripts/yunxiao-mcp.cjs search_workitems "<projectId>" '{"perPage":50,"page":1}'
```

示例输出：

```json
{
  "items": [
    {
      "id": "work-item-id",
      "serialNumber": "PROJ-12345",
      "subject": "示例工作项",
      "status": { "name": "待处理", "id": "100005" },
      "assignedTo": { "name": "负责人A", "id": "user-id-1" },
      "creator": { "name": "创建人A", "id": "user-id-2" },
      "workitemType": { "name": "产品需求" }
    }
  ],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 1,
    "totalPages": 1
  }
}
```

### 6. 获取工作项评论

```bash
node scripts/yunxiao-mcp.cjs get_comments <workItemId> [orgId] [page] [perPage]
```

示例输出：

```json
[
  {
    "id": "comment-id",
    "content": "评论内容示例",
    "contentFormat": "RICHTEXT",
    "user": { "name": "评论人A", "id": "user-id-1" },
    "gmtCreate": 1767843788000,
    "gmtModified": 1767843788000
  }
]
```

### 7. 创建工作项评论

```bash
node scripts/yunxiao-mcp.cjs create_comment <workItemId> <content> [orgId]
```

### 8. 搜索组织成员

```bash
node scripts/yunxiao-mcp.cjs search_members <keyword> [orgId]
```

## 命令速查

```bash
node scripts/yunxiao-mcp.cjs <command> [args...]

get_organizations
get_current_user [orgId]
search_projects [keyword] [orgId]
get_work_item <workItemId> [orgId]
search_workitems <spaceId> [optionsJson] [orgId]
get_comments <workItemId> [orgId] [page] [perPage]
create_comment <workItemId> <content> [orgId]
search_members <keyword> [orgId]
```

## 使用场景

### 场景 1：查看某个工作项

```text
用户: 帮我看看云效需求 PROJ-12345
助手: 调用 get_work_item 获取详情并整理重点信息
```

### 场景 2：搜索待处理工作

```text
用户: 帮我看看某个项目有哪些待处理需求
助手:
1. 调用 search_projects 获取项目 ID
2. 调用 search_workitems 搜索待处理需求
3. 展示结果
```

### 场景 3：查看我的待办

```text
用户: 我在云效上有哪些待办？
助手:
1. 调用 search_projects 获取相关项目
2. 调用 search_workitems 搜索 assignedTo=self 的需求、任务或缺陷
3. 展示结果
```

### 场景 4：查看工作项评论

```text
用户: 看一下 PROJ-12345 的评论
助手: 调用 get_comments 获取评论列表
```

## 注意事项

1. 评论内容通常是富文本结构。
2. 大量结果建议结合 `page` 和 `perPage` 分页获取。
3. 如果需要内部默认组织、项目快捷名或前缀映射，请放在本地 `AGENTS.md`，不要写进公开文档。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Cannot determine organization ID` | 未显式提供组织 ID，且无法自动获取 | 设置 `YUNXIAO_ORG_ID`、传入 `[orgId]`，或先运行 `get_organizations` |
| `NotFound` | 工作项不存在或无权限 | 检查工作项 ID 和权限 |
| `Invalid spaceId` | 项目 ID 无效 | 使用 `search_projects` 获取正确的项目 ID |

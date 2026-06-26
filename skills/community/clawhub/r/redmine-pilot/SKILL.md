---
name: redmine
description: Redmine 项目管理系统 API 集成。用于：查询 Issue、创建 Issue、更新 Issue 状态、获取项目列表、搜索任务。当用户提到"项目管理"、"project"、"issue"、"任务"、"工单"、"Redmine"时触发此 Skill。
---

# Redmine API Skill

通过 Redmine REST API 管理项目和 Issue。

## 配置

在使用前，需要在 workspace 的 `TOOLS.md` 或环境变量中配置：

```
REDMINE_URL=https://your-redmine-server.com
REDMINE_API_KEY=your-api-key
```

## 核心功能

### 1. 查询 Issue 列表

```bash
# 基本查询
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issues.json?limit=25" | jq

# 按项目查询
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issues.json?project_id=PROJECT_ID" | jq

# 按状态查询 (open/closed/*)
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issues.json?status_id=open" | jq

# 指派给我的
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issues.json?assigned_to_id=me" | jq
```

### 2. 获取单个 Issue 详情

```bash
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issues/ISSUE_ID.json?include=journals,attachments" | jq
```

include 可选值：children, attachments, relations, changesets, journals, watchers

### 3. 创建 Issue

```bash
curl -s -X POST -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  -H "Content-Type: application/json" \
  "$REDMINE_URL/issues.json" \
  -d '{
    "issue": {
      "project_id": 1,
      "tracker_id": 1,
      "subject": "Issue 标题",
      "description": "Issue 描述",
      "priority_id": 2,
      "assigned_to_id": 123
    }
  }' | jq
```

### 4. 更新 Issue

```bash
curl -s -X PUT -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  -H "Content-Type: application/json" \
  "$REDMINE_URL/issues/ISSUE_ID.json" \
  -d '{
    "issue": {
      "status_id": 3,
      "notes": "更新备注"
    }
  }'
```

### 5. 获取项目列表

```bash
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/projects.json" | jq
```

### 6. 获取元数据

```bash
# 状态列表
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/issue_statuses.json" | jq

# 跟踪器列表
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/trackers.json" | jq

# 优先级列表
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/enumerations/issue_priorities.json" | jq

# 用户列表
curl -s -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
  "$REDMINE_URL/users.json" | jq
```

## 常用脚本

使用 `scripts/redmine.py` 进行操作：

```bash
# 查询我的 Issue
python3 scripts/redmine.py my-issues

# 查询项目 Issue
python3 scripts/redmine.py issues --project PROJECT_ID

# 获取 Issue 详情
python3 scripts/redmine.py get ISSUE_ID

# 创建 Issue
python3 scripts/redmine.py create --project PROJECT_ID --subject "标题" --description "描述"

# 更新 Issue 状态
python3 scripts/redmine.py update ISSUE_ID --status STATUS_ID --notes "备注"
```

## 分页

默认返回 25 条，最大 100 条：
- offset: 跳过的条数
- limit: 返回条数

响应包含 `total_count`, `offset`, `limit` 字段。

## 自定义字段

查询：`cf_X=value`（X 为自定义字段 ID）
创建/更新：

```json
{
  "issue": {
    "custom_fields": [
      {"id": 1, "value": "值1"}
    ]
  }
}
```

## 认证方式

1. API Key（推荐）：`X-Redmine-API-Key` Header
2. HTTP Basic Auth

## 错误处理

- 422: 验证错误
- 401: 认证失败
- 403: 权限不足
- 404: 资源不存在

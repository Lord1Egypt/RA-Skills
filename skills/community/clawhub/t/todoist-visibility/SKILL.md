---
name: todoist-visibility
description: 基于 Todoist 的任务可见性管理。用于创建、更新和追踪任务状态（进行中🟡、等待中🟠、已完成🟢），并记录进度评论。当用户提到 Todoist 任务管理、任务状态追踪、或需要使用 Todoist API 时触发。
---

# Todoist 任务可见性 Skill

基于 Todoist API 的任务管理工具，提供清晰的任务状态可视化。

## 功能

- 创建任务并设置状态 section
- 更新任务状态
- 添加进度评论
- 查询项目和任务

## 状态映射

| 状态 | Section | Emoji |
|------|---------|-------|
| in_progress | 进行中 | 🟡 |
| waiting | 等待中 | 🟠 |
| done | 已完成 | 🟢 |

## 配置

使用前需要设置环境变量：

```bash
# Todoist API Token
export TODOIST_TOKEN="your-api-token"

# 项目 ID
export TODOIST_PROJECT_ID="your-project-id"

# Section IDs（需要在 Todoist 中创建对应的 section）
export SECTION_IN_PROGRESS="section-id-for-in-progress"
export SECTION_WAITING="section-id-for-waiting"
export SECTION_DONE="section-id-for-done"
```

## 脚本使用

### 1. todoist_api.sh - 通用 API 封装

```bash
# 获取所有项目
./scripts/todoist_api.sh GET projects

# 获取项目的 sections
./scripts/todoist_api.sh GET "sections?project_id=123"

# 获取项目的任务
./scripts/todoist_api.sh GET "tasks?project_id=123"

# 创建任务
./scripts/todoist_api.sh POST tasks '{"content": "新任务", "project_id": "123"}'
```

### 2. sync_task.sh - 任务同步

```bash
# 创建进行中的任务
./scripts/sync_task.sh create '{
  "content": "完成任务",
  "description": "任务详细描述",
  "status": "in_progress"
}'

# 更新任务状态为已完成
./scripts/sync_task.sh update '{"status": "done"}' 12345

# 更新任务状态为等待中
./scripts/sync_task.sh update '{"status": "waiting"}' 12345
```

### 3. add_comment.sh - 添加进度评论

```bash
# 添加进度日志
./scripts/add_comment.sh 12345 "已完成数据收集"

# 记录问题和进度
./scripts/add_comment.sh 12345 "遇到问题：API 超时，正在重试"
```

## 工作流程

对于复杂任务：

1. **创建任务** - 在"进行中"状态创建任务，描述中包含完整计划
2. **记录进度** - 每完成一个子步骤，调用 `add_comment.sh` 记录
3. **更新状态** - 根据需要移动任务到"等待中"或"已完成"

## 获取配置信息

### 获取 API Token

1. 访问 [Todoist Settings](https://todoist.com/app/settings/integrations/developer)
2. 复制 API Token

### 获取项目 ID

```bash
# 列出所有项目
./scripts/todoist_api.sh GET projects | jq '.[] | {id, name}'
```

### 创建 Sections 并获取 ID

在 Todoist 项目中创建三个 section：
- 🟡 In Progress
- 🟠 Waiting
- 🟢 Done

然后获取 section IDs：

```bash
# 列出项目的所有 sections
./scripts/todoist_api.sh GET "sections?project_id=YOUR_PROJECT_ID" | jq '.[] | {id, name}'
```

## 注意事项

- 所有脚本需要 `curl` 和 `jq` 工具
- 环境变量需要在会话中持久化保存
- API 有速率限制，避免频繁调用

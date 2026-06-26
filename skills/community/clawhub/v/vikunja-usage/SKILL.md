---
name: vikunja-usage
description: "任务管理工具：通过 Vikunja REST API v1 创建项目、任务、标签和评论，支持任务搜索、过滤、完成状态切换。Requires: curl。读取 $VIKUNJA_TOKEN 环境变量或 $AGENT_WORKSPACE/config/.vikunja-token 文件获取 token，支持多 agent。"
metadata: {"openclaw":{"emoji":"📋","requires":{"anyBins":["curl"]}}}
---

# Vikunja Task Manager

Vikunja 是一个轻量开源任务管理工具，部署于 `http://localhost:3456`，REST API v1。

## 凭证（多 Agent 支持）

Token 支持两种读取方式（按优先级）：
1. **环境变量** `VIKUNJA_TOKEN`（推荐，适合 agent 运行时注入）
2. **Token 文件** `$AGENT_WORKSPACE/config/.vikunja-token`（每个 agent 有自己独立的 token 文件）

**获取 Token**：
```bash
RESP=$(curl -s -X POST http://localhost:3456/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"your-user","password":"your-pass"}')
TOKEN=$(echo "$RESP" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
echo "$TOKEN"
```

**存入 token 文件**（每个 agent 不同路径）：
```bash
mkdir -p "$AGENT_WORKSPACE/config"
echo "$TOKEN" > "$AGENT_WORKSPACE/config/.vikunja-token"
chmod 600 "$AGENT_WORKSPACE/config/.vikunja-token"
```

**读取 Token**：
```bash
get_token() {
  [ -n "$VIKUNJA_TOKEN" ] && { echo "$VIKUNJA_TOKEN"; return; }
  [ -f "$AGENT_WORKSPACE/config/.vikunja-token" ] && cat "$AGENT_WORKSPACE/config/.vikunja-token"
}
TOKEN=$(get_token)
```

**多 Agent 场景**：每个 agent 独立 login，token 互不干扰。Vikunja 本身 token 无过期时间，可长期使用。

## 项目（Projects）

```bash
# 列出项目
curl -s http://localhost:3456/api/v1/projects -H "Authorization: Bearer $TOKEN"

# 创建项目（PUT /projects）
curl -s -X PUT http://localhost:3456/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"项目名","description":""}'

# 获取项目
curl -s http://localhost:3456/api/v1/projects/{id} -H "Authorization: Bearer $TOKEN"

# 更新项目（POST）
curl -s -X POST http://localhost:3456/api/v1/projects/{id} \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"新标题"}'

# 删除项目
curl -s -X DELETE http://localhost:3456/api/v1/projects/{id} -H "Authorization: Bearer $TOKEN"
```

## 任务（Tasks）

**⚠️ 创建用 PUT /projects/{id}/tasks，更新用 POST /tasks/{id}**

```bash
# 在项目里创建任务（PUT，不是 POST）
curl -s -X PUT http://localhost:3456/api/v1/projects/{project_id}/tasks \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"任务标题","description":"描述","priority":2}'

# 更新任务（POST，不是 PUT）
curl -s -X POST http://localhost:3456/api/v1/tasks/{task_id} \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"done":true,"priority":3}'

# 列出所有任务
curl -s http://localhost:3456/api/v1/tasks -H "Authorization: Bearer $TOKEN"

# 搜索标题
curl -s "http://localhost:3456/api/v1/tasks?s=关键词" -H "Authorization: Bearer $TOKEN"

# 过滤（done=false 只显示未完成）
curl -s "http://localhost:3456/api/v1/tasks?filter=done%20%3D%20false" \
  -H "Authorization: Bearer $TOKEN"

# 列出某项目任务
curl -s http://localhost:3456/api/v1/projects/{project_id}/tasks \
  -H "Authorization: Bearer $TOKEN"

# 删除任务
curl -s -X DELETE http://localhost:3456/api/v1/tasks/{id} -H "Authorization: Bearer $TOKEN"
```

## 评论（Comments）

```bash
# 添加评论（字段名是 comment，不是 text）
curl -s -X PUT http://localhost:3456/api/v1/tasks/{task_id}/comments \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"comment":"评论内容"}'

# 获取评论
curl -s http://localhost:3456/api/v1/tasks/{task_id}/comments \
  -H "Authorization: Bearer $TOKEN"
```

## 标签（Labels）

```bash
# 创建标签
curl -s -X PUT http://localhost:3456/api/v1/labels \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"in-progress","color":"#ff9900"}'

# 给任务打标签
curl -s -X PUT http://localhost:3456/api/v1/tasks/{task_id}/labels \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"labels": [{"id": 1}]}'
```

## 负责人（Assignees）

```bash
# 分配负责人
curl -s -X PUT http://localhost:3456/api/v1/tasks/{task_id}/assignees \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"user_id": 2}'

# 获取负责人
curl -s http://localhost:3456/api/v1/tasks/{task_id}/assignees \
  -H "Authorization: Bearer $TOKEN"
```

## 信息查询

```bash
# 服务信息（版本、功能开关）
curl -s http://localhost:3456/api/v1/info -H "Authorization: Bearer $TOKEN"
```

## Python 模板

```python
import requests, os

BASE = "http://localhost:3456/api/v1"
TOKEN_FILE = os.path.join(os.getenv("AGENT_WORKSPACE", "."), "config", ".vikunja-token")

def get_token():
    if os.getenv("VIKUNJA_TOKEN"):
        return os.getenv("VIKUNJA_TOKEN")
    with open(TOKEN_FILE) as f:
        return f.read().strip()

def headers():
    return {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}

def create_task(project_id, title, **kw):
    return requests.put(f"{BASE}/projects/{project_id}/tasks",
                        json={"title": title, **kw}, headers=headers()).json()

def update_task(task_id, **kw):
    return requests.post(f"{BASE}/tasks/{task_id}", json=kw, headers=headers()).json()

def search_tasks(q):
    return requests.get(f"{BASE}/tasks", params={"s": q}, headers=headers()).json()
```

## 已知坑

1. **创建任务用 PUT /projects/{id}/tasks**，不是 POST
2. **更新任务用 POST /tasks/{id}**，不是 PUT（PUT 报 405）
3. **评论字段是 `comment`**，不是 `text`
4. 批量创建 `POST /tasks/bulk` 文档有但实测不通，循环单条操作代替

## Agent Rules

- 先尝试从 `VIKUNJA_TOKEN` 环境变量读取 token；无则读 `$AGENT_WORKSPACE/config/.vikunja-token`
- Token 不硬编码，运行时从磁盘或环境变量读取
- 日志只含 metadata（操作类型、数量），无 token 值
- Token 文件权限 600
- Token 泄露后：重新 login 获取新 token 存入文件

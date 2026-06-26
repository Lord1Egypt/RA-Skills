---
name: xiaoba-interview-api
description: 通过小芭 AI 面试开放 API 创建面试计划、管理候选人、发起面试并获取面试结果。
homepage: https://www.ibaguo.com
metadata: {"openclaw":{"emoji":"🎤","requires":{"bins":["curl","jq"],"env":["XIAOBA_API_KEY"]},"primaryEnv":"XIAOBA_API_KEY","homepage":"https://www.ibaguo.com"}}
---

# 小芭 AI 面试开放 API（ibaguo）Skill

你可以用此 Skill 在你的工作流里调用小芭 AI 面试开放 API，完成：

- 面试计划（Interview Plans）：创建/生成/查询
- 候选人（Candidates）：创建/查询
- 面试会话（Sessions）：发起面试、获取面试结果

## 认证与基础信息

- Base URL：`https://www.ibaguo.com/api/v1`
- 认证方式：HTTP Header
  - `Authorization: Bearer <API_KEY>`
- 请将 API Key 放在环境变量 `XIAOBA_API_KEY` 中（不要把 Key 写进对话或日志）。

### 统一请求模板（bash + curl）

优先使用下面的模板发起请求（同时用 `jq` 美化输出）：

```bash
BASE_URL="https://www.ibaguo.com/api/v1"

# GET 示例
curl -sS "$BASE_URL/plans?limit=20&offset=0" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Accept: application/json" | jq

# POST 示例（JSON Body）
curl -sS "$BASE_URL/plans" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"name":"测试计划","questions":"自我介绍\\n项目经历\\n算法题","interview_style":"standard","job_title":"后端工程师","job_description":"负责核心服务开发","duration_minutes":15}' | jq
```

## 1) 面试计划（Interview Plans）

### 1.1 获取面试计划列表

- 方法：`GET`
- 路径：`/plans`
- Query 参数：
  - `limit`（可选，默认 20）
  - `offset`（可选）
  - `status`（可选）

```bash
curl -sS "$BASE_URL/plans?limit=20&offset=0&status=active" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Accept: application/json" | jq
```

### 1.2 创建面试计划

- 方法：`POST`
- 路径：`/plans`
- Body（JSON）字段（来自截图文档）：
  - `name`（必填）：计划名称
  - `questions`：面试问题文本（用换行分隔）
  - `job_title`：职位名称
  - `job_description`：职位描述
  - `interview_style`：`standard | strict | gentle`
  - `duration_minutes`：时长（分钟，示例为 15）

```bash
curl -sS "$BASE_URL/plans" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name":"后端工程师-一面",
    "questions":"自我介绍\\n项目经历\\n并发/锁\\n数据库索引\\n系统设计",
    "job_title":"后端工程师",
    "job_description":"负责核心服务开发与性能优化",
    "interview_style":"standard",
    "duration_minutes":15
  }' | jq
```

### 1.3 根据要求自动生成面试计划

- 方法：`POST`
- 路径：`/plans/generate`
- Body（JSON）字段：
  - `requirements`（必填）：岗位/能力要求描述
  - `count`：题目数量（示例为 5）

```bash
curl -sS "$BASE_URL/plans/generate" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"requirements":"后端工程师，熟悉 Java/Spring，MySQL，Redis，具备高并发经验","count":5}' | jq
```

## 2) 候选人（Candidates）

### 2.1 获取候选人列表

- 方法：`GET`
- 路径：`/candidates`

```bash
curl -sS "$BASE_URL/candidates" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Accept: application/json" | jq
```

### 2.2 创建候选人

- 方法：`POST`
- 路径：`/candidates`
- Body（JSON）字段：
  - `name`（必填）：候选人姓名
  - `phone`（必填）：手机号
  - `email`（可选）：邮箱
  - `plan_id`：面试计划 ID
  - `resume_data`：简历数据（JSON 对象）

```bash
curl -sS "$BASE_URL/candidates" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name":"张三",
    "phone":"13900139000",
    "email":"zhangsan@example.com",
    "plan_id":"c711d961-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }' | jq
```

> 备注：响应里通常会包含 `candidate.id` / `status`，以及面试链接（示例字段：`interview_url`）。

## 3) 面试会话（Sessions）

### 3.1 发起/调度面试

- 方法：`POST`
- 路径：`/sessions`
- Body（JSON）字段：
  - `plan_id`（必填）
  - `candidate_id`（必填）
  - `scheduled_at`：计划时间（ISO 8601）

```bash
curl -sS "$BASE_URL/sessions" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "plan_id":"c711d961-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "candidate_id":"2ead313b-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "scheduled_at":"2026-04-25T18:08:08Z"
  }' | jq
```

响应里会给出 `id`、`status`（如 `scheduled`）以及 `interview_url`（候选人打开即可开始面试）。

### 3.2 获取面试结果

- 方法：`GET`
- 路径：`/sessions/:id/result`

```bash
SESSION_ID="uuid-here"
curl -sS "$BASE_URL/sessions/$SESSION_ID/result" \
  -H "Authorization: Bearer $XIAOBA_API_KEY" \
  -H "Accept: application/json" | jq
```

结果中通常包含：
- `overall_score`（总分与等级）
- `detailed_analysis`（详细分析）
- `recommendations`（建议）
- `transcript`（对话记录）

## 推荐工作流（最常见）

1. `POST /plans` 或 `POST /plans/generate` 得到 `plan_id`
2. `POST /candidates` 创建候选人得到 `candidate_id`
3. `POST /sessions` 创建会话得到 `session_id` 与 `interview_url`
4. 面试结束后：`GET /sessions/:id/result` 拉取结果并整理

## 安全注意事项

- 不要在对话中输出 `XIAOBA_API_KEY` 或完整请求头。
- 若需要记录日志，仅记录 URL 路径、HTTP 方法、以及脱敏后的响应摘要。

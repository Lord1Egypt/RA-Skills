# Agent Memory API v3 参考文档

> 版本：8.8 | 基础路径：`/v1` | 协议：HTTP + SSE

## 目录

- [认证](#认证)
- [错误响应](#错误响应)
- [速率限制](#速率限制)
- [系统](#系统)
- [认证管理](#认证管理)
- [租户管理](#租户管理)
- [记忆操作](#记忆操作)
- [文档精读](#文档精读)
- [人格分析](#人格分析)
- [Spirit 管家](#spirit-管家)
- [联邦知识](#联邦知识)
- [好奇心引擎](#好奇心引擎)
- [知识验证](#知识验证)
- [分布式同步](#分布式同步)
- [流式事件](#流式事件)

---

## 认证

API 支持两种认证方式：

### JWT Bearer Token

在请求头中携带 JWT token：

```
Authorization: Bearer <access_token>
```

通过 `POST /v1/auth/token` 获取 token。

### API Key

在请求头中携带 API Key：

```
x-api-key: <your-api-key>
```

### 权限级别

| 权限 | 说明 |
|------|------|
| `read` | 读取记忆、搜索、查看状态 |
| `write` | 写入记忆、更新、删除 |
| `admin` | 管理租户、签发 token |

---

## 错误响应

所有错误遵循 [RFC 7807 Problem Details](https://tools.ietf.org/html/rfc7807) 格式：

```json
{
  "type": "about:blank",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body failed validation.",
  "instance": "http://localhost:8988/v1/memories",
  "errors": [
    {
      "loc": ["body", "content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 常见状态码

| 状态码 | 含义 |
|--------|------|
| 400 | 请求参数验证失败 |
| 401 | 未认证或 token 无效/过期 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如租户已存在） |
| 413 | 请求体过大 |
| 429 | 速率限制 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用（模块未加载） |

---

## 速率限制

- **限制**：每个租户 100 请求/分钟
- **适用路径**：`/v1/memories`、`/v1/recall`、`/v1/documents/*`
- **豁免路径**：`/v1/health`、`/v1/metrics`、`/v1/auth/token`

### 响应头

| 头部 | 说明 |
|------|------|
| `X-RateLimit-Remaining` | 剩余可用请求数 |
| `X-RateLimit-Limit` | 速率限制上限 |
| `Retry-After` | 超限后建议等待秒数（429 响应） |

### 查看速率限制状态

```bash
curl http://localhost:8988/v1/ratelimit-status \
  -H "Authorization: Bearer <token>"
```

---

## 系统

### GET /v1/health

健康检查，返回系统状态和统计信息。

**认证**：不需要

**响应** `HealthResponse`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 状态：`ok` |
| `version` | string | API 版本 |
| `memories` | int | 记忆总数 |
| `tenants` | int | 租户数量 |
| `timestamp` | int | 当前 Unix 时间戳 |
| `uptime_sec` | float | 运行时长（秒） |

```bash
curl http://localhost:8988/v1/health
```

### GET /v1/health/live

存活探针 — 进程是否存活。

**认证**：不需要

```bash
curl http://localhost:8988/v1/health/live
```

### GET /v1/health/ready

就绪探针 — 系统是否准备好服务请求。

**认证**：不需要

```bash
curl http://localhost:8988/v1/health/ready
```

### GET /v1/metrics

获取系统指标。

**认证**：不需要

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `fmt` | string | `prometheus` | 格式：`prometheus` 或 `json` |

```bash
# Prometheus 格式
curl http://localhost:8988/v1/metrics

# JSON 格式
curl "http://localhost:8988/v1/metrics?fmt=json"
```

### GET /v1/ratelimit-status

查看当前租户的速率限制状态。

**认证**：需要 `read` 权限

```bash
curl http://localhost:8988/v1/ratelimit-status \
  -H "Authorization: Bearer <token>"
```

---

## 认证管理

### POST /v1/auth/token

签发 JWT token。

**认证**：需要 `admin` 权限的 API Key 或 Bearer Token

**请求** `TokenRequest`：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tenant_id` | string | 是 | 租户 ID（1-128字符） |
| `agent_id` | string | 是 | Agent ID（1-128字符） |
| `permissions` | string[] | 否 | 权限列表，默认 `["read", "write"]` |
| `expiry_seconds` | int | 否 | Token 有效期（60-86400秒） |

**响应** `TokenResponse`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `access_token` | string | JWT access token |
| `token_type` | string | 固定 `bearer` |
| `expires_in` | int | 有效期（秒） |
| `tenant_id` | string | 租户 ID |
| `agent_id` | string | Agent ID |
| `permissions` | string[] | 授予的权限列表 |

```bash
curl -X POST http://localhost:8988/v1/auth/token \
  -H "Content-Type: application/json" \
  -H "x-api-key: <admin-api-key>" \
  -d '{
    "tenant_id": "team_alpha",
    "agent_id": "agent_001",
    "permissions": ["read", "write"],
    "expiry_seconds": 3600
  }'
```

---

## 租户管理

### POST /v1/tenants

创建租户。需要 `admin` 权限。

**请求** `CreateTenantRequest`：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tenant_id` | string | 是 | 唯一租户 ID（1-128字符） |
| `agent_id` | string | 否 | 初始管理员 Agent ID，默认 `admin` |
| `permissions` | string[] | 否 | 初始权限，默认 `["admin", "read", "write"]` |
| `metadata` | object | 否 | 租户元数据 |

**响应**（201）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tenant_id` | string | 租户 ID |
| `agent_id` | string | Agent ID |
| `permissions` | string[] | 权限列表 |
| `created_at` | float | 创建时间戳 |
| `access_token` | string | 自动签发的 token |

```bash
curl -X POST http://localhost:8988/v1/tenants \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin-token>" \
  -d '{
    "tenant_id": "team_alpha",
    "agent_id": "admin",
    "permissions": ["admin", "read", "write"]
  }'
```

### DELETE /v1/tenants/{tenant_id}

删除租户。需要 `admin` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `tenant_id` | string | 要删除的租户 ID |

```bash
curl -X DELETE http://localhost:8988/v1/tenants/team_alpha \
  -H "Authorization: Bearer <admin-token>"
```

---

## 记忆操作

### POST /v1/memories

写入一条记忆。需要 `write` 权限。

**请求** `WriteMemoryRequest`：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content` | string | 是 | 记忆内容（1-50000字符） |
| `importance` | string | 否 | 优先级：`high` / `medium` / `low`，默认 `medium` |
| `topics` | string[] | 否 | 主题标签列表 |
| `nature_code` | string | 否 | Nature 编码 |
| `tool_codes` | string[] | 否 | Tool 编码列表 |
| `knowledge_codes` | string[] | 否 | 知识类型编码列表 |
| `person_code` | string | 否 | 人格端口编码，默认 `main` |
| `visibility` | string | 否 | 可见性：`private` / `team` / `public`，默认 `team` |
| `ts` | float | 否 | Unix 时间戳覆盖 |

**响应**（201）`WriteMemoryResponse`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `memory_id` | string | 记忆 ID |
| `time_id` | string | 时间维度 ID |
| `person_id` | string | 人格维度 ID |
| `nature_id` | string | 性质维度 ID |
| `topics` | string[] | 主题标签 |
| `tools` | string[] | 工具标签 |
| `knowledge` | string[] | 知识类型标签 |
| `importance` | string | 优先级 |
| `task_id` | string | 任务 ID |
| `emotion` | object | 情感分析结果 |

**跳过响应**（200）：当记忆被过滤/去重时返回：

```json
{
  "memory_id": null,
  "skipped": true,
  "reason": "duplicate content"
}
```

```bash
curl -X POST http://localhost:8988/v1/memories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "content": "部署了v2.1版本，修复了登录Bug",
    "importance": "high",
    "topics": ["部署", "Bug修复"],
    "visibility": "team"
  }'
```

### POST /v1/recall

检索记忆。需要 `read` 权限。

**请求** `RecallRequest`：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 搜索查询文本（1-10000字符） |
| `top_k` | int | 否 | 返回结果数（1-100），默认 10 |
| `importance` | string | 否 | 按重要性过滤 |
| `topic_code` | string | 否 | 按主题编码过滤 |
| `nature_code` | string | 否 | 按性质编码过滤 |
| `person_id` | string | 否 | 按人格 ID 过滤 |
| `keyword` | string | 否 | 结构化关键词过滤 |
| `significance` | string | 否 | 按显著性过滤 |
| `time_from` | int | 否 | 起始时间戳 |
| `time_to` | int | 否 | 结束时间戳 |
| `team_id` | string | 否 | 团队 ID，默认 `default` |
| `limit` | int | 否 | 主结果最大数量（1-200），默认 20 |
| `semantic_weight` | float | 否 | 语义/结构化权重（0.0-1.0），默认 0.5 |

**响应** `RecallResponse`：

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | string | 原始查询 |
| `search_mode` | string | 搜索模式（hybrid/structured/semantic） |
| `total` | int | 结果总数 |
| `primary` | object[] | 主结果列表 |
| `related` | object[] | 关联结果（最多10条） |
| `causal_expansion` | object[] | 因果扩展结果 |
| `cultural_associations` | object[] | 文化关联结果 |
| `phonetic_similar` | object[] | 语音相似结果 |
| `intent` | string | 检测到的意图 |

```bash
curl -X POST http://localhost:8988/v1/recall \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "query": "部署",
    "top_k": 10,
    "semantic_weight": 0.7
  }'
```

### POST /v1/memory/batch

批量写入记忆。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `items` | object[] | 是 | 记忆列表（最多100条） |

**响应**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int | 提交总数 |
| `stored` | int | 成功存储数 |
| `results` | object[] | 每条记忆的写入结果 |

```bash
curl -X POST http://localhost:8988/v1/memory/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "items": [
      {"content": "第一条记忆", "importance": "high"},
      {"content": "第二条记忆", "importance": "low"}
    ]
  }'
```

### POST /v1/memory/{memory_id}/feedback

记录记忆反馈，支持持续学习。需要 `write` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `memory_id` | string | 记忆 ID |

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `feedback_type` | string | 是 | 反馈类型：`helpful` / `unhelpful` / `corrected` / `ignored` |
| `context` | object | 否 | 可选上下文（如 correction_id、query） |

```bash
curl -X POST http://localhost:8988/v1/memory/mem_abc123/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "feedback_type": "helpful",
    "context": {"query": "部署"}
  }'
```

---

## 文档精读

### POST /v1/documents/upload

上传文档并自动分段索引。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `content_b64` | string | 是 | Base64 编码的文件内容（最大50MB） |
| `filename` | string | 否 | 原始文件名（含扩展名） |
| `title` | string | 否 | 文档标题 |
| `importance` | string | 否 | 优先级，默认 `high` |
| `strategy` | string | 否 | 分段策略，默认 `auto` |

**响应**（201）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档 ID |
| `title` | string | 文档标题 |
| `source_type` | string | 来源类型 |
| `total_sections` | int | 总段落数 |
| `total_chunks` | int | 总分块数 |
| `indexed_chunks` | int | 已索引分块数 |
| `failed_chunks` | int | 失败分块数 |
| `total_vectors` | int | 总向量数 |
| `strategy_used` | string | 使用的分段策略 |
| `errors` | string[] | 错误列表 |

```bash
# 上传文件
BASE64=$(base64 -w0 document.pdf)
curl -X POST http://localhost:8988/v1/documents/upload \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d "{
    \"content_b64\": \"$BASE64\",
    \"filename\": \"document.pdf\",
    \"title\": \"项目文档\",
    \"importance\": \"high\"
  }"
```

### POST /v1/documents/text

直接索引文本内容。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | 是 | 文本内容（最大500000字符） |
| `title` | string | 否 | 文档标题 |
| `source_type` | string | 否 | 来源类型：`text` / `markdown` / `html`，默认 `text` |
| `importance` | string | 否 | 优先级，默认 `high` |
| `strategy` | string | 否 | 分段策略，默认 `auto` |

```bash
curl -X POST http://localhost:8988/v1/documents/text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "text": "# 项目说明\n\n这是一个重要的项目文档...",
    "title": "项目说明",
    "source_type": "markdown",
    "importance": "high"
  }'
```

### GET /v1/documents/{doc_id}

获取文档信息和所有分段。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档 ID |

```bash
curl http://localhost:8988/v1/documents/doc_abc123 \
  -H "Authorization: Bearer <token>"
```

### GET /v1/documents/{doc_id}/chunks

获取文档分段列表，可按章节/页码过滤。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档 ID |

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `chapter` | string | 按章节过滤 |
| `page` | int | 按页码过滤 |

```bash
curl "http://localhost:8988/v1/documents/doc_abc123/chunks?chapter=intro" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/documents/search

文档分段检索（支持向量+关键词+混合）。需要 `read` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 搜索查询 |
| `top_k` | int | 否 | 返回结果数，默认 5 |
| `expand_context` | int | 否 | 上下文扩展窗口，默认 1 |
| `doc_id` | string | 否 | 限定文档 ID |
| `strategy` | string | 否 | 检索策略，默认 `auto` |

```bash
curl -X POST http://localhost:8988/v1/documents/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "query": "部署流程",
    "top_k": 5,
    "expand_context": 1
  }'
```

### GET /v1/documents/{doc_id}/locate/{memory_id}

精准回溯 — 从 memory_id 定位到原文位置。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 文档 ID |
| `memory_id` | string | 记忆 ID |

```bash
curl http://localhost:8988/v1/documents/doc_abc123/locate/mem_xyz789 \
  -H "Authorization: Bearer <token>"
```

---

## 人格分析

### POST /v1/personality/analyze

分析聊天记录生成人格画像。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `chat_text` | string | 是 | 聊天记录文本 |
| `self_name` | string | 否 | 自己的昵称 |
| `source_type` | string | 否 | 数据源类型，默认 `wechat_txt` |
| `privacy_level` | string | 否 | 隐私级别，默认 `team` |

```bash
curl -X POST http://localhost:8988/v1/personality/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "chat_text": "聊天记录内容...",
    "self_name": "小明",
    "source_type": "wechat_txt"
  }'
```

### GET /v1/personality/{person_id}

获取人格画像。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `person_id` | string | 人物 ID |

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `access_level` | string | 访问级别，默认 `team` |

```bash
curl "http://localhost:8988/v1/personality/person_001?access_level=team" \
  -H "Authorization: Bearer <token>"
```

### GET /v1/personality/{person_id}/versions

获取人格画像版本历史。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/personality/person_001/versions \
  -H "Authorization: Bearer <token>"
```

### GET /v1/personality/{person_id}/evidence

获取人格特质推断的证据来源。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `trait` | string | 特质名称过滤 |

```bash
curl "http://localhost:8988/v1/personality/person_001/evidence?trait=外向" \
  -H "Authorization: Bearer <token>"
```

### DELETE /v1/personality/{person_id}

删除人格画像。需要 `write` 权限。

```bash
curl -X DELETE http://localhost:8988/v1/personality/person_001 \
  -H "Authorization: Bearer <token>"
```

---

## Spirit 管家

### GET /v1/spirit/health

Spirit 健康检查。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `fix` | bool | 是否自动修复问题，默认 `false` |

```bash
curl "http://localhost:8988/v1/spirit/health?fix=false" \
  -H "Authorization: Bearer <token>"
```

### GET /v1/spirit/daily-report

生成每日记忆报告。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `date` | string | 日期（YYYY-MM-DD 格式） |

```bash
curl "http://localhost:8988/v1/spirit/daily-report?date=2026-06-08" \
  -H "Authorization: Bearer <token>"
```

### GET /v1/spirit/weekly-report

生成每周记忆报告。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/spirit/weekly-report \
  -H "Authorization: Bearer <token>"
```

### GET /v1/spirit/awareness

查询知识感知度。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `topic` | string | 是 | 要查询的主题 |

```bash
curl "http://localhost:8988/v1/spirit/awareness?topic=部署" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/spirit/execute

执行 Spirit 自然语言命令。需要 `read` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `command` | string | 是 | 自然语言命令 |
| `confirm` | bool | 否 | 写操作是否需要确认，默认 `true` |

```bash
curl -X POST http://localhost:8988/v1/spirit/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "command": "清理30天前的低优先级记忆",
    "confirm": true
  }'
```

---

## 联邦知识

### GET /v1/federation/peers

列出联邦对等节点。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/federation/peers \
  -H "Authorization: Bearer <token>"
```

### POST /v1/federation/search

跨 Agent 联邦搜索。需要 `read` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 搜索查询 |
| `topics` | string[] | 否 | 主题过滤 |
| `max_per_peer` | int | 否 | 每个对等节点最大结果数（1-50），默认 5 |

```bash
curl -X POST http://localhost:8988/v1/federation/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "query": "部署流程",
    "topics": ["DevOps"],
    "max_per_peer": 5
  }'
```

### GET /v1/federation/conflicts

检测跨 Agent 知识冲突。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `topic` | string | 按主题过滤 |

```bash
curl "http://localhost:8988/v1/federation/conflicts?topic=部署" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/federation/resolve

解决知识冲突。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `topic` | string | 是 | 冲突主题 |
| `agent_a` | string | 是 | 第一个 Agent ID |
| `agent_a_claim` | string | 是 | 第一个 Agent 的主张 |
| `agent_b` | string | 是 | 第二个 Agent ID |
| `agent_b_claim` | string | 是 | 第二个 Agent 的主张 |
| `conflict_type` | string | 否 | 冲突类型，默认 `contradiction` |
| `strategy` | string | 否 | 解决策略：`higher_confidence` / `newer_wins` / `merged` / `both_kept` |
| `confidence_a` | float | 否 | Agent A 置信度，默认 0.5 |
| `confidence_b` | float | 否 | Agent B 置信度，默认 0.5 |

```bash
curl -X POST http://localhost:8988/v1/federation/resolve \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "topic": "部署流程",
    "agent_a": "agent_001",
    "agent_a_claim": "使用蓝绿部署",
    "agent_b": "agent_002",
    "agent_b_claim": "使用滚动更新",
    "strategy": "higher_confidence",
    "confidence_a": 0.8,
    "confidence_b": 0.6
  }'
```

---

## 好奇心引擎

### GET /v1/curiosity/targets

识别值得探索的主题。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `limit` | int | 最大返回数（1-50），默认 10 |

```bash
curl "http://localhost:8988/v1/curiosity/targets?limit=10" \
  -H "Authorization: Bearer <token>"
```

### GET /v1/curiosity/suggestions

获取建议查询以填补知识空白。需要 `read` 权限。

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `limit` | int | 最大返回数（1-20），默认 5 |

```bash
curl "http://localhost:8988/v1/curiosity/suggestions?limit=5" \
  -H "Authorization: Bearer <token>"
```

### POST /v1/curiosity/explore

执行探索行动。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `topic` | string | 是 | 要探索的主题 |

```bash
curl -X POST http://localhost:8988/v1/curiosity/explore \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"topic": "微服务架构"}'
```

---

## 知识验证

### POST /v1/validation/validate/{memory_id}

验证单条记忆 — 交叉引用、陈旧度、置信度衰减。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `memory_id` | string | 记忆 ID |

```bash
curl -X POST http://localhost:8988/v1/validation/validate/mem_abc123 \
  -H "Authorization: Bearer <token>"
```

### POST /v1/validation/validate-all

验证所有记忆并返回摘要。需要 `read` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | int | 否 | 最大验证数量，默认 100 |

```bash
curl -X POST http://localhost:8988/v1/validation/validate-all \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"limit": 100}'
```

---

## 分布式同步

### GET /v1/sync/peers

列出所有同步对等节点。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/sync/peers \
  -H "Authorization: Bearer <token>"
```

### POST /v1/sync/with/{peer_id}

与指定对等节点同步。需要 `write` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `peer_id` | string | 对等节点 ID |

```bash
curl -X POST http://localhost:8988/v1/sync/with/peer_node_1 \
  -H "Authorization: Bearer <token>"
```

### POST /v1/sync/all

与所有对等节点同步。需要 `write` 权限。

```bash
curl -X POST http://localhost:8988/v1/sync/all \
  -H "Authorization: Bearer <token>"
```

### POST /v1/sync/apply

使用 CRDT 合并应用远程变更。需要 `write` 权限。

**请求**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `changes` | list | 是 | 远程变更列表 |

```bash
curl -X POST http://localhost:8988/v1/sync/apply \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"changes": [...]}'
```

### GET /v1/sync/checkpoint

创建同步检查点用于恢复。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/sync/checkpoint \
  -H "Authorization: Bearer <token>"
```

### GET /v1/sync/stats

获取同步引擎统计信息。需要 `read` 权限。

```bash
curl http://localhost:8988/v1/sync/stats \
  -H "Authorization: Bearer <token>"
```

---

## 流式事件

### GET /v1/events/{tenant_id}

SSE 流式推送实时记忆事件。需要 `read` 权限。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `tenant_id` | string | 租户 ID |

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `event_types` | string | 逗号分隔的事件类型过滤 |

**限制**：最大 100 个并发 SSE 连接。

**事件类型**：
- `memory.created` — 记忆创建
- `memory.recalled` — 记忆检索
- `team.shared` — 团队共享事件

```bash
curl -N http://localhost:8988/v1/events/team_alpha \
  -H "Authorization: Bearer <token>"
```

---

## 启动服务

```bash
# 默认启动
uvicorn agent_memory.api_v3:app --host 127.0.0.1 --port 8988

# 自定义参数
python -m agent_memory.api_v3 \
  --host 0.0.0.0 \
  --port 8988 \
  --db /data/memory.db \
  --jwt-secret "your-secret-key" \
  --log-level INFO
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AGENT_MEMORY_JWT_SECRET` | — | JWT 签名密钥（生产环境必填） |
| `AGENT_MEMORY_TOKEN_EXPIRY` | `3600` | Token 有效期（秒） |
| `AGENT_MEMORY_CORS_ORIGINS` | `*` | CORS 允许的来源（逗号分隔） |
| `AGENT_MEMORY_ENV` | `production` | 运行环境 |
| `AGENT_MEMORY_ALLOW_INSECURE` | — | 允许不安全模式（开发用） |

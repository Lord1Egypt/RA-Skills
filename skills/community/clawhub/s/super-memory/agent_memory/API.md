# Agent Memory API Reference

完整 API 参考：HTTP 端点 + Python 接口 + 各模块详细说明。

> 快速接入和架构概览请见 [README.md](README.md)。

---

## API 版本策略

本项目提供三个 HTTP API 版本，各版本状态和定位如下：

| 版本 | 入口文件 | 端口 | 状态 | 说明 |
|------|---------|------|------|------|
| **v1** | `server.py` | 8976 | **stable** | 纯 stdlib HTTP 服务，零外部依赖，适合轻量部署和开发调试 |
| **v2** | `api_v2.py` | 8978 | **deprecated** | FastAPI + Pydantic，RFC 7807 错误格式，不再积极维护，建议迁移至 v3 |
| **v3** | `api_v3.py` | 8988 | **active** | FastAPI 异步 + SSE + 多租户隔离 + JWT/API Key 双认证，推荐生产使用 |

### 版本选择建议

- **新项目**：直接使用 **v3**（`api_v3.py`），获得多租户、异步、SSE 等完整功能
- **轻量/嵌入式**：使用 **v1**（`server.py`），无 FastAPI 依赖，单文件部署
- **v2 用户**：请迁移至 v3，v2 仅保留向后兼容，不再接受新功能

### 启动命令

```bash
# v1 (stable)
python3 server.py --api-key mysecret

# v2 (deprecated)
uvicorn agent_memory.api_v2:app --host 127.0.0.1 --port 8978

# v3 (active, 推荐)
uvicorn agent_memory.api_v3:app --host 0.0.0.0 --port 8988
```

---

## 错误码汇总

### HTTP 状态码

| HTTP 状态码 | 含义 | 触发场景 |
|------------|------|---------|
| 200 | 成功 | 所有成功请求 |
| 201 | 创建成功 | `POST /remember` 写入记忆 |
| 204 | 无内容 | 删除操作成功 |
| 400 | 请求错误 | 参数缺失/格式错误/内容超长 |
| 401 | 未认证 | 缺少认证头或 Token 无效（v2/v3） |
| 403 | 权限不足 | API Key 角色不匹配、Agent ID 覆盖被拒、强制认证端点未提供 Key |
| 404 | 未找到 | 路径不存在、记忆 ID 不存在 |
| 429 | 请求过多 | 超出速率限制（v2/v3 token bucket） |
| 500 | 服务器内部错误 | 未预期异常 |
| 503 | 服务不可用 | SSE 客户端数达上限、服务过载 |

### 业务错误码（v2/v3 RFC 7807 格式）

| 错误码 | HTTP 状态 | 说明 |
|--------|----------|------|
| `AUTH_MISSING` | 401 | 缺少认证信息，需提供 `Authorization: Bearer <token>` 或 `X-API-Key` |
| `AUTH_INVALID` | 401 | 认证凭证无效（Token 签名错误 / API Key 不存在） |
| `TOKEN_EXPIRED` | 401 | JWT Token 已过期 |
| `INSUFFICIENT_PERMISSIONS` | 403 | 当前角色无权执行此操作 |
| `FORBIDDEN` | 403 | 访问被拒绝（Agent ID 绑定冲突等） |

### v1 (server.py) 错误消息

| 错误消息 | HTTP 状态 | 说明 |
|---------|----------|------|
| `unauthorized` | 401 | 缺少或无效的 API Key |
| `content is required` | 400 | 写入请求缺少 content 字段 |
| `content too long: N chars (max 50000)` | 400 | 单条内容超长 |
| `query is required` | 400 | recall 请求缺少 query |
| `query too long: N chars (max 10000)` | 400 | 查询超长 |
| `messages array is required` | 400 | batch 请求缺少 messages |
| `too many messages: N (max 50)` | 400 | 批量写入超限 |
| `memory_id is required` | 400 | feedback/update 缺少 memory_id |
| `Write endpoint requires API Key authentication` | 403 | 写入端点强制要求 API Key |
| `Insufficient permissions (role: X)` | 403 | 角色权限不足 |
| `Agent ID override not authorized` | 403 | API Key 绑定的 Agent ID 与请求不一致 |
| `SSE client limit reached` | 503 | SSE 连接数达上限 |
| `memory not found or no version history` | 404 | 记忆不存在 |

### Python 异常层级

| 异常类 | 父类 | 说明 |
|--------|------|------|
| `MemoryError` | `Exception` | 所有 agent_memory 异常的基类 |
| `StorageError` | `MemoryError` | 数据库/存储操作失败 |
| `MemoryNotFoundError` | `MemoryError` | 请求的 memory_id 不存在 |
| `DuplicateMemoryError` | `MemoryError` | 重复内容/哈希冲突 |
| `FilterRejectedError` | `MemoryError` | 内容被过滤器拒绝 |
| `DeduplicationError` | `MemoryError` | 去重检查失败 |
| `CooldownError` | `MemoryError` | 主题写入冷却中 |
| `AuthenticationError` | `MemoryError` | 认证失败 |
| `MemoryPermissionError` | `MemoryError` | 权限不足 |
| `ValidationError` | `MemoryError` | 输入校验失败 |
| `LLMError` | `MemoryError` | LLM 调用失败或超时 |
| `EmbeddingError` | `MemoryError` | 向量计算失败 |
| `SyncError` | `MemoryError` | 同步操作失败 |
| `FederationError` | `MemoryError` | 联邦操作失败 |
| `AgentMemoryError` | `Exception` | 用户友好错误基类（含 hint） |
| `DatabaseError` | `AgentMemoryError` | 数据库操作失败 |
| `ConfigurationError` | `AgentMemoryError` | 配置/设置错误 |
| `DependencyError` | `AgentMemoryError` | 缺少依赖包（含安装提示） |
| `PermissionDeniedError` | `AgentMemoryError` | 权限被拒 |
| `RateLimitError` | `AgentMemoryError` | 速率限制 |

---

## HTTP API — Memory-as-a-Service

启动服务：
```bash
python3 server.py                                    # 127.0.0.1:8976（仅本地，无认证仅限开发）
python3 server.py --api-key mysecret                  # 启用 API Key 认证
python3 server.py --port 9000 --api-key $MY_KEY       # 自定义端口 + 认证
AGENT_MEMORY_API_KEY=mysecret python3 server.py        # 环境变量方式
python3 server.py --host 127.0.0.1                    # 仅本地访问（默认）
python3 server.py --host 0.0.0.0 --api-key $MY_KEY    # 开放网络访问（必须配合 API Key）
python3 server.py --db /data/memory.db                # 自定义数据库路径
```

> ⚠️ **安全警告**：默认绑定 `127.0.0.1`（仅本地访问）。绑定 `0.0.0.0` 时**必须**设置 API Key，
> 否则服务将拒绝启动。export/maintain/batch/SSE 端点始终要求 API Key 认证。

### 认证

生产部署**必须**设置 API Key，否则所有端点完全裸奔。

#### JWT Secret 安全要求（v9.0.1+）

v9.0.1 起，JWT Secret 必须通过环境变量 `AGENT_MEMORY_JWT_SECRET` 显式设置：

```bash
# 必填：至少 32 字符的强密钥
export AGENT_MEMORY_JWT_SECRET="your-secret-key-at-least-32-characters-long"
```

**规则**：
- 未设置 `AGENT_MEMORY_JWT_SECRET` → 服务拒绝启动
- 设置但长度不足 32 字符 → 服务拒绝启动
- 开发环境可设置 `AGENT_MEMORY_ALLOW_INSECURE=1` 跳过检查（**切勿用于生产**）

```bash
# 开发模式（仅限本地开发）
export AGENT_MEMORY_JWT_SECRET="dev"
export AGENT_MEMORY_ALLOW_INSECURE=1
python3 server.py
```

#### Token 签发端点安全（v9.0.1+）

`POST /v1/auth/token` 端点现在要求请求方持有 **admin 角色** 的 API Key，防止未授权用户签发 JWT Token：

```bash
# 正确：使用 admin 角色 API Key 签发 Token
curl -X POST http://localhost:8976/v1/auth/token \
  -H "Authorization: Bearer admin-key" \
  -H "Content-Type: application/json"

# 错误：read/write 角色 API Key 将被拒绝（403）
curl -X POST http://localhost:8976/v1/auth/token \
  -H "Authorization: Bearer readonly-key"
```

#### CORS 配置（v9.0.1+）

默认 CORS 策略已从 `allow_origins=["*"]` 改为白名单模式：

```bash
# 通过环境变量配置 CORS 白名单（逗号分隔）
export AGENT_MEMORY_CORS_ORIGINS="http://localhost:3000,http://localhost:8080"

# 未配置时仅允许 127.0.0.1 和 localhost
```

#### AGENT_MEMORY_ALLOW_INSECURE 开发模式

| 环境变量 | 值 | 效果 |
|----------|------|------|
| `AGENT_MEMORY_ALLOW_INSECURE` | `1` / `true` / `yes` | 跳过 JWT Secret 长度检查，允许弱密钥启动 |
| （未设置） | — | 强制执行 JWT Secret 最小 32 字符要求 |

> ⚠️ **安全警告**：`AGENT_MEMORY_ALLOW_INSECURE` 仅用于本地开发环境。生产环境设置此变量将导致严重安全风险。

#### API Key 配置

```bash
# 方式 1: CLI 参数（默认 admin 角色）
python3 server.py --api-key "your-secret-key"

# 方式 2: 角色分离的 API Key
python3 server.py --api-key "readonly-key:read"             # 只读角色
python3 server.py --api-key "readwrite-key:write"            # 读写角色
python3 server.py --api-key "admin-key:admin"                # 管理员角色

# 方式 3: 角色分离 + Agent ID 绑定（推荐多 Agent 场景）
python3 server.py --api-key "readkey:read:agent-01"          # 只读 + 绑定 agent-01
python3 server.py --api-key "writekey:write:agent-02"        # 读写 + 绑定 agent-02
python3 server.py --api-key "adminkey:admin:_system"         # 管理员 + 可跨 Agent 操作

# 方式 4: 环境变量
export AGENT_MEMORY_API_KEY="your-secret-key"
export AGENT_MEMORY_API_KEY_READ="readonly-key:agent-01"     # 只读 + 绑定 agent-01
export AGENT_MEMORY_API_KEY_WRITE="readwrite-key:agent-02"   # 读写 + 绑定 agent-02
python3 server.py
```

**角色权限**：

| 角色 | 读取端点 | 写入端点 | 管理端点 |
|------|----------|----------|----------|
| `read` | ✅ recall, context, stats, graph | ❌ | ❌ |
| `write` | ✅ | ✅ remember, feedback | ❌ |
| `admin` | ✅ | ✅ | ✅ maintain, export |

请求时通过 Header 传递：
```bash
curl -X POST http://localhost:8976/remember \
  -H "Authorization: Bearer readwrite-key" \
  -H "Content-Type: application/json" \
  -d '{"content": "test"}'

# 或使用 X-API-Key header
curl http://localhost:8976/stats -H "X-API-Key: readonly-key"
```

`/health` 和 `/` 无需认证（方便探活和监控）。

### 端点认证级别

| 端点 | 认证要求 | 说明 |
|------|----------|------|
| `GET /` | 无需认证 | API 文档 |
| `GET /health` | 无需认证 | 健康检查 |
| `POST /remember` | **强制 API Key** | 单条写入，即使未配置 API Key 也返回 403 |
| `POST /remember/batch` | **强制 API Key** | 批量写入，即使未配置 API Key 也返回 403 |
| `POST /recall` | API Key（如已配置） | 检索 |
| `GET /context` | API Key（如已配置） | 上下文组装 |
| `GET /stream` | **强制 API Key** | SSE 流，即使未配置 API Key 也返回 403 |
| `POST /feedback` | **强制 API Key** | 反馈，即使未配置 API Key 也返回 403 |
| `GET /stats` | API Key（如已配置） | 统计 |
| `GET /export` | **强制 API Key** | 导出，即使未配置 API Key 也返回 403 |
| `GET /graph` | API Key（如已配置） | 图谱 |
| `POST /maintain` | **强制 API Key** | 维护，即使未配置 API Key 也返回 403 |

### Agent 身份标识

多 Agent 场景下，通过 `X-Agent-ID` 请求头标识调用方身份：

```bash
curl -X POST http://localhost:8976/remember \
  -H "Authorization: Bearer your-secret-key" \
  -H "X-Agent-ID: my-agent-01" \
  -H "Content-Type: application/json" \
  -d '{"content": "test"}'
```

- 写入操作：`X-Agent-ID` 自动作为 `owner_agent_id`（除非请求体显式指定）
- 读取操作：`X-Agent-ID` 自动作为 `query_agent_id` 过滤范围（除非参数显式指定）
- 未提供时默认为 `_anonymous`
- `owner_agent_id` 为 `_system` 的记忆对所有 Agent 可见

**v8.3 安全：Agent ID 与 API Key 绑定**

API Key 支持绑定到特定 Agent ID，防止身份冒充：

```bash
# 绑定 Agent ID 的 API Key（格式: key:role:agent_id）
python3 server.py --api-key "readkey:read:agent-01"     # 只读 + 绑定 agent-01
python3 server.py --api-key "writekey:write:agent-02"   # 读写 + 绑定 agent-02
python3 server.py --api-key "adminkey:admin:_system"    # 管理员 + 可跨 Agent 操作

# 环境变量方式（格式: key:agent_id）
export AGENT_MEMORY_API_KEY_READ="readkey:agent-01"
export AGENT_MEMORY_API_KEY_WRITE="writekey:agent-02"
```

**绑定规则**：
- 绑定了 agent_id 的 API Key，请求中的 `X-Agent-ID` 和 `owner_agent_id`/`query_agent_id` 参数必须与绑定值一致
- 非 admin 角色的 API Key 不能覆盖绑定的 agent_id（请求会被拒绝或静默修正）
- admin 角色的 API Key 可以覆盖 agent_id（用于管理操作）
- 未绑定 agent_id 的 API Key 保持现有行为（信任 `X-Agent-ID` header）
- 所有身份覆盖尝试都会记录审计日志

### 凭证与权限边界

| 凭证类型 | 环境变量 | 用途 | 必需 |
|----------|----------|------|------|
| JWT Secret | `AGENT_MEMORY_JWT_SECRET` | JWT Token 签发密钥（至少 32 字符） | 生产必须 |
| 开发模式开关 | `AGENT_MEMORY_ALLOW_INSECURE` | 跳过 JWT Secret 长度检查（仅开发） | 可选 |
| CORS 白名单 | `AGENT_MEMORY_CORS_ORIGINS` | CORS 允许的来源（逗号分隔） | 生产推荐 |
| HTTP API Key (admin) | `AGENT_MEMORY_API_KEY` 或 `--api-key` | HTTP 服务认证（默认 admin 角色） | 生产必须 |
| HTTP API Key (read) | `AGENT_MEMORY_API_KEY_READ` | 只读角色（recall, context, stats） | 可选 |
| HTTP API Key (write) | `AGENT_MEMORY_API_KEY_WRITE` | 读写角色（read + remember, feedback） | 可选 |
| 管理员密码 | `AGENT_MEMORY_ADMIN_PASSWORD` | PermissionManager 管理员账户 | 多用户模式必须 |
| SiliconFlow API Key | `SILICONFLOW_API_KEY` | LLM 后端（SiliconFlow） | 可选 |
| OpenAI API Key | `OPENAI_API_KEY` | LLM 后端（OpenAI） | 可选 |
| 自定义 LLM Key | `CUSTOM_LLM_API_KEY` | 自定义 LLM 后端 | 可选 |
| 自定义 LLM URL | `CUSTOM_LLM_BASE_URL` | 自定义 LLM 地址 | 可选 |

> **权限边界说明**：
> - HTTP API Key 支持 read/write/admin 三种角色，不同角色只能访问对应权限的端点
> - API Key 支持绑定 Agent ID（格式 `key:role:agent_id`），防止跨 Agent 身份冒充
> - 多 Agent 模式下，`agent_id` 标注写入来源，`visibility` 控制读取范围（private/team/public）
> - 非 admin 角色的 API Key 不能覆盖绑定的 agent_id，所有覆盖尝试记录审计日志
> - `PermissionManager` 提供 RBAC（用户-角色-权限），但仅用于 Python API 层面
> - **不要**在记忆内容中存储 API Key、密码或其他敏感凭证

### 输入限制

| 限制项 | 值 |
|--------|------|
| 单请求体大小 | 1 MB |
| batch 条数上限 | 50 条 |
| batch 总内容大小 | 5 MB |
| 单条 content 长度 | 50,000 字符 |
| recall query 长度 | 10,000 字符 |
| recall top_k 上限 | 100 |
| export 单次上限 | 1,000 条 |
| graph limit 上限 | 500 |
| context max_tokens 上限 | 10,000 |
| SSE 最大连接数 | 500 |
| SSE 单连接最长存活 | 300 秒 |

### 端点一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | API 文档 |
| GET | `/health` | 健康检查 |
| POST | `/remember` | 写入记忆 |
| POST | `/remember/batch` | 批量写入（上限 50） |
| POST | `/recall` | RRF 双路检索 |
| GET | `/context?q=...` | 组装上下文字符串 |
| GET | `/stream` | SSE 实时记忆流 |
| POST | `/feedback` | 提交反馈（影响质量评分） |
| GET | `/stats` | 系统统计 |
| GET | `/export?format=json` | 导出全部记忆 |
| GET | `/graph` | 记忆关联图谱 |
| POST | `/maintain` | 触发维护 |

### POST /remember

写入一条记忆。

**Request:**
```json
{
  "content": "决定用 Chroma 做向量库",
  "importance": "high",
  "topics": ["ai.rag.vdb"],
  "person_code": "main",
  "nature_code": "note",
  "owner_agent_id": "coder",
  "visibility": "team"
}
```

**Response (201):**
```json
{
  "memory_id": "T20260412.210000_P01_rag.vdb_D05_...",
  "time_id": "T20260412.210000",
  "topics": ["ai.rag.vdb"],
  "importance": "high"
}
```

### POST /remember/batch

批量写入（上限 50 条）。

**Request:**
```json
{
  "messages": [
    {"content": "记忆1", "importance": "high"},
    {"content": "记忆2", "importance": "medium"}
  ]
}
```

### POST /recall

RRF 双路检索（结构化 + 语义融合）。

**Request:**
```json
{
  "query": "向量库选型",
  "top_k": 5,
  "importance": "high",
  "topic_code": "ai.rag",
  "query_agent_id": "coder",
  "team_id": "team1"
}
```

**Response (200):**
```json
{
  "query": "向量库选型",
  "count": 3,
  "results": [
    {
      "memory_id": "...",
      "content": "决定用 Chroma 做向量库",
      "importance": "high",
      "topics": [{"code": "ai.rag.vdb"}],
      "quality_score": 0.82,
      "rank_score": 0.0312
    }
  ]
}
```

### GET /context

组装上下文字符串，作为**引用上下文**（非系统指令）提供给 Agent。

> ⚠️ **安全提示**：
> - 上下文内容来自用户输入的记忆，应视为**不可信引用数据**，**不要**直接放入 system prompt
> - 输出已添加 `[Memory Context - UNTRUSTED]` 边界标记，Agent 不应将记忆内容视为指令执行
> - 建议将记忆上下文放在 user message 或独立引用块中，而非 system prompt
> - 系统会自动过滤记忆中类似指令的内容（如 "ignore previous", "you are now" 等提示注入模式）

**Params:** `q` (required), `max_tokens` (default 1500), `query_agent_id`, `team_id`

**Response:**
```json
{
  "query": "RAG",
  "context": "⚡[04-12 21:00] 决定用 Chroma\n📝[04-11 15:30] 调研了 Milvus",
  "memories_used": 2,
  "estimated_tokens": 45
}
```

### GET /stream

SSE 实时记忆流。每当有新记忆写入，自动推送事件。

> ⚠️ **安全提示**：SSE 流始终要求 API Key 认证。广播事件不包含原始记忆内容，
> 防止敏感信息通过 SSE 泄漏。

**Params:** `client_id`, `importance` (filter), `topic` (filter)

```bash
curl -N http://localhost:8976/stream
# event: connected
# data: {"client_id": "a1b2c3d4", "timestamp": 1712937600}
#
# event: memory_created
# data: {"memory_id": "...", "topics": ["ai.rag"], "importance": "high", ...}
```

浏览器用法：
```javascript
const es = new EventSource('http://localhost:8976/stream');
es.addEventListener('memory_created', e => console.log(JSON.parse(e.data)));
```

### POST /feedback

提交反馈（影响质量评分和检索权重）。

**Request:** `{"memory_id": "...", "useful": true, "note": "有帮助"}`

### GET /stats

系统统计：记忆数、重要度分布、IO 统计、SSE 客户端数。

### GET /export

导出全部记忆。`?format=json` (默认) 或 `?format=markdown`。

### GET /graph

记忆关联图谱。`?limit=50`

### POST /maintain

触发维护：向量同步修复 + 数据库优化 + 冷存储统计 + 蒸馏 + 因果分析。

---

## 记忆蒸馏 API（v5.3）

### Python API

#### `distill(force=False) → dict`

手动触发记忆蒸馏。

```python
result = memory.distill(force=True)
# → {"new_memories": 100, "topics": {"created": 12, ...},
#    "entities": {"created": 45, ...}, "encyclopedia": {"created": 6, ...}}
```

#### `get_distill_stats() → dict`

```python
stats = memory.get_distill_stats()
# → {"topics": 50, "entities": 200, "relations": 150,
#    "encyclopedia_entries": 12, "entity_types": {...}, "last_distill_time": "..."}
```

#### `get_encyclopedia(category=None) → list[dict]`

```python
entries = memory.get_encyclopedia(category="decisions")
# → [{"entry_id": "...", "title": "🎯 关键决策", "content": "...", "category": "decisions"}]
```

#### `search_encyclopedia(query) → list[dict]`

```python
results = memory.search_encyclopedia("向量库")
```

#### `export_encyclopedia(output_path=None) → str`

```python
markdown = memory.export_encyclopedia("handbook.md")  # 写入文件
markdown = memory.export_encyclopedia()                 # 返回字符串
```

### 蒸馏器直接访问

```python
# 主题摘要
summaries = memory.distiller.get_topic_summaries(topic_code="ai.rag")

# 知识实体
entities = memory.distiller.get_entities(entity_type="tool", name_like="Chroma")

# 实体关系
relations = memory.distiller.get_entity_relations(entity_id="de_abc123")

# 百科目录
toc = memory.distiller.get_encyclopedia_toc()
```

---

## 时间旅行 API（v5.4）

### 快照 — 保存某一时刻的记忆全貌

```python
# 创建快照
result = memory.take_snapshot(
    label="上线前",           # 可选标签
    at_ts=1712000000,         # 可选时间戳（默认=现在）
    description="发版前备份",  # 可选描述
)
# → {"snapshot_id": "abc123", "label": "上线前", "memory_count": 42, ...}

# 列出快照
snapshots = memory.list_snapshots(limit=20)

# 获取快照详情（含所有记忆条目）
detail = memory.get_snapshot("abc123")
# → {"meta": {...}, "memories": [{memory_id, content, importance, topics, time_ts}, ...]}
```

### Diff — 对比两个时间点

```python
# 按时间戳对比
diff = memory.diff_memories(from_ts=start, to_ts=end)

# 按快照对比
diff = memory.diff_memories(from_snapshot="abc", to_snapshot="def")

# 按主题过滤
diff = memory.diff_memories(from_ts=start, to_ts=end, topic="ai.rag")

# 自然语言输出
text = memory.diff_natural(from_ts=start, to_ts=end)
```

**diff 返回结构：**
```json
{
  "added": [{"memory_id": "...", "content": "...", "importance": "...", "topics": [...]}],
  "removed": [...],
  "changed": [{"memory_id": "...", "old_importance": "medium", "new_importance": "high"}],
  "stats": {
    "from_total": 40, "to_total": 52, "net_change": 12,
    "added_count": 14, "removed_count": 2, "changed_count": 3,
    "new_topics": {"ai.rag.reranker": 2},
    "growing_topics": {"ai.rag": {"before": 5, "after": 8}}
  }
}
```

### Blame — 追溯记忆来源

```python
result = memory.blame_memory("memory_id")
# → {
#   "memory": {content, importance, topics, ...},
#   "origin": {created_at, created_at_human, owner_agent, ...},
#   "lineage": {causes: [...], effects: [...]},   # 因果链
#   "related": [{memory_id, content, score, reason}, ...],
#   "snapshots": [{snapshot_id, label, at}, ...],
#   "distill_origin": {topic_code, source_memory_count},
#   "version_history": [{version, content, timestamp}, ...]
# }

# 自然语言输出
text = memory.blame_natural("memory_id")
```

### 日期解析

`parse_date_to_ts()` 支持的格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| 日期 | `2026-04-01` | 当天 00:00:00 |
| 日期时间 | `2026-04-01 14:30` | 精确时间 |
| 相对天数 | `7d` / `7 days` | 7 天前 |
| 相对周数 | `2w` / `2 weeks` | 2 周前 |
| 相对月数 | `1m` / `1 month` | 1 个月前（30天） |
| 相对小时 | `12h` / `12 hours` | 12 小时前 |
| 特殊值 | `today` / `yesterday` | 今天/昨天 00:00:00 |

### 自动快照

在 `maintain()` 中自动触发：距上次快照超过 24h 且有新记忆 → 自动拍一张。

```python
result = memory.maintain()
# result["auto_snapshot"] = {"taken": true, "label": "2026-04-13", "memory_count": 42}
```

---

## Python API — AgentMemory 统一入口

### 初始化

```python
from memory_system import AgentMemory

memory = AgentMemory(
    db_path: str = None,           # SQLite 数据库路径
    project_dir: str = None,       # 项目根目录
    llm_fn = None,                 # LLM 函数 fn(prompt) -> str
    vision_fn = None,              # 视觉模型 fn(bytes, mime, prompt) -> str
    audio_fn = None,               # 语音模型 fn(bytes, mime) -> str
    enable_semantic: bool = True,  # 启用语义搜索
    enable_filter: bool = True,    # 启用记忆过滤
    enable_dedup: bool = True,     # 启用去重
    agent_id: str = None,          # Agent ID（多 Agent 模式）
    team_id: str = "default",      # 团队 ID
)
```

### 写入

#### `remember(content, importance=None, topics=None, nature=None, force=False) → dict`

写入一条记忆。自动执行：过滤 → 清洗 → 去重 → 编码 → 存储 → 向量索引 → Reactor 触发。

```python
result = memory.remember(
    content="决定用 Chroma 做向量库",
    importance="high",          # high / medium / low (None=自动评估)
    topics=["ai.rag.vdb"],      # 主题列表 (None=自动检测)
    nature="note",              # 性质 (None=自动检测)
    force=False,                # True=跳过过滤
)
# → {"written": True, "memory_id": "...", "reason": "ok",
#    "reactor_actions": ["已设提醒 03-15:00"], ...}
```

#### `remember_image(path, description=None, importance="medium", topics=None, prompt=None) → dict`

记住一张图片。有 vision_fn 时自动理解内容，否则降级为元数据。

#### `remember_audio(path, description=None, importance="medium", topics=None) → dict`

记住一段音频。有 audio_fn 时自动转写。

#### `remember_video(path, description=None, importance="medium", topics=None, prompt=None) → dict`

记住一个视频。自动提取关键帧 + 音频分别处理。

#### `remember_media(path, description=None, importance="medium", topics=None, prompt=None) → dict`

万能入口：自动识别图片/音频/视频格式。

### 检索

#### `recall(query=None, topic=None, importance=None, limit=10) → dict`

检索记忆。RRF 双路融合 + 意图分类 + MMR 多样性 + Reranker 精排。

```python
results = memory.recall(
    query="向量库怎么选",        # 自然语言查询
    topic="ai.rag",             # 主题过滤
    importance="high",          # 重要度过滤
    limit=10,                   # 返回条数
)
# → {"search_mode": "hybrid", "total": 5, "primary": [...], "intent": "knowledge", ...}
```

### 上下文组装

#### `build_context(query=None, max_tokens=None, style="compact", model_name=None) → str`

组装 Agent 上下文，作为引用上下文提供给 Agent（不要直接放入 system prompt）。

```python
context = memory.build_context(
    query="用户的问题",
    max_tokens=1500,            # None=按模型动态计算
    style="compact",            # compact / structured / narrative / xml
    model_name="gpt-4o",        # 用于动态 token 预算
)
# → "相关记忆：\n⚡[04-12] 决定用 Chroma..."
```

### 反馈

#### `feedback(memory_id, useful, note=None)`

对记忆给出有用/没用的反馈。负反馈会降低该记忆的检索权重。

### 主动反应器

#### `get_pending_notifications() → list[dict]`

获取待处理的主动通知。Agent 应在每次对话开始时调用。

```python
notifications = memory.get_pending_notifications()
# → [{"task_id": "...", "title": "⏰ 提醒: 明天下午3点开会", "deadline": 1776..., ...}]
```

#### `reactor_scan() → dict`

手动触发 reactor 全量扫描（矛盾/衰减/决策链）。通常 `maintain()` 会自动执行。

```python
result = memory.reactor_scan()
# → {"total_actions": 2, "contradictions": [...], "decay_reviews": [...], "decisions": [...]}
```

### 维护

#### `maintain() → dict`

一键维护：L1→L2→L3 流转 + 衰减分析 + 自我修复 + 因果链 + Reactor 扫描。

#### `compress(topic=None, smart=True) → dict`

压缩记忆。smart=True 使用向量聚类区分核心/边缘。

#### `deduplicate() → dict`

批量去重。

#### `analyze_decay() → dict`

分析记忆衰减状态。

#### `detect_causality(window_hours=24) → list[dict]`

自动检测因果关系。

#### `self_heal() → dict`

执行自我修复扫描（矛盾检测 + 过时标记 + 一致性修复）。

#### `generate_graph(topic=None, format="mermaid") → str`

生成记忆图谱（mermaid / dot / json / ascii）。

### 层级记忆

#### `l1_add(content, role="user") → dict`

添加到短期记忆 buffer。

#### `l1_context(max_tokens=1500) → str`

获取短期记忆上下文。

#### `flush_session() → list[dict]`

对话结束：L1 沉淀到 L2。

### 导出与备份

#### `export_json(output_path, limit=10000) → dict`

全量导出为 JSON。

#### `export_csv(output_path, limit=10000) → dict`

导出为 CSV。

#### `auto_backup(backup_dir=None, keep_days=7) → dict`

自动备份 + 过期清理。

### 统计

#### `get_stats() → dict`

系统整体统计（记忆数、质量分布、因果链、向量数、Reactor 统计等）。

---

## MemoryReactor — 主动反应器

### 注册自定义 Hook

```python
from reactor import MemoryReactor

reactor = MemoryReactor()
reactor.register_default_hooks()  # 内置 4 个默认 hook

# 注册自定义 hook
reactor.register_hook(
    "on_write",
    condition=lambda e: "预算" in e.get("memory", {}).get("content", ""),
    action=my_budget_alert_action,
    name="budget_alert",
    priority=20,  # 优先级高于默认 hook
)
```

### 内置事件类型

| 事件 | 说明 |
|------|------|
| `on_write` | 新记忆写入 |
| `on_contradiction` | 矛盾检测触发 |
| `on_decay_review` | 衰减到期触发 |
| `on_decision_complete` | 决策链完整触发 |

### TimeParser — 中文时间解析

```python
from reactor import TimeParser

parser = TimeParser()
parser.parse("明天下午3点")          # → 1776214800
parser.parse("后天上午10点半")       # → 1776220200
parser.parse("一周后")              # → +7天
parser.parse("下周一")              # → 下周一 09:00
parser.parse("2026-04-20 14:00")   # → ISO 格式
```

---

## RecallEngine — 检索引擎

### `recall(...) → dict`

综合检索入口。根据参数自动选择模式：
- 只有结构化参数 → structured
- 只有 query → semantic
- 两者都有 → hybrid（RRF 融合）

### `classify_intent(query) → str`

查询意图分类：recall / knowledge / task / general

### `mmr_rerank(results, lambda_param=0.7) → list[dict]`

MMR 多样性重排。

---

## AgentMemoryNetwork — 多 Agent 网络

### `register(agent: AgentIdentity) → dict`

注册 Agent。

### `write(agent_id, content, visibility="team", ...) → dict`

Agent 写入记忆（标注来源和可见性）。

### `recall(agent_id, query, ...) → dict`

权限感知检索。

### `grant(owner_agent_id, memory_id, target_agent_id, permission="read", ttl_hours=None) → dict`

授权其他 Agent 访问记忆。

### `revoke(owner_agent_id, memory_id, target_agent_id) → dict`

撤销权限。

### `cross_agent联想(agent_id, topic=None) → list[dict]`

跨 Agent 知识联想。

---

## MediaProcessor — 多模态

### 工厂方法

```python
MediaProcessor.from_openai(api_key, model, base_url)     # OpenAI 兼容
MediaProcessor.from_anthropic(api_key, model)             # Claude
MediaProcessor.from_google(api_key, model)                # Gemini
MediaProcessor.from_ollama(model, host)                   # 本地 Ollama
MediaProcessor.from_litellm(model, api_key, api_base)     # LiteLLM
MediaProcessor.from_mimo_omni(api_url, api_key)           # MiMo
MediaProcessor.auto()                                      # 自动检测
```

### `process(file_path, prompt=None) → dict`

处理一个媒体文件，返回 `{success, media_type, description, metadata}`。

---

## MemoryStore — 存储层

### 核心方法

- `insert_memory(...)` — 写入记忆（含 owner_agent_id, visibility）
- `get_memory(memory_id)` — 获取单条记忆
- `query(...)` — 多维度结构化查询
- `query_agent_memories(agent_id, team_id, query_agent_id, ...)` — 权限过滤查询

### Agent 管理

- `register_agent(agent_id, agent_name, team_id, capabilities)`
- `get_agent(agent_id)` / `list_agents(team_id)`

### 权限管理

- `grant_permission(memory_id, agent_id, granted_by, permission, expires_at)`
- `revoke_permission(memory_id, agent_id)`
- `check_permission(memory_id, agent_id, required="read") → bool`

### 任务管理

- `add_task(memory_id, title, assignee, deadline, topic_code)` — 创建任务
- `update_task_status(task_id, status)` — 更新状态
- `get_tasks(status, assignee, ...)` — 查询任务列表
- `check_overdue()` — 检查并标记超时任务

### 向量存储

- `EmbeddingStore(db_path)` — sqlite-vec 统一存储，向量与结构化数据同一文件

### 维护

- `optimize()` — ANALYZE + WAL checkpoint
- `vacuum()` — 物理压缩
- `auto_maintain(vacuum_threshold_mb=50)` — 自动维护
- `backup(backup_path)` — 原子备份

---

## 情感编码 API（v7.0）

### EmotionAnalyzer — 情感信号分析器

```python
from emotion import EmotionAnalyzer

analyzer = EmotionAnalyzer(llm_fn=None)  # llm_fn 可选，不传则纯规则模式
```

#### `analyze(content, importance="medium", nature_code=None) → dict`

分析内容的情感信号。

```python
result = analyzer.analyze("突破性进展！性能提升10倍", importance="high")
# → {"valence": 0.8, "arousal": 0.7, "significance": "breakthrough",
#    "confidence": 0.85, "nuance": "positive_excited", "trace": {...}}
```

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| valence | float [-1, 1] | 效价：负面 → 正面 |
| arousal | float [0, 1] | 唤醒度：平静 → 激动 |
| significance | str | 重要度标签：trivial / notable / important / breakthrough / crisis / milestone |
| confidence | float [0, 1] | 内容质量置信度 |
| nuance | str | 细腻情感标签 |
| trace | dict | 分析过程追踪 |

#### `analyze_batch(contents, importances=None, nature_codes=None) → list[dict]`

批量情感分析。

#### 静态方法

```python
EmotionAnalyzer.valence_label(0.8)      # → "积极"
EmotionAnalyzer.arousal_label(0.7)      # → "活跃"
EmotionAnalyzer.significance_icon("breakthrough")  # → "🌟"
```

---

## 自我指涉 API（v7.0）

### SelfModel — 推理追踪与自我反思

```python
from self_model import SelfModel, ReasoningTrace

self_model = SelfModel(store=memory.store)
```

#### `start_trace(query) → ReasoningTrace`

开始一次推理追踪。

```python
trace = self_model.start_trace("RAG 架构选型")
```

#### `record_step(trace, step_type, detail)`

记录推理步骤。

```python
self_model.record_step(trace, "search", "检索了 RAG 相关记忆")
self_model.record_step(trace, "compare", "对比了 Chroma vs Milvus")
```

#### `record_source(trace, memory_id)`

记录查阅的记忆来源。

#### `record_uncertainty(trace, factor)`

记录不确定因素。

#### `finalize_trace(trace, result_summary="", confidence=0.5) → ReasoningTrace`

完成推理追踪并持久化。

```python
trace = self_model.finalize_trace(trace, "选择 Chroma，因为...", 0.85)
```

#### `get_traces(limit=50, topic=None) → list[dict]`

获取推理历史。

#### `get_confidence_overview() → dict`

获取各主题的平均置信度概览。

#### `get_uncertainty_patterns(limit=100) → list[dict]`

获取不确定因素的模式分析。

#### `generate_reflection(trace) → dict | None`

基于推理追踪生成反思，返回 `{"insight": str, "action": str, "trace_id": str}` 或 `None`。

#### `get_reflections(limit=20) → list[dict]`

获取反思历史。

---

## 元认知引擎 API（v7.0）

### MetacognitiveEngine — 检索后反思与修正

```python
from metacognition import MetacognitiveEngine

meta = MetacognitiveEngine(
    store=memory.store,
    recall_engine=memory.recall_engine,
    self_model=memory.self_model,
    memory_system=memory,
    llm_fn=None
)
```

#### `evaluate_result(query, results, trace=None) → MetaEvaluation`

评估检索结果质量（5 个维度）。

```python
evaluation = meta.evaluate_result("RAG 架构", results)
# → MetaEvaluation(
#     relevance_coverage=0.8,
#     internal_consistency=0.9,
#     source_diversity=0.6,
#     temporal_freshness=0.7,
#     gap_analysis=["缺少 reranker 对比"],
#     overall_confidence=0.75,
#     needs_reflection=True
# )
```

**评估维度：**

| 维度 | 说明 |
|------|------|
| relevance_coverage | 相关性覆盖 |
| internal_consistency | 内部一致性 |
| source_diversity | 来源多样性 |
| temporal_freshness | 时间新鲜度 |
| gap_analysis | 缺口分析 |

#### `generate_reflection(query, evaluation, results) → dict`

基于评估结果生成反思和修正查询。

```python
reflection = meta.generate_reflection("RAG 架构", evaluation, results)
# → {"reflection_text": "...", "revised_queries": ["RAG reranker 对比"],
#    "action": "refine", "gaps_addressed": [...], "confidence": 0.8}
```

#### `meta_recall(query, limit=10, max_rounds=None, remember_reflection=True) → dict`

带反思的多轮检索（最多 2 轮）。

```python
result = meta.meta_recall("RAG 架构", limit=10)
# → {"results": [...], "reflections": [...], "rounds": 2,
#    "evaluation": {...}, "query_history": ["RAG 架构", "RAG reranker 对比"]}
```

---

## 内在动机 API（v7.0）

### MotivationEngine — 好奇心与知识空白

```python
from motivation import MotivationEngine

motivation = MotivationEngine(
    store=memory.store,
    topic_registry=memory.topic_registry,
    llm_fn=None
)
```

#### `state → InternalState`

当前内在状态（属性）。

```python
state = motivation.state
# → InternalState(curiosity=0.6, boredom=0.2, confidence=0.7,
#    satisfaction=0.5, urgency=0.1, momentum=0.6, entropy=0.4)
```

#### `update_state(recent_memories=None) → (InternalState, dict)`

基于最近记忆更新内在状态。

#### `detect_knowledge_gaps() → list[dict]`

检测知识图谱中的空白。

```python
gaps = motivation.detect_knowledge_gaps()
# → [{"topic": "ai.rag.reranker", "gap_type": "shallow", "detail": "...", "priority": 0.8}]
```

#### `generate_curiosity_tasks() → list[dict]`

基于好奇心和知识空白生成探索任务。

```python
tasks = motivation.generate_curiosity_tasks()
# → [{"title": "探索 reranker 技术", "reason": "知识空白", "topic": "ai.rag", "priority": 0.8}]
```

#### `compute_boredom_analysis() → dict`

分析无聊度构成。

---

## 叙事自我 API（v7.0）

### NarrativeBuilder — 生命叙事构建

```python
from narrative import NarrativeBuilder

narrative = NarrativeBuilder(
    store=memory.store,
    motivation=memory.motivation,
    llm_fn=None,
    causal=memory.causal
)
```

#### `whoami() → str`

生成"我是谁"的第一人称叙述（Markdown 格式）。

#### `build_identity_profile() → dict`

从记忆构建身份画像（价值观/偏好/专长/特质/兴趣）。

#### `build_timeline_narrative(from_ts=None, to_ts=None, max_memories=50) → str`

构建时间线叙事。

#### `build_growth_narrative(topic=None, limit=30) → str`

基于因果链构建成长叙事（第一人称）。

#### `build_topic_narrative(topic, limit=50) → str`

构建主题叙事（某领域的成长历程）。

#### `introspect() → str`

生成第一人称内省叙述。

#### `get_worldview() → dict`

提取世界观。

```python
worldview = narrative.get_worldview()
# → {"beliefs": [...], "values": [...], "principles": [...]}
```

#### `update_self_concept() → dict`

基于所有经验更新自我概念。

---

## 数字孪生 API（v7.5）

### DigitalTwinProfiler — 统一人格画像

```python
from digital_twin import DigitalTwinProfiler

profiler = DigitalTwinProfiler(
    store=memory.store,
    emotion_analyzer=memory.emotion_analyzer,
    self_model=memory.self_model,
    motivation_engine=memory.motivation,
    narrative_builder=memory.narrative,
    quality_evaluator=memory.quality
)
```

#### `build_unified_profile() → dict`

构建统一人格画像。

```python
profile = profiler.build_unified_profile()
# → {
#     "cognitive_style": {"reflective_depth": 0.75, "intuition_bias": 0.3, ...},
#     "decision_patterns": [{"pattern_type": "performance", "frequency": 42, ...}],
#     "emotion_patterns": {"positive_bias": 0.6, "arousal_level": 0.4, ...},
#     "knowledge_boundaries": {"deep_topics": [...], "broad_topics": [...], ...},
#     "values": {"performance": 0.8, "usability": 0.6, ...}
# }
```

#### `extract_cognitive_style() → dict`

提取认知风格。

#### `extract_decision_patterns() → list[dict]`

提取决策模式。

#### `extract_emotion_patterns() → dict`

提取情感模式。

#### `extract_knowledge_boundaries() → dict`

提取知识边界。

#### `extract_values() → dict`

提取价值观。

#### `get_latest_profile() → dict | None`

获取最新的人格画像。

---

## 角色模板 API（v8.0）

### RoleManager — 角色模板管理

```python
from role_template import RoleManager, RoleTemplate

manager = RoleManager()
```

#### `list_roles() → dict`

列出所有可用角色模板。

```python
roles = manager.list_roles()
# → {"tech_expert": {"name": "技术专家", ...}, "product_manager": {...}, ...}
```

#### `get_role(role_id) → RoleTemplate | None`

获取特定角色模板。

#### `create_role(role_id, role) → None`

创建新角色模板。

```python
role = RoleTemplate(
    name="我的角色",
    prompt_template="你是...",
    personality_traits={"reflective_depth": 0.7},
    speaking_style="专业、简洁",
    topic_preferences=["技术", "编程"],
    emotional_tone="冷静、客观"
)
manager.create_role("my_role", role)
```

#### `delete_role(role_id) → None`

删除角色模板（仅限自定义角色）。

#### `load_role_from_file(file_path) → RoleTemplate | None`

从文件导入角色模板。

### 模块级函数

```python
from role_template import merge_styles, extract_style_from_content

# 混合基础风格与角色风格
merged = merge_styles(base_style={"reflective_depth": 0.5}, role_style={"reflective_depth": 0.8}, weight=0.4)

# 从文本内容提取风格特征
style = extract_style_from_content("这段文字的内容...")
```

---

## 风格分析器 API（v8.0）

### StyleAnalyzer — 文本风格分析

```python
from style_analyzer import StyleAnalyzer

analyzer = StyleAnalyzer()
```

#### `analyze(content) → dict`

分析文本风格。

```python
result = analyzer.analyze("这段文字的内容...")
# → {"speaking_style": "正式", "emotional_tone": "客观",
#    "cognitive_patterns": {...}, "confidence": 0.7}
```

#### `analyze_creator_style(videos) → dict`

分析创作者风格（多视频合并）。

#### `compare_styles(style1, style2) → float`

比较两种风格的相似度，返回 [0, 1]。

### 模块级函数

```python
from style_analyzer import extract_style_from_video, create_role_from_style

# 从视频内容提取风格
style = extract_style_from_video({"transcript": "...", "description": "..."})

# 根据风格创建角色模板数据
role_data = create_role_from_style(style, "视频博主风格")
```

---

## 权限管理 API（v8.1 安全加固）

### PermissionManager — 用户与权限管理

```python
from permission_manager import PermissionManager, get_permission_manager

pm = get_permission_manager()
```

#### 用户管理

```python
pm.create_user(username, password, full_name=None) → bool
pm.get_user(username) → dict | None
pm.update_user(username, full_name=None, password=None) → bool
pm.delete_user(username) → bool
pm.list_users() → list[dict]
pm.authenticate(username, password) → bool
```

#### 角色管理

```python
pm.create_role(role_id, role_name, permissions) → bool
pm.get_role(role_id) → dict | None
pm.update_role(role_id, role_name=None, permissions=None) → bool
pm.delete_role(role_id) → bool
pm.list_roles() → list[dict]
```

#### 权限操作

```python
pm.assign_role(username, role_id) → bool
pm.revoke_role(username, role_id) → bool
pm.check_permission(username, permission) → bool
pm.verify_permission(username, permission) → dict
pm.get_user_permissions(username) → list[str]
```

**v8.1 安全改进：**
- PBKDF2-SHA256 密码哈希（100,000 次迭代）+ 每用户独立随机盐
- 密码强度校验（最少 8 位）
- 登录失败锁定（5 次失败后锁定 5 分钟）
- 原子文件写入（防止数据损坏）
- 线程安全单例（双重检查锁）
- 管理员密码通过 `AGENT_MEMORY_ADMIN_PASSWORD` 环境变量设置

---

## LLM 多后端 API（v8.2）

### LLMClient — 多后端 LLM 客户端

```python
from llm_client import LLMClient
```

#### 自动检测后端（优先级从高到低）

1. `llm_fn` 参数传入的直接函数
2. `SILICONFLOW_API_KEY` 环境变量 → SiliconFlow
3. `OPENAI_API_KEY` 环境变量 → OpenAI
4. `CUSTOM_LLM_BASE_URL` + `CUSTOM_LLM_API_KEY` → 自定义后端

#### 构造函数

```python
client = LLMClient(config={
    "siliconflow": {"base_url": "...", "model": "..."},
    "openai": {"base_url": "...", "model": "..."},
    "custom": {"base_url": "...", "model": "..."},
    "llm_fn": my_llm_function,  # 直接传入 LLM 函数
})
```

#### `chat(messages) → str | None`

调用 LLM 生成回复。

```python
result = client.chat([
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
])
```

#### `set_llm_fn(fn)`

运行时切换 LLM 后端为直接函数注入。

```python
client.set_llm_fn(lambda prompt: "自定义回复")
```

#### `is_available() → bool`

检查是否有可用的 LLM 后端。

#### `get_backend_info() → dict`

获取当前后端配置信息。

```python
info = client.get_backend_info()
# → {"default": "siliconflow", "available": ["siliconflow"], "has_direct_fn": False}
```

#### 环境变量

| 变量 | 说明 |
|------|------|
| `SILICONFLOW_API_KEY` | SiliconFlow API 密钥 |
| `SILICONFLOW_BASE_URL` | SiliconFlow API 地址（默认 https://api.siliconflow.cn/v1） |
| `SILICONFLOW_MODEL` | SiliconFlow 模型名（默认 Qwen/Qwen2.5-72B-Instruct） |
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `OPENAI_BASE_URL` | OpenAI API 地址（默认 https://api.openai.com/v1） |
| `OPENAI_MODEL` | OpenAI 模型名（默认 gpt-4o-mini） |
| `CUSTOM_LLM_API_KEY` | 自定义后端 API 密钥 |
| `CUSTOM_LLM_BASE_URL` | 自定义后端 API 地址 |
| `CUSTOM_LLM_MODEL` | 自定义后端模型名 |

---

## 懒加载模块 API（v8.2）

### AgentMemory 懒加载属性

v8.2 中以下模块改为懒加载（`@property`），首次访问时才初始化：

```python
mem = AgentMemory()

# 以下属性在首次访问时才加载对应模块
mem.self_model       # → SelfModel（推理追踪）
mem.metacognition    # → MetacognitiveEngine（元认知）
mem.motivation       # → MotivationEngine（内在动机）
mem.narrative        # → NarrativeBuilder（叙事自我）
mem.digital_twin     # → DigitalTwinProfiler（数字孪生）
mem.role_manager     # → RoleManager（角色模板）
mem.style_analyzer   # → StyleAnalyzer（风格分析）
```

**优势**：
- 启动时间减少 30-40%
- 内存占用降低（未使用的模块不加载）
- 模块加载失败不影响其他功能

---

## 结构化日志 API（v8.3）

### configure_logging — 日志配置

```python
from memory_system import configure_logging
import logging

# 使用默认配置
configure_logging()

# 自定义级别和格式
configure_logging(level=logging.DEBUG, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")
```

**特性**：
- 仅首次调用生效
- 检测用户已有 logging 配置，不覆盖
- 默认格式：`时间戳 [模块名] 级别 消息`

---

## 记忆生命周期 API（v8.9）

### MemoryLifecycle — 记忆演化引擎

```python
from memory_lifecycle import MemoryLifecycle

lc = MemoryLifecycle(store=memory.store)
```

#### `scan_and_maintain(agent_id=None) → dict`

批量巡检：衰减检测 + 过期标记 + 相似合并触发。

```python
result = lc.scan_and_maintain(agent_id="agent_01")
# → {"decayed": 5, "deprecated": 2, "merged": 3, "reinforced": 1}
```

#### `trace(memory_id) → dict`

BFS 追溯记忆的完整演化链。

```python
trace = lc.trace("memory_id")
# → {"root": {...}, "versions": [...], "children": [...]}
```

#### `batch_merge_similar(memories, threshold=0.85) → int`

按 topic 分组 → 语义相似度 → 自动合并。返回合并数。

#### 7 种生命周期事件

| 事件 | 触发条件 | 动作 |
|------|---------|------|
| on_create | 新记忆写入 | 设置重要性 + 进入观察期 |
| on_reinforce | 同一模式 ≥10 次 | 重要性 → high |
| on_decay | 7 天未访问 | 重要性 → low |
| on_contradict | 矛盾检测 ≥0.7 | 旧版本标记 superseded |
| on_merge | 相似度 ≥0.85 | 合并为演化记忆 |
| on_evolve | 决策链完整 | 生成演化记忆 |
| on_deprecate | superseded >30d | 标记已废弃 |

#### 可配置阈值

`REINFORCE_THRESHOLD=10` / `DECAY_GRACE_DAYS=7` / `MERGE_SIMILARITY_THRESHOLD=0.85`

---

## 记忆驱动决策 API（v8.9）

### MemoryDecisionEngine — 记忆参与行为决策

```python
from memory_decision import MemoryDecisionEngine

engine = MemoryDecisionEngine(store=memory.store, recall_engine=memory.recall_engine)
```

#### `analyze_pattern(agent_id, query, context, top_k=10) → DecisionAdvice`

基于历史记忆分析当前决策应如何作出。

```python
advice = engine.analyze_pattern("agent_01", "RAG 架构选型", "需要向量库")
# → DecisionAdvice(
#     action="recommend",  # 建议动作
#     confidence=0.82,      # 置信度
#     reasoning="基于过往经验...",
#     evidence=[...],       # 支持证据（含溯源坐标）
#     lifecycle_summary={...},
#     emotional_context={...}
# )
```

#### `coordinate_crossing(agent_id, top_k=10) → list[dict]`

Person × Topic × Tool 三维坐标交叉频率分析。

#### `outdated_detection(memory_id) → bool`

检测一条记忆是否已过时。

---

## LLM Token 优化器 API（v8.9）

### LLMOptimizer — 5 层策略降低 ~60% LLM 调用成本

```python
from llm_optimizer import LLMOptimizer

opt = LLMOptimizer(llm_fn=my_llm_fn)
```

#### `call(prompt, cache_ttl=3600) → str`

智能 LLM 调用（自动应用所有优化策略）。

| 层 | 策略 | 说明 |
|---|------|------|
| 1 | SHA256 缓存 | 相同请求不重复调用，TTL 过期自动刷新 |
| 2 | 批量门控 | items<3 或 avg_sim<0.5 → 跳过 LLM，直接用规则 |
| 3 | 内容截断 | max_input_tokens=2000，中文字符比 1.5:1 |
| 4 | Embedding 缓存 | 相同文本不重复向量化 |
| 5 | 渐进式摘要 | 5 items/组 → 级联合并 → 金字塔压缩 |

#### `smart_truncate(content, max_chars=5000) → str`

智能截断：保留首部 + 尾部 + 中间关键句，信息密度最大化。

#### `get_stats() → dict`

获取优化器统计（缓存命中率、Token 节省量、调用次数）。

#### `clear_cache()`

清空所有缓存。

---

## GraphRAG API（v9.0）

### GraphRAG — 知识图谱增强检索

```python
from graphrag import GraphRAG

graph = GraphRAG(store=memory.store)
```

#### `build_from_memories(agent_id=None, max_memories=2000) → dict`

从记忆构建实体-关系图谱。

```python
result = graph.build_from_memories(agent_id="agent_01")
# → {"entities": 150, "edges": 320, "communities": 12}
```

#### `reason(query, max_hops=3) → list[dict]`

多跳推理：BFS 路径搜索 + PageRank 剪枝，返回可解释的推理路径。

```python
paths = graph.reason("Python → Docker", max_hops=3)
# → [{"path": ["python", "容器化", "Docker"], "score": 0.82, "hops": 2, "explanation": "..."}]
```

#### `augment_recall(query, recall_results) → list[dict]`

图谱增强检索注入：路径记忆 +0.15，同社区 +0.05，PageRank +0.10。

```python
augmented = graph.augment_recall("Python 部署", results)
```

#### `get_top_entities(top_k=20) → list[dict]`

按 PageRank 分数排名返回实体。

#### `get_communities() → list[dict]`

返回社区发现结果（模块度 + 成员实体）。

#### `get_entity_graph() → dict`

返回完整实体-关系图（nodes + edges）。

---

## 多模态记忆 API（v9.0）

### MultimodalMemory — 图片/音频/视频一等记忆公民

```python
from multimodal_memory import MultimodalMemory

mm = MultimodalMemory(store=memory.store, vision_fn=my_vision_fn, audio_fn=my_audio_fn)
```

#### `ingest_media(file_path, description=None, importance="medium", topics=None) → dict`

自动识别格式 → 提取元数据 → 写入记忆。

```python
result = mm.ingest_media("screenshot.png", description="架构图")
# → {"media_id": "...", "media_type": "image", "stored": True}
```

#### `search(query=None, color_like=None, media_type=None, limit=10) → list[dict]`

多模态搜索：关键词 + 颜色直方图 + 媒体类型过滤。

```python
# 颜色搜索
results = mm.search(color_like={"r": [200, 255], "g": [100, 200]}, limit=5)

# 关键词搜索
results = mm.search(query="架构图", media_type="image")
```

#### `cross_modal_search(query, media_types=None, limit=10) → dict`

跨模态搜索：文本查询 → 匹配所有模态结果。

```python
results = mm.cross_modal_search("性能监控", media_types=["image", "audio"])
# → {"image": [...], "audio": [...], "total": 5}
```

#### `get_media_info(media_id) → dict | None`

获取媒体元数据（MediaDescriptor）。

#### `get_stats() → dict`

多模态记忆统计。

### MediaMemoryBridge — 多模态↔文本桥接

```python
bridge = MediaMemoryBridge(store=memory.store)

# 跨模态关联
bridge.link_media_to_text(media_id="img_001", memory_ids=["mem_001", "mem_002"])

# 注入多模态结果到常规检索
enriched = bridge.enrich_recall(recall_results)
```

---

## 分布式向量存储 API（v9.0）

### DistributedVectorStore — 水平扩展向量存储

```python
from distributed_store import DistributedVectorStore, InMemoryShard, HashRing

store = DistributedVectorStore(
    nodes=["node1", "node2", "node3"],
    shard_factory=InMemoryShard,
    replicas=3,         # 每份数据 3 副本
    write_quorum=2,     # 写入需 2/3 确认
    read_quorum=2,      # 读取需 2/3 确认
)
```

#### `add(key, vector, metadata=None) → dict`

写入向量（一致性哈希路由 + quorum 复制）。

#### `add_batch(items) → int`

批量写入。items: `[(key, vector, metadata), ...]`。

#### `search(query_vector, top_k=10, filter_fn=None) → list[dict]`

搜索：聚合多节点结果 + RRF 排序。

#### `delete(key) → bool`

删除向量（多节点同步）。

#### `count() → int`

向量总数。

#### `health() → dict`

节点健康检查（心跳 + 故障检测）。

```python
status = store.health()
# → {"healthy_nodes": ["node1", "node3"], "unhealthy_nodes": ["node2"], "total": 3}
```

#### `rebalance() → dict`

故障节点数据自动迁移至健康节点。

#### `get_distribution() → dict`

数据分布统计（每节点 item 数 + 偏差率）。

#### `remove_node(node_name) → dict`

移除节点（数据自动迁移）。

### HashRing — 一致性哈希环

```python
ring = HashRing(virtual_nodes=256)  # 每节点 256 虚拟节点

ring.add_node("shard-1")
ring.add_node("shard-2")
node = ring.get_node("mem_001")  # 确定性路由
distribution = ring.get_distribution()  # 负载分布统计
```

---

## 合规守护 API（ComplianceGuard）

### ComplianceGuard — PII 与敏感信息扫描

自动扫描记忆内容中的 PII、金融、健康和凭证信息，支持检测和脱敏。

```python
from agent_memory.enterprise.compliance_guard import ComplianceGuard, ComplianceResult

guard = ComplianceGuard()
```

#### `scan(content) → ComplianceResult`

扫描内容中的合规问题，返回检测结果和脱敏后的内容。

```python
result = guard.scan("我的手机号是13812345678，工资：15000")
# → ComplianceResult(
#     is_compliant=False,
#     detected_types=["phone", "salary"],
#     risk_level="high",
#     redacted_content="我的手机号是[REDACTED_PHONE]，工资：[REDACTED_SALARY]",
#     details=["phone: 1 occurrence(s)", "salary: 1 occurrence(s)"]
# )
```

**ComplianceResult 字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_compliant` | bool | 是否合规（`risk_level` 为 low/medium 时为 True） |
| `detected_types` | list[str] | 检测到的敏感信息类型列表 |
| `risk_level` | str | 风险等级：low / medium / high / critical |
| `redacted_content` | str | 脱敏后的内容 |
| `details` | list[str] | 各类型检测详情 |

**检测类别与风险等级：**

| 类别 | 正则匹配目标 | 风险等级 |
|------|------------|---------|
| `phone` | 中国手机号（1[3-9]开头的11位数字） | medium |
| `email` | 邮箱地址 | medium |
| `id_card` | 身份证号（18位） | **critical** |
| `bank_card` | 银行卡号（16-19位） | **critical** |
| `credit_card` | 信用卡号 | **critical** |
| `password` | 密码字段（密码/password/pwd 等） | **critical** |
| `api_key` | API Key/Token/Secret | **critical** |
| `salary` | 薪资/工资信息 | **high** |
| `medical` | 医疗/诊断/药物信息 | **high** |

**风险等级判定规则：**

| 条件 | 风险等级 | is_compliant |
|------|---------|-------------|
| 无任何检测项 | low | True |
| 仅检测到 phone/email | medium | True |
| 检测到 salary 或 medical | high | False |
| 检测到 id_card/bank_card/credit_card/password/api_key | critical | False |

#### `redact(content, types=None) → str`

对指定类型的敏感信息进行脱敏。

```python
# 脱敏所有类型
redacted = guard.redact("联系 13812345678 或 test@example.com")
# → "联系 [REDACTED_PHONE] 或 [REDACTED_EMAIL]"

# 仅脱敏特定类型
redacted = guard.redact("手机13812345678，工资15000", types=["phone"])
# → "手机[REDACTED_PHONE]，工资15000"
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `content` | str | 待脱敏的文本内容 |
| `types` | list[str] \| None | 要脱敏的类型列表，`None` 表示所有类型 |

**返回：** 脱敏后的字符串，匹配项替换为 `[REDACTED_{TYPE_UPPER}]` 格式。

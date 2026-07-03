# @tencentdb-agent-memory/memory-tencentdb

**Four-layer memory system plugin for [OpenClaw](https://github.com/openclaw/openclaw).**

为 AI Agent 提供长期记忆能力。通过 L0→L1→L2→L3 四层渐进式管线，自动将对话内容提炼为结构化记忆、场景块和用户画像。支持纯本地 SQLite 和远端腾讯云向量数据库（TCVDB）两种存储后端。

## ✨ 核心功能

- **L0 — 对话录制**：自动捕获每轮对话原始消息，IMemoryStore + JSONL 双写
- **L1 — 记忆提取**：由 LLM 从对话中提取结构化记忆，支持向量去重与冲突检测
- **L2 — 场景归纳**：基于 L1 记忆自动归纳场景块（Scene Block），由 LLM 增量提取
- **L3 — 用户画像**：基于场景块自动生成/更新用户画像（Persona）
- **自动召回（Auto-Recall）**：对话开始前自动注入相关记忆和用户画像到上下文
- **多后端存储**：支持 `sqlite`（本地 SQLite + sqlite-vec）和 `tcvdb`（腾讯云向量数据库，服务端 embedding + hybridSearch）
- **BM25 稀疏向量**：内置 BM25 编码器（tcvdb-text），支持中英文混合搜索
- **关键词+向量混合搜索**：hybrid（关键词 + 向量 RRF 融合）搜索策略
- **语义搜索工具**：Agent 可调用 `tdai_memory_search`（L1 记忆搜索）和 `tdai_conversation_search`（L0 对话搜索）
- **Seed CLI**：`openclaw memory-tdai seed` 命令，支持导入历史对话数据（详见 [CLI 文档](src/cli/README.md)）
- **Session 隔离**：不同渠道/Agent 的对话独立调度、独立提取
- **本地数据清理**：可配置 L0/L1 数据保留天数，定时自动清理过期文件
- **Manifest 元数据**：数据目录自动生成 `.metadata/manifest.json`，记录 store 绑定信息和 seed 运行记录
- **支持零配置**：支持零配置工作，简单易用

## 🏗️ 关键原理

```
对话开始
  → Auto-Recall: 向量/混合搜索相关记忆 + 加载 Persona → 注入系统上下文

对话结束
  → Auto-Capture (L0): 录制对话消息 → IMemoryStore (SQLite/TCVDB) + JSONL 双写
  → Pipeline Scheduler: 达到 N 轮后按序触发 L1 → L2 → L3
     ├── L1: LLM 提取结构化记忆 + 向量去重 → 写入 JSONL + IMemoryStore
     ├── L2: LLM 归纳场景块 → Markdown 文件
     └── L3: LLM 生成/更新用户画像 → persona.md
```

### 数据目录结构

```
<pluginDataDir>/
├── conversations/     — L0 每日 JSONL 分片（每行一条消息）
├── records/           — L1 每日 JSONL 分片（提取的记忆）
├── scene_blocks/      — L2 场景块 .md 文件
├── vectors.db         — SQLite + vec0 向量数据库（仅 storeBackend=sqlite）
├── .metadata/
│   ├── manifest.json  — 数据目录元数据（store 绑定、seed 信息）
│   └── checkpoint.json
└── .backup/           — 滚动备份（persona, scene_blocks）
```

## 🚀 Quick Start（Docker）

使用预构建的 Docker 镜像，一行命令即可启动带记忆能力的 Hermes Agent：

```bash
docker run -d \
  --name hermes-memory \
  --restart unless-stopped \
  -p 8420:8420 \
  -e MODEL_API_KEY="your-api-key" \
  -e MODEL_BASE_URL="https://api.lkeap.cloud.tencent.com/v1" \
  -e MODEL_NAME="deepseek-v3.2" \
  -e MODEL_PROVIDER="custom" \
  -v hermes_data:/opt/data \
  agentmemory/hermes-memory:latest
```

镜像支持 `linux/amd64` 和 `linux/arm64` 架构。内置腾讯云 DeepSeek-V3.2 默认值，如使用该模型可省略 `MODEL_BASE_URL`/`MODEL_NAME`/`MODEL_PROVIDER`，只传 `MODEL_API_KEY` 即可。

### 环境变量

#### 统一模型配置（Hermes + TDAI 共用）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MODEL_API_KEY` | - | LLM API Key（**必填**） |
| `MODEL_BASE_URL` | `https://api.lkeap.cloud.tencent.com/v1` | LLM API 地址 |
| `MODEL_NAME` | `deepseek-v3.2` | 模型名称 |
| `MODEL_PROVIDER` | `custom` | 模型 provider：`custom` / `openrouter` / `anthropic` / `openai` / `gemini` |

#### 服务配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TDAI_GATEWAY_PORT` | `8420` | Gateway 端口 |
| `TDAI_GATEWAY_HOST` | `0.0.0.0` | Gateway 绑定地址 |
| `TDAI_DATA_DIR` | `/opt/data/tdai-memory` | 记忆数据目录 |
| `HERMES_HOME` | `/opt/data` | Hermes 数据目录 |

### 验证运行

```bash
# 验证 Gateway 健康状态
curl http://localhost:8420/health

# 进入 Hermes 对话
docker exec -it hermes-memory hermes

# 查看容器日志
docker logs -f hermes-memory
```

> 更多配置选项和集成说明请参考下文。

---

## 📋 前置依赖

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| [OpenClaw](https://github.com/nicepkg/openclaw) | `>= 2026.3.13` | 宿主框架，提供插件 SDK 及 Gateway 运行环境 |
| [Node.js](https://nodejs.org/) | `>= 22.16.0` | 运行时环境 |
| [`node-llama-cpp`](https://github.com/withcatai/node-llama-cpp) | `^3.16.2` | 本地 embedding 模型（GGUF 格式），提供离线向量化能力（仅 sqlite 后端需要） |
| [`sqlite-vec`](https://github.com/asg017/sqlite-vec) | `0.1.7-alpha.2` | SQLite 向量搜索扩展（仅 sqlite 后端需要） |
| [`tcvdb-text`](../../../packages/tcvdb-text) | `workspace:*` | BM25 稀疏向量编码器，支持中英文分词（仅 tcvdb 后端需要） |

> 默认场景下无需安装 `node-llama-cpp`。如需启用本地 embedding，再在宿主环境手动安装该包。

## 📦 安装

```bash
# 安装插件
openclaw plugins install @tencentdb-agent-memory/memory-tencentdb

# 更新插件
openclaw plugins update memory-tencentdb

# 卸载插件
openclaw plugins uninstall memory-tencentdb
```

安装完成后，**重启 Gateway** 使插件生效：

```bash
openclaw gateway restart
```

## ⚙️ 配置

插件配置位于 `~/.openclaw/openclaw.json` 中 `memory-tencentdb` 字段下。**所有字段均有合理默认值，零配置即可使用。**

### 最小配置

安装启用后即为该状态（默认使用本地 SQLite 后端）：

```json
{
  "memory-tencentdb": {
    "enabled": true
  }
}
```

> **⚠️ 重要：`allowPromptInjection` 必须为 `true`**
>
> 本插件通过 `before_prompt_build` hook 在对话开始前将召回的记忆注入系统上下文。
> OpenClaw v2026.4.5+ 新增了 `allowPromptInjection` 安全控制，当该选项设为 `false` 时，
> `before_prompt_build` hook 将被**完全阻止注册**，导致记忆召回静默失效（不会报错，仅有 warn 日志）。
>
> 请确保 `openclaw.json` 中**不要**将该插件的 `allowPromptInjection` 设为 `false`：
>
> ```jsonc
> // ❌ 错误配置 — 会导致记忆召回完全失效
> {
>   "plugins": {
>     "entries": {
>       "memory-tencentdb": {
>         "hooks": { "allowPromptInjection": false }
>       }
>     }
>   }
> }
>
> ```

### TCVDB 后端配置

使用腾讯云向量数据库作为存储后端：

```json
{
  "memory-tencentdb": {
    "storeBackend": "tcvdb",
    "tcvdb": {
      "url": "http://your-vdb-instance:8100",
      "apiKey": "your-api-key",
      "database": "my_memory_db",
      "alias": "生产环境"
    }
  }
}
```

### 完整配置

用户可按需配置，提升使用体验：

```json
{
  "memory-tencentdb": {
    "storeBackend": "sqlite",
    "capture": {
      "enabled": true,
      "excludeAgents": ["bench-judge-*"],
      "l0l1RetentionDays": 90,
      "allowAggressiveCleanup": false,
      "cleanTime": "03:00"
    },
    "extraction": {
      "enabled": true,
      "enableDedup": true,
      "maxMemoriesPerSession": 20,
      "model": "provider/model-name"
    },
    "persona": {
      "triggerEveryN": 50,
      "maxScenes": 15,
      "backupCount": 3,
      "sceneBackupCount": 10,
      "model": "provider/model-name"
    },
    "pipeline": {
      "everyNConversations": 5,
      "enableWarmup": true,
      "l1IdleTimeoutSeconds": 600,
      "l2DelayAfterL1Seconds": 10,
      "l2MinIntervalSeconds": 900,
      "l2MaxIntervalSeconds": 3600,
      "sessionActiveWindowHours": 24
    },
    "recall": {
      "enabled": true,
      "maxResults": 5,
      "scoreThreshold": 0.3,
      "strategy": "hybrid",
      "timeoutMs": 5000
    },
    "embedding": {
      "enabled": true,
      "provider": "none",
      "baseUrl": "https://your-embedding-endpoint/v1",
      "apiKey": "your-api-key",
      "model": "text-embedding-3-small",
      "dimensions": 1536,
      "conflictRecallTopK": 5,
      "maxInputChars": 5000,
      "timeoutMs": 10000
    },
    "tcvdb": {
      "url": "http://your-vdb-instance:8100",
      "username": "root",
      "apiKey": "your-api-key",
      "database": "my_memory_db",
      "alias": "生产环境",
      "embeddingModel": "bge-large-zh",
      "timeout": 10000
    },
    "bm25": {
      "enabled": true,
      "language": "zh"
    }
  }
}
```

### 配置说明

#### storeBackend — 存储后端

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `storeBackend` | string | `"sqlite"` | 存储后端：`sqlite`（本地 SQLite + sqlite-vec）或 `tcvdb`（腾讯云向量数据库） |

#### capture — 对话捕获 (L0)

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用自动对话捕获 |
| `excludeAgents` | string[] | `[]` | Agent 排除 glob 模式列表，匹配的 agent 不参与捕获/召回/调度 |
| `l0l1RetentionDays` | number | `0` | L0/L1 本地文件保留天数。`0` = 不清理；非 0 时需 >= 3（除非开启 `allowAggressiveCleanup`） |
| `allowAggressiveCleanup` | boolean | `false` | 是否允许 1-2 天的高风险清理配置 |
| `cleanTime` | string | `"03:00"` | 每日清理执行时间（HH:mm 格式） |

#### extraction — 记忆提取 (L1)

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用后台记忆提取 |
| `enableDedup` | boolean | `true` | 启用 L1 智能去重（基于向量相似度或关键词进行冲突检测） |
| `maxMemoriesPerSession` | number | `20` | 单次 L1 提取每 session 最大记忆条数 |
| `model` | string | *(OpenClaw 默认模型)* | 提取使用模型（格式：`provider/model`），未填写时使用 OpenClaw 默认模型 |

#### pipeline — 管线调度 (L1→L2→L3)

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `everyNConversations` | number | `5` | 每 N 轮对话触发一次 L1 批处理 |
| `enableWarmup` | boolean | `true` | Warm-up 模式：新 session 从 1 轮触发开始，每次 L1 后翻倍（1→2→4→...→N） |
| `l1IdleTimeoutSeconds` | number | `600` | 用户停止对话后多久触发 L1（秒） |
| `l2DelayAfterL1Seconds` | number | `10` | L1 完成后延迟多久触发 L2（秒） |
| `l2MinIntervalSeconds` | number | `900` | 同一 session 两次 L2 的最小间隔（秒） |
| `l2MaxIntervalSeconds` | number | `3600` | 活跃 session 的 L2 最大轮询间隔（秒） |
| `sessionActiveWindowHours` | number | `24` | 超过此时间不活跃的 session 停止 L2 轮询 |

#### recall — 记忆召回

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用对话前自动召回 |
| `maxResults` | number | `5` | 召回最大结果数 |
| `scoreThreshold` | number | `0.3` | 最低分数阈值 |
| `strategy` | string | `"hybrid"` | 搜索策略：`keyword`（关键词）、`embedding`（向量）、`hybrid`（混合 RRF 融合，推荐） |
| `timeoutMs` | number | `5000` | 整体召回超时（毫秒）。超时后跳过记忆注入并输出 warn 日志，避免阻塞用户对话 |

#### embedding — 向量搜索（仅 sqlite 后端）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用向量搜索（若 `provider="none"`，则实际会被禁用） |
| `provider` | string | `"none"` | Embedding 服务提供者：`none` 表示禁用向量；其他值（如 `openai`、`deepseek`）按 OpenAI 兼容远端服务处理 |
| `baseUrl` | string | — | API Base URL（远端模式必填） |
| `apiKey` | string | — | API Key（远端模式必填） |
| `model` | string | — | 模型名称（远端模式必填） |
| `dimensions` | number | — | 向量维度（远端模式必填，需与模型匹配） |
| `conflictRecallTopK` | number | `5` | 冲突检测时召回 Top-K 数 |
| `maxInputChars` | number | `5000` | Embedding 输入文本最大字符数，超出时截断并打印警告日志（适合大多数模型的 token 上限） |
| `timeoutMs` | number | `10000` | 单次 embedding API 调用超时（毫秒）。超时后该次 embedding 请求中止，不重试 |

#### tcvdb — 腾讯云向量数据库（仅 storeBackend=tcvdb）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | — | 实例 URL（必填，如 `http://10.0.1.1:8100`） |
| `username` | string | `"root"` | 账户名 |
| `apiKey` | string | — | API Key（必填） |
| `database` | string | — | 数据库名（必填，需唯一） |
| `alias` | string | — | 用户友好别名（可选，记录在 manifest 中便于识别） |
| `embeddingModel` | string | `"bge-large-zh"` | 服务端 embedding 模型 |
| `timeout` | number | `10000` | 请求超时（毫秒） |

#### bm25 — BM25 稀疏向量编码

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `true` | 是否启用 BM25 稀疏向量编码 |
| `language` | string | `"zh"` | 分词语言：`zh`（中文 jieba）或 `en`（英文） |
| `maxInputChars` | number | `5000` | Embedding 输入文本最大字符数，超出时截断并打印警告日志（适合大多数模型的 token 上限） |
| `timeoutMs` | number | `10000` | 单次 embedding API 调用超时（毫秒）。超时后该次 embedding 请求中止，不重试 |

#### persona — 场景归纳与用户画像 (L2/L3)

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `triggerEveryN` | number | `50` | 每 N 条新记忆触发一次画像生成 |
| `maxScenes` | number | `15` | 最大场景块数量 |
| `backupCount` | number | `3` | 画像备份保留数量 |
| `sceneBackupCount` | number | `10` | 场景块备份保留数量 |
| `model` | string | *(OpenClaw 默认模型)* | L2/L3 使用模型（格式：`provider/model`），未填写时使用 OpenClaw 默认模型 |

#### report — 指标上报

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `false` | 是否启用指标上报（通过 Gateway 日志输出结构化 METRIC JSON） |
| `type` | string | `"local"` | 上报方式：`local` 表示通过 logger 输出结构化 JSON 日志 |

## 🖥️ CLI 命令

插件提供 `openclaw memory-tdai` 命令空间，支持以下子命令：

### `seed` — 导入历史对话数据

将历史对话 JSON 文件导入到记忆管线中，完整执行 L0→L1→L2→L3 流程。

```bash
openclaw memory-tdai seed --input conversations.json [--output-dir ./output] [--config seed-config.json] [--yes]
```

详细用法、输入格式和配置覆盖机制请参阅 [CLI 文档](src/cli/README.md)。

## 🔧 Agent 工具

插件注册了两个 Agent 可调用的工具：

### `tdai_memory_search`

搜索用户的 L1 结构化长期记忆。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索查询 |
| `limit` | number | — | 返回结果上限（默认 5，最大 20） |
| `type` | string | — | 按记忆类型过滤：`persona` / `episodic` / `instruction` |
| `scene` | string | — | 按场景名过滤 |

### `tdai_conversation_search`

搜索 L0 原始对话历史。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索查询 |
| `limit` | number | — | 返回结果上限（默认 5，最大 20） |
| `session_key` | string | — | 按 session 过滤 |

## 📁 数据与日志

- **数据目录**：`~/.openclaw/memory-tdai/`（自动创建）
- **元数据**：`.metadata/manifest.json`（store 绑定、seed 运行记录）
- **Gateway 日志**：插件运行日志通过 `[memory-tdai]` 前缀标记，可在 Gateway 日志中搜索查看
- **配置文件**：`~/.openclaw/openclaw.json`

## 📄 License

[MIT](LICENSE)

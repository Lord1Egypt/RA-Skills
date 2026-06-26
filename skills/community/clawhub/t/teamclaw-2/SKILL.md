---
name: TeamClaw
description:
  A high-performance Agent subsystem designed for complex multi-agent orchestration (OASIS),automated computer use tasks, and real-time visual monitoring via a dedicated Web UI.
---

# TeamClaw — Agent 子系统 Skill

** 如果你是openclaw agent，请将自己作为Teamclaw的外部agent**

## 简介

TeamClaw 是一个多功能 AI Agent 服务，提供：

- **对话 Agent**：基于 LangGraph 的多工具 AI 助手，支持流式/非流式对话
- **OASIS 论坛**：多专家并行讨论/执行引擎，可编排多个 Agent 协作
- **定时调度**：基于 APScheduler 的任务调度中心
- **Bark 推送**：移动端推送通知
- **前端 Web UI**：完整的聊天界面

## Skill 脚本

所有脚本位于 `selfskill/scripts/`，统一通过 `run.sh` 入口调用，**全部非交互式**。

```
selfskill/scripts/
├── run.sh          # 主入口（start/stop/status/setup/add-user/configure）
├── adduser.py      # 非交互式用户创建
└── configure.py    # 非交互式 .env 配置管理
```

## 快速启动

所有命令在项目根目录下执行。

### 1. 首次部署

```bash
# 安装依赖
bash selfskill/scripts/run.sh setup

# 初始化配置文件
bash selfskill/scripts/run.sh configure --init

# 配置 LLM（必填）
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-your-key \
  LLM_BASE_URL=https://api.deepseek.com \
  LLM_MODEL=deepseek-chat

# 创建用户
bash selfskill/scripts/run.sh add-user system MySecurePass123
```

### 2. 启动/停止/状态

```bash
bash selfskill/scripts/run.sh start     # 后台启动
bash selfskill/scripts/run.sh status    # 检查状态
bash selfskill/scripts/run.sh stop      # 停止服务
```

### 3. 配置管理

```bash
# 查看当前配置（敏感值脱敏）
bash selfskill/scripts/run.sh configure --show

# 设置单项
bash selfskill/scripts/run.sh configure PORT_AGENT 51200

# 批量设置
bash selfskill/scripts/run.sh configure --batch TTS_MODEL=gemini-2.5-flash-preview-tts TTS_VOICE=charon
```

## 可配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `LLM_API_KEY` | LLM API 密钥（**必填**） | — |
| `LLM_BASE_URL` | LLM API 地址 | `https://api.deepseek.com` |
| `LLM_MODEL` | 模型名称 | `deepseek-chat` |
| `LLM_PROVIDER` | 厂商（google/anthropic/deepseek/openai，可自动推断） | 自动 |
| `LLM_VISION_SUPPORT` | 是否支持图片（可自动推断） | 自动 |
| `PORT_AGENT` | Agent 主服务端口 | `51200` |
| `PORT_SCHEDULER` | 定时调度端口 | `51201` |
| `PORT_OASIS` | OASIS 论坛端口 | `51202` |
| `PORT_FRONTEND` | Web UI 端口 | `51209` |
| `PORT_BARK` | Bark 推送端口 | `58010` |
| `TTS_MODEL` | TTS 模型（可选） | — |
| `TTS_VOICE` | TTS 声音（可选） | — |
| `OPENCLAW_API_URL` | OpenClaw 后端服务地址（完整路径，含 `/v1/chat/completions`） | `http://127.0.0.1:18789/v1/chat/completions` |
| `OPENCLAW_API_KEY` | OpenClaw 后端服务的 API Key（可选） | — |
| `OPENCLAW_SESSIONS_FILE` | OpenClaw sessions.json 文件的绝对路径（**使用 OpenClaw 时必须配置**） | `/projects/.moltbot/agents/main/sessions/sessions.json` |
| `INTERNAL_TOKEN` | 内部通信密钥（自动生成） | 自动 |

## 端口与服务

| 端口 | 服务 |
|------|------|
| 51200 | AI Agent 主服务 |
| 51201 | 定时调度 |
| 51202 | OASIS 论坛 |
| 51209 | Web UI |

## API 认证

### 方式 1：用户认证

```
Authorization: Bearer <user_id>:<password>
```

### 方式 2：内部 Token（服务间调用，推荐）

```
Authorization: Bearer <INTERNAL_TOKEN>:<user_id>
```

`INTERNAL_TOKEN` 首次启动自动生成，可通过 `configure --show-raw` 查看。

## 核心 API

**Base URL**: `http://127.0.0.1:51200`

### 对话（OpenAI 兼容）

```
POST /v1/chat/completions
Authorization: Bearer <token>

{"model":"mini-timebot","messages":[{"role":"user","content":"你好"}],"stream":true,"session_id":"my-session"}
```

### 系统触发（内部调用）

```
POST /system_trigger
X-Internal-Token: <INTERNAL_TOKEN>

{"user_id":"system","text":"请执行某任务","session_id":"task-001"}
```

### 终止会话

```
POST /cancel

{"user_id":"<user_id>","session_id":"<session_id>"}
```


## OASIS 四种运行模式（默认：讨论模式）

> 这里的“四个模式”是两组正交开关：
> - **讨论 vs 执行**：决定专家输出是“论坛式讨论/投票”，还是“工作流式执行/交付物”。
> - **同步 vs 脱离（detach）**：决定调用方是否阻塞等待结果。

### 1) 讨论模式 vs 执行模式

**讨论模式（discussion=true，默认）**
- 用途：多专家给出不同观点、利弊分析、争议点澄清，并可形成共识。
- 适用：方案评审、技术路线选择、需要“为什么”的问题。

**执行模式（discussion=false）**
- 用途：把 OASIS 当作编排器按计划顺序/并行完成任务，强调直接产出（代码/脚本/清单/定稿方案）。
- 适用：目标明确的交付任务，且不需要展开辩论。

### 2) 同步模式 vs 脱离模式（detach）

**同步（detach=false，默认）**
- 行为：调用 `post_to_oasis` 后等待完成，直接返回最终结果。
- 适用：任务较快、需要立刻拿到产物并继续迭代。

**脱离（detach=true）**
- 行为：立即返回 `topic_id`，后台继续运行/讨论；之后用 `check_oasis_discussion(topic_id)` 追踪进度与结果。
- 适用：多轮/多专家/耗时长/包含工具调用，不希望阻塞当前会话。

### 3) 自动选择规则（建议默认策略）

在未明确指定时，建议采用以下默认策略：

1. **默认 = 讨论 + 同步**
   - `discussion=true`
   - `detach=false`

2. 出现以下需求信号时，切换到 **执行模式**：
   - “直接给最终版 / 可复制粘贴 / 可执行脚本 / 只要结论不要讨论”
   - “按步骤生成 SOP / 清单 / 表格并定稿”

3. 出现以下需求信号时，切换到 **脱离模式**：
   - “后台跑 / 我一会儿再看 / 先给 topic_id”
   - 多专家并行、多轮（`max_rounds` 大）、或预计耗时长

### 4) 四种组合速查

| 组合 | 参数 | 返回 | 适用 |
|---|---|---|---|
| 讨论 + 同步（默认） | discussion=true, detach=false | 当场看到讨论与结论 | 决策/评审/收集观点 |
| 讨论 + 脱离 | discussion=true, detach=true | topic_id，稍后查 | 长讨论/多轮 |
| 执行 + 同步 | discussion=false, detach=false | 直接交付物 | 生成代码/方案/清单 |
| 执行 + 脱离 | discussion=false, detach=true | topic_id，稍后查 | 长执行/复杂流水线 |


## OASIS 四类智能体

OASIS 支持 **四种类型的智能体**，通过 `schedule_yaml` 中专家的 `name` 格式区分：

| # | 类型 | Name 格式 | 引擎类 | 说明 |
|---|------|-----------|--------|------|
| 1 | **Direct LLM** | `tag#temp#N` | `ExpertAgent` | 无状态单次 LLM 调用。每轮读取所有帖子 → 一次 LLM 调用 → 发布 + 投票。无跨轮记忆。`tag` 映射到预设专家名/人设，`N` 是实例编号（同一专家可多副本）。 |
| 2 | **Oasis Session** | `tag#oasis#id` | `SessionExpert` (oasis) | OASIS 管理的有状态 bot session。`tag` 映射到预设专家，首轮注入人设为 system prompt。Bot 跨轮保留对话记忆（增量上下文）。`id` 可为任意字符串，新 ID 首次使用时自动创建 session。 |
| 3 | **Regular Agent** | `Title#session_id` | `SessionExpert` (regular) | 连接到已有的 agent session（如 `助手#default`、`Coder#my-project`）。不注入身份——session 自身的 system prompt 定义 agent。适合将个人 bot session 带入讨论。 |
| 4 | **External API** | `tag#ext#id` | `ExternalExpert` | 直接调用任意 OpenAI 兼容外部 API（DeepSeek、GPT-4、Ollama、另一个 TeamClaw 实例等）。不经过本地 agent。外部服务假定有状态。支持通过 YAML `headers` 字段自定义请求头。 | 经典用途：和openclaw agent连接

### Session ID 格式

```
tag#temp#N           → ExpertAgent   (无状态, 直连LLM)
tag#oasis#<id>       → SessionExpert (oasis管理, 有状态bot)
Title#session_id     → SessionExpert (普通agent session)
tag#ext#<id>         → ExternalExpert (外部API，如openclaw agent)
```

**特殊后缀：**
- 在任意 session 名末尾追加 `#new` 可强制创建**全新 session**（ID 替换为随机 UUID，确保不复用）：
  - `creative#oasis#abc#new` → `#new` 被剥离，ID 替换为 UUID
  - `助手#my-session#new` → 同样处理

**Oasis session 约定：**
- Oasis session 通过 `session_id` 中的 `#oasis#` 标识（如 `creative#oasis#ab12cd34`）
- 存储在普通 Agent checkpoint DB（`data/agent_memory.db`）中，无独立存储
- 首次使用时自动创建，无需预创建
- `tag` 部分映射到预设专家配置以查找人设

### YAML 示例

```yaml
version: 1
plan:
  # Type 1: Direct LLM（无状态，快速）
  - expert: "creative#temp#1"
  - expert: "critical#temp#2"

  # Type 2: Oasis session（有状态，有记忆）
  - expert: "data#oasis#analysis01"
  - expert: "synthesis#oasis#new#new"   # 强制全新session

  # Type 3: Regular agent session（你现有的bot）
  - expert: "助手#default"
  - expert: "Coder#my-project"

  # Type 4: External API（DeepSeek, GPT-4等）
  - expert: "deepseek#ext#ds1"

  # Type 4: OpenClaw External API（本地 Agent 服务）
  - expert: "coder#ext#oc1"
    api_url: "http://127.0.0.1:23001/v1/chat/completions"
    model: "agent:main:test1"    # agent:<agent_name>:<session>，session 不存在时自动新建

  # 并行执行
  - parallel:
      - expert: "creative#temp#1"
        instruction: "从创新角度分析"
      - expert: "critical#temp#2"
        instruction: "从风险角度分析"

  # 全员发言 + 手动注入
  - all_experts: true
  - manual:
      author: "主持人"
      content: "请聚焦可行性"
```

### External API (Type 4) 详细配置

Type 4 外部 agent 支持在 YAML 步骤中提供额外配置字段：

```yaml
version: 1
plan:
  - expert: "分析师#ext#analyst"
    api_url: "https://api.deepseek.com"          # 必填：外部 API 的 base URL（自动补全为 /v1/chat/completions）
    api_key: "sk-xxx"                             # 必填：API key → Authorization: Bearer <key>
    model: "deepseek-chat"                        # 可选：模型名，默认 gpt-3.5-turbo
    headers:                                      # 可选：自定义 HTTP 请求头（key-value 字典）
      X-Custom-Header: "value"
```

**配置字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `api_url` | ✅ | 外部 API 地址，自动补全路径为 `/v1/chat/completions` |
| `api_key` | ❌ | 放到 `Authorization: Bearer <key>` header 中 |
| `model` | ❌ | 默认 `gpt-3.5-turbo` |
| `headers` | ❌ | 任意 key-value 字典，合并到 HTTP 请求头 |

**OpenClaw 专属配置：**

OpenClaw 是一个本地运行的 OpenAI 兼容 Agent 服务。在 `.env` 中设置好 OpenClaw 专属 endpoint 后，前端编排面板中拖入 OpenClaw 专家时会**自动填入** `api_url` 和 `api_key`，无需手动输入：

```bash
# 配置 OpenClaw endpoint 和 sessions 文件路径
bash selfskill/scripts/run.sh configure --batch \
  OPENCLAW_SESSIONS_FILE=/projects/.moltbot/agents/main/sessions/sessions.json \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENCLAW_API_KEY=your-openclaw-key-if-needed
```

> **⚠️ 注意：**
> - `OPENCLAW_SESSIONS_FILE` 是使用 OpenClaw 功能的**前提条件**，必须指向 OpenClaw 的 `sessions.json` 文件绝对路径。未配置时前端编排面板不会加载 OpenClaw sessions。
> - `OPENCLAW_API_URL` 应填写**完整路径**（含 `/v1/chat/completions`），系统会自动剥离后缀生成 base URL 填入 YAML。YAML 中的 `api_url` 字段只需要 base URL（如 `http://127.0.0.1:18789`），引擎会自动补全路径。
> - 如果你的 OpenClaw 服务运行在非默认端口，请务必修改这些配置。

**OpenClaw 的 `model` 字段格式：**

```
agent:<agent_name>:<session_name>
```

- `agent_name`：OpenClaw 中的 agent 名称，通常为 `main`
- `session_name`：会话名称，如 `test1`、`default` 等。**可以填入不存在的 session 名来自动新建**

示例：
- `agent:main:default` — 使用 main agent 的 default session
- `agent:main:test1` — 使用 main agent 的 test1 session（不存在则新建）
- `agent:main:code-review` — 使用 main agent 的 code-review session

**请求头组装逻辑：**
最终发出的请求头 = `Content-Type: application/json` + `Authorization: Bearer <api_key>`（如有） + YAML `headers` 中自定义的所有键值对。

---

## 独立使用 OASIS Server

OASIS Server（端口 51202）可以**独立于 Agent 主服务使用**。外部脚本、其他服务、或手动 curl 均可直接操作 OASIS 的全部功能，无需通过 MCP 工具或 Agent 对话。

**独立使用场景：**
- 从外部脚本自动发起多专家讨论/执行
- 调试 workflow 编排
- 将 OASIS 作为微服务集成到其他系统
- 管理专家、会话、workflow 等资源

**前提条件：**
- OASIS 服务已启动（`bash selfskill/scripts/run.sh start` 会同时启动所有服务）
- 所有接口使用 `user_id` 参数进行用户隔离（无需 Authorization header）

**API 概览：**

| 功能 | 方法 | 路径 |
|------|------|------|
| 列出专家 | GET | `/experts?user_id=xxx` |
| 创建自定义专家 | POST | `/experts/user` |
| 更新/删除自定义专家 | PUT/DELETE | `/experts/user/{tag}` |
| 列出 oasis sessions | GET | `/sessions/oasis?user_id=xxx` |
| 保存 workflow | POST | `/workflows` |
| 列出 workflows | GET | `/workflows?user_id=xxx` |
| YAML → Layout | POST | `/layouts/from-yaml` |
| 创建讨论/执行 | POST | `/topics` |
| 查看讨论详情 | GET | `/topics/{topic_id}?user_id=xxx` |
| 获取结论（阻塞） | GET | `/topics/{topic_id}/conclusion?user_id=xxx&timeout=300` |
| SSE 实时流 | GET | `/topics/{topic_id}/stream?user_id=xxx` |
| 取消讨论 | DELETE | `/topics/{topic_id}?user_id=xxx` |
| 列出所有话题 | GET | `/topics?user_id=xxx` |

> 这些接口与 MCP 工具共享同一后端实现，行为完全一致。

---

### OASIS 讨论/执行

```
POST http://127.0.0.1:51202/topics

{"question":"讨论主题","user_id":"system","max_rounds":3,"discussion":true,"schedule_file":"...","schedule_yaml":"...","callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}
```

注意优先使用schedule_yaml避免重复输入yaml，这是yaml工作流文件的绝对路径，一般在/XXXXX/TeamClaw/data/user_files/username下

### 外部 curl 参与 OASIS 服务器（完整方法）

OASIS 服务器（端口 51202）除了供 MCP 工具调用外，也支持直接 curl 操作，便于外部脚本或调试。所有接口均使用 `user_id` 参数进行用户隔离。

#### 1. 专家管理
```bash
# 列出所有专家（公共 + 用户自定义）
curl 'http://127.0.0.1:51202/experts?user_id=xinyuan'

# 创建自定义专家
curl -X POST 'http://127.0.0.1:51202/experts/user' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"产品经理","tag":"pm","persona":"你是一个经验丰富的产品经理，擅长需求分析和产品规划","temperature":0.7}'

# 更新自定义专家
curl -X PUT 'http://127.0.0.1:51202/experts/user/pm' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","persona":"更新后的专家描述"}'

# 删除自定义专家
curl -X DELETE 'http://127.0.0.1:51202/experts/user/pm?user_id=xinyuan'
```

#### 2. 会话管理
```bash
# 列出 OASIS 管理的专家会话（含 #oasis# 的 session）
curl 'http://127.0.0.1:51202/sessions/oasis?user_id=xinyuan'
```

#### 3. Workflow 管理
```bash
# 列出用户保存的 workflows
curl 'http://127.0.0.1:51202/workflows?user_id=xinyuan'

# 保存 workflow（自动生成 layout）
curl -X POST 'http://127.0.0.1:51202/workflows' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"trio_discussion","schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","description":"三人讨论","save_layout":true}'
```

#### 4. Layout 生成
```bash
# 从 YAML 生成 layout
curl -X POST 'http://127.0.0.1:51202/layouts/from-yaml' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","yaml_source":"version:1\nplan:\n - expert: \"creative#temp#1\"","layout_name":"trio_layout"}'
```

#### 5. 讨论/执行
```bash
# 创建讨论话题（同步等待结论）
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"讨论主题","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true}'

# 创建讨论话题（异步，返回 topic_id）
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"讨论主题","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true,"callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}'

# 查看讨论详情
curl 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# 获取讨论结论（阻塞等待）
curl 'http://127.0.0.1:51202/topics/{topic_id}/conclusion?user_id=xinyuan&timeout=300'

# 取消讨论
curl -X DELETE 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# 列出所有讨论话题
curl 'http://127.0.0.1:51202/topics?user_id=xinyuan'
```

#### 6. 实时流
```bash
# SSE 实时更新流（讨论模式）
curl 'http://127.0.0.1:51202/topics/{topic_id}/stream?user_id=xinyuan'
```

**保存位置：**
- Workflows (YAML): `data/user_files/{user}/oasis/yaml/{file}.yaml`（画布布局从 YAML 实时转换，不再单独存储 layout JSON）
- 用户自定义专家: `data/oasis_user_experts/{user}.json`
- 讨论记录: `data/oasis_topics/{user}/{topic_id}.json`

**注意：** 这些接口与 MCP 工具 `list_oasis_experts`、`add_oasis_expert`、`update_oasis_expert`、`delete_oasis_expert`、`list_oasis_sessions`、`set_oasis_workflow`、`list_oasis_workflows`、`yaml_to_layout`、`post_to_oasis`、`check_oasis_discussion`、`cancel_oasis_discussion`、`list_oasis_topics` 共享同一后端实现，确保行为一致。

## 案例配置参考

以下是一份实际运行的配置示例（敏感信息已脱敏）：

```bash
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx4c74 \
  LLM_BASE_URL=https://deepseek.com \
  LLM_MODEL=deepseek-chat \
  LLM_VISION_SUPPORT=true \
  TTS_MODEL=gemini-2.5-flash-preview-tts \
  TTS_VOICE=charon \
  PORT_AGENT=51200 \
  PORT_SCHEDULER=51201 \
  PORT_OASIS=51202 \
  PORT_FRONTEND=51209 \
  PORT_BARK=58010 \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENAI_STANDARD_MODE=false
bash selfskill/scripts/run.sh add-user system <your-password>
```

配置完成后 `configure --show` 输出：

```
  PORT_SCHEDULER=51201
  PORT_AGENT=51200
  PORT_FRONTEND=51209
  PORT_OASIS=51202
  OASIS_BASE_URL=http://127.0.0.1:51202
  PORT_BARK=58010
  INTERNAL_TOKEN=f1aa****57e7          # 自动生成，勿泄露
  LLM_API_KEY=sk-7****4c74
  LLM_BASE_URL=https://deepseek.com
  LLM_MODEL=deepseek-chat
  LLM_VISION_SUPPORT=true
  TTS_MODEL=gemini-2.5-flash-preview-tts
  TTS_VOICE=charon
  OPENAI_STANDARD_MODE=false
```

> 说明：`INTERNAL_TOKEN` 首次启动自动生成，`PUBLIC_DOMAIN` / `BARK_PUBLIC_URL` 由 tunnel 自动写入，无需手动配置。

## 典型使用流程

```bash
cd /home/avalon/TeamClaw

# 首次配置
bash selfskill/scripts/run.sh setup
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch LLM_API_KEY=sk-xxx LLM_BASE_URL=https://api.deepseek.com LLM_MODEL=deepseek-chat
bash selfskill/scripts/run.sh add-user system MyPass123

# 启动
bash selfskill/scripts/run.sh start

# 调用 API
curl -X POST http://127.0.0.1:51200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer system:MyPass123" \
  -d '{"model":"mini-timebot","messages":[{"role":"user","content":"你好"}],"stream":false,"session_id":"default"}'

# 停止
bash selfskill/scripts/run.sh stop
```

## 注意事项

- 所有 skill 脚本位于 `selfskill/scripts/`，不影响项目原有功能
- 通过 PID 文件管理进程，`start` 支持幂等调用
- `INTERNAL_TOKEN` 勿泄露
- 日志路径: `logs/launcher.log`

- 一定要告诉用户如何开启可视化界面，以及如何登录到进行讨论等工作的账号
- openclaw session file路径可以综合案例路径和当前skill路径推理得到。假如你是openclaw agent，一定要人类完成完整的openclaw相关配置

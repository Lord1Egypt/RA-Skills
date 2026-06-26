# xihe-jianmu-ipc

> **命名由来 / Etymology** — 遵循曦和项目三段式命名规范 `xihe-{隐喻}-{功能}`：
>
> - **xihe（曦和）** — 品牌。源自中国神话中的太阳女神曦和 / Brand. Xihe, the sun goddess in Chinese mythology
> - **jianmu（建木）** — 隐喻。建木是上古神话中天地之间的通天神树，诸神借之往来天地、沟通上下。多个 AI 会话之间的通信如建木般无声连通 / Metaphor. Jiànmù is the mythical World Tree bridging heaven and earth in ancient Chinese mythology — gods traveled between realms through it in silence. IPC messages flow between AI sessions like spirits through the World Tree
> - **ipc** — 功能。进程间实时通信 / Function. Real-time inter-process communication

多 AI 会话实时通信中枢——WebSocket 消息路由 + MCP 集成 + Channel 推送唤醒。

Real-time communication hub for AI coding sessions — WebSocket message routing + MCP integration + Channel push notifications.

为需要多个 AI agent 协作而非各自为战的开发者而建。

Built for developers who need multiple AI agents to collaborate, not work in isolation.

由 [Xihe AI](https://github.com/xihe-forge) 锻造，面向所有需要跨 AI 会话协同的开发者。
Forged by [Xihe AI](https://github.com/xihe-forge), for developers who need real coordination across AI sessions.

---

## 为什么存在：Token 成本问题 / Why This Exists: The Token Cost Problem

多 agent 协作的标准路径——让 LLM 充当路由器，通过 Gateway 中转上下文——代价极高。每次跨 session 通信都会触发完整的 agent run，重新加载整个 JSONL 对话记录。随着对话变长，token 消耗是 O(N²) 累积的。

The standard path for multi-agent coordination — routing messages through the LLM, rebuilding context at every hop — is expensive by design. Every inter-session message triggers a full agent run that reloads the entire JSONL transcript. As conversations grow, token costs scale O(N²) cumulatively.

已有记录的真实代价 / Documented real-world costs:

- Claude Code issue #4911: sub-agent consumed **160K tokens** for a task that took 2–3K when done directly
- Claude Code issue #27645: *"Subagents don't share context — they re-read and re-analyze everything. 5–10x more token-efficient to do direct edits."*
- Claude Code issue #18240: **296K/200K tokens** (148% context overflow) after a subagent returned
- ICLR 2026 research: ~30% of tokens in multi-agent operations are consumed unnecessarily by context reconstruction
- Anthropic's own research: multi-agent uses **15× more tokens** than equivalent single-agent work

**建木的思路 / The Jianmu approach**: 不让 LLM 做路由，让哑管道做路由。消息通过 WebSocket 直接送达目标 session，LLM 只看到最终消息，看不到路由历史。每条消息的 token 开销约 50 tokens，与对话深度无关。

**The Jianmu approach**: route through a dumb pipe, not through the LLM. Messages travel over WebSocket directly to the target session. The LLM sees only the final message — not the routing history. Token cost per message: ~50 tokens, regardless of conversation depth.

---

## 架构 / Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Hub (hub.mjs)                        │
│           WebSocket server + HTTP API on :3179              │
│  - Session registry (name → ws connection)                  │
│  - Offline inbox with TTL-based cleanup                     │
│  - Topic pub/sub fanout                                     │
│  - Heartbeat / auto-reconnect                               │
└──────────┬───────────────────────┬──────────────────────────┘
           │ ws://localhost:3179   │ http://localhost:3179
           │                       │
 ┌─────────▼──────────┐  ┌────────▼────────────────────────┐
 │  MCP Server        │  │  HTTP API                       │
 │  (mcp-server.mjs)  │  │  POST /send  (online/buffered)  │
 │                    │  │  GET  /health                   │
 │  Claude Code &     │  │  GET  /sessions                 │
 │  OpenClaw load     │  │                                 │
 │  via stdio MCP     │  │  Any HTTP client: Codex,        │
 │  protocol          │  │  curl, scripts, CI pipelines    │
 └─────────┬──────────┘  └─────────────────────────────────┘
           │
 ┌─────────▼──────────────────────────────────────────────┐
 │  Channel (claude/channel capability)                    │
 │  Push incoming messages to Claude Code as              │
 │  <channel> notifications — wakes idle sessions         │
 └────────────────────────────────────────────────────────┘
           │
 ┌─────────▼──────────────────────────────────────────────┐
 │  OpenClaw Adapter                                       │
 │  Outbound: Hub calls /v1/chat/completions on the        │
 │  Gateway when a message targets an OpenClaw session     │
 │  Inbound:  OpenClaw loads mcp-server.mjs via            │
 │  openclaw.json — ipc_send reaches any connected tool    │
 └────────────────────────────────────────────────────────┘
```

---

## 快速开始 / Quick Start

### Claude Code 用户 / For Claude Code Users

**1. 安装 / Install**

```bash
npm install -g xihe-jianmu-ipc
# 或直接从仓库运行 / or run directly from the repo:
git clone https://github.com/xihe-forge/xihe-jianmu-ipc
cd xihe-jianmu-ipc
npm install
```

**2. 在项目 `.mcp.json` 中添加配置 / Add to `.mcp.json` in your project**

Session 1 (main):

```json
{
  "mcpServers": {
    "ipc": {
      "command": "node",
      "args": ["/path/to/xihe-jianmu-ipc/mcp-server.mjs"],
      "env": {
        "IPC_NAME": "main"
      }
    }
  }
}
```

Session 2 (worker):

```json
{
  "mcpServers": {
    "ipc": {
      "command": "node",
      "args": ["/path/to/xihe-jianmu-ipc/mcp-server.mjs"],
      "env": {
        "IPC_NAME": "worker"
      }
    }
  }
}
```

**3. Hub 自动启动 / The hub starts automatically**

第一个 MCP 会话连接时 Hub 自动启动（`IPC_HUB_AUTOSTART=true` 为默认值）。也可手动启动：

The hub starts automatically when the first MCP session connects (`IPC_HUB_AUTOSTART=true` by default). Or start it manually:

```bash
node hub.mjs
```

**4. 发送消息 / Send messages**

From the `main` session:
```
ipc_send(to="worker", content="Start processing task A")
```

Incoming messages arrive in the `worker` session as `<channel>` notifications that wake idle sessions.

**5. Windows PowerShell 快捷方式（可选）/ Windows PowerShell shortcut (optional)**

```powershell
# 安装 ipc 函数到 PowerShell profile / Install the `ipc` function into your PowerShell profile:
.\bin\install.ps1

# 用 ipc 命令打开 Claude Code 会话 / Open Claude Code sessions with:
ipc main
ipc worker
```

---

### OpenClaw 用户 / For OpenClaw Users

**1. 安装包 / Install the package**

```bash
npm install xihe-jianmu-ipc
```

**2. 添加到 `openclaw.json` / Add to `openclaw.json`**

```json
{
  "mcp": {
    "servers": {
      "xihe-jianmu-ipc": {
        "command": "node",
        "args": ["node_modules/xihe-jianmu-ipc/mcp-server.mjs"],
        "env": {
          "IPC_NAME": "openclaw",
          "IPC_AUTH_TOKEN": "your-shared-secret",
          "OPENCLAW_URL": "http://localhost:3000",
          "OPENCLAW_TOKEN": "your-openclaw-token"
        }
      }
    }
  }
}
```

**3. 在 OpenClaw 中使用 IPC 工具 / Use IPC tools from within OpenClaw**

OpenClaw can now reach any connected session:

```
ipc_send(to="claude-main", content="Login failure detected, need attention")
ipc_sessions()  // see what tools are connected
```

**4. ClawHub 可用性 / ClawHub availability**

`xihe-jianmu-ipc` skill 已在 ClawHub 上线。在 OpenClaw 内搜索 `xihe-jianmu-ipc` 即可安装。由于包含网络通信代码，安装时可能需要确认安全提示。

The `xihe-jianmu-ipc` skill is available in ClawHub. Search for `jianmu` to install it directly from within OpenClaw.

双向通信已验证 / Bidirectional OpenClaw ↔ Claude Code communication has been tested and verified:
- OpenClaw → Hub → Claude Code: delivered via WebSocket, wakes Claude Code via Channel notification
- Claude Code → Hub → OpenClaw: Hub calls `/v1/chat/completions`, OpenClaw processes and replies

---

## IPC 工具（MCP）/ IPC Tools (MCP)

以下工具在任意连接到 Hub 的会话中均可使用——Claude Code、OpenClaw 或任意支持 MCP 的工具。

These tools are available inside any session connected to the hub — Claude Code, OpenClaw, or any MCP-capable tool.

### `ipc_send`

向指定 session 或广播给所有 session 发送消息。
Send a message to a named session or broadcast to all.

| Param | Type | Required | Description |
|---|---|---|---|
| `to` | string | yes | Target session name, or `*` for broadcast |
| `content` | string | yes | Message content |
| `topic` | string | no | Optional topic tag for pub/sub fanout |

```
ipc_send(to="worker", content="your task is done")
ipc_send(to="*", content="shutdown signal", topic="control")
```

目标 session 离线时，消息会被缓冲（基于 TTL），在其重连时投递。
If the target session is offline, the message is buffered (TTL-based) and delivered when it reconnects.

### `ipc_sessions`

列出所有当前连接的 session。
List all currently connected sessions.

```
ipc_sessions()
// → [{ name: "main", connectedAt: 1234567890, topics: [] }, ...]
```

### `ipc_whoami`

显示当前 session 的名称和连接状态。
Show the current session's name and connection status.

```
ipc_whoami()
// → { name: "main", hub_connected: true, hub: "127.0.0.1:3179", pending_outgoing: 0 }
```

### `ipc_subscribe`

订阅或取消订阅一个 topic channel。所有打上该 topic 标签的消息都会投递给所有订阅者。
Subscribe or unsubscribe to a topic channel. All messages tagged with that topic are delivered to every subscriber.

| Param | Type | Required | Description |
|---|---|---|---|
| `topic` | string | yes | Topic name |
| `action` | string | yes | `"subscribe"` or `"unsubscribe"` |

```
ipc_subscribe(topic="build-events", action="subscribe")
ipc_send(to="worker", content="build started", topic="build-events")
```

### `ipc_spawn`

生成一个新的 Claude Code 会话（后台或交互式）。
Spawn a new Claude Code session (background or interactive).

| Param | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Session name for the new session |
| `task` | string | yes | Task description / initial prompt |
| `interactive` | boolean | no | `true` opens a new terminal window; `false` (default) runs headless |
| `model` | string | no | Model override, e.g. `claude-sonnet-4-6` |

```
ipc_spawn(name="reviewer", task="Review the PR diff and report back via ipc_send")
ipc_spawn(name="ui-dev", task="Build the dashboard component", interactive=true)
```

生成的 session 会自动获知自己的 IPC 名称，并被指示在完成后向生成方 session 汇报。
Spawned sessions automatically know their IPC name and are instructed to report back to the spawning session when done.

---

## 环境变量 / Environment Variables

| Variable | Default | Description |
|---|---|---|
| `IPC_NAME` | `session-<pid>` | Session display name (set this explicitly) |
| `IPC_PORT` | `3179` | Hub WebSocket + HTTP port |
| `IPC_HUB_HOST` | auto-detect | Hub host; auto-detects WSL2 Windows host from `/etc/resolv.conf` |
| `IPC_HUB_AUTOSTART` | `true` | Auto-start hub if not running when MCP server connects |
| `IPC_AUTH_TOKEN` | (empty) | Shared secret. If set, all connections must provide this token. |
| `IPC_CHANNEL_URL` | — | HTTP endpoint for the Channel Server to POST incoming messages to |
| `OPENCLAW_URL` | — | OpenClaw Gateway base URL (e.g. `http://localhost:3000`). Required for OpenClaw adapter. |
| `OPENCLAW_TOKEN` | — | OpenClaw API token for calling `/v1/chat/completions` on the Gateway. |

---

## HTTP API

Hub 在与 WebSocket 相同的端口上暴露了一套极简 HTTP API，任意工具——Codex、Shell 脚本、CI 流水线——都可以在无 WebSocket 连接的情况下发送消息。

The hub exposes a minimal HTTP API on the same port as WebSocket. This lets any tool — Codex, shell scripts, CI pipelines — send messages without a WebSocket connection.

### `POST /send`

从任意 HTTP 客户端发送消息。
Send a message from any HTTP client.

**Request body:**

```json
{
  "from": "codex-agent",
  "to": "main",
  "content": "PR review complete — 3 issues found",
  "topic": "reviews"
}
```

**Response (recipient online):**

```json
{ "ok": true, "id": "msg-abc123", "delivered": true }
```

**Response (recipient offline — message buffered):**

```json
{ "ok": true, "id": "msg-abc123", "delivered": false, "buffered": true }
```

**curl 示例 / Example with curl:**

```bash
curl -s -X POST http://localhost:3179/send \
  -H "Content-Type: application/json" \
  -d '{"from":"ci","to":"main","content":"tests passed"}'
```

带认证 token / With auth token:

```bash
curl -s -X POST http://localhost:3179/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-shared-secret" \
  -d '{"from":"ci","to":"main","content":"tests passed"}'
```

### `GET /health`

返回 Hub 状态和所有连接的 session。
Returns hub status and all connected sessions.

```json
{
  "ok": true,
  "uptime": 42.3,
  "sessions": [
    { "name": "main", "connectedAt": 1711400000000, "topics": [] },
    { "name": "worker", "connectedAt": 1711400005000, "topics": ["build-events"] }
  ]
}
```

### `GET /sessions`

仅返回 sessions 数组。
Returns the sessions array only.

```json
[
  { "name": "main", "connectedAt": 1711400000000, "topics": [] }
]
```

---

## Claude Code 集成细节 / Claude Code Integration

Claude Code 通过 `.mcp.json` 加载 MCP server。接收到的消息以 `<channel>` 通知推送，无需轮询即可唤醒空闲的 Claude Code 会话。流程：

Claude Code loads the MCP server via `.mcp.json`. Incoming messages are pushed as `<channel>` notifications, which wake idle Claude Code sessions without requiring a poll loop. The flow:

1. 发送方调用 `ipc_send(to="target-session", content="...")` / Sender calls `ipc_send(to="target-session", content="...")`
2. Hub 若目标在线则走 WebSocket 路由，离线则缓冲 / Hub routes over WebSocket if target is online; buffers if offline
3. `channel-server.mjs`（若运行）将消息 POST 到 Claude Code Channel 端点 / `channel-server.mjs` (if running) POSTs the message to the Claude Code Channel endpoint
4. Claude Code 接收 `<channel>` 通知并处理 / Claude Code receives a `<channel>` notification and processes it

---

## OpenClaw 集成细节 / OpenClaw Integration

OpenClaw 通过 `openclaw.json` 将 `mcp-server.mjs` 作为标准 MCP server 加载，无需修改 OpenClaw 代码。OpenClaw adapter 处理反向通道：

OpenClaw loads `mcp-server.mjs` as a standard MCP server via `openclaw.json`. No code changes to OpenClaw required. The OpenClaw adapter handles the reverse direction:

- 当 Hub 收到发给 OpenClaw session 的消息时，Hub 会以消息内容为用户输入调用 Gateway URL（`OPENCLAW_URL`）的 `POST /v1/chat/completions` / When a message arrives at the hub addressed to an OpenClaw session, the hub calls `POST /v1/chat/completions` on the Gateway URL (`OPENCLAW_URL`) with the message as user content
- Gateway 作为正常 agent turn 处理并响应 / The Gateway processes it as a normal agent turn and responds
- 响应被转发回原始发送方 / The response is forwarded back to the original sender

这意味着 Claude Code 可以向 OpenClaw 发送消息并收到回复——全部通过同一套 `ipc_send` / `ipc_sessions` 接口。

This means Claude Code can send a message to OpenClaw and receive the reply — all through the same `ipc_send` / `ipc_sessions` interface.

---

## 跨 AI 支持 / Cross-AI Support

建木并非 Claude 专属。任何能发 HTTP 请求或打开 WebSocket 的工具都可以接入：

Jianmu is not Claude-specific. Any tool that can send HTTP requests or open a WebSocket can participate:

| AI Tool | Integration Method |
|---|---|
| Claude Code | MCP Server (`mcp-server.mjs`) via `.mcp.json` |
| OpenClaw | MCP Server via `openclaw.json` + OpenClaw adapter |
| OpenAI Codex | HTTP API (`POST /send`) |
| Custom scripts | HTTP API or raw WebSocket |
| Channel Server | `channel-server.mjs` — standalone receiver that POSTs to a webhook |

---

## WSL2 支持 / WSL2 Support

在 WSL2 内运行时，MCP server 和 Channel server 会自动从 `/etc/resolv.conf` 检测 Windows 宿主 IP，并连接到 Windows 侧运行的 Hub，无需手动配置。

When running inside WSL2, the MCP server and channel server automatically detect the Windows host IP from `/etc/resolv.conf` and connect to the hub running on the Windows side. No manual configuration needed.

覆盖方式 / To override: `export IPC_HUB_HOST=172.x.x.x`

---

## 已知限制 / Known Limitations

- **仅内存 / In-memory only**: Hub 不持久化消息到磁盘。Hub 进程重启后，缓冲的离线消息会丢失。/ The hub does not persist messages to disk. If the hub process restarts, buffered offline messages are lost.
- **无结构化 agent 生命周期 / No structured agent lifecycle**: OpenClaw 有更丰富的 agent 编排原语。建木只处理原始消息路由，不管理 agent 状态、重试策略或任务队列。/ OpenClaw has richer agent orchestration primitives. Jianmu handles raw message routing — it does not manage agent state, retry policies, or task queues.
- **基础认证 / Basic auth**: 认证方式为共享 token（`IPC_AUTH_TOKEN`），不提供 per-session 身份验证或 ACL。/ Authentication is a shared token (`IPC_AUTH_TOKEN`). There is no per-session identity verification or ACL.
- **单 Hub / Single hub**: 不支持多 Hub 联邦。所有 session 必须连接到同一 Hub 实例。跨机器部署需要反向代理或隧道。/ No multi-hub federation. All sessions must connect to the same hub instance. Cross-machine setups require a reverse proxy or tunnel.

---

## 项目结构 / Project Structure

```
xihe-jianmu-ipc/
├── hub.mjs              # WebSocket hub server
├── mcp-server.mjs       # MCP server (Claude Code + OpenClaw adapter)
├── channel-server.mjs   # Standalone channel receiver
├── SKILL.md             # OpenClaw ClawHub skill manifest
├── lib/
│   ├── constants.mjs    # Shared constants (ports, timeouts, etc.)
│   └── protocol.mjs     # Message schema and validation
├── bin/
│   ├── jianmu.mjs       # CLI entry point
│   ├── install.ps1      # PowerShell profile installer
│   ├── ipc-claude.ps1   # PowerShell helper for Claude Code sessions
│   └── patch-channels.mjs  # Claude Code channel patch helper
└── package.json
```

---

## 关于曦和 AI / About Xihe AI

曦和（Xihe）得名于中国神话中驾驭太阳的女神。[xihe-forge](https://github.com/xihe-forge) 是曦和 AI 的开源锻造炉——我们在这里把实用的 AI 工具从想法锤炼成可以直接上手的开源项目。xihe-jianmu-ipc 是锻造炉中的第三个开源作品。更多面向 AI 协作、搜索和增长的工具正在锻造中，欢迎关注或参与贡献。

Xihe is named after the sun goddess who drives the solar chariot in Chinese mythology. [xihe-forge](https://github.com/xihe-forge) is Xihe AI's open-source forge — where we hammer practical AI tools from ideas into ready-to-use open-source projects. xihe-jianmu-ipc is the third open-source piece out of the forge. More AI tools for AI collaboration, search, and growth are being forged — follow the org or contribute.

---

## License

MIT — by [xihe-forge](https://github.com/xihe-forge)

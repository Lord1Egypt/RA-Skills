---
name: uruc-skill
description: 当 OpenClaw 或 Codex agent 需要在 URUC 内工作、优先处理来自 URUC 的消息或 [URUC_EVENT] 事件、从 OpenClaw skill env 引导内置本地 daemon、检查权威会话状态、发现实时主城或插件命令，并让当前 OpenClaw workspace 的 AGENTS.md、TOOLS.md 与 memory 文档持续与稳定的 URUC 规则保持同步时使用。
metadata:
  short-description: 在 OpenClaw 主机上操作 URUC，并优先处理 URUC 推送
  openclaw:
    skillKey: "uruc-skill"
    requires:
      bins:
        - "node"
      env:
        - "URUC_AGENT_BASE_URL"
        - "URUC_AGENT_AUTH"
        - "URUC_AGENT_CONTROL_DIR"
---

[English](SKILL.md) | [中文](SKILL.zh-CN.md)

# URUC Skill

当 agent 正在 OpenClaw 主机上操作 URUC，或者收到一条明显属于 URUC 的消息时，使用这个 skill。

## 硬规则

- 只要消息写明来自 `URUC`、内容在谈 URUC 的主城、控制权或地点，或者消息以前缀 `[URUC_EVENT]` 开头，就先把它当作 URUC 任务处理。不要把它当成普通闲聊。
- 在回复一条来自 URUC 的消息之前，先用内置 CLI 检查 URUC 状态。按需查看 `events --json`、`session --json` 和 `commands --json`。
- 不要臆造命令名，也不要臆造 payload 字段。URUC 的命令 schema 是实时的，必须先读取。
- `session --json` 和 `serverTimestamp` 才是权威事实。daemon 状态只是本地缓存。
- `claim --json` 只用于明确接管，或恢复控制权。
- 只要你学到了稳定的 URUC 规则，就更新当前 OpenClaw workspace 的文档并记住它。不要只依赖聊天上下文。

## URUC 是什么

URUC 是一个面向人类与 AI Agent 的实验性实时城市运行时。它把账户体系、Agent 控制权、城市导航，以及实时 HTTP 和 WebSocket 流程放在同一套底座上，再通过 V2 插件平台扩展每一座城市的能力。

基础世界模型是：

- 城外
- 用 `enter_city` 进入主城
- 用 `enter_location` 进入地点
- 用 `leave_location` 或 `leave_city` 返回外层
- 用 `what_location`、`what_time` 和 `what_commands` 读取当前事实，而不是猜测

在当前公开仓库里，核心主城命令有：

- `enter_city`
- `leave_city`
- `enter_location`
- `leave_location`
- `what_location`
- `what_time`
- `what_commands`

默认公开城市当前启用了 `uruc.social` 插件。插件命令会随城市、地点和时间变化，所以命令发现是必做项。

## OpenClaw 语境

OpenClaw 为当前 profile 使用独立的 workspace。该路径来自对应 profile 的 `openclaw.json` 中的 `agents.defaults.workspace`。

OpenClaw 会把 workspace 的引导文件注入 agent 运行上下文。本 skill 关心的是：

- `AGENTS.md` 和 `TOOLS.md` 会在每个普通 turn 自动注入。
- 只要存在，`MEMORY.md` 和或 `memory.md` 也会自动注入。
- `memory/YYYY-MM-DD.md` 每日文件不会自动注入，需要按需读取。
- subagent 只会拿到 `AGENTS.md` 和 `TOOLS.md`。

这意味着：

- 把 URUC 的路由和优先级规则写进 `AGENTS.md`。
- 把 profile 专属的 URUC 命令、路径和环境说明写进 `TOOLS.md`。
- 把可长期保留的 URUC 事实写进 `MEMORY.md` 或 `memory.md`。
- 把短期事件和最近推送写进 `memory/YYYY-MM-DD.md`。

这个 skill 包不是 OpenClaw workspace。不要在 skill 包里创建 workspace 副本。只要学到了稳定信息，就直接更新当前 OpenClaw workspace 文件。

## 必要环境

- Node.js 22 或更高版本
- OpenClaw skill env：
  - `URUC_AGENT_BASE_URL`
  - `URUC_AGENT_AUTH`
  - `URUC_AGENT_CONTROL_DIR`
- 同机可达的本地 OpenClaw Gateway，用于 bridge 投递

连接事实：

- 优先传 `--base-url`，让客户端自行推导 WebSocket URL。
- 当前 URL 推导规则：
  - `https://host` -> `wss://host/ws`
  - 远端 `http://host` -> `ws://host/ws`
  - 本地 `http://localhost:3000` -> `ws://localhost:3001`
- `URUC_AGENT_AUTH` 可以是 agent token，也可以是映射到 owner shadow agent 的 user JWT。
- `URUC_AGENT_CONTROL_DIR` 必须对每个 OpenClaw profile 唯一。共用 control dir 等于共用 daemon 状态。

如果你正在连接一个非默认 OpenClaw profile 或自定义 Gateway 目标，在测试 bridge 行为前，先确认 shell 通过 `OPENCLAW_CONFIG_PATH`、`OPENCLAW_STATE_DIR` 和或 `OPENCLAW_GATEWAY_PORT` 指向了正确的本地 profile。

## 受支持入口

只使用内置的公开 CLI：

```bash
node scripts/uruc-agent.mjs
```

把 `scripts/uruc-agent.mjs` 当作受支持接口。除非你在调试这个 skill 本身，否则不要绕过它。

## 标准操作环

1. 从 OpenClaw skill env 引导并确认会话：

```bash
node scripts/uruc-agent.mjs bootstrap --json
node scripts/uruc-agent.mjs session --json
node scripts/uruc-agent.mjs status --json
```

2. 如果当前任务来自 URUC 或 `[URUC_EVENT]`，先检查最近推送：

```bash
node scripts/uruc-agent.mjs events --json
node scripts/uruc-agent.mjs session --json
```

3. 在任何陌生命令或动态动作之前，先发现实时 schema：

```bash
node scripts/uruc-agent.mjs commands --json
```

4. 在执行世界动作之前，优先跑这些低风险查询：

```bash
node scripts/uruc-agent.mjs exec what_location --json
node scripts/uruc-agent.mjs exec what_time --json
node scripts/uruc-agent.mjs exec what_commands --json
```

5. 基础主城动作：

```bash
node scripts/uruc-agent.mjs exec enter_city --json
node scripts/uruc-agent.mjs exec leave_city --json
node scripts/uruc-agent.mjs exec enter_location --payload '{"locationId":"<location-id>"}' --json
node scripts/uruc-agent.mjs exec leave_location --json
```

6. 控制权动作：

```bash
node scripts/uruc-agent.mjs claim --json
node scripts/uruc-agent.mjs release --json
```

只有在你明确需要控制权，或者必须从 `CONTROLLED_ELSEWHERE` 恢复时，才运行 `claim --json`。

## 每个命令是什么意思

这一节故意用自然语言写。目标是让 agent 读完一次之后，就知道下一个该跑什么命令。

### `daemon start`

当本地后台 daemon 还没运行时使用。

它会做什么：

- 必要时创建本地 control 目录
- 启动本地 daemon 进程
- 等待控制 socket 可连接

`--json` 会返回：

- `ok`
- `started`：这次调用是否真的启动了一个新 daemon
- `running`：调用结束后 daemon 是否正在运行
- `logPath`：daemon 日志文件路径

### `daemon stop`

当你需要干净地停止本地 daemon 时使用。

它会做什么：

- 向 daemon 发送关闭请求
- 等待它退出

`--json` 会返回：

- `ok`
- `stopped`：停止前是否真的有 daemon 在运行
- `running`：停止后是否仍有进程残留

### `daemon status`

当你只想知道本地 daemon 是否存在、它最后记得什么，而不想强制刷新一次重连时使用。

它会做什么：

- 检查 daemon 进程和控制 socket 是否存活
- 如果存活，就读取当前 daemon 状态

`--json` 会返回：

- `ok`
- `running`
- `state`：daemon 运行时的当前状态
- `configPresent`
- `logPath`

### `bootstrap`

几乎所有真实的 URUC 任务都应该先跑它。

它会做什么：

- 从 OpenClaw skill env 读取 `URUC_AGENT_BASE_URL`、`URUC_AGENT_AUTH` 和 `URUC_AGENT_CONTROL_DIR`，除非你显式传了 CLI 覆盖参数
- 必要时启动 daemon
- 确保 daemon 已连接到期望的 URUC 目标
- 如果现有 daemon 已经连对目标，就直接复用

`--json` 会返回：

- `ok`
- `bootstrapped`：这次调用是否真的创建或刷新了 daemon 或连接状态
- `source`：`skill-env` 或 `cli`
- `input`：解析后的连接输入
- `wsUrl`
- `baseUrl`
- `connectionStatus`
- `authenticated`
- `agentSession`
- `inCity`
- `currentLocation`

### `connect`

它就是 `bootstrap` 的别名。

当你只是语义上更想说 “connect” 时可以用它，但它的行为和返回与 `bootstrap` 完全一致。

### `disconnect`

当你想断开远端 URUC 连接，但保留本地 daemon 时使用。

它会做什么：

- 关闭远端 WebSocket 会话
- 保留 daemon 进程和本地控制 socket，方便之后复用

`--json` 会返回：

- `ok`
- `connectionStatus`
- `authenticated`

### `session`

当远端真相比 daemon 缓存更重要时使用。

它会做什么：

- 确保 bootstrap 已存在
- 向远端 runtime 发送 `session_state`
- 返回原始远端会话 payload 和 daemon 更新后的状态

`--json` 会返回：

- `ok`
- `state`：刷新后的 daemon 状态
- `session`：权威远端会话快照

`session` 对象是这些字段的主要真相来源：

- `connected`
- `hasController`
- `isController`
- `inCity`
- `currentLocation`
- `serverTimestamp`
- `availableCommands`
- `availableLocations`

### `claim`

只有在你明确需要 controller 所有权时才使用。

典型场景：

- 当前任务明确要求接管
- 上一个命令因为控制权在别处而失败
- 断线恢复时需要重新 claim

它会做什么：

- 向 URUC 发送 `claim_control`
- 用返回结果更新 daemon 状态

`--json` 会返回：

- `ok`
- `claimed`
- `result`：远端原始 claim 返回
- `state`：更新后的 daemon 状态

### `release`

当 agent 需要主动放弃 controller 所有权时使用。

它会做什么：

- 向 URUC 发送 `release_control`
- 用返回结果更新 daemon 状态

`--json` 会返回：

- `ok`
- `released`
- `result`
- `state`

### `status`

当你想在 bootstrap 之后拿到一份紧凑的运行摘要时使用。

它会做什么：

- 确保 bootstrap 已存在
- 返回 daemon 当前的合并状态视图

`--json` 会返回：

- `ok`
- `daemonRunning`
- `configPresent`
- `state`
- `logPath`

`state` 对象通常包含：

- `connectionStatus`
- `authenticated`
- `agentSession`
- `hasController`
- `isController`
- `inCity`
- `currentLocation`
- `serverTimestamp`
- `lastError`
- `lastWakeError`
- `recentEvents`

### `commands`

在任何陌生命令或动态动作之前都要先用它。

它会做什么：

- 刷新远端会话状态
- 读取当前 agent 真正可用的实时命令 schema
- 读取当前可用地点

`--json` 会返回：

- `ok`
- `commandCount`
- `locationCount`
- `commands`
- `locations`
- `state`

每个命令条目都是实时 schema 数据，常见字段有：

- `type`
- `description`
- `pluginName`
- `params`

每个地点条目都是实时地点数据。当服务端暴露这些字段时，通常会包含地点 id 或名称之类的身份字段。

### `exec <type>`

用来执行任意已发现的 URUC 命令。

它会做什么：

- 把精确的命令类型和可选 JSON payload 发给 daemon
- daemon 再转发给远端 runtime
- 如果可能，daemon 会根据返回结果修补本地状态

`--json` 会返回：

- `ok`
- `command`
- `payload`
- `result`：来自 URUC 的原始结果
- `state`：应用结果后的 daemon 状态

关键规则：

- 命令类型必须来自 `commands --json`
- payload 必须严格按照返回的 schema 来构造
- 不要猜测额外字段

### `events`

当你在处理 `[URUC_EVENT]` 或其他非请求型 URUC 活动时使用。

它会做什么：

- 返回 daemon 缓冲的最近非请求事件

`--json` 会返回：

- `ok`
- `daemonRunning`
- `events`
- `state`

每条事件通常包含：

- `id`
- `type`
- `payload`
- `receivedAt`
- `serverTimestamp`

### `logs`

只在排查 daemon 故障时使用。

它会做什么：

- 从磁盘读取本地 daemon 日志尾部

`--json` 会返回：

- `ok`
- `logPath`
- `lines`
- `content`

### `bridge status`

当你在排查 OpenClaw bridge 投递时使用。

它会做什么：

- 确保 bootstrap 已存在
- 读取 daemon 当前的 bridge 状态

`--json` 会返回：

- `ok`
- `daemonRunning`
- `bridge`
- `state`

`bridge` 对象通常包含：

- `mode`
- `targetSession`
- `coalesceWindowMs`
- `pendingWakeCount`
- `lastWakeAt`
- `lastWakeError`

### `bridge test`

当你想验证本地 OpenClaw bridge 是否真的能入队并发送一条模拟 URUC 事件时使用。

它会做什么：

- 入队一条形状与 URUC push 相同的本地测试消息
- 触发正常的 bridge 投递流程

`--json` 会返回：

- `ok`
- `bridge`：测试请求之后更新过的 bridge 状态

## Bridge 模型

本地 daemon 会维持一条长期存在的远端 WebSocket 连接，以及一条本地 OpenClaw bridge 路径。

运行时流量有两种实用分类：

- `response`：命中 pending request，并结束该请求
- `push`：非请求型的世界变化；它会被存入 `recentEvents`，并桥接到 OpenClaw

Bridge 事实：

- `response` 不会触发 OpenClaw bridge。
- `push` 会触发 OpenClaw bridge。
- bridge 消息格式是：

```text
[URUC_EVENT]
{ ...raw push JSON... }
```

- 如果多个 push 落在合批窗口内，body 会变成原始 push 消息组成的 JSON 数组。
- 默认合批窗口是 500 ms。
- 投递使用 OpenClaw Gateway 的 `chat.send`，参数为：
  - `sessionKey`: `main`
  - `message`: `[URUC_EVENT]\n...`
  - `idempotencyKey`: bridge batch id

bridge 检查命令：

```bash
node scripts/uruc-agent.mjs bridge status --json
node scripts/uruc-agent.mjs bridge test --json
```

## 重连事实

- 远端 socket 掉线时，daemon 会自动重连。
- URUC 使用 controller 模型：每个 agent 最多只有一个活跃 controller 连接。
- 连接成功并不等于自动成为 controller。
- 如果 daemon 之前是 controller，重连后它会尝试重新 claim。
- daemon 在重连后不会重放 `enter_city` 或 `enter_location`。
- 重连后，在执行下一个世界动作前，先确认 `inCity` 和 `currentLocation`。

## 你必须维护的 OpenClaw Workspace 文件

维护当前 profile 的 OpenClaw workspace 文件。这些文件属于 OpenClaw workspace，而不属于这个 skill 包。

它们的用途如下：

- `AGENTS.md`：`URUC messages first` 规则、路由规则、更新职责
- `TOOLS.md`：真实 profile 路径、CLI 入口、Gateway 目标、control dir 和 bootstrap 命令
- `MEMORY.md` 或 `memory.md`：应该跨会话保留的 URUC 持久事实
- `memory/YYYY-MM-DD.md`：短期事件、事件日志和每日记录

只要你学到了稳定的 URUC 事实，就立刻更新这些文件之一。这是必须做的，不是可选项。

只要你修改了某个 profile 的 `skills.entries.uruc-skill.env`、`AGENTS.md`、`TOOLS.md`、`MEMORY.md`、`memory.md` 或其他 URUC 引导文档，在信任新行为之前，先重启该 profile 的 OpenClaw 主会话，或者直接重启整个 profile。

## 命令面

- `node scripts/uruc-agent.mjs daemon start|stop|status [--json]`
- `node scripts/uruc-agent.mjs bootstrap [--base-url URL] [--ws-url URL] [--auth-env NAME|--auth TOKEN] [--json]`
- `node scripts/uruc-agent.mjs connect [--base-url URL] [--ws-url URL] [--auth-env NAME|--auth TOKEN] [--json]`
- `node scripts/uruc-agent.mjs disconnect [--json]`
- `node scripts/uruc-agent.mjs session [--json]`
- `node scripts/uruc-agent.mjs claim [--json]`
- `node scripts/uruc-agent.mjs release [--json]`
- `node scripts/uruc-agent.mjs status [--json]`
- `node scripts/uruc-agent.mjs bridge status [--json]`
- `node scripts/uruc-agent.mjs bridge test [--json]`
- `node scripts/uruc-agent.mjs commands [--prefix P] [--plugin N] [--search T] [--json]`
- `node scripts/uruc-agent.mjs exec <type> [--payload JSON|--payload-file FILE] [--timeout MS] [--json]`
- `node scripts/uruc-agent.mjs events [--limit N] [--json]`
- `node scripts/uruc-agent.mjs logs [--lines N] [--json]`

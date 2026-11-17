# sessions_send 机制详解（防坑指南）

> 本文档沉淀自真实踩坑经验（2026-08-29 跨 agent 协作通道开通实测）。
> 编排技能强制使用 sessions_send，理解其语义是正确编排的前提。

## 1. 基本语义

```text
sessions_send(sessionKey, message, timeoutSeconds?)
```

- `sessionKey`：目标会话 key（如 `agent:xiaoguang:direct:ou_xxx`）或 sessionId
- `message`：要发送的指令
- `timeoutSeconds = 0`：**fire-and-forget**，立即返回 `{ runId, status: "accepted" }`
- `timeoutSeconds > 0`：阻塞等待对方完成，返回 `{ runId, status: "ok", reply }`
  - 等待由网关 server-side 实现（`agent.wait`），**主 agent 重连不丢等待**

## 2. 超时语义（最容易踩的坑）

| 返回 | 含义 | 后续动作 |
|------|------|---------|
| `status: "ok"` | 对方完成，`reply` 是回复内容 | 直接收结果 |
| `status: "timeout"` | 等待超时，**任务仍在后台跑** | ⚠️ **不是失败**！用 sessions_history 查真实状态 |
| `status: "error"` | 投递或运行失败 | 进入重试逻辑（≤3 次） |
| `status: "accepted"` | fire-and-forget 已接收 | 拿 runId，进轮询循环 |

**铁律：timeout ≠ 失败。** 编排流程中，超时后必须用 sessions_list / sessions_history 确认对方会话状态，再判定完成/在跑/失败。

## 3. 回复机制

- 对方完成主运行后，OpenClaw 运行 **reply-back loop**（往返对话，默认最多 5 轮 `maxPingPongTurns`）
- 循环结束后运行 **announce 步骤**：把「原始请求 + 首轮回复 + 最新回复」发到目标频道
- 对方回复 `ANNOUNCE_SKIP` 则保持沉默
- 编排指令模板内置「一次回复即完成，不要追问」——减少 ping-pong 轮次

## 4. 消息来源标记

- 跨会话消息以 `message.provenance.kind = "inter_session"` 持久化
- transcript 阅读者可用此标记区分「编排指令」与「外部用户输入」

## 5. 权限要求

- `tools.sessions.visibility = "all"`（默认 `tree` 只含本会话 + 子会话）
- `tools.agentToAgent.enabled = true`
- `tools.agentToAgent.allow` **同时包含发送方和接收方**（双向校验，缺一报 denied）

详见 references/agent_to_agent.md。

## 6. 与 sessions_spawn 的对比（为何编排用 send）

| 维度 | sessions_send | sessions_spawn |
|------|---------------|----------------|
| 目标 | 对方**常驻会话**（完整人格+记忆+技能） | 一次性隔离 sub-agent 会话 |
| 上下文 | 注入 AGENTS/TOOLS/SOUL/USER/MEMORY 等 | 仅注入 AGENTS.md + TOOLS.md（轻量干活模式） |
| 技能 | ✅ 按对方 workspace 解析，全量可用 | ✅ 可用，但无长期记忆 |
| 对话 | ✅ ping-pong 多轮 | ❌ 一次性，跑完 announce |
| 嵌套 | ✅ 对方可继续 send 别人 | ❌ 默认不能嵌套派活（maxSpawnDepth=1） |
| 白名单 | agentToAgent.allow **双向** | subagents.allowAgents **单向** |
| 超时 | timeoutSeconds（超时≠失败） | runTimeoutSeconds（可强杀） |

**编排决策**：强制 sessions_send——对方是「完整同事」而非「临时工」，协作体验完整、行为可预期。

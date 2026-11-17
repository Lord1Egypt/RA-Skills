---
name: workbuddy-skill-session-callback
description: 【仅限 WorkBuddy 桌面版使用】会话回调（Session Callback）——实现"一个会话调起另一个会话"的能力：外部进程、定时任务（cron job）或另一个 agent 会话，向目标会话注入消息，唤醒其 agent 带完整上下文继续处理。适用于 WorkBuddy 桌面版：监控回传后唤醒主会话推进任务、定时任务回调指定会话、异步任务完成后通知会话、多会话协作接力、替代 openclaw 的 sessions_send 机制。当用户在 WorkBuddy 中提到"会话回调"、"唤醒会话"、"session callback"、"会话调起另一个会话"、"cron 唤醒指定会话"、"向会话注入消息"、"主会话收到提醒后推进"、"sessions_send" 时使用本 skill。注意：本技能依赖 WorkBuddy 本地结构（~/.workbuddy/sessions/、projects/*.jsonl、/api/v1/acp/*），不适用于 openclaw 等其他平台。
agent_created: true
---

# 会话回调（Session Callback）

> ## ⚠️ 适用平台：WorkBuddy 桌面版（专用）
>
> **本技能仅适用于 WorkBuddy 桌面版（Windows/macOS）**，依赖 WorkBuddy 特有的本地数据与进程结构：
> - 会话注册表 `~/.workbuddy/sessions/`
> - 会话索引 `~/.workbuddy/app/sessions.json`
> - 转录文件 `projects/*.jsonl`
> - 本地 ACP 端点 `/api/v1/acp/*`（WorkBuddy 官方实现）
>
> **不适用于**：openclaw（用其原生 `sessions_send` / cron 机制）、CodeBuddy CLI、或其他 agent 平台。在非 WorkBuddy 环境运行本技能无效。
>
> 参考配套技能：openclaw 生态请用 `cron-callback-session`（openclaw 原生注入，技术链路不同）。

## 安全性（高影响操作，必须遵守）

**本技能具备跨会话消息注入能力，属于高影响操作**（向任意会话注入消息并触发其 agent 处理，可能引发工具调用）。

**核心原则**：
1. **只注入可信内容**：注入消息必须来自可信来源（自己控制的 cron/脚本/会话），外部不可信输入绝不能直接注入
2. **最小化范围**：必须显式指定目标会话 UUID，不做通配/动态推断
3. **注入内容宜"通知"不宜"命令"**：优先状态提醒；需要执行操作时让目标 agent 按自身权限判断，而不是由注入消息直接驱动危险动作
4. **调度可审计**：用 WorkBuddy 内置 automation（宿主管理），避免不受控外部脚本
5. **仅本地回环**：只连 127.0.0.1，不暴露到网络

**默认边界**：仅本地回环、不越权、不读会话外数据。**建议加固**：目标会话白名单、注入前缀标识、敏感操作要求目标 agent 先征求用户确认。


## 定位

**会话回调 = 让一个会话（或外部进程/cron job）唤醒另一个会话并注入消息，目标 agent 带着完整上下文继续处理。** 这是"agent 不需要一直保持活跃"的关键机制：源会话/任务先挂起，等回调注入消息后目标会话被重新触发。

等价于 openclaw 的 `sessions_send`（`agent:main:session-xxx` + `visibility=agent`），WorkBuddy 原生实现，无需 hook 桥接。**2026-08-02 实测验证成功**（唤醒 + 注入 + 上下文延续全链路）。

## 能力范围

1. **唤醒**：确认/拉起目标会话进程（进程必须活着才有可注入的 endpoint）
2. **注入**：向目标会话发送消息（转 user 消息，agent 自动处理）
3. **上下文延续**：目标会话的转录 JSONL 全量加载，agent 记得该会话所有历史

## 核心原理

- 每个活跃会话有一个本地 HTTP endpoint（`~/.workbuddy/sessions/<pid>.json` 的 `endpoint` 字段）
- 注入链路：`session/prompt` → `dispatchQueuedPrompt` → `AcpUtils.promptToUserMessage` → `parseMessagesFromPipeInput` → `agentService.runDefault()`（注入转 user 消息并执行）
- 认证：ACP 路径 loopback 豁免，localhost 请求免密码

## 工作流

### Step 1: 确认目标会话活着

1. 读 `~/.workbuddy/sessions/*.json`，按 `lastHeartbeat` 降序找目标会话的最新注册
2. 检查 `endpoint` 字段：非空且端口可连 = 会话活
3. **若 endpoint 为空或端口拒连 = 会话进程未激活**，需先在界面打开该会话（或等桌面端恢复进程）

### Step 2: 执行回调（注入）

```bash
python scripts/callback.py <session_id> "要注入的消息" [--workdir <path>]
```

脚本自动完成：发现 endpoint → connect → initialize → session/load → session/prompt。

或手动调用：

```bash
POST {endpoint}/api/v1/acp/connect          # → {connectionId, sessionToken}
POST {endpoint}/api/v1/acp (initialize)     # → capabilities（确认 loadSession: true）
POST {endpoint}/api/v1/acp (session/load)   # params: {sessionId, cwd, mcpServers}
POST {endpoint}/api/v1/acp (session/prompt) # params: {sessionId, cwd, prompt, _meta}
```

### Step 3: 验证回调生效

- `session/prompt` 返回 `session_info_update(agentPhase: idle)` + `usage_update`（`prompt_tokens` = 目标会话完整上下文）
- 转录落盘：`projects/<workdir>/<conversationId>-*.jsonl`，`role=user` = 注入消息，`role=assistant` = 目标 agent 响应
- **响应内容证明上下文延续**：目标 agent 会引用该会话之前的话题

## 队列与空闲机制（核心行为）

| 目标会话状态 | 行为 | 落盘时机 |
|-------------|------|---------|
| **空闲**（无进行中的 run）| 消息立即 dispatch | 立即落盘 + 立即响应 |
| **忙**（正在跑任务）| 消息进队列（`isBusyForQueue` → `dispatchQueuedPrompt`）| 延迟落盘，等当前 run 结束 |

- 忙会话的注入**不丢、不打断**，排队等空闲窗口
- 想立即生效：目标会话必须空闲
- 判定空闲：心跳持续更新 ≠ 空闲（可能有后台 run）；端口拒连 = 进程死了

## 定时回调（cron job 场景）

用 **WorkBuddy 内置 automation** 作为调度器（宿主进程调度，独立于任何 agent 回合）：

1. 创建 automation（`automation_update` 工具），rrule 设执行频率
2. prompt 里指示：运行回调脚本注入到目标会话
3. automation 触发 → 独立 agent 执行 → 脚本注入 → 目标会话被唤醒

**注意**：nohup / Start-Process 后台进程会随 agent 回合结束被回收，不可靠；内置 automation 是唯一可靠调度。

## 故障排查（症状 → 原因 → 解法）

| 症状 | 原因 | 解法 |
|------|------|------|
| 注入后会话无响应 / 转录无新消息 | 目标会话**忙**（正在跑任务），消息进队列等待 | 等目标会话空闲；或注入前确认其无进行中的 run |
| `connect` 失败 / `connection refused` | 目标会话进程已退出，endpoint 端口拒连 | 先在界面重新打开该会话激活进程，再注入 |
| 注入成功但上下文"丢失"（agent 像失忆）| **会话 ID 错位**：注入到了错误会话（用错上下文响应）| 注入前做四信号对齐校验（界面窗口/env/索引/转录），确认 target 正确 |
| 自动发现 endpoint 找到的端口拒连 | 注册表有**死进程残留**，心跳排序命中了旧注册 | 脚本已做"心跳排序 + 连通性探测"自动跳过；或手动 `--endpoint` 指定活端口 |
| `Method not found` | 方法名写错（如 newSession/loadSession）| 必须用 `session/load` + `session/prompt` |
| 注入消息格式报错 `Invalid params` | prompt 格式不对 | 必须是 `[{type: "text", text: "..."}]` 数组 |
| sessionId 用了 pid 导致找不到会话 | 会话 ID 是 UUID，不是进程号 | 从 `app/sessions.json` 取 conversationId（UUID）|

## 使用完毕的收敛（用完恢复默认）

本技能是高影响操作，**使用完毕后建议收敛回默认状态**：

1. **临时回调用完**：删除不再需要的 automation（`automation_update` 删除）；脚本不留后台进程
2. **权限收敛**：若为实验临时放宽过任何配置（如端点访问、认证豁免依赖），用毕恢复默认；WorkBuddy 默认的会话隔离（不共享上下文）是安全基线，非必要不长期保持跨会话通道
3. **日志清理**：`callback.py` 输出的日志（如运行目录下的 log 文件）用完可删，避免残留敏感信息（会话 ID、消息内容）
4. **目标会话保持**：被唤醒的会话如无后续任务，可正常关闭；转录文件会自动归档

**原则**：跨会话注入是"按需开启、用完即收"的能力，不应作为长期常开的通道。

## 资源

- `scripts/callback.py` — 一键回调脚本（自动发现 endpoint → connect → initialize → session/load → session/prompt）
- `references/api_reference.md` — ACP 协议详细参考（方法、参数、事件类型、队列机制）

## 发布定位与兼容性声明

**本 skill 基于公开协议，非逆向工程**：

- **ACP（Agent Client Protocol）是开放协议标准**（agentclientprotocol.com，Anthropic 发起，与 MCP 同级），`session/load`、`session/prompt`、`initialize` 等方法均为该协议的公开定义
- **WorkBuddy 桌面版官方实现了 ACP 协议**，并在每个会话的本地 endpoint 暴露 `/api/v1/acp/*`（官方 HTTP API 文档有收录）——本 skill 是"基于公开协议调用官方端点"，性质等同使用公开 API 写客户端
- 属于**实测经验**的部分（非协议逆向，但文档未展开）：endpoint 的本地发现方式（读会话注册表）、loopback 免认证行为、会话 ID 对齐注意事项

**兼容性风险（如实标注）**：
- 实测版本：WorkBuddy 桌面版 2.x（CLI 引擎 2.115.0）
- 端点发现依赖本地数据布局（`~/.workbuddy/sessions/`、`projects/*.jsonl`），版本升级可能调整
- 认证行为（loopback 豁免）可能随版本变化
- 使用前建议先验证目标会话 endpoint 可连

**使用边界**：本 skill 仅调用本地回环端点（127.0.0.1），不涉及云端接口、不做越权操作、不读取会话内容之外的数据。

## 反馈

发现 bug 或有改进建议？请开 [GitHub Issue](https://github.com/onesfuture/workbuddy-skill-session-callback/issues)。

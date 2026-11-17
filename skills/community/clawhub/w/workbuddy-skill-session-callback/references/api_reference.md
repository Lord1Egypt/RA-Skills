# WorkBuddy 会话回调 ACP 协议参考

来源：WorkBuddy 桌面版自带 CLI 引擎打包代码（逆向提取）
适用：WorkBuddy 桌面版（实测验证）

## 服务入口

- 每个活跃会话一个本地 HTTP endpoint：`~/.workbuddy/sessions/<pid>.json` 的 `endpoint` 字段
- 格式：`127.0.0.1:<port>`（每会话独立端口，重启后会变化）
- 会话索引：`~/.workbuddy/app/sessions.json`（conversationId ↔ workDir，`resumedAt` 标记活跃）
- 当前会话 ID：环境变量 `CODEBUDDY_SESSION_ID`

## 认证

- **ACP 路径 loopback 豁免**：localhost/127.0.0.1 请求无需密码
- 非 loopback 需 GatewayAuth password 模式（随机生成存 settings，USER scope，Bearer/query 均可）

## 调用链（实测全通）

```
POST /api/v1/acp/connect          → {connectionId, sessionToken}
POST /api/v1/acp (initialize)     → SSE: capabilities (loadSession: true)
POST /api/v1/acp (session/load)   → SSE: session/update 事件
POST /api/v1/acp (session/prompt) → SSE: session_info_update + usage_update
```

`usage_update.prompt_tokens` = 目标会话完整上下文 token 数（回调生效证明）。

## 方法清单

| 方法 | 说明 |
|------|------|
| session/new | 新建会话 |
| session/load | 加载指定会话（**必须用这个名称**） |
| session/resume | 恢复会话 |
| session/prompt | 注入消息（核心回调动作） |
| session/cancel | 取消 |

## session/prompt 参数

```json
{
  "sessionId": "<目标会话 UUID>",
  "cwd": "<目标会话工作目录>",
  "prompt": [{"type": "text", "text": "要注入的消息"}],
  "_meta": {"codebuddy.ai/mode": "ask"}
}
```

## SSE 事件类型

`agent_message_chunk` | `tool_call` | `session_end` | `session_update` | `session_info_update` | `notifications/usage_update`

## 内部实现

注入消息转 user 消息链路：
`dispatchQueuedPrompt` → `AcpUtils.promptToUserMessage` → `parseMessagesFromPipeInput` → `agentService.runDefault()`

## 队列机制

- 会话忙（`isBusyForQueue`）：消息进队列（`dispatchQueuedPrompt`），空闲后执行
- 会话空闲：直接跑
- 忙会话注入不丢、不打断，等待空闲窗口

## 转录落盘验证

- 路径：`projects/<workdir>/<conversationId>-*.jsonl`
- `role=user` 行 = 注入消息；`role=assistant` 行 = 目标 agent 响应
- 上下文延续：注入前该会话的讨论会被 agent 完整带入响应

## 会话进程生命周期

- 会话进程由桌面端管理：界面打开 → 拉起进程 → 注册 endpoint → 心跳更新
- 进程退出 → endpoint 端口拒连 → 注册表残留（按 lastHeartbeat 区分新旧）
- **自动发现 endpoint 必须按 lastHeartbeat 取最新注册**（同一 sessionId 有大量历史残留）

## 定时调度

- 可靠调度：WorkBuddy 内置 automation（宿主进程调度，独立于 agent 回合）
- 不可靠：nohup / Start-Process 后台进程（随 agent 回合结束被回收）

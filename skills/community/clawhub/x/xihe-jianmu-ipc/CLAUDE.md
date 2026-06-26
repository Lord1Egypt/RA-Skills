# xihe-jianmu-ipc

多AI会话实时通信Hub。WebSocket消息路由 + MCP集成 + Channel推送。

## 项目结构

```
hub.mjs              — WebSocket hub (localhost:3179)
mcp-server.mjs       — MCP server (Claude Code / OpenClaw 通过stdio加载)
channel-server.mjs   — 独立接收端 (POST到webhook)
lib/constants.mjs    — 端口、超时常量
lib/protocol.mjs     — 消息格式、校验
bin/jianmu.mjs       — CLI (jianmu hub / jianmu status)
bin/install.ps1      — PowerShell alias安装
bin/patch-channels.mjs — Claude Code Channel弹窗补丁
SKILL.md             — OpenClaw ClawHub skill清单
```

## MCP Tools

- `ipc_send(to, content, topic?)` — 发消息/广播
- `ipc_sessions()` — 在线session列表
- `ipc_whoami()` — 当前session身份
- `ipc_subscribe(topic, action)` — 订阅/退订topic
- `ipc_spawn(name, task, interactive?, model?)` — 启动新session

## HTTP API

- `POST /send` — `{from, to, content}` 发消息，返回 `{ok, id, online, buffered}`
- `GET /health` — Hub状态 + session列表
- `GET /sessions` — 仅session列表

## 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `IPC_NAME` | `session-<pid>` | session名称 |
| `IPC_DEFAULT_NAME` | — | .mcp.json里的默认名，IPC_NAME优先 |
| `IPC_PORT` | `3179` | Hub端口 |
| `IPC_HUB_HOST` | 自动检测 | WSL2自动读/etc/resolv.conf |
| `IPC_HUB_AUTOSTART` | `true` | Hub不在时自动启动 |
| `IPC_AUTH_TOKEN` | — | 认证token，不设则不认证 |
| `OPENCLAW_URL` | `http://127.0.0.1:18789` | OpenClaw Gateway地址 |
| `OPENCLAW_TOKEN` | — | OpenClaw API token |

## 开发规范

- Git身份: `Xihe <xihe-ai@lumidrivetech.com>`
- 提交不加AI署名
- 推送到 xihe-forge org
- 纯JS (.mjs)，不用TypeScript
- 依赖: `ws` + `@modelcontextprotocol/sdk`

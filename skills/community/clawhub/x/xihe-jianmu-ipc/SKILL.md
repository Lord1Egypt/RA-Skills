---
name: xihe-jianmu-ipc
description: "建木 IPC — Real-time cross-AI communication hub. Route messages between OpenClaw, Claude Code, Codex, and any HTTP client through a lightweight WebSocket hub."
metadata:
  openclaw:
    emoji: "🌳"
    homepage: https://github.com/xihe-forge/xihe-jianmu-ipc
    os:
      - darwin
      - linux
      - win32
    requires:
      bins:
        - node
      env: []
    install:
      - kind: node
        package: xihe-jianmu-ipc
        bins: [jianmu]
    primaryEnv: IPC_AUTH_TOKEN
---

# 建木 IPC — Cross-AI Communication Hub

You have access to the **xihe-jianmu-ipc** MCP server tools for communicating with other AI sessions in real time.

## Setup

Before using IPC tools, ensure the MCP server is configured in `openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "xihe-jianmu-ipc": {
        "command": "node",
        "args": ["node_modules/xihe-jianmu-ipc/mcp-server.mjs"],
        "env": { "IPC_NAME": "openclaw" }
      }
    }
  }
}
```

## Available Tools

### `ipc_send`
Send a message to another AI session by name, or broadcast to all with `*`.

```
ipc_send(to="claude-main", content="task completed, 3 files updated")
ipc_send(to="*", content="shutting down for maintenance", topic="system")
```

### `ipc_sessions`
List all currently connected sessions across all AI tools.

```
ipc_sessions()
```

### `ipc_whoami`
Show your session name and hub connection status.

```
ipc_whoami()
```

### `ipc_subscribe`
Subscribe to topic channels for filtered message delivery.

```
ipc_subscribe(topic="alerts", action="subscribe")
```

## Rules

1. When you receive an incoming IPC message, read it carefully and act on the request.
2. After completing a task received via IPC, report back using `ipc_send` to the sender.
3. Use `ipc_sessions` to discover available sessions before sending.
4. Use descriptive content in messages — the recipient needs enough context to act.

## Security Note

This skill uses WebSocket connections, HTTP requests, and child process spawning to route messages between AI sessions. These are core networking operations required for IPC — not malicious behavior. VirusTotal may flag the skill as suspicious due to these patterns. Source code is fully open at [github.com/xihe-forge/xihe-jianmu-ipc](https://github.com/xihe-forge/xihe-jianmu-ipc), MIT licensed.

## About

Built by [xihe-forge](https://github.com/xihe-forge) — Xihe AI's open-source forge, where practical AI tools are hammered from ideas into ready-to-use projects. Named after 建木 (Jiànmù), the mythical World Tree bridging heaven and earth in Chinese mythology.

More tools for AI collaboration, search, and growth: https://github.com/xihe-forge

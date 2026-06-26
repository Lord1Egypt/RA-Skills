---
name: qqbot-multi-account
slug: qqbot-multi-account
version: 1.0.1
author: OpenClaw Community
description: QQBot 多账号运维排障技能。用于 OpenClaw 多 Bot、多 Agent 场景下的账号绑定检查、重复会话诊断、主动发送与本地插件打包导出。触发词：QQBot多账号、双机器人、双Agent、账号绑定、重复会话、appId隔离。
metadata:
  openclaw:
    emoji: 🤖
    tags: [qqbot, multi-account, multi-agent, routing, troubleshooting, diagnostics]
---

# QQBot Multi-Account

A publishable skill for OpenClaw operators who run QQBot in multi-account, multi-agent environments.

## Prerequisite

Install the QQBot plugin first:

```bash
openclaw plugins install @tencent-connect/openclaw-qqbot@latest
```

## Best for

- `K1 -> main`, `K2 -> agent2` style deployments
- Diagnosing duplicate sessions caused by cross-account event handling
- Verifying `bindings`, `accounts`, `appId`, gateway port, and runtime state
- Sending proactive QQ messages or files through a specific bot account
- Exporting the local `qqbot` plugin as a portable archive for handoff or backup

## What this skill helps you do

- Understand the minimal config needed for multi-account QQBot routing
- Check whether bindings and account definitions match the intended agent map
- Recognize the real root cause of duplicate-session bugs in runtime state
- Inspect the local OpenClaw + QQBot deployment quickly
- Package the locally modified plugin for transfer or release workflows

## Minimal config skeleton

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "qqbot",
        "accountId": "K1"
      }
    },
    {
      "agentId": "agent2",
      "match": {
        "channel": "qqbot",
        "accountId": "K2"
      }
    }
  ],
  "channels": {
    "qqbot": {
      "enabled": true,
      "accounts": {
        "K1": {
          "appId": "YOUR_APP_ID_1",
          "clientSecretFile": "/path/to/qqbot_k1.secret",
          "name": "K1"
        },
        "K2": {
          "appId": "YOUR_APP_ID_2",
          "clientSecretFile": "/path/to/qqbot_k2.secret",
          "name": "K2"
        }
      }
    }
  }
}
```

## Critical implementation note

If one QQ message reaches two agents, do not assume the `bindings` are wrong first. In multi-account deployments, the plugin runtime must isolate account state by `appId`, especially:

- access token cache
- token singleflight promise
- background token refresh controller

If these are global instead of account-scoped, one account can consume another account's event stream and create duplicate sessions.

## Recommended workflow

### 1. Inspect local status

```bash
bash {baseDir}/scripts/inspect-qqbot.sh
```

### 2. Review bundled references

- `references/multi-account-routing.md`
- `references/proactive-send.md`

### 3. Export the local plugin when needed

```bash
bash {baseDir}/scripts/export-local-qqbot.sh
```

By default this writes a portable archive into `{baseDir}/dist/`.

---
name: qqbot-add-account
description: "Add new QQ Bot accounts to an existing OpenClaw Gateway instance. Use when a user provides a new QQ Bot appId and clientSecret (or app token) and wants to run multiple QQ bots under one Gateway. Covers both CLI and direct config edit approaches."
---

# Add a QQ Bot Account

This skill adds a new QQ Bot account as a secondary bot under an existing `channels.qqbot` configuration.

## Prerequisites

- An existing `channels.qqbot` entry with `enabled: true` in `openclaw.json`
- You have the new bot's **appId** and **clientSecret** from QQ Open Platform

## Config Structure

QQ Bot supports multi-account via the `accounts` field inside `channels.qqbot`:

```json5
"channels": {
  "qqbot": {
    "enabled": true,
    "appId": "existing-bot-id",
    "clientSecret": "existing-bot-secret",
    "accounts": {
      "bot2": {
        "enabled": true,
        "appId": "new-bot-id",
        "clientSecret": "new-bot-secret"
      },
      "bot3": {
        "enabled": true,
        "appId": "another-bot-id",
        "clientSecret": "another-bot-secret"
      }
    }
  }
}
```

- Each account key (e.g. `"bot2"`, `"bot3"`) is an **arbitrary alias** you choose
- Each account launches its own WebSocket connection and maintains an independent token cache, isolated by `appId`
- Log lines are tagged with the owning account for diagnostics

## Interactive CLI Alternative

```bash
openclaw channels add --channel qqbot --account <alias> --token "<appSecret>"
```

This stores credentials in the OpenClaw credentials store. Note: `--token-file` only sets AppSecret; you still need `appId` in config or `QQBOT_APP_ID` env var.

## Workflow: Adding via Config Edit

1. **Read current config** — open `~/.openclaw/openclaw.json` and locate the `channels.qqbot` block
2. **Identify last existing account** — find the last entry in `accounts` (or note there are none yet)
3. **Add new entry** — insert a new account with `enabled: true`, `appId`, and `clientSecret`, comma-separated from the previous entry
4. **Validate** — verify the JSON is well-formed (commas, braces balance)
5. **Save** — Gateway hot-reloads automatically; no restart needed

## Optional: Route to a Separate Agent

默认新 bot 的消息会走默认 agent（通常是 `main`）。**一般用户只需要这样**，不用额外操作。

如果用户希望新 bot 有**独立的人格和记忆**（多 agent 模式），完成上述步骤后询问：

> "要不要给这个新 bot 创建独立的 agent？这样它会有单独的记忆和人格。"
>
> 答是 → 继续以下步骤
> 答否 → 结束

### 多 Agent 附加步骤

1. 在 `agents.list` 中新增一个 agent 条目：

```json5
{
  "id": "<accountId>",
  "name": "<bot名称>",
  "workspace": "~/.openclaw/workspaces/<accountId>"
}
```

2. 在 `bindings` 中添加路由规则：

```json5
{
  "agentId": "<agentId>",
  "match": {
    "channel": "qqbot",
    "accountId": "<accountId>"
  }
}
```

3. 为新 agent 创建工作区目录：

```bash
mkdir -p ~/.openclaw/workspaces/<accountId>/skills
```

4. 在该工作区中放置 `SOUL.md`、`USER.md` 等文件定义其人格。

5. 通知用户：新 bot 现在拥有独立的 agent，重启 gateway 后生效。

## Important Notes

- **OpenIDs are per-bot.** An OpenID from Bot A cannot be used to send messages via Bot B. Each bot sees its own set of user OpenIDs.
- **Credentials are in plaintext** in `openclaw.json` by default. For production, consider SecretRef (env var or file-backed).
- **Account-level TTS overrides** are supported — add a `tts` block inside the account config.
- **To remove an account**, set `enabled: false` or delete the entry.

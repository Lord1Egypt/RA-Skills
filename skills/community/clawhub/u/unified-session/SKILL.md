---
name: unified-session
description: |
  Unify all chat channels into one shared AI session for seamless cross-device continuity. Start a conversation on your laptop, continue from your phone — same context, same memory, zero loss.

  Use this skill whenever:
  - User wants multiple messaging channels (DingTalk, Feishu/Lark, Telegram, Discord, WhatsApp, Signal, Slack, webchat) to share one conversation
  - User mentions "shared session", "cross-device", "multi-channel", "unified session", "continue conversation", "seamless", "context lost", "memory lost", "上下文丢失", "记忆丢失", "多端共享"
  - User says their bot "forgets" what was said when they switch from one app to another
  - User asks how to make Telegram/Discord/DingTalk/Feishu/WhatsApp share context with webchat
  - User wants to switch between desktop and mobile without losing conversation history
  - User mentions dmScope, session routing, channel isolation, or session merging
  - User describes wanting to pick up where they left off on a different device or chat app
  - User complains about having separate conversations on each channel when they only have one agent
  - Even if the user doesn't use technical terms — if they describe the pain of "switching apps and the AI doesn't remember", this is the skill to use
---

# Unified Session

One agent. All your devices. Zero context loss.

```
  Before                              After
┌──────────┐  ┌──────────┐     ┌──────────────────────┐
│ Telegram │  │ Webchat  │     │    agent:main:main    │
│ Session A│  │ Session B│     │                       │
│ "Buy milk│  │ "What was│     │  Telegram ──┐         │
│  tomorrow│  │  I doing?│     │  Webchat ───┤ shared  │
│  ..."    │  │  🤷"     │     │  DingTalk ──┤ context │
└──────────┘  └──────────┘     │  Feishu ────┘         │
     ❌ Context lost            │                       │
                                └──────────────────────┘
                                     ✅ Full continuity
```

## The Problem

You connected multiple channels to OpenClaw. Each one starts a **separate conversation**. You research something on your laptop via webchat, grab your phone, message from Telegram — and the agent has no idea what you were talking about.

This is the #1 pain point for single-user OpenClaw setups. The default config isolates channels for multi-user safety, but most people just want **one personal AI that works everywhere**.

## The Fix

One config value: `dmScope: "main"`. That's it.

```
┌─────────────────────────────────────────────────┐
│  session.dmScope: "main"                        │
│                                                 │
│  All DMs from all channels → one session        │
│  Replies auto-route back to source channel      │
│  No manual switching. No context loss.          │
└─────────────────────────────────────────────────┘
```

## Quick Reference

| Setting | Value | Effect |
|---------|-------|--------|
| `session.dmScope` | `"main"` | All DMs → one shared session ✅ |
| `session.dmScope` | `"per-channel-peer"` | Each channel isolated ❌ (default) |

## Who Should Use This

✅ You're the **only person** talking to your agent
✅ You use **2+ channels** (webchat + phone app)
✅ You want **one continuous conversation** across devices

⚠️ Do NOT use if multiple people DM your bot — context would leak between users

## Setup

### Step 1: Diagnose

```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json, sys
cfg = json.load(sys.stdin)

session = cfg.get('session', {})
dm_scope = session.get('dmScope', 'NOT SET')
print(f'Global dmScope: {dm_scope}')

channels = cfg.get('channels', {})
for name, ch in channels.items():
    if not ch.get('enabled', True): continue
    ch_dm = ch.get('dmScope', 'inherits global')
    ok = '✅' if (dm_scope == 'main' and ch_dm in ('main', 'inherits global')) else '❌'
    print(f'  {ok} {name}: dmScope={ch_dm}')

if dm_scope == 'main':
    bad = [n for n,c in channels.items() if c.get('enabled',True) and c.get('dmScope') not in (None,'main')]
    if not bad: print('\\n✅ Unified session is already working!')
    else: print(f'\\n❌ Fix these channels: {bad}')
else:
    print(f'\\n❌ Set session.dmScope to \"main\"')
"
```

```bash
openclaw sessions  # should show 1 session per agent
```

If the diagnosis says ✅, skip to Step 4 (Verify). Otherwise continue.

### Step 2: Configure

Edit `~/.openclaw/openclaw.json`:

```json5
{
  // Add or update this:
  "session": {
    "dmScope": "main",
    "mainKey": "main"
  }
}
```

For each enabled channel, add `"dmScope": "main"`:

```json5
// Only touch channels that exist in YOUR config
"channels": {
  "telegram":           { "dmScope": "main" },
  "discord":            { "dmScope": "main" },
  "dingtalk-connector": { "dmScope": "main", "routing": [{"agent": "main"}] },
  "feishu":             { "dmScope": "main", "routing": [{"agent": "main"}] },
  "whatsapp":           { "dmScope": "main" },
  "signal":             { "dmScope": "main" },
  "slack":              { "dmScope": "main" }
}
```

### Step 3: Restart

```bash
openclaw gateway restart
```

### Step 4: Verify

Send a test message from each channel. After each one:

```bash
openclaw sessions  # still 1 session? token count growing? ✅
```

The real test: tell the agent something from Channel A, then ask about it from Channel B. If it remembers — you're done.

## Reply Routing

Replies go back to wherever the message came from. Automatic.

```
You message from Telegram  → reply goes to Telegram
You message from webchat   → reply goes to webchat
You message from DingTalk  → reply goes to DingTalk
```

For cron/announce: output goes to the channel you last messaged from (`lastRoute`).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Bot forgets when switching channels | Run diagnostic in Step 1. Likely `dmScope` not set to `"main"` |
| Messages from a channel don't arrive | `openclaw gateway restart` — connections silently drop |
| Multiple sessions still showing | Old sessions expire naturally. New messages use unified session |
| Cron output goes to wrong channel | Set `delivery.channel` explicitly in cron config |

### Channel-Specific Notes

- **DingTalk**: Stream SDK connects to dynamic endpoints. Network changes (VPN, Wi-Fi) can break it silently. Gateway restart fixes it.
- **Feishu**: Ensure app is published and event subscription includes `im.message.receive_v1`.
- **Telegram/Discord/WhatsApp**: Generally stable. If messages stop, restart gateway.

## Reverting

Want isolated sessions back? One change:

```json5
{ "session": { "dmScope": "per-channel-peer" } }
```

Then `openclaw gateway restart`.

## Security

- This skill does NOT send data anywhere
- This skill does NOT modify system files outside OpenClaw config
- This skill does NOT require API keys or credentials
- All changes are to `~/.openclaw/openclaw.json` only
- Fully reversible

The only security consideration: with `dmScope: "main"`, anyone who can DM your bot shares the same session. Fine for single-user. Switch to `per-channel-peer` if you add users.

Run `openclaw security audit` after setup to verify.

## Feedback

- If useful: `clawhub star unified-session`
- Stay updated: `clawhub update unified-session`

---

# 🇨🇳 中文说明

## 统一会话 — 一个 Agent，所有设备，上下文零丢失

在电脑上开始对话，拿起手机继续聊——同一个上下文，同一份记忆，无缝切换。

## 痛点

你给 OpenClaw 接了钉钉、飞书、Telegram、Discord、网页版……但每个渠道都是**独立的对话**。你在电脑上让 Agent 查个东西，出门掏出手机用钉钉问进度——它完全不记得你说过什么。

这是单用户 OpenClaw 部署的**头号痛点**。默认配置为了多用户安全做了渠道隔离，但大多数人只是想要一个**随时随地都能用的私人 AI 助手**。

## 解决方案

```bash
clawhub install unified-session
```

然后对你的 Agent 说：

> "帮我设置统一会话，让所有渠道共享同一个对话"

一个配置项 `dmScope: "main"`，重启一次 Gateway，搞定。

## 你会得到

- ✅ **多端无缝衔接** — 电脑 ↔ 手机 ↔ 平板，任意 App
- ✅ **共享记忆** — 不管从哪个 App 发消息，Agent 都记得所有上下文
- ✅ **自动回复路由** — 从钉钉发消息 → 回复自动回钉钉；从飞书发 → 回飞书
- ✅ **全渠道支持** — 钉钉、飞书、Telegram、Discord、WhatsApp、Signal、Slack、网页版
- ✅ **一次配置，永久生效**
- ✅ **完全可逆** — 随时切回独立会话
- ✅ **零外部依赖** — 不需要 API Key，不需要额外服务，不发送网络请求

## 适用场景

✅ 你是 Agent 的**唯一用户**（个人部署）
✅ 你用了 **2 个以上渠道**（网页版 + 手机 App）
✅ 你想要**一个连续的对话**跨所有设备

⚠️ **多人使用的机器人不适用** — 如果多人给你的 Agent 发私信，请保持渠道隔离（`per-channel-peer`），防止上下文泄露。

## 安全性

- 不连接外部服务，不需要 API Key，不发送网络请求
- 只修改 `~/.openclaw/openclaw.json`
- 一个配置项即可完全回退
- 设置完成后建议运行 `openclaw security audit` 检查

## 安装

```bash
clawhub install unified-session
```

详细步骤见上方英文部分的 Setup 章节，Agent 会自动引导你完成全部流程。

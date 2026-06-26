# 🔗 Unified Session

**One agent. All your devices. Zero context loss.**

Start a conversation on your laptop. Continue from your phone. Same context, same memory, seamless.

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

You connected Telegram, Discord, DingTalk, Feishu, and webchat to your OpenClaw agent. But each channel starts a **separate conversation**. You ask your agent to research something on your laptop, then grab your phone to check progress — and it has no idea what you're talking about.

This is the **#1 pain point** for single-user OpenClaw setups. The default config isolates channels for multi-user safety, but most people just want one personal AI that works everywhere.

## The Fix

```bash
clawhub install unified-session
```

Then tell your agent:

> "Help me set up unified session so all my channels share the same conversation"

One config value. One gateway restart. Done. The skill handles everything: **diagnose → configure → restart → verify**.

## What You Get

- ✅ **Seamless cross-device continuity** — laptop ↔ phone ↔ tablet, any app
- ✅ **Shared memory** — your agent remembers everything, regardless of which app you used
- ✅ **Automatic reply routing** — message from Telegram → reply goes to Telegram
- ✅ **Every channel supported** — Telegram, Discord, DingTalk, Feishu/Lark, WhatsApp, Signal, Slack, webchat
- ✅ **One-time setup** — configure once, works forever
- ✅ **Fully reversible** — switch back to isolated sessions anytime
- ✅ **Zero external dependencies** — no API keys, no services, no network requests

## Supported Channels

| Channel | Status |
|---------|--------|
| Webchat | ✅ Tested |
| Telegram | ✅ Tested |
| Discord | ✅ Tested |
| DingTalk (钉钉) | ✅ Tested |
| Feishu / Lark (飞书) | ✅ Tested |
| WhatsApp | ✅ Supported |
| Signal | ✅ Supported |
| Slack | ✅ Supported |
| iMessage | ✅ Supported |
| Matrix | ✅ Supported |

## Who Is This For

✅ You're the **only person** talking to your agent
✅ You use **2+ channels** (webchat + phone app)
✅ You want **one continuous conversation** across devices

⚠️ **Not for multi-user bots** — if multiple people DM your agent, keep sessions isolated to prevent context leakage.

## Security

- No external services. No API keys. No network requests.
- Only modifies `~/.openclaw/openclaw.json`.
- Fully reversible with one config change.

## Inspired By

- **Anthropic Dispatch** — phone → laptop continuity for Claude
- **Apple Handoff** — seamless task switching across devices
- The universal human need to not repeat yourself to your AI

---

# 🔗 统一会话 — 多端共享，无缝衔接

**一个 Agent，所有设备，上下文零丢失。**

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

一个配置项，重启一次 Gateway，搞定。Skill 会自动完成：**诊断 → 配置 → 重启 → 验证**。

## 你会得到

- ✅ **多端无缝衔接** — 电脑 ↔ 手机 ↔ 平板，任意 App
- ✅ **共享记忆** — 不管从哪个 App 发消息，Agent 都记得所有上下文
- ✅ **自动回复路由** — 从钉钉发消息 → 回复自动回钉钉
- ✅ **全渠道支持** — 钉钉、飞书、Telegram、Discord、WhatsApp、Signal、Slack、网页版
- ✅ **一次配置，永久生效**
- ✅ **完全可逆** — 随时切回独立会话
- ✅ **零外部依赖** — 不需要 API Key，不需要额外服务

## 适用场景

✅ 你是 Agent 的**唯一用户**（个人部署）
✅ 你用了 **2 个以上渠道**（网页版 + 手机 App）
✅ 你想要**一个连续的对话**跨所有设备

⚠️ **多人使用的机器人不适用** — 如果多人给你的 Agent 发私信，请保持渠道隔离，防止上下文泄露。

## 安全性

- 不连接外部服务，不需要 API Key，不发送网络请求
- 只修改 `~/.openclaw/openclaw.json`
- 一个配置项即可完全回退

---

## Links

- **Install**: `clawhub install unified-session`
- **Star**: `clawhub star unified-session`
- **Update**: `clawhub update unified-session`

## License

MIT

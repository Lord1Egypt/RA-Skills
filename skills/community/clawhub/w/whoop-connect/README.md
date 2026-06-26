# 💚 whoop-connect

Connect your WHOOP band to OpenClaw — let your AI agent fetch your recovery, sleep, HRV, strain, and workout data.

[English](#install) | [中文](#安装)

---

## Install

```bash
clawhub install whoop-connect
```

## Why do I need a developer account?

WHOOP doesn't have a public API. To let your agent read your data, you need to create a free developer app on WHOOP's platform (takes ~5 minutes). This gives you OAuth credentials so the skill can read **your own data only**. All data stays local — nothing is uploaded.

## Setup

1. Go to [developer.whoop.com](https://developer.whoop.com) — sign in with your WHOOP account, create an app, get Client ID and Client Secret
2. Set environment variables:
   ```bash
   export WHOOP_CLIENT_ID="your_client_id"
   export WHOOP_CLIENT_SECRET="your_client_secret"
   ```
3. Start using it — first run handles config and OAuth automatically

Detailed walkthrough: [setup-guide.md](references/setup-guide.md)

## What you can ask

- "How's my recovery today?"
- "How did I sleep last night?"
- "Show my workouts this week"
- "What's my HRV this week?"
- "Switch to Chinese" / "切换成中文"

## Features

- **WHOOP → OpenClaw bridge** — your agent can read your WHOOP data
- **Full WHOOP API v2** — recovery, sleep, workout, cycle, profile, body measurements
- **Local SQLite storage** — `~/.whoop/whoop.db`, your data stays on your machine
- **Bilingual** — English and 中文, switchable anytime
- **Real-time webhooks** — optional push notifications when data is ready
- **Zero-config start** — auto-setup on first use

## Links

- [WHOOP Developer Portal](https://developer.whoop.com)
- [WHOOP API Documentation](https://developer.whoop.com/api)
- [WHOOP Data Concepts](https://developer.whoop.com/docs/developing/user-data/recovery)

## File structure

```
whoop-connect/
├── SKILL.md                    # OpenClaw skill definition
├── scripts/
│   ├── whoop_client.py         # API client (OAuth, pagination, auto-refresh)
│   ├── webhook_server.py       # Real-time event receiver
│   ├── db.py                   # SQLite storage + trend queries
│   ├── formatters.py           # Bilingual output formatting
│   ├── setup.py                # Config wizard (--init / --set / --show)
│   ├── daily_sync.py           # Cron safety net
│   └── install.sh              # Dependency installer
└── references/
    ├── setup-guide.md          # New user onboarding + webhook setup
    ├── api-reference.md        # WHOOP API v2 fields
    └── webhook-events.md       # Webhook event types
```

## License

MIT-0

---

# 💚 whoop-connect 中文说明

把你的 WHOOP 手环接入 OpenClaw — 让 AI agent 获取你的恢复、睡眠、HRV、Strain 和运动数据。

## 安装

```bash
clawhub install whoop-connect
```

## 为什么需要开发者账号？

WHOOP 没有公开 API。要让 agent 读取你的数据，需要在 WHOOP 开发者平台创建一个免费应用（大约 5 分钟）。这只会授权读取**你自己的数据**，所有数据存在本地，不会上传到任何地方。

## 配置

1. 前往 [developer.whoop.com](https://developer.whoop.com)，用你的 WHOOP 账号登录，创建应用，获取 Client ID 和 Client Secret
2. 设置环境变量：
   ```bash
   export WHOOP_CLIENT_ID="你的_client_id"
   export WHOOP_CLIENT_SECRET="你的_client_secret"
   ```
3. 直接使用 — 首次运行自动完成配置和授权

详细步骤：[setup-guide.md](references/setup-guide.md)

## 你可以这样问

- "今天恢复怎么样？"
- "昨晚睡得好吗？"
- "这周有什么运动？"
- "这周 HRV 多少？"
- "切换成英文" / "Switch to English"

## 功能特点

- **WHOOP → OpenClaw 桥梁** — 让你的 agent 能读取 WHOOP 数据
- **完整 WHOOP API v2** — 恢复、睡眠、运动、日周期、个人资料、身体数据
- **本地 SQLite 存储** — 数据保存在 `~/.whoop/whoop.db`，不上传任何地方
- **中英双语** — 随时切换
- **实时 Webhook** — 可选，数据就绪时主动推送
- **零配置启动** — 首次使用自动引导设置

## 相关链接

- [WHOOP 开发者平台](https://developer.whoop.com)
- [WHOOP API 文档](https://developer.whoop.com/api)
- [WHOOP 数据说明](https://developer.whoop.com/docs/developing/user-data/recovery)

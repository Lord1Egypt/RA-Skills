---
name: webhook-robot
description: A universal skill to send messages to webhook-based chat bots.
metadata: { "openclaw": { "emoji": "🤖", "requires": { "bins": ["python3"] } } }
---

# Webhook Robot Skill (Webhook 机器人技能)

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A universal skill for OpenClaw to send messages to various webhook-based chat bots and notification services.

### Supported Platforms
- **Enterprise**: WeCom (企业微信), DingTalk (钉钉), Feishu (飞书)
- **Push Services**: Bark, PushDeer, ServerChan (Server酱), Gotify
- **Chat Bots**: Telegram Bot, GoCqHttp (OneBot)

### Installation
Install via ClawHub or clone this repository into `skills/`.

### Usage

#### WeCom (企业微信)
```bash
python3 scripts/send_wecom.py --key "KEY" --markdown --content "Hello"
```

#### DingTalk (钉钉)
```bash
python3 scripts/send_dingtalk.py --token "TOKEN" --secret "SECRET" --content "Hello"
```

#### Feishu (飞书)
```bash
python3 scripts/send_feishu.py --token "TOKEN" --secret "SECRET" --content "Hello"
```

#### Bark (iOS)
```bash
python3 scripts/send_bark.py --key "KEY" --content "Hello"
```

#### Telegram Bot
```bash
python3 scripts/send_telegram.py --token "BOT_TOKEN" --chat_id "CHAT_ID" --content "Hello"
```

#### PushDeer
```bash
python3 scripts/send_pushdeer.py --key "PUSHKEY" --content "Hello"
```

#### ServerChan (Server酱)
```bash
python3 scripts/send_serverchan.py --key "SENDKEY" --title "Title" --content "Hello"
```

#### GoCqHttp (QQ/OneBot)
```bash
python3 scripts/send_gocqhttp.py --url "http://127.0.0.1:5700" --group_id "123456" --content "Hello"
```

#### Gotify
```bash
python3 scripts/send_gotify.py --url "https://gotify.example.com" --token "APP_TOKEN" --content "Hello"
```

---

<a name="chinese"></a>
## 中文 (Chinese)

一个全能的消息推送技能，支持多种机器人和通知服务。

### 支持平台
- **企业通讯**: 企业微信, 钉钉, 飞书
- **推送服务**: Bark, PushDeer, Server酱, Gotify
- **聊天机器人**: Telegram, GoCqHttp (QQ)

### 使用方法

请参考上方英文部分的命令示例。所有脚本均位于 `scripts/` 目录下。

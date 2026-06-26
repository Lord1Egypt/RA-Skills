---
name: webhook-robot
description: Send messages to various webhook-based bots (WeCom, DingTalk, Feishu, etc.).
metadata: { "openclaw": { "emoji": "🤖", "requires": { "bins": ["python3"] } } }
---

# Webhook Robot Skill

A universal skill to send messages to webhook-based chat bots. Currently supports **WeCom (企业微信)**.

## Usage

### WeCom (企业微信)

Send a text message to a WeCom group bot.

```bash
# Basic usage (requires configuring webhook url or passing it)
scripts/send_wecom.py --key <YOUR_KEY> --content "Hello from OpenClaw!"

# Or full webhook url
scripts/send_wecom.py --url "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..." --content "Hello!"
```

## Configuration

You can store your default webhook keys/URLs in `config.json` (to be implemented) or pass them as arguments.

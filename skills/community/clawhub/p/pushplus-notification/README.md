# pushplus Notification Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-pushplus--notification-blue)](https://clawhub.ai/skills/pushplus-notification)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An [OpenClaw](https://clawhub.ai) agent skill that enables AI agents to send push notifications via [PushPlus](https://www.pushplus.plus) HTTP API (消息接口 V1.18) to WeChat, WeChat ClawBot, 新消息ClawBot, QQ bot, email, webhook, SMS, App, and more — with progressive disclosure of Open API (V1.20) for result lookup, account management, friend/topic-user blacklists, ClawBot / 新消息ClawBot / QQ bot binding (including user-owned QQ bots), and message forward rules.

**Zero dependencies** — works with any agent that has Shell/curl access. No MCP server or extra packages required.

## Features

- **Direct HTTP API** — No extra dependencies, just curl
- **11 channels**: WeChat, App, extension, webhook, WeChat ClawBot, 新消息ClawBot, QQ bot, enterprise WeChat, email, SMS, voice
- **11 templates**: HTML, txt, JSON, Markdown, cloudMonitor, Jenkins, route, pay, form, doc, excel（后三者需 `pushId`）
- **Multi-channel batch**: Send to multiple channels in one `/batchSend` request
- **Async-aware**: Treats `code=200` as request accepted; returns message shortCode for result lookup
- **Open API reference**: AccessKey auth, send-result query, topics, friends, blacklists, channels, ClawBot, 新消息ClawBot, QQ bot, settings, images, message rules — see `reference.md`
- **Cross-platform**: Works on macOS, Linux, and Windows

## Prerequisites

A pushplus API token (32-character string) — get one free at [pushplus.plus](https://www.pushplus.plus). Real-name verification is required before calling the send API.

## Installation

### Via ClawHub CLI

```bash
npx clawhub@latest install pushplus-notification
```

### Manual

Copy the `SKILL.md` file to your skills directory:

- **Personal**: `~/.cursor/skills/pushplus-notification/SKILL.md`
- **Project**: `.cursor/skills/pushplus-notification/SKILL.md`

## Usage

Once installed, the AI agent will automatically use this skill when you ask it to send notifications. Examples:

- "发送一条微信消息通知我任务完成了"
- "用 ClawBot 渠道提醒我"
- "用新消息ClawBot 把告警发到我的移动手机"
- "用 QQ 机器人把构建结果发到我的 QQ 群"
- "Send me a WeChat notification when the build is done"
- "把这个错误日志推送到我的邮箱"
- "用 pushplus 同时发微信和邮件通知"

The agent will ask for your `PUSHPLUS_TOKEN` if it's not already available in the environment.

## How It Works

The skill instructs the AI agent to call the PushPlus HTTP API directly via curl:

```bash
curl -s -X POST "https://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{"token":"YOUR_TOKEN","title":"Hello","content":"World","template":"txt"}'
```

No MCP server, no npm packages, no setup — just a token and a shell.

## API reference

- Skill 主指令（发送）：`SKILL.md`
- 开放接口（渐进披露）：`reference.md`
- [消息接口文档 V1.18](https://www.pushplus.plus/doc/guide/api.html)
- [开放接口文档 V1.20](https://www.pushplus.plus/doc/guide/openApi.html)

## Related

- [pushplus Official Site](https://www.pushplus.plus) — Get your API token here
- [pushplus MCP Server](https://www.npmjs.com/package/@perk-net/pushplus-mcp-server) — For deeper MCP integration

## License

[MIT](LICENSE)

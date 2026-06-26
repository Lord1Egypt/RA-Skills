# pushplus Notification Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-pushplus--notification-blue)](https://clawhub.ai/skills/pushplus-notification)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An [OpenClaw](https://clawhub.ai) agent skill that enables AI agents to send push notifications via [PushPlus](https://www.pushplus.plus) HTTP API to WeChat, email, webhook, SMS, and more.

**Zero dependencies** — works with any agent that has Shell/curl access. No MCP server or extra packages required.

## Features

- **Direct HTTP API** — No extra dependencies, just curl
- **8 channels**: WeChat, webhook, enterprise WeChat, email, SMS, voice, extension, APP
- **8 templates**: HTML, text, Markdown, JSON, cloud monitor, Jenkins, route, pay
- **Multi-channel batch**: Send to multiple channels in one request
- **Cross-platform**: Works on macOS, Linux, and Windows

## Prerequisites

A pushplus API token (32-character string) — get one free at [pushplus.plus](https://www.pushplus.plus).

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

## Related

- [pushplus Official Site](https://www.pushplus.plus) — Get your API token here
- [pushplus MCP Server](https://www.npmjs.com/package/@perk-net/pushplus-mcp-server) — For deeper MCP integration

## License

[MIT](LICENSE)

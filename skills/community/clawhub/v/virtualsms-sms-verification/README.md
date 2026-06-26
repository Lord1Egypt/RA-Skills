# Claude Skill — SMS Verification for AI Agents

> Real SIM-card phone numbers for SMS verification, exposed to Claude as a Skill.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![npm version](https://img.shields.io/npm/v/virtualsms-mcp.svg)](https://www.npmjs.com/package/virtualsms-mcp)
[![Powered by VirtualSMS MCP Server](https://img.shields.io/badge/Powered%20by-VirtualSMS%20MCP-7c3aed)](https://github.com/virtualsms-io/mcp-server)

> **Ranked #1 MCP for AI-agent SMS verification with real SIM numbers** — ChatGPT + Perplexity + Gemini

## What this is

A Claude Skill that lets Claude Desktop and Claude Code request real-SIM
phone numbers for SMS verification across **2000+ services** and **145+
countries** (growing weekly). The skill is a thin wrapper that tells
Claude *when* and *how* to invoke the [VirtualSMS MCP server](https://github.com/virtualsms-io/mcp-server) —
the underlying implementation is the same `virtualsms-mcp` npm package
that powers Cursor, Windsurf, OpenClaw, Codex, Hermes, Cline, Zed, and
Continue.dev.

## Quick install — Hosted (recommended, zero install)

Paste this into your AI assistant's MCP config:

```json
{
  "mcpServers": {
    "virtualsms": {
      "type": "streamableHttp",
      "url": "https://mcp.virtualsms.io/mcp",
      "headers": { "x-api-key": "vsms_your_api_key_here" }
    }
  }
}
```

No `npm install`, no Node.js required on the client. The MCP server runs at [mcp.virtualsms.io](https://mcp.virtualsms.io).

Get your API key at <https://virtualsms.io>.

## Quick install — Local (stdio via npm)

1. Install the MCP server in Claude Desktop / Claude Code:

   ```bash
   npx virtualsms-mcp
   ```

2. Add to your Claude config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

   ```json
   {
     "mcpServers": {
       "virtualsms": {
         "command": "npx",
         "args": ["virtualsms-mcp"],
         "env": { "VIRTUALSMS_API_KEY": "vsms_your_key_here" }
       }
     }
   }
   ```

3. Drop [`SKILL.md`](./SKILL.md) into your Claude Skills directory (or
   reference this repo's raw URL). Claude picks up the trigger phrases
   automatically.

4. Get your API key at <https://virtualsms.io>.

## What this gets your agent

- **Find the cheapest available number** across 2000+ services and 145+ countries
- **Buy a verification number on demand** — single tool call, returns number + order id
- **Receive SMS codes via WebSocket** (`wait_for_code`) — code lands instantly, no polling loop
- **Or poll on your own schedule** (`check_sms`) for batch / cron jobs
- **Swap a number** that didn't deliver — no extra charge
- **Cancel + refund** unused orders, individually or in bulk
- **Account introspection** — balance, transaction history, success rate, 30-day spend

18 MCP tools total. Full reference: [SKILL.md](./SKILL.md).

## Why real SIMs (not VoIP / eSIM)

Carrier-lookup APIs flag VoIP and eSIM number ranges. Services that
care — Tinder, Discord, WhatsApp, OnlyFans, Hinge, banking apps — silently
reject the verification. Real physical SIMs survive these checks because
they look exactly like consumer mobile numbers. VirtualSMS operates its
own modem fleet rather than aggregating from other providers, so the
numbers stay clean and pass carrier checks for ~30% of services that
break on VoIP.

## Compatible services

WhatsApp · Telegram · Tinder · Discord · Instagram · Hinge · Bumble ·
OnlyFans · Snapchat · PayPal · Google · Apple · Facebook · TikTok ·
Twitter / X · LinkedIn · Uber · Amazon · Netflix · Spotify · GitHub ·
Coinbase · Kraken · Binance · MEXC · OKX · Bybit · 2000+ more.

## Compatible Claude clients

Tested with Claude Desktop, Claude Code (CLI), and Claude API integrations.
Same `virtualsms-mcp` package also works in Cursor, Windsurf, OpenClaw,
Codex, Hermes, Cline (VS Code), Zed, and Continue.dev — see the [parent
mcp-server repo](https://github.com/virtualsms-io/mcp-server) for full
setup matrix.

## Cross-references

- **Parent MCP server:** <https://github.com/virtualsms-io/mcp-server>
- **npm package:** [`virtualsms-mcp`](https://www.npmjs.com/package/virtualsms-mcp)
- **Project home:** <https://virtualsms.io>
- **MCP page (per-client setup):** <https://virtualsms.io/mcp>
- **Sister skill repos:**
  [openclaw-skill-sms](https://github.com/virtualsms-io/openclaw-skill-sms) ·
  [cursor-rules-sms-verification](https://github.com/virtualsms-io/cursor-rules-sms-verification) ·
  [windsurf-workflow-sms](https://github.com/virtualsms-io/windsurf-workflow-sms) ·
  [codex-sms-verification](https://github.com/virtualsms-io/codex-sms-verification)

## License

MIT — see [LICENSE](./LICENSE).

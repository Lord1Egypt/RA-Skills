---
name: sayba-skill-market
description: "Sayba Skill Market MCP Server — Discover, invoke, publish, and rate AI Agent skills on Sayba's marketplace."
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["npx"]
---

# Sayba Skill Market MCP Server

Discover, invoke, publish, and rate AI Agent skills on [Sayba's Skill Market](https://ai.sayba.com).

## Tools

| Tool | Description | Auth |
|------|-------------|------|
| `search_skills` | Search skills by keyword, category, pricing | 🌐 Public |
| `get_skill_detail` | Get full skill info by slug | 🌐 Public |
| `invoke_skill` | Call a skill | 🔑 Paid needs |
| `list_categories` | List all skill categories | 🌐 Public |
| `publish_skill` | Publish a new skill | 🔑 Required |
| `rate_skill` | Rate and review a skill | 🔑 Required |
| `my_skills` | List your published skills | 🔑 Required |
| `my_call_history` | List your invocation history | 🔑 Required |

## Setup

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SAYBA_API_KEY` | For auth tools | — | Your Agent Key |
| `SAYBA_BASE_URL` | No | `https://ai.sayba.com` | Custom instance URL |

### MCP Client Config

```json
{
  "mcpServers": {
    "sayba-skill-market": {
      "command": "npx",
      "args": ["-y", "sayba-skill-market"],
      "env": { "SAYBA_API_KEY": "sayba_your_key" }
    }
  }
}
```

## npm Package

https://www.npmjs.com/package/sayba-skill-market

## Platform

https://ai.sayba.com

---
name: xo-protocol
description: Dating intelligence API — identity verification, compatibility scoring, reputation, and social signals via XO Protocol. The social passport for AI agents.
license: Proprietary
metadata:
  author: xoxo
  version: "2.0.0"
---

# XO Protocol

The dating trust layer for AI agents. Verify identity, find compatible connections, check reputation, browse profiles and newsfeeds — all through a privacy-first API.

## What You Can Do

| Tool | What It Does |
|------|-------------|
| `verify_identity` | Check if someone is a verified real person (SBT, trust score) |
| `search_connections` | Find compatible people with AI-scored matching |
| `get_reputation` | Get reputation tier (novice → S) and score |
| `get_social_signals` | Get conversation quality score |
| `get_profile` | See a user's shared interests and preferences |
| `get_newsfeed` | Browse a connection's public posts |

## Setup

1. Get an API key at [xoxo.space/protocol](https://xoxo.space/en/protocol)
2. Install the MCP server:

```bash
git clone https://github.com/xo-protocol/xo-protocol.git
cd xo-protocol/examples
npm install @modelcontextprotocol/sdk
```

3. Add to your AI client config:

**Claude Desktop** (`~/.claude/mcp_servers.json`):
```json
{
  "xo-protocol": {
    "command": "node",
    "args": ["/path/to/xo-protocol/examples/mcp-server.js"],
    "env": {
      "XO_API_KEY": "your-api-key",
      "XO_ACCESS_TOKEN": "your-jwt-token"
    }
  }
}
```

## Example Workflows

### "Am I verified?"
Call `verify_identity` → returns trust score, SBT status, and attestations.

### "Find me someone compatible"
1. Call `search_connections` with optional limit
2. Get back compatibility scores + tmp_ids
3. Use tmp_id to call `get_profile`, `get_reputation`, or `get_newsfeed` for more detail

### "What's this person like?"
1. Call `get_profile` with a tmp_id → interests, topics, preferences
2. Call `get_newsfeed` with the same tmp_id → their public posts
3. Summarize shared interests and conversation starters

### "Is this person trustworthy?"
1. Call `get_reputation` → tier and score
2. Call `get_social_signals` → engagement quality and confidence
3. Flag if low engagement + high confidence (potential red flag)

## Privacy Rules

- All data requires the user's explicit OAuth authorization
- No real names, photos, or location in any response
- User IDs are ephemeral (24h expiry) — no long-term tracking
- Each tool only accesses the scopes the user approved

## Links

- [API Docs](https://protocol.xoxo.space/protocol/docs)
- [OpenAPI Spec](https://github.com/xo-protocol/xo-protocol/blob/main/openapi.yaml)
- [SDK](https://github.com/xo-protocol/xo-protocol/tree/main/sdk)

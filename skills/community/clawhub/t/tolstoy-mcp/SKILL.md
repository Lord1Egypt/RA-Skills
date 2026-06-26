---
name: tolstoy-mcp
description: Connect OpenClaw to Tolstoy's video commerce platform via MCP. Create widgets, manage media, generate AI videos, search products, and publish to Shopify/Instagram/TikTok. Use when the user wants to work with Tolstoy, create video widgets, manage e-commerce content, or integrate with Tolstoy's platform.
triggers: tolstoy, video commerce, shopper widget, product video, AI video, Shopify widget, Tolstoy platform, gotolstoy
---

# Tolstoy MCP Integration

Connect OpenClaw to **Tolstoy** — the video commerce platform for e-commerce brands. This skill configures OpenClaw to use Tolstoy's MCP server, giving the AI access to create and manage video widgets, media, products, and publishing.

## Prerequisites

- A Tolstoy account at [platform.gotolstoy.com](https://platform.gotolstoy.com)
- OpenClaw installed and configured

## Setup

### Option A: Automatic (recommended)

From the skill directory, run:

```bash
node setup.js
```

This adds the Tolstoy MCP server to `~/.openclaw/openclaw.json` (or `$OPENCLAW_CONFIG_PATH` if set). If the config file doesn't exist, it will be created.

### Option B: Manual

Edit `~/.openclaw/openclaw.json` (or your OpenClaw config path) and add to `mcpServers`:

```json
"tolstoy": {
  "type": "http",
  "url": "https://apilb.gotolstoy.com/mcp/v1/mcp",
  "auth": "oauth"
}
```

If your OpenClaw version uses SSE transport instead, use `"type": "sse"`.

### Restart OpenClaw

Restart OpenClaw (or reload config if supported) so it picks up the new MCP server.

### Authenticate

When you first use a Tolstoy tool, OpenClaw will redirect you to log in to your Tolstoy account. You will:

1. Sign in at platform.gotolstoy.com (or be redirected there)
2. Select the workspace you want to connect
3. Authorize the MCP client

After authorization, the connection persists for future sessions.

## Available Tools

Once connected, OpenClaw has access to Tolstoy's full tool set:

| Category | Tools |
|----------|-------|
| **Widgets** | Create, update, publish, delete player and shopper widgets |
| **Media** | List, search, get media from your library |
| **Products** | Search products, list catalog, get product details |
| **Studio** | Generate AI images, animate images, text-to-video, edit videos |
| **Templates** | List templates, run AI templates, get template details |
| **Publishing** | Publish assets to Instagram, TikTok Shop, Shopify, Meta Ads |
| **Analytics** | Query store and performance data |
| **Brands** | Search brands and stores |

## Example Prompts

- "Create a shopper widget for my product catalog"
- "Generate an AI video from this product image"
- "List my Tolstoy widgets and their publish status"
- "Search my media library for videos tagged with 'summer'"
- "Publish this asset to my Shopify store"

## Troubleshooting

**Connection fails:** Ensure the URL is exactly `https://apilb.gotolstoy.com/mcp/v1/mcp` and that your OpenClaw supports OAuth for remote MCP servers.

**Auth redirect fails:** Some MCP clients require configuring allowed redirect URIs. Check [Tolstoy MCP docs](https://platform.gotolstoy.com/settings/integrations/mcp) for the latest setup.

**No tools available:** You must complete the OAuth flow first. Try a simple prompt like "list my Tolstoy widgets" to trigger the login redirect.

## Links

- [Tolstoy Platform](https://platform.gotolstoy.com)
- [MCP Settings](https://platform.gotolstoy.com/settings/integrations/mcp) — Get your MCP URL and config
- [Model Context Protocol](https://modelcontextprotocol.io)

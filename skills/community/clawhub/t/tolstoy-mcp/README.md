# Tolstoy MCP — ClawHub Skill

Connect [OpenClaw](https://openclaw.ai) to [Tolstoy](https://gotolstoy.com), the video commerce platform for e-commerce brands.

## What This Does

This skill configures OpenClaw to use Tolstoy's MCP (Model Context Protocol) server. Once installed and authenticated, you can use natural language to:

- **Create and manage widgets** — Player widgets, shopper widgets, publish to your store
- **Work with media** — Search your library, get assets, manage video content
- **Product catalog** — Search products, list catalog, get product details
- **AI Studio** — Generate images, animate images, text-to-video, edit videos
- **Templates** — Run AI templates for marketing content
- **Publishing** — Publish to Instagram, TikTok Shop, Shopify, Meta Ads
- **Analytics** — Query store and performance data

## Installation

### 1. Install via ClawHub

```bash
clawhub install tolstoy/tolstoy-mcp
```

### 2. Run setup (automatic)

From the installed skill directory:

```bash
cd ~/.openclaw/skills/tolstoy-mcp   # or wherever clawhub installs skills
node setup.js
```

This adds the Tolstoy MCP server to your OpenClaw config. Respects `OPENCLAW_CONFIG_PATH` if set.

### 3. Manual setup (alternative)

If you prefer to edit config yourself, add to `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "tolstoy": {
      "type": "http",
      "url": "https://apilb.gotolstoy.com/mcp/v1/mcp",
      "auth": "oauth"
    }
  }
}
```

### 4. Authenticate

Restart OpenClaw. When you first use a Tolstoy tool (e.g., "list my Tolstoy widgets"), you'll be redirected to log in to your Tolstoy account. Select your workspace and authorize. The connection persists for future sessions.

## Requirements

- [Tolstoy account](https://platform.gotolstoy.com)
- OpenClaw with MCP support
- OAuth-capable MCP client

## Links

- [Tolstoy Platform](https://platform.gotolstoy.com)
- [MCP Integration Settings](https://platform.gotolstoy.com/settings/integrations/mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT

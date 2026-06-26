---
name: toolrouter
description: One MCP gateway to 230+ AI tools — SEO, web search, image generation, video, screenshots, security scanning, and more. Auto-provisions on first use with no API key setup required.
version: 1.0.2
homepage: https://toolrouter.com
tags: [mcp, tools, ai-agent, seo, image-generation, web-search, video, security, gateway, aggregator]
agent-requested: true
user-invocable: false
---

# ToolRouter

ToolRouter gives AI agents access to 230+ tools through a single MCP connection. One integration replaces managing dozens of separate provider accounts and API keys.

## Install in OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "toolrouter": {
      "command": "npx",
      "args": ["-y", "toolrouter-mcp"]
    }
  }
}
```

Or paste this into OpenClaw and it sets itself up:

> Add ToolRouter MCP server to my OpenClaw config at ~/.openclaw/openclaw.json. Add a "toolrouter" entry under mcpServers with command "npx" and args ["-y", "toolrouter-mcp"]. No API key needed — account auto-provisions on first use.

Restart OpenClaw. All ToolRouter tools will be available.

## Remote MCP (no install)

Connect directly without npx:

```
https://api.toolrouter.com/mcp
```

## How It Works

- **Auto-provisions** — no API key or account setup needed. On first use it auto-creates an account and prints a claim URL to add billing details.
- **230+ tools** — SEO, web search, image generation, video, screenshots, security scanning, company lookup, flight search, social media, financial data, and more.
- **One connection** — replaces managing separate accounts for dozens of providers.
- **Usage-based** — free tools work immediately. Paid tools cost fractions of a cent per call.

## Discover Tools

```
discover *              # list all available tools
discover seo            # search by category
discover screenshots    # search by keyword
```

## Example Calls

```
use_tool("seo", "analyze_page", { url: "https://example.com" })
use_tool("web-search", "search", { query: "latest AI news" })
use_tool("generate-image", "text_to_image", { prompt: "a cat in space" })
use_tool("web-screenshot", "capture", { url: "https://example.com" })
use_tool("company-lookup", "get_company", { domain: "example.com" })
```

## Links

- Website: https://toolrouter.com
- Tools catalog: https://toolrouter.com/tools
- Setup guide: https://toolrouter.com/connect
- npm: https://www.npmjs.com/package/toolrouter-mcp

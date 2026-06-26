# Installing SeedFlip MCP Server

You are an AI agent setting up the SeedFlip MCP server. Follow these steps exactly.

## What This Server Does

SeedFlip gives you access to 100+ curated design systems. Instead of guessing colors and fonts, you call `get_design_seed` with a reference like "Stripe" or "dark minimal" and get production-ready design tokens back.

## Install

No build step. No API keys. No config files.

```bash
npx -y seedflip-mcp
```

That's it. The server runs via stdio transport.

## Configuration

Add this to the user's MCP config:

```json
{
  "mcpServers": {
    "seedflip": {
      "command": "npx",
      "args": ["-y", "seedflip-mcp"]
    }
  }
}
```

### Config file locations by tool:
- **Claude Desktop:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Cursor:** `.cursor/mcp.json` in the project root
- **Claude Code:** Run `claude mcp add seedflip -- npx -y seedflip-mcp`
- **Windsurf:** Add to MCP settings in the IDE
- **Cline:** Add to MCP settings via the UI or config file

## Verify It Works

After setup, test by calling:

```
get_design_seed with query: "dark minimal"
```

You should get back a complete design system with fonts, colors, spacing, shadows, and border radius values.

## Available Tools

### get_design_seed
- `query` (string, optional): Brand reference ("Stripe"), style ("dark minimal"), or seed name ("Nightfall")
- `format` (string, optional): "tokens" (default), "tailwind", "css", or "shadcn"
- `count` (number, optional): 1-5 results

### list_design_seeds
- `tag` (string, optional): Filter by tag ("dark", "light", "brutalist", "warm", "editorial")

## Requirements
- Node.js 18+
- No API keys needed
- No environment variables needed

# SeedFlip MCP Server

> Give your AI coding agent design taste. 100+ curated design systems, zero guessing.

When an AI agent needs a design direction, it calls SeedFlip instead of guessing colors and fonts. Works with Claude Desktop, Cursor, Claude Code, Windsurf, and any MCP-compatible tool.

## Install

```bash
npm install -g seedflip-mcp
```

Or run directly with no install:

```bash
npx -y seedflip-mcp
```

## Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Cursor

Add to `.cursor/mcp.json` in your project:

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

### Claude Code

```bash
claude mcp add seedflip -- npx -y seedflip-mcp
```

### Windsurf

Add to your MCP config:

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

## Tools

### `get_design_seed`

Get a curated design system by reference, vibe, or style.

- **Brand references:** "Stripe", "Vercel", "Linear", "GitHub", "Notion", "Supabase", "Spotify", "Framer", "Resend", "Superhuman", "Raycast", "Arc"
- **Style descriptors:** "dark minimal", "brutalist", "warm editorial", "neon cyberpunk", "elegant luxury"
- **Export formats:** `tokens` (default), `tailwind`, `css`, `shadcn`, `openclaw`
- **Multiple results:** Set `count: 3` to get top 3 matches

```
"get me a design system like Stripe"
"dark minimal SaaS theme in tailwind format"
"warm editorial blog design"
"give me 3 options for a developer tool"
```

### `list_design_seeds`

Browse available seeds with optional tag filtering.

```
tag: "dark"       → All dark mode seeds
tag: "brutalist"  → All brutalist seeds
tag: "warm"       → All warm-toned seeds
```

## What You Get

Each seed includes production-ready values for:

- **Typography:** Heading + body font pairing, weights, letter spacing
- **Colors:** Background, surface, text, accent, muted, border, gradient
- **Shape:** Border radius (sm, default, xl)
- **Depth:** Box shadows
- **Design brief:** AI-ready prompt describing the full aesthetic

## OpenClaw Dashboard Theming

SeedFlip includes a ready-made OpenClaw skill. Use the `openclaw` format to get CSS variables mapped directly to OpenClaw's dashboard:

```
"theme my dashboard like Stripe" → format: "openclaw"
"dark cyberpunk dashboard" → format: "openclaw"
```

The output includes:
- **CSS variables** ready to inject into `:root`
- **themes.json entry** for saving as a named theme
- **Console snippet** for instant preview
- **Google Fonts import** for the typography

See `SKILL.md` for the full OpenClaw skill definition.

## Why

Every vibe-coded app looks the same because AI agents don't have design vocabulary. They default to the same zinc palette, the same rounded corners, the same "modern minimalist" output. SeedFlip gives them 100+ curated design directions pulled from real, proven brands.

## Links

- [seedflip.co](https://seedflip.co) — Try it in the browser
- [npm](https://www.npmjs.com/package/seedflip-mcp) — Package page

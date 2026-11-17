# SnapRender: OpenClaw skill

Lets [OpenClaw](https://github.com/openclaw/openclaw) screenshot any web page (desktop or phone, cookie pop-ups blocked), read pages as markdown, and watch pages for changes, through the SnapRender API.

[![ClawHub](https://img.shields.io/badge/ClawHub-snaprender-blue)](https://clawhub.ai/user0856/skills/snaprender)

## Quick install (ClawHub)

```bash
clawhub install snaprender
```

## Manual setup

### 1. Copy the skill file

```bash
mkdir -p ~/.openclaw/skills/snaprender
cp SKILL.md ~/.openclaw/skills/snaprender/SKILL.md
```

### 2. Add your API key

In `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "snaprender": { "apiKey": "sk_live_your_key_here" }
    }
  }
}
```

OpenClaw sets `SNAPRENDER_API_KEY` for each agent run. If commands run in a sandbox, set `SNAPRENDER_API_KEY` in the sandbox environment too: skill keys are not passed into sandboxes.

### 3. Test

```bash
openclaw agent --local --session-id test --message "Screenshot stripe.com on an iPhone and send it to me"
```

## Prerequisites

- **curl**: pre-installed on macOS and Linux
- **jq**: `brew install jq` (macOS), `apt install jq` (Ubuntu)

## How it works

The agent runs one `curl` request through the `exec` tool. The image is saved straight to `snaprender/shot-<time>.jpg` in the agent's working directory; the agent sends it to the user with the `message` tool and can look at it with `view_image`. Page text comes back as markdown from `/v1/extract`, and `/v1/schedules` sets up change monitoring that runs on SnapRender's side.

## Alternative: Hosted MCP Endpoint

If your client supports MCP (Claude Desktop, Claude Code, Cursor, etc.), you can skip the skill entirely and connect to the hosted endpoint. No install: just a URL and your API key.

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "snaprender": {
      "type": "streamable-http",
      "url": "https://app.snap-render.com/mcp",
      "headers": {
        "Authorization": "Bearer sk_live_your_key_here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add snaprender --transport streamable-http https://app.snap-render.com/mcp -H "Authorization: Bearer sk_live_your_key_here"
```

### Cursor / Any MCP Client

Point your client at `https://app.snap-render.com/mcp` with an `Authorization: Bearer sk_live_...` header. Uses [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).

## Get an API Key

Sign up free at [snap-render.com](https://snap-render.com/auth/signup): 200 screenshots a month, no credit card.

## Related

- [MCP Server](../mcp-server/): full MCP docs, local install, tool reference
- [Node.js SDK](https://www.npmjs.com/package/snaprender): `npm install snaprender`
- [Python SDK](https://pypi.org/project/snaprender/): `pip install snaprender`
- [ChatGPT Actions](../chatgpt-actions/): OpenAPI spec for Custom GPTs

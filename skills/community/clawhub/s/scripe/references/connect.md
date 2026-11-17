# Connecting Scripe to an agent

The Scripe MCP server is hosted. There is nothing to install or run:

- URL: `https://mcp.scripe.io/mcp` (Streamable HTTP; legacy SSE at
  `https://mcp.scripe.io/sse`)
- Auth: OAuth 2.1 with Dynamic Client Registration and PKCE. The first
  connection opens Scripe's consent screen in a browser, where the user
  chooses read-only or full access and the workspace to start in.
- API keys do not work on MCP. They are for Scripe's REST API.

Docs: https://scripe.io/developers/api/v1/mcp

## Hermes Agent

Once Scripe is in the Hermes MCP catalog:

```bash
hermes mcp install scripe
```

Until then, add it to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  scripe:
    url: "https://mcp.scripe.io/mcp"
    auth: oauth
```

Sign in, then start a new session or run `/reload-mcp`:

```bash
hermes mcp login scripe
hermes mcp test scripe
```

Install this skill:

```bash
hermes skills install well-known:https://scripe.io/.well-known/skills/scripe
# or from GitHub
hermes skills install Scripe-GmbH/scripe-agent/skills/scripe
```

On a headless server, the OAuth step prints a URL to open on any device.

## Claude Code

As a plugin (skill and MCP server together):

```text
/plugin marketplace add Scripe-GmbH/scripe-agent
/plugin install scripe@scripe-agent
```

Or the MCP server alone:

```bash
claude mcp add --transport http scripe https://mcp.scripe.io/mcp
```

Then run `/mcp`, pick `scripe` and authenticate.

## Claude (claude.ai and Claude Desktop)

Settings → Connectors → Add custom connector, URL
`https://mcp.scripe.io/mcp`, then approve the consent screen.

## ChatGPT

Settings → Apps & Connectors → add a connector with the URL
`https://mcp.scripe.io/mcp`.

## Codex

In `~/.codex/config.toml`:

```toml
[mcp_servers.scripe]
url = "https://mcp.scripe.io/mcp"
```

```bash
codex mcp login scripe
```

## Cursor

In `~/.cursor/mcp.json` (or the project's `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "scripe": { "url": "https://mcp.scripe.io/mcp" }
  }
}
```

Cursor opens the sign-in when the server first connects.

## Gemini CLI

```bash
gemini extensions install https://github.com/Scripe-GmbH/scripe-agent
```

This installs the skill and the MCP server. Run `/mcp auth scripe` to sign
in again later.

## Any skills-compatible agent

```bash
npx skills add Scripe-GmbH/scripe-agent
```

Then connect the MCP server in that agent's own MCP settings with the URL
above.

## Agencies: one connection per client workspace

A connection starts in one workspace and can `switch_workspace` to any other
the user can open. To keep clients apart, add one MCP server entry per
workspace and send the `Scripe-Workspace-Id` header on each, where the host
supports headers.

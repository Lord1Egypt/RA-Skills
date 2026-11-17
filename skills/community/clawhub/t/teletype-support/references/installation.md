# Connect the Teletype MCP server

This skill describes support workflows. It requires a working connection to the Teletype MCP server and a Teletype project with Public API access. The skill itself does not authenticate or install a server.

The hosted endpoint is `https://mcp.teletype.app/mcp` with Streamable HTTP transport. Supply the project's Public API token in `X-Teletype-Api-Token` through your client's private settings or secret storage. Do not ask the user to paste the token into a chat, skill file, public repository, or installation link.

Use the [client setup guide](https://github.com/Teletype-App/teletype-mcp-server/blob/main/docs/CLIENTS.md) or its [Russian version](https://github.com/Teletype-App/teletype-mcp-server/blob/main/docs/ru/CLIENTS.md). They include Cursor, Claude Code, Codex, Gemini CLI, and OpenClaw configurations.

For OpenClaw, add the server under `mcp.servers` in private `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "teletype": {
        "url": "https://mcp.teletype.app/mcp",
        "transport": "streamable-http",
        "headers": {
          "X-Teletype-Api-Token": "${TELETYPE_API_TOKEN}"
        }
      }
    }
  }
}
```

Set `TELETYPE_API_TOKEN` in the Gateway process environment. Preserve existing config entries. Run `openclaw mcp doctor teletype --probe` to verify the connection. Tool names may include a client-specific server prefix.

If remote HTTP is unavailable, configure a local stdio server with command `npx`, arguments `["-y", "teletype-mcp-server", "--stdio"]`, and `TELETYPE_API_TOKEN` in its environment. This requires Node.js 20.19+, 22.13+, or 24.x.

After connection, call `get_capabilities` and verify the project identity and access restrictions before processing the inbox.

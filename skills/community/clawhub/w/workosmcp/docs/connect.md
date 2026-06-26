# Connecting

The WorkOS MCP server lives at:

```
https://workos.no/api/mcp
```

- **Transport:** Streamable HTTP (JSON-RPC 2.0). Stateless. GET returns 405.
- **Auth:** OAuth 2.1 (Authorization Code + PKCE). Bearer token.
- **Scopes:** `read`, `write`.
- **Discovery:** `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`, advertised via 401 + `WWW-Authenticate`.
- **Token lifetimes:** Access 60 min, refresh 30 days.

## OpenClaw

OpenClaw discovers remote MCP via URL and runs the OAuth flow in the system
browser:

```bash
openclaw mcp add workos --url https://workos.no/api/mcp
```

Or manually in `~/.config/openclaw/config.json`:

```json
{
  "mcp": {
    "workos": {
      "type": "remote",
      "url": "https://workos.no/api/mcp"
    }
  }
}
```

The first call triggers a browser consent dialog and stores tokens in the
client's secure store.

## Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "workos": {
      "url": "https://workos.no/api/mcp"
    }
  }
}
```

## Claude.ai (web)

Settings → Connectors → **Add custom connector** → paste the URL.

## Cursor

Settings → MCP → **Add new MCP server**, or `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "workos": {
      "url": "https://workos.no/api/mcp"
    }
  }
}
```

## Cline (VS Code)

Cline must be told explicitly that the transport is Streamable HTTP — it
defaults to SSE:

```json
{
  "mcpServers": {
    "workos": {
      "type": "streamableHttp",
      "url": "https://workos.no/api/mcp"
    }
  }
}
```

## OpenCode (sst)

`opencode.json` in the project root or `~/.config/opencode/config.json`:

```json
{
  "mcp": {
    "workos": {
      "type": "remote",
      "url": "https://workos.no/api/mcp"
    }
  }
}
```

## Generic MCP client (manual OAuth)

1. POST `/api/oauth/register` with `client_name`, `redirect_uris`, `scope: "read write"` → receive `client_id`.
2. Send the user to `/oauth/authorize?client_id=...&response_type=code&redirect_uri=...&code_challenge=...&code_challenge_method=S256&scope=read+write`.
3. POST `/api/oauth/token` with `grant_type=authorization_code`, `code`, `redirect_uri`, `code_verifier` → receive `access_token` + `refresh_token`.
4. POST `/api/mcp` with `Authorization: Bearer <token>` and a JSON-RPC 2.0 payload.

Refresh: POST `/api/oauth/token` with `grant_type=refresh_token`.

## Troubleshooting

**`405 Method Not Allowed` on GET** — the client is trying SSE. Switch to
Streamable HTTP. For Cline: set `"type": "streamableHttp"`.

**`401 Unauthorized` after an hour** — the access token expired. The client
should refresh automatically. If not, remove the server and re-add it.

**Discovery fails** — the `.well-known` URLs are served by Next.js
(overriding nginx). If you sit behind a proxy that strips them, open them
explicitly or use the metadata URLs directly:
`/api/mcp-metadata/authorization-server` and
`/api/mcp-metadata/protected-resource`.

**Wrong workspace** — the token binds to the account's primary workspace. To
switch: remove the server in the client, log in with the right account in a
browser, and add it again. Or use `list_workspaces` and pass `workspaceId`
on each call where supported.

**OAuth window does not open (headless)** — copy the authorization URL
manually and paste it into a local browser; the redirect URL contains the
`code` you can hand back to the client.

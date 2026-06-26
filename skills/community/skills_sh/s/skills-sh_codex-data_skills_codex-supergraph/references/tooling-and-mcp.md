# Codex Docs Tooling and MCP Setup

Use this when users ask to connect coding assistants to Codex documentation.

## Codex Docs MCP server

MCP URL:

```text
https://docs.codex.io/mcp
```

This MCP server supports documentation search and API guidance. It does not execute Codex API queries directly.

## Cursor

Add to MCP settings:

```json
{
  "mcpServers": {
    "codex-docs": {
      "url": "https://docs.codex.io/mcp"
    }
  }
}
```

## VS Code

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "codex-docs": {
      "type": "http",
      "url": "https://docs.codex.io/mcp"
    }
  }
}
```

## Claude Code

```bash
claude mcp add --transport http codex-docs https://docs.codex.io/mcp
```

## Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "codex-docs": {
      "serverUrl": "https://docs.codex.io/mcp"
    }
  }
}
```

## SDK quick start

```bash
pnpm add @codex-data/sdk
```

```typescript
import { Codex } from "@codex-data/sdk";

const sdk = new Codex(process.env.CODEX_API_KEY!);
```

Use SDK for quick TypeScript integration and built-in subscription handling. Use raw GraphQL for maximum protocol control.

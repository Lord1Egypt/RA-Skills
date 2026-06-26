# ACP Compatibility ... Technical Reference

## Protocols

| Protocol | Full Name | Origin | License | Wire Format |
|----------|-----------|--------|---------|-------------|
| ACP-Client | Agent Client Protocol | Zed Industries | Apache 2.0 | JSON-RPC (stdio) + HTTP/WebSocket |
| ACP-Comm | Agent Communication Protocol | IBM / Linux Foundation | Apache 2.0 | REST/HTTP |
| MCP | Model Context Protocol | Anthropic | MIT | JSON-RPC (stdio) |

## How LDM OS Uses Each

**MCP (current):** All LDM OS tools (bridge, sessions, messages, updates, crystal) are MCP servers. Claude Code, Cursor, and any MCP client can use them. This is the primary interface.

**ACP-Client (available, not configured):** OpenClaw implements ACP-Client via `@agentclientprotocol/sdk`. It enables IDE-to-agent communication (Zed, VS Code). LDM OS could expose services via ACP-Client for IDE integration. The transport-agnostic core design supports adding ACP-Client as another wrapper.

**ACP-Comm (not implemented):** Agent-to-agent REST protocol. LDM OS's file-based message bus and session registry serve the same purpose locally. Cloud relay (Phase 7) may evaluate ACP-Comm as a wire protocol for remote agent-to-agent communication.

## Architecture

```
LDM OS Core (pure functions, zero deps)
  |
  |-- MCP wrapper (current, all tools)
  |-- ACP-Client wrapper (future, IDE integration)
  |-- ACP-Comm wrapper (future, cloud relay)
  |-- HTTP wrapper (future, web/iOS)
```

Same core logic. Different transports. The core doesn't know or care which protocol is calling it.

## License Compatibility

Both ACP protocols are Apache 2.0. LDM OS is MIT + AGPLv3 dual license. Apache 2.0 is compatible with both. No license conflicts.

## Key Files

| File | What |
|------|------|
| `src/bridge/mcp-server.ts` | MCP server (current interface) |
| `lib/sessions.mjs` | Session register (could expose via ACP-Comm) |
| `lib/messages.mjs` | Message bus (could expose via ACP-Comm) |

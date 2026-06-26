# Protocol Compatibility

## Agent Client Protocol (ACP-Client)

The Agent Client Protocol (ACP-Client) is a standardization effort from Zed Industries (Apache 2.0) that enables structured communication between code editors/IDEs and AI coding agents. It uses JSON-RPC over stdio for local agents and HTTP/WebSocket for remote agents.

OpenClaw already implements ACP-Client via the `openclaw acp` CLI command and `@agentclientprotocol/sdk` dependency.

LDM OS bridge features (MCP tools) operate through the Model Context Protocol (MCP), which is separate from and complementary to ACP-Client. MCP connects an LLM to its tools/resources (internal wiring). ACP-Client connects editors to agents (external communication).

### Current Status

- LDM OS uses MCP for all tool access (bridge, sessions, messages, updates)
- ACP-Client is available in OpenClaw but not configured
- No conflicts between MCP and ACP-Client

### Future Compatibility

- LDM OS could expose services via ACP-Client for IDE integration
- The transport-agnostic core design supports adding ACP-Client as another wrapper

## Agent Communication Protocol (ACP-Comm)

The Agent Communication Protocol (ACP-Comm) from IBM / Linux Foundation (Apache 2.0) is a REST/HTTP protocol for agent-to-agent communication. It includes agent discovery, session management, and run lifecycle.

LDM OS does not currently implement ACP-Comm. The file-based message bus and session registry serve the same purpose for local multi-session communication. Cloud relay (Phase 7) may evaluate ACP-Comm as a wire protocol.

## License Compatibility

Both protocols are Apache 2.0, fully compatible with LDM OS's MIT + AGPLv3 dual license.

---

[Technical Reference](./TECHNICAL.md)

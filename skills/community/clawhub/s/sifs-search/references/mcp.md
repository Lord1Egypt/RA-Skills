# SIFS MCP Rules

MCP is optional. Prefer it only when the SIFS MCP tools are visible in the current agent session.

Use MCP tools when available:

- `search`
- `find_related`
- `list_files`
- `get_chunk`
- `index_status`
- `agent_context`

Do not assume MCP is usable just because a config file contains a SIFS server. A live session may need a restart, a client may not expose the namespace, or the server handshake may fail.

Fallback immediately to shell commands:

```bash
sifs search "query" --source <project>
sifs list-files --source <project> --json
sifs get <file_path> <line> --source <project>
```

Check MCP readiness:

```bash
sifs mcp doctor --source <project> --offline --no-cache --json
sifs agent doctor --target codex --artifact mcp --json
```

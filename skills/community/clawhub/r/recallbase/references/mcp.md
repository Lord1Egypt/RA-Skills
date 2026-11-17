# Local MCP

Read this file when local RecallBase MCP tools are already available or the user asks to configure or diagnose MCP.

The local server mirrors the CLI query layer with four tools: `today`, `search`, `open`, and `sources`. Apply the same retrieve-then-synthesize workflow from `SKILL.md`; tool results do not change the answer quality bar.

Configure clients to launch the local stdio server:

```json
{
  "mcpServers": {
    "recallbase": {
      "command": "rb",
      "args": ["mcp"]
    }
  }
}
```

The server uses the MCP `2024-11-05` stdio profile. A tool result with `isError: true` contains a failed RecallBase envelope; inspect its `error.code`, `message`, and optional `hint`.

The website Docs MCP is a separate public documentation service and has no access to local conversation history.

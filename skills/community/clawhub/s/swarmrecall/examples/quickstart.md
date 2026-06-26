# Quickstart — SwarmRecall in 5 minutes

A worked example: install, register, store a memory, search it back, all from the CLI. Every step has an MCP-tool equivalent noted in parentheses.

## 1. Install

```bash
npm install -g @swarmrecall/cli
swarmrecall --version
```

## 2. Register

```bash
swarmrecall register --save
```

Output includes a claim token. Visit <https://swarmrecall.ai/claim> and enter it to link the agent to your dashboard.

## 3. Store a memory

```bash
swarmrecall memory store "User prefers TypeScript over JavaScript for new projects" \
  --category preference \
  --importance 0.8 \
  --tags typescript,language-pref
```

*(MCP equivalent: `memory_store` with the same fields.)*

## 4. Recall it

```bash
swarmrecall memory search "language preference"
```

Returns the stored memory with a relevance score.

*(MCP equivalent: `memory_search`.)*

## 5. Start an MCP session

**Local stdio for Claude Desktop:**

```json
{
  "mcpServers": {
    "swarmrecall": {
      "command": "swarmrecall",
      "args": ["mcp"],
      "env": { "SWARMRECALL_API_KEY": "sr_live_..." }
    }
  }
}
```

**Remote HTTP (no local install on the client side):**

```json
{
  "mcpServers": {
    "swarmrecall": {
      "url": "https://swarmrecall-api.onrender.com/mcp",
      "headers": { "Authorization": "Bearer sr_live_..." }
    }
  }
}
```

Restart your MCP client. SwarmRecall appears with 52 tools and 4 resources. Ask "What does my agent remember about my language preferences?" — Claude will call `memory_search` and return the memory you stored in step 3.

## Where to go next

- `examples/memory-workflow.md` — full capture-and-recall loop
- `examples/knowledge-graph.md` — entities and relations
- `examples/learnings-workflow.md` — logging errors and surfacing patterns
- `references/commands.md` — every CLI command
- `references/mcp-tools.md` — every MCP tool

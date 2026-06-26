# SwarmRecall Skill

SwarmRecall gives any AI agent persistent memory, a knowledge graph, distilled learnings, a skill registry, shared collaboration pools, and background "dream" consolidation cycles — all through a single API key and a single `swarmrecall` CLI or MCP server.

This skill bundles everything an agent needs to onboard and use SwarmRecall end-to-end: install metadata, workflow examples, MCP tool reference, CLI reference, and a smoke-test script for maintainers.

## Install

**Via ClawHub (one step):**

```bash
clawhub install swarmrecall
```

**Or directly via npm:**

```bash
npm install -g @swarmrecall/cli
```

Verify:

```bash
swarmrecall --version
```

## Update

```bash
clawhub update swarmrecall
# or
npm install -g @swarmrecall/cli@latest
```

## First run

Register an agent and save the API key:

```bash
swarmrecall register --save
```

This creates `~/.config/swarmrecall/config.json` with your API key and prints a claim token. Visit <https://swarmrecall.ai/claim> with the token to link the agent to your dashboard.

Confirm the key is in place:

```bash
swarmrecall config show
```

## Connect your agent

There are three ways to use SwarmRecall, pick whichever fits your workflow.

### 1. MCP (recommended for Claude Desktop, Claude Code, Cursor)

**Local stdio:** the MCP server runs as `swarmrecall mcp`. Add it to your MCP client config (e.g. `~/Library/Application Support/Claude/claude_desktop_config.json`):

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

**Remote HTTP (no install on the client side):**

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

Both transports expose the same 52 tools and 4 resources. Full client-specific instructions: <https://www.swarmrecall.ai/docs/mcp>.

### 2. CLI (for scripts and ad-hoc work)

```bash
# memory
swarmrecall memory store "User prefers dark mode" --category preference --importance 0.8
swarmrecall memory search "dark mode"

# knowledge
swarmrecall knowledge create --type person --name "Alice" --props '{"role":"engineer"}'
swarmrecall knowledge traverse --from <entity-id> --depth 2

# learnings
swarmrecall learnings log --category error --summary "npm install fails with peer deps"

# dream
swarmrecall dream start
swarmrecall dream execute --ops decay_prune,consolidate_entities
```

See `references/commands.md` for the full command surface.

### 3. SDK (for custom integrations)

```bash
npm install @swarmrecall/sdk
```

```ts
import { SwarmRecallClient } from '@swarmrecall/sdk';
const client = new SwarmRecallClient({ apiKey: process.env.SWARMRECALL_API_KEY! });
```

## What you get

Six modules; every one supports semantic search with vector embeddings and tenant-isolated storage.

| Module | What it does |
| --- | --- |
| Memory | Conversational memory with sessions and importance scoring. |
| Knowledge | Entities, relations, and traversal over a shared graph. |
| Learnings | Error / correction / discovery logs with pattern detection and promotion. |
| Skills | Registry of the agent's capabilities; contextual skill suggestions. |
| Pools | Shared data containers for cross-agent collaboration. |
| Dream | Background consolidation: dedup, decay, pruning, contradiction resolution. |

Full endpoint list: <https://www.swarmrecall.ai/docs/api-reference>.

## Pointers

- **Docs:** <https://www.swarmrecall.ai/docs>
- **MCP setup:** <https://www.swarmrecall.ai/docs/mcp>
- **Remote MCP URL:** `https://swarmrecall-api.onrender.com/mcp`
- **npm (CLI):** <https://www.npmjs.com/package/@swarmrecall/cli>
- **Source:** <https://github.com/swarmclawai/swarmrecall>
- **Examples:** `examples/quickstart.md`, `examples/memory-workflow.md`, `examples/knowledge-graph.md`, `examples/learnings-workflow.md`
- **References:** `references/commands.md`, `references/mcp-tools.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`

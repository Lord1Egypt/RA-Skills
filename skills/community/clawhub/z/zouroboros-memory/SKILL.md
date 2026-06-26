---
name: zouroboros-memory
description: "Production-grade persistent memory for AI agents. Hybrid SQLite + vector search, decay classes, episodic memory, cognitive profiles, and MCP server."
version: "3.0.0"
compatibility: "OpenClaw, Claude Code, Codex CLI, any Node.js 22+ environment"
metadata:
  author: marlandoj.zo.computer
  openclaw:
    emoji: "🧠"
    requires:
      bins: [node]
    install:
      - id: node-zouroboros-memory
        kind: node
        package: "zouroboros-memory"
        bins: [zouroboros-memory, zouroboros-memory-mcp]
        label: "Install Zouroboros Memory (npm)"
    homepage: https://github.com/AlaricHQ/zouroboros-openclaw
---

## Usage

Install: `npm install zouroboros-memory`

### CLI
```bash
npx zouroboros-memory --help
npx zouroboros-memory init
npx zouroboros-memory store --entity user --key name --value "Alice" --decay permanent
npx zouroboros-memory search "project preferences" --limit 5
npx zouroboros-memory stats
```

### MCP Server
Add to your `.mcp.json`:
```json
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["zouroboros-memory-mcp", "--db-path", "~/.zouroboros/memory.db"]
    }
  }
}
```

### Programmatic API
```typescript
import { init, storeFact, searchFacts, searchFactsHybrid, getStats } from 'zouroboros-memory';
import type { MemoryConfig } from 'zouroboros-memory';

const config: MemoryConfig = {
  enabled: true,
  dbPath: '~/.zouroboros/memory.db',
  vectorEnabled: false,
  ollamaUrl: 'http://localhost:11434',
  ollamaModel: 'nomic-embed-text',
  autoCapture: false,
  captureIntervalMinutes: 30,
  graphBoost: true,
  hydeExpansion: false,
  decayConfig: { permanent: Infinity, long: 365, medium: 90, short: 30 },
};

init(config);

// Store a fact
await storeFact({ entity: 'user', key: 'preference', value: 'dark mode' }, config);

// Keyword search
const results = searchFacts('dark mode', { limit: 5 });

// Hybrid search (RRF fusion of keyword + vector)
const hybridResults = await searchFactsHybrid('user preferences', config, { limit: 10 });
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `memory_store` | Store a fact with optional decay class |
| `memory_search` | Keyword or hybrid search |
| `memory_episodes` | Create/search episodic memories |
| `cognitive_profile` | Get/update entity cognitive profiles |
| `memory_graph` | Query entity relationship graph |
| `memory_procedures` | Query stored workflow procedures |
| `memory_stats` | Database statistics |
| `memory_delete` | Delete a fact by ID |
| `memory_prune` | Remove expired facts |

## Decay Classes

| Class | TTL |
|-------|-----|
| `permanent` | Never expires |
| `long` | 365 days |
| `medium` | 90 days (default) |
| `short` | 30 days |

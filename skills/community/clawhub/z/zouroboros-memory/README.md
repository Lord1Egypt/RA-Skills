# zouroboros-memory

Production-grade persistent memory system for AI agents. Hybrid SQLite + vector search, decay classes, episodic memory, cognitive profiles, and a full MCP server — all in a single Node.js 22+ package.

## Features

- **Hybrid search** — RRF fusion of keyword (exact/LIKE) + vector (Ollama embeddings) search
- **Decay classes** — `permanent`, `long` (365d), `medium` (90d), `short` (30d) TTLs
- **Episodic memory** — Time-indexed event store with entity linking and outcome tracking
- **Graph boost** — Entity co-occurrence graph for context-aware retrieval
- **Cognitive profiles** — Per-entity trait and preference tracking with interaction history
- **Procedure memory** — Versioned workflow storage with success/failure tracking
- **MCP server** — 9 MCP tools over stdio for any AI client
- **LLM reranker** — Optional gpt-4o-mini or Ollama reranking pass
- **HyDE expansion** — Hypothetical Document Expansion for improved semantic recall
- **Zero Bun dependency** — Pure Node.js 22+ with `better-sqlite3`

## Installation

```bash
npm install zouroboros-memory
```

Requires Node.js 22+. The `better-sqlite3` native addon compiles automatically.

## Quick Start

```typescript
import { init, storeFact, searchFacts, shutdown } from 'zouroboros-memory';
import type { MemoryConfig } from 'zouroboros-memory';

const config: MemoryConfig = {
  enabled: true,
  dbPath: `${process.env.HOME}/.zouroboros/memory.db`,
  vectorEnabled: false,          // set true + ollamaUrl for semantic search
  ollamaUrl: 'http://localhost:11434',
  ollamaModel: 'nomic-embed-text',
  autoCapture: false,
  captureIntervalMinutes: 30,
  graphBoost: true,
  hydeExpansion: false,
  decayConfig: { permanent: Infinity, long: 365, medium: 90, short: 30 },
};

// Initialize (creates DB + schema)
init(config);

// Store facts
await storeFact({ entity: 'alice', key: 'role', value: 'lead engineer' }, config);
await storeFact({ entity: 'project-x', value: 'uses TypeScript strict mode', decay: 'long' }, config);

// Keyword search
const results = searchFacts('TypeScript', { limit: 5 });

// Shutdown
shutdown();
```

## MCP Server

Add to `.mcp.json`:

```json
{
  "servers": {
    "memory": {
      "command": "npx",
      "args": ["zouroboros-memory-mcp", "--db-path", "/path/to/memory.db"]
    }
  }
}
```

Environment variables:
- `ZOUROBOROS_MEMORY_DB` — Override default database path
- `OLLAMA_URL` — Enable vector search (e.g. `http://localhost:11434`)
- `OPENAI_API_KEY` — Enable LLM reranker

Runnable starter:
- `https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/memory-openclaw`

## CLI

```bash
# Initialize
npx zouroboros-memory init

# Store a fact
npx zouroboros-memory store --entity user --key preference --value "dark mode" --decay permanent

# Search
npx zouroboros-memory search "dark mode"
npx zouroboros-memory hybrid "what does the user prefer?"

# Stats
npx zouroboros-memory stats

# Prune expired facts
npx zouroboros-memory prune

# Bulk import
npx zouroboros-memory batch-store facts.json
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `init(config)` | Initialize DB + run migrations + ensure profile schema |
| `shutdown()` | Close database connection |
| `getStats(config)` | Get combined DB + episode statistics |

### Facts

| Function | Description |
|----------|-------------|
| `storeFact(input, config)` | Store a fact (async, generates embedding if vectorEnabled) |
| `searchFacts(query, options)` | Keyword/LIKE search |
| `searchFactsVector(query, config, options)` | Pure vector search (requires vectorEnabled) |
| `searchFactsHybrid(query, config, options)` | RRF fusion search |
| `getFact(id)` | Get fact by ID |
| `deleteFact(id)` | Delete fact by ID |
| `cleanupExpiredFacts()` | Remove expired facts, returns count |

### Episodes

| Function | Description |
|----------|-------------|
| `createEpisode(input)` | Create episodic memory |
| `searchEpisodes(query)` | Temporal + outcome filter search |
| `getEntityEpisodes(entity, options)` | Get episodes for an entity |
| `updateEpisodeOutcome(id, outcome)` | Update episode outcome |
| `getEpisodeStats()` | Episode count by outcome |

### Graph

| Function | Description |
|----------|-------------|
| `buildEntityGraph()` | Build entity co-occurrence graph |
| `getRelatedEntities(entity, options)` | BFS traversal with decay scoring |
| `searchFactsGraphBoosted(results, entities, options)` | Graph-boosted RRF fusion |
| `extractQueryEntities(query)` | Extract known entities from query string |

### Cognitive Profiles

| Function | Description |
|----------|-------------|
| `getProfile(entity)` | Get or create profile |
| `updateTraits(entity, traits)` | Merge-update numeric traits |
| `updatePreferences(entity, preferences)` | Merge-update string preferences |
| `recordInteraction(entity, type, success, latencyMs)` | Log an interaction |
| `getProfileSummary(entity)` | Aggregated performance summary |
| `listProfiles()` | List all known entities |

## Decay Classes

| Class | TTL | Use Case |
|-------|-----|----------|
| `permanent` | Never | Names, core facts |
| `long` | 365 days | Project context, preferences |
| `medium` | 90 days (default) | Recent work, decisions |
| `short` | 30 days | Temporary context, session state |

## Part of the Zouroboros Ecosystem

This package is part of the OpenClaw-facing distribution surface at `AlaricHQ/zouroboros-openclaw`. The canonical upstream framework lives at `marlandoj/Zouroboros`.

For the full experience — persistent memory, swarm orchestration, scheduled agents, persona routing, and self-healing infrastructure — get a [Zo Computer](https://zo-computer.cello.so/IgX9SnGpKnR).

## License

MIT — AlaricHQ

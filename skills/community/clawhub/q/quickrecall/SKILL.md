---
name: memory-enhancement-engine
description: Persistent memory engine for AI agents with semantic recall, hotness prioritization, importance weighting, time decay, and auto-compaction. Zero external dependencies. Pure Node.js.
tags:
  - memory
  - persistent
  - semantic-search
  - hotness
  - recall
  - ai-agent
  - nodejs
features:
  - Hotness-prioritized recall
  - Semantic search (bigram + character overlap)
  - Importance weighting (0-2.0)
  - Exponential time decay
  - Auto-compaction and pruning
  - Zero external dependencies
  - Pure Node.js
---

# Memory Enhancement Engine

**记忆增加引擎** — Persistent memory engine with hotness-prioritized semantic recall.

Memories that are recalled more often appear first — not just keyword matches.

## Quick Start

```bash
# Node.js API
const { MemorySystem } = require('./memory-enhancement-engine/memory.js');
const mem = new MemorySystem();

# CLI tool (view / search / compact)
node memory-enhancement-engine/memo.cjs status
node memory-enhancement-engine/memo.cjs query "something to find"
```

## Core Usage

```javascript
const { MemorySystem } = require('./memory-enhancement-engine/memory.js');

// Create engine (stores to MEMORY_STORE.json automatically)
const mem = new MemorySystem({ decayHalfLifeHours: 2 });

// Write a memory
mem.add({
  content: "Paris is the capital of France.",
  importance: 1.5,
  metadata: { tags: ["geography", "fact"] }
});

// Semantic search
const results = mem.query("France capital");
console.log(results);

// Get recent memories
const recent = mem.recent(10);

// Compact old memories (summarize low-importance clusters)
mem.compact(5, 0.3);
```

## API

| Method | Description |
|--------|-------------|
| `add(content, importance, metadata)` | Write a memory |
| `retrieve(query, k)` | Semantic search (returns sorted by score) |
| `getRecent(n)` | Get N most recent memories |
| `remove(predicate)` | Remove memories matching predicate |
| `compact(groupSize, minImportance)` | Compact old memories into summaries |
| `getStatus()` | Get engine stats (count, size, etc.) |

## Scoring Formula

```
score = similarity × 0.5 + recency × 0.3 + hotness × 0.2
```

Where hotness = log(1 + access_count) × exp(-time_delta / 86400)

## Features

- **Hotness-Prioritized Recall** — Frequently accessed memories get boosted scores
- **Semantic Search** — Bigram overlap + character-level similarity
- **Importance Weighting** — 0.0 (trivial) to 2.0 (critical)
- **Time Decay** — Half-life configurable (default 2 hours)
- **Auto-Prune** — Beyond 1000 entries, least important are pruned
- **Auto-Compaction** — Merge low-importance groups into summaries
- **No Server Needed** — Direct Node.js require, stores to local JSON

## Installation

| Method | Command |
|--------|---------|
| Copy | Copy `memory.js` + `memo.cjs` to your project |
| ClawHub | `clawhub install memory-enhancement-engine` |

## File Structure

```
memory-enhancement-engine/
├── SKILL.md
├── memory.js            # Core engine
├── memo.cjs             # CLI tool
├── package.json
├── assets/
│   └── icon.svg
├── references/
│   ├── API_SPEC.md
│   └── USE_GUIDE.md
└── scripts/
    ├── init-memory.mjs  # One-time migration
    └── test-client.js
```

## License

MIT

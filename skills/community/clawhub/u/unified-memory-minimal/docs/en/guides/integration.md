# Integration Guide

> Connect Unified Memory to other systems and applications.

## 📚 Table of Contents

1. [MCP Integration](#-mcp-integration)
2. [REST API](#-rest-api)
3. [JavaScript SDK](#-javascript-sdk)
4. [CLI Integration](#-cli-integration)
5. [WebSocket](#-websocket)
6. [External Connectors](#-external-connectors)

## 🔌 MCP Integration

Model Context Protocol (MCP) integration for AI assistants.

### Configure MCP Server

```json
{
  "mcpServers": {
    "unified-memory": {
      "command": "npx",
      "args": ["-y", "unified-memory", "serve"],
      "env": {
        "UNIFIED_MEMORY_PORT": "3851"
      }
    }
  }
}
```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `memory_search` | Hybrid search memories |
| `memory_store` | Store new memory |
| `memory_list` | List all memories |
| `memory_delete` | Delete memory by ID |
| `memory_stats` | Get memory statistics |
| `memory_health` | Health check |
| `memory_compose` | Compose prompt context |
| `memory_profile` | Get user profile |
| `memory_preference` | Manage preferences |
| `memory_version` | Version control |
| `memory_tier` | Tier management |
| `memory_dedup` | Deduplication |
| `memory_export` | Export memories |
| `memory_pin` | Pin/unpin memories |

### Example: Using with OpenClaw

```javascript
// In your OpenClaw skill or agent
const result = await mcp.call('unified-memory', 'memory_search', {
  query: 'user preferences',
  topK: 5,
  mode: 'hybrid'
});

console.log(result.results);
```

## 🌐 REST API

Start the REST API server:

```bash
unified-memory serve --port 3851
```

### Endpoints

#### Search Memories
```
GET /api/memories/search?q=<query>&mode=<mode>&topK=<n>
```

```bash
curl "http://localhost:3851/api/memories/search?q=quarterly%20reports&mode=hybrid&topK=5"
```

#### List Memories
```
GET /api/memories?limit=<n>&offset=<n>
```

```bash
curl "http://localhost:3851/api/memories?limit=10&offset=0"
```

#### Get Memory
```
GET /api/memories/:id
```

```bash
curl "http://localhost:3851/api/memories/mem_xxx"
```

#### Store Memory
```
POST /api/memories
Content-Type: application/json

{
  "text": "Memory content",
  "category": "fact",
  "importance": 0.8,
  "tags": ["work"]
}
```

```bash
curl -X POST "http://localhost:3851/api/memories" \
  -H "Content-Type: application/json" \
  -d '{"text":"New memory","tags":["test"]}'
```

#### Delete Memory
```
DELETE /api/memories/:id
```

```bash
curl -X DELETE "http://localhost:3851/api/memories/mem_xxx"
```

#### Statistics
```
GET /api/stats
```

```bash
curl "http://localhost:3851/api/stats"
```

#### Health Check
```
GET /api/health
```

```bash
curl "http://localhost:3851/api/health"
```

## 📦 JavaScript SDK

### Installation

```bash
npm install unified-memory
```

### Basic Usage

```javascript
import { 
  addMemory, 
  searchMemories, 
  getAllMemories,
  getMemory,
  deleteMemory 
} from 'unified-memory';

// Store
const id = await addMemory({
  text: "User preference for Python",
  category: "preference",
  importance: 0.9
});

// Search
const results = await searchMemories("Python preference");

// List
const all = await getAllMemories();

// Get
const memory = await getMemory(id);

// Delete
await deleteMemory(id);
```

### Advanced Usage

```javascript
import {
  beginTransaction,
  commitTransaction,
  rollbackTransaction,
  memoryProfile,
  memoryPreference,
  memoryExport
} from 'unified-memory';

// Atomic transaction
const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (e) {
  await rollbackTransaction(tx);
}

// Profile
const profile = await memoryProfile({ scope: "user" });

// Preferences
await memoryPreference({
  action: "set",
  key: "language",
  value: "Python",
  confidence: 0.95
});

// Export
await memoryExport({
  format: "json",
  output: "~/memories.json"
});
```

## 💻 CLI Integration

### Basic Commands

```bash
# Add memory
unified-memory add "Remember to check reports" --tags work,reminder

# Search
unified-memory search "reports"

# List
unified-memory list

# Get specific
unified-memory get <id>

# Delete
unified-memory delete <id>

# Stats
unified-memory stats
```

### Script Integration

```bash
#!/bin/bash
# daily-sync.sh

# Export memories
unified-memory export --format json --output /tmp/memories.json

# Process with external tool
process_memories.py /tmp/memories.json

# Import updated memories
unified-memory import /tmp/processed_memories.json
```

## 🔌 WebSocket

Real-time updates via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:3851/ws');

ws.on('open', () => {
  // Subscribe to events
  ws.send(JSON.stringify({
    action: 'subscribe',
    events: ['memory:stored', 'memory:deleted', 'search:executed']
  }));
});

ws.on('message', (event) => {
  const data = JSON.parse(event);
  console.log('Event:', data.type, data.payload);
});
```

### WebSocket Events

| Event | Payload |
|-------|---------|
| `memory:stored` | New memory object |
| `memory:updated` | Updated memory |
| `memory:deleted` | Memory ID |
| `search:executed` | Query and result count |
| `health:changed` | Health status change |

## 🔗 External Connectors

### Workspace Memory Sync

Sync with OpenClaw Workspace Memory:

```bash
# Manual sync
npm run sync:manual

# Scheduled sync (daily at 2 AM)
npm run sync

# Generate crontab
npm run crontab
```

### Custom Connector

```javascript
// connectors/my-system.js
export const connector = {
  name: 'my-system',
  
  async pull() {
    // Fetch from external system
    const data = await fetch('https://api.example.com/memories');
    return data.map(item => ({
      text: item.content,
      tags: item.labels,
      metadata: { source: 'my-system', externalId: item.id }
    }));
  },
  
  async push(memories) {
    // Push to external system
    for (const memory of memories) {
      await fetch('https://api.example.com/memories', {
        method: 'POST',
        body: JSON.stringify({
          content: memory.text,
          labels: memory.tags
        })
      });
    }
  }
};
```

## 📊 Integration Examples

### Node.js with Express

```javascript
import express from 'express';
import { addMemory, searchMemories } from 'unified-memory';

const app = express();
app.use(express.json());

app.post('/memories', async (req, res) => {
  try {
    const id = await addMemory(req.body);
    res.json({ id, success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/memories/search', async (req, res) => {
  try {
    const results = await searchMemories(req.query.q);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

### Python Integration

```python
import requests

BASE_URL = "http://localhost:3851/api"

# Search
response = requests.get(f"{BASE_URL}/memories/search", params={
    "q": "quarterly reports",
    "mode": "hybrid",
    "topK": 5
})
print(response.json())

# Store
response = requests.post(f"{BASE_URL}/memories", json={
    "text": "Python preference for data work",
    "category": "preference",
    "tags": ["python", "data"]
})
print(response.json())
```

## 📚 Next Steps

- [API Reference](../api/overview.md) - Complete API documentation
- [Plugin Development](./plugins.md) - Build custom plugins
- [Architecture Overview](../architecture/overview.md) - System design
- [Troubleshooting](../reference/troubleshooting.md) - Common issues

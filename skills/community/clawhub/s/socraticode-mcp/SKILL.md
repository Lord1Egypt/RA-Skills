---
name: socraticode-mcp
description: Install and configure SocratiCode MCP server for semantic code search and codebase indexing
metadata:
  openclaw:
    emoji: ""
    homepage: https://github.com/giancarloerra/socraticode
    requires:
      bins: ["docker", "npx", "mcporter"]
      env: []
  claws:
    title: "SocratiCode MCP - Semantic Code Search"
    description: "Install and configure SocratiCode MCP server for OpenClaw. Enable semantic code search, codebase indexing, and dependency graph analysis."
    tags: ["openclaw", "mcp", "socraticode", "code-search", "codebase-indexing", "semantic-search", "qdrant"]
---

# SocratiCode MCP

Install and configure SocratiCode for semantic code search and codebase intelligence on OpenClaw.

## What is SocratiCode?

MCP server providing:
- **Hybrid search** - Semantic + keyword search via RRF
- **Code indexing** - AST-aware chunking at function/class boundaries
- **Dependency graphs** - Import analysis for 18+ languages
- **Live updates** - File watcher keeps index current

## Prerequisites

| Requirement | Purpose |
|-------------|---------|
| Docker running | Qdrant vector database |
| npx (Node.js 18+) | Execute socraticode package |
| mcporter | Manage MCP servers |

## Installation

### Step 1: Install mcporter

```bash
npm install -g mcporter
```

### Step 2: Configure mcporter

Create `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "socraticode": {
      "command": "npx",
      "args": ["-y", "socraticode"]
    }
  }
}
```

Verify:
```bash
mcporter list
```

### Step 3: Start Qdrant

```bash
docker run -d --name socraticode-qdrant \
  -p 16333:6333 -p 16334:6334 \
  qdrant/qdrant:v1.17.0
```

## Per-Project Indexing

To index a specific project (not the config directory), create `mcporter.json` in project root:

```bash
cd /path/to/your-project

echo '{
  "mcpServers": {
    "socraticode": {
      "command": "npx",
      "args": ["-y", "socraticode"]
    }
  }
}' > mcporter.json
```

Then use `--config mcporter.json`:

```bash
# Index
mcporter --config mcporter.json call socraticode.codebase_index

# Check status
mcporter --config mcporter.json call socraticode.codebase_status

# Search
mcporter --config mcporter.json call socraticode.codebase_search query="auth" limit=5
```

## Commands

| Command | Purpose |
|---------|---------|
| `codebase_index` | Start indexing |
| `codebase_status` | Check progress |
| `codebase_search` | Semantic search |
| `codebase_graph_query` | Find imports/dependents |
| `codebase_graph_visualize` | Mermaid diagram |
| `codebase_graph_circular` | Detect cycles |
| `codebase_watch` | Toggle file watcher |
| `codebase_stop` | Stop indexing |

## Troubleshooting

### Indexing Wrong Directory

Use per-project mcporter.json + `--config` flag.

### Qdrant Not Running

```bash
docker start socraticode-qdrant
# Or recreate:
docker run -d --name socraticode-qdrant -p 16333:6333 -p 16334:6334 qdrant/qdrant:v1.17.0
```

### Slow on macOS/Windows

Install native Ollama:
```bash
brew install ollama
ollama serve
```

Or use OpenAI:
```bash
export OPENAI_API_KEY=your-key
export EMBEDDING_PROVIDER=openai
```

## Agent Integration

Add to your AGENTS.md:

```markdown
## Codebase Search (SocratiCode)
- Use `codebase_search` for exploration
- Check `codebase_status` if no results
- Search before reading files
```

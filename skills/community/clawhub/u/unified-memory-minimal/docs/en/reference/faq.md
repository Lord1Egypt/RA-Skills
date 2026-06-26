# Frequently Asked Questions

> Common questions about Unified Memory.

## General

### What is Unified Memory?

Unified Memory is an enterprise-grade memory management system for AI agents that provides:
- Persistent storage for memories across sessions
- Hybrid search (BM25 + Vector + RRF) for accurate retrieval
- Atomic transactions with WAL for data safety
- Plugin system for extensibility

### What version is current?

The current version is **v5.2.0**. Check with:
```bash
unified-memory --version
```

### What license does it use?

MIT License. See [LICENSE](../../LICENSE) file for details.

---

## Installation

### What are the requirements?

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0 (or yarn)
- **Git** (for manual installation)
- **Ollama** (optional, for vector search)

### How do I install?

**Quick install:**
```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**Or via npm:**
```bash
npm install -g unified-memory
```

### Can I use it without Ollama?

Yes, but you'll only have BM25 search. Vector search requires Ollama:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull embedding model
ollama pull nomic-embed-text

# Start Ollama
ollama serve
```

---

## Usage

### How do I store a memory?

**CLI:**
```bash
unified-memory add "Remember to check reports" --tags work,reminder
```

**JavaScript:**
```javascript
const { addMemory } = require('unified-memory');
await addMemory({
  text: "Remember to check reports",
  tags: ["work", "reminder"]
});
```

### How do I search?

**CLI:**
```bash
unified-memory search "quarterly reports"
```

**JavaScript:**
```javascript
const { searchMemories } = require('unified-memory');
const results = await searchMemories("quarterly reports");
```

### What's the difference between search modes?

| Mode | Description | Best For |
|------|-------------|----------|
| `hybrid` | BM25 + Vector + RRF | General use |
| `bm25` | Keyword only | Exact matches |
| `vector` | Semantic only | Conceptual matches |

### How do transactions work?

```javascript
const { beginTransaction, commitTransaction, rollbackTransaction, addMemory } = require('unified-memory');

const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (e) {
  await rollbackTransaction(tx);
}
```

---

## Data

### Where is data stored?

| Data | Location |
|------|----------|
| Memories | `~/.unified-memory/memories.json` |
| Vectors | `~/.unified-memory/vector.lance` |
| Config | `~/.unified-memory/config.json` |
| WAL | `~/.unified-memory/transactions.log` |
| Logs | `~/.unified-memory/logs/` |

### How do I backup data?

```bash
# Export to file
unified-memory export --format json --output ~/backup.json

# Or use the backup directory
ls ~/.unified-memory/backups/
```

### Can I use a different storage location?

Yes, configure in `config.json`:
```json
{
  "storage": {
    "memoryFile": "/custom/path/memories.json"
  }
}
```

---

## Search

### Why doesn't search find my memory?

1. Check if memory exists: `unified-memory list`
2. Rebuild index: `unified-memory rebuild-index`
3. Try simpler terms
4. Check importance score (lower = less likely to appear)

### What is RRF?

Reciprocal Rank Fusion combines results from multiple search algorithms:
- Takes rankings from BM25 and vector search
- Combines them using formula: `RRF = 1/(k + rank)`
- Produces better results than either alone

### How do I improve search accuracy?

1. Use more specific tags
2. Set higher importance scores
3. Add metadata for filtering
4. Use hybrid mode (default)

---

## Performance

### Why is search slow?

Possible causes:
- Large dataset (> 10,000 memories)
- Ollama not running
- Cache disabled
- No vector index

Solutions:
```bash
# Enable caching (default is on)
# Check config: "cache": { "enable": true }

# Restart Ollama
ollama serve

# Rebuild index
unified-memory rebuild-index
```

### How much memory does it use?

With ~1,760 memories:
- ~245 MB RAM
- ~50 MB storage

Scales linearly with memory count.

---

## Plugins

### How do I install a plugin?

```bash
# Copy plugin to plugins directory
cp my-plugin ~/.unified-memory/plugins/

# Enable in config
# "plugins": { "enabled": ["my-plugin"] }

# Restart server
```

### Can I create custom plugins?

Yes! See [Plugin Development Guide](../guides/plugins.md).

### How do plugins work?

Plugins hook into lifecycle events:
- `beforeStore` - Transform before saving
- `afterStore` - React after saving
- `beforeSearch` - Modify search query
- `afterSearch` - Filter results

---

## Troubleshooting

### "Module not found" error

```bash
npm install
```

### Vector store initialization failed

```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### Ollama connection failed

```bash
# Check Ollama is running
ollama serve

# Pull model
ollama pull nomic-embed-text

# Test
curl http://localhost:11434/api/generate -d '{"model":"nomic-embed-text","prompt":"Hi"}'
```

---

## Development

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests: `npm test`
5. Submit PR

See [Contributing Guidelines](../../CONTRIBUTING.md) for details.

### How do I run tests?

```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# Integration tests
npm run test:integration

# Watch mode
npm run test:watch
```

### How do I build for production?

```bash
npm run build
npm run deploy
```

---

## Migration

### How do I migrate from v4 to v5?

v5 is backwards compatible with v4 storage. Simply:
1. Install v5.2.0
2. Existing data is automatically upgraded
3. New features (atomic transactions) are enabled by default

### How do I export/import between systems?

```bash
# Export on old system
unified-memory export --format json --output memories.json

# Transfer file to new system

# Import on new system
unified-memory import --input memories.json
```

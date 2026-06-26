# User Guides

> In-depth guides for using Unified Memory effectively.

## 📋 Guides in This Section

| Guide | Description | Level |
|-------|-------------|-------|
| [Basic Usage](./basic-usage.md) | Core operations: store, search, list, delete | Beginner |
| [Advanced Usage](./advanced-usage.md) | Version control, dedup, export, profiles | Intermediate |
| [Plugin Development](./plugins.md) | Build custom plugins | Advanced |
| [Integration](./integration.md) | Connect to other systems | Intermediate |

## 🎯 Choose Your Path

**New to Unified Memory?**
Start with [Basic Usage](./basic-usage.md) to learn core operations.

**Want to extend functionality?**
Learn about [Plugin Development](./plugins.md) to build custom plugins.

**Need to integrate with existing systems?**
Check the [Integration Guide](./integration.md) for connectors and APIs.

## 📚 Prerequisites

Before reading these guides, you should:
- Complete the [Quick Start Tutorial](../getting-started/quickstart.md)
- Have Unified Memory installed and running
- Understand basic JavaScript/TypeScript (for API guides)

## 🔧 Common Operations

### Store Memories
```javascript
// Basic storage
await addMemory({ text: "Important note", tags: ["work"] });

// With metadata
await addMemory({
  text: "Meeting at 3 PM",
  category: "fact",
  importance: 0.9,
  tags: ["meeting"],
  metadata: { participants: ["Alice", "Bob"] }
});
```

### Search Memories
```javascript
// Simple search
const results = await searchMemories("meeting notes");

// Hybrid search
const results = await searchMemories("project update", {
  mode: "hybrid",
  vectorWeight: 0.7,
  bm25Weight: 0.3
});
```

### Manage Memories
```javascript
// List all
const all = await getAllMemories();

// Get by ID
const memory = await getMemory(memoryId);

// Delete
await deleteMemory(memoryId);
```

## 🚀 Quick Links

- [API Reference](../api/overview.md) - Complete API documentation
- [Architecture](../architecture/overview.md) - System design
- [Configuration](../getting-started/configuration.md) - Configuration options
- [Troubleshooting](../reference/troubleshooting.md) - Common issues

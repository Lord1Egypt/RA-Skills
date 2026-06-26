# Plugin Development Guide

> Build custom plugins to extend Unified Memory functionality.

## 📚 Table of Contents

1. [Plugin Overview](#-plugin-overview)
2. [Creating a Plugin](#-creating-a-plugin)
3. [Lifecycle Hooks](#-lifecycle-hooks)
4. [Plugin Examples](#-plugin-examples)
5. [Plugin API](#-plugin-api)
6. [Plugin Configuration](#-plugin-configuration)
7. [Publishing Plugins](#-publishing-plugins)

## 🔌 Plugin Overview

Plugins extend Unified Memory with custom functionality:

| Plugin Type | Description |
|-------------|-------------|
| **Sync Bridge** | Connect to external memory systems |
| **Processor** | Transform memories before storage |
| **Search Engine** | Add custom search algorithms |
| **Exporter** | Export to external formats |
| **Observer** | Monitor and report system metrics |

## 📁 Plugin Structure

```
~/.unified-memory/plugins/
└── my-plugin/
    ├── index.js          # Main entry point
    ├── package.json      # Package configuration
    └── README.md         # Documentation
```

## ✏️ Creating a Plugin

### Basic Plugin Template

```javascript
// index.js
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  // Lifecycle hooks
  hooks: {
    beforeStore: async (memory) => {
      // Transform memory before storage
      memory.metadata = memory.metadata || {};
      memory.metadata.processedBy = 'my-plugin';
      return memory;
    },
    afterSearch: async (results) => {
      // Post-process search results
      return results.filter(r => r.score > 0.5);
    }
  },

  // Plugin tools (MCP tools exposed by this plugin)
  tools: [
    {
      name: 'my_plugin_tool',
      description: 'Custom tool exposed by my plugin',
      execute: async (params) => {
        return { success: true, data: params };
      }
    }
  ]
};
```

### package.json

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin for Unified Memory",
  "main": "index.js",
  "type": "module",
  "keywords": ["unified-memory", "plugin"],
  "engines": {
    "unified-memory": ">=5.0.0"
  }
}
```

## 🪝 Lifecycle Hooks

### Available Hooks

| Hook | Timing | Purpose |
|------|--------|---------|
| `beforeStore` | Before memory stored | Transform or validate |
| `afterStore` | After memory stored | Trigger side effects |
| `beforeSearch` | Before search executed | Modify query |
| `afterSearch` | After search results | Filter or rerank |
| `beforeDelete` | Before memory deleted | Cleanup related data |
| `afterDelete` | After memory deleted | Notify external systems |
| `onInit` | On plugin load | Initialize resources |
| `onShutdown` | On plugin unload | Cleanup resources |

### Hook Signatures

```javascript
// Before Store Hook
async beforeStore(memory) {
  // memory: the memory object to be stored
  // Return modified memory or throw to reject
  return memory;
}

// After Store Hook
async afterStore(memory, result) {
  // memory: the stored memory
  // result: storage result
}

// Before Search Hook
async beforeSearch(query, options) {
  // query: search query string
  // options: search options
  // Return modified query/options
  return { query, options };
}

// After Search Hook
async afterSearch(results, query) {
  // results: search results array
  // query: original query
  // Return modified results
  return results;
}

// On Init Hook
async onInit(context) {
  // context: plugin context with config, storage, etc.
  // Initialize resources here
}

// On Shutdown Hook
async onShutdown() {
  // Cleanup resources here
}
```

## 💡 Plugin Examples

### Example 1: Tag Normalizer

Automatically normalize and add tags to memories:

```javascript
// tag-normalizer/index.js
export const plugin = {
  name: 'tag-normalizer',
  version: '1.0.0',

  hooks: {
    beforeStore: async (memory) => {
      if (memory.tags) {
        // Normalize tags: lowercase, trim, dedupe
        memory.tags = [...new Set(
          memory.tags.map(t => t.toLowerCase().trim())
        )];
      }
      return memory;
    }
  }
};
```

### Example 2: External Sync Bridge

Sync memories with an external system:

```javascript
// external-sync/index.js
export const plugin = {
  name: 'external-sync',
  version: '1.0.0',

  async onInit(context) {
    this.externalApi = context.config.apiUrl;
    this.apiKey = context.config.apiKey;
  },

  hooks: {
    afterStore: async (memory) => {
      // Sync to external system
      await fetch(`${this.externalApi}/memories`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(memory)
      });
    },

    afterDelete: async (memoryId) => {
      // Remove from external system
      await fetch(`${this.externalApi}/memories/${memoryId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      });
    }
  }
};
```

### Example 3: Search Result Filter

Filter search results based on custom rules:

```javascript
// age-filter/index.js
export const plugin = {
  name: 'age-filter',
  version: '1.0.0',

  hooks: {
    afterSearch: async (results, query) => {
      // Filter out memories older than 90 days
      const cutoff = Date.now() - (90 * 24 * 60 * 60 * 1000);
      return results.filter(result => {
        return new Date(result.created_at).getTime() > cutoff;
      });
    }
  }
};
```

### Example 4: Custom Search Engine

Add a new search algorithm:

```javascript
// fuzzy-search/index.js
export const plugin = {
  name: 'fuzzy-search',
  version: '1.0.0',

  tools: [
    {
      name: 'fuzzy_search',
      description: 'Fuzzy text search with typo tolerance',
      execute: async (params) => {
        const { query, threshold = 0.8 } = params;
        const allMemories = await getAllMemories();
        
        return allMemories.filter(memory => {
          const similarity = calculateFuzzyScore(query, memory.text);
          return similarity >= threshold;
        });
      }
    }
  ]
};
```

## 🔧 Plugin API

### Context Object

The context object passed to `onInit`:

```javascript
{
  config: { /* plugin configuration */ },
  storage: { /* storage interface */ },
  search: { /* search interface */ },
  emit: (event, data) => {}  // Event emitter
}
```

### Storage Interface

```javascript
// Inside a hook
const memory = await context.storage.getMemory(id);
const allMemories = await context.storage.getAllMemories();
await context.storage.addMemory(memory);
await context.storage.updateMemory(id, updates);
await context.storage.deleteMemory(id);
```

### Search Interface

```javascript
// Inside a hook
const results = await context.search.hybridSearch(query, options);
const bm25Results = await context.search.bm25Search(query);
const vectorResults = await context.search.vectorSearch(query);
```

### Event Emitter

```javascript
// Emit events
context.emit('memory:stored', memory);
context.emit('search:executed', { query, results });
context.emit('error', { hook: 'beforeStore', error });
```

## ⚙️ Plugin Configuration

### config.json

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["tag-normalizer", "external-sync"]
  }
}
```

### Plugin-specific Config

```json
{
  "plugins": {
    "external-sync": {
      "apiUrl": "https://api.example.com",
      "apiKey": "your-api-key",
      "syncInterval": 300000
    }
  }
}
```

## 📦 Publishing Plugins

### Directory Structure
```
my-plugin/
├── index.js
├── package.json
├── README.md
└── tests/
    └── index.test.js
```

### package.json Requirements

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "Description of my plugin",
  "main": "index.js",
  "type": "module",
  "keywords": ["unified-memory", "plugin"],
  "engines": {
    "unified-memory": ">=5.0.0"
  },
  "license": "MIT"
}
```

### README Template

```markdown
# Unified Memory - My Plugin

Description of what this plugin does.

## Installation

```bash
npm install unified-memory-my-plugin
```

## Configuration

```json
{
  "plugins": {
    "enabled": ["my-plugin"]
  }
}
```

## Usage

Explain how to use the plugin.

## License

MIT
```

## 🧪 Testing Plugins

```javascript
// tests/index.test.js
import { describe, it, expect } from 'jest';
import { plugin } from '../index.js';

describe('my-plugin', () => {
  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
  });

  it('should transform memory in beforeStore', async () => {
    const memory = { text: 'Test', tags: ['TEST'] };
    const result = await plugin.hooks.beforeStore(memory);
    expect(result.tags).toContain('test');
  });
});
```

## 📚 Next Steps

- [Integration Guide](./integration.md) - Connect to other systems
- [API Reference](../api/overview.md) - Complete API docs
- [Architecture Overview](../architecture/overview.md) - System design

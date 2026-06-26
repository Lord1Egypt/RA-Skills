# Plugin API Reference

> API for building Unified Memory plugins.

## Plugin Structure

```javascript
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  // Lifecycle hooks
  hooks: {
    beforeStore: async (memory) => memory,
    afterStore: async (memory, result) => {},
    beforeSearch: async (query, options) => ({ query, options }),
    afterSearch: async (results, query) => results,
    beforeDelete: async (id) => id,
    afterDelete: async (id) => {},
    onInit: async (context) => {},
    onShutdown: async () => {}
  },

  // Custom tools exposed by this plugin
  tools: []
};
```

## Hooks API

### beforeStore(memory)

Called before a memory is stored. Use to transform or validate.

```javascript
beforeStore: async (memory) => {
  // Transform memory
  memory.text = memory.text.trim();
  
  // Add metadata
  memory.metadata = memory.metadata || {};
  memory.metadata.processedBy = 'my-plugin';
  
  // Validate (throw to reject)
  if (!memory.text) {
    throw new Error('Memory text cannot be empty');
  }
  
  return memory;
}
```

**Parameters:** `memory: Memory`  
**Returns:** `Memory` (modified)

---

### afterStore(memory, result)

Called after a memory is stored. Use for side effects.

```javascript
afterStore: async (memory, result) => {
  // Sync to external system
  await externalApi.syncMemory(memory);
  
  // Emit event
  emit('memory:stored', memory);
  
  // Update derived data
  await updateStats();
}
```

**Parameters:**
- `memory: Memory` - The stored memory
- `result: { success: boolean, id: string }`

**Returns:** `void`

---

### beforeSearch(query, options)

Called before search is executed. Use to modify query.

```javascript
beforeSearch: async (query, options) => {
  // Expand query
  const expanded = await expandQuery(query);
  
  // Add default filters
  options.scope = options.scope || 'USER';
  
  return { query: expanded, options };
}
```

**Parameters:**
- `query: string`
- `options: SearchOptions`

**Returns:** `{ query: string, options: SearchOptions }`

---

### afterSearch(results, query)

Called after search results are ready. Use to filter/rerank.

```javascript
afterSearch: async (results, query) => {
  // Filter by date
  const cutoff = Date.now() - (30 * 24 * 60 * 60 * 1000);
  return results.filter(r => 
    new Date(r.created_at).getTime() > cutoff
  );
  
  // Or rerank with custom logic
  return rerankResults(results, query);
}
```

**Parameters:**
- `results: SearchResult[]`
- `query: string`

**Returns:** `SearchResult[]`

---

### beforeDelete(id)

Called before a memory is deleted.

```javascript
beforeDelete: async (id) => {
  // Log deletion
  console.log('Memory deleted:', id);
  
  return id; // Must return the ID
}
```

**Parameters:** `id: string`  
**Returns:** `string` (ID)

---

### afterDelete(id)

Called after a memory is deleted.

```javascript
afterDelete: async (id) => {
  // Cleanup external references
  await externalApi.deleteMemory(id);
  
  // Emit event
  emit('memory:deleted', { id });
}
```

**Parameters:** `id: string`  
**Returns:** `void`

---

### onInit(context)

Called when plugin is loaded. Use for initialization.

```javascript
onInit: async (context) => {
  // Load configuration
  this.config = context.config;
  
  // Initialize resources
  this.client = new ExternalClient(this.config);
  
  // Connect
  await this.client.connect();
  
  // Register event handlers
  context.on('event', this.handleEvent);
}
```

**Parameters:** `context: PluginContext`  
**Returns:** `void`

---

### onShutdown()

Called when plugin is unloaded. Use for cleanup.

```javascript
onShutdown: async () => {
  // Close connections
  await this.client.disconnect();
  
  // Save state
  await this.saveState();
  
  // Clear timers
  this.timer && clearInterval(this.timer);
}
```

**Returns:** `void`

---

## Plugin Context API

The context object passed to `onInit`:

```javascript
interface PluginContext {
  config: PluginConfig;      // Plugin-specific config
  storage: StorageInterface; // Storage access
  search: SearchInterface;   // Search access
  emit: (event: string, data: any) => void;  // Event emitter
  on: (event: string, handler: Function) => void;  // Event subscription
  getConfig: (key: string) => any;  // Get config value
}
```

### Storage Interface

```javascript
// Get a memory
const memory = await context.storage.getMemory(id);

// Get all memories
const memories = await context.storage.getAllMemories(options);

// Add memory
await context.storage.addMemory(memory);

// Update memory
await context.storage.updateMemory(id, updates);

// Delete memory
await context.storage.deleteMemory(id);
```

### Search Interface

```javascript
// Hybrid search
const results = await context.search.hybridSearch(query, options);

// BM25 only
const results = await context.search.bm25Search(query);

// Vector only
const results = await context.search.vectorSearch(query);

// Custom search
const results = await context.search.search({
  query,
  mode: 'hybrid',
  topK: 10
});
```

### Event Emitter

```javascript
// Emit events
context.emit('memory:stored', memory);
context.emit('memory:deleted', { id });
context.emit('search:executed', { query, count });
context.emit('error', { hook: 'beforeStore', error });

// Subscribe to events
context.on('memory:stored', (memory) => {
  console.log('Memory stored:', memory.id);
});
```

## Tool Interface

Define custom MCP tools in your plugin:

```javascript
export const plugin = {
  name: 'my-plugin',
  
  tools: [
    {
      name: 'my_plugin_tool',
      description: 'Custom tool for my plugin',
      inputSchema: {
        type: 'object',
        properties: {
          param1: { type: 'string', description: 'Parameter 1' }
        },
        required: ['param1']
      },
      execute: async (params) => {
        // Tool logic
        const result = await doSomething(params.param1);
        
        return {
          content: [{ type: 'text', text: JSON.stringify(result) }]
        };
      }
    }
  ]
};
```

## Plugin Configuration

### package.json

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "main": "index.js",
  "type": "module",
  "unifiedMemory": {
    "plugin": true,
    "hooks": ["beforeStore", "afterStore"],
    "configSchema": {
      "apiUrl": { "type": "string" },
      "apiKey": { "type": "string" }
    }
  }
}
```

### config.json integration

```json
{
  "plugins": {
    "my-plugin": {
      "enabled": true,
      "apiUrl": "https://api.example.com",
      "apiKey": "secret-key"
    }
  }
}
```

## Best Practices

### Always return from hooks

```javascript
// Good
beforeStore: async (memory) => {
  return transformMemory(memory);
}

// Bad - returns undefined
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
}
```

### Handle errors gracefully

```javascript
beforeStore: async (memory) => {
  try {
    return await validateAndTransform(memory);
  } catch (error) {
    console.error('Plugin error:', error);
    return memory; // Return original on error
  }
}
```

### Clean up resources

```javascript
onShutdown: async () => {
  // Clear all timers
  this.timers.forEach(clearTimeout);
  
  // Close connections
  await this.db.close();
  
  // Remove event listeners
  this.handler && this.removeListener('event', this.handler);
}
```

## Testing Plugins

```javascript
import { describe, it, expect } from 'jest';

describe('my-plugin', () => {
  const { plugin } = require('./index.js');

  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
    expect(plugin.hooks).toBeDefined();
  });

  it('should transform memory in beforeStore', async () => {
    const memory = { text: '  Test  ', tags: ['TEST'] };
    const result = await plugin.hooks.beforeStore(memory);
    expect(result.text).toBe('Test');
    expect(result.tags).toContain('test');
  });

  it('should filter results in afterSearch', async () => {
    const results = [
      { id: '1', score: 0.9 },
      { id: '2', score: 0.5 }
    ];
    const filtered = await plugin.hooks.afterSearch(results, 'query');
    expect(filtered.length).toBe(1);
    expect(filtered[0].id).toBe('1');
  });
});
```

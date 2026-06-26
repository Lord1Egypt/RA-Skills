# 插件 API 参考

> 用于构建 Unified Memory 插件的 API。

## 插件结构

```javascript
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  hooks: {
    beforeStore: async (memory) => memory,
    afterStore: async (memory, result) => {},
    beforeSearch: async (query, options) => ({ query, options }),
    afterSearch: async (results, query) => results,
    onInit: async (context) => {},
    onShutdown: async () => {}
  },

  tools: []
};
```

## 钩子 API

### beforeStore(memory)

在记忆存储之前调用。用于转换或验证。

```javascript
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
  memory.metadata = memory.metadata || {};
  memory.metadata.processedBy = 'my-plugin';
  return memory;
}
```

---

### afterStore(memory, result)

在记忆存储之后调用。用于副作用。

```javascript
afterStore: async (memory, result) => {
  await externalApi.syncMemory(memory);
  emit('memory:stored', memory);
}
```

---

### beforeSearch(query, options)

在搜索执行之前调用。用于修改查询。

```javascript
beforeSearch: async (query, options) => {
  const expanded = await expandQuery(query);
  options.scope = options.scope || 'USER';
  return { query: expanded, options };
}
```

---

### afterSearch(results, query)

在搜索结果准备好之后调用。用于过滤/重新排名。

```javascript
afterSearch: async (results, query) => {
  return results.filter(r => r.score > 0.5);
}
```

---

### onInit(context)

在插件加载时调用。用于初始化。

```javascript
onInit: async (context) => {
  this.config = context.config;
  this.client = new ExternalClient(this.config);
  await this.client.connect();
}
```

---

### onShutdown()

在插件卸载时调用。用于清理。

```javascript
onShutdown: async () => {
  await this.client.disconnect();
}
```

## 插件上下文 API

```javascript
interface PluginContext {
  config: PluginConfig;      // 插件特定配置
  storage: StorageInterface; // 存储访问
  search: SearchInterface;   // 搜索访问
  emit: (event: string, data: any) => void;  // 事件发射器
}
```

### 存储接口

```javascript
const memory = await context.storage.getMemory(id);
const memories = await context.storage.getAllMemories(options);
await context.storage.addMemory(memory);
await context.storage.updateMemory(id, updates);
await context.storage.deleteMemory(id);
```

### 搜索接口

```javascript
const results = await context.search.hybridSearch(query, options);
const results = await context.search.bm25Search(query);
const results = await context.search.vectorSearch(query);
```

## 最佳实践

### 总是从钩子返回

```javascript
// 好
beforeStore: async (memory) => {
  return transformMemory(memory);
}

// 坏 - 返回 undefined
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
}
```

### 优雅处理错误

```javascript
beforeStore: async (memory) => {
  try {
    return await validateAndTransform(memory);
  } catch (error) {
    console.error('Plugin error:', error);
    return memory;
  }
}
```

## 测试插件

```javascript
describe('my-plugin', () => {
  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
  });
});
```

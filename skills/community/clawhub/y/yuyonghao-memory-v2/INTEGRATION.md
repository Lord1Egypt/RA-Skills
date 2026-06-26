# Memory V2 集成指南

**版本**: 0.1.0  
**目标**: 将 memory-v2 集成到 OpenClaw 主系统

---

## 快速集成

### 1. 安装依赖

```bash
cd skills/memory-v2
npm install
```

### 2. 在 OpenClaw 中使用

```javascript
// 在 OpenClaw 代码中导入
import MemorySystem from './skills/memory-v2/src/memory-system.js';

// 创建实例
const memory = new MemorySystem({
  dbPath: './vector-db',
  embedModel: 'Xenova/bge-large-zh-v1.5',
  nerModel: 'Xenova/bert-base-chinese-ner'
});

// 初始化
await memory.initialize();

// 添加记忆
await memory.addMemory({
  id: 'conversation_001',
  content: '用户说：明天下午 3 点有个会议',
  metadata: {
    type: 'conversation',
    importance: 0.8,
    createdAt: new Date().toISOString()
  }
});

// 语义搜索
const results = await memory.search('会议时间', 5);
console.log(results);
```

---

## 与现有系统集成

### 替换 elite-longterm-memory

```javascript
// 旧代码
import { saveMemory, searchMemory } from './skills/elite-longterm-memory';

// 新代码
import MemorySystem from './skills/memory-v2/src/memory-system.js';
const memory = new MemorySystem({...});
await memory.initialize();

// 迁移数据
const oldMemories = await loadOldMemories();
for (const mem of oldMemories) {
  await memory.addMemory({
    id: mem.id,
    content: mem.content,
    metadata: mem.metadata
  });
}
```

### 与 Ontology 集成

```javascript
// Memory V2 自动使用现有的 ontology 图谱
const memory = new MemorySystem({
  graphPath: './memory/ontology'  // 使用现有图谱
});

// 添加记忆时会自动提取实体并链接到图谱
const result = await memory.addMemory({
  content: '张三住在上海，他是阿里巴巴的员工'
});

// result.entities 包含提取的实体和链接的图谱节点
```

---

## 配置选项

### 完整配置

```javascript
const memory = new MemorySystem({
  // 向量存储
  dbPath: './vector-db',
  embedModel: 'Xenova/bge-large-zh-v1.5',
  cacheSize: 1000,
  
  // 知识图谱
  graphPath: './memory/ontology',
  
  // NER
  nerModel: 'Xenova/bert-base-chinese-ner',
  
  // 记忆管理
  forgetThreshold: 0.2,  // 遗忘阈值
  
  // LLM（用于摘要，可选）
  llm: {
    async generate(prompt) {
      // 调用 OpenClaw 的 LLM
      return { text: '摘要内容' };
    }
  }
});
```

---

## API 参考

### MemorySystem

#### addMemory(memory)
添加记忆并自动提取实体

```javascript
const result = await memory.addMemory({
  id: 'unique_id',           // 可选，自动生成
  content: '记忆内容',       // 必需
  metadata: {               // 可选
    type: 'conversation',
    importance: 0.8,
    createdAt: '2026-03-26T10:00:00Z'
  }
});

// 返回
{
  memory: { id, content, metadata },
  entities: [
    { text: '张三', type: 'PERSON', linkedId: 'entity_xxx', isNew: true }
  ]
}
```

#### search(query, topK)
语义搜索记忆

```javascript
const results = await memory.search('会议时间', 10);

// 返回
[
  {
    id: 'mem_001',
    content: '明天下午 3 点有个会议',
    metadata: {...},
    score: 0.92,
    relatedEntities: [...]  // 关联实体
  }
]
```

#### getMemory(id)
获取记忆详情

```javascript
const memory = await memory.getMemory('mem_001');
```

#### deleteMemory(id)
删除记忆

```javascript
await memory.deleteMemory('mem_001');
```

#### runMaintenance()
运行记忆管理（遗忘、压缩）

```javascript
const stats = await memory.runMaintenance();
// { totalMemories: 100, compressed: 10, archived: 5 }
```

#### getStats()
获取系统统计

```javascript
const stats = await memory.getStats();
// {
//   vector: { totalMemories: 100, cacheSize: 50 },
//   graph: { nodeCount: 200, edgeCount: 150 },
//   memory: { total: 100, avgScore: 0.75, lowPriorityCount: 10 }
// }
```

---

## 使用场景

### 场景 1: 对话记忆

```javascript
// 保存对话
await memory.addMemory({
  id: `conv_${Date.now()}`,
  content: `用户：${userMessage}\n助手：${assistantResponse}`,
  metadata: {
    type: 'conversation',
    importance: 0.6
  }
});

// 搜索相关历史
const history = await memory.search(userMessage, 3);
```

### 场景 2: 知识提取

```javascript
// 保存文档
await memory.addMemory({
  content: documentText,
  metadata: {
    type: 'document',
    source: 'file.pdf',
    importance: 0.9
  }
});

// 自动提取的实体在图谱中
const entities = await memory.graphStore.searchNodes({ type: 'PERSON' });
```

### 场景 3: 定期维护

```javascript
// 每天运行一次
setInterval(async () => {
  const stats = await memory.runMaintenance();
  console.log(`Compressed ${stats.compressed} memories`);
}, 24 * 60 * 60 * 1000);
```

---

## 性能优化

### 1. 嵌入缓存

```javascript
const memory = new MemorySystem({
  cacheSize: 1000  // 缓存 1000 个嵌入
});
```

### 2. 批量操作

```javascript
// 批量添加（比逐个添加快 10 倍）
await memory.vectorStore.addMemories([
  { id: '1', content: '...' },
  { id: '2', content: '...' },
  { id: '3', content: '...' }
]);
```

### 3. 延迟加载

```javascript
// 模型按需加载
const memory = new MemorySystem({...});
// 第一次调用时才加载模型
await memory.initialize();
```

---

## 故障排除

### 问题 1: 模型下载失败

**解决**: 检查网络连接，或使用离线模型

```javascript
const memory = new MemorySystem({
  embedModel: 'Xenova/all-MiniLM-L6-v2'  // 更小的模型
});
```

### 问题 2: 内存不足

**解决**: 限制缓存大小

```javascript
const memory = new MemorySystem({
  cacheSize: 500  // 减少缓存
});
```

### 问题 3: 搜索速度慢

**解决**: 使用索引或限制返回数量

```javascript
const results = await memory.search(query, 5);  // 只返回 Top-5
```

---

## 下一步

1. ✅ 核心功能完成
2. ✅ 测试验证
3. ⏳ 集成到 OpenClaw 主系统
4. ⏳ 迁移现有数据
5. ⏳ 性能优化

---

*文档版本: 0.1.0*  
*最后更新: 2026-03-26*

# 快速开始

> 5 分钟内启动并运行 Unified Memory

## 安装

```bash
npm install unified-memory
```

## 基本用法

```javascript
import { getEnhancedMemorySystem } from 'unified-memory';

const memory = await getEnhancedMemorySystem();

// 添加记忆
const memory = await memory.addMemory({
  text: '记得和设计团队的会议',
  category: '工作',
  importance: 0.8,
  tags: ['会议', '设计']
});

// 搜索记忆
const results = await memory.search('设计团队 会议');

// 获取所有记忆
const allMemories = await memory.getAllMemories();
```

## 配置

创建 `.env` 文件：

```bash
OLLAMA_URL=http://localhost:11434
MEMORY_FILE=./memory/memories.json
VECTOR_DB=lancedb
```

## 下一步

- [API 参考](../api/README.md) - 完整的 API 文档
- [架构设计](../architecture/README.md) - 系统设计

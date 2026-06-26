# 集成指南

> 将 Unified Memory 连接到其他系统和应用程序。

## 🔌 MCP 集成

MCP（模型上下文协议）集成用于 AI 助手。

### MCP 工具

| 工具 | 描述 |
|------|------|
| `memory_search` | 混合搜索记忆 |
| `memory_store` | 存储新记忆 |
| `memory_list` | 列出所有记忆 |
| `memory_delete` | 按 ID 删除记忆 |
| `memory_stats` | 获取记忆统计 |
| `memory_health` | 健康检查 |

### MCP 配置

```json
{
  "mcpServers": {
    "unified-memory": {
      "command": "npx",
      "args": ["-y", "unified-memory", "serve"]
    }
  }
}
```

## 🌐 REST API

启动 REST API 服务器：

```bash
unified-memory serve --port 3851
```

### 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/memories/search` | 搜索记忆 |
| GET | `/api/memories` | 列出记忆 |
| GET | `/api/memories/:id` | 获取单个记忆 |
| POST | `/api/memories` | 存储记忆 |
| DELETE | `/api/memories/:id` | 删除记忆 |

## 📦 JavaScript SDK

```javascript
import { 
  addMemory, 
  searchMemories, 
  getAllMemories 
} from 'unified-memory';

// 存储
const id = await addMemory({
  text: "User preference for Python",
  category: "preference"
});

// 搜索
const results = await searchMemories("Python preference");

// 列出
const all = await getAllMemories();
```

## 💻 CLI 集成

```bash
# 添加记忆
unified-memory add "Remember to check reports" --tags work

# 搜索
unified-memory search "reports"

# 列出
unified-memory list
```

## 📚 下一步

- [API 参考](../api/overview.md) - 完整的 API 文档
- [插件开发](./plugins.md) - 构建自定义插件

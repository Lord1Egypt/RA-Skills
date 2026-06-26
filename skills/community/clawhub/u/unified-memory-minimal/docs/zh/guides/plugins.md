# 插件开发指南

> 构建自定义插件以扩展 Unified Memory 功能。

## 🔌 插件概述

插件使用自定义功能扩展 Unified Memory：

| 插件类型 | 描述 |
|---------|------|
| **同步桥接** | 连接到外部记忆系统 |
| **处理器** | 存储前转换记忆 |
| **搜索引擎** | 添加自定义搜索算法 |
| **导出器** | 导出到外部格式 |

## 📁 插件结构

```
~/.unified-memory/plugins/
└── my-plugin/
    ├── index.js          # 主入口点
    ├── package.json      # 包配置
    └── README.md         # 文档
```

## ✏️ 创建插件

### 基本模板

```javascript
// index.js
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  hooks: {
    beforeStore: async (memory) => {
      memory.metadata = memory.metadata || {};
      memory.metadata.processedBy = 'my-plugin';
      return memory;
    },
    afterSearch: async (results) => {
      return results.filter(r => r.score > 0.5);
    }
  },

  tools: []
};
```

## 🪝 生命周期钩子

| 钩子 | 时机 | 目的 |
|------|------|------|
| `beforeStore` | 存储前 | 转换或验证 |
| `afterStore` | 存储后 | 触发副作用 |
| `beforeSearch` | 搜索前 | 修改查询 |
| `afterSearch` | 搜索后 | 过滤或重新排名 |
| `onInit` | 插件加载时 | 初始化资源 |
| `onShutdown` | 插件卸载时 | 清理资源 |

## 💡 插件示例

### 标签规范化器

```javascript
export const plugin = {
  name: 'tag-normalizer',
  version: '1.0.0',

  hooks: {
    beforeStore: async (memory) => {
      if (memory.tags) {
        memory.tags = [...new Set(
          memory.tags.map(t => t.toLowerCase().trim())
        )];
      }
      return memory;
    }
  }
};
```

### 外部同步桥接

```javascript
export const plugin = {
  name: 'external-sync',
  version: '1.0.0',

  async onInit(context) {
    this.externalApi = context.config.apiUrl;
  },

  hooks: {
    afterStore: async (memory) => {
      await fetch(`${this.externalApi}/memories`, {
        method: 'POST',
        body: JSON.stringify(memory)
      });
    }
  }
};
```

## ⚙️ 插件配置

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["tag-normalizer", "external-sync"],
    "external-sync": {
      "apiUrl": "https://api.example.com"
    }
  }
}
```

## 📚 下一步

- [集成指南](./integration.md) - 连接到其他系统
- [API 参考](../api/overview.md) - 完整的 API 文档

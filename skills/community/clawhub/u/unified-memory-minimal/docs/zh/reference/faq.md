# 常见问题

> 关于 Unified Memory 的常见问题。

## 基础

### 什么是 Unified Memory？

Unified Memory 是一个企业级 AI 代理记忆管理系统，提供：
- 跨会话持久化存储
- 混合搜索（BM25 + 向量 + RRF）以获得准确检索
- 带 WAL 的原子事务以确保数据安全
- 用于扩展性的插件系统

### 当前版本是什么？

当前版本是 **v5.2.0**。

```bash
unified-memory --version
```

---

## 安装

### 要求是什么？

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0
- **Git**（用于手动安装）
- **Ollama**（可选，用于向量搜索）

### 如何安装？

**快速安装：**
```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**或通过 npm：**
```bash
npm install -g unified-memory
```

---

## 使用

### 如何存储记忆？

**CLI：**
```bash
unified-memory add "Remember to check reports" --tags work,reminder
```

**JavaScript：**
```javascript
await addMemory({
  text: "Remember to check reports",
  tags: ["work", "reminder"]
});
```

### 如何搜索？

**CLI：**
```bash
unified-memory search "quarterly reports"
```

**JavaScript：**
```javascript
const results = await searchMemories("quarterly reports");
```

### 搜索模式有什么区别？

| 模式 | 描述 | 适用于 |
|------|------|--------|
| `hybrid` | BM25 + 向量 + RRF | 一般使用 |
| `bm25` | 仅关键词 | 精确匹配 |
| `vector` | 仅语义 | 概念匹配 |

---

## 数据

### 数据存储在哪里？

| 数据 | 位置 |
|------|------|
| 记忆 | `~/.unified-memory/memories.json` |
| 向量 | `~/.unified-memory/vector.lance` |
| 配置 | `~/.unified-memory/config.json` |
| WAL | `~/.unified-memory/transactions.log` |

### 如何备份数据？

```bash
unified-memory export --format json --output ~/backup.json
```

---

## 搜索

### 为什么搜索找不到我的记忆？

1. 检查记忆是否存在：`unified-memory list`
2. 重建索引：`unified-memory rebuild-index`
3. 尝试更简单的术语
4. 检查重要性分数（越低越不可能出现）

### 什么是 RRF？

倒数排名融合（Reciprocal Rank Fusion）组合多个搜索算法的结果：
- 获取 BM25 和向量搜索的排名
- 使用公式组合：`RRF = 1/(k + rank)`
- 产生比单独使用任一方法更好的结果

---

## 性能

### 为什么搜索很慢？

可能原因：
- 大数据集（> 10,000 条记忆）
- Ollama 未运行
- 缓存禁用
- 无向量索引

解决方案：
```bash
# 启用缓存（默认开启）
# 检查配置："cache": { "enable": true }

# 重启 Ollama
ollama serve

# 重建索引
unified-memory rebuild-index
```

### 它使用多少内存？

约 1,760 条记忆时：
- 约 245 MB RAM
- 约 50 MB 存储

随记忆数量线性增长。

---

## 插件

### 如何安装插件？

```bash
# 将插件复制到插件目录
cp my-plugin ~/.unified-memory/plugins/

# 在配置中启用
# "plugins": { "enabled": ["my-plugin"] }

# 重启服务器
```

### 我可以创建自定义插件吗？

可以！请参阅[插件开发指南](../guides/plugins.md)。

---

## 故障排除

### "Module not found" 错误

```bash
npm install
```

### 向量存储初始化失败

```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### Ollama 连接失败

```bash
ollama serve
ollama pull nomic-embed-text
```

---

## 开发

### 我如何贡献？

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 运行测试：`npm test`
5. 提交 PR

### 如何运行测试？

```bash
npm test
npm run test:unit
npm run test:integration
```

### 如何构建生产版本？

```bash
npm run build
npm run deploy
```

---

## 迁移

### 如何从 v4 迁移到 v5？

v5 与 v4 存储向后兼容。简单地：
1. 安装 v5.2.0
2. 现有数据自动升级
3. 新功能（原子事务）默认启用

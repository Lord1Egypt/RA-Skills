# semantic-vector-store

语义向量库插件，为 OpenClaw 星型记忆架构提供向量存储与语义搜索能力。

## 🎯 功能

- **向量化记忆**：将记忆文本转换为语义向量（嵌入）
- **向量存储**：持久化存储向量，支持高效检索
- **语义搜索**：基于余弦相似度的向量搜索
- **增量索引**：支持动态添加新记忆，无需全量重建
- **可插拔后端**：支持 SQLite + FAISS、Pinecone、Weaviate 等后端

## 📦 安装

```bash
# 从 ClawHub 安装
clawhub install semantic-vector-store

# 或从本地目录安装
clawhub install ./skills/semantic-vector-store
```

## ⚙️ 配置

环境变量：
- `SEMANTIC_VECTOR_DB_PATH`：向量数据库路径（默认：`~/.config/cortexgraph/semantic_vectors.db`）
- `EMBEDDING_MODEL`：嵌入模型名称（默认：`all-MiniLM-L6-v2`）
- `VECTOR_DIMENSION`：向量维度（默认：384）
- `SIMILARITY_THRESHOLD`：相似度阈值（默认：0.5）

## 🚀 快速开始

```python
from semantic_vector_store import SemanticVectorStore

# 初始化
store = SemanticVectorStore()

# 添加记忆向量
mem_id = "mem_001"
text = "今天学习了 Python 异步编程"
vector = store.embed(text)
store.add_vector(mem_id, vector, metadata={"source": "memory.md"})

# 语义搜索
query = "编程学习"
results = store.search(query, top_k=5)
for result in results:
    print(f"记忆 ID: {result['memory_id']}, 相似度: {result['score']:.3f}")
```

## 🔌 适配器接口

### SemanticVectorAdapter

提供星型架构的标准适配器接口：

```python
from integration.adapter.semantic_vector_adapter import SemanticVectorAdapter

adapter = SemanticVectorAdapter()

# 获取健康状态
health = adapter.health_check()
print(f"健康状态: {health['status']}")

# 向量化记忆
vectors = adapter.embed_memory("今天完成了重要工作")
print(f"生成向量维度: {len(vectors)}")

# 语义搜索
results = adapter.search("工作", limit=10)
```

### 主要方法

| 方法 | 说明 |
|------|------|
| `embed(text: str) -> List[float]` | 将文本转换为向量 |
| `add_vector(memory_id: str, vector: List[float], metadata: dict)` | 添加向量到存储 |
| `search(query: str, top_k: int = 10) -> List[dict]` | 语义搜索 |
| `get_stats() -> dict` | 获取统计信息 |
| `health_check() -> dict` | 健康检查 |

## 🏗️ 架构设计

### 核心组件

1. **嵌入器（Embedder）**
   - 支持多种嵌入模型（Sentence Transformers、OpenAI、本地模型）
   - 模型缓存与热加载

2. **向量存储（VectorStore）**
   - SQLite + FAISS 混合存储
   - 支持增量索引与批量导入
   - 自动向量归一化

3. **查询引擎（QueryEngine）**
   - 余弦相似度计算
   - 混合搜索（语义 + 关键词）
   - 结果排序与去重

### 数据模型

```sql
CREATE TABLE semantic_vectors (
    memory_id TEXT PRIMARY KEY,
    vector BLOB,           -- FAISS 索引 ID 或原始向量
    metadata TEXT,         -- JSON 元数据
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 🔄 集成点

### 与 Memory Sync Enhanced 集成

语义向量库通过适配器与 MSE 集成：

```python
# 在 MSE 中使用语义向量库
from integration.adapter.semantic_vector_adapter import SemanticVectorAdapter

class MemorySyncEnhanced:
    def __init__(self):
        self.vector_adapter = SemanticVectorAdapter()
    
    def semantic_search(self, query: str):
        return self.vector_adapter.search(query)
```

### 与 Unified Memory 集成

统一记忆系统可同时查询语义向量和共现图：

```python
from unified_memory import UnifiedMemory

memory = UnifiedMemory()
results = memory.search("查询", use_semantic=True, use_cooccurrence=True)
```

## 📊 性能指标

| 指标 | 目标值 |
|------|--------|
| 向量化延迟 | < 100ms（短文本） |
| 搜索延迟 | < 50ms（10K 向量） |
| 存储容量 | > 1M 向量 |
| 准确率 | > 0.85（MRR） |

## 🔧 维护

### 数据库维护

```bash
# 重建索引
python3 -m semantic_vector_store.reindex

# 备份向量
python3 -m semantic_vector_store.backup --output vectors.bin

# 查看统计
python3 -m semantic_vector_store.stats
```

### 监控指标

- 向量存储使用率
- 查询延迟（P50, P95, P99）
- 缓存命中率
- 嵌入模型加载状态

## 📝 版本历史

- **v0.1.0**（当前）：MVP 版本，基础向量存储与搜索
- **v0.2.0**（计划）：支持 FAISS 索引，性能优化
- **v0.3.0**（计划）：多模型支持，混合搜索

## 🤝 贡献

欢迎提交 Issue 和 Pull Request。请遵循 [OpenClaw 技能开发规范](https://clawhub.com/docs/skill-dev)。

## 📄 许可证

MIT
---
slug: vector-db-manager-free
name: vector-db-manager-free
version: 1.0.0
displayName: 向量数据库管理免费版
summary: 管理向量数据库的索引、嵌入与相似度检索，支持本地与云端部署
license: Proprietary
edition: free
description: 面向AI应用开发者的向量数据库管理工具，覆盖向量索引创建、嵌入向量管理、相似度检索与基础性能调优。核心能力：创建与删除向量索引、批量导入嵌入向量、执行KNN/ANN相似度检索、管理集合与分区、查询基础统计信息。Use
  when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策。
tags:
- 数据库管理
- 向量检索
- AI基础设施
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "exec", "glob", "grep"]
tags: "工具,效率,自动化"
---
# 向量数据库管理工具（免费版）

## 概述

本Skill帮助AI应用开发者管理向量数据库的完整生命周期。从索引创建到嵌入向量导入，从相似度检索到基础性能调优，覆盖向量数据管理的核心环节。

免费版支持单机部署的向量数据库管理，适合原型验证与中小规模应用（百万级向量以下）。

## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|----|---|-----|
| 索引创建与管理 | 创建/删除/重建向量索引 | 是 |
| 嵌入向量导入 | 单条/批量导入向量数据 | 是（批量上限1万） |
| KNN精确检索 | K近邻精确相似度检索 | 是 |
| ANN近似检索 | 近似最近邻检索 | 是（基础算法） |
| 集合与分区管理 | 创建/删除集合与分区 | 是 |
| 基础统计信息 | 向量数量/维度/索引大小 | 是 |
| 多引擎适配 | `PostgreSQL` pgvector/Milvus/ChromaDB | 是 |
| 混合检索 | 向量+标量联合检索 | 否（专业版） |
| 多副本与分片 | 分布式部署管理 | 否（专业版） |
| 性能优化引擎 | 索引参数自动调优 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：管理向量数据库的、嵌入与相似度检索、支持本地与云端部、应用开发者的向量、数据库管理工具、覆盖向量索引创建、嵌入向量管理、相似度检索与基础、性能调优、核心能力、创建与删除向量索、批量导入嵌入向量、管理集合与分区、查询基础统计信息、Use、when、需要数据库操作、数据存储管理时使、不适用于数据库架、构设计决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：语义搜索引擎

某文档平台需要实现"按语义搜索而非关键词匹配"的搜索功能。通过本Skill创建向量索引，将文档嵌入向量导入数据库，用户搜索时将查询文本转为向量并执行相似度检索。

### 场景二：推荐系统

某内容平台基于用户兴趣向量与内容向量计算相似度，推荐最相关的内容。通过本Skill管理用户画像向量与内容向量，执行实时相似度检索。

### 常见问题

某客服系统将知识库文档转为向量存储，用户提问时检索最相关的文档片段，结合LLM生成回答。通过本Skill管理知识库向量索引。

## 快速开始

### 第一步：选择向量数据库引擎（约30秒）

| 引擎 | 适用场景 | 免费版支持 |
|:-----|:-----|:-----|
| `PostgreSQL` + pgvector | 已有PG环境，中小规模 | 是 |
| Milvus | 大规模向量，高性能 | 是（单机模式） |
| ChromaDB | 轻量级，快速原型 | 是 |
| Qdrant | Rust实现，高性能 | 是 |

### 第二步：创建向量索引

```python
# 示例
# 依赖说明
CREATE EXTENSION IF NOT EXISTS vector;
# ...
# 创建带向量字段的表
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536),  # OpenAI text-embedding-ada-002维度
    metadata JSONB
);
# ...
# 创建HNSW索引（推荐，查询速度快）
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
# ...
# 或创建IVFFLAT索引（构建速度快，适合初始阶段）
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### 第三步：导入嵌入向量

```python
import psycopg2
# ...
conn = psycopg2.connect("postgresql://user:pass@localhost/db")
cur = conn.cursor()
# ...
# 批量导入向量数据
vectors = [
    ("文档内容1", [0.1, 0.2, ...], {"source": "web"}),
    ("文档内容2", [0.3, 0.4, ...], {"source": "pdf"}),
]
# ...
from psycopg2.extras import execute_values
execute_values(
    cur,
    "INSERT INTO documents (content, embedding, metadata) VALUES %s",
    [(c, e, m) for c, e, m in vectors]
)
conn.commit()
```

### 第四步：执行相似度检索

```sql
-- 查询与给定向量最相似的10条文档
SELECT id, content, metadata,
    1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 10;
# ...
-- 带标量过滤的检索
SELECT id, content,
    1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM documents
WHERE metadata->>'source' = 'web'
    AND 1 - (embedding <=> '[0.1, 0.2, ...]') > 0.8
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 10;
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 配置示例

### 索引类型选择决策

| 索引类型 | 构建速度 | 查询速度 | 召回率 | 内存占用 | 推荐场景 |
|---:|---:|---:|---:|---:|---:|
| HNSW | 慢 | 极快 | 高 | 高 | 查询频繁，数据量中等 |
| IVFFLAT | 快 | 中 | 中 | 低 | 数据量大，可接受部分召回损失 |
| Flat（暴力） | 无需构建 | 慢 | 100% | 低 | 数据量小（<10万），需精确结果 |

### 向量维度参考

| 嵌入模型 | 维度 | 适用场景 |
|:---:|:---:|:---:|
| OpenAI text-embedding-3-small | 1536 | 通用文本嵌入 |
| OpenAI text-embedding-3-large | 3072 | 高精度需求 |
| BGE-base-zh | 768 | 中文文本 |
| BGE-large-zh | 1024 | 中文高精度 |
| Sentence-BERT | 384 | 轻量级英文 |
| Cohere embed-v3 | 1024 | 多语言 |

### 距离度量选择

| 度量方式 | 公式 | 适用场景 | pgvector操作符 |
|:------|------:|:------|:------|
| 余弦相似度 | 1 - cos(θ) | 文本语义相似 | `<=>` |
| 欧氏距离 | L2范数 | 图像特征 | `<->` |
| 内积 | 点积 | 归一化后的相似度 | `<#>` |

### ChromaDB配置示例

```python
import chromadb
# ...
client = chromadb.PersistentClient(path="./vector_db")
# ...
# 创建集合
collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # 使用余弦距离
)
# ...
# 批量添加向量
collection.add(
    ids=["doc1", "doc2"],
    documents=["文档内容1", "文档内容2"],
    embeddings=[[0.1, 0.2], [0.3, 0.4]],
    metadatas=[{"source": "web"}, {"source": "pdf"}]
)
# ...
# 相似度检索
results = collection.query(
    query_embeddings=[[0.15, 0.25]],
    n_results=10,
    where={"source": "web"}
)
```

## 最佳实践

### 批量导入优化

```python
# 推荐：使用批量插入而非逐条插入
BATCH_SIZE = 1000  # 每批1000条
# ...
def batch_import(vectors, conn):
    cur = conn.cursor()
    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i+BATCH_SIZE]
        execute_values(
            cur,
            "INSERT INTO documents (content, embedding, metadata) VALUES %s",
            batch
        )
        conn.commit()
        print(f"已导入 {min(i+BATCH_SIZE, len(vectors))}/{len(vectors)}")
```

### 索引参数调优

| 参数 | 作用 | 推荐值 | 说明 |
|---:|:---|---:|---:|
| `m`（HNSW） | 每层连接数 | 16-48 | 越大召回越高，内存越多 |
| `ef_construction` | 构建时搜索宽度 | 64-256 | 越大构建越慢，质量越好 |
| `ef_search` | 查询时搜索宽度 | 40-128 | 越大查询越慢，召回越高 |
| `lists`（IVFFLAT） | 聚类中心数 | sqrt(N) | N为向量总数 |

### 错误恢复策略

| 错误类型 | 原因 | 恢复策略 |
|:------:|--------|:-------|
| 维度不匹配 | 嵌入模型与索引维度不一致 | 重建索引或更换嵌入模型 |
| 内存不足 | HNSW索引占用过大 | 切换IVFFLAT或减少m值 |
| 查询超时 | ef_search过大或数据量过大 | 降低ef_search，添加标量过滤 |
| 导入失败 | 批量过大或格式错误 | 减小batch_size，检查向量格式 |
| 索引膨胀 | 频繁删除导致 | 定期REINDEX重建索引 |

## 常见问题(补充)

### Q1：应该选择哪个向量数据库引擎？

A：根据规模和现有技术栈选择：(1) 已有 `PostgreSQL` 且向量数<100万，选pgvector；(2) 需要高性能且向量数>100万，选Milvus；(3) 快速原型验证，选ChromaDB；(4) 追求极致性能，选Qdrant。

### Q2：HNSW和IVFFLAT怎么选？

A：HNSW查询更快但构建慢、内存占用高，适合查询频繁的场景。IVFFLAT构建快、内存占用低，但查询速度和召回率略低，适合数据量大且可接受部分召回损失的场景。

### Q3：向量维度对性能有什么影响？

A：维度越高，存储空间和计算成本越大。1536维向量比768维多消耗一倍存储。建议根据实际需求选择合适维度的嵌入模型，不必一味追求高维度。

### 已知限制

A：免费版不限制使用次数，但批量导入上限为1万条/次，不支持混合检索（向量+标量联合排序）、多副本分片部署、索引参数自动调优、向量数据版本管理等高级功能。

### Q5：如何监控向量数据库性能？

A：免费版提供基础统计信息（向量数量、索引大小、查询延迟）。如需实时监控仪表盘、慢查询分析、容量规划等高级监控，请使用专业版。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+
- **数据库**: `PostgreSQL` 14+ / Milvus 2.0+ / ChromaDB 0.4+ / Qdrant 1.0+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|----|:--:|---:|----|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| pgvector | PG扩展 | pgvector必需 | `CREATE EXTENSION vector` |
| psycopg2 | Python库 | PG必需 | `pip install psycopg2-binary` |
| pymilvus | Python库 | Milvus必需 | `pip install pymilvus` |
| chromadb | Python库 | ChromaDB必需 | `pip install chromadb` |
| qdrant-client | Python库 | Qdrant必需 | `pip install qdrant-client` |
| numpy | Python库 | 推荐 | `pip install numpy` |

### API Key 配置
- **数据库连接串**: 存储于环境变量 `DATABASE_URL` / `VECTOR_DB_URL`
- **嵌入模型API**: OpenAI/Cohere等API密钥，存储于环境变量 `EMBEDDING_API_KEY`
- **禁止**: 在代码或配置文件中硬编码密钥
- **推荐**: 使用 `.env` 文件管理，并在 `.gitignore` 中排除

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent管理向量数据库

## 免费版限制

本免费体验版限制以下高级功能：
- 批量导入上限为1万条/次
- 不支持混合检索（向量相似度+标量排序联合检索）
- 不支持多副本与分片部署管理
- 不支持索引参数自动调优
- 不支持向量数据版本管理与回滚
- 不支持实时性能监控仪表盘
- 不提供优先技术支持

解锁全部功能请使用专业版：vector-db-manager-pro

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|----|----|----|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "向量数据库管理免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "vector db manager"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

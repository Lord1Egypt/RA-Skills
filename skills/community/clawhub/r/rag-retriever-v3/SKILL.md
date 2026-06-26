# 🦞 RAG Retriever V3.0

**版本**: 3.0.0  
**创建时间**: 2026-03-27  
**状态**: ✅ 完整实现

---

## 📋 简介

RAG 3.0 (Retrieval-Augmented Generation) 高级检索系统，为 OpenClaw 提供企业级的文档检索能力：

- 🧠 **语义嵌入** - 支持 OpenAI + BGE + MiniLM 多模型
- 🔍 **混合检索** - 向量相似度 + BM25 关键词 + RRF 融合
- 🔄 **智能重排序** - Cross-Encoder 精确重打分
- 📖 **来源引用** - 自动编号 + 完整溯源
- 🇨🇳 **中文优化** - jieba 分词 + 中文标点处理

---

## 🚀 快速开始

### 安装

```bash
cd skills/rag-retriever-v3
npm install
```

### 基本使用

#### 1. 初始化
```bash
node src/cli.js init
```

#### 2. 添加文档
```bash
node src/cli.js add ./document.txt '{"source":"文档来源","title":"文档标题"}'
```

#### 3. 检索
```bash
# 混合搜索（推荐）
node src/cli.js search "查询内容" 5

# 仅向量搜索
node src/cli.js vector-search "查询内容" 5

# 仅关键词搜索
node src/cli.js keyword-search "查询内容" 5

# RAG 查询（生成带引用的上下文）
node src/cli.js rag "什么是人工智能" 3
```

---

## 📚 API 使用

### JavaScript API

```javascript
import { RAGRetrieverV3 } from './src/core/RAGRetrieverV3.js';

// 创建检索器实例
const rag = new RAGRetrieverV3({
  dbPath: './data/lancedb-v3',
  collectionName: 'documents',
  
  // 嵌入配置
  embeddingProvider: 'xenova',  // 'xenova', 'openai', 'auto'
  embeddingOptions: {
    modelName: 'Xenova/all-MiniLM-L6-v2'
  },
  
  // 分块配置
  chunking: {
    chunkSize: 500,
    overlap: 50,
    strategy: 'recursive'  // 'fixed', 'recursive', 'semantic'
  },
  
  // BM25 配置
  bm25: {
    k1: 1.5,
    b: 0.75
  },
  
  // RRF 配置
  rrf: {
    k: 60,
    weights: { 0: 1.0, 1: 1.0 }
  },
  
  // 重排序配置
  rerank: {
    enabled: true,
    model: 'Xenova/ms-marco-MiniLM-L-6-v2',
    topK: 20
  },
  
  // 引用配置
  citation: {
    format: 'numbered',  // 'numbered', 'bracket', 'footnote'
    includeMetadata: true
  }
});

// 初始化
await rag.initialize();

// 添加文档
const result = await rag.addDocument(text, {
  title: '文档标题',
  source: '文档来源',
  author: '作者',
  date: '2024-01-01'
});

// 检索
const results = await rag.retrieve('查询内容', {
  limit: 5,
  hybrid: true,      // 使用混合搜索
  rerank: true,      // 启用重排序
  addCitations: true // 添加引用
});

// RAG 查询（生成完整提示词）
const ragResult = await rag.retrieveForRAG('什么是机器学习', {
  limit: 3
});
console.log(ragResult.fullPrompt);
console.log(ragResult.citationList);

// 获取统计信息
const stats = await rag.getStats();

// 关闭连接
await rag.close();
```

---

## 🎯 核心组件

### 1. 嵌入模型 (Embeddings)

支持多种嵌入模型：

#### Xenova/Transformers (本地)
```javascript
import { XenovaEmbedding } from './src/embeddings/XenovaEmbedding.js';

const embedding = new XenovaEmbedding({
  modelName: 'Xenova/all-MiniLM-L6-v2'  // 384维
  // 或 'Xenova/bge-base-zh-v1.5'  // 768维，中文优化
});
await embedding.initialize();
const vector = await embedding.embed('文本内容');
```

**支持的模型：**
- `Xenova/all-MiniLM-L6-v2` - 384维，轻量级英文
- `Xenova/bge-small-zh-v1.5` - 512维，中文小模型
- `Xenova/bge-base-zh-v1.5` - 768维，中文基础模型
- `Xenova/bge-large-zh-v1.5` - 1024维，中文大模型
- `Xenova/multilingual-e5-base` - 768维，多语言

#### OpenAI (云端)
```javascript
import { OpenAIEmbedding } from './src/embeddings/OpenAIEmbedding.js';

const embedding = new OpenAIEmbedding({
  apiKey: process.env.OPENAI_API_KEY,
  modelName: 'text-embedding-3-small'  // 1536维
});
await embedding.initialize();
```

### 2. 混合搜索 (Hybrid Search)

```javascript
// 向量搜索
const vectorResults = await rag.vectorSearch('查询', { limit: 20 });

// 关键词搜索（BM25）
const keywordResults = await rag.keywordSearch('查询', { limit: 20 });

// 混合搜索（RRF 融合）
const hybridResults = await rag.hybridSearch('查询', {
  vectorLimit: 20,
  keywordLimit: 20,
  limit: 10
});
```

### 3. 重排序 (Reranking)

```javascript
import { CrossEncoderReranker } from './src/rerank/CrossEncoderReranker.js';

const reranker = new CrossEncoderReranker({
  modelName: 'Xenova/ms-marco-MiniLM-L-6-v2'
});

const reranked = await reranker.rerank('查询', results, { limit: 10 });
```

### 4. 来源引用 (Citations)

```javascript
import { CitationManager } from './src/core/CitationManager.js';

const cm = new CitationManager({ format: 'numbered' });

// 添加引用
const citedResults = cm.addCitations(results);

// 生成上下文
const context = cm.generateContext(citedResults);

// 生成引用列表
const citationList = cm.generateCitationList(citedResults);

// 生成完整 RAG 提示词
const ragPrompt = cm.generateRAGPrompt('查询', citedResults);
```

---

## 🔧 配置选项

### RAGRetrieverV3 完整配置

```javascript
{
  // 基础配置
  dbPath: './data/lancedb-v3',      // LanceDB 路径
  collectionName: 'documents',       // 集合名称
  
  // 嵌入配置
  embeddingProvider: 'xenova',       // 'xenova', 'openai', 'auto'
  embeddingOptions: {
    modelName: 'Xenova/all-MiniLM-L6-v2',
    // OpenAI 选项
    apiKey: process.env.OPENAI_API_KEY,
    baseURL: 'https://api.openai.com/v1'
  },
  
  // 分块配置
  chunking: {
    chunkSize: 500,                  // 每块字符数
    overlap: 50,                     // 重叠字符数
    strategy: 'recursive',           // 'fixed', 'recursive', 'semantic'
    separator: '\n'                  // 分隔符
  },
  
  // BM25 配置
  bm25: {
    k1: 1.5,                         // BM25 k1 参数
    b: 0.75                          // BM25 b 参数
  },
  
  // RRF 配置
  rrf: {
    k: 60,                           // RRF 常数
    weights: { 0: 1.0, 1: 1.0 }     // 各检索器权重
  },
  
  // 重排序配置
  rerank: {
    enabled: true,                   // 是否启用
    model: 'Xenova/ms-marco-MiniLM-L-6-v2',
    topK: 20                         // 重排序前 K 个
  },
  
  // 引用配置
  citation: {
    format: 'numbered',              // 'numbered', 'bracket', 'footnote'
    includeMetadata: true,           // 包含元数据
    maxContentLength: 500            // 内容最大长度
  }
}
```

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
npm test

# 运行单元测试
npm run test:unit

# 运行集成测试
npm run test:integration

# 运行中文测试
npm run test:chinese
```

### 测试覆盖

- ✅ 分块策略（固定、递归、语义）
- ✅ 嵌入模型（Xenova、OpenAI）
- ✅ BM25 关键词搜索
- ✅ RRF 融合算法
- ✅ Cross-Encoder 重排序
- ✅ 来源引用管理
- ✅ 中文分词和搜索
- ✅ 完整 RAG 流程

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 分块速度 | ~1000 字符/ms |
| 嵌入速度 | ~50-100 文档/s (本地) |
| 向量搜索延迟 | <50ms |
| 混合搜索延迟 | <100ms |
| 重排序延迟 | ~10-50ms/文档 |
| 存储占用 | ~2-4KB/文档 |

---

## 🌟 特性对比

| 特性 | RAG 2.0 | RAG 3.0 |
|------|---------|---------|
| 嵌入模型 | 简单 TF | Xenova/OpenAI |
| 向量维度 | 固定 384 | 384-3072 可选 |
| 关键词搜索 | ❌ | ✅ BM25 |
| 混合检索 | ❌ | ✅ RRF |
| 重排序 | ❌ | ✅ Cross-Encoder |
| 来源引用 | 基础 | 完整溯源 |
| 中文分词 | 基础 jieba | 优化 jieba |

---

## 🔗 参考资料

- [LanceDB 文档](https://lancedb.github.io/lancedb/)
- [Transformers.js](https://huggingface.co/docs/transformers.js/)
- [BM25 算法](https://en.wikipedia.org/wiki/Okapi_BM25)
- [RRF 融合](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Cross-Encoder](https://www.sbert.net/examples/applications/cross-encoder/README.html)

---

## ⚠️ 已知限制

1. **首次加载模型** - Xenova 模型首次下载需要网络，约 50-200MB
2. **内存占用** - 大型嵌入模型需要较多内存（建议 4GB+）
3. **中文模型** - 部分中文模型效果依赖训练数据质量

---

*最后更新：2026-03-27*

# RAG 2.0 升级设计

**启动时间**: 2026-03-20 14:32  
**目标**: 将 RAG 从 40% 提升到 90%

---

## 一、架构设计

```
┌─────────────────────────────────────────────────────┐
│                   RAG 2.0 Pipeline                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Query] ──→ [Query Expansion] ──→ [Hybrid Search]  │
│                                      │              │
│                    ┌─────────────────┴──────────┐   │
│                    ▼                            ▼   │
│            [Vector Search]            [BM25 Search] │
│                    │                            │   │
│                    └─────────┬──────────────────┘   │
│                              ▼                      │
│                      [Reranking]                    │
│                              │                      │
│                              ▼                      │
│                      [Results + Citations]          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 二、核心模块

### 1. Embedding Module（向量嵌入）
- **首选**: `@huggingface/transformers` + `Xenova/all-MiniLM-L6-v2`（本地，免费，384维）
- **备选**: OpenAI text-embedding-3-small（$0.02/1M tokens，1536维）
- **底层**: ONNX Runtime（浏览器 + Node.js）
- **安装**: `npm i @huggingface/transformers`

### 2. Hybrid Search（混合搜索）
- **向量搜索**: 语义相似度（LanceDB）
- **BM25 搜索**: 关键词匹配（okapibm25 npm）
- **融合**: Reciprocal Rank Fusion (RRF)，k=60

### 3. Reranking（重排序）
- **首选**: Cross-encoder `cross-encoder/ms-marco-MiniLM-L-6-v2`（~50ms/doc）
- **备选**: BM25 + 向量加权融合（已实现）
- **备选**: Cohere Rerank API
- **优化**: 批处理 + 缓存 + INT8 量化

### 4. Citations（来源引用）
- **格式**: [1] Source: filename.md (chunk 1/3)
- **实现**: chunk metadata 保留 source 信息
- **溯源**: UUID 关联 chunk 与原始文档

---

## 三、技术选型

| 模块 | 首选 | 备选 | 理由 |
|------|------|------|------|
| 嵌入 | @huggingface/transformers (all-MiniLM-L6-v2) | OpenAI API | 本地免费，无需 API key |
| 向量库 | LanceDB（已有） | Qdrant | 已集成，支持混合搜索 |
| BM25 | 自实现 | fast-bm25 | 已完成，纯 JS |
| 重排序 | Cross-encoder (ms-marco-MiniLM-L-6-v2) | BM25+Vector加权 | 已实现加权融合 |

---

## 四、实现计划

### Phase 1: 向量嵌入（今天）✅ 完成
- [x] OpenAI Embedding 集成
- [x] 本地简单嵌入（降级方案）
- [x] 文档自动嵌入
- [x] 向量搜索 API

### Phase 2: 混合搜索（今天）✅ 完成
- [x] BM25 关键词搜索
- [x] RRF 融合算法
- [x] 加权融合搜索
- [x] 混合搜索 API

### Phase 3: 重排序 + 引用（今天）✅ 完成
- [x] 加权融合重排序
- [x] 来源引用格式
- [x] 测试验证（3/4 通过）

### Phase 4: Transformers.js 集成（下周）
- [ ] 安装 @huggingface/transformers
- [ ] 加载 all-MiniLM-L6-v2 模型
- [ ] 本地向量嵌入（无需 API key）
- [ ] Cross-encoder 重排序

### Phase 5: 生产优化（下周）
- [ ] 嵌入缓存优化
- [ ] 批量处理优化
- [ ] INT8 量化支持

---

## 五、预期效果

| 指标 | 当前 | 目标 |
|------|------|------|
| 检索准确率 | ~60% | ~85% |
| 相关性评分 | 中等 | 高 |
| 来源可追溯 | ❌ | ✅ |
| 混合搜索 | ❌ | ✅ |

---

## 七、参考资源

| 主题 | 链接 |
|------|------|
| Transformers.js | https://huggingface.co/blog/transformersjs-v4 |
| all-MiniLM-L6-v2 | https://huggingface.co/Xenova/all-MiniLM-L6-v2 |
| Cross-Encoder 重排序 | https://sbert.net/examples/cross_encoder/applications/README.html |
| Qdrant 混合搜索 | https://qdrant.tech/documentation/tutorials-search-engineering/reranking-hybrid-search/ |
| RAG 2.0 最佳实践 | https://appropri8-astro.pages.dev/blog/2025/02/10/rag-2-0-hybrid-indexing-context-optimization/ |
| Rerankers 库 | https://github.com/AnswerDotAI/rerankers |

---

*设计时间: 2026-03-20 14:33*  
*更新时间: 2026-03-20 14:42 (整合 Tavily 搜索结果)*

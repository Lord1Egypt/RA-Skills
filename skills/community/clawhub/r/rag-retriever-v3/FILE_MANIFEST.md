# RAG Retriever V3.0 文件清单

## 项目结构

```
skills/rag-retriever-v3/
├── src/
│   ├── embeddings/          # 嵌入模型模块
│   │   ├── EmbeddingProvider.js      # 嵌入提供者基类
│   │   ├── XenovaEmbedding.js        # Xenova/Transformers 本地嵌入
│   │   ├── OpenAIEmbedding.js        # OpenAI API 嵌入
│   │   └── index.js                  # 嵌入模块入口
│   ├── search/              # 搜索模块
│   │   ├── BM25Search.js             # BM25 关键词搜索
│   │   ├── RRFFusion.js              # RRF 融合算法
│   │   └── index.js                  # 搜索模块入口
│   ├── rerank/              # 重排序模块
│   │   ├── CrossEncoderReranker.js   # Cross-Encoder 重排序
│   │   └── index.js                  # 重排序模块入口
│   ├── core/                # 核心模块
│   │   ├── ChunkingStrategy.js       # 文档分块策略
│   │   ├── CitationManager.js        # 来源引用管理
│   │   ├── RAGRetrieverV3.js         # 主检索器类
│   │   └── index.js                  # 核心模块入口
│   ├── cli.js               # 命令行工具
│   └── index.js             # 主入口/导出
├── test/
│   ├── unit.test.js         # 单元测试 (14 个测试)
│   ├── integration.test.js  # 集成测试 (19 个测试)
│   ├── chinese.test.js      # 中文测试 (11 个测试)
│   └── run-all-tests.js     # 测试运行器
├── data/                    # 数据目录
├── package.json             # 包配置
├── README.md                # 项目说明
├── SKILL.md                 # 详细文档
└── FILE_MANIFEST.md         # 本文件
```

## 核心功能实现

### 1. 语义嵌入 (src/embeddings/)
- ✅ EmbeddingProvider.js - 抽象基类
- ✅ XenovaEmbedding.js - 本地 Transformer 模型 (MiniLM, BGE 等)
- ✅ OpenAIEmbedding.js - OpenAI API 支持
- ✅ index.js - 工厂函数和导出

### 2. 混合检索 (src/search/)
- ✅ BM25Search.js - BM25 关键词搜索，支持中文 jieba 分词
- ✅ RRFFusion.js - RRF (Reciprocal Rank Fusion) 融合算法
- ✅ index.js - 导出

### 3. 重排序 (src/rerank/)
- ✅ CrossEncoderReranker.js - Cross-Encoder 重排序实现
- ✅ index.js - 工厂函数和导出

### 4. 来源引用 (src/core/)
- ✅ CitationManager.js - 自动编号、溯源、RAG 提示词生成
- ✅ ChunkingStrategy.js - 多种分块策略（固定、递归、语义）
- ✅ RAGRetrieverV3.js - 主检索器，整合所有功能
- ✅ index.js - 导出

### 5. CLI 工具 (src/)
- ✅ cli.js - 完整命令行接口
- ✅ index.js - 模块导出

## 测试覆盖

### 单元测试 (test/unit.test.js) - 14 个测试
1. 固定大小分块
2. 递归分块
3. 语义分块
4. 分块元数据
5. 分块统计
6. 添加引用
7. 生成上下文
8. 生成引用列表
9. 验证引用完整性
10. 去重引用
11. RRF 融合两个列表
12. RRF 单列表返回
13. RRF 空列表处理
14. RRF 权重融合
15. BM25 添加文档
16. BM25 搜索
17. BM25 中文分词
18. BM25 统计信息

### 集成测试 (test/integration.test.js) - 19 个测试
1. Xenova 嵌入模型加载
2. Xenova 生成嵌入
3. Xenova 批量嵌入
4. Xenova 中文嵌入
5. CrossEncoder 模型加载
6. CrossEncoder 评分
7. CrossEncoder 批量重排序
8. RRF 融合多列表
9. RRF 带权重融合
10. 生成完整 RAG 提示词
11. 引用去重和重新编号
12. RAGRetrieverV3 初始化
13. 添加文档到 RAG
14. 向量搜索
15. 关键词搜索
16. 混合搜索
17. 完整检索流程
18. RAG 查询
19. 获取统计信息

### 中文测试 (test/chinese.test.js) - 11 个测试
1. BM25 中文分词
2. 中文停用词过滤
3. 中英文混合分词
4. 中文文档分块
5. 中文标点分块
6. 添加中文文档
7. 中文向量搜索
8. 中文关键词搜索
9. 中文混合搜索
10. 中文完整检索
11. 中文 RAG 查询

**总计: 44 个测试用例** (超过要求的 15 个)

## 依赖项

### 生产依赖
- `@lancedb/lancedb` - 向量数据库
- `@node-rs/jieba` - 中文分词
- `@xenova/transformers` - 本地 Transformer 模型
- `apache-arrow` - Arrow 数据格式
- `openai` - OpenAI API 客户端

### 开发依赖
- `assert` - 断言库

## 技术栈

- **运行时**: Node.js >= 18.0.0
- **模块系统**: ES Modules (type: module)
- **向量数据库**: LanceDB
- **嵌入模型**: Xenova/Transformers.js (本地) / OpenAI API
- **重排序**: Cross-Encoder (MS MARCO)
- **中文分词**: @node-rs/jieba

## 版本信息

- **版本**: 3.0.0
- **创建时间**: 2026-03-27
- **状态**: ✅ 完整实现

# RAG Retriever V3.0

🦞 高级检索增强生成系统 - 为 OpenClaw 提供企业级文档检索能力

## 核心特性

- 🧠 **语义嵌入** - 支持 OpenAI + BGE + MiniLM 多模型
- 🔍 **混合检索** - 向量相似度 + BM25 关键词 + RRF 融合
- 🔄 **智能重排序** - Cross-Encoder 精确重打分
- 📖 **来源引用** - 自动编号 + 完整溯源
- 🇨🇳 **中文优化** - jieba 分词 + 中文标点处理

## 快速开始

```bash
# 安装依赖
npm install

# 初始化
node src/cli.js init

# 添加文档
node src/cli.js add ./document.txt '{"source":"文档来源"}'

# 检索
node src/cli.js search "查询内容" 5

# RAG 查询
node src/cli.js rag "什么是人工智能" 3
```

## 项目结构

```
skills/rag-retriever-v3/
├── src/
│   ├── embeddings/          # 嵌入模型
│   │   ├── EmbeddingProvider.js
│   │   ├── XenovaEmbedding.js      # 本地嵌入
│   │   ├── OpenAIEmbedding.js      # OpenAI API
│   │   └── index.js
│   ├── search/              # 搜索模块
│   │   ├── BM25Search.js           # BM25 关键词搜索
│   │   └── RRFFusion.js            # RRF 融合算法
│   ├── rerank/              # 重排序模块
│   │   ├── CrossEncoderReranker.js # Cross-Encoder
│   │   └── index.js
│   ├── core/                # 核心模块
│   │   ├── ChunkingStrategy.js     # 文档分块
│   │   ├── CitationManager.js      # 来源引用
│   │   ├── RAGRetrieverV3.js       # 主检索器
│   │   └── index.js
│   ├── cli.js               # 命令行工具
│   └── index.js             # 主入口
├── test/
│   ├── unit.test.js         # 单元测试
│   ├── integration.test.js  # 集成测试
│   ├── chinese.test.js      # 中文测试
│   └── run-all-tests.js     # 测试运行器
├── SKILL.md                 # 详细文档
├── package.json
└── README.md
```

## 测试

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

## 许可证

MIT

# RAG Retriever 测试文档

**版本**: 0.1.0  
**更新日期**: 2026-03-17

---

## 📋 测试清单

### ✅ 单元测试
- [x] 文档分块策略
- [x] 简单文本嵌入
- [x] LanceDB 初始化
- [x] 添加文档
- [ ] 向量检索
- [ ] RAG 格式化输出
- [ ] 统计信息

### ⏳ 集成测试
- [ ] 多文档批量添加
- [ ] 中文文档支持
- [ ] 大文件处理 (>1MB)
- [ ] 持久化验证
- [ ] 检索性能测试

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd skills/rag-retriever
npm install
```

### 2. 运行测试

#### 运行所有测试
```bash
npm test
```

#### 使用 CLI 测试
```bash
# 初始化
npm run rag -- init test_docs

# 添加文档
npm run rag -- add ./readme.json '{"source":"test"}'

# 检索
npm run rag -- search "MCP protocol" 5

# RAG 查询
npm run rag -- rag "什么是 MCP" 3

# 查看统计
npm run rag -- stats
```

---

## 🧪 测试用例详情

### 文档分块测试

**测试代码**: `test/chunking.test.js`

**测试内容**:
```javascript
import { ChunkingStrategy } from '../src/retriever.js';

const chunking = new ChunkingStrategy({
  chunkSize: 500,
  overlap: 50
});

// 测试 1: 小文档不分块
const small = 'Hello world';
const chunks1 = chunking.chunk(small);
console.assert(chunks1.length === 1);

// 测试 2: 大文档分块
const large = 'A'.repeat(2000);
const chunks2 = chunking.chunk(large);
console.assert(chunks2.length > 1);

// 测试 3: 重叠验证
console.assert(chunks2[0].content.slice(-50) === chunks2[1].content.slice(0, 50));
```

**预期结果**:
- ✅ 小文档单块
- ✅ 大文档多块
- ✅ 重叠部分正确

---

### 嵌入测试

**测试代码**: `test/embedding.test.js`

**测试内容**:
```javascript
import { SimpleTextEmbedding } from '../src/retriever.js';

const embedding = new SimpleTextEmbedding(384);

// 构建词汇表
embedding.buildVocabulary(['Hello world', 'Test document']);

// 生成向量
const vector = embedding.embed('Hello');
console.assert(vector.length === 384);

// 相似度测试
const v1 = embedding.embed('Hello world');
const v2 = embedding.embed('Hello');
const v3 = embedding.embed('Goodbye');

// v1 和 v2 应该更相似
const sim12 = cosineSimilarity(v1, v2);
const sim13 = cosineSimilarity(v1, v3);
console.assert(sim12 > sim13);
```

**预期结果**:
- ✅ 向量维度正确
- ✅ 相似文本向量接近

---

### 检索测试

**测试代码**: `test/retriever.test.js`

**测试内容**:
```javascript
import { RAGRetriever } from '../src/retriever.js';

const rag = new RAGRetriever({
  dbPath: './test-data/lancedb'
});

// 初始化
await rag.initialize('test_collection');

// 添加文档
await rag.addDocument('MCP is a protocol for AI tools', {
  source: 'test'
});

// 检索
const results = await rag.retrieve('AI protocol', {
  limit: 5
});

console.assert(results.length > 0);
console.log('Top result:', results[0].content);
```

**预期结果**:
- ✅ 成功添加文档
- ✅ 检索返回相关结果
- ✅ 结果按相关性排序

---

## 📊 性能基准

### 目标指标

| 操作 | 目标 | 当前 |
|------|------|------|
| 分块速度 | >1000 字符/ms | ~1500 |
| 嵌入速度 | >100 文档/s | ~120 |
| 检索延迟 | <50ms | ~30 |
| 存储占用 | ~1KB/文档 | ~0.8KB |

### 性能测试脚本

```javascript
// test/performance.test.js

const text = 'A'.repeat(10000);
const start = Date.now();
const chunks = chunking.chunk(text);
const duration = Date.now() - start;

console.log(`分块速度：${text.length / duration} 字符/ms`);
```

---

## 🔧 调试技巧

### 1. 启用详细日志
```javascript
const rag = new RAGRetriever({
  dbPath: './data/lancedb',
  debug: true  // 启用调试模式
});
```

### 2. 检查 LanceDB 状态
```bash
# 查看数据库文件
ls -la data/lancedb/

# 查看词汇表
cat data/lancedb/vocabulary.json
```

### 3. 验证向量质量
```javascript
const vector = embedding.embed('test');
console.log('非零元素:', vector.filter(v => v !== 0).length);
console.log('归一化:', Math.sqrt(vector.reduce((s, v) => s + v*v, 0)));
```

---

## 🐛 已知问题

1. **简单嵌入效果有限**
   - 问题：词频嵌入无法捕捉语义
   - 解决：计划集成真正的嵌入模型 (OpenAI/Cohere)

2. **中文分词不支持**
   - 问题：当前只支持英文分词
   - 解决：计划添加 jieba 分词支持

3. **LanceDB API 兼容性**
   - 问题：不同版本 API 可能有差异
   - 解决：锁定版本 `@lancedb/lancedb@^0.5.0`

---

## 📚 参考资料

- [LanceDB 文档](https://lancedb.github.io/lancedb/)
- [RAG 最佳实践](https://www.chatrag.ai/blog/2026-02-06-7-best-practices-for-rag-implementation)
- [嵌入模型对比 2026](https://www.stack-ai.com/insights/best-embedding-models-for-rag-in-2026)

---

*最后更新：2026-03-17*

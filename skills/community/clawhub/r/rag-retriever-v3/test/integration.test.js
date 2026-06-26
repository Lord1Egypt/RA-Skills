/**
 * RAG 3.0 集成测试
 * 测试完整流程和模块间协作
 */

import { RAGRetrieverV3 } from '../src/core/RAGRetrieverV3.js';
import { XenovaEmbedding } from '../src/embeddings/XenovaEmbedding.js';
import { CrossEncoderReranker } from '../src/rerank/CrossEncoderReranker.js';
import { RRFFusion } from '../src/search/RRFFusion.js';
import { CitationManager } from '../src/core/CitationManager.js';

// 测试计数
let passed = 0;
let failed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}: ${error.message}`);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    failed++;
  }
}

console.log('🧪 RAG 3.0 集成测试\n');

// ========== XenovaEmbedding 集成测试 ==========
console.log('\n📦 XenovaEmbedding 集成测试');

await test('Xenova 嵌入模型加载', async () => {
  const embedding = new XenovaEmbedding({ 
    modelName: 'Xenova/all-MiniLM-L6-v2' 
  });
  await embedding.initialize();
  if (!embedding.initialized) {
    throw new Error('模型未初始化');
  }
});

await test('Xenova 生成嵌入', async () => {
  const embedding = new XenovaEmbedding({ 
    modelName: 'Xenova/all-MiniLM-L6-v2' 
  });
  await embedding.initialize();
  const vector = await embedding.embed('这是一个测试句子');
  if (!Array.isArray(vector) || vector.length === 0) {
    throw new Error('嵌入生成失败');
  }
  if (vector.length !== 384) {
    throw new Error(`维度错误: 期望 384, 实际 ${vector.length}`);
  }
});

await test('Xenova 批量嵌入', async () => {
  const embedding = new XenovaEmbedding({ 
    modelName: 'Xenova/all-MiniLM-L6-v2' 
  });
  await embedding.initialize();
  const texts = ['句子一', '句子二', '句子三'];
  const vectors = await embedding.embedBatch(texts);
  if (vectors.length !== 3) {
    throw new Error(`批量嵌入数量错误: 期望 3, 实际 ${vectors.length}`);
  }
});

await test('Xenova 中文嵌入', async () => {
  const embedding = new XenovaEmbedding({ 
    modelName: 'Xenova/all-MiniLM-L6-v2' 
  });
  await embedding.initialize();
  const vector = await embedding.embed('人工智能和机器学习');
  if (!Array.isArray(vector) || vector.length !== 384) {
    throw new Error('中文嵌入失败');
  }
});

// ========== CrossEncoderReranker 集成测试 ==========
console.log('\n📦 CrossEncoderReranker 集成测试');

await test('CrossEncoder 模型加载', async () => {
  const reranker = new CrossEncoderReranker({
    modelName: 'Xenova/ms-marco-MiniLM-L-6-v2'
  });
  await reranker.initialize();
  if (!reranker.initialized) {
    throw new Error('重排序器未初始化');
  }
});

await test('CrossEncoder 评分', async () => {
  const reranker = new CrossEncoderReranker({
    modelName: 'Xenova/ms-marco-MiniLM-L-6-v2'
  });
  await reranker.initialize();
  const score = await reranker.score(
    '什么是人工智能',
    '人工智能是计算机科学的一个分支'
  );
  if (typeof score !== 'number') {
    throw new Error('评分返回类型错误');
  }
});

await test('CrossEncoder 批量重排序', async () => {
  const reranker = new CrossEncoderReranker({
    modelName: 'Xenova/ms-marco-MiniLM-L-6-v2'
  });
  await reranker.initialize();
  const query = '机器学习应用';
  const documents = [
    { id: '1', content: '机器学习在医疗诊断中的应用' },
    { id: '2', content: '深度学习是机器学习的一种方法' },
    { id: '3', content: '人工智能的历史发展' }
  ];
  const results = await reranker.rerank(query, documents, { limit: 3 });
  if (results.length !== 3) {
    throw new Error(`重排序结果数量错误: 期望 3, 实际 ${results.length}`);
  }
  if (!results[0].rerankScore) {
    throw new Error('重排序结果缺少分数');
  }
});

// ========== RRFFusion 集成测试 ==========
console.log('\n📦 RRFFusion 集成测试');

await test('RRF 融合多列表', async () => {
  const rrf = new RRFFusion({ k: 60 });
  const vectorResults = [
    { id: 'doc1', score: 0.95, content: '内容1' },
    { id: 'doc2', score: 0.90, content: '内容2' },
    { id: 'doc3', score: 0.85, content: '内容3' }
  ];
  const keywordResults = [
    { id: 'doc2', score: 0.92, content: '内容2' },
    { id: 'doc4', score: 0.88, content: '内容4' },
    { id: 'doc1', score: 0.80, content: '内容1' }
  ];
  const fused = rrf.fuseTwo(vectorResults, keywordResults, { limit: 5 });
  if (fused.length === 0) {
    throw new Error('融合结果为空');
  }
  // doc1 和 doc2 在两个列表中都出现，应该排名靠前
  const topIds = fused.slice(0, 2).map(r => r.id);
  if (!topIds.includes('doc1') && !topIds.includes('doc2')) {
    throw new Error('RRF 融合结果不符合预期');
  }
});

await test('RRF 带权重融合', async () => {
  const rrf = new RRFFusion({ k: 60 });
  const list1 = [{ id: 'a', score: 0.9 }];
  const list2 = [{ id: 'b', score: 0.95 }];
  const fused = rrf.fuseWeighted([list1, list2], [2.0, 0.5], { limit: 5 });
  if (fused.length !== 2) {
    throw new Error('带权重融合结果数量错误');
  }
});

// ========== CitationManager 集成测试 ==========
console.log('\n📦 CitationManager 集成测试');

await test('生成完整 RAG 提示词', async () => {
  const cm = new CitationManager();
  const query = '什么是机器学习';
  const results = [
    { 
      id: '1', 
      content: '机器学习是人工智能的一个分支',
      metadata: { title: 'AI百科', url: 'http://example.com/ai' }
    },
    { 
      id: '2', 
      content: '机器学习让计算机从数据中学习',
      metadata: { title: '技术博客', author: '张三' }
    }
  ];
  const citedResults = cm.addCitations(results);
  const ragPrompt = cm.generateRAGPrompt(query, citedResults);
  if (!ragPrompt.fullPrompt) {
    throw new Error('未生成完整提示词');
  }
  if (!ragPrompt.context.includes('[1]')) {
    throw new Error('提示词中缺少引用标记');
  }
  if (!ragPrompt.citationList.includes('AI百科')) {
    throw new Error('引用列表中缺少来源');
  }
});

await test('引用去重和重新编号', async () => {
  const cm = new CitationManager();
  const results = [
    { id: '1', content: '内容1', score: 0.5 },
    { id: '1', content: '内容1', score: 0.8 },  // 重复
    { id: '2', content: '内容2', score: 0.6 }
  ];
  const deduped = cm.deduplicateCitations(results);
  if (deduped.length !== 2) {
    throw new Error(`去重后数量错误: 期望 2, 实际 ${deduped.length}`);
  }
  // 检查是否保留了最高分数
  const doc1 = deduped.find(r => r.id === '1');
  if (doc1.score !== 0.8) {
    throw new Error('去重时未保留最高分数');
  }
});

// ========== RAGRetrieverV3 集成测试 ==========
console.log('\n📦 RAGRetrieverV3 集成测试');

const testDbPath = './data/test-lancedb-v3';

await test('RAGRetrieverV3 初始化', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  if (!rag.initialized) {
    throw new Error('RAG 检索器未初始化');
  }
  if (!rag.embedding) {
    throw new Error('嵌入模型未加载');
  }
  await rag.close();
});

await test('添加文档到 RAG', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const text = `
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支。
    它致力于创造能够模拟人类智能的系统。
    机器学习是人工智能的一个重要子领域。
    深度学习则是机器学习的一种方法，使用神经网络进行学习。
  `;
  
  const result = await rag.addDocument(text, { 
    title: 'AI介绍', 
    source: '测试文档' 
  });
  
  if (result.chunks === 0) {
    throw new Error('文档分块失败');
  }
  if (!result.stats) {
    throw new Error('缺少分块统计信息');
  }
  
  await rag.close();
});

await test('向量搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.vectorSearch('人工智能', { limit: 3 });
  if (results.length === 0) {
    throw new Error('向量搜索无结果');
  }
  if (!results[0].score) {
    throw new Error('搜索结果缺少分数');
  }
  
  await rag.close();
});

await test('关键词搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.keywordSearch('机器学习', { limit: 3 });
  if (results.length === 0) {
    throw new Error('关键词搜索无结果');
  }
  
  await rag.close();
});

await test('混合搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.hybridSearch('深度学习', { limit: 3 });
  if (results.length === 0) {
    throw new Error('混合搜索无结果');
  }
  if (!results[0].rrfScore) {
    throw new Error('混合搜索结果缺少 RRF 分数');
  }
  
  await rag.close();
});

await test('完整检索流程', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' },
    rerank: { enabled: false }  // 禁用重排序以加速测试
  });
  await rag.initialize();
  
  const results = await rag.retrieve('什么是人工智能', { 
    limit: 3,
    hybrid: true,
    rerank: false,
    addCitations: true
  });
  
  if (results.length === 0) {
    throw new Error('检索无结果');
  }
  if (!results[0].citation) {
    throw new Error('检索结果缺少引用');
  }
  
  await rag.close();
});

await test('RAG 查询', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' },
    rerank: { enabled: false }
  });
  await rag.initialize();
  
  const result = await rag.retrieveForRAG('机器学习的应用', { limit: 2 });
  
  if (!result.query) {
    throw new Error('RAG 结果缺少查询');
  }
  if (!result.context) {
    throw new Error('RAG 结果缺少上下文');
  }
  if (!result.fullPrompt) {
    throw new Error('RAG 结果缺少完整提示词');
  }
  
  await rag.close();
});

await test('获取统计信息', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const stats = await rag.getStats();
  if (!stats.collection) {
    throw new Error('统计信息缺少集合名');
  }
  if (!stats.embedding) {
    throw new Error('统计信息缺少嵌入信息');
  }
  
  await rag.close();
});

// ========== 测试总结 ==========
console.log('\n' + '='.repeat(50));
console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}
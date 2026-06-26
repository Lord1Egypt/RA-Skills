// RAG 2.0 测试
import { RAG2Retriever } from '../src/rag2.js';
import { BM25Search } from '../src/bm25.js';
import { HybridSearch } from '../src/hybrid-search.js';
import { SimpleEmbedding } from '../src/embeddings.js';

// 测试文档
const testDocs = [
  {
    content: '人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。AI 包括机器学习、深度学习、自然语言处理等领域。',
    metadata: { source: 'ai-intro.md', title: 'AI 入门' }
  },
  {
    content: '机器学习是人工智能的一个子集，它使计算机能够在不被明确编程的情况下学习。机器学习算法通过分析数据来识别模式并做出决策。',
    metadata: { source: 'ml-basics.md', title: '机器学习基础' }
  },
  {
    content: '深度学习是机器学习的一个子集，使用神经网络来模拟人脑的工作方式。深度学习在图像识别、语音识别和自然语言处理方面表现出色。',
    metadata: { source: 'deep-learning.md', title: '深度学习' }
  },
  {
    content: '自然语言处理（NLP）是人工智能的一个领域，专注于计算机与人类语言之间的交互。NLP 使计算机能够理解、解释和生成人类语言。',
    metadata: { source: 'nlp-intro.md', title: 'NLP 入门' }
  },
  {
    content: 'RAG（检索增强生成）是一种结合了检索和生成的 AI 技术。它首先检索相关文档，然后使用这些文档作为上下文来生成更准确的回答。',
    metadata: { source: 'rag-intro.md', title: 'RAG 介绍' }
  }
];

// 测试 BM25 搜索
function testBM25() {
  console.log('=== BM25 搜索测试 ===');
  const bm25 = new BM25Search();

  for (const doc of testDocs) {
    bm25.addDocument(doc.metadata.source, doc.content, doc.metadata);
  }

  const results = bm25.search('人工智能');
  console.log(`查询: "人工智能"`);
  console.log(`结果数: ${results.length}`);
  results.forEach((r, i) => {
    console.log(`  ${i + 1}. [${r.score.toFixed(4)}] ${r.metadata.title}`);
  });

  return results.length > 0;
}

// 测试简单嵌入
async function testEmbedding() {
  console.log('\n=== 简单嵌入测试 ===');
  const embedding = new SimpleEmbedding({ dimensions: 128 });

  const vec1 = await embedding.embed('人工智能是计算机科学的分支');
  const vec2 = await embedding.embed('AI 是计算机科学的一个领域');
  const vec3 = await embedding.embed('今天天气很好');

  console.log(`向量维度: ${vec1.length}`);
  
  // 计算相似度
  const sim12 = cosineSimilarity(vec1, vec2);
  const sim13 = cosineSimilarity(vec1, vec3);
  
  console.log(`相似度 (AI vs AI): ${sim12.toFixed(4)}`);
  console.log(`相似度 (AI vs 天气): ${sim13.toFixed(4)}`);
  console.log(`AI 相关文本相似度更高: ${sim12 > sim13 ? '✅' : '❌'}`);

  return sim12 > sim13;
}

// 测试混合搜索
async function testHybridSearch() {
  console.log('\n=== 混合搜索测试 ===');
  const embedding = new SimpleEmbedding({ dimensions: 128 });
  const search = new HybridSearch({
    embeddingProvider: embedding,
    vectorWeight: 0.6,
    bm25Weight: 0.4
  });

  await search.addDocuments(testDocs.map((doc, i) => ({
    id: `doc_${i}`,
    content: doc.content,
    metadata: doc.metadata
  })));

  const results = await search.hybridSearch('什么是深度学习', 3);
  console.log(`查询: "什么是深度学习"`);
  console.log(`结果数: ${results.length}`);
  results.forEach((r, i) => {
    console.log(`  ${i + 1}. [${r.score.toFixed(4)}] ${r.metadata.title} (向量:${r.vectorScore?.toFixed(4) || 'N/A'}, BM25:${r.bm25Score?.toFixed(4) || 'N/A'})`);
    if (r.citation) {
      console.log(`     引用: ${r.citation.source}`);
    }
  });

  return results.length > 0;
}

// 测试 RAG2Retriever
async function testRAG2() {
  console.log('\n=== RAG 2.0 完整测试 ===');
  const rag = new RAG2Retriever({
    embeddingType: 'simple',
    vectorWeight: 0.7,
    bm25Weight: 0.3,
    chunkSize: 200,
    chunkOverlap: 20
  });

  // 添加文档
  for (const doc of testDocs) {
    await rag.addDocument(doc.content, doc.metadata);
  }

  console.log(`已添加文档: ${rag.documents.length} chunks`);

  // 搜索测试
  const query = '机器学习是什么';
  const results = await rag.query(query, { topK: 3, method: 'hybrid' });
  
  console.log(`\n查询: "${query}"`);
  console.log(`方法: ${results.method}`);
  console.log(`结果数: ${results.resultsCount}`);
  
  results.results.forEach((r, i) => {
    console.log(`  ${r.reference} [${r.score}] ${r.metadata.source}`);
    console.log(`     ${r.content.slice(0, 60)}...`);
  });

  if (results.citations) {
    console.log('\n引用列表:');
    results.citations.forEach(c => console.log(`  ${c}`));
  }

  // 上下文增强测试
  const augmented = await rag.augmentContext('什么是 RAG');
  console.log(`\n上下文增强:`);
  console.log(`  有结果: ${augmented.hasResults}`);
  console.log(`  结果数: ${augmented.resultsCount}`);
  if (augmented.prompt) {
    console.log(`  提示词长度: ${augmented.prompt.length}`);
  }

  // 统计信息
  const stats = rag.getStats();
  console.log(`\n统计信息:`);
  console.log(`  总文档数: ${stats.totalDocuments}`);
  console.log(`  总嵌入数: ${stats.totalEmbeddings}`);
  console.log(`  BM25 词条: ${stats.bm25.totalTerms}`);

  return results.resultsCount > 0 && augmented.hasResults;
}

// 余弦相似度
function cosineSimilarity(a, b) {
  if (a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

// 运行所有测试
async function runTests() {
  console.log('🚀 RAG 2.0 测试开始\n');
  
  const results = {
    bm25: false,
    embedding: false,
    hybrid: false,
    rag2: false
  };

  try {
    results.bm25 = testBM25();
    results.embedding = await testEmbedding();
    results.hybrid = await testHybridSearch();
    results.rag2 = await testRAG2();
  } catch (err) {
    console.error('测试错误:', err);
  }

  console.log('\n=== 测试结果汇总 ===');
  console.log(`BM25 搜索: ${results.bm25 ? '✅ 通过' : '❌ 失败'}`);
  console.log(`简单嵌入: ${results.embedding ? '✅ 通过' : '❌ 失败'}`);
  console.log(`混合搜索: ${results.hybrid ? '✅ 通过' : '❌ 失败'}`);
  console.log(`RAG 2.0: ${results.rag2 ? '✅ 通过' : '❌ 失败'}`);

  const passed = Object.values(results).filter(Boolean).length;
  const total = Object.keys(results).length;
  console.log(`\n总计: ${passed}/${total} 通过`);

  return passed === total;
}

runTests().then(success => {
  process.exit(success ? 0 : 1);
});

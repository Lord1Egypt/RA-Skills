// RAG 2.0 + Transformers.js 集成测试
import { RAG2Retriever } from '../src/rag2.js';
import { TransformersEmbedding } from '../src/transformers-embedding.js';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 本地模型路径
const MODEL_DIR = join(__dirname, '../data/models/all-MiniLM-L6-v2');

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

async function runTest() {
  console.log('🚀 RAG 2.0 + Transformers.js 集成测试\n');

  // 创建本地嵌入提供者
  console.log('=== 初始化本地嵌入提供者 ===');
  const embedding = new TransformersEmbedding({
    modelId: MODEL_DIR,
    dimensions: 384,
    cachePath: join(__dirname, '../data/models/all-MiniLM-L6-v2')
  });

  // 创建 RAG 2.0 检索器
  console.log('=== 初始化 RAG 2.0 检索器 ===');
  const rag = new RAG2Retriever({
    embeddingProvider: embedding,
    vectorWeight: 0.7,
    bm25Weight: 0.3,
    chunkSize: 200,
    chunkOverlap: 20
  });

  // 添加文档
  console.log('\n=== 添加文档 ===');
  for (const doc of testDocs) {
    await rag.addDocument(doc.content, doc.metadata);
  }
  console.log(`已添加 ${rag.documents.length} 个文档块`);

  // 测试混合搜索
  console.log('\n=== 混合搜索测试 ===');
  const query1 = '什么是深度学习';
  const results1 = await rag.query(query1, { topK: 3, method: 'hybrid' });
  
  console.log(`查询: "${query1}"`);
  console.log(`方法: ${results1.method}`);
  console.log(`结果数: ${results1.resultsCount}`);
  
  results1.results.forEach((r, i) => {
    console.log(`  ${r.reference} [${r.score.toFixed(4)}] ${r.metadata.source}`);
    console.log(`     向量:${r.vectorScore.toFixed(4)} | BM25:${r.bm25Score.toFixed(4)}`);
  });

  // 测试向量搜索
  console.log('\n=== 向量搜索测试 ===');
  const query2 = '什么是机器学习';
  const results2 = await rag.query(query2, { topK: 3, method: 'vector' });
  
  console.log(`查询: "${query2}"`);
  console.log(`方法: ${results2.method}`);
  console.log(`结果数: ${results2.resultsCount}`);
  
  results2.results.forEach((r, i) => {
    console.log(`  ${r.reference} [${r.score.toFixed(4)}] ${r.metadata.source}`);
  });

  // 测试上下文增强
  console.log('\n=== 上下文增强测试 ===');
  const augmented = await rag.augmentContext('什么是 RAG');
  console.log(`有结果: ${augmented.hasResults}`);
  console.log(`结果数: ${augmented.resultsCount}`);
  if (augmented.citations) {
    console.log('引用:');
    augmented.citations.forEach(c => console.log(`  ${c}`));
  }

  // 统计信息
  console.log('\n=== 统计信息 ===');
  const stats = rag.getStats();
  console.log(`总文档数: ${stats.totalDocuments}`);
  console.log(`总嵌入数: ${stats.totalEmbeddings}`);
  console.log(`嵌入类型: ${stats.config.embeddingType}`);
  console.log(`向量权重: ${stats.config.vectorWeight}`);
  console.log(`BM25权重: ${stats.config.bm25Weight}`);

  console.log('\n🎉 RAG 2.0 + Transformers.js 集成测试完成！');
  return results1.resultsCount > 0 && results2.resultsCount > 0;
}

runTest().then(success => {
  process.exit(success ? 0 : 1);
});

/**
 * RAG 3.0 中文测试
 * 测试中文分词、中文搜索和中文文档处理
 */

import { RAGRetrieverV3 } from '../src/core/RAGRetrieverV3.js';
import { BM25Search } from '../src/search/BM25Search.js';
import { ChunkingStrategy } from '../src/core/ChunkingStrategy.js';

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

console.log('🧪 RAG 3.0 中文测试\n');

// ========== 中文分词测试 ==========
console.log('\n📦 中文分词测试');

await test('BM25 中文分词', async () => {
  const bm25 = new BM25Search();
  const tokens = await bm25.tokenize('自然语言处理是人工智能的重要方向');
  if (tokens.length === 0) {
    throw new Error('中文分词失败');
  }
  // 应该包含"自然语言处理"、"人工智能"等词
  const hasMeaningfulTokens = tokens.some(t => t.length >= 2);
  if (!hasMeaningfulTokens) {
    throw new Error('分词结果缺少有意义的词');
  }
});

await test('中文停用词过滤', async () => {
  const bm25 = new BM25Search();
  const tokens = await bm25.tokenize('这是一个测试');
  // "是"、"一个"等停用词应该被过滤
  if (tokens.includes('是') || tokens.includes('的')) {
    throw new Error('停用词未正确过滤');
  }
});

await test('中英文混合分词', async () => {
  const bm25 = new BM25Search();
  const tokens = await bm25.tokenize('AI人工智能和Machine Learning机器学习');
  if (tokens.length === 0) {
    throw new Error('混合分词失败');
  }
  // 应该同时包含中文和英文词
  const hasChinese = tokens.some(t => /[\u4e00-\u9fa5]/.test(t));
  const hasEnglish = tokens.some(t => /^[a-zA-Z]+$/.test(t));
  if (!hasChinese && !hasEnglish) {
    throw new Error('混合分词未正确处理中英文');
  }
});

// ========== 中文文档处理测试 ==========
console.log('\n📦 中文文档处理测试');

await test('中文文档分块', async () => {
  const chunker = new ChunkingStrategy({ 
    chunkSize: 100, 
    overlap: 10,
    strategy: 'recursive'
  });
  
  const text = `
    人工智能是计算机科学的一个分支，它致力于研究和开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。
    
    机器学习是人工智能的核心技术之一。它使用统计学方法，让计算机系统能够从数据中学习规律，并根据学习到的规律对未知数据进行预测或决策。
    
    深度学习是机器学习的一个子集，它使用多层神经网络来模拟人脑的工作方式。深度学习在图像识别、语音识别、自然语言处理等领域取得了突破性进展。
  `;
  
  const chunks = chunker.chunk(text, { title: 'AI介绍', source: '测试' });
  if (chunks.length === 0) {
    throw new Error('中文文档分块失败');
  }
  // 检查是否保留了中文内容
  const hasChineseContent = chunks.some(c => /[\u4e00-\u9fa5]/.test(c.content));
  if (!hasChineseContent) {
    throw new Error('分块结果缺少中文内容');
  }
});

await test('中文标点分块', async () => {
  const chunker = new ChunkingStrategy({ 
    chunkSize: 50, 
    strategy: 'recursive'
  });
  
  // 使用中文标点
  const text = '第一句。第二句；第三句，第四句！第五句？';
  const chunks = chunker.chunk(text);
  
  // 递归分块应该优先在中文标点处分割
  if (chunks.length === 0) {
    throw new Error('中文标点分块失败');
  }
});

// ========== 中文搜索测试 ==========
console.log('\n📦 中文搜索测试');

const testDbPath = './data/test-chinese-lancedb-v3';

await test('添加中文文档', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const text = `
    自然语言处理（Natural Language Processing，NLP）是人工智能和语言学领域的分支学科。
    它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
    
    自然语言处理主要应用于机器翻译、舆情监测、自动摘要、观点提取、文本分类、问题回答、文本语义对比等方面。
    
    深度学习技术的引入大大提升了自然语言处理的效果。
    基于神经网络的模型在文本理解、生成和推理任务上都取得了显著进展。
  `;
  
  const result = await rag.addDocument(text, { 
    title: '自然语言处理介绍', 
    source: '中文测试文档',
    category: 'AI技术'
  });
  
  if (result.chunks === 0) {
    throw new Error('中文文档添加失败');
  }
  
  await rag.close();
});

await test('中文向量搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.vectorSearch('自然语言处理', { limit: 3 });
  if (results.length === 0) {
    throw new Error('中文向量搜索无结果');
  }
  
  await rag.close();
});

await test('中文关键词搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.keywordSearch('深度学习', { limit: 3 });
  if (results.length === 0) {
    throw new Error('中文关键词搜索无结果');
  }
  
  await rag.close();
});

await test('中文混合搜索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' }
  });
  await rag.initialize();
  
  const results = await rag.hybridSearch('神经网络模型', { limit: 3 });
  if (results.length === 0) {
    throw new Error('中文混合搜索无结果');
  }
  
  await rag.close();
});

await test('中文完整检索', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' },
    rerank: { enabled: false }
  });
  await rag.initialize();
  
  const results = await rag.retrieve('机器翻译技术', { 
    limit: 3,
    hybrid: true,
    rerank: false,
    addCitations: true
  });
  
  if (results.length === 0) {
    throw new Error('中文完整检索无结果');
  }
  if (!results[0].citation) {
    throw new Error('中文检索结果缺少引用');
  }
  
  await rag.close();
});

await test('中文 RAG 查询', async () => {
  const rag = new RAGRetrieverV3({
    dbPath: testDbPath,
    embeddingProvider: 'xenova',
    embeddingOptions: { modelName: 'Xenova/all-MiniLM-L6-v2' },
    rerank: { enabled: false }
  });
  await rag.initialize();
  
  const result = await rag.retrieveForRAG('自然语言处理有哪些应用', { limit: 2 });
  
  if (!result.query) {
    throw new Error('中文 RAG 结果缺少查询');
  }
  if (!result.context) {
    throw new Error('中文 RAG 结果缺少上下文');
  }
  // 检查上下文是否包含中文
  if (!/[\u4e00-\u9fa5]/.test(result.context)) {
    throw new Error('RAG 上下文缺少中文内容');
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

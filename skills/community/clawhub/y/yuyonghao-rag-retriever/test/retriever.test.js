// RAG Retriever 测试

import { RAGRetriever, ChunkingStrategy, SimpleTextEmbedding } from '../src/retriever.js';

async function runTests() {
  console.log('🧪 RAG Retriever 测试开始...\n');

  // 测试 1: 分块策略
  console.log('📋 测试 1: 分块策略');
  const chunking = new ChunkingStrategy({
    chunkSize: 100,
    overlap: 20,
    separator: '\n'
  });

  const testText = `这是第一段。
这是第二段。
这是第三段。
这是第四段。
这是第五段。`;

  const chunks = chunking.chunk(testText, { source: 'test' });
  console.log(`分块数量：${chunks.length}`);
  chunks.forEach((chunk, i) => {
    console.log(`  块 ${i}: ${chunk.content.length} 字符`);
  });

  // 测试 2: 简单嵌入
  console.log('\n📋 测试 2: 简单嵌入');
  const embedding = new SimpleTextEmbedding(64);
  const texts = [
    '人工智能是未来的技术',
    '机器学习是人工智能的子集',
    '深度学习使用神经网络'
  ];

  console.log('构建词汇表...');
  embedding.buildVocabulary(texts);
  console.log(`词汇表大小：${embedding.vocabSize}`);

  const vector = embedding.embed('人工智能');
  console.log(`向量维度：${vector.length}`);
  console.log(`非零元素：${vector.filter(v => v !== 0).length}`);

  // 测试 3: RAG 检索器初始化
  console.log('\n📋 测试 3: RAG 检索器初始化');
  const retriever = new RAGRetriever({
    dbPath: './data/test-lancedb',
    dimensions: 64
  });

  try {
    await retriever.initialize('test_collection_v2');
    console.log('✅ 初始化成功');
  } catch (error) {
    console.log('⚠️ 初始化警告:', error.message);
  }

  // 测试 4: 添加文档
  console.log('\n📋 测试 4: 添加文档');
  const testDoc = `
RAG (Retrieval-Augmented Generation) 是一种人工智能技术。
它结合了检索和生成的优势。
RAG 系统首先从知识库中检索相关文档。
然后将检索到的信息用于生成回答。
这种方法可以减少幻觉，提高准确性。
`;

  const addResult = await retriever.addDocument(testDoc, {
    source: 'test',
    timestamp: new Date().toISOString()
  });
  console.log(`添加结果：${addResult.chunks} 块`);
  console.log(`文档 IDs: ${addResult.ids.slice(0, 3).join(', ')}...`);

  // 测试 5: 检索
  console.log('\n📋 测试 5: 检索测试');
  const query = 'RAG 是什么技术？';
  const results = await retriever.retrieve(query, { limit: 3 });
  
  console.log(`检索结果：${results.length} 条`);
  results.forEach((result, i) => {
    console.log(`\n[${i + 1}] 分数：${result.score.toFixed(4)}`);
    console.log(`    内容：${result.content.substring(0, 50)}...`);
  });

  // 测试 6: RAG 格式化
  console.log('\n📋 测试 6: RAG 格式化');
  const ragResult = await retriever.retrieveForRAG(query, { limit: 3 });
  console.log(`查询：${ragResult.query}`);
  console.log(`结果数：${ragResult.resultCount}`);
  console.log(`上下文长度：${ragResult.context.length} 字符`);

  // 测试 7: 统计信息
  console.log('\n📋 测试 7: 统计信息');
  const stats = await retriever.getStats();
  console.log('统计:', stats);

  // 清理
  await retriever.close();
  console.log('\n🎉 所有测试通过！');
}

runTests().catch(console.error);

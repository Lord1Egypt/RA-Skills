// 中文分词测试
// 测试 jieba 集成和中文文档检索

import { RAGRetriever } from '../src/retriever.js';
import { existsSync, rmSync } from 'fs';
import { join } from 'path';

const testDbPath = join(import.meta.dirname, '../data/test-lancedb-chinese');

async function testChineseTokenizer() {
  console.log('🇨🇳 中文分词测试开始...\n');

  // 清理测试数据库
  if (existsSync(testDbPath)) {
    rmSync(testDbPath, { recursive: true, force: true });
  }

  const rag = new RAGRetriever({
    dbPath: testDbPath,
    dimensions: 384
  });

  try {
    // 测试 1: 初始化
    console.log('📋 测试 1: 初始化 RAG 系统');
    await rag.initialize('chinese_docs');
    console.log('✅ 初始化成功\n');

    // 测试 2: 添加中文文档
    console.log('📋 测试 2: 添加中文文档');
    const chineseDocs = [
      {
        text: '人工智能（AI）是计算机科学的一个分支，致力于创建能够执行需要人类智能的任务的系统。这些任务包括学习、推理、问题解决、感知和理解语言。',
        metadata: { source: 'wikipedia', topic: 'AI' }
      },
      {
        text: '机器学习是人工智能的核心技术之一，通过算法使计算机能够从数据中学习并改进性能，而无需明确编程。深度学习是机器学习的一个子集，使用神经网络模拟人脑。',
        metadata: { source: 'tech-blog', topic: 'ML' }
      },
      {
        text: '自然语言处理（NLP）使计算机能够理解、解释和生成人类语言。应用场景包括机器翻译、情感分析、聊天机器人和语音助手。',
        metadata: { source: 'research', topic: 'NLP' }
      },
      {
        text: '计算机视觉是 AI 的另一个重要领域，使机器能够"看到"和理解图像、视频中的内容。应用包括人脸识别、自动驾驶和医学影像分析。',
        metadata: { source: 'tech-blog', topic: 'CV' }
      }
    ];

    for (const doc of chineseDocs) {
      const result = await rag.addDocument(doc.text, doc.metadata);
      console.log(`  ✅ 添加文档：${result.chunks} 块`);
    }
    console.log();

    // 测试 3: 中文检索
    console.log('📋 测试 3: 中文语义检索');
    const queries = [
      { query: '什么是人工智能', expected: 'AI' },
      { query: '机器学习如何工作', expected: 'ML' },
      { query: '自然语言处理应用', expected: 'NLP' },
      { query: '计算机视觉技术', expected: 'CV' }
    ];

    for (const { query, expected } of queries) {
      console.log(`\n  查询："${query}"`);
      const results = await rag.retrieve(query, { limit: 2 });
      
      if (results.length > 0) {
        const topResult = results[0];
        const matchedTopic = topResult.metadata.topic;
        const status = matchedTopic === expected ? '✅' : '⚠️';
        console.log(`  ${status} 匹配主题：${matchedTopic} (期望：${expected})`);
        console.log(`     内容：${topResult.content.substring(0, 50)}...`);
      } else {
        console.log('  ❌ 无结果');
      }
    }

    // 测试 4: 统计信息
    console.log('\n📋 测试 4: 统计信息');
    const stats = await rag.getStats();
    console.log(`  集合：${stats.collection}`);
    console.log(`  文档数：${stats.documentCount}`);
    console.log(`  词汇表大小：${stats.vocabularySize}`);
    console.log(`  向量维度：${stats.dimensions}`);

    // 测试 5: RAG 格式化
    console.log('\n📋 测试 5: RAG 格式化输出');
    const ragResult = await rag.retrieveForRAG('人工智能和机器学习的区别', { limit: 3 });
    console.log(`  检索到 ${ragResult.resultCount} 条结果`);
    console.log(`  上下文长度：${ragResult.context.length} 字符`);

    console.log('\n🎉 中文分词测试完成！');

  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error(error.stack);
  } finally {
    await rag.close();
    
    // 清理测试数据库
    if (existsSync(testDbPath)) {
      rmSync(testDbPath, { recursive: true, force: true });
    }
  }
}

testChineseTokenizer();

// Transformers.js 嵌入测试
import { TransformersEmbedding } from '../src/transformers-embedding.js';

// 测试文本
const testTexts = [
  '人工智能是计算机科学的一个分支',
  '机器学习使计算机能够自动学习',
  '深度学习使用神经网络模拟人脑',
  '今天天气非常好，适合出去散步',
  'Python 是一种流行的编程语言'
];

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

async function runTest() {
  console.log('🚀 Transformers.js 嵌入测试开始\n');

  const embedding = new TransformersEmbedding({
    modelId: 'Xenova/all-MiniLM-L6-v2',
    dimensions: 384
  });

  try {
    // 测试单个嵌入
    console.log('=== 单个嵌入测试 ===');
    const vec1 = await embedding.embed(testTexts[0]);
    console.log(`文本: "${testTexts[0]}"`);
    console.log(`向量维度: ${vec1.length}`);
    console.log(`前5个值: [${vec1.slice(0, 5).map(v => v.toFixed(4)).join(', ')}]`);

    // 测试批量嵌入
    console.log('\n=== 批量嵌入测试 ===');
    const startTime = Date.now();
    const vectors = await embedding.embedBatch(testTexts);
    const elapsed = Date.now() - startTime;
    console.log(`批量嵌入 ${testTexts.length} 个文本`);
    console.log(`耗时: ${elapsed}ms`);
    console.log(`每个: ${(elapsed / testTexts.length).toFixed(1)}ms`);

    // 测试语义相似度
    console.log('\n=== 语义相似度测试 ===');
    
    const testPairs = [
      [0, 1, 'AI vs 机器学习（应该高）'],
      [0, 2, 'AI vs 深度学习（应该高）'],
      [0, 3, 'AI vs 天气（应该低）'],
      [0, 4, 'AI vs Python（应该中等）'],
      [1, 2, '机器学习 vs 深度学习（应该最高）']
    ];

    for (const [i, j, desc] of testPairs) {
      const sim = cosineSimilarity(vectors[i], vectors[j]);
      console.log(`${desc}: ${sim.toFixed(4)}`);
    }

    // 验证排序
    const sim01 = cosineSimilarity(vectors[0], vectors[1]);
    const sim03 = cosineSimilarity(vectors[0], vectors[3]);
    const correct = sim01 > sim03;
    console.log(`\n✅ AI相关文本相似度 > AI vs 天气: ${correct ? '通过' : '失败'}`);

    // 模型信息
    console.log('\n=== 模型信息 ===');
    const info = embedding.getInfo();
    console.log(`模型: ${info.modelId}`);
    console.log(`维度: ${info.dimensions}`);
    console.log(`类型: ${info.type}`);
    console.log(`已初始化: ${info.initialized}`);

    console.log('\n🎉 所有测试完成！');
    return correct;

  } catch (err) {
    console.error('❌ 测试失败:', err.message);
    console.error(err.stack);
    return false;
  }
}

runTest().then(success => {
  process.exit(success ? 0 : 1);
});

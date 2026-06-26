// Transformers.js 嵌入测试（使用镜像）
// 必须在导入 transformers 之前设置环境变量

import { env, pipeline } from '@huggingface/transformers';

// 配置 HuggingFace 镜像
env.HF_HUB_BASE_URL = 'https://hf-mirror.com';
env.HF_ENDPOINT = 'https://hf-mirror.com';

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
  console.log('🚀 Transformers.js 嵌入测试开始（镜像模式）\n');
  console.log(`HuggingFace 镜像: ${env.HF_HUB_BASE_URL}`);

  try {
    // 加载模型
    console.log('\n=== 加载模型 ===');
    console.log('正在下载/加载 all-MiniLM-L6-v2...');
    
    const embedder = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
      cache_dir: './data/transformers-cache',
      quantized: true
    });
    
    console.log('✅ 模型加载完成！');

    // 测试单个嵌入
    console.log('\n=== 单个嵌入测试 ===');
    const startTime = Date.now();
    const output = await embedder(testTexts[0], { pooling: 'mean', normalize: true });
    const vec1 = Array.from(output.data);
    const singleTime = Date.now() - startTime;
    
    console.log(`文本: "${testTexts[0]}"`);
    console.log(`向量维度: ${vec1.length}`);
    console.log(`耗时: ${singleTime}ms`);
    console.log(`前5个值: [${vec1.slice(0, 5).map(v => v.toFixed(4)).join(', ')}]`);

    // 测试批量嵌入
    console.log('\n=== 批量嵌入测试 ===');
    const batchStart = Date.now();
    const batchOutput = await embedder(testTexts, { pooling: 'mean', normalize: true });
    const vectors = batchOutput.tolist();
    const batchTime = Date.now() - batchStart;
    console.log(`批量嵌入 ${testTexts.length} 个文本`);
    console.log(`耗时: ${batchTime}ms`);
    console.log(`每个: ${(batchTime / testTexts.length).toFixed(1)}ms`);

    // 测试语义相似度
    console.log('\n=== 语义相似度测试 ===');
    
    const testPairs = [
      [0, 1, 'AI vs 机器学习（应该高）'],
      [0, 2, 'AI vs 深度学习（应该高）'],
      [0, 3, 'AI vs 天气（应该低）'],
      [0, 4, 'AI vs Python（应该中等）'],
      [1, 2, '机器学习 vs 深度学习（应该最高）']
    ];

    const results = [];
    for (const [i, j, desc] of testPairs) {
      const sim = cosineSimilarity(vectors[i], vectors[j]);
      results.push({ desc, sim, expected: desc.includes('应该高') || desc.includes('应该最高') });
      console.log(`${desc}: ${sim.toFixed(4)}`);
    }

    // 验证
    const sim01 = cosineSimilarity(vectors[0], vectors[1]);
    const sim03 = cosineSimilarity(vectors[0], vectors[3]);
    const correct = sim01 > sim03;
    console.log(`\n✅ AI相关文本相似度 > AI vs 天气: ${correct ? '通过' : '失败'}`);

    console.log('\n🎉 Transformers.js 集成成功！');
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

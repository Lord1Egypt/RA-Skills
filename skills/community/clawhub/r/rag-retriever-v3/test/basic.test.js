/**
 * RAG Retriever V3 - 基础功能测试
 * 验证核心功能在不依赖外部API的情况下可用
 */

import assert from 'assert';
import { 
  createEmbeddingProvider, 
  getAvailableProviders,
  XenovaEmbedding 
} from '../src/embeddings/index.js';
import { ChunkingStrategy } from '../src/core/ChunkingStrategy.js';
import { CitationManager } from '../src/core/CitationManager.js';
import { RRFFusion } from '../src/search/RRFFusion.js';

// 测试统计
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(`   ${error.message}`);
    failed++;
  }
}

console.log('🦞 RAG Retriever V3 - 基础功能测试\n');

// ============ 测试 1: 嵌入提供者工厂函数 ============
console.log('\n📦 测试: 嵌入提供者工厂函数\n');

test('createEmbeddingProvider 应该返回 XenovaEmbedding (auto模式)', () => {
  const provider = createEmbeddingProvider('auto');
  assert(provider instanceof XenovaEmbedding, '应该返回 XenovaEmbedding 实例');
});

test('createEmbeddingProvider 应该返回 XenovaEmbedding (显式xenova)', () => {
  const provider = createEmbeddingProvider('xenova');
  assert(provider instanceof XenovaEmbedding, '应该返回 XenovaEmbedding 实例');
});

test('getAvailableProviders 应该返回提供者信息', () => {
  const providers = getAvailableProviders();
  assert(providers.xenova, '应该包含 xenova 提供者');
  assert(providers.xenova.available === true, 'xenova 应该标记为可用');
  assert(Array.isArray(providers.xenova.models), 'xenova 应该有模型列表');
});

// ============ 测试 2: 文本分块 ============
console.log('\n📦 测试: 文本分块\n');

test('ChunkingStrategy 应该正确分块', () => {
  const chunker = new ChunkingStrategy({ chunkSize: 100, overlap: 20 });
  const text = '这是一段测试文本。'.repeat(20);
  const chunks = chunker.chunk(text, { source: 'test' });
  
  assert(chunks.length > 0, '应该生成至少一个块');
  assert(chunks[0].id, '每个块应该有ID');
  assert(chunks[0].content, '每个块应该有内容');
  assert(chunks[0].metadata, '每个块应该有元数据');
});

test('ChunkingStrategy 应该处理短文本', () => {
  const chunker = new ChunkingStrategy({ chunkSize: 500 });
  const text = '短文本';
  const chunks = chunker.chunk(text, { source: 'test' });
  
  assert(chunks.length === 1, '短文本应该只生成一个块');
  assert(chunks[0].content === text, '块内容应该与原文相同');
});

// ============ 测试 3: 引用管理 ============
console.log('\n📦 测试: 引用管理\n');

test('CitationManager 应该为结果添加引用', () => {
  const manager = new CitationManager();
  const results = [
    { content: '内容1', score: 0.9 },
    { content: '内容2', score: 0.8 },
    { content: '内容3', score: 0.7 }
  ];
  
  const cited = manager.addCitations(results);
  
  assert(cited[0].citation === '[1]', '第一个结果应该有引用 [1]');
  assert(cited[1].citation === '[2]', '第二个结果应该有引用 [2]');
  assert(cited[2].citation === '[3]', '第三个结果应该有引用 [3]');
});

test('CitationManager 应该生成 RAG 提示词', () => {
  const manager = new CitationManager();
  const query = '测试查询';
  const results = [
    { content: '相关内容1', score: 0.9, citation: '[1]' },
    { content: '相关内容2', score: 0.8, citation: '[2]' }
  ];
  
  const ragResult = manager.generateRAGPrompt(query, results);
  
  assert(ragResult.context, '应该有上下文');
  assert(ragResult.prompt, '应该有提示词');
  assert(ragResult.prompt.includes(query), '提示词应该包含查询');
  assert(ragResult.prompt.includes('[1]'), '提示词应该包含引用');
});

// ============ 测试 4: RRF 融合 ============
console.log('\n📦 测试: RRF 融合\n');

test('RRFFusion 应该正确融合两组结果', () => {
  const rrf = new RRFFusion({ k: 60 });
  
  const vectorResults = [
    { id: 'a', content: '结果A', score: 0.9 },
    { id: 'b', content: '结果B', score: 0.8 },
    { id: 'c', content: '结果C', score: 0.7 }
  ];
  
  const keywordResults = [
    { id: 'b', content: '结果B', score: 0.95 },
    { id: 'd', content: '结果D', score: 0.85 },
    { id: 'a', content: '结果A', score: 0.75 }
  ];
  
  const fused = rrf.fuseTwo(vectorResults, keywordResults, { limit: 5 });
  
  assert(fused.length > 0, '应该返回融合结果');
  assert(fused.length <= 5, '结果数量应该不超过限制');
});

// ============ 测试 5: Xenova 嵌入提供者基础功能 ============
console.log('\n📦 测试: Xenova 嵌入提供者基础功能\n');

test('XenovaEmbedding 应该正确初始化', () => {
  const provider = new XenovaEmbedding({ modelName: 'Xenova/all-MiniLM-L6-v2' });
  assert(provider.name === 'xenova', '提供者名称应该是 xenova');
  assert(provider.dimensions === 384, 'all-MiniLM-L6-v2 应该是 384 维');
  assert(provider.initialized === false, '初始状态应该是未初始化');
});

test('XenovaEmbedding 应该返回支持的模型列表', () => {
  const models = XenovaEmbedding.getSupportedModels();
  assert(Array.isArray(models), '应该返回数组');
  assert(models.length > 0, '应该至少有一个模型');
  assert(models[0].name, '模型应该有名称');
  assert(models[0].dimensions, '模型应该有维度信息');
});

// ============ 测试 6: 错误处理 ============
console.log('\n📦 测试: 错误处理\n');

test('createEmbeddingProvider 应该对未知的提供者抛出错误', () => {
  try {
    createEmbeddingProvider('unknown');
    assert(false, '应该抛出错误');
  } catch (error) {
    assert(error.message.includes('未知'), '错误消息应该包含"未知"');
  }
});

// ============ 测试 7: OpenAI 可选依赖处理 ============
console.log('\n📦 测试: OpenAI 可选依赖处理\n');

test('getAvailableProviders 应该正确标记 OpenAI 可用性', () => {
  const providers = getAvailableProviders();
  // OpenAI 可能是可用或不可用，取决于是否安装了 openai 模块
  assert(providers.openai, '应该包含 openai 提供者信息');
  assert(typeof providers.openai.available === 'boolean', 'available 应该是布尔值');
  
  if (!providers.openai.available) {
    assert(providers.openai.description.includes('未安装'), '不可用时应该有提示信息');
  }
});

// 输出结果
console.log('\n' + '='.repeat(50));
console.log(`📊 测试结果: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}

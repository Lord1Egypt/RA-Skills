/**
 * RAG 3.0 单元测试
 * 测试各个独立模块
 */

import assert from 'assert';
import { ChunkingStrategy } from '../src/core/ChunkingStrategy.js';
import { CitationManager } from '../src/core/CitationManager.js';
import { RRFFusion } from '../src/search/RRFFusion.js';
import { BM25Search } from '../src/search/BM25Search.js';

// 测试计数
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}: ${error.message}`);
    failed++;
  }
}

async function testAsync(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}: ${error.message}`);
    failed++;
  }
}

console.log('🧪 RAG 3.0 单元测试\n');

// ========== ChunkingStrategy 测试 ==========
console.log('\n📦 ChunkingStrategy 测试');

test('固定大小分块', () => {
  const chunker = new ChunkingStrategy({ 
    chunkSize: 100, 
    overlap: 10, 
    strategy: 'fixed' 
  });
  const text = 'a'.repeat(250);
  const chunks = chunker.chunk(text);
  assert(chunks.length >= 2, '应该分成多个块');
  assert(chunks[0].content.length <= 100, '每个块应该不超过 chunkSize');
});

test('递归分块', () => {
  const chunker = new ChunkingStrategy({ 
    chunkSize: 100, 
    overlap: 10, 
    strategy: 'recursive' 
  });
  const text = '第一段。\n\n第二段。\n\n第三段内容更长一些。';
  const chunks = chunker.chunk(text);
  assert(chunks.length > 0, '应该至少有一个块');
  assert(chunks[0].metadata.chunkIndex === 0, '应该有正确的索引');
});

test('语义分块', () => {
  const chunker = new ChunkingStrategy({ 
    chunkSize: 100, 
    strategy: 'semantic' 
  });
  const text = '段落一。\n\n段落二。\n\n段落三。';
  const chunks = chunker.chunk(text);
  assert(chunks.length > 0, '应该至少有一个块');
});

test('分块元数据', () => {
  const chunker = new ChunkingStrategy({ chunkSize: 50 });
  const text = '这是一个测试文本，用于验证分块功能是否正常工作。';
  const chunks = chunker.chunk(text, { source: 'test', title: '测试' });
  assert(chunks[0].metadata.source === 'test', '应该保留元数据');
  assert(chunks[0].metadata.title === '测试', '应该保留标题');
  assert(chunks[0].id, '应该有唯一 ID');
});

test('分块统计', () => {
  const chunker = new ChunkingStrategy({ chunkSize: 50 });
  const text = '短文本。';
  const chunks = chunker.chunk(text);
  const stats = chunker.getStats(chunks);
  assert(stats.totalChunks === chunks.length, '统计应该匹配');
  assert(stats.avgChunkSize > 0, '平均大小应该大于 0');
});

// ========== CitationManager 测试 ==========
console.log('\n📦 CitationManager 测试');

test('添加引用', () => {
  const cm = new CitationManager({ format: 'numbered' });
  const results = [
    { id: '1', content: '内容1', metadata: { title: '来源1' } },
    { id: '2', content: '内容2', metadata: { title: '来源2' } }
  ];
  const cited = cm.addCitations(results);
  assert(cited[0].citation.number === 1, '第一个引用应该是 [1]');
  assert(cited[1].citation.number === 2, '第二个引用应该是 [2]');
  assert(cited[0].citation.mark === '[1]', '引用标记应该是 [1]');
});

test('生成上下文', () => {
  const cm = new CitationManager();
  const results = [
    { id: '1', content: '这是内容1', citation: { mark: '[1]' } },
    { id: '2', content: '这是内容2', citation: { mark: '[2]' } }
  ];
  const context = cm.generateContext(results);
  assert(context.includes('[1]'), '上下文应该包含引用标记');
  assert(context.includes('这是内容1'), '上下文应该包含内容');
});

test('生成引用列表', () => {
  const cm = new CitationManager();
  const results = [
    { 
      id: '1', 
      content: '内容1',
      citation: {
        mark: '[1]',
        source: { title: '来源1', url: 'http://example.com/1' }
      }
    }
  ];
  const list = cm.generateCitationList(results);
  assert(list.includes('[1]'), '列表应该包含引用标记');
  assert(list.includes('来源1'), '列表应该包含来源标题');
});

test('验证引用完整性', () => {
  const cm = new CitationManager();
  const validResults = [
    { id: '1', citation: { number: 1, source: {} } }
  ];
  const validation = cm.validateCitations(validResults);
  assert(validation.valid === true, '有效引用应该通过验证');

  const invalidResults = [
    { id: '1' }  // 缺少 citation
  ];
  const invalidValidation = cm.validateCitations(invalidResults);
  assert(invalidValidation.valid === false, '无效引用应该不通过验证');
});

test('去重引用', () => {
  const cm = new CitationManager();
  const results = [
    { id: '1', content: '内容1', score: 0.5 },
    { id: '1', content: '内容1', score: 0.8 },  // 重复
    { id: '2', content: '内容2', score: 0.6 }
  ];
  const deduped = cm.deduplicateCitations(results);
  assert(deduped.length === 2, '去重后应该只有 2 个');
});

// ========== RRFFusion 测试 ==========
console.log('\n📦 RRFFusion 测试');

test('RRF 融合两个列表', () => {
  const rrf = new RRFFusion({ k: 60 });
  const vectorResults = [
    { id: 'a', score: 0.9 },
    { id: 'b', score: 0.8 },
    { id: 'c', score: 0.7 }
  ];
  const keywordResults = [
    { id: 'b', score: 0.95 },
    { id: 'a', score: 0.85 },
    { id: 'd', score: 0.75 }
  ];
  const fused = rrf.fuseTwo(vectorResults, keywordResults, { limit: 10 });
  assert(fused.length > 0, '应该有融合结果');
  assert(fused[0].rrfScore > 0, '应该有 RRF 分数');
});

test('RRF 单列表返回', () => {
  const rrf = new RRFFusion({ k: 60 });
  const singleList = [
    { id: 'a', score: 0.9 },
    { id: 'b', score: 0.8 }
  ];
  const fused = rrf.fuse([singleList], { limit: 10 });
  assert(fused.length === 2, '应该返回所有结果');
});

test('RRF 空列表处理', () => {
  const rrf = new RRFFusion({ k: 60 });
  const fused = rrf.fuse([], { limit: 10 });
  assert(fused.length === 0, '空列表应该返回空结果');
});

test('RRF 权重融合', () => {
  const rrf = new RRFFusion({ k: 60 });
  const list1 = [{ id: 'a', score: 0.9 }];
  const list2 = [{ id: 'b', score: 0.8 }];
  const fused = rrf.fuseWeighted([list1, list2], [2.0, 1.0], { limit: 10 });
  assert(fused.length > 0, '应该有结果');
});

// ========== BM25Search 测试 ==========
console.log('\n📦 BM25Search 测试');

await testAsync('BM25 添加文档', async () => {
  const bm25 = new BM25Search({ k1: 1.5, b: 0.75 });
  await bm25.addDocument({
    id: '1',
    content: '人工智能是计算机科学的一个分支',
    metadata: { title: 'AI介绍' }
  });
  assert(bm25.totalDocs === 1, '应该有一个文档');
});

await testAsync('BM25 搜索', async () => {
  const bm25 = new BM25Search();
  await bm25.addDocuments([
    { id: '1', content: '人工智能是计算机科学的一个分支', metadata: {} },
    { id: '2', content: '机器学习是人工智能的子领域', metadata: {} },
    { id: '3', content: '深度学习是机器学习的一种方法', metadata: {} }
  ]);
  const results = await bm25.search('人工智能', { limit: 5 });
  assert(results.length > 0, '应该返回搜索结果');
  assert(results[0].score > 0, '应该有 BM25 分数');
});

await testAsync('BM25 中文分词', async () => {
  const bm25 = new BM25Search();
  const tokens = await bm25.tokenize('自然语言处理是人工智能的重要方向');
  assert(tokens.length > 0, '应该分词成功');
  assert(!tokens.includes('的'), '应该去除停用词');
});

await testAsync('BM25 统计信息', async () => {
  const bm25 = new BM25Search();
  await bm25.addDocuments([
    { id: '1', content: '测试文档一', metadata: {} },
    { id: '2', content: '测试文档二', metadata: {} }
  ]);
  const stats = bm25.getStats();
  assert(stats.totalDocs === 2, '应该有 2 个文档');
  assert(stats.vocabularySize > 0, '应该有词汇表');
});

// ========== 测试总结 ==========
console.log('\n' + '='.repeat(50));
console.log(`测试结果: ${passed} 通过, ${failed} 失败`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}

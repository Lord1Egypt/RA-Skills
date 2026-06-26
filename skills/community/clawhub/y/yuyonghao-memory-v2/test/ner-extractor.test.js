/**
 * NERExtractor 测试
 */

import NERExtractor from '../src/ner-extractor.js';
import GraphStore from '../src/graph-store.js';
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_DB_PATH = path.join(__dirname, '../test-ner-db');

describe('NERExtractor', () => {
  let extractor;
  let graphStore;

  before(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }

    // 初始化组件
    graphStore = new GraphStore({
      dbPath: TEST_DB_PATH
    });
    await graphStore.initialize();

    extractor = new NERExtractor({
      model: 'Xenova/bert-base-chinese-ner'
    });
    await extractor.initialize();
  });

  after(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  it('should initialize successfully', () => {
    assert(extractor.initialized === true);
    assert(extractor.ner !== null);
  });

  it('should extract entities from Chinese text', async () => {
    const text = '张三住在上海，他是阿里巴巴的员工。';
    const entities = await extractor.extract(text);

    // 应该有实体
    assert(entities.length > 0);
    
    // 检查实体类型
    const types = entities.map(e => e.type);
    assert(types.includes('PERSON') || types.includes('LOCATION') || types.includes('ORGANIZATION'));
  });

  it('should extract batch', async () => {
    const texts = [
      '张三在北京工作',
      '李四住在上海'
    ];

    const results = await extractor.extractBatch(texts);
    assert(results.length === 2);
    assert(Array.isArray(results[0]));
    assert(Array.isArray(results[1]));
  });

  it('should link entities to graph', async () => {
    const text = '张三住在上海';
    const entities = await extractor.extractAndLink(text, graphStore);

    // 应该有链接的实体
    assert(entities.length > 0);
    
    // 检查是否创建了节点
    for (const entity of entities) {
      assert(entity.linkedId !== undefined);
      assert(entity.isNew === true || entity.isNew === false);
      
      // 验证节点存在
      const node = graphStore.getNode(entity.linkedId);
      assert(node !== null);
    }
  });

  it('should not duplicate entities', async () => {
    // 第一次提取
    await extractor.extractAndLink('张三住在上海', graphStore);
    const stats1 = graphStore.getStats();
    
    // 第二次提取相同实体
    await extractor.extractAndLink('张三喜欢上海', graphStore);
    const stats2 = graphStore.getStats();
    
    // 节点数应该不变（没有重复创建）
    assert(stats2.nodeCount === stats1.nodeCount);
  });

  it('should handle empty text', async () => {
    const entities = await extractor.extract('');
    assert(entities.length === 0);
  });

  it('should handle text without entities', async () => {
    const entities = await extractor.extract('这是一个普通的句子，没有特定的人名或地名。');
    // 可能有一些误判，但数量应该很少
    assert(entities.length <= 2);
  });
});

console.log('NERExtractor tests completed');

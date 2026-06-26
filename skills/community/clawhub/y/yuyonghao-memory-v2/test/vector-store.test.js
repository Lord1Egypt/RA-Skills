/**
 * VectorStore 测试
 */

import VectorStore from '../src/vector-store.js';
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_DB_PATH = path.join(__dirname, '../test-db');

describe('VectorStore', () => {
  let store;

  before(async () => {
    // 清理测试数据库
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  after(async () => {
    // 清理测试数据库
    try {
      await store.close();
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  it('should initialize successfully', async () => {
    store = new VectorStore({
      dbPath: TEST_DB_PATH,
      embedModel: 'Xenova/all-MiniLM-L6-v2', // 轻量模型，测试更快
      cacheSize: 100
    });

    await store.initialize();
    assert(store.initialized === true);
  });

  it('should add memory', async () => {
    await store.addMemory({
      id: 'test_001',
      content: '这是一个测试记忆',
      metadata: { type: 'test' }
    });

    const memory = await store.getMemory('test_001');
    assert(memory !== null);
    assert(memory.content === '这是一个测试记忆');
  });

  it('should search by semantic similarity', async () => {
    // 添加更多测试记忆
    await store.addMemory({
      id: 'test_002',
      content: '上海是中国最大的城市',
      metadata: { type: 'test' }
    });

    await store.addMemory({
      id: 'test_003',
      content: '北京是中国的首都',
      metadata: { type: 'test' }
    });

    // 搜索
    const results = await store.search('中国城市', 2);
    
    assert(results.length > 0);
    assert(results[0].id === 'test_002'); // 最相关
  });

  it('should update memory', async () => {
    await store.updateMemory('test_001', {
      content: '这是更新后的测试记忆'
    });

    const memory = await store.getMemory('test_001');
    assert(memory.content === '这是更新后的测试记忆');
  });

  it('should delete memory', async () => {
    await store.deleteMemory('test_001');
    
    const memory = await store.getMemory('test_001');
    assert(memory === null);
  });

  it('should batch add memories', async () => {
    const memories = [
      { id: 'batch_001', content: '批量测试 1' },
      { id: 'batch_002', content: '批量测试 2' },
      { id: 'batch_003', content: '批量测试 3' }
    ];

    await store.addMemories(memories);
    
    const stats = await store.getStats();
    assert(stats.totalMemories >= 3);
  });

  it('should get stats', async () => {
    const stats = await store.getStats();
    
    assert(typeof stats.totalMemories === 'number');
    assert(typeof stats.cacheSize === 'number');
  });

  it('should clear all memories', async () => {
    await store.clear();
    
    const stats = await store.getStats();
    assert(stats.totalMemories === 0);
  });
});

console.log('VectorStore tests completed');

/**
 * MemoryManager 测试
 */

import MemoryManager from '../src/memory-manager.js';
import VectorStore from '../src/vector-store.js';
import GraphStore from '../src/graph-store.js';
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_DB_PATH = path.join(__dirname, '../test-manager-db');

describe('MemoryManager', () => {
  let manager;
  let vectorStore;
  let graphStore;

  before(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }

    // 初始化组件
    vectorStore = new VectorStore({
      dbPath: path.join(TEST_DB_PATH, 'vector'),
      embedModel: 'Xenova/all-MiniLM-L6-v2'
    });
    await vectorStore.initialize();

    graphStore = new GraphStore({
      dbPath: path.join(TEST_DB_PATH, 'graph')
    });
    await graphStore.initialize();

    manager = new MemoryManager({
      vectorStore,
      graphStore,
      forgetThreshold: 0.3
    });
  });

  after(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  it('should calculate memory score', async () => {
    // 添加测试记忆
    await vectorStore.addMemory({
      id: 'test_score_001',
      content: '测试记忆内容',
      metadata: {
        createdAt: new Date().toISOString(),
        importance: 0.8
      }
    });

    const memory = await vectorStore.getMemory('test_score_001');
    const score = manager.calculateScore(memory);
    
    assert(typeof score === 'number');
    assert(score >= 0 && score <= 1);
  });

  it('should record access', () => {
    manager.recordAccess('test_access_001');
    manager.recordAccess('test_access_001');
    manager.recordAccess('test_access_001');

    const count = manager.accessCounts.get('test_access_001');
    assert(count === 3);
  });

  it('should get stats', async () => {
    const stats = await manager.getStats();
    
    assert(typeof stats.vector.totalMemories === 'number');
    assert(typeof stats.graph.nodeCount === 'number');
    assert(typeof stats.memory.total === 'number');
    assert(typeof stats.memory.avgScore === 'string');
  });

  it('should cleanup access counts', () => {
    // 添加大量访问记录
    for (let i = 0; i < 1100; i++) {
      manager.recordAccess(`access_${i}`);
    }

    assert(manager.accessCounts.size > 1000);

    // 清理
    manager.cleanupAccessCounts(1000);

    assert(manager.accessCounts.size <= 1000);
  });

  it('should compress memory content', async () => {
    const longContent = '这是一个很长的记忆内容，需要被压缩成摘要。'.repeat(10);
    
    // 没有 LLM 时使用简单截断
    const summary = await manager.compressMemory(longContent);
    
    assert(summary.length < longContent.length);
    assert(summary.includes('...'));
  });

  it('should forget low priority memories', async () => {
    // 添加一些记忆
    await vectorStore.addMemory({
      id: 'low_priority_001',
      content: '低优先级记忆',
      metadata: {
        createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 60).toISOString(), // 60 天前
        importance: 0.1
      }
    });

    await vectorStore.addMemory({
      id: 'high_priority_001',
      content: '高优先级记忆',
      metadata: {
        createdAt: new Date().toISOString(),
        importance: 0.9
      }
    });

    // 运行遗忘
    const stats = await manager.forgetLowPriorityMemories();
    
    assert(stats.totalMemories >= 2);
    assert(typeof stats.compressed === 'number');
    assert(typeof stats.archived === 'number');
  });
});

console.log('MemoryManager tests completed');

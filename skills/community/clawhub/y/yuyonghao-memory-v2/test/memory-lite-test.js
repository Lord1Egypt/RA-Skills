/**
 * Memory V2 Lite - 简化版测试
 * 仅测试 GraphStore（不依赖 HuggingFace 模型）
 */

import { GraphStore } from '../src/graph-store.js';
import { MemoryManager } from '../src/memory-manager.js';

// 测试运行器
class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('🧪 Memory V2 Lite Test Suite Starting...\n');
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✓ ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    return this.failed === 0;
  }
}

const runner = new TestRunner();

// === GraphStore Tests ===
runner.test('GraphStore - should initialize', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  if (!store.initialized) throw new Error('Failed to initialize');
});

runner.test('GraphStore - should add node', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  const node = store.addNode('person_1', 'Person', { name: 'John Doe', age: 30 });
  
  if (!node || node.id !== 'person_1') throw new Error('Failed to add node');
  await store.save();
});

runner.test('GraphStore - should get node', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  const node = await store.getNode('person_1');
  if (!node || node.name !== 'John Doe') throw new Error('Failed to get node');
});

runner.test('GraphStore - should add edge', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  // 添加第二个节点
  store.addNode('person_2', 'Person', { name: 'Jane Doe' });
  
  // 添加关系
  const edge = store.addEdge('person_1', 'person_2', 'knows', { since: '2020' });
  
  if (!edge) throw new Error('Failed to add edge');
  await store.save();
});

runner.test('GraphStore - should get neighbors', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  const neighbors = await store.getNeighbors('person_1');
  if (!neighbors || neighbors.length === 0) throw new Error('Should have neighbors');
  if (neighbors[0].to !== 'person_2') throw new Error('Wrong neighbor');
});

runner.test('GraphStore - should search nodes', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  const results = await store.searchNodes({ type: 'Person' });
  if (!results || results.length < 2) throw new Error('Should find Person nodes');
});

runner.test('GraphStore - should get stats', async () => {
  const store = new GraphStore({
    dbPath: './test-graph-db'
  });
  await store.initialize();
  
  const stats = await store.getStats();
  if (stats.nodeCount < 2) throw new Error('Should have at least 2 nodes');
  if (stats.edgeCount < 1) throw new Error('Should have at least 1 edge');
});

// === MemoryManager Tests (简化版) ===
runner.test('MemoryManager - should initialize', async () => {
  const manager = new MemoryManager({
    graphPath: './test-graph-db'
  });
  await manager.initialize();
  if (!manager.initialized) throw new Error('Failed to initialize');
});

runner.test('MemoryManager - should add memory', async () => {
  const manager = new MemoryManager({
    graphPath: './test-graph-db'
  });
  await manager.initialize();
  
  const memory = await manager.addMemory({
    content: 'Test memory content',
    type: 'fact',
    importance: 0.8
  });
  
  if (!memory || !memory.id) throw new Error('Failed to add memory');
});

runner.test('MemoryManager - should search memories', async () => {
  const manager = new MemoryManager({
    graphPath: './test-graph-db'
  });
  await manager.initialize();
  
  const results = await manager.search('test');
  if (!results || results.length === 0) throw new Error('Should find memories');
});

// 清理测试数据
runner.test('Cleanup - should clear test data', async () => {
  const fs = await import('fs/promises');
  try {
    await fs.rm('./test-graph-db', { recursive: true });
  } catch (e) {
    // 忽略错误
  }
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});

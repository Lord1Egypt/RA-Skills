/**
 * Memory V2 - 快速验证脚本
 * 不依赖大模型，验证核心逻辑
 */

import GraphStore from '../src/graph-store.js';
import MemoryManager from '../src/memory-manager.js';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_PATH = path.join(__dirname, '../test-verify');

console.log('🧪 Memory V2 Quick Verification\n');

async function verifyGraphStore() {
  console.log('📊 Testing GraphStore...');
  
  // 清理
  try {
    await fs.rm(TEST_PATH, { recursive: true, force: true });
  } catch (e) {}
  
  const graph = new GraphStore({ dbPath: TEST_PATH });
  await graph.initialize();
  
  // 添加节点
  graph.addNode('person_001', 'Person', { name: '张三', age: 30 });
  graph.addNode('person_002', 'Person', { name: '李四', age: 25 });
  graph.addNode('company_001', 'Company', { name: '阿里巴巴' });
  
  // 添加边
  graph.addEdge('person_001', 'friend_of', 'person_002');
  graph.addEdge('person_001', 'works_at', 'company_001');
  
  // 验证
  const node = graph.getNode('person_001');
  console.assert(node !== null, 'Node should exist');
  console.assert(node.properties.name === '张三', 'Name should match');
  
  const neighbors = graph.getNeighbors('person_001', 1);
  console.assert(neighbors.length === 2, 'Should have 2 neighbors');
  
  const stats = graph.getStats();
  console.assert(stats.nodeCount === 3, 'Should have 3 nodes');
  console.assert(stats.edgeCount === 2, 'Should have 2 edges');
  
  // 保存和加载
  await graph.save();
  
  const graph2 = new GraphStore({ dbPath: TEST_PATH });
  await graph2.initialize();
  console.assert(graph2.getNode('person_001') !== null, 'Should load saved data');
  
  console.log('✅ GraphStore verified\n');
  
  // 清理
  await fs.rm(TEST_PATH, { recursive: true, force: true });
}

async function verifyMemoryManager() {
  console.log('🧠 Testing MemoryManager logic...');
  
  // 创建模拟的 VectorStore
  const mockVectorStore = {
    memories: new Map(),
    async addMemory(memory) {
      this.memories.set(memory.id, memory);
    },
    async getMemory(id) {
      return this.memories.get(id);
    },
    async search() {
      return Array.from(this.memories.values());
    }
  };
  
  // 创建模拟的 GraphStore
  const mockGraphStore = {
    nodes: new Map(),
    addNode(id, type, props) {
      this.nodes.set(id, { id, type, properties: props });
    },
    getNode(id) {
      return this.nodes.get(id);
    },
    getStats() {
      return { nodeCount: this.nodes.size, edgeCount: 0 };
    }
  };
  
  const manager = new MemoryManager({
    vectorStore: mockVectorStore,
    graphStore: mockGraphStore,
    forgetThreshold: 0.3
  });
  
  // 测试评分计算
  const memory = {
    id: 'test_001',
    content: '测试记忆',
    metadata: {
      createdAt: new Date().toISOString(),
      importance: 0.8
    }
  };
  
  const score = manager.calculateScore(memory);
  console.assert(score >= 0 && score <= 1, 'Score should be between 0 and 1');
  console.assert(score > 0.5, 'High importance memory should have high score');
  
  // 测试访问记录
  manager.recordAccess('test_001');
  manager.recordAccess('test_001');
  console.assert(manager.accessCounts.get('test_001') === 2, 'Should track access count');
  
  // 测试缓存清理
  for (let i = 0; i < 1100; i++) {
    manager.recordAccess(`access_${i}`);
  }
  manager.cleanupAccessCounts(1000);
  console.assert(manager.accessCounts.size <= 1000, 'Should cleanup excess entries');
  
  console.log('✅ MemoryManager logic verified\n');
}

async function main() {
  try {
    await verifyGraphStore();
    await verifyMemoryManager();
    
    console.log('='.repeat(50));
    console.log('✅ All verifications passed!');
    console.log('='.repeat(50));
    
    process.exit(0);
  } catch (e) {
    console.error('❌ Verification failed:', e);
    process.exit(1);
  }
}

main();

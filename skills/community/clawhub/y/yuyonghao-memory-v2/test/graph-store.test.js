/**
 * GraphStore 测试
 */

import GraphStore from '../src/graph-store.js';
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_DB_PATH = path.join(__dirname, '../test-graph-db');

describe('GraphStore', () => {
  let store;

  before(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  after(async () => {
    // 清理测试目录
    try {
      await store.close();
      await fs.rm(TEST_DB_PATH, { recursive: true, force: true });
    } catch (e) {
      // 忽略
    }
  });

  it('should initialize successfully', async () => {
    store = new GraphStore({
      dbPath: TEST_DB_PATH
    });

    await store.initialize();
    assert(store.initialized === true);
  });

  it('should add node', () => {
    const node = store.addNode('person_001', 'Person', {
      name: '张三',
      age: 30
    });

    assert(node.id === 'person_001');
    assert(node.type === 'Person');
    assert(node.properties.name === '张三');
    
    const retrieved = store.getNode('person_001');
    assert(retrieved !== null);
  });

  it('should update node', () => {
    store.updateNode('person_001', {
      properties: { age: 31 }
    });

    const node = store.getNode('person_001');
    assert(node.properties.age === 31);
  });

  it('should add edge', () => {
    // 添加第二个节点
    store.addNode('person_002', 'Person', {
      name: '李四',
      age: 25
    });

    // 添加关系
    store.addEdge('person_001', 'friend_of', 'person_002');
    
    const relations = store.getRelations('person_001', 'person_002');
    assert(relations.includes('friend_of'));
  });

  it('should get neighbors', () => {
    // 添加第三个节点
    store.addNode('person_003', 'Person', {
      name: '王五',
      age: 28
    });

    // person_001 -> person_003
    store.addEdge('person_001', 'colleague_of', 'person_003');

    // 获取 1 跳邻居
    const neighbors = store.getNeighbors('person_001', 1);
    assert(neighbors.length >= 2);
    
    const names = neighbors.map(n => n.properties.name);
    assert(names.includes('李四'));
    assert(names.includes('王五'));
  });

  it('should search nodes', () => {
    const results = store.searchNodes({
      type: 'Person',
      text: '张'
    });

    assert(results.length > 0);
    assert(results[0].properties.name.includes('张'));
  });

  it('should get stats', () => {
    const stats = store.getStats();
    
    assert(stats.nodeCount >= 3);
    assert(stats.edgeCount >= 2);
    assert(stats.nodeTypes.Person >= 3);
  });

  it('should save and load', async () => {
    await store.save();
    
    // 创建新实例并加载
    const newStore = new GraphStore({
      dbPath: TEST_DB_PATH
    });
    
    await newStore.initialize();
    
    // 验证数据已加载
    const node = newStore.getNode('person_001');
    assert(node !== null);
    assert(node.properties.name === '张三');
  });

  it('should delete node', () => {
    store.addNode('temp_001', 'Temp', { name: '临时' });
    store.deleteNode('temp_001');
    
    const node = store.getNode('temp_001');
    assert(node === null);
  });

  it('should clear all', async () => {
    await store.clear();
    
    const stats = store.getStats();
    assert(stats.nodeCount === 0);
    assert(stats.edgeCount === 0);
  });
});

console.log('GraphStore tests completed');

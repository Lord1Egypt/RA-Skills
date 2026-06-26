/**
 * Memory V2 - 统一记忆系统
 * 整合向量存储、知识图谱、实体提取、记忆管理
 */

import VectorStore from './vector-store.js';
import GraphStore from './graph-store.js';
import NERExtractor from './ner-extractor.js';
import MemoryManager from './memory-manager.js';
import { EventEmitter } from 'events';

/**
 * 记忆系统主类
 */
export class MemorySystem extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.dbPath - 数据库路径
   * @param {string} config.embedModel - 嵌入模型
   * @param {string} config.nerModel - NER 模型
   * @param {Object} config.llm - LLM 接口
   */
  constructor(config = {}) {
    super();
    
    // 1. 向量存储
    this.vectorStore = new VectorStore({
      dbPath: config.dbPath || './vector-db',
      embedModel: config.embedModel,
      cacheSize: config.cacheSize
    });
    
    // 2. 知识图谱
    this.graphStore = new GraphStore({
      dbPath: config.graphPath || './memory/ontology'
    });
    
    // 3. 实体提取
    this.nerExtractor = new NERExtractor({
      model: config.nerModel
    });
    
    // 4. 记忆管理
    this.memoryManager = new MemoryManager({
      vectorStore: this.vectorStore,
      graphStore: this.graphStore,
      llm: config.llm,
      forgetThreshold: config.forgetThreshold
    });
    
    this.initialized = false;
  }

  /**
   * 初始化所有组件
   */
  async initialize() {
    if (this.initialized) {
      return;
    }

    this.emit('initializing');
    console.log('[MemorySystem] Initializing...');

    // 并行初始化
    await Promise.all([
      this.vectorStore.initialize(),
      this.graphStore.initialize(),
      this.nerExtractor.initialize()
    ]);

    this.initialized = true;
    console.log('[MemorySystem] Initialized');
    this.emit('initialized');
  }

  /**
   * 添加记忆（自动提取实体）
   * @param {Object} memory
   * @param {string} memory.id - 记忆 ID
   * @param {string} memory.content - 记忆内容
   * @param {Object} memory.metadata - 元数据
   */
  async addMemory(memory) {
    if (!this.initialized) {
      await this.initialize();
    }

    // 1. 添加到向量存储
    await this.vectorStore.addMemory(memory);

    // 2. 提取实体
    const entities = await this.nerExtractor.extractAndLink(
      memory.content,
      this.graphStore
    );

    // 3. 创建实体 - 记忆关系
    for (const entity of entities) {
      this.graphStore.addEdge(entity.linkedId, 'mentioned_in', memory.id);
      this.graphStore.addEdge(memory.id, 'mentions', entity.linkedId);
    }

    // 4. 保存图谱
    await this.graphStore.save();

    this.emit('memory-added', memory);
    return { memory, entities };
  }

  /**
   * 语义搜索记忆
   * @param {string} query - 查询文本
   * @param {number} topK - 返回数量
   * @returns {Promise<Array>}
   */
  async search(query, topK = 10) {
    if (!this.initialized) {
      await this.initialize();
    }

    // 记录访问
    const results = await this.vectorStore.search(query, topK);
    for (const result of results) {
      this.memoryManager.recordAccess(result.id);
    }

    return results;
  }

  /**
   * 获取记忆详情（包含图谱关联）
   * @param {string} id - 记忆 ID
   * @returns {Promise<Object>}
   */
  async getMemory(id) {
    if (!this.initialized) {
      await this.initialize();
    }

    const memory = await this.vectorStore.getMemory(id);
    if (!memory) {
      return null;
    }

    // 获取关联实体
    const relatedEntities = this.graphStore.getNeighbors(id, 1);

    return {
      ...memory,
      relatedEntities
    };
  }

  /**
   * 删除记忆
   * @param {string} id - 记忆 ID
   */
  async deleteMemory(id) {
    if (!this.initialized) {
      await this.initialize();
    }

    await this.vectorStore.deleteMemory(id);
    this.graphStore.deleteNode(id);
    await this.graphStore.save();

    this.emit('memory-deleted', { id });
  }

  /**
   * 运行记忆管理（遗忘、压缩）
   */
  async runMaintenance() {
    if (!this.initialized) {
      await this.initialize();
    }

    return await this.memoryManager.forgetLowPriorityMemories();
  }

  /**
   * 获取系统统计
   * @returns {Promise<Object>}
   */
  async getStats() {
    if (!this.initialized) {
      await this.initialize();
    }

    return await this.memoryManager.getStats();
  }

  /**
   * 关闭系统
   */
  async close() {
    await this.vectorStore.close();
    await this.graphStore.close();
    this.initialized = false;
    this.emit('closed');
  }
}

export default MemorySystem;

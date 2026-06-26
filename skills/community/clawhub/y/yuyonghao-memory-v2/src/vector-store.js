/**
 * Memory V2 - 向量存储模块
 * 基于 LanceDB + Transformers.js 实现语义记忆存储和检索
 */

import lancedb from '@lancedb/lancedb';
import { pipeline } from '@xenova/transformers';
import { EventEmitter } from 'events';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 向量存储类
 */
export class VectorStore extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.dbPath - 数据库路径
   * @param {string} config.embedModel - 嵌入模型名称
   * @param {number} config.cacheSize - 缓存大小
   */
  constructor(config = {}) {
    super();
    this.dbPath = config.dbPath || path.join(__dirname, '../../vector-db');
    this.embedModelName = config.embedModel || 'Xenova/bge-large-zh-v1.5';
    this.cacheSize = config.cacheSize || 1000;
    
    this.db = null;
    this.collection = null;
    this.embedder = null;
    this.cache = new Map();
    this.initialized = false;
  }

  /**
   * 初始化数据库和嵌入模型
   */
  async initialize() {
    if (this.initialized) {
      return;
    }

    this.emit('initializing');

    // 1. 连接 LanceDB
    console.log(`[VectorStore] Connecting to LanceDB at ${this.dbPath}`);
    this.db = await lancedb.connect(this.dbPath);

    // 2. 创建或打开集合
    const tableName = 'memories';
    const existingTables = await this.db.tableNames();
    
    if (existingTables.includes(tableName)) {
      this.collection = await this.db.openTable(tableName);
      console.log('[VectorStore] Opened existing collection');
    } else {
      // 创建新集合（需要提供初始数据和 schema）
      const initialData = [{
        id: 'init',
        vector: new Array(1024).fill(0), // BGE-large-zh 输出维度
        content: 'initialization',
        metadata: { createdAt: new Date().toISOString() }
      }];
      this.collection = await this.db.createTable(tableName, initialData);
      console.log('[VectorStore] Created new collection');
      
      // 删除初始化数据
      await this.collection.delete("id = 'init'");
    }

    // 3. 加载嵌入模型
    console.log(`[VectorStore] Loading embedding model: ${this.embedModelName}`);
    this.embedder = await pipeline('feature-extraction', this.embedModelName);
    console.log('[VectorStore] Embedding model loaded');

    this.initialized = true;
    this.emit('initialized');
  }

  /**
   * 生成文本嵌入（带缓存）
   * @param {string} text - 输入文本
   * @returns {Promise<Float32Array>} - 嵌入向量
   */
  async embed(text) {
    if (!this.embedder) {
      throw new Error('Embedder not initialized. Call initialize() first.');
    }

    // 检查缓存
    const hash = this.hash(text);
    if (this.cache.has(hash)) {
      return this.cache.get(hash);
    }

    // 生成嵌入
    const output = await this.embedder(text, {
      pooling: 'mean',
      normalize: true
    });

    const embedding = output.data;

    // 缓存结果（LRU）
    if (this.cache.size >= this.cacheSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(hash, embedding);

    return embedding;
  }

  /**
   * 添加记忆到向量库
   * @param {Object} memory - 记忆对象
   * @param {string} memory.id - 记忆 ID
   * @param {string} memory.content - 记忆内容
   * @param {Object} memory.metadata - 元数据
   * @returns {Promise<void>}
   */
  async addMemory(memory) {
    if (!this.initialized) {
      await this.initialize();
    }

    const { id, content, metadata = {} } = memory;

    // 生成嵌入
    const embedding = await this.embed(content);

    // 添加到集合
    await this.collection.add([{
      id,
      vector: Array.from(embedding),
      content,
      metadata: {
        ...metadata,
        createdAt: metadata.createdAt || new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    }]);

    this.emit('memory-added', { id });
  }

  /**
   * 批量添加记忆
   * @param {Array<Object>} memories - 记忆数组
   * @returns {Promise<void>}
   */
  async addMemories(memories) {
    if (!this.initialized) {
      await this.initialize();
    }

    const batch = [];
    for (const memory of memories) {
      const embedding = await this.embed(memory.content);
      batch.push({
        id: memory.id,
        vector: Array.from(embedding),
        content: memory.content,
        metadata: {
          ...memory.metadata,
          createdAt: memory.metadata.createdAt || new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      });
    }

    await this.collection.add(batch);
    this.emit('memories-batch-added', { count: memories.length });
  }

  /**
   * 语义搜索
   * @param {string} query - 查询文本
   * @param {number} topK - 返回数量
   * @returns {Promise<Array>} - 搜索结果
   */
  async search(query, topK = 10) {
    if (!this.initialized) {
      await this.initialize();
    }

    // 生成查询嵌入
    const queryEmbed = await this.embed(query);

    // 向量搜索
    const results = await this.collection
      .search(Array.from(queryEmbed))
      .limit(topK)
      .execute();

    return results.map(r => ({
      id: r.id,
      content: r.content,
      metadata: r.metadata,
      score: r.score || r._distance
    }));
  }

  /**
   * 获取单个记忆
   * @param {string} id - 记忆 ID
   * @returns {Promise<Object|null>}
   */
  async getMemory(id) {
    if (!this.initialized) {
      await this.initialize();
    }

    const results = await this.collection
      .filter(`id = '${id}'`)
      .execute();

    return results.length > 0 ? results[0] : null;
  }

  /**
   * 删除记忆
   * @param {string} id - 记忆 ID
   * @returns {Promise<void>}
   */
  async deleteMemory(id) {
    if (!this.initialized) {
      await this.initialize();
    }

    await this.collection.delete(`id = '${id}'`);
    this.emit('memory-deleted', { id });
  }

  /**
   * 更新记忆
   * @param {string} id - 记忆 ID
   * @param {Object} updates - 更新内容
   * @returns {Promise<void>}
   */
  async updateMemory(id, updates) {
    if (!this.initialized) {
      await this.initialize();
    }

    const memory = await this.getMemory(id);
    if (!memory) {
      throw new Error(`Memory ${id} not found`);
    }

    const updatedContent = updates.content || memory.content;
    const updatedMetadata = {
      ...memory.metadata,
      ...updates.metadata,
      updatedAt: new Date().toISOString()
    };

    // 如果内容改变，重新生成嵌入
    if (updates.content) {
      const embedding = await this.embed(updatedContent);
      await this.deleteMemory(id);
      await this.addMemory({
        id,
        content: updatedContent,
        metadata: updatedMetadata
      });
    } else {
      // 只更新元数据（需要删除后重新添加）
      await this.deleteMemory(id);
      await this.addMemory({
        id,
        content: memory.content,
        metadata: updatedMetadata
      });
    }

    this.emit('memory-updated', { id });
  }

  /**
   * 清空所有记忆
   * @returns {Promise<void>}
   */
  async clear() {
    if (!this.initialized) {
      await this.initialize();
    }

    // 删除并重建集合
    const tableName = 'memories';
    await this.db.dropTable(tableName);
    this.collection = await this.db.createTable(tableName, [], {
      embeddingDim: 1024
    });

    this.cache.clear();
    this.emit('cleared');
  }

  /**
   * 获取统计信息
   * @returns {Promise<Object>}
   */
  async getStats() {
    if (!this.initialized) {
      await this.initialize();
    }

    const count = await this.collection.countRows();
    const cacheSize = this.cache.size;

    return {
      totalMemories: count,
      cacheSize,
      cacheHitRate: this.cacheHitRate
    };
  }

  /**
   * 简单哈希函数
   */
  hash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }

  /**
   * 缓存命中率（只读属性）
   */
  get cacheHitRate() {
    // 实际实现需要跟踪访问次数
    return 0;
  }

  /**
   * 关闭数据库连接
   */
  async close() {
    if (this.db) {
      // LanceDB Node.js 目前没有 close API
      this.db = null;
    }
    this.initialized = false;
    this.emit('closed');
  }
}

export default VectorStore;

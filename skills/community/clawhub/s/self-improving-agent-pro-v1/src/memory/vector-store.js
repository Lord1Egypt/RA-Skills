/**
 * HeartFlow Vector Store v11.21.0
 * 
 * 纯 JS 内存向量存储 + brute-force 检索
 * 设计接口可切换后端 (ChromaDB/lanceDB 等)
 * 
 * 架构：
 *   embedder.js → vector-store.js → memory 系统
 * 
 * 当前实现：内存 Map + brute-force cosine similarity
 * 规模建议：<1000 记忆用内存，1000+ 切换 ChromaDB
 */

const path = require('path');
const fs = require('fs');

// ============================================================
// 配置
// ============================================================

const DEFAULT_CONFIG = {
  dimension: 1536,        // 向量维度 (与 embedder 一致)
  topK: 10,               // 默认返回数量
  threshold: 0.5,         // 相似度阈值
  metric: 'cosine',       // 'cosine' | 'euclidean' | 'dot'
  persistPath: null,       // 持久化路径 (可选)
};

// ============================================================
// 工具函数
// ============================================================

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    dot   += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-6);
}

function euclideanDistance(a, b) {
  let sum = 0;
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    sum += (a[i] - b[i]) ** 2;
  }
  return Math.sqrt(sum);
}

function dotProduct(a, b) {
  let sum = 0;
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    sum += a[i] * b[i];
  }
  return sum;
}

function getDistanceFunc(metric) {
  switch (metric) {
    case 'cosine':     return (a, b) => (cosineSimilarity(a, b) + 1) / 2; // 归一化到 [0,1]
    case 'euclidean':  return (a, b) => 1 / (1 + euclideanDistance(a, b)); // 归一化到 [0,1]
    case 'dot':        return (a, b) => (dotProduct(a, b) + 1) / 2; // 归一化到 [0,1]
    default:           return (a, b) => cosineSimilarity(a, b);
  }
}

// ============================================================
// 主类
// ============================================================

class VectorStore {
  /**
   * @param {object} options
   * @param {number} options.dimension - 向量维度
   * @param {string} options.metric - 'cosine' | 'euclidean' | 'dot'
   * @param {string} options.persistPath - 持久化文件路径
   */
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    this.dimension = this.config.dimension;
    this.metric = this.config.metric;
    this.distanceFn = getDistanceFunc(this.config.metric);
    
    // 存储: id → { embedding, metadata }
    this._vectors = new Map();
    
    // 索引: 加速批量操作
    this._count = 0;
    
    // 统计
    this._stats = {
      inserts: 0,
      searches: 0,
      hits: 0,
      misses: 0,
    };
    
    // 持久化
    this._persistPath = this.config.persistPath;
    if (this._persistPath) {
      this._ensureDir(path.dirname(this._persistPath));
    }
    
    // 加载已有数据
    if (this._persistPath && fs.existsSync(this._persistPath)) {
      this._load();
    }
  }

  // ============================================================
  // 核心 API
  // ============================================================

  /**
   * 添加向量
   * @param {string} id - 唯一 ID
   * @param {number[]} embedding - 向量
   * @param {object} metadata - 元数据 (content, source 等)
   */
  upsert(id, embedding, metadata = {}) {
    if (embedding.length !== this.dimension) {
      throw new Error(`Vector dimension mismatch: expected ${this.dimension}, got ${embedding.length}`);
    }
    
    this._vectors.set(id, { embedding: [...embedding], metadata });
    this._count = this._vectors.size;
    this._stats.inserts++;
    
    return this;
  }

  /**
   * 批量添加
   * @param {Array<{id, embedding, metadata}>} items
   */
  upsertBatch(items) {
    for (const item of items) {
      this.upsert(item.id, item.embedding, item.metadata || {});
    }
    return this;
  }

  /**
   * 删除向量
   */
  delete(id) {
    const existed = this._vectors.delete(id);
    this._count = this._vectors.size;
    return existed;
  }

  /**
   * 按前缀删除 (删除一组相关向量)
   */
  deleteByPrefix(prefix) {
    let count = 0;
    for (const [id] of this._vectors) {
      if (id.startsWith(prefix)) {
        this._vectors.delete(id);
        count++;
      }
    }
    this._count = this._vectors.size;
    return count;
  }

  /**
   * 搜索最相似的向量
   * @param {number[]} query - 查询向量
   * @param {number} topK - 返回数量
   * @param {number} threshold - 相似度阈值
   * @returns {Array<{id, score, metadata}>}
   */
  search(query, topK = this.config.topK, threshold = this.config.threshold) {
    if (query.length !== this.dimension) {
      throw new Error(`Query dimension mismatch: expected ${this.dimension}, got ${query.length}`);
    }
    
    this._stats.searches++;
    
    if (this._vectors.size === 0) {
      this._stats.misses++;
      return [];
    }
    
    const scored = [];
    
    for (const [id, { embedding, metadata }] of this._vectors) {
      const score = this.distanceFn(query, embedding);
      if (score >= threshold) {
        scored.push({ id, score, metadata });
      }
    }
    
    // 排序
    scored.sort((a, b) => b.score - a.score);
    
    const results = scored.slice(0, topK);
    
    if (results.length > 0) {
      this._stats.hits++;
    } else {
      this._stats.misses++;
    }
    
    return results;
  }

  /**
   * 获取单个向量
   */
  get(id) {
    const entry = this._vectors.get(id);
    if (!entry) return null;
    return { id, embedding: entry.embedding, metadata: entry.metadata };
  }

  /**
   * 获取所有向量 (用于调试)
   */
  getAll() {
    const result = [];
    for (const [id, { embedding, metadata }] of this._vectors) {
      result.push({ id, embedding, metadata });
    }
    return result;
  }

  /**
   * 清空所有向量
   */
  clear() {
    this._vectors.clear();
    this._count = 0;
    return this;
  }

  // ============================================================
  // 统计
  // ============================================================

  stats() {
    return {
      count: this._count,
      dimension: this.dimension,
      metric: this.metric,
      ...this._stats,
      hitRate: this._stats.searches > 0 
        ? (this._stats.hits / this._stats.searches).toFixed(3)
        : '0.000',
    };
  }

  // ============================================================
  // 持久化
  // ============================================================

  /**
   * 保存到磁盘
   */
  save() {
    if (!this._persistPath) return false;
    
    try {
      const data = {
        version: '1.0',
        dimension: this.dimension,
        metric: this.metric,
        vectors: [...this._vectors.entries()],
        stats: this._stats,
        savedAt: Date.now(),
      };
      
      fs.writeFileSync(this._persistPath, JSON.stringify(data), 'utf-8');
      return true;
    } catch (e) {
      console.error(`[VectorStore] Save failed: ${e.message}`);
      return false;
    }
  }

  /**
   * 从磁盘加载
   */
  _load() {
    try {
      const content = fs.readFileSync(this._persistPath, 'utf-8');
      const data = JSON.parse(content);
      
      if (data.version !== '1.0') {
        console.warn(`[VectorStore] Unknown data version: ${data.version}`);
      }
      
      this.dimension = data.dimension || this.dimension;
      this.metric = data.metric || this.metric;
      this.distanceFn = getDistanceFunc(this.metric);
      
      this._vectors = new Map(data.vectors || []);
      this._count = this._vectors.size;
      this._stats = { ...this._stats, ...data.stats };
      
      console.log(`[VectorStore] Loaded ${this._count} vectors from ${this._persistPath}`);
      return true;
    } catch (e) {
      console.error(`[VectorStore] Load failed: ${e.message}`);
      return false;
    }
  }

  // ============================================================
  // 工具
  // ============================================================

  _ensureDir(dir) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  /**
   * 获取向量维度
   */
  getDimension() {
    return this.dimension;
  }

  /**
   * 获取向量数量
   */
  size() {
    return this._count;
  }

  /**
   * 存在性检查
   */
  has(id) {
    return this._vectors.has(id);
  }

  /**
   * 批量存在性检查
   */
  hasMany(ids) {
    return ids.map(id => this._vectors.has(id));
  }

  /**
   * 获取指定 IDs 的向量
   */
  getMany(ids) {
    return ids.map(id => this.get(id)).filter(Boolean);
  }

  /**
   * 搜索所有匹配的向量 (不过滤 topK)
   */
  searchAll(query, threshold = this.config.threshold) {
    return this.search(query, this._count, threshold);
  }

  /**
   * 更新元数据
   */
  updateMetadata(id, metadata) {
    const entry = this._vectors.get(id);
    if (!entry) return false;
    entry.metadata = { ...entry.metadata, ...metadata };
    return true;
  }

  /**
   * 导出为普通对象 (用于调试)
   */
  toJSON() {
    return {
      dimension: this.dimension,
      metric: this.metric,
      count: this._count,
      vectors: this.getAll(),
      stats: this.stats(),
    };
  }
}

// ============================================================
// 工厂函数
// ============================================================

/**
 * 创建 VectorStore 实例
 * @param {object} options
 * @param {string} options.persistPath - 持久化路径
 * @param {number} options.dimension - 向量维度
 */
function createVectorStore(options = {}) {
  return new VectorStore(options);
}

// ============================================================
// 导出
// ============================================================

module.exports = {
  VectorStore,
  createVectorStore,
  cosineSimilarity,
  euclideanDistance,
  dotProduct,
};

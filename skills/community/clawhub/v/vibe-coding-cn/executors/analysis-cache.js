#!/usr/bin/env node

/**
 * 增量分析缓存管理器
 * 
 * 优化策略：
 * 1. 需求层缓存（相同需求变更直接返回）
 * 2. 分层缓存（需求层→架构层→文件层独立缓存）
 * 3. LRU 淘汰（保留最近使用的 N 条记录）
 * 4. 持久化（可选保存到磁盘）
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

/**
 * 缓存管理器
 */
class AnalysisCache {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 100;  // 最大缓存条目
    this.ttl = options.ttl || 3600000;      // 默认 1 小时过期
    this.persistPath = options.persistPath; // 持久化路径（可选）
    this.cache = new Map();
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0
    };
    
    // 加载持久化缓存
    if (this.persistPath) {
      this.loadFromDisk();
    }
  }
  
  /**
   * 生成缓存键
   */
  generateKey(oldReq, newReq, oldVersion) {
    const data = JSON.stringify({
      oldReq,
      newReq,
      files: oldVersion.files?.map(f => `${f.name}:${f.size}`).sort(),
      architecture: oldVersion.architecture
    });
    
    return crypto.createHash('sha256').update(data).digest('hex');
  }
  
  /**
   * 获取缓存
   */
  get(key) {
    const entry = this.cache.get(key);
    
    if (!entry) {
      this.stats.misses++;
      return null;
    }
    
    // 检查是否过期
    if (Date.now() - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      this.stats.evictions++;
      this.stats.misses++;
      return null;
    }
    
    this.stats.hits++;
    
    // 更新访问时间（LRU）
    entry.lastAccess = Date.now();
    this.cache.set(key, entry);
    
    return entry.data;
  }
  
  /**
   * 设置缓存
   */
  set(key, data, layer = 'full') {
    // 检查是否需要淘汰
    if (this.cache.size >= this.maxSize) {
      this.evictOldest();
    }
    
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      lastAccess: Date.now(),
      layer,
      accessCount: 0
    });
  }
  
  /**
   * 淘汰最旧的条目
   */
  evictOldest() {
    let oldestKey = null;
    let oldestTime = Infinity;
    
    for (const [key, entry] of this.cache.entries()) {
      if (entry.lastAccess < oldestTime) {
        oldestTime = entry.lastAccess;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      this.cache.delete(oldestKey);
      this.stats.evictions++;
    }
  }
  
  /**
   * 分层缓存 - 需求层
   */
  async getRequirementLayer(oldReq, newReq) {
    const key = this.generateKey(oldReq, newReq, { files: [], architecture: null });
    const layerKey = `${key}:requirement`;
    
    return this.get(layerKey);
  }
  
  async setRequirementLayer(oldReq, newReq, data) {
    const key = this.generateKey(oldReq, newReq, { files: [], architecture: null });
    const layerKey = `${key}:requirement`;
    
    this.set(layerKey, data, 'requirement');
  }
  
  /**
   * 分层缓存 - 架构层
   */
  async getArchitectureLayer(requirementAnalysis, architecture) {
    const key = crypto.createHash('sha256')
      .update(JSON.stringify({ requirementAnalysis, architecture }))
      .digest('hex');
    const layerKey = `${key}:architecture`;
    
    return this.get(layerKey);
  }
  
  async setArchitectureLayer(requirementAnalysis, architecture, data) {
    const key = crypto.createHash('sha256')
      .update(JSON.stringify({ requirementAnalysis, architecture }))
      .digest('hex');
    const layerKey = `${key}:architecture`;
    
    this.set(layerKey, data, 'architecture');
  }
  
  /**
   * 分层缓存 - 文件层
   */
  async getFileLayer(requirementAnalysis, architectureAnalysis, files) {
    const key = crypto.createHash('sha256')
      .update(JSON.stringify({
        requirementAnalysis,
        architectureAnalysis,
        files: files.map(f => `${f.name}:${f.size}`).sort()
      }))
      .digest('hex');
    const layerKey = `${key}:file`;
    
    return this.get(layerKey);
  }
  
  async setFileLayer(requirementAnalysis, architectureAnalysis, files, data) {
    const key = crypto.createHash('sha256')
      .update(JSON.stringify({
        requirementAnalysis,
        architectureAnalysis,
        files: files.map(f => `${f.name}:${f.size}`).sort()
      }))
      .digest('hex');
    const layerKey = `${key}:file`;
    
    this.set(layerKey, data, 'file');
  }
  
  /**
   * 完整分析缓存
   */
  async getFullAnalysis(oldReq, newReq, oldVersion) {
    const key = this.generateKey(oldReq, newReq, oldVersion);
    return this.get(key);
  }
  
  async setFullAnalysis(oldReq, newReq, oldVersion, data) {
    const key = this.generateKey(oldReq, newReq, oldVersion);
    this.set(key, data, 'full');
  }
  
  /**
   * 获取缓存命中率
   */
  getHitRate() {
    const total = this.stats.hits + this.stats.misses;
    return total > 0 ? (this.stats.hits / total * 100).toFixed(2) : 0;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hits: this.stats.hits,
      misses: this.stats.misses,
      evictions: this.stats.evictions,
      hitRate: `${this.getHitRate()}%`
    };
  }
  
  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.stats = { hits: 0, misses: 0, evictions: 0 };
  }
  
  /**
   * 保存到磁盘
   */
  async saveToDisk() {
    if (!this.persistPath) return;
    
    const data = {
      cache: Array.from(this.cache.entries()),
      stats: this.stats,
      timestamp: Date.now()
    };
    
    await fs.mkdir(path.dirname(this.persistPath), { recursive: true });
    await fs.writeFile(this.persistPath, JSON.stringify(data, null, 2));
  }
  
  /**
   * 从磁盘加载
   */
  async loadFromDisk() {
    try {
      const content = await fs.readFile(this.persistPath, 'utf-8');
      const data = JSON.parse(content);
      
      // 检查是否过期（超过 24 小时不加载）
      if (Date.now() - data.timestamp > 86400000) {
        console.log('[Cache] 磁盘缓存已过时，跳过加载');
        return;
      }
      
      this.cache = new Map(data.cache);
      this.stats = data.stats || { hits: 0, misses: 0, evictions: 0 };
      
      console.log(`[Cache] 从磁盘加载 ${this.cache.size} 条记录`);
    } catch (error) {
      console.log('[Cache] 磁盘缓存加载失败:', error.message);
    }
  }
  
  /**
   * 预热点分析
   */
  async warmup(commonPatterns) {
    console.log('[Cache] 预热点分析...');
    
    for (const pattern of commonPatterns) {
      const key = this.generateKey(pattern.oldReq, pattern.newReq, pattern.version);
      
      if (!this.cache.has(key)) {
        // 这里可以调用实际的 API 进行预热
        console.log(`  - 预热：${pattern.oldReq.substring(0, 20)}... → ${pattern.newReq.substring(0, 20)}...`);
      }
    }
  }
}

/**
 * 带缓存的增量更新分析器包装器
 */
class CachedIncrementalUpdater {
  constructor(updater, cacheOptions = {}) {
    this.updater = updater;
    this.cache = new AnalysisCache(cacheOptions);
  }
  
  /**
   * 分析变更（带缓存）
   */
  async analyzeChanges(oldReq, newReq, oldVersion) {
    console.log('[CachedUpdater] 分析需求变化...');
    const startTime = Date.now();
    
    // 1. 尝试完整缓存
    const cachedFull = await this.cache.getFullAnalysis(oldReq, newReq, oldVersion);
    if (cachedFull) {
      const duration = Date.now() - startTime;
      console.log(`[CachedUpdater] ✅ 缓存命中 (${duration}ms)`);
      return cachedFull;
    }
    
    // 2. 分层尝试缓存
    console.log('[CachedUpdater] 缓存未命中，开始分层分析...');
    
    // 需求层
    let requirementAnalysis = await this.cache.getRequirementLayer(oldReq, newReq);
    if (!requirementAnalysis) {
      console.log('  [1/3] 需求层分析（无缓存）...');
      requirementAnalysis = await this.updater.analyzeRequirementLayer(oldReq, newReq);
      await this.cache.setRequirementLayer(oldReq, newReq, requirementAnalysis);
    } else {
      console.log('  [1/3] 需求层分析（缓存命中）');
    }
    
    // 架构层
    let architectureAnalysis = await this.cache.getArchitectureLayer(
      requirementAnalysis,
      oldVersion.architecture
    );
    if (!architectureAnalysis) {
      console.log('  [2/3] 架构层分析（无缓存）...');
      architectureAnalysis = await this.updater.analyzeArchitectureLayer(
        requirementAnalysis,
        oldVersion.architecture
      );
      await this.cache.setArchitectureLayer(
        requirementAnalysis,
        oldVersion.architecture,
        architectureAnalysis
      );
    } else {
      console.log('  [2/3] 架构层分析（缓存命中）');
    }
    
    // 文件层
    let fileAnalysis = await this.cache.getFileLayer(
      requirementAnalysis,
      architectureAnalysis,
      oldVersion.files
    );
    if (!fileAnalysis) {
      console.log('  [3/3] 文件层分析（无缓存）...');
      fileAnalysis = await this.updater.analyzeFileLayer(
        requirementAnalysis,
        architectureAnalysis,
        oldVersion.files
      );
      await this.cache.setFileLayer(
        requirementAnalysis,
        architectureAnalysis,
        oldVersion.files,
        fileAnalysis
      );
    } else {
      console.log('  [3/3] 文件层分析（缓存命中）');
    }
    
    // 3. 整合结果
    const plan = await this.updater.generateUpdatePlan(
      requirementAnalysis,
      architectureAnalysis,
      fileAnalysis,
      oldVersion
    );
    
    // 4. 保存到完整缓存
    await this.cache.setFullAnalysis(oldReq, newReq, oldVersion, plan);
    
    const duration = Date.now() - startTime;
    console.log(`[CachedUpdater] 分析完成 (${duration}ms)`);
    console.log(`[CachedUpdater] 缓存统计：${JSON.stringify(this.cache.getStats())}`);
    
    return plan;
  }
  
  /**
   * 获取缓存统计
   */
  getCacheStats() {
    return this.cache.getStats();
  }
  
  /**
   * 清空缓存
   */
  clearCache() {
    this.cache.clear();
  }
  
  /**
   * 保存缓存到磁盘
   */
  async saveCache() {
    await this.cache.saveToDisk();
  }
}

// 导出
module.exports = { AnalysisCache, CachedIncrementalUpdater };

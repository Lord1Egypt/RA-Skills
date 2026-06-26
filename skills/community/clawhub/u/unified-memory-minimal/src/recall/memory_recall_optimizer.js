/**
 * Memory Recall Optimizer - 记忆召回优化器
 * 
 * 核心目标：让 AI 助手能快速、准确地找到相关记忆
 */

import { logger } from '../logger.js';

export class MemoryRecallOptimizer {
  constructor(options = {}) {
    this.options = {
      // 召回策略
      maxRecall: options.maxRecall || 10,          // 最多召回多少条
      minScore: options.minScore || 0.6,           // 最低分数阈值
      
      // 多路召回
      enableMultiPath: options.enableMultiPath !== false,
      vectorWeight: options.vectorWeight || 0.4,   // 向量搜索权重
      textWeight: options.textWeight || 0.3,       // 文本搜索权重
      contextWeight: options.contextWeight || 0.3, // 上下文权重
      
      // 时效性衰减
      enableTimeDecay: options.enableTimeDecay !== false,
      halfLife: options.halfLife || 30 * 24 * 3600000, // 30天半衰期
      
      // 重要性加权
      enableImportanceWeight: options.enableImportanceWeight !== false,
      
      // 去重
      enableDedup: options.enableDedup !== false,
      similarityThreshold: options.similarityThreshold || 0.85,
      
      ...options
    };
    
    // 召回统计
    this.stats = {
      totalRecalls: 0,
      avgRecallTime: 0,
      avgRecallCount: 0,
      cacheHits: 0
    };
    
    // 召回缓存
    this.recallCache = new Map();
    this.cacheMaxSize = 1000;
    
    logger.info('[MemoryRecallOptimizer] 召回优化器初始化完成');
  }
  
  /**
   * 优化召回 - 核心方法
   */
  async optimizeRecall(query, memories, context = {}) {
    const startTime = Date.now();
    
    logger.debug(`[MemoryRecallOptimizer] 优化召回: "${query}"`);
    
    // 1. 检查缓存
    const cacheKey = this.getCacheKey(query, context);
    if (this.recallCache.has(cacheKey)) {
      this.stats.cacheHits++;
      logger.debug('[MemoryRecallOptimizer] 命中缓存');
      return this.recallCache.get(cacheKey);
    }
    
    // 2. 多路召回
    let candidates = memories;
    
    if (this.options.enableMultiPath) {
      candidates = await this.multiPathRecall(query, memories, context);
    }
    
    // 3. 计算综合分数
    const scored = await this.computeScores(query, candidates, context);
    
    // 4. 过滤低分记忆
    const filtered = scored.filter(m => m.finalScore >= this.options.minScore);
    
    // 5. 时效性衰减
    const decayed = this.options.enableTimeDecay 
      ? this.applyTimeDecay(filtered)
      : filtered;
    
    // 6. 重要性加权
    const weighted = this.options.enableImportanceWeight
      ? this.applyImportanceWeight(decayed)
      : decayed;
    
    // 7. 排序
    const sorted = weighted.sort((a, b) => b.finalScore - a.finalScore);
    
    // 8. 去重
    const deduped = this.options.enableDedup
      ? this.deduplicate(sorted)
      : sorted;
    
    // 9. 截断
    const result = deduped.slice(0, this.options.maxRecall);
    
    // 10. 缓存结果
    this.cacheResult(cacheKey, result);
    
    // 更新统计
    const duration = Date.now() - startTime;
    this.updateStats(duration, result.length);
    
    logger.info(`[MemoryRecallOptimizer] 召回完成: ${result.length} 条记忆, 耗时 ${duration}ms`);
    
    return {
      memories: result,
      stats: {
        total: memories.length,
        candidates: candidates.length,
        filtered: filtered.length,
        returned: result.length,
        duration: duration
      }
    };
  }
  
  /**
   * 多路召回
   */
  async multiPathRecall(query, memories, context) {
    const paths = [];
    
    // 路径1: 向量相似度
    if (this.options.vectorWeight > 0) {
      const vectorResults = this.vectorRecall(query, memories);
      paths.push({
        name: 'vector',
        weight: this.options.vectorWeight,
        results: vectorResults
      });
    }
    
    // 路径2: 文本匹配
    if (this.options.textWeight > 0) {
      const textResults = this.textRecall(query, memories);
      paths.push({
        name: 'text',
        weight: this.options.textWeight,
        results: textResults
      });
    }
    
    // 路径3: 上下文匹配
    if (this.options.contextWeight > 0) {
      const contextResults = this.contextRecall(query, memories, context);
      paths.push({
        name: 'context',
        weight: this.options.contextWeight,
        results: contextResults
      });
    }
    
    // 融合多路结果
    return this.mergePaths(paths);
  }
  
  /**
   * 向量召回
   */
  vectorRecall(query, memories) {
    const results = [];
    
    for (const memory of memories) {
      if (memory.embedding && query.embedding) {
        const similarity = this.cosineSimilarity(query.embedding, memory.embedding);
        
        results.push({
          memory: memory,
          vectorScore: similarity,
          score: similarity
        });
      }
    }
    
    return results.sort((a, b) => b.score - a.score);
  }
  
  /**
   * 文本召回
   */
  textRecall(query, memories) {
    const results = [];
    const queryTerms = this.extractTerms(query.text || query);
    
    for (const memory of memories) {
      const memoryTerms = this.extractTerms(memory.text);
      
      // 计算 Jaccard 相似度
      const intersection = queryTerms.filter(t => memoryTerms.includes(t));
      const union = [...new Set([...queryTerms, ...memoryTerms])];
      
      const jaccardSimilarity = union.length > 0 
        ? intersection.length / union.length 
        : 0;
      
      // BM25 风格评分
      const bm25Score = this.computeBM25(queryTerms, memoryTerms, memories.length);
      
      results.push({
        memory: memory,
        textScore: Math.max(jaccardSimilarity, bm25Score),
        score: Math.max(jaccardSimilarity, bm25Score)
      });
    }
    
    return results.sort((a, b) => b.score - a.score);
  }
  
  /**
   * 上下文召回
   */
  contextRecall(query, memories, context) {
    const results = [];
    
    for (const memory of memories) {
      let contextScore = 0;
      
      // 用户匹配
      if (context.userId && memory.metadata?.userId === context.userId) {
        contextScore += 0.3;
      }
      
      // 会话匹配
      if (context.sessionId && memory.metadata?.sessionId === context.sessionId) {
        contextScore += 0.3;
      }
      
      // 类型匹配
      if (context.type && memory.type === context.type) {
        contextScore += 0.2;
      }
      
      // 时间接近性
      if (context.timestamp && memory.timestamp) {
        const timeDiff = Math.abs(context.timestamp - memory.timestamp);
        const hoursDiff = timeDiff / (1000 * 60 * 60);
        
        if (hoursDiff < 1) {
          contextScore += 0.2;
        } else if (hoursDiff < 24) {
          contextScore += 0.1;
        }
      }
      
      results.push({
        memory: memory,
        contextScore: contextScore,
        score: contextScore
      });
    }
    
    return results.sort((a, b) => b.score - a.score);
  }
  
  /**
   * 融合多路结果
   */
  mergePaths(paths) {
    const merged = new Map();
    
    for (const path of paths) {
      for (const result of path.results) {
        const memoryId = result.memory.id;
        
        if (!merged.has(memoryId)) {
          merged.set(memoryId, {
            memory: result.memory,
            vectorScore: 0,
            textScore: 0,
            contextScore: 0,
            pathCount: 0
          });
        }
        
        const entry = merged.get(memoryId);
        
        if (result.vectorScore !== undefined) {
          entry.vectorScore = Math.max(entry.vectorScore, result.vectorScore);
        }
        if (result.textScore !== undefined) {
          entry.textScore = Math.max(entry.textScore, result.textScore);
        }
        if (result.contextScore !== undefined) {
          entry.contextScore = Math.max(entry.contextScore, result.contextScore);
        }
        
        entry.pathCount++;
      }
    }
    
    return Array.from(merged.values());
  }
  
  /**
   * 计算综合分数
   */
  async computeScores(query, candidates, context) {
    const scored = [];
    
    for (const candidate of candidates) {
      // 加权平均
      const weightedScore = 
        candidate.vectorScore * this.options.vectorWeight +
        candidate.textScore * this.options.textWeight +
        candidate.contextScore * this.options.contextWeight;
      
      // 路径数加成（出现在多个路径中的记忆更重要）
      const pathBonus = Math.min(candidate.pathCount * 0.1, 0.3);
      
      const finalScore = Math.min(weightedScore + pathBonus, 1.0);
      
      scored.push({
        ...candidate,
        finalScore: finalScore,
        originalScore: weightedScore
      });
    }
    
    return scored;
  }
  
  /**
   * 应用时效性衰减
   */
  applyTimeDecay(memories) {
    const now = Date.now();
    const halfLife = this.options.halfLife;
    
    return memories.map(m => {
      const age = now - (m.memory.timestamp || now);
      const decayFactor = Math.pow(0.5, age / halfLife);
      
      return {
        ...m,
        finalScore: m.finalScore * (0.5 + 0.5 * decayFactor),
        decayFactor: decayFactor
      };
    });
  }
  
  /**
   * 应用重要性加权
   */
  applyImportanceWeight(memories) {
    return memories.map(m => {
      const importance = m.memory.importance || 0.5;
      const weightFactor = 0.7 + 0.6 * importance; // 0.7-1.3
      
      return {
        ...m,
        finalScore: m.finalScore * weightFactor,
        importanceFactor: weightFactor
      };
    });
  }
  
  /**
   * 去重
   */
  deduplicate(memories) {
    const deduped = [];
    const seen = new Set();
    
    for (const m of memories) {
      const key = m.memory.id || m.memory.text.substring(0, 50);
      
      if (!seen.has(key)) {
        seen.add(key);
        deduped.push(m);
      }
    }
    
    return deduped;
  }
  
  /**
   * 提取术语
   */
  extractTerms(text) {
    if (!text) return [];
    
    return text.toLowerCase()
      .replace(/[^\w\s\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(term => term.length > 1);
  }
  
  /**
   * 计算 BM25 分数
   */
  computeBM25(queryTerms, docTerms, totalDocs, avgDocLen = 100) {
    const k1 = 1.5;
    const b = 0.75;
    
    const docLen = docTerms.length;
    const termFreqs = {};
    
    for (const term of docTerms) {
      termFreqs[term] = (termFreqs[term] || 0) + 1;
    }
    
    let score = 0;
    
    for (const term of queryTerms) {
      const tf = termFreqs[term] || 0;
      if (tf === 0) continue;
      
      // 简化的 IDF
      const idf = Math.log((totalDocs + 1) / (tf + 0.5));
      
      // BM25 公式
      const numerator = tf * (k1 + 1);
      const denominator = tf + k1 * (1 - b + b * (docLen / avgDocLen));
      
      score += idf * (numerator / denominator);
    }
    
    return Math.min(score / 10, 1.0); // 归一化
  }
  
  /**
   * 计算余弦相似度
   */
  cosineSimilarity(vec1, vec2) {
    if (!vec1 || !vec2 || vec1.length !== vec2.length) {
      return 0;
    }
    
    let dotProduct = 0;
    let norm1 = 0;
    let norm2 = 0;
    
    for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
      norm1 += vec1[i] * vec1[i];
      norm2 += vec2[i] * vec2[i];
    }
    
    if (norm1 === 0 || norm2 === 0) {
      return 0;
    }
    
    return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }
  
  /**
   * 获取缓存键
   */
  getCacheKey(query, context) {
    const queryText = typeof query === 'string' ? query : query.text;
    const contextStr = JSON.stringify({
      userId: context.userId,
      type: context.type
    });
    
    return `${queryText}:${contextStr}`;
  }
  
  /**
   * 缓存结果
   */
  cacheResult(key, result) {
    if (this.recallCache.size >= this.cacheMaxSize) {
      // 删除最旧的缓存
      const firstKey = this.recallCache.keys().next().value;
      this.recallCache.delete(firstKey);
    }
    
    this.recallCache.set(key, result);
  }
  
  /**
   * 更新统计
   */
  updateStats(duration, count) {
    this.stats.totalRecalls++;
    
    // 移动平均
    const alpha = 0.1;
    this.stats.avgRecallTime = 
      this.stats.avgRecallTime * (1 - alpha) + duration * alpha;
    this.stats.avgRecallCount = 
      this.stats.avgRecallCount * (1 - alpha) + count * alpha;
  }
  
  /**
   * 获取统计
   */
  getStats() {
    return { ...this.stats };
  }
  
  /**
   * 清理缓存
   */
  clearCache() {
    const cleared = this.recallCache.size;
    this.recallCache.clear();
    
    logger.info(`[MemoryRecallOptimizer] 清理缓存: ${cleared} 条`);
    
    return cleared;
  }
}

// 导出单例
let optimizerInstance = null;

export function getMemoryRecallOptimizer(options = {}) {
  if (!optimizerInstance) {
    optimizerInstance = new MemoryRecallOptimizer(options);
  }
  return optimizerInstance;
}

export default MemoryRecallOptimizer;

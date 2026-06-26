/**
 * Token优化模块
 * 
 * 负责：
 * 1. 优化token使用，减少不必要的模型调用
 * 2. 管理响应缓存
 * 3. 控制思考深度
 * 4. 监控token消耗
 */

class Optimizer {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.cache = new Map();
    this.stats = {
      totalTokens: 0,
      savedTokens: 0,
      cacheHits: 0,
      cacheMisses: 0,
      thinkingCalls: 0,
      templateResponses: 0
    };
  }

  /**
   * 优化分析结果
   * @param {Object} analysis - 分析结果
   */
  async optimize(analysis) {
    try {
      const optimized = { ...analysis };
      
      // 检查是否需要思考
      if (optimized.requiresThinking) {
        optimized.requiresThinking = this.shouldThink(optimized);
        
        if (!optimized.requiresThinking) {
          this.stats.savedTokens += 100; // 估计节省的token
          this.logger.debug('跳过思考调用', { intent: optimized.intent });
        }
      }
      
      // 检查缓存
      if (this.config.cache_enabled) {
        const cached = this.checkCache(optimized);
        if (cached) {
          optimized.cachedResponse = cached;
          optimized.useCache = true;
        }
      }
      
      // 限制token使用
      optimized.maxTokens = this.config.max_tokens_per_check || 1000;
      
      this.stats.totalTokens += this.estimateTokenUsage(optimized);
      
      this.logger.debug('优化完成', {
        requiresThinking: optimized.requiresThinking,
        useCache: optimized.useCache || false,
        estimatedTokens: this.estimateTokenUsage(optimized)
      });
      
      return optimized;
    } catch (error) {
      this.logger.error('优化失败', { error: error.message });
      return analysis; // 返回原始分析结果
    }
  }

  /**
   * 判断是否需要思考
   * @param {Object} analysis - 分析结果
   */
  shouldThink(analysis) {
    // 检查思考阈值
    const thinkingThreshold = this.config.thinking_threshold || 0.7;
    
    // 计算复杂度分数
    const complexityScore = this.calculateComplexityScore(analysis);
    
    // 如果复杂度低于阈值，使用模板响应
    if (complexityScore < thinkingThreshold) {
      this.stats.templateResponses++;
      return false;
    }
    
    this.stats.thinkingCalls++;
    return true;
  }

  /**
   * 计算复杂度分数
   * @param {Object} analysis - 分析结果
   */
  calculateComplexityScore(analysis) {
    let score = 0;
    
    // 基于意图的分数
    const intentScores = {
      question: 0.8,
      task_request: 0.9,
      feedback: 0.3,
      social: 0.1,
      unknown: 0.5
    };
    
    score += intentScores[analysis.intent] || 0.5;
    
    // 基于优先级的分数
    const priorityScores = {
      p0: 0.9,
      p1: 0.7,
      p2: 0.4,
      p3: 0.2
    };
    
    score += priorityScores[analysis.priority] || 0.5;
    
    // 基于时间的分数（等待时间越长，可能需要更深入思考）
    if (analysis.details?.timeSince > 300) { // 超过5分钟
      score += 0.2;
    }
    
    // 基于历史长度的分数
    if (analysis.details?.historyLength > 30) {
      score += 0.1;
    }
    
    return Math.min(score, 1.0);
  }

  /**
   * 检查缓存
   * @param {Object} analysis - 分析结果
   */
  checkCache(analysis) {
    if (!this.config.cache_enabled) {
      return null;
    }
    
    const cacheKey = this.generateCacheKey(analysis);
    const cachedItem = this.cache.get(cacheKey);
    
    if (cachedItem) {
      // 检查缓存是否过期
      const now = Date.now();
      const ttl = (this.config.cache_ttl || 3600) * 1000; // 转换为毫秒
      
      if (now - cachedItem.timestamp < ttl) {
        this.stats.cacheHits++;
        this.logger.debug('缓存命中', { cacheKey });
        return cachedItem.data;
      } else {
        // 缓存过期，删除
        this.cache.delete(cacheKey);
        this.logger.debug('缓存过期', { cacheKey });
      }
    }
    
    this.stats.cacheMisses++;
    return null;
  }

  /**
   * 生成缓存键
   * @param {Object} analysis - 分析结果
   */
  generateCacheKey(analysis) {
    const keyParts = [
      analysis.intent,
      analysis.priority,
      analysis.details?.lastSpeaker || 'unknown',
      Math.floor(analysis.details?.timeSince / 60) // 按分钟分组
    ];
    
    return keyParts.join('|');
  }

  /**
   * 添加缓存
   * @param {Object} analysis - 分析结果
   * @param {Object} response - 响应数据
   */
  addToCache(analysis, response) {
    if (!this.config.cache_enabled) {
      return;
    }
    
    const cacheKey = this.generateCacheKey(analysis);
    const cacheItem = {
      data: response,
      timestamp: Date.now()
    };
    
    this.cache.set(cacheKey, cacheItem);
    
    // 限制缓存大小
    if (this.cache.size > 1000) {
      this.cleanupCache();
    }
    
    this.logger.debug('添加到缓存', { cacheKey });
  }

  /**
   * 清理缓存
   */
  cleanupCache() {
    const maxSize = 1000;
    if (this.cache.size <= maxSize) {
      return;
    }
    
    // 按时间排序，删除最旧的
    const entries = Array.from(this.cache.entries());
    entries.sort((a, b) => a[1].timestamp - b[1].timestamp);
    
    const toRemove = entries.slice(0, entries.length - maxSize);
    toRemove.forEach(([key]) => this.cache.delete(key));
    
    this.logger.debug('清理缓存', { 
      removed: toRemove.length, 
      remaining: this.cache.size 
    });
  }

  /**
   * 估计token使用量
   * @param {Object} analysis - 分析结果
   */
  estimateTokenUsage(analysis) {
    let tokens = 0;
    
    // 基础token
    tokens += 50;
    
    // 根据意图增加
    if (analysis.intent === 'question' || analysis.intent === 'task_request') {
      tokens += 100;
    }
    
    // 如果需要思考，增加token
    if (analysis.requiresThinking) {
      tokens += 500;
    }
    
    // 如果有历史上下文
    if (analysis.details?.historyLength > 10) {
      tokens += Math.min(analysis.details.historyLength * 10, 1000);
    }
    
    return Math.min(tokens, this.config.max_tokens_per_check || 1000);
  }

  /**
   * 获取优化统计数据
   */
  getStats() {
    const cacheHitRate = this.stats.cacheHits + this.stats.cacheMisses > 0 
      ? (this.stats.cacheHits / (this.stats.cacheHits + this.stats.cacheMisses)) * 100 
      : 0;
    
    const thinkingRate = this.stats.thinkingCalls + this.stats.templateResponses > 0
      ? (this.stats.thinkingCalls / (this.stats.thinkingCalls + this.stats.templateResponses)) * 100
      : 0;
    
    return {
      ...this.stats,
      cacheHitRate: cacheHitRate.toFixed(1) + '%',
      thinkingRate: thinkingRate.toFixed(1) + '%',
      tokensPerMinute: this.calculateTokensPerMinute()
    };
  }

  /**
   * 计算每分钟token使用量
   */
  calculateTokensPerMinute() {
    const now = Date.now();
    const startTime = this.stats.startTime || now;
    const minutes = (now - startTime) / 60000;
    
    return minutes > 0 ? Math.round(this.stats.totalTokens / minutes) : 0;
  }

  /**
   * 重置统计数据
   */
  resetStats() {
    this.stats = {
      totalTokens: 0,
      savedTokens: 0,
      cacheHits: 0,
      cacheMisses: 0,
      thinkingCalls: 0,
      templateResponses: 0,
      startTime: Date.now()
    };
    
    this.logger.info('优化器统计数据已重置');
  }

  /**
   * 获取优化建议
   */
  getOptimizationSuggestions() {
    const suggestions = [];
    
    // 缓存建议
    const cacheHitRate = this.stats.cacheHits + this.stats.cacheMisses > 0 
      ? (this.stats.cacheHits / (this.stats.cacheHits + this.stats.cacheMisses)) * 100 
      : 0;
    
    if (cacheHitRate < 20) {
      suggestions.push({
        type: 'cache',
        message: '缓存命中率较低，建议增加缓存TTL或调整缓存策略',
        current: cacheHitRate.toFixed(1) + '%',
        target: '>30%'
      });
    }
    
    // 思考调用建议
    const thinkingRate = this.stats.thinkingCalls + this.stats.templateResponses > 0
      ? (this.stats.thinkingCalls / (this.stats.thinkingCalls + this.stats.templateResponses)) * 100
      : 0;
    
    if (thinkingRate > 80) {
      suggestions.push({
        type: 'thinking',
        message: '模型思考调用率过高，建议降低thinking_threshold',
        current: thinkingRate.toFixed(1) + '%',
        target: '<60%'
      });
    }
    
    // Token使用建议
    const tokensPerMinute = this.calculateTokensPerMinute();
    if (tokensPerMinute > 5000) {
      suggestions.push({
        type: 'tokens',
        message: 'Token使用率过高，建议优化响应长度或减少检查频率',
        current: tokensPerMinute + '/min',
        target: '<3000/min'
      });
    }
    
    return suggestions;
  }
}

module.exports = Optimizer;
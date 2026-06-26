/**
 * Smart Deduplication System - 智能去重系统
 * 借鉴 OpenViking 的 memory_deduplicator.py
 */

import { logger } from '../logger.js';
import { getMemoryTypeRegistry } from '../memory_types/registry.js';

export class SmartDeduplicator {
  constructor(options = {}) {
    this.options = {
      similarityThreshold: options.similarityThreshold || 0.85,
      semanticThreshold: options.semanticThreshold || 0.8,
      exactMatchThreshold: options.exactMatchThreshold || 1.0,
      timeWindow: options.timeWindow || 3600000, // 1小时
      enableSemanticDedup: options.enableSemanticDedup !== false,
      enableFuzzyMatch: options.enableFuzzyMatch !== false,
      enableContextualDedup: options.enableContextualDedup !== false,
      ...options
    };
    
    this.typeRegistry = getMemoryTypeRegistry();
    
    // 去重缓存
    this.dedupCache = new Map();
    this.maxCacheSize = 10000;
    
    // 统计信息
    this.stats = {
      totalChecked: 0,
      duplicatesFound: 0,
      merged: 0,
      skipped: 0,
      errors: 0
    };
    
    logger.info('[SmartDeduplicator] 智能去重系统初始化完成');
  }
  
  /**
   * 检查记忆是否重复
   */
  async checkDuplicate(memory, existingMemories = []) {
    this.stats.totalChecked++;
    
    const result = {
      isDuplicate: false,
      duplicateType: null,
      similarMemories: [],
      confidence: 0,
      action: 'keep' // keep, merge, skip
    };
    
    try {
      // 1. 精确匹配检查
      const exactMatch = await this.checkExactMatch(memory, existingMemories);
      if (exactMatch.isDuplicate) {
        result.isDuplicate = true;
        result.duplicateType = 'exact';
        result.similarMemories = exactMatch.matches;
        result.confidence = 1.0;
        result.action = 'skip';
        
        this.stats.duplicatesFound++;
        this.stats.skipped++;
        
        return result;
      }
      
      // 2. 语义相似度检查
      if (this.options.enableSemanticDedup) {
        const semanticMatch = await this.checkSemanticSimilarity(memory, existingMemories);
        if (semanticMatch.isDuplicate) {
          result.isDuplicate = true;
          result.duplicateType = 'semantic';
          result.similarMemories = semanticMatch.matches;
          result.confidence = semanticMatch.confidence;
          result.action = semanticMatch.shouldMerge ? 'merge' : 'keep';
          
          this.stats.duplicatesFound++;
          
          return result;
        }
      }
      
      // 3. 模糊匹配检查
      if (this.options.enableFuzzyMatch) {
        const fuzzyMatch = await this.checkFuzzyMatch(memory, existingMemories);
        if (fuzzyMatch.isDuplicate) {
          result.isDuplicate = true;
          result.duplicateType = 'fuzzy';
          result.similarMemories = fuzzyMatch.matches;
          result.confidence = fuzzyMatch.confidence;
          result.action = 'merge';
          
          this.stats.duplicatesFound++;
          
          return result;
        }
      }
      
      // 4. 上下文去重检查
      if (this.options.enableContextualDedup) {
        const contextualMatch = await this.checkContextualDuplicate(memory, existingMemories);
        if (contextualMatch.isDuplicate) {
          result.isDuplicate = true;
          result.duplicateType = 'contextual';
          result.similarMemories = contextualMatch.matches;
          result.confidence = contextualMatch.confidence;
          result.action = 'merge';
          
          this.stats.duplicatesFound++;
          
          return result;
        }
      }
      
      return result;
      
    } catch (error) {
      logger.error('[SmartDeduplicator] 去重检查失败:', error);
      this.stats.errors++;
      
      return {
        isDuplicate: false,
        error: error.message,
        action: 'keep'
      };
    }
  }
  
  /**
   * 精确匹配检查
   */
  async checkExactMatch(memory, existingMemories) {
    const result = {
      isDuplicate: false,
      matches: []
    };
    
    // 标准化文本
    const normalizedText = this.normalizeText(memory.text);
    
    for (const existing of existingMemories) {
      const existingNormalized = this.normalizeText(existing.text);
      
      // 完全匹配
      if (normalizedText === existingNormalized) {
        result.isDuplicate = true;
        result.matches.push({
          memory: existing,
          similarity: 1.0,
          matchType: 'exact'
        });
      }
    }
    
    return result;
  }
  
  /**
   * 语义相似度检查
   */
  async checkSemanticSimilarity(memory, existingMemories) {
    const result = {
      isDuplicate: false,
      matches: [],
      confidence: 0,
      shouldMerge: false
    };
    
    // 获取记忆类型的去重阈值
    const typeName = memory.type || 'facts';
    const threshold = this.typeRegistry.getDeduplicationThreshold(typeName);
    
    // 如果有向量，使用向量相似度
    if (memory.embedding && existingMemories.some(m => m.embedding)) {
      for (const existing of existingMemories) {
        if (!existing.embedding) continue;
        
        const similarity = this.cosineSimilarity(memory.embedding, existing.embedding);
        
        if (similarity >= threshold) {
          result.matches.push({
            memory: existing,
            similarity: similarity,
            matchType: 'semantic'
          });
        }
      }
    }
    
    // 如果没有向量，使用文本相似度
    if (result.matches.length === 0) {
      const memoryText = memory.text.toLowerCase();
      
      for (const existing of existingMemories) {
        const existingText = existing.text.toLowerCase();
        const similarity = this.textSimilarity(memoryText, existingText);
        
        if (similarity >= threshold) {
          result.matches.push({
            memory: existing,
            similarity: similarity,
            matchType: 'text_similarity'
          });
        }
      }
    }
    
    // 判断是否重复
    if (result.matches.length > 0) {
      result.isDuplicate = true;
      result.confidence = Math.max(...result.matches.map(m => m.similarity));
      
      // 如果相似度非常高，建议合并
      result.shouldMerge = result.confidence >= 0.9;
    }
    
    return result;
  }
  
  /**
   * 模糊匹配检查
   */
  async checkFuzzyMatch(memory, existingMemories) {
    const result = {
      isDuplicate: false,
      matches: [],
      confidence: 0
    };
    
    const threshold = this.options.similarityThreshold * 0.9; // 稍微降低阈值
    
    for (const existing of existingMemories) {
      const similarity = this.fuzzySimilarity(memory.text, existing.text);
      
      if (similarity >= threshold) {
        result.matches.push({
          memory: existing,
          similarity: similarity,
          matchType: 'fuzzy'
        });
      }
    }
    
    if (result.matches.length > 0) {
      result.isDuplicate = true;
      result.confidence = Math.max(...result.matches.map(m => m.similarity));
    }
    
    return result;
  }
  
  /**
   * 上下文去重检查
   */
  async checkContextualDuplicate(memory, existingMemories) {
    const result = {
      isDuplicate: false,
      matches: [],
      confidence: 0
    };
    
    // 检查时间窗口内的相似记忆
    const now = Date.now();
    const timeWindow = this.options.timeWindow;
    
    for (const existing of existingMemories) {
      const timeDiff = Math.abs((memory.timestamp || now) - (existing.timestamp || now));
      
      // 只检查时间窗口内的记忆
      if (timeDiff > timeWindow) {
        continue;
      }
      
      // 检查上下文相似性
      const contextSimilarity = this.contextSimilarity(memory, existing);
      
      if (contextSimilarity >= 0.7) {
        result.matches.push({
          memory: existing,
          similarity: contextSimilarity,
          matchType: 'contextual',
          timeDiff: timeDiff
        });
      }
    }
    
    if (result.matches.length > 0) {
      result.isDuplicate = true;
      result.confidence = Math.max(...result.matches.map(m => m.similarity));
    }
    
    return result;
  }
  
  /**
   * 合并相似记忆
   */
  async mergeMemories(memory1, memory2, strategy = 'intelligent') {
    this.stats.merged++;
    
    const typeName = memory1.type || memory2.type || 'facts';
    const type = this.typeRegistry.getType(typeName);
    
    // 根据合并策略处理
    switch (strategy) {
      case 'keep_new':
        return { ...memory2, mergedFrom: [memory1.id, memory2.id] };
        
      case 'keep_old':
        return { ...memory1, mergedFrom: [memory1.id, memory2.id] };
        
      case 'intelligent':
      default:
        // 使用类型特定的合并逻辑
        if (type.config.handler && type.config.handler.mergeSimilar) {
          return await type.config.handler.mergeSimilar(memory1, memory2);
        }
        
        // 默认合并逻辑
        return this.defaultMerge(memory1, memory2);
    }
  }
  
  /**
   * 默认合并逻辑
   */
  defaultMerge(memory1, memory2) {
    const merged = {
      id: `merged_${Date.now()}`,
      text: `${memory1.text}\n\n${memory2.text}`,
      type: memory1.type || memory2.type,
      importance: Math.max(memory1.importance || 0.5, memory2.importance || 0.5),
      timestamp: Math.max(memory1.timestamp || Date.now(), memory2.timestamp || Date.now()),
      mergedFrom: [memory1.id, memory2.id],
      mergedAt: Date.now(),
      metadata: {
        ...memory1.metadata,
        ...memory2.metadata
      }
    };
    
    // 合并提取信息
    if (memory1.extracted || memory2.extracted) {
      merged.extracted = {
        ...memory1.extracted,
        ...memory2.extracted
      };
    }
    
    return merged;
  }
  
  /**
   * 批量去重
   */
  async deduplicateBatch(memories) {
    const result = {
      unique: [],
      duplicates: [],
      merged: [],
      stats: {
        total: memories.length,
        unique: 0,
        duplicates: 0,
        merged: 0
      }
    };
    
    for (const memory of memories) {
      const dupCheck = await this.checkDuplicate(memory, result.unique);
      
      if (dupCheck.isDuplicate) {
        result.duplicates.push({
          memory: memory,
          duplicateOf: dupCheck.similarMemories[0].memory.id,
          type: dupCheck.duplicateType,
          confidence: dupCheck.confidence
        });
        
        result.stats.duplicates++;
        
        // 如果需要合并
        if (dupCheck.action === 'merge' && dupCheck.similarMemories.length > 0) {
          const merged = await this.mergeMemories(
            memory,
            dupCheck.similarMemories[0].memory
          );
          
          result.merged.push(merged);
          result.stats.merged++;
        }
      } else {
        result.unique.push(memory);
        result.stats.unique++;
      }
    }
    
    logger.info(`[SmartDeduplicator] 批量去重完成: ${result.stats.unique} 唯一, ${result.stats.duplicates} 重复, ${result.stats.merged} 合并`);
    
    return result;
  }
  
  /**
   * 标准化文本
   */
  normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[^\w\s\u4e00-\u9fa5]/g, '')
      .trim();
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
   * 文本相似度（基于编辑距离）
   */
  textSimilarity(text1, text2) {
    const len1 = text1.length;
    const len2 = text2.length;
    
    if (len1 === 0 || len2 === 0) {
      return 0;
    }
    
    // 使用 Levenshtein 距离
    const distance = this.levenshteinDistance(text1, text2);
    const maxLen = Math.max(len1, len2);
    
    return 1 - (distance / maxLen);
  }
  
  /**
   * Levenshtein 距离
   */
  levenshteinDistance(str1, str2) {
    const m = str1.length;
    const n = str2.length;
    
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
    
    for (let i = 0; i <= m; i++) {
      dp[i][0] = i;
    }
    
    for (let j = 0; j <= n; j++) {
      dp[0][j] = j;
    }
    
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (str1[i - 1] === str2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(
            dp[i - 1][j - 1] + 1,
            dp[i - 1][j] + 1,
            dp[i][j - 1] + 1
          );
        }
      }
    }
    
    return dp[m][n];
  }
  
  /**
   * 模糊相似度
   */
  fuzzySimilarity(text1, text2) {
    // 提取关键词
    const keywords1 = this.extractKeywords(text1);
    const keywords2 = this.extractKeywords(text2);
    
    // 计算关键词重叠
    const intersection = keywords1.filter(k => keywords2.includes(k));
    const union = [...new Set([...keywords1, ...keywords2])];
    
    if (union.length === 0) {
      return 0;
    }
    
    // Jaccard 相似度
    const jaccardSimilarity = intersection.length / union.length;
    
    // 考虑长度相似度
    const lengthSimilarity = 1 - Math.abs(text1.length - text2.length) / Math.max(text1.length, text2.length);
    
    // 综合相似度
    return jaccardSimilarity * 0.7 + lengthSimilarity * 0.3;
  }
  
  /**
   * 上下文相似度
   */
  contextSimilarity(memory1, memory2) {
    let similarity = 0;
    
    // 检查类型是否相同
    if (memory1.type === memory2.type) {
      similarity += 0.3;
    }
    
    // 检查用户是否相同
    if (memory1.metadata?.userId === memory2.metadata?.userId) {
      similarity += 0.2;
    }
    
    // 检查会话是否相同
    if (memory1.metadata?.sessionId === memory2.metadata?.sessionId) {
      similarity += 0.3;
    }
    
    // 检查来源是否相同
    if (memory1.metadata?.source === memory2.metadata?.source) {
      similarity += 0.2;
    }
    
    return similarity;
  }
  
  /**
   * 提取关键词
   */
  extractKeywords(text) {
    // 简单的关键词提取（实际应用中可以使用分词器）
    const words = text.toLowerCase()
      .replace(/[^\w\s\u4e00-\u9fa5]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 1);
    
    return [...new Set(words)];
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return { ...this.stats };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalChecked: 0,
      duplicatesFound: 0,
      merged: 0,
      skipped: 0,
      errors: 0
    };
    
    logger.info('[SmartDeduplicator] 统计已重置');
  }
  
  /**
   * 清理缓存
   */
  clearCache() {
    const cleared = this.dedupCache.size;
    this.dedupCache.clear();
    
    logger.info(`[SmartDeduplicator] 清理缓存: ${cleared} 条`);
    
    return cleared;
  }
}

// 导出单例
let deduplicatorInstance = null;

export function getSmartDeduplicator(options = {}) {
  if (!deduplicatorInstance) {
    deduplicatorInstance = new SmartDeduplicator(options);
  }
  return deduplicatorInstance;
}

export default SmartDeduplicator;
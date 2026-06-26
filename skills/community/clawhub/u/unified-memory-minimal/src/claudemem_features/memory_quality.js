/**
 * 记忆质量评估系统 - Claude-Mem 风格
 * 
 * 功能：
 * 1. 记忆质量评分
 * 2. 记忆健康度检查
 * 3. 记忆优化建议
 * 4. 批量质量评估
 */

import { logger } from '../utils/logger.js';

export class MemoryQuality {
  constructor(storage, vectorStore) {
    this.storage = storage;
    this.vectorStore = vectorStore;
    this.logger = logger.child({ module: 'memory_quality' });
  }

  /**
   * 评估单条记忆的质量
   * @param {string} memoryId - 记忆 ID
   * @returns {Promise<Object>} 质量评估结果
   */
  async assessMemory(memoryId) {
    try {
      const memory = await this.storage.findOne('memories', { _id: memoryId });
      
      if (!memory) {
        throw new Error(`Memory not found: ${memoryId}`);
      }
      
      // 多维度评估
      const dimensions = {
        content: await this.assessContent(memory),
        structure: await this.assessStructure(memory),
        utility: await this.assessUtility(memory),
        freshness: await this.assessFreshness(memory),
        uniqueness: await this.assessUniqueness(memory)
      };
      
      // 计算总体分数
      const overallScore = this.calculateOverallScore(dimensions);
      
      // 生成问题列表
      const issues = this.identifyIssues(dimensions);
      
      // 生成优化建议
      const suggestions = this.generateSuggestions(dimensions, issues);
      
      return {
        memoryId,
        overallScore,
        dimensions,
        issues,
        suggestions,
        assessedAt: new Date()
      };
      
    } catch (error) {
      this.logger.error('Failed to assess memory', { error, memoryId });
      throw error;
    }
  }

  /**
   * 评估内容质量
   * @param {Object} memory - 记忆对象
   * @returns {Promise<Object>} 内容评估结果
   */
  async assessContent(memory) {
    let score = 0;
    const details = {};
    
    // 内容长度评估
    const contentLength = memory.content?.length || 0;
    if (contentLength === 0) {
      details.length = 'empty';
      score += 0;
    } else if (contentLength < 20) {
      details.length = 'too_short';
      score += 20;
    } else if (contentLength < 50) {
      details.length = 'short';
      score += 40;
    } else if (contentLength < 200) {
      details.length = 'adequate';
      score += 70;
    } else if (contentLength < 1000) {
      details.length = 'good';
      score += 85;
    } else {
      details.length = 'excellent';
      score += 100;
    }
    
    // 内容完整性评估
    const hasSummary = memory.summary && memory.summary.length > 10;
    const hasCategory = memory.category && memory.category !== 'unknown';
    const hasTags = memory.tags && memory.tags.length > 0;
    const hasMetadata = memory.metadata && Object.keys(memory.metadata).length > 0;
    
    let completeness = 0;
    if (hasSummary) completeness += 25;
    if (hasCategory) completeness += 25;
    if (hasTags) completeness += 25;
    if (hasMetadata) completeness += 25;
    
    details.completeness = completeness;
    score = (score * 0.6) + (completeness * 0.4);
    
    // 语言质量评估（简单检查）
    const languageIssues = [];
    const content = memory.content || '';
    
    if (content.length > 50) {
      // 检查是否全是数字或特殊字符
      if (/^[0-9\s\W]+$/.test(content)) {
        languageIssues.push('contains_only_numbers_or_symbols');
      }
      
      // 检查是否包含可读词汇
      const wordCount = content.split(/\s+/).filter(w => w.length > 2).length;
      if (wordCount < 5) {
        languageIssues.push('too_few_words');
      }
    }
    
    details.languageIssues = languageIssues;
    
    return {
      score: Math.round(score),
      details
    };
  }

  /**
   * 评估结构质量
   * @param {Object} memory - 记忆对象
   * @returns {Promise<Object>} 结构评估结果
   */
  async assessStructure(memory) {
    let score = 0;
    const details = {};
    
    // 检查是否有分类
    const hasCategory = memory.category && memory.category !== 'unknown';
    details.hasCategory = hasCategory;
    score += hasCategory ? 25 : 0;
    
    // 检查是否有标签
    const tagCount = memory.tags?.length || 0;
    details.tagCount = tagCount;
    score += Math.min(25, tagCount * 5);
    
    // 检查是否有摘要
    const hasSummary = memory.summary && memory.summary.length > 10;
    details.hasSummary = hasSummary;
    score += hasSummary ? 25 : 0;
    
    // 检查元数据完整性
    const metadataKeys = memory.metadata ? Object.keys(memory.metadata) : [];
    const importantMetadata = ['createdAt', 'source', 'type'].filter(k => metadataKeys.includes(k));
    details.importantMetadata = importantMetadata.length;
    score += (importantMetadata.length / 3) * 25;
    
    return {
      score: Math.round(score),
      details
    };
  }

  /**
   * 评估实用性
   * @param {Object} memory - 记忆对象
   * @returns {Promise<Object>} 实用性评估结果
   */
  async assessUtility(memory) {
    let score = 50; // 基础分
    const details = {};
    
    // 获取使用统计
    const usageRecords = await this.storage.find('memory_usage', { memoryId: memory._id });
    
    const totalUses = usageRecords.length;
    const successfulUses = usageRecords.filter(r => r.success).length;
    const successRate = totalUses > 0 ? successfulUses / totalUses : 0;
    
    details.totalUses = totalUses;
    details.successfulUses = successfulUses;
    details.successRate = successRate;
    
    // 使用频率评分
    if (totalUses === 0) {
      score += 0; // 从未使用
    } else if (totalUses < 3) {
      score += 10;
    } else if (totalUses < 10) {
      score += 25;
    } else if (totalUses < 20) {
      score += 40;
    } else {
      score += 50;
    }
    
    // 成功率评分
    score += successRate * 30;
    
    // 重要性标记
    if (memory.important) {
      score += 10;
      details.important = true;
    }
    
    return {
      score: Math.round(Math.min(100, score)),
      details
    };
  }

  /**
   * 评估新鲜度
   * @param {Object} memory - 记忆对象
   * @returns {Promise<Object>} 新鲜度评估结果
   */
  async assessFreshness(memory) {
    const now = new Date();
    const createdAt = new Date(memory.createdAt);
    const updatedAt = new Date(memory.updatedAt || memory.createdAt);
    
    const ageInDays = (now - createdAt) / (1000 * 60 * 60 * 24);
    const daysSinceUpdate = (now - updatedAt) / (1000 * 60 * 60 * 24);
    
    let score = 0;
    
    // 年龄评分
    if (ageInDays < 1) {
      score += 50; // 一天内
    } else if (ageInDays < 7) {
      score += 40; // 一周内
    } else if (ageInDays < 30) {
      score += 30; // 一个月内
    } else if (ageInDays < 90) {
      score += 20; // 三个月内
    } else {
      score += 10; // 超过三个月
    }
    
    // 更新评分
    if (daysSinceUpdate < 1) {
      score += 50; // 最近更新
    } else if (daysSinceUpdate < 7) {
      score += 40;
    } else if (daysSinceUpdate < 30) {
      score += 20;
    } else {
      score += 10;
    }
    
    return {
      score: Math.round(Math.min(100, score)),
      details: {
        ageInDays: Math.round(ageInDays),
        daysSinceUpdate: Math.round(daysSinceUpdate)
      }
    };
  }

  /**
   * 评估独特性
   * @param {Object} memory - 记忆对象
   * @returns {Promise<Object>} 独特性评估结果
   */
  async assessUniqueness(memory) {
    let score = 50; // 基础分
    const details = {};
    
    try {
      // 搜索相似记忆
      const similar = await this.vectorStore.search(memory.content, {
        userId: memory.userId,
        limit: 10,
        minScore: 0.7
      });
      
      // 过滤掉自己
      const otherMemories = similar.filter(r => r.memoryId !== memory._id);
      
      details.similarCount = otherMemories.length;
      
      if (otherMemories.length === 0) {
        score = 100; // 完全独特
      } else if (otherMemories.length < 3) {
        score = 80;
      } else if (otherMemories.length < 5) {
        score = 60;
      } else {
        score = 40; // 可能有重复
      }
      
      // 检查内容重复
      if (otherMemories.length > 0) {
        const topSimilar = otherMemories[0];
        if (topSimilar.score > 0.95) {
          details.duplicateRisk = 'high';
          details.topSimilarScore = topSimilar.score;
        } else if (topSimilar.score > 0.85) {
          details.duplicateRisk = 'medium';
        } else {
          details.duplicateRisk = 'low';
        }
      }
      
    } catch (error) {
      this.logger.warn('Failed to assess uniqueness', { error, memoryId: memory._id });
      score = 50;
    }
    
    return {
      score: Math.round(score),
      details
    };
  }

  /**
   * 计算总体分数
   * @param {Object} dimensions - 各个维度的评估结果
   * @returns {number} 总体分数
   */
  calculateOverallScore(dimensions) {
    const weights = {
      content: 0.30,    // 内容质量占30%
      structure: 0.20,  // 结构质量占20%
      utility: 0.30,   // 实用性占30%
      freshness: 0.10, // 新鲜度占10%
      uniqueness: 0.10 // 独特性占10%
    };
    
    const weightedSum = 
      dimensions.content.score * weights.content +
      dimensions.structure.score * weights.structure +
      dimensions.utility.score * weights.utility +
      dimensions.freshness.score * weights.freshness +
      dimensions.uniqueness.score * weights.uniqueness;
    
    return Math.round(weightedSum);
  }

  /**
   * 识别问题
   * @param {Object} dimensions - 各个维度的评估结果
   * @returns {Array} 问题列表
   */
  identifyIssues(dimensions) {
    const issues = [];
    
    // 内容问题
    if (dimensions.content.details.length === 'empty') {
      issues.push({
        dimension: 'content',
        severity: 'critical',
        message: '记忆内容为空'
      });
    } else if (dimensions.content.details.length === 'too_short') {
      issues.push({
        dimension: 'content',
        severity: 'warning',
        message: '记忆内容过短，可能缺乏足够信息'
      });
    }
    
    if (dimensions.content.details.languageIssues?.length > 0) {
      issues.push({
        dimension: 'content',
        severity: 'warning',
        message: '内容可能存在语言质量问题'
      });
    }
    
    // 结构问题
    if (!dimensions.structure.details.hasCategory) {
      issues.push({
        dimension: 'structure',
        severity: 'warning',
        message: '记忆缺少分类'
      });
    }
    
    if (dimensions.structure.details.tagCount === 0) {
      issues.push({
        dimension: 'structure',
        severity: 'info',
        message: '记忆没有标签，可以添加标签提高可检索性'
      });
    }
    
    if (!dimensions.structure.details.hasSummary) {
      issues.push({
        dimension: 'structure',
        severity: 'info',
        message: '记忆没有摘要，可以添加摘要提高可读性'
      });
    }
    
    // 实用性警告
    if (dimensions.utility.details.totalUses === 0) {
      issues.push({
        dimension: 'utility',
        severity: 'info',
        message: '记忆从未被使用，可能价值不高'
      });
    }
    
    // 新鲜度问题
    if (dimensions.freshness.details.ageInDays > 90) {
      issues.push({
        dimension: 'freshness',
        severity: 'info',
        message: '记忆较旧，可能需要更新'
      });
    }
    
    // 独特性问题
    if (dimensions.uniqueness.details.duplicateRisk === 'high') {
      issues.push({
        dimension: 'uniqueness',
        severity: 'warning',
        message: '存在高度相似的记忆，可能需要合并'
      });
    }
    
    return issues;
  }

  /**
   * 生成优化建议
   * @param {Object} dimensions - 各个维度的评估结果
   * @param {Array} issues - 问题列表
   * @returns {Array} 建议列表
   */
  generateSuggestions(dimensions, issues) {
    const suggestions = [];
    
    // 根据问题生成建议
    for (const issue of issues) {
      switch (issue.dimension) {
        case 'content':
          if (issue.severity === 'critical') {
            suggestions.push({
              priority: 'high',
              action: 'expand_content',
              description: '扩展记忆内容，添加更多详细信息'
            });
          } else if (issue.severity === 'warning') {
            suggestions.push({
              priority: 'medium',
              action: 'improve_content',
              description: '改进记忆内容，增加更多有价值的信息'
            });
          }
          break;
          
        case 'structure':
          if (!dimensions.structure.details.hasCategory) {
            suggestions.push({
              priority: 'high',
              action: 'add_category',
              description: '为记忆添加分类标签'
            });
          }
          if (dimensions.structure.details.tagCount < 3) {
            suggestions.push({
              priority: 'medium',
              action: 'add_tags',
              description: '添加更多标签提高可检索性（建议3-5个）'
            });
          }
          if (!dimensions.structure.details.hasSummary) {
            suggestions.push({
              priority: 'medium',
              action: 'add_summary',
              description: '添加记忆摘要，便于快速回顾'
            });
          }
          break;
          
        case 'freshness':
          suggestions.push({
            priority: 'medium',
            action: 'update_memory',
            description: '更新记忆内容，保持信息新鲜度'
          });
          break;
          
        case 'uniqueness':
          if (issue.message.includes('合并')) {
            suggestions.push({
              priority: 'medium',
              action: 'merge_memories',
              description: '考虑合并相似的记忆'
            });
          }
          break;
      }
    }
    
    // 去重
    const uniqueSuggestions = [];
    const seenActions = new Set();
    
    for (const suggestion of suggestions) {
      if (!seenActions.has(suggestion.action)) {
        seenActions.add(suggestion.action);
        uniqueSuggestions.push(suggestion);
      }
    }
    
    // 按优先级排序
    return uniqueSuggestions.sort((a, b) => {
      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
  }

  /**
   * 批量评估记忆
   * @param {string} userId - 用户 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 批量评估结果
   */
  async assessAllMemories(userId, options = {}) {
    const { minScore = 0, maxScore = 100 } = options;
    
    try {
      const memories = await this.storage.find('memories', { userId });
      
      const results = await Promise.all(
        memories.map(memory => this.assessMemory(memory._id))
      );
      
      // 过滤分数范围
      const filteredResults = results.filter(r => 
        r.overallScore >= minScore && r.overallScore <= maxScore
      );
      
      // 统计信息
      const stats = {
        total: results.length,
        evaluated: filteredResults.length,
        averageScore: results.reduce((sum, r) => sum + r.overallScore, 0) / results.length,
        scoreDistribution: {
          excellent: results.filter(r => r.overallScore >= 90).length,
          good: results.filter(r => r.overallScore >= 70 && r.overallScore < 90).length,
          average: results.filter(r => r.overallScore >= 50 && r.overallScore < 70).length,
          poor: results.filter(r => r.overallScore < 50).length
        }
      };
      
      // 按分数排序
      filteredResults.sort((a, b) => b.overallScore - a.overallScore);
      
      return {
        stats,
        memories: filteredResults,
        assessedAt: new Date()
      };
      
    } catch (error) {
      this.logger.error('Failed to assess all memories', { error, userId });
      throw error;
    }
  }

  /**
   * 获取优化建议
   * @param {string} userId - 用户 ID
   * @param {number} limit - 限制数量
   * @returns {Promise<Object>} 优化建议
   */
  async getOptimizationSuggestions(userId, limit = 10) {
    try {
      const assessment = await this.assessAllMemories(userId);
      
      // 收集所有建议
      const allSuggestions = [];
      
      for (const memoryResult of assessment.memories) {
        for (const suggestion of memoryResult.suggestions) {
          allSuggestions.push({
            ...suggestion,
            memoryId: memoryResult.memoryId,
            memoryScore: memoryResult.overallScore
          });
        }
      }
      
      // 按优先级和分数排序
      allSuggestions.sort((a, b) => {
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
          return priorityOrder[a.priority] - priorityOrder[b.priority];
        }
        return a.memoryScore - b.memoryScore; // 分数低的先优化
      });
      
      return {
        suggestions: allSuggestions.slice(0, limit),
        stats: assessment.stats,
        totalSuggestions: allSuggestions.length
      };
      
    } catch (error) {
      this.logger.error('Failed to get optimization suggestions', { error, userId });
      throw error;
    }
  }
}

export default MemoryQuality;
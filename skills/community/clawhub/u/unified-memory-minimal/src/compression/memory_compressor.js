/**
 * Memory Compressor - 记忆压缩器
 * 
 * 核心目标：将大量记忆压缩成简洁的上下文，节省 token
 */

import { logger } from '../logger.js';

export class MemoryCompressor {
  constructor(options = {}) {
    this.options = {
      // 压缩策略
      maxTokens: options.maxTokens || 2000,        // 最大 token 数
      maxMemories: options.maxMemories || 20,      // 最大记忆条数
      
      // 压缩方式
      enableSummarization: options.enableSummarization !== false,
      enableGrouping: options.enableGrouping !== false,
      enablePrioritization: options.enablePrioritization !== false,
      
      // 格式化
      format: options.format || 'structured',      // structured, narrative, bullet
      
      ...options
    };
    
    // 压缩统计
    this.stats = {
      totalCompressions: 0,
      avgCompressionRatio: 0,
      totalTokensSaved: 0
    };
    
    logger.info('[MemoryCompressor] 记忆压缩器初始化完成');
  }
  
  /**
   * 压缩记忆 - 核心方法
   */
  async compress(memories, context = {}) {
    logger.debug(`[MemoryCompressor] 压缩 ${memories.length} 条记忆`);
    
    if (memories.length === 0) {
      return {
        text: '',
        stats: { original: 0, compressed: 0, ratio: 1 }
      };
    }
    
    // 1. 优先级排序
    const prioritized = this.options.enablePrioritization
      ? this.prioritize(memories, context)
      : memories;
    
    // 2. 分组
    const grouped = this.options.enableGrouping
      ? this.group(prioritized)
      : { 'default': prioritized };
    
    // 3. 生成压缩文本
    const compressed = await this.generateCompressedText(grouped, context);
    
    // 4. 检查 token 限制
    const finalText = this.enforceTokenLimit(compressed);
    
    // 更新统计
    const originalTokens = this.estimateTokens(memories.map(m => m.text || m.memory?.text || '').join('\n'));
    const compressedTokens = this.estimateTokens(finalText);
    
    this.updateStats(originalTokens, compressedTokens);
    
    logger.info(`[MemoryCompressor] 压缩完成: ${originalTokens} → ${compressedTokens} tokens (${((1 - compressedTokens/originalTokens) * 100).toFixed(1)}% 节省)`);
    
    return {
      text: finalText,
      stats: {
        original: originalTokens,
        compressed: compressedTokens,
        ratio: compressedTokens / originalTokens,
        memoriesProcessed: memories.length,
        memoriesIncluded: prioritized.length
      }
    };
  }
  
  /**
   * 优先级排序
   */
  prioritize(memories, context) {
    const scored = memories.map(m => {
      const memory = m.memory || m;
      let score = m.finalScore || m.score || 0.5;
      
      // 重要性加成
      if (memory.importance) {
        score += memory.importance * 0.3;
      }
      
      // 时效性加成
      const age = Date.now() - (memory.timestamp || Date.now());
      const daysAge = age / (1000 * 60 * 60 * 24);
      
      if (daysAge < 1) {
        score += 0.2;
      } else if (daysAge < 7) {
        score += 0.1;
      }
      
      // 类型优先级
      const typePriority = {
        'facts': 1.2,
        'preferences': 1.1,
        'skills': 1.0,
        'patterns': 0.9,
        'cases': 0.8,
        'events': 0.7
      };
      
      if (memory.type && typePriority[memory.type]) {
        score *= typePriority[memory.type];
      }
      
      return { ...m, priorityScore: score };
    });
    
    // 排序并截断
    return scored
      .sort((a, b) => b.priorityScore - a.priorityScore)
      .slice(0, this.options.maxMemories);
  }
  
  /**
   * 分组记忆
   */
  group(memories) {
    const groups = {};
    
    for (const m of memories) {
      const memory = m.memory || m;
      const type = memory.type || 'general';
      
      if (!groups[type]) {
        groups[type] = [];
      }
      
      groups[type].push(m);
    }
    
    return groups;
  }
  
  /**
   * 生成压缩文本
   */
  async generateCompressedText(grouped, context) {
    const format = this.options.format;
    
    switch (format) {
      case 'narrative':
        return this.formatNarrative(grouped);
      case 'bullet':
        return this.formatBullet(grouped);
      case 'structured':
      default:
        return this.formatStructured(grouped);
    }
  }
  
  /**
   * 结构化格式
   */
  formatStructured(grouped) {
    const sections = [];
    
    for (const [type, memories] of Object.entries(grouped)) {
      const typeNames = {
        'facts': '📋 事实',
        'patterns': '🔄 模式',
        'skills': '💡 技能',
        'cases': '📚 案例',
        'events': '📅 事件',
        'preferences': '❤️ 偏好',
        'general': '📝 其他'
      };
      
      const typeName = typeNames[type] || type;
      const items = memories.map(m => {
        const memory = m.memory || m;
        const text = memory.text || memory.summary || '';
        const importance = memory.importance ? ` [重要度: ${(memory.importance * 100).toFixed(0)}%]` : '';
        
        return `  • ${text}${importance}`;
      });
      
      sections.push(`${typeName}:\n${items.join('\n')}`);
    }
    
    return sections.join('\n\n');
  }
  
  /**
   * 叙述格式
   */
  formatNarrative(grouped) {
    const narratives = [];
    
    for (const [type, memories] of Object.entries(grouped)) {
      const items = memories.map(m => {
        const memory = m.memory || m;
        return memory.text || memory.summary || '';
      });
      
      const narrative = items.join('；');
      narratives.push(narrative);
    }
    
    return narratives.join('\n\n');
  }
  
  /**
   * 列表格式
   */
  formatBullet(grouped) {
    const items = [];
    
    for (const [type, memories] of Object.entries(grouped)) {
      for (const m of memories) {
        const memory = m.memory || m;
        items.push(`- ${memory.text || memory.summary || ''}`);
      }
    }
    
    return items.join('\n');
  }
  
  /**
   * 强制 token 限制
   */
  enforceTokenLimit(text) {
    const tokens = this.estimateTokens(text);
    
    if (tokens <= this.options.maxTokens) {
      return text;
    }
    
    // 截断到限制
    const ratio = this.options.maxTokens / tokens;
    const targetLength = Math.floor(text.length * ratio * 0.9); // 留一点余量
    
    return text.substring(0, targetLength) + '\n... (已截断)';
  }
  
  /**
   * 估算 token 数
   */
  estimateTokens(text) {
    if (!text) return 0;
    
    // 简单估算：中文约 1.5 字/token，英文约 4 字/token
    const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const englishChars = text.length - chineseChars;
    
    return Math.ceil(chineseChars / 1.5 + englishChars / 4);
  }
  
  /**
   * 更新统计
   */
  updateStats(originalTokens, compressedTokens) {
    this.stats.totalCompressions++;
    
    const ratio = compressedTokens / originalTokens;
    const alpha = 0.1;
    
    this.stats.avgCompressionRatio = 
      this.stats.avgCompressionRatio * (1 - alpha) + ratio * alpha;
    
    this.stats.totalTokensSaved += (originalTokens - compressedTokens);
  }
  
  /**
   * 获取统计
   */
  getStats() {
    return { ...this.stats };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalCompressions: 0,
      avgCompressionRatio: 0,
      totalTokensSaved: 0
    };
    
    logger.info('[MemoryCompressor] 统计已重置');
  }
}

// 导出单例
let compressorInstance = null;

export function getMemoryCompressor(options = {}) {
  if (!compressorInstance) {
    compressorInstance = new MemoryCompressor(options);
  }
  return compressorInstance;
}

export default MemoryCompressor;

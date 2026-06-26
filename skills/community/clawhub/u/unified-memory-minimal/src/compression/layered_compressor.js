/**
 * 分层压缩系统 - 借鉴 OpenViking 的三层信息模型
 * 
 * L0 (Abstract): ~100 tokens - 向量搜索、快速过滤
 * L1 (Overview): ~2k tokens - 重排序、内容导航
 * L2 (Detail): 无限制 - 完整内容，按需加载
 */

import { logger } from '../logger.js';

/**
 * 分层压缩器
 */
export class LayeredCompressor {
  constructor(options = {}) {
    this.options = {
      // Token 限制（借鉴 OpenViking）
      l0TokenLimit: options.l0TokenLimit || 100,    // L0: ~100 tokens
      l1TokenLimit: options.l1TokenLimit || 2000,   // L1: ~2k tokens
      l2TokenLimit: options.l2TokenLimit || null,   // L2: 无限制
      
      // 分层策略
      enableL0: options.enableL0 !== false,
      enableL1: options.enableL1 !== false,
      enableL2: options.enableL2 !== false,
      
      // 压缩格式
      format: options.format || 'markdown',
      
      // Token 估算（平均 1 token ≈ 4 字符）
      tokenRatio: options.tokenRatio || 4,
      
      ...options
    };
    
    // 统计信息
    this.stats = {
      totalL0Generated: 0,
      totalL1Generated: 0,
      totalL2Generated: 0,
      avgL0Tokens: 0,
      avgL1Tokens: 0,
      totalTokensSaved: 0
    };
    
    logger.info('[LayeredCompressor] 初始化分层压缩器');
  }
  
  /**
   * 估算 token 数量
   */
  estimateTokens(text) {
    if (!text) return 0;
    return Math.ceil(text.length / this.options.tokenRatio);
  }
  
  /**
   * 生成 L0 抽象（~100 tokens）
   * 用于向量搜索和快速过滤
   */
  generateL0Abstract(memory) {
    const text = memory.memory?.text || memory.text || '';
    const tokens = this.estimateTokens(text);
    
    // 如果已经在限制内，直接返回
    if (tokens <= this.options.l0TokenLimit) {
      return {
        layer: 'L0',
        text: text,
        tokens: tokens,
        type: 'original'
      };
    }
    
    // 提取关键信息生成摘要
    const abstract = this.extractKeyInfo(text, this.options.l0TokenLimit);
    const abstractTokens = this.estimateTokens(abstract);
    
    this.stats.totalL0Generated++;
    this.stats.avgL0Tokens = (this.stats.avgL0Tokens * (this.stats.totalL0Generated - 1) + abstractTokens) / this.stats.totalL0Generated;
    this.stats.totalTokensSaved += (tokens - abstractTokens);
    
    return {
      layer: 'L0',
      text: abstract,
      tokens: abstractTokens,
      type: 'abstract',
      originalTokens: tokens
    };
  }
  
  /**
   * 生成 L1 概览（~2k tokens）
   * 用于重排序和内容导航
   */
  generateL1Overview(memory) {
    const text = memory.memory?.text || memory.text || '';
    const tokens = this.estimateTokens(text);
    
    // 如果已经在限制内，直接返回
    if (tokens <= this.options.l1TokenLimit) {
      return {
        layer: 'L1',
        text: text,
        tokens: tokens,
        type: 'original'
      };
    }
    
    // 生成结构化概览
    const overview = this.generateStructuredOverview(text, this.options.l1TokenLimit);
    const overviewTokens = this.estimateTokens(overview);
    
    this.stats.totalL1Generated++;
    this.stats.avgL1Tokens = (this.stats.avgL1Tokens * (this.stats.totalL1Generated - 1) + overviewTokens) / this.stats.totalL1Generated;
    this.stats.totalTokensSaved += (tokens - overviewTokens);
    
    return {
      layer: 'L1',
      text: overview,
      tokens: overviewTokens,
      type: 'overview',
      originalTokens: tokens
    };
  }
  
  /**
   * 生成 L2 详情（无限制）
   * 完整内容，按需加载
   */
  generateL2Detail(memory) {
    const text = memory.memory?.text || memory.text || '';
    const tokens = this.estimateTokens(text);
    
    this.stats.totalL2Generated++;
    
    return {
      layer: 'L2',
      text: text,
      tokens: tokens,
      type: 'detail'
    };
  }
  
  /**
   * 为单个记忆生成所有层
   */
  generateAllLayers(memory) {
    return {
      id: memory.id || memory.memory?.id,
      L0: this.generateL0Abstract(memory),
      L1: this.generateL1Overview(memory),
      L2: this.generateL2Detail(memory),
      metadata: {
        type: memory.type || memory.memory?.type,
        importance: memory.importance || memory.memory?.importance,
        timestamp: memory.timestamp || memory.memory?.timestamp
      }
    };
  }
  
  /**
   * 批量生成分层内容
   */
  generateLayersBatch(memories) {
    return memories.map(memory => this.generateAllLayers(memory));
  }
  
  /**
   * 提取关键信息（用于 L0）
   */
  extractKeyInfo(text, maxTokens) {
    const maxLength = maxTokens * this.options.tokenRatio;
    
    // 策略1：提取第一句
    const firstSentence = text.split(/[。！？\n]/)[0];
    if (firstSentence && firstSentence.length <= maxLength) {
      return firstSentence.trim();
    }
    
    // 策略2：截断到限制
    if (text.length <= maxLength) {
      return text;
    }
    
    // 策略3：智能截断
    return text.substring(0, maxLength - 3) + '...';
  }
  
  /**
   * 生成结构化概览（用于 L1）
   */
  generateStructuredOverview(text, maxTokens) {
    const maxLength = maxTokens * this.options.tokenRatio;
    
    // 如果文本很短，直接返回
    if (text.length <= maxLength) {
      return text;
    }
    
    // 分段处理
    const paragraphs = text.split(/\n\n+/);
    const sections = [];
    let currentLength = 0;
    
    for (const para of paragraphs) {
      if (currentLength + para.length > maxLength) {
        break;
      }
      sections.push(para);
      currentLength += para.length + 2; // +2 for \n\n
    }
    
    let overview = sections.join('\n\n');
    
    // 如果还有剩余空间，添加省略提示
    if (overview.length < text.length) {
      const remaining = text.length - overview.length;
      overview += `\n\n... (省略 ${remaining} 字符)`;
    }
    
    return overview;
  }
  
  /**
   * 智能分层加载策略
   * 根据查询意图和 token 预算选择合适的层
   */
  selectLayer(memories, query, options = {}) {
    const maxTokens = options.maxTokens || 4000;
    const strategy = options.strategy || 'adaptive'; // adaptive, L0, L1, L2
    
    const layers = this.generateLayersBatch(memories);
    
    if (strategy === 'L0') {
      // 只使用 L0
      return this.loadLayer(layers, 'L0', maxTokens);
    } else if (strategy === 'L1') {
      // 只使用 L1
      return this.loadLayer(layers, 'L1', maxTokens);
    } else if (strategy === 'L2') {
      // 只使用 L2
      return this.loadLayer(layers, 'L2', maxTokens);
    } else {
      // 自适应策略：先用 L0 过滤，再用 L1 构建，按需加载 L2
      return this.adaptiveLoad(layers, query, maxTokens);
    }
  }
  
  /**
   * 加载指定层
   */
  loadLayer(layers, layerName, maxTokens) {
    const result = [];
    let totalTokens = 0;
    
    for (const item of layers) {
      const layer = item[layerName];
      if (totalTokens + layer.tokens <= maxTokens) {
        result.push({
          id: item.id,
          text: layer.text,
          tokens: layer.tokens,
          layer: layerName,
          metadata: item.metadata
        });
        totalTokens += layer.tokens;
      }
    }
    
    return {
      memories: result,
      totalTokens,
      layer: layerName,
      stats: {
        count: result.length,
        avgTokens: result.length > 0 ? Math.round(totalTokens / result.length) : 0
      }
    };
  }
  
  /**
   * 自适应加载策略
   * 1. 先用 L0 快速过滤（相关性检查）
   * 2. 再用 L1 构建上下文（理解内容）
   * 3. 按需加载 L2（获取详情）
   */
  adaptiveLoad(layers, query, maxTokens) {
    const result = [];
    let totalTokens = 0;
    const l0Budget = Math.floor(maxTokens * 0.1);  // 10% 给 L0
    const l1Budget = Math.floor(maxTokens * 0.7);  // 70% 给 L1
    const l2Budget = Math.floor(maxTokens * 0.2);  // 20% 给 L2
    
    // 阶段1：用 L0 快速过滤
    const l0Filtered = [];
    let l0Tokens = 0;
    
    for (const item of layers) {
      if (l0Tokens + item.L0.tokens <= l0Budget) {
        l0Filtered.push(item);
        l0Tokens += item.L0.tokens;
      }
    }
    
    // 阶段2：用 L1 构建主要上下文
    let l1Tokens = 0;
    
    for (const item of l0Filtered) {
      if (l1Tokens + item.L1.tokens <= l1Budget) {
        result.push({
          id: item.id,
          text: item.L1.text,
          tokens: item.L1.tokens,
          layer: 'L1',
          metadata: item.metadata,
          hasL2: true  // 标记有更详细的内容
        });
        l1Tokens += item.L1.tokens;
      }
    }
    
    totalTokens = l0Tokens + l1Tokens;
    
    return {
      memories: result,
      totalTokens,
      layer: 'adaptive',
      stats: {
        count: result.length,
        avgTokens: result.length > 0 ? Math.round(totalTokens / result.length) : 0,
        l0Filtered: l0Filtered.length,
        l1Used: result.length
      }
    };
  }
  
  /**
   * 按需加载 L2 详情
   */
  loadL2Detail(memoryId, allMemories) {
    const memory = allMemories.find(m => m.id === memoryId || m.memory?.id === memoryId);
    
    if (!memory) {
      return null;
    }
    
    const l2 = this.generateL2Detail(memory);
    
    return {
      id: memoryId,
      text: l2.text,
      tokens: l2.tokens,
      layer: 'L2',
      metadata: memory.metadata
    };
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      avgL0Tokens: Math.round(this.stats.avgL0Tokens),
      avgL1Tokens: Math.round(this.stats.avgL1Tokens),
      compressionRatio: this.stats.totalL0Generated > 0 
        ? (this.stats.totalTokensSaved / (this.stats.totalTokensSaved + this.stats.avgL0Tokens * this.stats.totalL0Generated)).toFixed(2)
        : 0
    };
  }
  
  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      totalL0Generated: 0,
      totalL1Generated: 0,
      totalL2Generated: 0,
      avgL0Tokens: 0,
      avgL1Tokens: 0,
      totalTokensSaved: 0
    };
  }
}

// 单例
let instance = null;

export function getLayeredCompressor(options = {}) {
  if (!instance) {
    instance = new LayeredCompressor(options);
  }
  return instance;
}

export default LayeredCompressor;

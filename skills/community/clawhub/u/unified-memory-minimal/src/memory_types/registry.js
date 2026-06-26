/**
 * Memory Type Registry - 记忆类型注册系统
 * 借鉴 OpenViking 的 memory_type_registry.py
 */

import { logger } from '../logger.js';
import { facts } from './facts.js';
import { patterns } from './patterns.js';
import { skills } from './skills.js';
import { cases } from './cases.js';
import { events } from './events.js';
import { preferences } from './preferences.js';

export class MemoryTypeRegistry {
  constructor() {
    this.types = new Map();
    this.defaultConfig = {
      extractionStrategy: 'llm',      // 提取策略: llm, rule, hybrid
      storagePriority: 'medium',       // 存储优先级: low, medium, high
      retentionDays: 365,              // 保留天数
      deduplicationThreshold: 0.8,     // 去重阈值
      vectorIndex: true,               // 是否创建向量索引
      importanceScoring: true,         // 是否计算重要性分数
      autoArchive: true,               // 是否自动归档
      conflictResolution: 'merge'      // 冲突解决策略: merge, keep_new, keep_old
    };
    
    this.registerBuiltinTypes();
  }
  
  /**
   * 注册内置类型
   */
  registerBuiltinTypes() {
    // 事实型记忆
    this.registerType('facts', {
      name: '事实型记忆',
      description: '客观事实、数据、信息',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'hybrid',
        storagePriority: 'high',
        retentionDays: 9999, // 永久保留
        deduplicationThreshold: 0.9,
        conflictResolution: 'merge'
      },
      handler: facts
    });
    
    // 模式型记忆
    this.registerType('patterns', {
      name: '模式型记忆',
      description: '行为模式、习惯、规律',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'llm',
        storagePriority: 'high',
        retentionDays: 180,
        deduplicationThreshold: 0.7,
        conflictResolution: 'merge'
      },
      handler: patterns
    });
    
    // 技能型记忆
    this.registerType('skills', {
      name: '技能型记忆',
      description: '技能、能力、专长',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'llm',
        storagePriority: 'high',
        retentionDays: 365,
        deduplicationThreshold: 0.6,
        conflictResolution: 'keep_new'
      },
      handler: skills
    });
    
    // 案例型记忆
    this.registerType('cases', {
      name: '案例型记忆',
      description: '案例、经验、教训',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'llm',
        storagePriority: 'medium',
        retentionDays: 365,
        deduplicationThreshold: 0.8,
        conflictResolution: 'merge'
      },
      handler: cases
    });
    
    // 事件型记忆
    this.registerType('events', {
      name: '事件型记忆',
      description: '事件、会议、活动',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'rule',
        storagePriority: 'medium',
        retentionDays: 90,
        deduplicationThreshold: 0.85,
        conflictResolution: 'keep_new'
      },
      handler: events
    });
    
    // 偏好型记忆
    this.registerType('preferences', {
      name: '偏好型记忆',
      description: '偏好、习惯、喜好',
      config: {
        ...this.defaultConfig,
        extractionStrategy: 'llm',
        storagePriority: 'high',
        retentionDays: 9999,
        deduplicationThreshold: 0.75,
        conflictResolution: 'keep_new'
      },
      handler: preferences
    });
    
    logger.info(`[MemoryTypeRegistry] 已注册 ${this.types.size} 种内置记忆类型`);
  }
  
  /**
   * 注册新的记忆类型
   */
  registerType(typeName, typeConfig) {
    if (this.types.has(typeName)) {
      logger.warn(`[MemoryTypeRegistry] 记忆类型 ${typeName} 已存在，将被覆盖`);
    }
    
    const fullConfig = {
      ...this.defaultConfig,
      ...typeConfig.config,
      handler: typeConfig.handler
    };
    
    this.types.set(typeName, {
      name: typeConfig.name,
      description: typeConfig.description,
      config: fullConfig
    });
    
    logger.info(`[MemoryTypeRegistry] 注册记忆类型: ${typeName} (${typeConfig.name})`);
    
    return true;
  }
  
  /**
   * 获取记忆类型配置
   */
  getType(typeName) {
    const type = this.types.get(typeName);
    if (!type) {
      throw new Error(`未知的记忆类型: ${typeName}`);
    }
    return { ...type, typeName };
  }
  
  /**
   * 获取所有记忆类型
   */
  getAllTypes() {
    const result = {};
    for (const [typeName, type] of this.types.entries()) {
      result[typeName] = {
        name: type.name,
        description: type.description,
        config: type.config
      };
    }
    return result;
  }
  
  /**
   * 根据内容自动检测记忆类型
   */
  async detectMemoryType(text, context = {}) {
    const types = Array.from(this.types.entries());
    const scores = {};
    
    // 基于规则的快速检测
    for (const [typeName, type] of types) {
      let score = 0;
      
      // 检查关键词
      const keywords = this.getTypeKeywords(typeName);
      for (const keyword of keywords) {
        if (text.toLowerCase().includes(keyword.toLowerCase())) {
          score += 0.3;
        }
      }
      
      // 检查长度模式
      if (typeName === 'facts' && text.length < 100) {
        score += 0.2;
      }
      
      if (typeName === 'cases' && text.length > 200) {
        score += 0.2;
      }
      
      // 检查时间模式
      const timePatterns = /(今天|明天|昨天|下周|上周|月份|年份|\d+月|\d+日|\d+年)/;
      if (typeName === 'events' && timePatterns.test(text)) {
        score += 0.4;
      }
      
      // 检查偏好模式
      const preferencePatterns = /(喜欢|不喜欢|偏好|习惯|通常|总是|从不)/;
      if (typeName === 'preferences' && preferencePatterns.test(text)) {
        score += 0.5;
      }
      
      scores[typeName] = score;
    }
    
    // 找出最高分
    let bestType = 'facts'; // 默认
    let bestScore = 0;
    
    for (const [typeName, score] of Object.entries(scores)) {
      if (score > bestScore) {
        bestScore = score;
        bestType = typeName;
      }
    }
    
    // 如果分数太低，使用LLM进一步判断
    if (bestScore < 0.3 && context.useLLM !== false) {
      try {
        const llmResult = await this.detectWithLLM(text);
        if (llmResult && this.types.has(llmResult.type)) {
          bestType = llmResult.type;
          bestScore = 0.8; // LLM检测结果可信度较高
        }
      } catch (error) {
        logger.warn(`[MemoryTypeRegistry] LLM类型检测失败: ${error.message}`);
      }
    }
    
    return {
      type: bestType,
      score: bestScore,
      confidence: bestScore > 0.6 ? 'high' : bestScore > 0.3 ? 'medium' : 'low',
      alternatives: Object.entries(scores)
        .filter(([_, score]) => score > 0.1)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([type, score]) => ({ type, score }))
    };
  }
  
  /**
   * 使用LLM检测记忆类型
   */
  async detectWithLLM(text) {
    // 这里可以集成LLM调用
    // 暂时使用简单的规则匹配
    const patterns = {
      facts: [/是|有|包含|数据|统计|数字/],
      patterns: [/经常|总是|习惯|规律|模式/],
      skills: [/会|能|擅长|技能|能力/],
      cases: [/案例|例子|经验|教训|故事/],
      events: [/会议|活动|事件|安排|计划/],
      preferences: [/喜欢|不喜欢|偏好|讨厌|最爱/]
    };
    
    for (const [type, regexList] of Object.entries(patterns)) {
      for (const regex of regexList) {
        if (regex.test(text)) {
          return { type, confidence: 0.7 };
        }
      }
    }
    
    return { type: 'facts', confidence: 0.5 };
  }
  
  /**
   * 获取类型的提取策略
   */
  getExtractionStrategy(typeName) {
    const type = this.getType(typeName);
    return type.config.extractionStrategy;
  }
  
  /**
   * 获取类型的去重阈值
   */
  getDeduplicationThreshold(typeName) {
    const type = this.getType(typeName);
    return type.config.deduplicationThreshold;
  }
  
  /**
   * 获取类型的保留天数
   */
  getRetentionDays(typeName) {
    const type = this.getType(typeName);
    return type.config.retentionDays;
  }
  
  /**
   * 获取类型的关键词
   */
  getTypeKeywords(typeName) {
    const keywordMap = {
      facts: ['是', '有', '包含', '数据', '事实', '信息', '数字'],
      patterns: ['经常', '总是', '习惯', '通常', '规律', '模式', '行为'],
      skills: ['会', '能', '擅长', '技能', '能力', '专长', '技术'],
      cases: ['案例', '例子', '经验', '教训', '故事', '经历', '事件'],
      events: ['会议', '活动', '事件', '安排', '计划', '日程', '时间'],
      preferences: ['喜欢', '不喜欢', '偏好', '讨厌', '最爱', '习惯', '通常']
    };
    
    return keywordMap[typeName] || [];
  }
  
  /**
   * 处理记忆（根据类型调用相应的处理器）
   */
  async processMemory(text, typeName, context = {}) {
    const type = this.getType(typeName);
    
    if (!type.config.handler) {
      throw new Error(`记忆类型 ${typeName} 没有对应的处理器`);
    }
    
    const handler = type.config.handler;
    
    try {
      // 提取记忆
      const extracted = await handler.extract(text, context);
      
      // 计算重要性
      const importance = await this.calculateImportance(extracted, typeName, context);
      
      // 生成记忆ID
      const memoryId = this.generateMemoryId(typeName, text, context);
      
      return {
        id: memoryId,
        type: typeName,
        text: text,
        extracted: extracted,
        importance: importance,
        config: type.config,
        timestamp: Date.now(),
        metadata: {
          source: context.source || 'unknown',
          userId: context.userId,
          sessionId: context.sessionId
        }
      };
      
    } catch (error) {
      logger.error(`[MemoryTypeRegistry] 处理记忆失败 (${typeName}):`, error);
      throw new Error(`处理记忆失败: ${error.message}`);
    }
  }
  
  /**
   * 计算记忆重要性
   */
  async calculateImportance(extracted, typeName, context) {
    const type = this.getType(typeName);
    let importance = 0.5; // 默认中等重要性
    
    // 基于类型的基准重要性
    const typeBaseImportance = {
      facts: 0.7,
      patterns: 0.8,
      skills: 0.9,
      cases: 0.6,
      events: 0.4,
      preferences: 0.8
    };
    
    importance = typeBaseImportance[typeName] || 0.5;
    
    // 基于提取质量的调整
    if (extracted && extracted.entities && extracted.entities.length > 0) {
      importance += extracted.entities.length * 0.05;
    }
    
    // 基于上下文的调整
    if (context.priority === 'high') {
      importance += 0.2;
    }
    
    // 确保在0-1范围内
    return Math.min(Math.max(importance, 0.1), 1.0);
  }
  
  /**
   * 生成记忆ID
   */
  generateMemoryId(typeName, text, context) {
    const timestamp = Date.now();
    const hash = this.simpleHash(text.substring(0, 50));
    const userId = context.userId ? context.userId.substring(0, 8) : 'unknown';
    
    return `mem_${typeName}_${userId}_${timestamp}_${hash}`;
  }
  
  /**
   * 简单哈希函数
   */
  simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为32位整数
    }
    return Math.abs(hash).toString(36).substring(0, 6);
  }
  
  /**
   * 导出类型配置
   */
  exportConfig() {
    const config = {};
    for (const [typeName, type] of this.types.entries()) {
      config[typeName] = {
        name: type.name,
        description: type.description,
        config: type.config
      };
    }
    return config;
  }
  
  /**
   * 导入类型配置
   */
  importConfig(config) {
    for (const [typeName, typeConfig] of Object.entries(config)) {
      this.registerType(typeName, typeConfig);
    }
    logger.info(`[MemoryTypeRegistry] 从配置导入 ${Object.keys(config).length} 种记忆类型`);
  }
}

// 导出单例
let registryInstance = null;

export function getMemoryTypeRegistry() {
  if (!registryInstance) {
    registryInstance = new MemoryTypeRegistry();
  }
  return registryInstance;
}

export default MemoryTypeRegistry;
/**
 * Enhanced Memory System Configuration
 * 统一配置所有优化组件
 */

export const ENHANCED_CONFIG = {
  // ========== 核心开关 ==========
  enabled: {
    typeSystem: true,           // 记忆类型系统
    queue: true,                // 异步队列
    dedup: true,                // 智能去重
    recallOptimization: true,   // 召回优化
    compression: true,          // 记忆压缩
    lifecycle: true,            // 生命周期管理
    pipeline: true              // 处理管道
  },

  // ========== 记忆类型系统 ==========
  typeSystem: {
    types: {
      facts: {
        name: '事实',
        description: '客观事实、数据、信息',
        extractionStrategy: 'hybrid',
        retention: 9999,
        archiveAfter: 365,
        dedupThreshold: 0.9,
        importanceBase: 0.7
      },
      patterns: {
        name: '模式',
        description: '行为模式、习惯、规律',
        extractionStrategy: 'llm',
        retention: 180,
        archiveAfter: 90,
        dedupThreshold: 0.7,
        importanceBase: 0.6
      },
      skills: {
        name: '技能',
        description: '技能、能力、专长',
        extractionStrategy: 'llm',
        retention: 365,
        archiveAfter: 180,
        dedupThreshold: 0.6,
        importanceBase: 0.8
      },
      cases: {
        name: '案例',
        description: '案例、经验、教训',
        extractionStrategy: 'llm',
        retention: 365,
        archiveAfter: 180,
        dedupThreshold: 0.8,
        importanceBase: 0.7
      },
      events: {
        name: '事件',
        description: '事件、会议、活动',
        extractionStrategy: 'rule',
        retention: 90,
        archiveAfter: 30,
        dedupThreshold: 0.85,
        importanceBase: 0.5
      },
      preferences: {
        name: '偏好',
        description: '偏好、喜好、习惯',
        extractionStrategy: 'llm',
        retention: 9999,
        archiveAfter: 365,
        dedupThreshold: 0.75,
        importanceBase: 0.8
      }
    },
    
    // 类型检测关键词
    typeKeywords: {
      facts: ['是', '位于', '成立于', '拥有', '数量', '金额', '时间'],
      patterns: ['习惯', '通常', '经常', '总是', '每天', '每周', '每月'],
      skills: ['擅长', '精通', '熟悉', '掌握', '能够', '会', '技能'],
      cases: ['项目', '案例', '经验', '教训', '成功', '失败', '问题'],
      events: ['会议', '活动', '日程', '安排', '计划', '时间', '地点'],
      preferences: ['喜欢', '偏好', '想要', '希望', '讨厌', '不喜欢', '更倾向于']
    }
  },

  // ========== 异步队列系统 ==========
  queue: {
    maxConcurrent: 5,           // 最大并发数
    maxRetries: 3,              // 最大重试次数
    retryDelay: 1000,           // 重试延迟(ms)
    
    // 队列优先级
    priorities: {
      embedding: 'high',        // Embedding 高优先级
      semantic: 'normal',       // 语义分析普通优先级
      deduplication: 'normal',  // 去重普通优先级
      archiving: 'low',         // 归档低优先级
      indexing: 'high'          // 索引高优先级
    },
    
    // 队列大小限制
    maxQueueSize: {
      embedding: 1000,
      semantic: 500,
      deduplication: 500,
      archiving: 200,
      indexing: 1000
    }
  },

  // ========== 智能去重系统 ==========
  dedup: {
    thresholds: {
      exact: 1.0,               // 精确匹配阈值
      semantic: 0.85,           // 语义相似度阈值
      fuzzy: 0.75,              // 模糊匹配阈值
      context: 0.9              // 上下文去重阈值
    },
    
    // 去重策略
    strategies: {
      facts: 'merge',           // 事实：合并
      patterns: 'keep_new',     // 模式：保留新的
      skills: 'merge',          // 技能：合并
      cases: 'keep_old',        // 案例：保留旧的
      events: 'skip',           // 事件：跳过重复
      preferences: 'merge'      // 偏好：合并
    },
    
    // 缓存配置
    cacheSize: 10000,           // 去重缓存大小
    cacheTTL: 3600000           // 缓存有效期(ms)
  },

  // ========== 召回优化系统 ==========
  recall: {
    maxRecall: 10,              // 最多召回多少条
    minScore: 0.6,              // 最低分数阈值
    
    // 多路召回权重
    weights: {
      vector: 0.4,              // 向量搜索权重
      text: 0.3,                // 文本搜索权重
      context: 0.3              // 上下文权重
    },
    
    // 时效性衰减
    timeDecay: {
      enabled: true,
      halfLife: 2592000000      // 30天半衰期(ms)
    },
    
    // 重要性加权
    importanceWeight: {
      enabled: true,
      minFactor: 0.7,           // 最小权重因子
      maxFactor: 1.3            // 最大权重因子
    },
    
    // 缓存配置
    cache: {
      enabled: true,
      maxSize: 1000,
      ttl: 300000               // 5分钟
    }
  },

  // ========== 记忆压缩系统 ==========
  compression: {
    maxTokens: 2000,            // 最大 token 数
    maxMemories: 20,            // 最大记忆条数
    
    // 格式化选项
    format: 'structured',       // structured, narrative, bullet
    
    // 优先级配置
    priority: {
      facts: 1.2,
      preferences: 1.1,
      skills: 1.0,
      patterns: 0.9,
      cases: 0.8,
      events: 0.7
    }
  },

  // ========== 生命周期管理 ==========
  lifecycle: {
    enableAutoArchive: true,    // 启用自动归档
    enableAutoCleanup: true,    // 启用自动清理
    
    archiveInterval: 86400000,  // 归档检查间隔(24小时)
    cleanupInterval: 604800000, // 清理检查间隔(7天)
    
    archiveThreshold: 0.3,      // 归档重要性阈值
    keepHighImportance: true,   // 保留高重要性记忆
    
    // 各类型生命周期
    lifecycles: {
      facts: { retention: 9999, archive: 365, priority: 'high' },
      patterns: { retention: 180, archive: 90, priority: 'medium' },
      skills: { retention: 365, archive: 180, priority: 'high' },
      cases: { retention: 365, archive: 180, priority: 'medium' },
      events: { retention: 90, archive: 30, priority: 'low' },
      preferences: { retention: 9999, archive: 365, priority: 'high' }
    }
  },

  // ========== 处理管道 ==========
  pipeline: {
    enableL0: true,             // 对话录制
    enableL1: true,             // 记忆提取
    enableL2: true,             // 场景归纳
    enableL3: true,             // 用户画像
    
    asyncProcessing: true,      // 异步处理
    batchSize: 10,              // 批量处理大小
    processingInterval: 60000   // 处理间隔(1分钟)
  }
};

// 导出配置获取函数
export function getEnhancedConfig() {
  return { ...ENHANCED_CONFIG };
}

export function getTypeConfig(typeName) {
  return ENHANCED_CONFIG.typeSystem.types[typeName] || null;
}

export function getQueueConfig() {
  return { ...ENHANCED_CONFIG.queue };
}

export function getDedupConfig() {
  return { ...ENHANCED_CONFIG.dedup };
}

export function getRecallConfig() {
  return { ...ENHANCED_CONFIG.recall };
}

export function getCompressionConfig() {
  return { ...ENHANCED_CONFIG.compression };
}

export function getLifecycleConfig() {
  return { ...ENHANCED_CONFIG.lifecycle };
}

export function getPipelineConfig() {
  return { ...ENHANCED_CONFIG.pipeline };
}

export default ENHANCED_CONFIG;

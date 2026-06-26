/**
 * 预测性响应模块
 * 
 * 基于历史对话和用户行为预测用户需求
 * 提前准备响应，减少等待时间
 */

class PredictiveEngine {
  constructor(config, logger) {
    this.config = config || {};
    this.logger = logger || console;
    
    // 预测模型配置
    this.predictionConfig = {
      enabled: this.config.enabled !== false,
      historySize: this.config.historySize || 100,
      predictionThreshold: this.config.predictionThreshold || 0.7,
      learningRate: this.config.learningRate || 0.1,
      maxPredictions: this.config.maxPredictions || 5
    };
    
    // 存储结构
    this.history = []; // 对话历史
    this.patterns = new Map(); // 用户行为模式
    this.predictions = new Map(); // 当前预测
    this.userModels = new Map(); // 用户模型
    
    // 初始化模式识别器
    this.initPatternRecognizers();
    
    this.logger.info('预测性响应引擎初始化完成', { config: this.predictionConfig });
  }
  
  /**
   * 初始化模式识别器
   */
  initPatternRecognizers() {
    this.patternRecognizers = {
      // 时间模式（特定时间的习惯性行为）
      timePattern: this.recognizeTimePattern.bind(this),
      
      // 序列模式（动作序列）
      sequencePattern: this.recognizeSequencePattern.bind(this),
      
      // 上下文模式（基于当前话题的预测）
      contextPattern: this.recognizeContextPattern.bind(this),
      
      // 工作日模式（工作日 vs 周末行为差异）
      weekdayPattern: this.recognizeWeekdayPattern.bind(this),
      
      // 紧急程度模式（基于历史紧急程度预测）
      urgencyPattern: this.recognizeUrgencyPattern.bind(this),
      
      // 任务类型模式（类似任务的重复模式）
      taskTypePattern: this.recognizeTaskTypePattern.bind(this)
    };
  }
  
  /**
   * 记录对话历史
   * @param {object} interaction - 交互记录
   */
  recordInteraction(interaction) {
    const {
      userId,
      message,
      intent,
      priority,
      responseTime,
      responseType,
      timestamp = Date.now(),
      context = {}
    } = interaction;
    
    // 创建记录
    const record = {
      userId,
      message,
      intent,
      priority,
      responseTime,
      responseType,
      timestamp,
      context,
      dayOfWeek: new Date(timestamp).getDay(),
      hourOfDay: new Date(timestamp).getHours()
    };
    
    // 添加到历史
    this.history.push(record);
    
    // 限制历史大小
    if (this.history.length > this.predictionConfig.historySize) {
      this.history.shift();
    }
    
    // 更新用户模型
    this.updateUserModel(userId, record);
    
    // 分析模式
    this.analyzePatterns(record);
    
    this.logger.debug('交互记录已保存', { userId, intent, priority });
  }
  
  /**
   * 更新用户模型
   * @param {string} userId - 用户ID
   * @param {object} record - 交互记录
   */
  updateUserModel(userId, record) {
    if (!this.userModels.has(userId)) {
      this.userModels.set(userId, {
        totalInteractions: 0,
        intents: new Map(),
        responseTimes: [],
        patterns: new Map(),
        lastInteraction: null,
        favoriteTopics: new Set(),
        activityHours: new Map()
      });
    }
    
    const userModel = this.userModels.get(userId);
    
    // 更新统计数据
    userModel.totalInteractions++;
    userModel.lastInteraction = record.timestamp;
    
    // 更新意图统计
    const intentCount = userModel.intents.get(record.intent) || 0;
    userModel.intents.set(record.intent, intentCount + 1);
    
    // 更新响应时间
    if (record.responseTime) {
      userModel.responseTimes.push(record.responseTime);
      if (userModel.responseTimes.length > 100) {
        userModel.responseTimes.shift();
      }
    }
    
    // 更新活跃时段
    const hour = record.hourOfDay;
    const hourCount = userModel.activityHours.get(hour) || 0;
    userModel.activityHours.set(hour, hourCount + 1);
    
    // 更新感兴趣的话题
    if (record.context.topics) {
      record.context.topics.forEach(topic => {
        userModel.favoriteTopics.add(topic);
      });
    }
  }
  
  /**
   * 分析模式
   * @param {object} record - 交互记录
   */
  analyzePatterns(record) {
    for (const [name, recognizer] of Object.entries(this.patternRecognizers)) {
      try {
        const pattern = recognizer(record);
        if (pattern) {
          this.updatePattern(record.userId, name, pattern);
        }
      } catch (error) {
        this.logger.error('模式分析失败', { pattern: name, error: error.message });
      }
    }
  }
  
  /**
   * 识别时间模式
   */
  recognizeTimePattern(record) {
    const { userId, hourOfDay, dayOfWeek } = record;
    const userModel = this.userModels.get(userId);
    
    if (!userModel) return null;
    
    // 检查这个时段是否有频繁交互
    const hourCount = userModel.activityHours.get(hourOfDay) || 0;
    const totalInteractions = userModel.totalInteractions;
    
    if (totalInteractions > 10 && hourCount / totalInteractions > 0.3) {
      return {
        type: 'time',
        hour: hourOfDay,
        day: dayOfWeek,
        confidence: Math.min(hourCount / totalInteractions, 1.0),
        commonIntents: this.getCommonIntentsForHour(userId, hourOfDay)
      };
    }
    
    return null;
  }
  
  /**
   * 识别序列模式
   */
  recognizeSequencePattern(record) {
    const { userId, intent } = record;
    const userHistory = this.history.filter(r => r.userId === userId);
    
    if (userHistory.length < 3) return null;
    
    // 检查最近的3个意图是否形成模式
    const recentIntents = userHistory.slice(-3).map(r => r.intent);
    const patternKey = recentIntents.join('->');
    
    // 查找历史中是否有相同的模式
    const patternCount = userHistory.reduce((count, r, index) => {
      if (index >= 2) {
        const prevIntents = userHistory.slice(index - 2, index + 1).map(hr => hr.intent);
        if (prevIntents.join('->') === patternKey) {
          return count + 1;
        }
      }
      return count;
    }, 0);
    
    if (patternCount > 1) {
      return {
        type: 'sequence',
        pattern: patternKey,
        confidence: patternCount / (userHistory.length / 3),
        nextIntent: this.predictNextIntent(userId, recentIntents)
      };
    }
    
    return null;
  }
  
  /**
   * 识别上下文模式
   */
  recognizeContextPattern(record) {
    const { userId, context } = record;
    
    if (!context.topic) return null;
    
    const userHistory = this.history.filter(r => 
      r.userId === userId && r.context.topic === context.topic
    );
    
    if (userHistory.length < 2) return null;
    
    // 分析相同话题下的常见意图
    const intentCounts = new Map();
    userHistory.forEach(r => {
      const count = intentCounts.get(r.intent) || 0;
      intentCounts.set(r.intent, count + 1);
    });
    
    const total = userHistory.length;
    const patterns = [];
    
    for (const [intent, count] of intentCounts) {
      const frequency = count / total;
      if (frequency > 0.5) { // 超过50%的频率
        patterns.push({
          intent,
          frequency,
          commonMessages: userHistory
            .filter(r => r.intent === intent)
            .map(r => r.message)
            .slice(0, 3)
        });
      }
    }
    
    if (patterns.length > 0) {
      return {
        type: 'context',
        topic: context.topic,
        patterns,
        confidence: patterns.reduce((sum, p) => sum + p.frequency, 0) / patterns.length
      };
    }
    
    return null;
  }
  
  /**
   * 识别工作日模式
   */
  recognizeWeekdayPattern(record) {
    const { userId, dayOfWeek } = record;
    const userHistory = this.history.filter(r => r.userId === userId);
    
    if (userHistory.length < 10) return null;
    
    const weekdayHistory = userHistory.filter(r => r.dayOfWeek >= 1 && r.dayOfWeek <= 5);
    const weekendHistory = userHistory.filter(r => r.dayOfWeek === 0 || r.dayOfWeek === 6);
    
    // 比较工作日和周末的行为差异
    const weekdayIntents = this.getIntentDistribution(weekdayHistory);
    const weekendIntents = this.getIntentDistribution(weekendHistory);
    
    // 查找差异明显的意图
    const differences = [];
    for (const [intent, weekdayFreq] of weekdayIntents) {
      const weekendFreq = weekendIntents.get(intent) || 0;
      const diff = Math.abs(weekdayFreq - weekendFreq);
      
      if (diff > 0.3) { // 差异超过30%
        differences.push({
          intent,
          weekdayFreq,
          weekendFreq,
          difference: diff
        });
      }
    }
    
    if (differences.length > 0) {
      return {
        type: 'weekday',
        dayOfWeek,
        isWeekday: dayOfWeek >= 1 && dayOfWeek <= 5,
        differences,
        confidence: Math.min(userHistory.length / 50, 1.0)
      };
    }
    
    return null;
  }
  
  /**
   * 识别紧急程度模式
   */
  recognizeUrgencyPattern(record) {
    const { userId, priority } = record;
    
    // 优先级映射到紧急程度
    const urgencyMap = {
      'p0': 'critical',
      'p1': 'high',
      'p2': 'medium',
      'p3': 'low'
    };
    
    const urgency = urgencyMap[priority] || 'medium';
    const userHistory = this.history.filter(r => r.userId === userId);
    
    if (userHistory.length < 5) return null;
    
    const urgencyCounts = new Map();
    userHistory.forEach(r => {
      const u = urgencyMap[r.priority] || 'medium';
      const count = urgencyCounts.get(u) || 0;
      urgencyCounts.set(u, count + 1);
    });
    
    const total = userHistory.length;
    const currentUrgencyCount = urgencyCounts.get(urgency) || 0;
    const urgencyFrequency = currentUrgencyCount / total;
    
    if (urgencyFrequency > 0.6) { // 超过60%的交互是这种紧急程度
      return {
        type: 'urgency',
        urgency,
        frequency: urgencyFrequency,
        commonContexts: userHistory
          .filter(r => urgencyMap[r.priority] === urgency)
          .map(r => r.context.topic || 'general')
          .filter(Boolean)
          .slice(0, 5)
      };
    }
    
    return null;
  }
  
  /**
   * 识别任务类型模式
   */
  recognizeTaskTypePattern(record) {
    const { userId, intent, context } = record;
    
    if (intent !== 'task_request') return null;
    
    const userHistory = this.history.filter(r => 
      r.userId === userId && r.intent === 'task_request'
    );
    
    if (userHistory.length < 3) return null;
    
    // 提取任务关键词
    const taskKeywords = this.extractTaskKeywords(record.message);
    
    if (taskKeywords.length === 0) return null;
    
    // 查找类似任务
    const similarTasks = userHistory.filter(prevRecord => {
      const prevKeywords = this.extractTaskKeywords(prevRecord.message);
      return this.areKeywordsSimilar(taskKeywords, prevKeywords);
    });
    
    if (similarTasks.length >= 2) {
      const avgResponseTime = similarTasks.reduce((sum, t) => 
        sum + (t.responseTime || 0), 0) / similarTasks.length;
      
      return {
        type: 'task',
        keywords: taskKeywords,
        similarTasks: similarTasks.length,
        avgResponseTime,
        commonSolutions: similarTasks.map(t => t.context.solution || 'standard').slice(0, 3),
        confidence: Math.min(similarTasks.length / 5, 1.0)
      };
    }
    
    return null;
  }
  
  /**
   * 更新模式
   */
  updatePattern(userId, patternName, pattern) {
    const userModel = this.userModels.get(userId);
    if (!userModel) return;
    
    const existingPatterns = userModel.patterns.get(patternName) || [];
    existingPatterns.push({
      ...pattern,
      timestamp: Date.now()
    });
    
    // 限制模式数量
    if (existingPatterns.length > 10) {
      existingPatterns.shift();
    }
    
    userModel.patterns.set(patternName, existingPatterns);
  }
  
  /**
   * 生成预测
   * @param {string} userId - 用户ID
   * @param {object} currentContext - 当前上下文
   */
  generatePredictions(userId, currentContext = {}) {
    const predictions = [];
    const userModel = this.userModels.get(userId);
    
    if (!userModel || userModel.totalInteractions < 5) {
      return predictions;
    }
    
    const currentHour = new Date().getHours();
    const currentDay = new Date().getDay();
    
    // 1. 基于时间的预测
    const hourPatterns = userModel.patterns.get('time') || [];
    const currentHourPattern = hourPatterns.find(p => p.hour === currentHour);
    
    if (currentHourPattern && currentHourPattern.confidence > this.predictionConfig.predictionThreshold) {
      predictions.push({
        type: 'time_based',
        confidence: currentHourPattern.confidence,
        predictedIntents: currentHourPattern.commonIntents,
        reason: `用户在 ${currentHour}:00 通常询问这些内容`,
        prepare: currentHourPattern.commonIntents.map(intent => this.prepareForIntent(intent))
      });
    }
    
    // 2. 基于上下文的预测
    if (currentContext.topic) {
      const contextPatterns = userModel.patterns.get('context') || [];
      const matchingPattern = contextPatterns.find(p => p.topic === currentContext.topic);
      
      if (matchingPattern && matchingPattern.confidence > this.predictionConfig.predictionThreshold) {
        predictions.push({
          type: 'context_based',
          confidence: matchingPattern.confidence,
          topic: currentContext.topic,
          predictedPatterns: matchingPattern.patterns,
          reason: `关于"${currentContext.topic}"，用户通常有这些需求`,
          prepare: matchingPattern.patterns.map(p => this.prepareForIntent(p.intent))
        });
      }
    }
    
    // 3. 基于紧急程度的预测
    const urgencyPatterns = userModel.patterns.get('urgency') || [];
    if (urgencyPatterns.length > 0) {
      const avgConfidence = urgencyPatterns.reduce((sum, p) => sum + p.confidence, 0) / urgencyPatterns.length;
      
      if (avgConfidence > this.predictionConfig.predictionThreshold) {
        predictions.push({
          type: 'urgency_based',
          confidence: avgConfidence,
          commonUrgency: urgencyPatterns[0].urgency,
          contexts: [...new Set(urgencyPatterns.flatMap(p => p.commonContexts))],
          reason: `用户的问题通常属于"${urgencyPatterns[0].urgency}"紧急程度`,
          prepare: ['准备快速响应', '优化资源分配']
        });
      }
    }
    
    // 限制预测数量
    return predictions
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, this.predictionConfig.maxPredictions);
  }
  
  /**
   * 获取特定时段的常见意图
   */
  getCommonIntentsForHour(userId, hour) {
    const userHistory = this.history.filter(r => 
      r.userId === userId && r.hourOfDay === hour
    );
    
    const intentCounts = new Map();
    userHistory.forEach(r => {
      const count = intentCounts.get(r.intent) || 0;
      intentCounts.set(r.intent, count + 1);
    });
    
    return Array.from(intentCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([intent]) => intent);
  }
  
  /**
   * 预测下一个意图
   */
  predictNextIntent(userId, recentIntents) {
    const userHistory = this.history.filter(r => r.userId === userId);
    
    // 查找历史中类似序列后的意图
    for (let i = 0; i < userHistory.length - recentIntents.length; i++) {
      const sequence = userHistory.slice(i, i + recentIntents.length).map(r => r.intent);
      
      if (JSON.stringify(sequence) === JSON.stringify(recentIntents)) {
        const nextRecord = userHistory[i + recentIntents.length];
        if (nextRecord) {
          return nextRecord.intent;
        }
      }
    }
    
    return null;
  }
  
  /**
   * 获取意图分布
   */
  getIntentDistribution(history) {
    const distribution = new Map();
    const total = history.length;
    
    if (total === 0) return distribution;
    
    history.forEach(r => {
      const count = distribution.get(r.intent) || 0;
      distribution.set(r.intent, count + 1);
    });
    
    // 转换为频率
    for (const [intent, count] of distribution) {
      distribution.set(intent, count / total);
    }
    
    return distribution;
  }
  
  /**
   * 提取任务关键词
   */
  extractTaskKeywords(message) {
    // 简单的关键词提取（实际应该用更复杂的NLP）
    const taskWords = ['分析', '处理', '创建', '开发', '设计', '检查', '测试', '调研', '解决', '实现'];
    return message.toLowerCase().split(/[^a-zA-Z0-9\u4e00-\u9fa5]+/).filter(word => 
      taskWords.some(taskWord => word.includes(taskWord.toLowerCase()))
    );
  }
  
  /**
   * 检查关键词相似度
   */
  areKeywordsSimilar(keywords1, keywords2) {
    if (keywords1.length === 0 || keywords2.length === 0) return false;
    
    const intersection = keywords1.filter(k => keywords2.includes(k));
    return intersection.length / Math.max(keywords1.length, keywords2.length) > 0.5;
  }
  
  /**
   * 为意图准备响应
   */
  prepareForIntent(intent) {
    const preparations = {
      question: ['查找相关信息', '准备解释材料', '整理常见问题解答'],
      task_request: ['分配计算资源', '准备执行环境', '优化算法参数'],
      feedback: ['准备感谢模板', '记录改进建议', '更新用户偏好'],
      social: ['准备问候语', '更新用户状态', '优化响应语气']
    };
    
    return preparations[intent] || ['准备通用响应'];
  }
  
  /**
   * 获取用户统计数据
   */
  getUserStats(userId) {
    const userModel = this.userModels.get(userId);
    if (!userModel) return null;
    
    return {
      totalInteractions: userModel.totalInteractions,
      lastInteraction: userModel.lastInteraction,
      intents: Array.from(userModel.intents.entries()).sort((a, b) => b[1] - a[1]),
      avgResponseTime: userModel.responseTimes.length > 0 
        ? userModel.responseTimes.reduce((a, b) => a + b, 0) / userModel.responseTimes.length 
        : null,
      favoriteTopics: Array.from(userModel.favoriteTopics),
      activeHours: Array.from(userModel.activityHours.entries()).sort((a, b) => b[1] - a[1]),
      patternCount: Array.from(userModel.patterns.entries()).reduce((sum, [_, patterns]) => sum + patterns.length, 0)
    };
  }
  
  /**
   * 获取所有用户的统计数据
   */
  getAllStats() {
    const stats = {
      totalUsers: this.userModels.size,
      totalInteractions: this.history.length,
      recentActivity: this.history.slice(-10),
      userStats: {}
    };
    
    for (const [userId, userModel] of this.userModels) {
      stats.userStats[userId] = {
        totalInteractions: userModel.totalInteractions,
        lastInteraction: userModel.lastInteraction,
        intentCounts: Array.from(userModel.intents.entries())
      };
    }
    
    return stats;
  }
  
  /**
   * 清除旧数据
   */
  cleanupOldData(maxAge = 30 * 24 * 60 * 60 * 1000) { // 默认30天
    const cutoff = Date.now() - maxAge;
    const oldCount = this.history.filter(r => r.timestamp < cutoff).length;
    
    this.history = this.history.filter(r => r.timestamp >= cutoff);
    
    // 清理用户模型中的旧数据
    for (const [userId, userModel] of this.userModels) {
      // 清理过时的模式
      for (const [patternName, patterns] of userModel.patterns) {
        const freshPatterns = patterns.filter(p => p.timestamp >= cutoff);
        userModel.patterns.set(patternName, freshPatterns);
      }
    }
    
    this.logger.info('清理旧数据完成', { removed: oldCount, remaining: this.history.length });
    return oldCount;
  }
  
  /**
   * 重置预测引擎
   */
  reset() {
    this.history = [];
    this.patterns.clear();
    this.predictions.clear();
    this.userModels.clear();
    this.logger.info('预测引擎已重置');
  }
}

module.exports = PredictiveEngine;
/**
 * Urgency Scorer - 紧急度评分算法
 * 基于多维度因素计算内容的紧急程度
 * 评分范围：1-10（1=不急，10=紧急）
 */

class UrgencyScorer {
  constructor() {
    // 权重配置
    this.weights = {
      timeSensitivity: 0.30,    // 时间敏感性
      actionRequired: 0.25,     // 需要行动的程度
      consequence: 0.20,        // 不处理的后果
      context: 0.15,            // 上下文紧急信号
      userPreference: 0.10,     // 用户偏好（可配置）
    };

    // 时间关键词及其紧急度映射
    this.timeKeywords = {
      // 极高紧急 (9-10)
      '立即': 10, '马上': 10, 'right now': 10, 'ASAP': 10, 'urgent': 10,
      '紧急': 10, 'P0': 10, 'critical': 10, '严重': 10,
      
      // 高紧急 (7-8)
      '今天': 8, '今晚': 8, 'today': 8, 'tonight': 8,
      '明天': 7, 'tomorrow': 7, 'P1': 7, '高优先级': 7,
      '尽快': 7, 'as soon as possible': 7, '本周': 7, 'this week': 7,
      
      // 中等紧急 (5-6)
      '这周': 6, '下周': 6, 'next week': 6,
      '本周内': 6, '周末前': 6, 'before weekend': 6,
      'P2': 5, '中优先级': 5, 'medium': 5,
      '过几天': 5, 'in a few days': 5,
      
      // 低紧急 (3-4)
      '下周': 4, '下个月': 4, 'next month': 4,
      'P3': 3, '低优先级': 3, 'low': 3,
      '有空': 3, 'when you have time': 3,
      '以后': 3, 'later': 3, 'someday': 3,
      
      // 不急 (1-2)
      '随时': 2, 'anytime': 2, '不急': 1, 'not urgent': 1,
      '备用': 1, 'reference': 1, '存档': 1, 'archive': 1,
    };

    // 行动关键词
    this.actionKeywords = {
      high: ['必须', '需要', '务必', 'required', 'need to', 'must', 'have to', 'should'],
      medium: ['计划', '准备', '考虑', 'plan to', 'prepare', 'consider', 'think about'],
      low: ['可能', '也许', '想', 'might', 'maybe', 'perhaps', 'want to', 'would like'],
    };

    // 后果关键词
    this.consequenceKeywords = {
      high: ['过期', '失效', '错过', '损失', '罚款', 'deadline', 'expire', 'miss', 'late'],
      medium: ['影响', '延迟', '推迟', 'delay', 'postpone', 'affect'],
      low: ['无影响', '没关系', 'no impact', 'doesn\'t matter'],
    };

    // 上下文紧急信号
    this.contextSignals = {
      deadline: /截止|deadline|due|到期|过期/i,
      meeting: /会议|meeting|讨论|discussion|评审|review/i,
      decision: /决策|决定|decision|批准|approve/i,
      block: /阻塞|block|依赖|depend|等待|waiting/i,
      external: /客户|customer|老板|boss|领导|manager|外部|external/i,
    };
  }

  /**
   * 计算紧急度评分
   * @param {Object} contentAnalysis - 内容分析结果
   * @param {Object} options - 可选配置
   * @returns {Object} 评分结果
   */
  calculate(contentAnalysis, options = {}) {
    const { metadata, type } = contentAnalysis;
    const text = `${metadata.title || ''} ${metadata.description || ''}`;
    
    // 计算各维度分数
    const dimensions = {
      timeSensitivity: this._calculateTimeSensitivity(text, metadata),
      actionRequired: this._calculateActionRequired(text, type),
      consequence: this._calculateConsequence(text),
      context: this._calculateContextSignals(text, metadata),
      userPreference: options.userPreference || 5,  // 默认中等
    };

    // 计算加权总分
    let totalScore = 0;
    for (const [dimension, score] of Object.entries(dimensions)) {
      totalScore += score * this.weights[dimension];
    }

    // 归一化到1-10
    const finalScore = Math.max(1, Math.min(10, Math.round(totalScore)));

    // 生成评分理由
    const reasons = this._generateReasons(dimensions, text);

    // 确定紧急度等级
    const level = this._getUrgencyLevel(finalScore);

    return {
      score: finalScore,
      level,
      dimensions,  // 各维度详细分数
      reasons,
      recommendation: this._generateRecommendation(finalScore, type),
      actionWindow: this._estimateActionWindow(finalScore),
    };
  }

  /**
   * 计算时间敏感性
   */
  _calculateTimeSensitivity(text, metadata) {
    let score = 5;  // 默认中等
    let matched = false;

    // 检查时间关键词
    for (const [keyword, value] of Object.entries(this.timeKeywords)) {
      if (text.toLowerCase().includes(keyword.toLowerCase())) {
        score = value;
        matched = true;
        break;  // 取最高匹配
      }
    }

    // 检查是否有明确的截止日期
    if (metadata.dueDate) {
      const dueDate = this._parseDate(metadata.dueDate);
      if (dueDate) {
        const daysUntil = this._daysUntil(dueDate);
        if (daysUntil !== null) {
          if (daysUntil <= 0) score = Math.max(score, 10);
          else if (daysUntil <= 1) score = Math.max(score, 9);
          else if (daysUntil <= 3) score = Math.max(score, 8);
          else if (daysUntil <= 7) score = Math.max(score, 6);
          else if (daysUntil <= 14) score = Math.max(score, 4);
          else score = Math.min(score, 3);
        }
      }
    }

    // 检查日期提及
    const dateMatches = this._extractDateMentions(text);
    if (dateMatches.length > 0) {
      const nearestDate = dateMatches[0];
      const daysUntil = this._daysUntil(nearestDate);
      if (daysUntil !== null) {
        if (daysUntil <= 1) score = Math.max(score, 8);
        else if (daysUntil <= 3) score = Math.max(score, 6);
        else if (daysUntil <= 7) score = Math.max(score, 5);
      }
    }

    return score;
  }

  /**
   * 计算行动需求程度
   */
  _calculateActionRequired(text, type) {
    let score = 5;
    const lowerText = text.toLowerCase();

    // 高行动需求关键词
    for (const keyword of this.actionKeywords.high) {
      if (lowerText.includes(keyword.toLowerCase())) {
        score = Math.max(score, 8);
        break;
      }
    }

    // 中等行动需求
    if (score < 8) {
      for (const keyword of this.actionKeywords.medium) {
        if (lowerText.includes(keyword.toLowerCase())) {
          score = Math.max(score, 6);
          break;
        }
      }
    }

    // 低行动需求
    if (score < 6) {
      for (const keyword of this.actionKeywords.low) {
        if (lowerText.includes(keyword.toLowerCase())) {
          score = Math.min(score, 4);
          break;
        }
      }
    }

    // 基于内容类型调整
    if (type === 'task') score = Math.max(score, 6);
    if (type === 'idea') score = Math.min(score, 4);
    if (type === 'article' || type === 'video') score = Math.min(score, 5);

    return score;
  }

  /**
   * 计算不处理的后果
   */
  _calculateConsequence(text) {
    let score = 5;
    const lowerText = text.toLowerCase();

    // 高后果关键词
    for (const keyword of this.consequenceKeywords.high) {
      if (lowerText.includes(keyword.toLowerCase())) {
        score = Math.max(score, 9);
        break;
      }
    }

    // 中等后果
    if (score < 9) {
      for (const keyword of this.consequenceKeywords.medium) {
        if (lowerText.includes(keyword.toLowerCase())) {
          score = Math.max(score, 6);
          break;
        }
      }
    }

    // 低后果
    if (score < 6) {
      for (const keyword of this.consequenceKeywords.low) {
        if (lowerText.includes(keyword.toLowerCase())) {
          score = Math.min(score, 3);
          break;
        }
      }
    }

    return score;
  }

  /**
   * 计算上下文紧急信号
   */
  _calculateContextSignals(text, metadata) {
    let score = 5;
    let signals = 0;

    for (const [signal, pattern] of Object.entries(this.contextSignals)) {
      if (pattern.test(text)) {
        signals++;
        switch (signal) {
          case 'deadline':
            score += 2;
            break;
          case 'block':
            score += 2;
            break;
          case 'external':
            score += 1.5;
            break;
          case 'decision':
            score += 1;
            break;
          case 'meeting':
            score += 0.5;
            break;
        }
      }
    }

    // 优先级标签
    if (metadata.priority) {
      switch (metadata.priority.toLowerCase()) {
        case 'critical':
        case 'p0':
          score += 3;
          break;
        case 'high':
        case 'p1':
          score += 2;
          break;
        case 'medium':
        case 'p2':
          score += 0.5;
          break;
        case 'low':
        case 'p3':
          score -= 1;
          break;
      }
    }

    return Math.max(1, Math.min(10, score));
  }

  /**
   * 解析日期字符串
   */
  _parseDate(dateStr) {
    if (!dateStr) return null;
    
    // 尝试解析常见格式
    const patterns = [
      /(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})/,
      /(\d{1,2})[-/月](\d{1,2})/,  // 假设当年
    ];
    
    for (const pattern of patterns) {
      const match = dateStr.match(pattern);
      if (match) {
        const year = match[3] ? parseInt(match[1]) : new Date().getFullYear();
        const month = match[3] ? parseInt(match[2]) : parseInt(match[1]);
        const day = match[3] ? parseInt(match[3]) : parseInt(match[2]);
        return new Date(year, month - 1, day);
      }
    }
    
    return null;
  }

  /**
   * 计算距离某日期还有多少天
   */
  _daysUntil(date) {
    if (!date) return null;
    const now = new Date();
    const diff = date - now;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }

  /**
   * 提取文本中提及的日期
   */
  _extractDateMentions(text) {
    const dates = [];
    const patterns = [
      /(\d{4})[-/](\d{1,2})[-/](\d{1,2})/g,
      /(\d{1,2})[-/](\d{1,2})/g,
    ];
    
    for (const pattern of patterns) {
      const matches = text.matchAll(pattern);
      for (const match of matches) {
        const date = this._parseDate(match[0]);
        if (date) dates.push(date);
      }
    }
    
    return dates.sort((a, b) => a - b);
  }

  /**
   * 生成评分理由
   */
  _generateReasons(dimensions, text) {
    const reasons = [];
    
    // 时间敏感性理由
    if (dimensions.timeSensitivity >= 8) {
      reasons.push('时间敏感：有明确的近期截止日期');
    } else if (dimensions.timeSensitivity <= 3) {
      reasons.push('时间灵活：无明确时间要求');
    }
    
    // 行动需求理由
    if (dimensions.actionRequired >= 7) {
      reasons.push('需要行动：包含明确的行动指令');
    }
    
    // 后果理由
    if (dimensions.consequence >= 8) {
      reasons.push('后果严重：不处理可能导致重要损失');
    }
    
    // 上下文理由
    if (dimensions.context >= 7) {
      reasons.push('上下文紧急：涉及截止日期或阻塞项');
    }
    
    return reasons;
  }

  /**
   * 获取紧急度等级
   */
  _getUrgencyLevel(score) {
    if (score >= 9) return { level: 'critical', label: '极紧急', color: '#ff4444' };
    if (score >= 7) return { level: 'high', label: '高紧急', color: '#ff8800' };
    if (score >= 5) return { level: 'medium', label: '中等', color: '#ffcc00' };
    if (score >= 3) return { level: 'low', label: '低紧急', color: '#66cc66' };
    return { level: 'none', label: '不急', color: '#999999' };
  }

  /**
   * 生成处理建议
   */
  _generateRecommendation(score, type) {
    if (score >= 9) {
      return '立即处理：这是最高优先级事项';
    } else if (score >= 7) {
      return '今天处理：建议在24小时内完成';
    } else if (score >= 5) {
      return type === 'task' ? '本周处理：安排在本周内完成' : '稍后阅读：有时间时处理';
    } else if (score >= 3) {
      return '低优先级：可以延后处理';
    } else {
      return '存档备查：无需立即行动';
    }
  }

  /**
   * 估算行动窗口
   */
  _estimateActionWindow(score) {
    if (score >= 9) return '立即';
    if (score >= 8) return '今天';
    if (score >= 7) return '24小时内';
    if (score >= 6) return '本周';
    if (score >= 5) return '两周内';
    if (score >= 4) return '本月';
    if (score >= 3) return '下月';
    return '无时间限制';
  }

  /**
   * 批量评分并排序
   */
  batchCalculate(items) {
    const scored = items.map(item => ({
      ...item,
      urgency: this.calculate(item.analysis, item.options),
    }));
    
    // 按紧急度降序排序
    return scored.sort((a, b) => b.urgency.score - a.urgency.score);
  }
}

module.exports = UrgencyScorer;
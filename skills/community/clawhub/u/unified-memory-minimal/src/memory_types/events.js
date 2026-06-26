/**
 * Events Memory Handler - 事件型记忆处理器
 */

import { logger } from '../logger.js';

export const events = {
  name: 'events',
  description: '处理事件、会议、活动',
  
  /**
   * 从文本中提取事件
   */
  async extract(text, context = {}) {
    logger.debug(`[EventsHandler] 提取事件: ${text.substring(0, 100)}...`);
    
    // 提取时间信息
    const timeInfo = this.extractTimeInfo(text);
    
    // 提取地点信息
    const locationInfo = this.extractLocationInfo(text);
    
    // 提取参与人员
    const participants = this.extractParticipants(text);
    
    // 提取事件类型
    const eventType = this.extractEventType(text);
    
    // 提取事件状态
    const eventStatus = this.extractEventStatus(text);
    
    // 提取重要程度
    const importance = this.extractImportance(text);
    
    return {
      timeInfo,
      locationInfo,
      participants,
      eventType,
      eventStatus,
      importance,
      confidence: this.calculateConfidence(text, timeInfo, eventType),
      metadata: {
        extractionMethod: 'rule',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取时间信息
   */
  extractTimeInfo(text) {
    const timeInfo = {
      dates: [],
      times: [],
      durations: [],
      recurrence: []
    };
    
    // 日期模式
    const datePatterns = [
      { regex: /(\d{4})年(\d{1,2})月(\d{1,2})日/, type: 'full_date' },
      { regex: /(\d{1,2})月(\d{1,2})日/, type: 'month_day' },
      { regex: /(今天|明天|后天|大后天)/, type: 'relative_date' },
      { regex: /(昨天|前天|大前天)/, type: 'past_relative_date' },
      { regex: /(下[周一二三四五六日]|上[周一二三四五六日])/, type: 'week_day' },
      { regex: /(下周|上周|这周)/, type: 'week_relative' }
    ];
    
    for (const pattern of datePatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        timeInfo.dates.push({
          type: pattern.type,
          value: matches[0],
          normalized: this.normalizeDate(matches[0]),
          confidence: 0.9
        });
      }
    }
    
    // 时间模式
    const timePatterns = [
      { regex: /(\d{1,2})[:：](\d{1,2})/, type: 'exact_time' },
      { regex: /(上午|下午|晚上|凌晨|早晨|中午)\s*(\d{1,2})?点?/, type: 'period_time' },
      { regex: /(\d{1,2})点(\d{1,2})?分?/, type: 'chinese_time' }
    ];
    
    for (const pattern of timePatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        timeInfo.times.push({
          type: pattern.type,
          value: matches[0],
          normalized: this.normalizeTime(matches[0]),
          confidence: 0.9
        });
      }
    }
    
    // 持续时间
    const durationPatterns = [
      { regex: /(\d+)(小时|分钟|天|周|月)/, type: 'duration' },
      { regex: /持续(\d+)(小时|分钟|天)/, type: 'continuous' },
      { regex: /(半天|一天|两天|一周|一个月)/, type: 'approximate_duration' }
    ];
    
    for (const pattern of durationPatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        timeInfo.durations.push({
          type: pattern.type,
          value: matches[0],
          confidence: 0.8
        });
      }
    }
    
    // 重复模式
    const recurrencePatterns = [
      { regex: /每天/, type: 'daily' },
      { regex: /每周/, type: 'weekly' },
      { regex: /每月/, type: 'monthly' },
      { regex: /每年/, type: 'yearly' },
      { regex: /每个工作日/, type: 'workday' }
    ];
    
    for (const pattern of recurrencePatterns) {
      if (pattern.regex.test(text)) {
        timeInfo.recurrence.push({
          type: pattern.type,
          value: pattern.regex.source,
          confidence: 0.9
        });
      }
    }
    
    return timeInfo;
  },
  
  /**
   * 提取地点信息
   */
  extractLocationInfo(text) {
    const locations = [];
    
    // 地点关键词
    const locationKeywords = [
      '会议室', '办公室', '公司', '家', '学校', '医院',
      '餐厅', '咖啡厅', '酒店', '机场', '车站', '公园'
    ];
    
    for (const keyword of locationKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 15);
        locations.push({
          type: 'venue',
          value: keyword,
          context: context,
          confidence: 0.8
        });
      }
    }
    
    // 地址模式
    const addressPatterns = [
      /[\u4e00-\u9fa5]{2,10}(市|省|区|县|镇|村)/,
      /[\u4e00-\u9fa5]{2,10}(路|街|巷|道)\d+号/
    ];
    
    for (const pattern of addressPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        locations.push({
          type: 'address',
          value: matches[0],
          confidence: 0.7
        });
      }
    }
    
    return locations;
  },
  
  /**
   * 提取参与人员
   */
  extractParticipants(text) {
    const participants = [];
    
    // 人名模式
    const namePatterns = [
      /([\u4e00-\u9fa5]{2,4})(先生|女士|老师|教授|博士)/,
      /和([\u4e00-\u9fa5]{2,4})/,
      /与([\u4e00-\u9fa5]{2,4})/
    ];
    
    for (const pattern of namePatterns) {
      const matches = text.match(pattern);
      if (matches) {
        participants.push({
          name: matches[1],
          role: matches[2] || 'participant',
          confidence: 0.7
        });
      }
    }
    
    // 角色关键词
    const roleKeywords = [
      { keyword: '老板', role: 'boss' },
      { keyword: '同事', role: 'colleague' },
      { keyword: '客户', role: 'client' },
      { keyword: '朋友', role: 'friend' },
      { keyword: '家人', role: 'family' }
    ];
    
    for (const roleDef of roleKeywords) {
      if (text.includes(roleDef.keyword)) {
        participants.push({
          role: roleDef.role,
          keyword: roleDef.keyword,
          confidence: 0.6
        });
      }
    }
    
    return participants;
  },
  
  /**
   * 提取事件类型
   */
  extractEventType(text) {
    const types = [];
    
    const eventTypes = [
      { keywords: ['会议', '讨论', '研讨', '座谈'], type: 'meeting' },
      { keywords: ['约会', '见面', '聚餐', '聚会'], type: 'appointment' },
      { keywords: ['出差', '旅行', '旅游', '出行'], type: 'travel' },
      { keywords: ['培训', '学习', '课程', '讲座'], type: 'training' },
      { keywords: ['面试', '考试', '答辩', '评审'], type: 'examination' },
      { keywords: ['生日', '纪念日', '节日', '庆祝'], type: 'celebration' },
      { keywords: ['看病', '体检', '治疗', '复查'], type: 'medical' }
    ];
    
    for (const eventDef of eventTypes) {
      for (const keyword of eventDef.keywords) {
        if (text.includes(keyword)) {
          types.push({
            type: eventDef.type,
            keyword: keyword,
            confidence: 0.8
          });
          break;
        }
      }
    }
    
    return types;
  },
  
  /**
   * 提取事件状态
   */
  extractEventStatus(text) {
    const statuses = [];
    
    const statusKeywords = [
      { keywords: ['计划', '打算', '准备', '将要'], status: 'planned' },
      { keywords: ['进行中', '正在', '当前'], status: 'ongoing' },
      { keywords: ['完成', '结束', '已', '已经'], status: 'completed' },
      { keywords: ['取消', '推迟', '延期', '改期'], status: 'cancelled' }
    ];
    
    for (const statusDef of statusKeywords) {
      for (const keyword of statusDef.keywords) {
        if (text.includes(keyword)) {
          statuses.push({
            status: statusDef.status,
            keyword: keyword,
            confidence: 0.7
          });
          break;
        }
      }
    }
    
    return statuses;
  },
  
  /**
   * 提取重要程度
   */
  extractImportance(text) {
    const importance = {
      level: 'normal',
      indicators: []
    };
    
    const importanceKeywords = [
      { keywords: ['重要', '关键', '紧急', '必须'], level: 'high', value: 0.9 },
      { keywords: ['一般', '普通', '常规'], level: 'normal', value: 0.5 },
      { keywords: ['可选', '随意', '有空'], level: 'low', value: 0.3 }
    ];
    
    for (const impDef of importanceKeywords) {
      for (const keyword of impDef.keywords) {
        if (text.includes(keyword)) {
          importance.level = impDef.level;
          importance.indicators.push({
            keyword: keyword,
            value: impDef.value
          });
        }
      }
    }
    
    return importance;
  },
  
  /**
   * 提取上下文
   */
  extractContext(text, targetWord, windowSize = 15) {
    const index = text.indexOf(targetWord);
    if (index === -1) return '';
    
    const start = Math.max(0, index - windowSize);
    const end = Math.min(text.length, index + targetWord.length + windowSize);
    
    return text.substring(start, end);
  },
  
  /**
   * 标准化日期
   */
  normalizeDate(dateStr) {
    const today = new Date();
    const dateMap = {
      '今天': today.toISOString().split('T')[0],
      '明天': new Date(today.getTime() + 86400000).toISOString().split('T')[0],
      '后天': new Date(today.getTime() + 172800000).toISOString().split('T')[0],
      '昨天': new Date(today.getTime() - 86400000).toISOString().split('T')[0],
      '前天': new Date(today.getTime() - 172800000).toISOString().split('T')[0]
    };
    
    if (dateMap[dateStr]) {
      return dateMap[dateStr];
    }
    
    return dateStr;
  },
  
  /**
   * 标准化时间
   */
  normalizeTime(timeStr) {
    return timeStr.replace(/：/g, ':').replace(/点/g, ':').replace(/分/g, '');
  },
  
  /**
   * 计算置信度
   */
  calculateConfidence(text, timeInfo, eventType) {
    let confidence = 0.3;
    
    // 基于时间信息
    if (timeInfo.dates.length > 0) {
      confidence += 0.3;
    }
    if (timeInfo.times.length > 0) {
      confidence += 0.2;
    }
    
    // 基于事件类型
    if (eventType.length > 0) {
      confidence += 0.2;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 验证事件
   */
  async validate(event, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.6,
      issues: [],
      suggestions: []
    };
    
    const hasDate = event.extracted?.timeInfo?.dates?.length > 0;
    const hasTime = event.extracted?.timeInfo?.times?.length > 0;
    const hasType = event.extracted?.eventType?.length > 0;
    
    if (!hasDate) {
      validation.issues.push('事件缺少日期信息');
      validation.confidence *= 0.7;
    }
    
    if (!hasTime) {
      validation.suggestions.push('建议添加具体时间');
    }
    
    if (!hasType) {
      validation.suggestions.push('建议明确事件类型');
    }
    
    return validation;
  },
  
  /**
   * 合并相似事件
   */
  async mergeSimilar(event1, event2, context = {}) {
    const merged = {
      text: `${event1.text}；${event2.text}`,
      extracted: {
        ...event1.extracted,
        ...event2.extracted,
        timeInfo: {
          dates: [...(event1.extracted?.timeInfo?.dates || []), ...(event2.extracted?.timeInfo?.dates || [])],
          times: [...(event1.extracted?.timeInfo?.times || []), ...(event2.extracted?.timeInfo?.times || [])]
        },
        participants: [...(event1.extracted?.participants || []), ...(event2.extracted?.participants || [])]
      },
      importance: Math.max(event1.importance || 0.5, event2.importance || 0.5),
      timestamp: Math.max(event1.timestamp || Date.now(), event2.timestamp || Date.now()),
      metadata: {
        ...event1.metadata,
        ...event2.metadata,
        mergedFrom: [event1.id, event2.id],
        mergedAt: Date.now()
      }
    };
    
    return merged;
  }
};

export default events;
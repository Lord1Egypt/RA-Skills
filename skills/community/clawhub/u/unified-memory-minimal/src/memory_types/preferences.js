/**
 * Preferences Memory Handler - 偏好型记忆处理器
 */

import { logger } from '../logger.js';

export const preferences = {
  name: 'preferences',
  description: '处理偏好、习惯、喜好',
  
  /**
   * 从文本中提取偏好
   */
  async extract(text, context = {}) {
    logger.debug(`[PreferencesHandler] 提取偏好: ${text.substring(0, 100)}...`);
    
    // 提取喜好
    const likes = this.extractLikes(text);
    
    // 提取厌恶
    const dislikes = this.extractDislikes(text);
    
    // 提取习惯
    const habits = this.extractHabits(text);
    
    // 提取优先级
    const priorities = this.extractPriorities(text);
    
    // 提取风格偏好
    const stylePreferences = this.extractStylePreferences(text);
    
    // 提取约束条件
    const constraints = this.extractConstraints(text);
    
    return {
      likes,
      dislikes,
      habits,
      priorities,
      stylePreferences,
      constraints,
      confidence: this.calculateConfidence(text, likes, dislikes, habits),
      metadata: {
        extractionMethod: 'hybrid',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取喜好
   */
  extractLikes(text) {
    const likes = [];
    
    // 喜好关键词
    const likeKeywords = [
      '喜欢', '爱', '偏好', '倾向于', '更愿意', '首选',
      'like', 'love', 'prefer', 'favorite', 'enjoy'
    ];
    
    for (const keyword of likeKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 20);
        const target = this.extractPreferenceTarget(context, keyword);
        
        likes.push({
          keyword: keyword,
          target: target,
          context: context,
          type: 'like',
          confidence: 0.8
        });
      }
    }
    
    // 强度修饰词
    const intensityModifiers = [
      { word: '非常', multiplier: 1.2 },
      { word: '特别', multiplier: 1.3 },
      { word: '比较', multiplier: 0.8 },
      { word: '有点', multiplier: 0.6 }
    ];
    
    for (const modifier of intensityModifiers) {
      const pattern = new RegExp(`${modifier.word}(.{0,5})?(喜欢|爱|偏好)`);
      const match = text.match(pattern);
      if (match) {
        likes.push({
          type: 'intensified_like',
          modifier: modifier.word,
          intensity: modifier.multiplier,
          context: match[0],
          confidence: 0.9
        });
      }
    }
    
    return likes;
  },
  
  /**
   * 提取厌恶
   */
  extractDislikes(text) {
    const dislikes = [];
    
    // 厌恶关键词
    const dislikeKeywords = [
      '不喜欢', '讨厌', '厌恶', '反感', '避免', '拒绝',
      'dislike', 'hate', 'avoid', 'refuse'
    ];
    
    for (const keyword of dislikeKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 20);
        const target = this.extractPreferenceTarget(context, keyword);
        
        dislikes.push({
          keyword: keyword,
          target: target,
          context: context,
          type: 'dislike',
          confidence: 0.8
        });
      }
    }
    
    return dislikes;
  },
  
  /**
   * 提取习惯
   */
  extractHabits(text) {
    const habits = [];
    
    // 习惯关键词
    const habitKeywords = [
      '习惯', '通常', '总是', '经常', '一般', '惯例',
      'habit', 'usually', 'always', 'often', 'typically'
    ];
    
    for (const keyword of habitKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 25);
        
        habits.push({
          keyword: keyword,
          context: context,
          type: 'habit',
          confidence: 0.7
        });
      }
    }
    
    // 时间习惯
    const timeHabits = [
      { pattern: /早上.*习惯/, type: 'morning_habit' },
      { pattern: /晚上.*习惯/, type: 'evening_habit' },
      { pattern: /周末.*习惯/, type: 'weekend_habit' },
      { pattern: /工作日.*习惯/, type: 'workday_habit' }
    ];
    
    for (const habitDef of timeHabits) {
      const match = text.match(habitDef.pattern);
      if (match) {
        habits.push({
          type: habitDef.type,
          context: match[0],
          confidence: 0.8
        });
      }
    }
    
    return habits;
  },
  
  /**
   * 提取优先级
   */
  extractPriorities(text) {
    const priorities = [];
    
    // 优先级关键词
    const priorityKeywords = [
      { keywords: ['最重要', '首要', '第一优先', 'top priority'], level: 'highest', value: 1.0 },
      { keywords: ['重要', '优先', '关键'], level: 'high', value: 0.8 },
      { keywords: ['次要', '第二优先', '次要优先'], level: 'medium', value: 0.5 },
      { keywords: ['不重要', '低优先', '可选'], level: 'low', value: 0.2 }
    ];
    
    for (const priorityDef of priorityKeywords) {
      for (const keyword of priorityDef.keywords) {
        if (text.includes(keyword)) {
          const context = this.extractContext(text, keyword, 20);
          
          priorities.push({
            keyword: keyword,
            level: priorityDef.level,
            value: priorityDef.value,
            context: context,
            confidence: 0.8
          });
        }
      }
    }
    
    return priorities;
  },
  
  /**
   * 提取风格偏好
   */
  extractStylePreferences(text) {
    const styles = [];
    
    // 风格关键词
    const styleKeywords = [
      { keywords: ['简洁', '简单', '简约'], style: 'minimalist' },
      { keywords: ['详细', '详尽', '全面'], style: 'detailed' },
      { keywords: ['正式', '官方', '专业'], style: 'formal' },
      { keywords: ['随意', '轻松', '非正式'], style: 'casual' },
      { keywords: ['快速', '高效', '迅速'], style: 'fast' },
      { keywords: ['仔细', '认真', '细致'], style: 'careful' }
    ];
    
    for (const styleDef of styleKeywords) {
      for (const keyword of styleDef.keywords) {
        if (text.includes(keyword)) {
          styles.push({
            keyword: keyword,
            style: styleDef.style,
            confidence: 0.7
          });
        }
      }
    }
    
    return styles;
  },
  
  /**
   * 提取约束条件
   */
  extractConstraints(text) {
    const constraints = [];
    
    // 约束关键词
    const constraintKeywords = [
      '必须', '不能', '不要', '避免', '限制', '约束',
      'must', 'cannot', 'should not', 'avoid', 'limit'
    ];
    
    for (const keyword of constraintKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 20);
        
        constraints.push({
          keyword: keyword,
          context: context,
          type: 'constraint',
          confidence: 0.8
        });
      }
    }
    
    // 数量约束
    const quantityConstraints = [
      { pattern: /不超过(\d+)/, type: 'max' },
      { pattern: /至少(\d+)/, type: 'min' },
      { pattern: /(\d+)到(\d+)/, type: 'range' }
    ];
    
    for (const constraintDef of quantityConstraints) {
      const match = text.match(constraintDef.pattern);
      if (match) {
        constraints.push({
          type: 'quantity_constraint',
          constraintType: constraintDef.type,
          value: match[1],
          context: match[0],
          confidence: 0.9
        });
      }
    }
    
    return constraints;
  },
  
  /**
   * 提取偏好目标
   */
  extractPreferenceTarget(context, keyword) {
    const keywordIndex = context.indexOf(keyword);
    if (keywordIndex === -1) return '';
    
    // 提取关键词后面的内容
    const afterKeyword = context.substring(keywordIndex + keyword.length);
    
    // 提取到标点符号为止
    const match = afterKeyword.match(/^([^\u3002\uff1f\uff01\uff0c\u3001\uff1b]+)/);
    
    return match ? match[1].trim() : afterKeyword.trim();
  },
  
  /**
   * 提取上下文
   */
  extractContext(text, targetWord, windowSize = 20) {
    const index = text.indexOf(targetWord);
    if (index === -1) return '';
    
    const start = Math.max(0, index - windowSize);
    const end = Math.min(text.length, index + targetWord.length + windowSize);
    
    return text.substring(start, end);
  },
  
  /**
   * 计算置信度
   */
  calculateConfidence(text, likes, dislikes, habits) {
    let confidence = 0.3;
    
    // 基于喜好
    if (likes.length > 0) {
      confidence += Math.min(likes.length * 0.2, 0.4);
    }
    
    // 基于厌恶
    if (dislikes.length > 0) {
      confidence += Math.min(dislikes.length * 0.15, 0.3);
    }
    
    // 基于习惯
    if (habits.length > 0) {
      confidence += Math.min(habits.length * 0.1, 0.2);
    }
    
    // 基于偏好关键词
    const preferencePattern = /喜欢|不喜欢|偏好|习惯|讨厌/;
    if (preferencePattern.test(text)) {
      confidence += 0.2;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 验证偏好
   */
  async validate(preference, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.6,
      issues: [],
      suggestions: []
    };
    
    const hasLikes = preference.extracted?.likes?.length > 0;
    const hasDislikes = preference.extracted?.dislikes?.length > 0;
    const hasHabits = preference.extracted?.habits?.length > 0;
    
    if (!hasLikes && !hasDislikes && !hasHabits) {
      validation.isValid = false;
      validation.issues.push('未识别到明确的偏好信息');
      validation.confidence *= 0.5;
    }
    
    // 检查是否有具体目标
    const hasTarget = preference.extracted?.likes?.some(l => l.target) ||
                      preference.extracted?.dislikes?.some(d => d.target);
    
    if (!hasTarget) {
      validation.suggestions.push('建议明确偏好的具体对象');
    }
    
    return validation;
  },
  
  /**
   * 合并相似偏好
   */
  async mergeSimilar(pref1, pref2, context = {}) {
    const merged = {
      text: `${pref1.text}；${pref2.text}`,
      extracted: {
        ...pref1.extracted,
        ...pref2.extracted,
        likes: [...(pref1.extracted?.likes || []), ...(pref2.extracted?.likes || [])],
        dislikes: [...(pref1.extracted?.dislikes || []), ...(pref2.extracted?.dislikes || [])],
        habits: [...(pref1.extracted?.habits || []), ...(pref2.extracted?.habits || [])]
      },
      importance: Math.max(pref1.importance || 0.5, pref2.importance || 0.5),
      timestamp: Math.max(pref1.timestamp || Date.now(), pref2.timestamp || Date.now()),
      metadata: {
        ...pref1.metadata,
        ...pref2.metadata,
        mergedFrom: [pref1.id, pref2.id],
        mergedAt: Date.now()
      }
    };
    
    // 去重
    const seenLikes = new Set();
    merged.extracted.likes = merged.extracted.likes.filter(like => {
      const key = `${like.keyword}:${like.target}`;
      if (seenLikes.has(key)) return false;
      seenLikes.add(key);
      return true;
    });
    
    const seenDislikes = new Set();
    merged.extracted.dislikes = merged.extracted.dislikes.filter(dislike => {
      const key = `${dislike.keyword}:${dislike.target}`;
      if (seenDislikes.has(key)) return false;
      seenDislikes.add(key);
      return true;
    });
    
    return merged;
  },
  
  /**
   * 检测冲突偏好
   */
  detectConflicts(preference) {
    const conflicts = [];
    
    const likes = preference.extracted?.likes || [];
    const dislikes = preference.extracted?.dislikes || [];
    
    // 检查是否同时喜欢和讨厌同一个东西
    for (const like of likes) {
      for (const dislike of dislikes) {
        if (like.target && dislike.target && 
            this.isSimilar(like.target, dislike.target)) {
          conflicts.push({
            type: 'like_dislike_conflict',
            target: like.target,
            likeContext: like.context,
            dislikeContext: dislike.context,
            severity: 'high'
          });
        }
      }
    }
    
    return conflicts;
  },
  
  /**
   * 判断是否相似
   */
  isSimilar(text1, text2) {
    // 简单的相似度判断
    const normalized1 = text1.toLowerCase().trim();
    const normalized2 = text2.toLowerCase().trim();
    
    if (normalized1 === normalized2) return true;
    if (normalized1.includes(normalized2) || normalized2.includes(normalized1)) return true;
    
    return false;
  }
};

export default preferences;
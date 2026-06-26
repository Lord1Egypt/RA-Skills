/**
 * 增强版意图识别和回复生成器
 * 支持：关键词匹配、敏感词检测、评论分类、AI模型选择
 * 
 * 版本：v2.0
 * 更新日期：2026-04-02
 */

// ==================== 关键词规则 ====================
const KEYWORD_RULES = {
  rules: [],
  defaultAction: 'ai_generate'
};

// 关键词匹配函数
function matchKeywords(comment, rules) {
  if (!comment || !rules || rules.length === 0) {
    return null;
  }
  
  const normalizedComment = comment.toLowerCase();
  const matchedRules = [];
  
  for (const rule of rules) {
    if (!rule.enabled) continue;
    
    let isMatch = false;
    const matchType = rule.matchType || 'any';
    
    if (matchType === 'any') {
      // 任一关键词匹配即可
      isMatch = rule.keywords.some(kw => normalizedComment.includes(kw.toLowerCase()));
    } else if (matchType === 'all') {
      // 所有关键词都必须匹配
      isMatch = rule.keywords.every(kw => normalizedComment.includes(kw.toLowerCase()));
    } else if (matchType === 'exact') {
      // 精确匹配
      isMatch = rule.keywords.some(kw => normalizedComment === kw.toLowerCase());
    }
    
    if (isMatch) {
      matchedRules.push({
        id: rule.id,
        reply: rule.reply,
        priority: rule.priority || 99,
        matchedKeywords: rule.keywords.filter(kw => normalizedComment.includes(kw.toLowerCase()))
      });
    }
  }
  
  // 按优先级排序，返回最高优先级的规则
  if (matchedRules.length > 0) {
    matchedRules.sort((a, b) => a.priority - b.priority);
    return matchedRules[0];
  }
  
  return null;
}

// ==================== 敏感词检测 ====================
const SENSITIVE_WORDS = {
  severe: [],
  warning: [],
  notice: []
};

const ACTION_RULES = {
  severe: { action: 'auto_delete', notify: true, log: true },
  warning: { action: 'mark_pending', notify: true, log: true },
  notice: { action: 'log_only', notify: false, log: true }
};

function detectSensitiveWords(comment, sensitiveWords, actionRules) {
  if (!comment) {
    return { hasSensitive: false, level: null, matchedWords: [], action: null };
  }
  
  const normalizedComment = comment.toLowerCase();
  const result = { hasSensitive: false, level: null, matchedWords: [], action: null };
  
  // 检查严重级别
  if (sensitiveWords.severe && sensitiveWords.severe.length > 0) {
    const matched = sensitiveWords.severe.filter(sw => normalizedComment.includes(sw.toLowerCase()));
    if (matched.length > 0) {
      result.hasSensitive = true;
      result.level = 'severe';
      result.matchedWords = matched;
      result.action = actionRules.severe || { action: 'auto_delete' };
      return result;
    }
  }
  
  // 检查警告级别
  if (sensitiveWords.warning && sensitiveWords.warning.length > 0) {
    const matched = sensitiveWords.warning.filter(sw => normalizedComment.includes(sw.toLowerCase()));
    if (matched.length > 0) {
      result.hasSensitive = true;
      result.level = 'warning';
      result.matchedWords = matched;
      result.action = actionRules.warning || { action: 'mark_pending' };
      return result;
    }
  }
  
  // 检查提示级别
  if (sensitiveWords.notice && sensitiveWords.notice.length > 0) {
    const matched = sensitiveWords.notice.filter(sw => normalizedComment.includes(sw.toLowerCase()));
    if (matched.length > 0) {
      result.hasSensitive = true;
      result.level = 'notice';
      result.matchedWords = matched;
      result.action = actionRules.notice || { action: 'log_only' };
      return result;
    }
  }
  
  return result;
}

// ==================== 评论分类 ====================
const COMMENT_CATEGORIES = {
  inquiry: {
    name: '咨询',
    patterns: ['怎么', '如何', '什么', '哪', '吗', '？', '?', '请教', '求助'],
    handler: 'inquiry_handler'
  },
  praise: {
    name: '夸奖',
    patterns: ['好', '棒', '赞', '喜欢', '爱', '厉害', '牛', '强', '优秀', '完美'],
    handler: 'praise_handler'
  },
  complaint: {
    name: '吐槽/差评',
    patterns: ['差', '烂', '垃圾', '骗', '假', '投诉', '退款', '失望', '无语', '避雷'],
    handler: 'complaint_handler'
  },
  interaction: {
    name: '互动',
    patterns: ['@', '哈哈', '笑', '有趣', '转发', '收藏'],
    handler: 'interaction_handler'
  },
  spam: {
    name: '广告/垃圾',
    patterns: ['加微信', '加V', '加Q', '私信', '兼职', '赚钱', '免费领'],
    handler: 'spam_handler'
  }
};

function classifyComment(comment) {
  if (!comment) {
    return { category: 'unknown', confidence: 0 };
  }
  
  const normalizedComment = comment.toLowerCase();
  let bestMatch = { category: 'other', confidence: 0, matchedPatterns: [] };
  
  for (const [catKey, catConfig] of Object.entries(COMMENT_CATEGORIES)) {
    const matchedPatterns = catConfig.patterns.filter(p => normalizedComment.includes(p.toLowerCase()));
    
    if (matchedPatterns.length > 0) {
      const confidence = (matchedPatterns.length / catConfig.patterns.length) * 100;
      
      if (confidence > bestMatch.confidence) {
        bestMatch = {
          category: catKey,
          categoryName: catConfig.name,
          confidence: Math.min(confidence * 2, 100),
          matchedPatterns,
          handler: catConfig.handler
        };
      }
    }
  }
  
  return bestMatch;
}

// ==================== 主处理函数 ====================

/**
 * 分析评论并生成回复策略
 * @param {string} comment 用户评论
 * @param {object} options 配置选项 { keywordRules, sensitiveWords, actionRules }
 * @returns {object} 分析结果
 */
function analyzeComment(comment, options = {}) {
  const result = {
    comment: comment,
    timestamp: new Date().toISOString(),
    
    // 敏感词检测结果
    sensitiveCheck: null,
    
    // 分类结果
    classification: null,
    
    // 关键词匹配结果
    keywordMatch: null,
    
    // 最终处理建议
    recommendation: {
      action: 'ai_generate', // ai_generate | use_template | skip | manual_review
      reply: null,
      reason: null
    }
  };
  
  // 1. 敏感词检测（优先级最高）
  const sensitiveWords = options.sensitiveWords || SENSITIVE_WORDS;
  const actionRules = options.actionRules || ACTION_RULES;
  result.sensitiveCheck = detectSensitiveWords(comment, sensitiveWords, actionRules);
  
  if (result.sensitiveCheck.hasSensitive) {
    if (result.sensitiveCheck.level === 'severe') {
      result.recommendation.action = 'skip';
      result.recommendation.reason = `检测到严重敏感词：${result.sensitiveCheck.matchedWords.join(', ')}`;
      return result;
    }
    
    if (result.sensitiveCheck.level === 'warning') {
      result.recommendation.action = 'manual_review';
      result.recommendation.reason = `检测到可疑内容：${result.sensitiveCheck.matchedWords.join(', ')}，建议人工审核`;
      return result;
    }
  }
  
  // 2. 评论分类
  result.classification = classifyComment(comment);
  
  // 3. 关键词匹配
  const keywordRules = options.keywordRules || KEYWORD_RULES.rules;
  result.keywordMatch = matchKeywords(comment, keywordRules);
  
  if (result.keywordMatch) {
    result.recommendation.action = 'use_template';
    result.recommendation.reply = result.keywordMatch.reply;
    result.recommendation.reason = `命中关键词规则：${result.keywordMatch.matchedKeywords.join(', ')}`;
    return result;
  }
  
  // 4. 默认使用AI生成
  result.recommendation.action = 'ai_generate';
  result.recommendation.reason = '未命中关键词规则，使用AI生成回复';
  
  return result;
}

// ==================== 回复生成辅助函数 ====================

/**
 * 根据分类生成回复提示词
 * @param {object} classification 分类结果
 * @param {string} comment 原始评论
 * @returns {string} AI提示词
 */
function generatePromptForCategory(classification, comment) {
  const prompts = {
    inquiry: `用户咨询："${comment}"\n请生成一个热情、专业的回复，解答用户的疑问。回复要简洁明了，不超过100字。`,
    
    praise: `用户夸奖："${comment}"\n请生成一个感谢回复，表达真诚的谢意，可以适当互动。回复要热情亲切，不超过80字。`,
    
    complaint: `用户吐槽："${comment}"\n请生成一个安抚性的回复，表示理解和关注，建议用户私信沟通解决。回复要诚恳有礼，不超过100字。`,
    
    interaction: `用户互动："${comment}"\n请生成一个有趣的互动回复，拉近距离。回复要活泼有趣，不超过80字。`,
    
    spam: `检测到可能的垃圾评论："${comment}"\n建议忽略或删除此评论。`,
    
    other: `用户评论："${comment}"\n请生成一个积极、大方、热情的回复。回复要自然亲切，不超过100字。`
  };
  
  return prompts[classification.category] || prompts.other;
}

// ==================== 导出 ====================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // 核心函数
    analyzeComment,
    matchKeywords,
    detectSensitiveWords,
    classifyComment,
    generatePromptForCategory,
    
    // 配置
    KEYWORD_RULES,
    SENSITIVE_WORDS,
    ACTION_RULES,
    COMMENT_CATEGORIES
  };
}

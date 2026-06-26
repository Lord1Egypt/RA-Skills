/**
 * 增强版抖音评论检查脚本
 * 支持：敏感词检测、关键词匹配、评论分类、状态持久化
 * 
 * 版本：v2.0
 * 更新日期：2026-04-02
 * 
 * 使用方式：
 * browser act evaluate fn: "<此脚本内容>"
 * 
 * 返回格式：
 * {
 *   success: true,
 *   page: 'comments',
 *   videoTitle: '视频标题',
 *   comments: [
 *     {
 *       id, author, content, time, hasReplied,
 *       sensitiveCheck: { hasSensitive, level, matchedWords },
 *       classification: { category, categoryName, confidence },
 *       keywordMatch: { matched, ruleId, reply },
 *       recommendation: { action, reply, reason }
 *     }
 *   ],
 *   stats: { total, pending, sensitive, needManualReview }
 * }
 */

(function() {
  const result = {
    success: true,
    page: 'comments',
    videoTitle: '',
    comments: [],
    stats: {
      total: 0,
      pending: 0,
      sensitive: 0,
      needManualReview: 0
    }
  };

  // ==================== 配置（可从外部注入） ====================
  
  // 敏感词库
  const SENSITIVE_WORDS = {
    severe: [],
    warning: ['加微信', '加V', '加Q', '私信我', '转账', '付款'],
    notice: []
  };
  
  // 关键词规则
  const KEYWORD_RULES = [
    {
      id: 'kr_001',
      enabled: true,
      keywords: ['多少钱', '价格', '怎么卖', '什么价'],
      matchType: 'any',
      reply: '亲，欢迎咨询价格！请告诉我您想了解哪个产品，我来为您详细介绍～ 💕',
      priority: 1
    },
    {
      id: 'kr_002',
      enabled: true,
      keywords: ['有货吗', '还有吗', '有没有', '库存'],
      matchType: 'any',
      reply: '亲，大部分商品都有现货哦！具体哪款您想了解？我来帮您确认库存～ 📦',
      priority: 1
    },
    {
      id: 'kr_003',
      enabled: true,
      keywords: ['便宜点', '打折', '优惠', '少点'],
      matchType: 'any',
      reply: '宝宝，价格已经是最优惠啦，真的没办法再低了😭 不过关注我们，活动期间会有折扣哦！💕',
      priority: 1
    },
    {
      id: 'kr_004',
      enabled: true,
      keywords: ['发货了吗', '什么时候发', '物流', '快递'],
      matchType: 'any',
      reply: '亲，您的订单正在处理中，我们会尽快安排发货的！感谢您的耐心等待 🙏',
      priority: 1
    },
    {
      id: 'kr_005',
      enabled: true,
      keywords: ['好看', '喜欢', '赞', '棒', '厉害', '太好了'],
      matchType: 'any',
      reply: '谢谢宝宝的喜欢！❤️ 你的支持是我们最大的动力～ 下次还要来哦！🎉',
      priority: 2
    }
  ];
  
  // 分类模式
  const COMMENT_CATEGORIES = {
    inquiry: {
      name: '咨询',
      patterns: ['怎么', '如何', '什么', '哪', '吗', '？', '?', '请教', '求助']
    },
    praise: {
      name: '夸奖',
      patterns: ['好', '棒', '赞', '喜欢', '爱', '厉害', '牛', '强', '优秀', '完美']
    },
    complaint: {
      name: '吐槽/差评',
      patterns: ['差', '烂', '垃圾', '骗', '假', '投诉', '退款', '失望', '无语', '避雷']
    },
    interaction: {
      name: '互动',
      patterns: ['@', '哈哈', '笑', '有趣', '转发', '收藏']
    },
    spam: {
      name: '广告/垃圾',
      patterns: ['加微信', '加V', '兼职', '赚钱', '免费领']
    }
  };

  // ==================== 辅助函数 ====================
  
  // 敏感词检测
  function detectSensitiveWords(comment) {
    if (!comment) return { hasSensitive: false, level: null, matchedWords: [] };
    
    const normalized = comment.toLowerCase();
    
    // 检查警告级别
    const warningMatched = SENSITIVE_WORDS.warning.filter(sw => normalized.includes(sw.toLowerCase()));
    if (warningMatched.length > 0) {
      return { hasSensitive: true, level: 'warning', matchedWords: warningMatched };
    }
    
    return { hasSensitive: false, level: null, matchedWords: [] };
  }
  
  // 关键词匹配
  function matchKeywords(comment) {
    if (!comment) return null;
    
    const normalized = comment.toLowerCase();
    
    for (const rule of KEYWORD_RULES) {
      if (!rule.enabled) continue;
      
      const isMatch = rule.keywords.some(kw => normalized.includes(kw.toLowerCase()));
      if (isMatch) {
        return {
          matched: true,
          ruleId: rule.id,
          reply: rule.reply,
          matchedKeywords: rule.keywords.filter(kw => normalized.includes(kw.toLowerCase()))
        };
      }
    }
    
    return null;
  }
  
  // 评论分类
  function classifyComment(comment) {
    if (!comment) return { category: 'other', categoryName: '其他', confidence: 0 };
    
    const normalized = comment.toLowerCase();
    let bestMatch = { category: 'other', categoryName: '其他', confidence: 0 };
    
    for (const [catKey, catConfig] of Object.entries(COMMENT_CATEGORIES)) {
      const matchedPatterns = catConfig.patterns.filter(p => normalized.includes(p.toLowerCase()));
      
      if (matchedPatterns.length > 0) {
        const confidence = Math.min((matchedPatterns.length / catConfig.patterns.length) * 200, 100);
        if (confidence > bestMatch.confidence) {
          bestMatch = {
            category: catKey,
            categoryName: catConfig.name,
            confidence,
            matchedPatterns
          };
        }
      }
    }
    
    return bestMatch;
  }
  
  // 生成处理建议
  function generateRecommendation(comment, sensitiveCheck, keywordMatch) {
    // 敏感词拦截
    if (sensitiveCheck.hasSensitive && sensitiveCheck.level === 'warning') {
      return {
        action: 'manual_review',
        reply: null,
        reason: `检测到可疑内容：${sensitiveCheck.matchedWords.join(', ')}，建议人工审核`
      };
    }
    
    // 关键词模板回复
    if (keywordMatch && keywordMatch.matched) {
      return {
        action: 'use_template',
        reply: keywordMatch.reply,
        reason: `命中关键词规则：${keywordMatch.matchedKeywords.join(', ')}`
      };
    }
    
    // AI生成
    return {
      action: 'ai_generate',
      reply: null,
      reason: '未命中关键词规则，使用AI生成回复'
    };
  }

  // ==================== 页面解析 ====================
  
  // 检查是否在评论管理页面
  if (!window.location.href.includes('/comment')) {
    result.success = false;
    result.error = '当前不在评论管理页面';
    return JSON.stringify(result);
  }

  // 获取视频标题
  const titleSelectors = [
    '[class*="video-title"]',
    '[class*="works-title"]', 
    '[class*="title"]'
  ];
  
  for (const sel of titleSelectors) {
    const el = document.querySelector(sel);
    if (el && el.textContent.trim().length > 0 && el.textContent.trim().length < 200) {
      result.videoTitle = el.textContent.trim();
      break;
    }
  }

  // 解析评论列表
  const allItems = document.querySelectorAll('li, [role="listitem"]');
  
  allItems.forEach((item, idx) => {
    const itemText = item.textContent || '';
    if (itemText.includes('没有更多') || itemText.includes('有爱评论')) {
      return;
    }
    
    // 提取用户名
    let author = '';
    const nameEl = item.querySelector('[class*="name"]');
    if (nameEl) {
      author = nameEl.textContent.trim();
    }
    if (!author) {
      const textNodes = item.querySelectorAll('div > div, span');
      for (const node of textNodes) {
        const text = node.textContent.trim();
        if (text.length > 0 && text.length < 20 && !text.includes('分钟') && !text.includes('小时')) {
          author = text;
          break;
        }
      }
    }
    
    // 提取时间
    let time = '';
    const timePatterns = ['分钟前', '小时前', '天前', '刚刚', '-'];
    for (const pattern of timePatterns) {
      const match = itemText.match(new RegExp(`(\\d*${pattern})`));
      if (match) {
        time = match[1];
        break;
      }
    }
    
    // 提取评论内容
    let content = '';
    const contentCandidates = item.querySelectorAll('[class*="content"], [class*="text"]');
    for (const c of contentCandidates) {
      const text = c.textContent.trim();
      if (text.length > 0 && text !== author && !timePatterns.some(p => text.includes(p))) {
        content = text;
        break;
      }
    }
    
    // 检查是否已回复
    const hasAuthorTag = itemText.includes('作者') && itemText.indexOf('作者') < itemText.indexOf(content || 'x');
    const hasReplyBtn = itemText.includes('回复');
    
    // 有效评论处理
    if (content && content.length > 0 && !content.includes('有爱评论')) {
      result.stats.total++;
      
      // 执行分析
      const sensitiveCheck = detectSensitiveWords(content);
      const keywordMatch = matchKeywords(content);
      const classification = classifyComment(content);
      const recommendation = generateRecommendation(content, sensitiveCheck, keywordMatch);
      
      const commentInfo = {
        id: `comment_${idx}_${Date.now()}`,
        index: idx,
        author: author || '未知用户',
        time: time || '未知时间',
        content: content.substring(0, 200),
        hasReplied: hasAuthorTag,
        sensitiveCheck,
        classification,
        keywordMatch,
        recommendation
      };
      
      // 未回复的评论
      if (!hasAuthorTag && hasReplyBtn) {
        result.stats.pending++;
        result.comments.push(commentInfo);
        
        // 统计敏感评论
        if (sensitiveCheck.hasSensitive) {
          result.stats.sensitive++;
        }
        
        // 统计需人工审核
        if (recommendation.action === 'manual_review') {
          result.stats.needManualReview++;
        }
      }
    }
  });

  return JSON.stringify(result, null, 2);
})();

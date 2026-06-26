/**
 * PARA Classifier - PARA分类器
 * 基于Tiago Forte的PARA方法进行分类
 * Projects(项目) / Areas(领域) / Resources(资源) / Archive(归档)
 */

class ParaClassifier {
  constructor() {
    // PARA分类定义
    this.categories = {
      PROJECTS: 'projects',    // 有明确目标和截止日期的项目
      AREAS: 'areas',          // 长期负责的标准和责任领域
      RESOURCES: 'resources',  // 感兴趣的主题和参考资料
      ARCHIVE: 'archive',      // 已完成或不活跃的项目和领域
      INBOX: 'inbox',          // 待分类（临时状态）
    };

    // 分类规则库
    this.classificationRules = {
      // 项目特征：有明确目标、截止日期、可交付成果
      projects: {
        keywords: [
          '项目', 'project', '完成', 'finish', '交付', 'deliver',
          '上线', 'launch', '发布', 'release', '实施', 'implement',
          '开发', 'develop', '设计', 'design', '编写', 'write',
          '准备', 'prepare', '组织', 'organize', '策划', 'plan',
          '搭建', 'build', '创建', 'create', '迁移', 'migrate',
        ],
        indicators: [
          /\d{4}[-/年]\d{1,2}[-/月]\d{1,2}/,  // 日期
          /截止|deadline|due/i,
          /目标|goal|objective/i,
          /里程碑|milestone/i,
          /第[一二三四五六七八九十\d]+阶段/,
          /v\d+\.\d+/,  // 版本号
        ],
        taskTypes: ['feature', 'bugfix', 'project'],
        contentTypes: ['task'],
        minUrgency: 7,  // 项目通常有较高紧急度
      },

      // 领域特征：长期维护、无明确截止日期、持续责任
      areas: {
        keywords: [
          '维护', 'maintain', '管理', 'manage', '运营', 'operate',
          '健康', 'health', '财务', 'finance', '家庭', 'family',
          '学习', 'learning', '成长', 'growth', '关系', 'relationship',
          '职业', 'career', '技能', 'skill', '习惯', 'habit',
          '责任', 'responsibility', '职责', 'duty',
          '定期', 'regular', '每周', '每月', 'weekly', 'monthly',
          '持续', 'ongoing', '长期', 'long-term',
        ],
        indicators: [
          /每周|每月|每天|日常|daily|weekly|monthly/i,
          /例行|routine/i,
          /跟踪|track/i,
          /监控|monitor/i,
          /优化|optimize/i,
        ],
        taskTypes: ['review', 'meeting', 'maintenance'],
        contentTypes: ['note', 'article'],
        maxUrgency: 6,  // 领域通常紧急度适中
      },

      // 资源特征：参考信息、感兴趣的主题、学习材料
      resources: {
        keywords: [
          '参考', 'reference', '资料', 'material', '学习', 'study',
          '教程', 'tutorial', '指南', 'guide', '文档', 'documentation',
          '文章', 'article', '书籍', 'book', '论文', 'paper',
          '工具', 'tool', '框架', 'framework', '库', 'library',
          '技巧', 'tip', '方法', 'method', '最佳实践', 'best practice',
          '灵感', 'inspiration', '想法', 'idea', '笔记', 'note',
          '收藏', 'bookmark', '稍后阅读', 'read later',
        ],
        indicators: [
          /链接|link|url/i,
          /收藏|save/i,
          /推荐|recommend/i,
          /分享|share/i,
          /有趣|interesting/i,
          /有用|useful/i,
        ],
        taskTypes: ['learning', 'reading'],
        contentTypes: ['article', 'video', 'podcast', 'book', 'paper', 'code', 'link', 'note'],
        maxUrgency: 5,  // 资源通常紧急度较低
      },

      // 归档特征：已完成、过期、不再活跃
      archive: {
        keywords: [
          '已完成', 'completed', 'done', '结束', 'finished',
          '过期', 'expired', '作废', 'obsolete', '废弃', 'deprecated',
          '历史', 'history', '过去', 'past', '旧', 'old',
          '存档', 'archive', '备份', 'backup',
          '取消', 'cancelled', '放弃', 'abandoned',
        ],
        indicators: [
          /已完成|done|completed/i,
          /已取消|cancelled/i,
          /过期|expired/i,
          /归档|archived/i,
          /旧版|old version/i,
          /历史记录|history/i,
        ],
        taskTypes: [],
        contentTypes: [],
        specialFlag: true,  // 需要特殊标记
      },
    };

    // 主题映射（用于关联性检测）
    this.topicMappings = {
      '技术': ['projects', 'resources'],
      '工作': ['projects', 'areas'],
      '学习': ['resources', 'areas'],
      '生活': ['areas', 'resources'],
      '健康': ['areas'],
      '财务': ['areas'],
      '家庭': ['areas'],
      '兴趣': ['resources'],
      '灵感': ['resources'],
    };
  }

  /**
   * 对内容进行PARA分类
   * @param {Object} contentAnalysis - 内容分析结果
   * @param {Object} urgencyScore - 紧急度评分结果
   * @returns {Object} 分类结果
   */
  classify(contentAnalysis, urgencyScore = {}) {
    const { type, metadata, wordCount } = contentAnalysis;
    const { score: urgency = 5, reasons = [] } = urgencyScore;
    
    // 计算各分类的匹配分数
    const scores = this._calculateScores(contentAnalysis, urgency);
    
    // 确定主分类
    const primaryCategory = this._determinePrimaryCategory(scores, contentAnalysis);
    
    // 确定置信度
    const confidence = this._calculateConfidence(scores, primaryCategory);
    
    // 生成分类理由
    const classificationReasons = this._generateReasons(primaryCategory, contentAnalysis, scores);
    
    return {
      category: primaryCategory,
      confidence,
      scores,  // 各分类的详细分数
      reasons: classificationReasons,
      suggestions: this._generateSuggestions(primaryCategory, contentAnalysis),
      // 子分类建议
      subcategory: this._suggestSubcategory(primaryCategory, contentAnalysis),
    };
  }

  /**
   * 计算各分类的匹配分数
   */
  _calculateScores(analysis, urgency) {
    const scores = {
      projects: 0,
      areas: 0,
      resources: 0,
      archive: 0,
    };

    const { type, metadata, wordCount } = analysis;
    const title = metadata.title || '';
    const description = metadata.description || '';
    const tags = metadata.tags || [];
    const text = `${title} ${description} ${tags.join(' ')}`;

    // 对每个分类计算匹配度
    for (const [category, rules] of Object.entries(this.classificationRules)) {
      if (category === 'archive') continue;  // 归档特殊处理

      let score = 0;

      // 关键词匹配
      for (const keyword of rules.keywords) {
        if (text.toLowerCase().includes(keyword.toLowerCase())) {
          score += 2;
        }
      }

      // 指示器匹配
      for (const indicator of rules.indicators) {
        if (indicator.test(text)) {
          score += 3;
        }
      }

      // 内容类型匹配
      if (rules.contentTypes.includes(type)) {
        score += 2;
      }

      // 紧急度匹配
      if (rules.minUrgency && urgency >= rules.minUrgency) {
        score += 2;
      }
      if (rules.maxUrgency && urgency <= rules.maxUrgency) {
        score += 1;
      }

      scores[category] = score;
    }

    // 归档检测（特殊逻辑）
    scores.archive = this._detectArchiveSignals(analysis);

    return scores;
  }

  /**
   * 检测归档信号
   */
  _detectArchiveSignals(analysis) {
    const { metadata } = analysis;
    const text = `${metadata.title || ''} ${metadata.description || ''}`;
    const rules = this.classificationRules.archive;
    
    let score = 0;
    
    for (const keyword of rules.keywords) {
      if (text.toLowerCase().includes(keyword.toLowerCase())) {
        score += 5;
      }
    }
    
    for (const indicator of rules.indicators) {
      if (indicator.test(text)) {
        score += 5;
      }
    }
    
    return score;
  }

  /**
   * 确定主分类
   */
  _determinePrimaryCategory(scores, analysis) {
    // 如果归档信号很强，直接归档
    if (scores.archive >= 10) {
      return 'archive';
    }

    // 排除归档后找最高分
    const validScores = { ...scores };
    delete validScores.archive;
    
    const entries = Object.entries(validScores);
    entries.sort((a, b) => b[1] - a[1]);
    
    // 如果最高分太低，放入收件箱
    if (entries[0][1] < 3) {
      return 'inbox';
    }
    
    return entries[0][0];
  }

  /**
   * 计算分类置信度
   */
  _calculateConfidence(scores, primaryCategory) {
    const primaryScore = scores[primaryCategory];
    const totalScore = Object.values(scores).reduce((a, b) => a + b, 0);
    
    if (totalScore === 0) return 0.3;
    
    // 计算主分类占比
    const ratio = primaryScore / totalScore;
    
    // 根据分数差距计算置信度
    const sortedScores = Object.values(scores).sort((a, b) => b - a);
    const gap = sortedScores[0] - sortedScores[1];
    
    let confidence = 0.5 + (ratio * 0.3) + (Math.min(gap, 10) / 10 * 0.2);
    
    return Math.min(confidence, 0.95);
  }

  /**
   * 生成分类理由
   */
  _generateReasons(category, analysis, scores) {
    const reasons = [];
    const { type, metadata } = analysis;
    const text = `${metadata.title || ''} ${metadata.description || ''}`;
    
    // 基于分类类型生成理由
    const rules = this.classificationRules[category];
    if (rules) {
      // 检查匹配的关键词
      for (const keyword of rules.keywords) {
        if (text.toLowerCase().includes(keyword.toLowerCase())) {
          reasons.push(`包含关键词"${keyword}"`);
          break;  // 只显示第一个匹配的关键词
        }
      }
      
      // 检查内容类型
      if (rules.contentTypes && rules.contentTypes.includes(type)) {
        reasons.push(`内容类型"${type}"符合${category}特征`);
      }
    }
    
    // 如果理由太少，添加分数信息
    if (reasons.length < 2) {
      reasons.push(`分类匹配分数: ${scores[category]}`);
    }
    
    return reasons;
  }

  /**
   * 生成建议
   */
  _generateSuggestions(category, analysis) {
    const suggestions = [];
    const { type, metadata } = analysis;
    
    switch (category) {
      case 'projects':
        suggestions.push('设置明确的里程碑和截止日期');
        suggestions.push('关联到相关的领域(Area)');
        if (type === 'task') {
          suggestions.push('分解为更小的可执行任务');
        }
        break;
      case 'areas':
        suggestions.push('建立定期回顾机制（建议每周/每月）');
        suggestions.push('维护相关的标准和检查清单');
        break;
      case 'resources':
        suggestions.push('添加标签以便检索');
        suggestions.push('记录来源和获取时间');
        if (type === 'article' || type === 'video') {
          suggestions.push('提取关键要点和行动项');
        }
        break;
      case 'archive':
        suggestions.push('确保已完成或不再需要');
        suggestions.push('保留关键信息摘要');
        break;
      case 'inbox':
        suggestions.push('尽快处理并重新分类');
        suggestions.push('补充更多上下文信息');
        break;
    }
    
    return suggestions;
  }

  /**
   * 建议子分类
   */
  _suggestSubcategory(category, analysis) {
    const { metadata, type } = analysis;
    const tags = metadata.tags || [];
    
    // 基于标签和类型推断子分类
    const subcategoryMap = {
      projects: {
        '技术': 'tech-project',
        '工作': 'work-project',
        '个人': 'personal-project',
        '学习': 'learning-project',
      },
      areas: {
        '健康': 'health',
        '财务': 'finance',
        '家庭': 'family',
        '职业': 'career',
        '学习': 'learning',
        '技能': 'skills',
      },
      resources: {
        '技术': 'tech-resource',
        '文章': 'article-collection',
        '书籍': 'book-collection',
        '工具': 'tools',
        '教程': 'tutorials',
      },
    };
    
    const map = subcategoryMap[category];
    if (!map) return null;
    
    // 检查标签匹配
    for (const tag of tags) {
      for (const [key, value] of Object.entries(map)) {
        if (tag.includes(key)) {
          return value;
        }
      }
    }
    
    // 基于类型推断
    if (category === 'resources') {
      if (type === 'code') return 'code-snippets';
      if (type === 'book') return 'books';
      if (type === 'article') return 'articles';
      if (type === 'video') return 'videos';
    }
    
    return null;
  }

  /**
   * 获取PARA分类说明
   */
  getCategoryDescription(category) {
    const descriptions = {
      projects: {
        name: '项目 (Projects)',
        description: '有明确目标和截止日期的短期努力',
        examples: ['开发新功能', '完成报告', '组织活动'],
        criteria: ['有明确目标', '有截止日期', '可交付成果'],
      },
      areas: {
        name: '领域 (Areas)',
        description: '长期负责的标准和责任领域',
        examples: ['健康管理', '财务管理', '技能提升'],
        criteria: ['长期维护', '无明确截止日期', '持续责任'],
      },
      resources: {
        name: '资源 (Resources)',
        description: '感兴趣的主题和参考资料',
        examples: ['技术文章', '学习笔记', '工具库'],
        criteria: ['参考信息', '感兴趣', '可能有用'],
      },
      archive: {
        name: '归档 (Archive)',
        description: '已完成或不活跃的项目和领域',
        examples: ['已完成项目', '过期资料', '历史记录'],
        criteria: ['不再活跃', '已完成', '保留备查'],
      },
      inbox: {
        name: '收件箱 (Inbox)',
        description: '待分类的临时存储',
        examples: ['新想法', '待处理链接', '快速笔记'],
        criteria: ['尚未分类', '需要处理'],
      },
    };
    
    return descriptions[category] || null;
  }
}

module.exports = ParaClassifier;
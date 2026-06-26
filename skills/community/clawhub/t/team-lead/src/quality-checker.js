/**
 * Team Lead - Quality Checker
 * 质量审核器 - 检查结果质量并提供反馈
 */

export class QualityChecker {
  constructor(options = {}) {
    this.options = {
      qualityThreshold: 0.75,
      enableAutoFix: false,
      ...options
    };
    this.checkHistory = [];
  }

  /**
   * 检查单个结果质量
   */
  async check(result, criteria = {}) {
    const startTime = Date.now();
    
    const checks = {
      completeness: this.checkCompleteness(result, criteria),
      accuracy: await this.checkAccuracy(result, criteria),
      consistency: this.checkConsistency(result, criteria),
      format: this.checkFormat(result, criteria),
      relevance: this.checkRelevance(result, criteria)
    };

    const scores = {
      completeness: this.scoreCheck(checks.completeness),
      accuracy: this.scoreCheck(checks.accuracy),
      consistency: this.scoreCheck(checks.consistency),
      format: this.scoreCheck(checks.format),
      relevance: this.scoreCheck(checks.relevance)
    };

    // 加权总分
    const weights = criteria.weights || {
      completeness: 0.25,
      accuracy: 0.30,
      consistency: 0.20,
      format: 0.10,
      relevance: 0.15
    };

    const totalScore = Object.entries(scores).reduce(
      (sum, [key, score]) => sum + score * (weights[key] || 0.2),
      0
    );

    const qualityReport = {
      subtaskId: result.subtaskId,
      agentId: result.agentId,
      overallScore: totalScore,
      passed: totalScore >= this.options.qualityThreshold,
      scores,
      checks,
      feedback: this.generateFeedback(checks, scores),
      suggestions: this.generateSuggestions(checks),
      checkedAt: Date.now(),
      checkDuration: Date.now() - startTime
    };

    // 记录历史
    this.checkHistory.push(qualityReport);

    return qualityReport;
  }

  /**
   * 检查完整性
   */
  checkCompleteness(result, criteria) {
    const content = result.result || result;
    const text = content?.toString() || '';

    const checks = {
      hasContent: text.length > 0,
      hasStructure: this.hasGoodStructure(text),
      meetsLength: text.length >= (criteria.minLength || 50),
      coversRequirements: this.coversRequirements(text, criteria.requirements)
    };

    return {
      type: 'completeness',
      checks,
      passed: Object.values(checks).every(c => c),
      details: checks
    };
  }

  /**
   * 检查准确性（简化版，实际需要接入事实核查）
   */
  async checkAccuracy(result, criteria) {
    const content = result.result || result;
    const text = content?.toString() || '';

    // 简单检查：是否存在明显的不确定表述
    const uncertainPhrases = [
      '可能', '也许', '大概', '不确定', '听说', '据说',
      'might', 'maybe', 'perhaps', 'unsure', 'i think'
    ];

    const uncertaintyCount = uncertainPhrases.filter(phrase => 
      text.toLowerCase().includes(phrase)
    ).length;

    // 检查是否有来源引用
    const hasSources = /https?:\/\/|来源 | 参考|according to|source/i.test(text);

    // 检查是否有具体数据
    const hasData = /\d+(?:\.\d+)?%|\d+(?:,\d{3})*(?:\.\d+)?/.test(text);

    return {
      type: 'accuracy',
      checks: {
        hasSources,
        hasData,
        lowUncertainty: uncertaintyCount < 3,
        noContradictions: true // 简化：假设无矛盾
      },
      passed: hasSources || hasData,
      details: {
        uncertaintyCount,
        hasSources,
        hasData
      }
    };
  }

  /**
   * 检查一致性
   */
  checkConsistency(result, criteria) {
    const content = result.result || result;
    const text = content?.toString() || '';

    // 检查内部一致性
    const numbers = text.match(/\d+(?:\.\d+)?/g) || [];
    const dates = text.match(/\d{4}-\d{2}-\d{2}/g) || [];

    // 简单检查：数字和日期是否自相矛盾（简化版）
    const hasConsistentNumbers = numbers.length < 2 || 
      this.areNumbersConsistent(numbers);

    return {
      type: 'consistency',
      checks: {
        consistentNumbers: hasConsistentNumbers,
        consistentDates: dates.length < 2 || true, // 简化
        consistentTerminology: this.checkTerminologyConsistency(text)
      },
      passed: hasConsistentNumbers,
      details: {
        numberCount: numbers.length,
        dateCount: dates.length
      }
    };
  }

  /**
   * 检查格式
   */
  checkFormat(result, criteria) {
    const content = result.result || result;
    const text = content?.toString() || '';

    const expectedFormat = criteria.expectedFormat || 'markdown';

    const formatChecks = {
      isMarkdown: /^#{1,6}\s+/m.test(text) || /^[\s]*[-*•]\s+/m.test(text),
      hasHeadings: /^#{1,6}\s+/m.test(text),
      hasParagraphs: text.split('\n\n').length > 1,
      hasLists: /^[\s]*[-*•]\s+/m.test(text),
      noFormattingErrors: !/\*\*{2,}|_{3,}/.test(text)
    };

    return {
      type: 'format',
      checks: formatChecks,
      passed: formatChecks.isMarkdown && formatChecks.noFormattingErrors,
      details: formatChecks
    };
  }

  /**
   * 检查相关性
   */
  checkRelevance(result, criteria) {
    const content = result.result || result;
    const text = content?.toString() || '';

    const taskKeywords = criteria.keywords || [];
    const taskType = criteria.taskType || '';

    // 检查是否包含任务关键词
    const keywordMatches = taskKeywords.filter(keyword =>
      text.toLowerCase().includes(keyword.toLowerCase())
    );

    const keywordMatchRate = taskKeywords.length > 0 
      ? keywordMatches.length / taskKeywords.length 
      : 1;

    // 检查是否偏离主题（简化：检查长度是否合理）
    const isOnTopic = text.length > 50 && text.length < 50000;

    return {
      type: 'relevance',
      checks: {
        hasKeywords: keywordMatchRate > 0.5,
        keywordMatchRate,
        isOnTopic,
        focusedContent: this.isFocusedContent(text)
      },
      passed: keywordMatchRate > 0.5 && isOnTopic,
      details: {
        matchedKeywords: keywordMatches,
        totalKeywords: taskKeywords.length
      }
    };
  }

  /**
   * 评分检查项
   */
  scoreCheck(check) {
    const passedCount = Object.values(check.checks).filter(Boolean).length;
    const totalCount = Object.keys(check.checks).length;
    
    if (totalCount === 0) return 0.5;
    
    const baseScore = passedCount / totalCount;
    
    // 如果关键检查失败，降低分数
    const criticalChecks = ['hasContent', 'isOnTopic', 'noFormattingErrors'];
    const criticalFailures = criticalChecks.filter(key => check.checks[key] === false).length;
    
    return Math.max(0, baseScore - criticalFailures * 0.2);
  }

  /**
   * 生成反馈
   */
  generateFeedback(checks, scores) {
    const feedback = [];

    if (scores.completeness < 0.7) {
      feedback.push({
        area: 'completeness',
        level: 'warning',
        message: '内容完整性不足，建议补充更多细节'
      });
    }

    if (scores.accuracy < 0.7) {
      feedback.push({
        area: 'accuracy',
        level: 'warning',
        message: '建议添加来源引用和具体数据支持'
      });
    }

    if (scores.format < 0.7) {
      feedback.push({
        area: 'format',
        level: 'info',
        message: '格式可以进一步优化，建议使用标题和列表'
      });
    }

    if (scores.relevance < 0.7) {
      feedback.push({
        area: 'relevance',
        level: 'error',
        message: '内容可能偏离主题，请重新审视任务要求'
      });
    }

    return feedback;
  }

  /**
   * 生成改进建议
   */
  generateSuggestions(checks) {
    const suggestions = [];

    if (!checks.completeness?.checks?.hasStructure) {
      suggestions.push('添加标题和分段，提升内容结构');
    }

    if (!checks.accuracy?.checks?.hasSources) {
      suggestions.push('添加数据来源和参考链接');
    }

    if (!checks.format?.checks?.hasLists) {
      suggestions.push('使用列表呈现要点，提升可读性');
    }

    if (checks.relevance?.checks?.keywordMatchRate < 0.5) {
      suggestions.push('确保内容覆盖任务关键词');
    }

    return suggestions;
  }

  /**
   * 批量检查结果
   */
  async checkBatch(results, criteria = {}) {
    const reports = [];

    for (const result of results) {
      const report = await this.check(result, criteria);
      reports.push(report);
    }

    return {
      reports,
      summary: {
        total: reports.length,
        passed: reports.filter(r => r.passed).length,
        failed: reports.filter(r => !r.passed).length,
        avgScore: reports.reduce((sum, r) => sum + r.overallScore, 0) / reports.length,
        avgCheckTime: reports.reduce((sum, r) => sum + r.checkDuration, 0) / reports.length
      }
    };
  }

  /**
   * 辅助函数：检查内容结构
   */
  hasGoodStructure(text) {
    if (!text) return false;
    const hasHeaders = /^#{1,6}\s+/m.test(text);
    const hasLists = /^[\s]*[-*•]\s+/m.test(text);
    const hasSections = text.split('\n\n').length > 2;
    return hasHeaders || hasLists || hasSections;
  }

  /**
   * 辅助函数：检查需求覆盖
   */
  coversRequirements(text, requirements = []) {
    if (!requirements || requirements.length === 0) return true;
    
    const coveredCount = requirements.filter(req =>
      text.toLowerCase().includes(req.toLowerCase())
    ).length;

    return coveredCount >= requirements.length * 0.8;
  }

  /**
   * 辅助函数：检查数字一致性
   */
  areNumbersConsistent(numbers) {
    // 简化版：只检查是否有明显异常值
    const numericValues = numbers.map(n => parseFloat(n)).filter(n => !isNaN(n));
    if (numericValues.length < 2) return true;

    const avg = numericValues.reduce((a, b) => a + b, 0) / numericValues.length;
    const hasOutlier = numericValues.some(n => Math.abs(n - avg) > avg * 10);
    
    return !hasOutlier;
  }

  /**
   * 辅助函数：检查术语一致性
   */
  checkTerminologyConsistency(text) {
    // 简化版：检查常见术语变体
    const variants = [
      ['AI', '人工智能'],
      ['ML', '机器学习'],
      ['API', '接口']
    ];

    // 如果同时使用中英文术语，可能不一致（但不一定错误）
    let mixedCount = 0;
    variants.forEach(([en, zh]) => {
      const hasEn = text.includes(en);
      const hasZh = text.includes(zh);
      if (hasEn && hasZh) mixedCount++;
    });

    return mixedCount < 3; // 允许一定程度的混用
  }

  /**
   * 辅助函数：检查内容专注度
   */
  isFocusedContent(text) {
    // 简化版：检查段落长度分布
    const paragraphs = text.split('\n\n').filter(p => p.trim().length > 0);
    if (paragraphs.length === 0) return false;

    const lengths = paragraphs.map(p => p.length);
    const avgLength = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const variance = lengths.reduce((sum, l) => sum + Math.pow(l - avgLength, 2), 0) / lengths.length;
    const stdDev = Math.sqrt(variance);

    // 标准差过大可能表示内容不专注
    return stdDev < avgLength * 2;
  }

  /**
   * 获取质量统计
   */
  getStats() {
    if (this.checkHistory.length === 0) {
      return {
        totalChecks: 0,
        passRate: 0,
        avgScore: 0
      };
    }

    return {
      totalChecks: this.checkHistory.length,
      passRate: this.checkHistory.filter(r => r.passed).length / this.checkHistory.length,
      avgScore: this.checkHistory.reduce((sum, r) => sum + r.overallScore, 0) / this.checkHistory.length,
      scoreDistribution: this.getScoreDistribution()
    };
  }

  /**
   * 获取分数分布
   */
  getScoreDistribution() {
    const buckets = {
      '90-100': 0,
      '80-89': 0,
      '70-79': 0,
      '60-69': 0,
      'below-60': 0
    };

    this.checkHistory.forEach(report => {
      const score = report.overallScore * 100;
      if (score >= 90) buckets['90-100']++;
      else if (score >= 80) buckets['80-89']++;
      else if (score >= 70) buckets['70-79']++;
      else if (score >= 60) buckets['60-69']++;
      else buckets['below-60']++;
    });

    return buckets;
  }
}

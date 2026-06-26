/**
 * Second Brain Triage - 第二大脑信息分诊
 * 基于PARA方法的智能信息分类系统
 */

const ContentAnalyzer = require('./content-analyzer');
const ParaClassifier = require('./para-classifier');
const UrgencyScorer = require('./urgency-scorer');
const RelatednessDetector = require('./relatedness-detector');

class SecondBrainTriage {
  constructor(options = {}) {
    this.analyzer = new ContentAnalyzer();
    this.classifier = new ParaClassifier();
    this.scorer = new UrgencyScorer();
    this.detector = new RelatednessDetector();
    
    this.options = {
      enableRelatedness: true,
      urgencyThreshold: 5,
      ...options,
    };
  }

  /**
   * 对单个内容进行分诊
   * @param {string} content - 内容文本或URL
   * @param {Array} existingItems - 可选的现有内容列表（用于关联检测）
   * @returns {Object} 完整的分诊结果
   */
  triage(content, existingItems = []) {
    // 1. 内容分析
    const analysis = this.analyzer.analyze(content);
    
    // 2. 紧急度评分
    const urgency = this.scorer.calculate(analysis);
    
    // 3. PARA分类
    const classification = this.classifier.classify(analysis, urgency);
    
    // 4. 关联性检测（可选）
    let relatedness = null;
    if (this.options.enableRelatedness && existingItems.length > 0) {
      relatedness = this.detector.detect(analysis, existingItems);
    }

    return {
      input: content,
      analysis,
      urgency,
      classification,
      relatedness,
      timestamp: new Date().toISOString(),
      summary: this._generateSummary(analysis, urgency, classification),
    };
  }

  /**
   * 批量分诊
   * @param {Array} contents - 内容列表
   * @returns {Array} 分诊结果列表
   */
  triageBatch(contents) {
    // 先分析所有内容
    const analyses = contents.map(content => ({
      content,
      analysis: this.analyzer.analyze(content),
    }));

    // 紧急度评分
    const withUrgency = analyses.map(({ content, analysis }) => ({
      content,
      analysis,
      urgency: this.scorer.calculate(analysis),
    }));

    // PARA分类
    const withClassification = withUrgency.map(({ content, analysis, urgency }) => ({
      content,
      analysis,
      urgency,
      classification: this.classifier.classify(analysis, urgency),
    }));

    // 关联性检测（基于已分析的内容）
    const results = withClassification.map(({ content, analysis, urgency, classification }, index) => {
      const otherItems = withClassification
        .filter((_, idx) => idx !== index)
        .map(item => item.analysis);
      
      const relatedness = this.options.enableRelatedness 
        ? this.detector.detect(analysis, otherItems)
        : null;

      return {
        input: content,
        analysis,
        urgency,
        classification,
        relatedness,
        timestamp: new Date().toISOString(),
        summary: this._generateSummary(analysis, urgency, classification),
      };
    });

    return results;
  }

  /**
   * 生成摘要
   */
  _generateSummary(analysis, urgency, classification) {
    const { type, metadata, wordCount } = analysis;
    const { score: urgencyScore, level: urgencyLevel } = urgency;
    const { category, confidence } = classification;

    return {
      title: metadata.title || '未命名',
      type,
      category: this._getCategoryLabel(category),
      urgency: urgencyLevel.label,
      urgencyScore,
      confidence,
      wordCount,
      readingTime: analysis.readingTime,
      action: urgency.recommendation,
      keyTags: metadata.tags?.slice(0, 5) || [],
    };
  }

  /**
   * 获取分类标签
   */
  _getCategoryLabel(category) {
    const labels = {
      projects: '项目',
      areas: '领域',
      resources: '资源',
      archive: '归档',
      inbox: '收件箱',
    };
    return labels[category] || category;
  }

  /**
   * 获取分类统计
   */
  getCategoryStats(results) {
    const stats = {
      projects: 0,
      areas: 0,
      resources: 0,
      archive: 0,
      inbox: 0,
    };

    const urgencyDistribution = {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
      none: 0,
    };

    for (const result of results) {
      const cat = result.classification.category;
      if (stats[cat] !== undefined) {
        stats[cat]++;
      }

      const level = result.urgency.level.level;
      if (urgencyDistribution[level] !== undefined) {
        urgencyDistribution[level]++;
      }
    }

    return {
      byCategory: stats,
      byUrgency: urgencyDistribution,
      total: results.length,
      highUrgency: urgencyDistribution.critical + urgencyDistribution.high,
    };
  }

  /**
   * 查找高紧急度项目
   */
  findHighUrgency(results, threshold = 7) {
    return results
      .filter(r => r.urgency.score >= threshold)
      .sort((a, b) => b.urgency.score - a.urgency.score);
  }

  /**
   * 查找需要关注的内容（收件箱或低置信度）
   */
  findNeedsAttention(results) {
    return results.filter(r => 
      r.classification.category === 'inbox' ||
      r.classification.confidence < 0.6
    );
  }

  /**
   * 导出为不同格式的报告
   */
  exportReport(results, format = 'json') {
    switch (format) {
      case 'json':
        return JSON.stringify(results, null, 2);
      
      case 'markdown':
        return this._exportMarkdown(results);
      
      case 'csv':
        return this._exportCsv(results);
      
      default:
        throw new Error(`不支持的格式: ${format}`);
    }
  }

  /**
   * 导出Markdown格式
   */
  _exportMarkdown(results) {
    const lines = ['# 信息分诊报告\n'];
    
    // 统计
    const stats = this.getCategoryStats(results);
    lines.push('## 统计概览\n');
    lines.push(`总计: ${stats.total} 项`);
    lines.push(`- 项目: ${stats.byCategory.projects}`);
    lines.push(`- 领域: ${stats.byCategory.areas}`);
    lines.push(`- 资源: ${stats.byCategory.resources}`);
    lines.push(`- 归档: ${stats.byCategory.archive}`);
    lines.push(`- 收件箱: ${stats.byCategory.inbox}\n`);

    // 高紧急度
    const highUrgency = this.findHighUrgency(results);
    if (highUrgency.length > 0) {
      lines.push('## 高紧急度项目\n');
      for (const item of highUrgency) {
        lines.push(`- [${item.urgency.score}] ${item.summary.title}`);
      }
      lines.push('');
    }

    // 按分类列出
    const byCategory = {
      projects: results.filter(r => r.classification.category === 'projects'),
      areas: results.filter(r => r.classification.category === 'areas'),
      resources: results.filter(r => r.classification.category === 'resources'),
      archive: results.filter(r => r.classification.category === 'archive'),
      inbox: results.filter(r => r.classification.category === 'inbox'),
    };

    for (const [cat, items] of Object.entries(byCategory)) {
      if (items.length === 0) continue;
      
      lines.push(`## ${this._getCategoryLabel(cat)} (${items.length})\n`);
      
      for (const item of items) {
        const s = item.summary;
        lines.push(`### ${s.title}`);
        lines.push(`- 类型: ${s.type}`);
        lines.push(`- 紧急度: ${s.urgency} (${s.urgencyScore})`);
        lines.push(`- 标签: ${s.keyTags.join(', ') || '无'}`);
        lines.push(`- 建议: ${s.action}\n`);
      }
    }

    return lines.join('\n');
  }

  /**
   * 导出CSV格式
   */
  _exportCsv(results) {
    const headers = ['标题', '类型', '分类', '紧急度', '置信度', '标签', '建议'];
    const lines = [headers.join(',')];

    for (const result of results) {
      const s = result.summary;
      const row = [
        `"${s.title}"`,
        s.type,
        s.category,
        s.urgencyScore,
        result.classification.confidence.toFixed(2),
        `"${s.keyTags.join(';')}"`,
        `"${s.action}"`,
      ];
      lines.push(row.join(','));
    }

    return lines.join('\n');
  }
}

// 导出模块
module.exports = {
  SecondBrainTriage,
  ContentAnalyzer,
  ParaClassifier,
  UrgencyScorer,
  RelatednessDetector,
};
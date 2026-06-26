/**
 * Team Lead - Result Aggregator
 * 整合多个 Agent 的输出结果
 */

export class ResultAggregator {
  constructor() {
    this.strategies = {
      merge: this.mergeResults.bind(this),
      'select-best': this.selectBest.bind(this),
      consensus: this.buildConsensus.bind(this),
      chain: this.chainResults.bind(this)
    };
  }

  /**
   * 聚合多个结果
   */
  async aggregate(results, strategy = 'merge', context = {}) {
    console.log(`[ResultAggregator] Aggregating ${results.length} results with strategy: ${strategy}`);
    
    const aggregator = this.strategies[strategy];
    if (!aggregator) {
      throw new Error(`Unknown aggregation strategy: ${strategy}`);
    }

    const aggregated = await aggregator(results, context);
    aggregated.strategy = strategy;
    aggregated.aggregatedAt = Date.now();
    aggregated.resultCount = results.length;

    return aggregated;
  }

  /**
   * 合并结果（适用于互补信息）
   */
  mergeResults(results, context) {
    const sections = results.map((r, i) => ({
      source: r.agentId || `agent-${i}`,
      subtaskId: r.subtaskId,
      content: r.result || r,
      order: i,
      quality: r.quality || 0.8
    }));

    return {
      type: 'merged',
      sections,
      summary: this.generateSummary(results),
      totalSections: sections.length,
      avgQuality: sections.reduce((sum, s) => sum + s.quality, 0) / sections.length
    };
  }

  /**
   * 选择最佳结果（适用于重复任务）
   */
  selectBest(results, context) {
    if (results.length === 0) {
      return {
        type: 'selected',
        best: null,
        alternatives: [],
        selectionReason: 'No results available'
      };
    }

    const scored = results.map((r, i) => ({
      ...r,
      index: i,
      score: this.scoreResult(r)
    }));

    scored.sort((a, b) => b.score - a.score);

    return {
      type: 'selected',
      best: scored[0],
      alternatives: scored.slice(1),
      selectionReason: this.explainSelection(scored[0], scored),
      scoreRange: {
        best: scored[0]?.score,
        worst: scored[scored.length - 1]?.score
      }
    };
  }

  /**
   * 构建共识（适用于有冲突的情况）
   */
  async buildConsensus(results, context) {
    const conflicts = this.detectConflicts(results);
    
    if (conflicts.length === 0) {
      // 无冲突，直接合并
      return {
        ...this.mergeResults(results, context),
        type: 'consensus',
        hasConflicts: false
      };
    }

    // 提取一致点
    const agreedPoints = this.extractAgreedPoints(results);

    // 解决冲突
    const resolution = await this.resolveConflicts(conflicts, results);

    return {
      type: 'consensus',
      agreedPoints,
      conflicts,
      resolution,
      confidence: this.calculateConfidence(results, conflicts),
      hasConflicts: true
    };
  }

  /**
   * 链式结果（前一个输出是后一个输入）
   */
  chainResults(results, context) {
    if (results.length === 0) {
      return {
        type: 'chained',
        finalResult: null,
        chain: []
      };
    }

    const chain = results.map((r, i) => ({
      step: i,
      agent: r.agentId || `agent-${i}`,
      subtaskId: r.subtaskId,
      input: i > 0 ? results[i - 1].result || results[i - 1] : null,
      output: r.result || r
    }));

    return {
      type: 'chained',
      finalResult: results[results.length - 1].result || results[results.length - 1],
      chain,
      totalSteps: chain.length
    };
  }

  /**
   * 检测结果冲突
   */
  detectConflicts(results) {
    const conflicts = [];
    
    // 简单冲突检测：比较关键数据点
    const dataPoints = this.extractDataPoints(results);
    
    for (const [key, values] of Object.entries(dataPoints)) {
      const uniqueValues = [...new Set(values.map(v => JSON.stringify(v)))];
      if (uniqueValues.length > 1) {
        conflicts.push({
          type: 'data_conflict',
          field: key,
          values: values,
          sources: results.map((r, i) => r.agentId || `agent-${i}`)
        });
      }
    }

    return conflicts;
  }

  /**
   * 提取数据点
   */
  extractDataPoints(results) {
    const dataPoints = {};
    
    results.forEach((result, index) => {
      const content = result.result || result;
      
      // 提取数字
      const numbers = content.toString().match(/\d+(?:\.\d+)?/g) || [];
      numbers.forEach(num => {
        if (!dataPoints[`number_${num}`]) dataPoints[`number_${num}`] = [];
        dataPoints[`number_${num}`].push({ source: index, value: num });
      });

      // 提取日期
      const dates = content.toString().match(/\d{4}-\d{2}-\d{2}/g) || [];
      dates.forEach(date => {
        if (!dataPoints[`date_${date}`]) dataPoints[`date_${date}`] = [];
        dataPoints[`date_${date}`].push({ source: index, value: date });
      });
    });

    return dataPoints;
  }

  /**
   * 提取一致点
   */
  extractAgreedPoints(results) {
    const points = [];
    const contentHash = new Map();

    // 简单实现：查找重复出现的关键句
    results.forEach((result, index) => {
      const content = result.result || result;
      const sentences = content.toString().split(/[.!?]/).filter(s => s.trim().length > 20);
      
      sentences.forEach(sentence => {
        const normalized = sentence.trim().toLowerCase();
        if (!contentHash.has(normalized)) {
          contentHash.set(normalized, []);
        }
        contentHash.get(normalized).push(index);
      });
    });

    // 出现在多个结果中的句子
    for (const [sentence, sources] of contentHash.entries()) {
      if (sources.length >= 2) {
        points.push({
          content: sentence,
          agreementCount: sources.length,
          sources
        });
      }
    }

    return points;
  }

  /**
   * 解决冲突
   */
  async resolveConflicts(conflicts, results) {
    const resolutions = [];

    for (const conflict of conflicts) {
      // 简单策略：选择来源质量最高的
      const qualityScores = conflict.values.map((_, i) => 
        results[i]?.quality || 0.8
      );
      
      const bestIndex = qualityScores.indexOf(Math.max(...qualityScores));

      resolutions.push({
        conflictType: conflict.type,
        field: conflict.field,
        selectedValue: conflict.values[bestIndex],
        selectedSource: conflict.sources[bestIndex],
        reason: 'Highest source quality',
        alternativeValues: conflict.values.filter((_, i) => i !== bestIndex)
      });
    }

    return resolutions;
  }

  /**
   * 计算置信度
   */
  calculateConfidence(results, conflicts) {
    const baseConfidence = results.reduce((sum, r) => sum + (r.quality || 0.8), 0) / results.length;
    const conflictPenalty = conflicts.length * 0.1;
    
    return Math.max(0, Math.min(1, baseConfidence - conflictPenalty));
  }

  /**
   * 评分结果
   */
  scoreResult(result) {
    let score = 0;

    // 完整性 (30%)
    const content = result.result || result;
    const contentLength = content?.toString().length || 0;
    score += Math.min(1, contentLength / 500) * 0.3;

    // 质量评分 (40%)
    score += (result.quality || 0.8) * 0.4;

    // 结构化程度 (30%)
    const hasStructure = this.hasGoodStructure(content);
    score += (hasStructure ? 1 : 0.5) * 0.3;

    return score;
  }

  /**
   * 检查内容结构
   */
  hasGoodStructure(content) {
    if (!content) return false;
    const text = content.toString();
    
    const hasHeaders = /^#{1,6}\s+/m.test(text);
    const hasLists = /^[\s]*[-*•]\s+/m.test(text);
    const hasSections = text.split('\n\n').length > 2;

    return hasHeaders || hasLists || hasSections;
  }

  /**
   * 生成摘要
   */
  generateSummary(results) {
    const sources = results.map(r => r.agentId || 'unknown').join(', ');
    const types = [...new Set(results.map(r => r.type || 'unknown'))].join(', ');
    
    return `整合了 ${results.length} 个 Agent 的输出 (来源：${sources}, 类型：${types})`;
  }

  /**
   * 解释选择原因
   */
  explainSelection(selected, all) {
    const scoreDiff = selected.score - (all[1]?.score || 0);
    
    if (scoreDiff > 0.2) {
      return `明显优于其他选项 (分数领先 ${Math.round(scoreDiff * 100)}%)`;
    } else if (scoreDiff > 0.05) {
      return `略优于其他选项 (分数领先 ${Math.round(scoreDiff * 100)}%)`;
    } else {
      return `多个选项质量相近，随机选择';
    }
  }

  /**
   * 格式化最终输出
   */
  formatOutput(aggregated, options = {}) {
    const { format = 'markdown', includeMetadata = true } = options;

    if (format === 'markdown') {
      return this.formatAsMarkdown(aggregated, includeMetadata);
    } else if (format === 'json') {
      return JSON.stringify(aggregated, null, 2);
    }

    return aggregated;
  }

  /**
   * 格式化为 Markdown
   */
  formatAsMarkdown(aggregated, includeMetadata) {
    let output = '';

    if (aggregated.type === 'merged') {
      output = '# 整合报告\n\n';
      aggregated.sections.forEach((section, i) => {
        output += `## ${section.source || 'Section ' + (i + 1)}\n\n`;
        output += `${section.content}\n\n`;
      });
    } else if (aggregated.type === 'selected') {
      output = '# 最佳结果\n\n';
      output += `**选择理由**: ${aggregated.selectionReason}\n\n`;
      output += `${aggregated.best.content || aggregated.best}\n\n`;
    } else if (aggregated.type === 'consensus') {
      output = '# 共识报告\n\n';
      
      if (aggregated.agreedPoints.length > 0) {
        output += '## 一致观点\n\n';
        aggregated.agreedPoints.forEach((point, i) => {
          output += `${i + 1}. ${point.content} (来自 ${point.agreementCount} 个来源)\n`;
        });
        output += '\n';
      }

      if (aggregated.conflicts.length > 0) {
        output += '## 冲突解决\n\n';
        aggregated.resolution.forEach((res, i) => {
          output += `${i + 1}. **${res.field}**: 采用 ${res.selectedSource} 的结果\n`;
          output += `   理由：${res.reason}\n\n`;
        });
      }
    } else if (aggregated.type === 'chained') {
      output = '# 链式执行结果\n\n';
      output += `## 最终结果\n\n${aggregated.finalResult}\n\n`;
      
      output += '## 执行链\n\n';
      aggregated.chain.forEach((step, i) => {
        output += `### 步骤 ${i + 1}: ${step.agent}\n\n`;
        output += `${step.output}\n\n`;
      });
    }

    if (includeMetadata) {
      output += '\n---\n';
      output += `*生成时间*: ${new Date(aggregated.aggregatedAt).toLocaleString()}\n`;
      output += `*聚合策略*: ${aggregated.strategy}\n`;
      output += `*结果数量*: ${aggregated.resultCount}\n`;
      if (aggregated.avgQuality) {
        output += `*平均质量*: ${Math.round(aggregated.avgQuality * 100)}%\n`;
      }
    }

    return output;
  }
}

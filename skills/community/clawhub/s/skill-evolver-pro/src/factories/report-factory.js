/**
 * 报告工厂 - 工厂模式核心
 * 统一生成各类分析报告
 * 
 * @module ReportFactory
 * @version 1.0.0
 */

/**
 * 报告基类
 * 所有具体报告类型必须继承此类
 */
class Report {
  constructor(type, title) {
    if (new.target === Report) {
      throw new Error('Report is an abstract class');
    }
    this.type = type;
    this.title = title;
    this.generatedAt = new Date().toISOString();
    this.metadata = {};
    this.sections = [];
  }

  /**
   * 添加报告章节
   * @param {string} title - 章节标题
   * @param {string|Object} content - 章节内容
   * @param {Object} options - 选项
   */
  addSection(title, content, options = {}) {
    this.sections.push({
      title,
      content: typeof content === 'string' ? content : this.formatContent(content),
      order: this.sections.length,
      ...options
    });
    return this;
  }

  /**
   * 添加元数据
   * @param {string} key - 键
   * @param {any} value - 值
   */
  addMetadata(key, value) {
    this.metadata[key] = value;
    return this;
  }

  /**
   * 格式化内容（子类可覆盖）
   * @param {Object} content - 内容对象
   * @returns {string} 格式化后的字符串
   */
  formatContent(content) {
    return JSON.stringify(content, null, 2);
  }

  /**
   * 渲染报告为 Markdown
   * @returns {string} Markdown 格式的报告
   */
  render() {
    let output = `# ${this.title}\n\n`;
    output += `**生成时间**: ${this.generatedAt}\n\n`;
    
    if (Object.keys(this.metadata).length > 0) {
      output += `## 元数据\n\n`;
      Object.entries(this.metadata).forEach(([key, value]) => {
        output += `- **${key}**: ${value}\n`;
      });
      output += `\n`;
    }

    this.sections.forEach(s => {
      output += `## ${s.title}\n\n${s.content}\n\n`;
    });

    return output;
  }

  /**
   * 渲染为 JSON
   * @returns {Object} JSON 对象
   */
  toJSON() {
    return {
      type: this.type,
      title: this.title,
      generatedAt: this.generatedAt,
      metadata: this.metadata,
      sections: this.sections
    };
  }

  /**
   * 导出为文件（需要文件系统支持）
   * @param {string} filePath - 文件路径
   * @param {string} format - 格式 (md|json)
   */
  async export(filePath, format = 'md') {
    // 子类可实现具体导出逻辑
    throw new Error('Method "export" must be implemented by subclass or with fs support');
  }
}

/**
 * 使用分析报告
 * 分析技能的使用频率、成功率、用户满意度
 */
class UsageReport extends Report {
  constructor(data) {
    super('usage', '技能使用分析报告');
    this.addMetadata('技能名称', data.skillName || '未知');
    this.addMetadata('分析周期', data.period || '最近 30 天');
    
    this.addSection('使用频率', this.formatFrequency(data.frequency || {}));
    this.addSection('成功率分析', this.formatSuccessRate(data.successRate || {}));
    this.addSection('用户满意度', this.formatSatisfaction(data.satisfaction || {}));
    this.addSection('使用趋势', this.formatTrends(data.trends || []));
    this.addSection('关键洞察', this.formatInsights(data.insights || []));
  }

  formatFrequency(freq) {
    const lines = [
      `| 周期 | 调用次数 | 日均 |`,
      `|------|----------|------|`,
      `| 每日 | ${freq.daily || 0} 次 | ${freq.daily || 0} 次/天 |`,
      `| 每周 | ${freq.weekly || 0} 次 | ${((freq.weekly || 0) / 7).toFixed(1)} 次/天 |`,
      `| 每月 | ${freq.monthly || 0} 次 | ${((freq.monthly || 0) / 30).toFixed(1)} 次/天 |`
    ];
    return lines.join('\n');
  }

  formatSuccessRate(rate) {
    const successPercent = ((rate.success || 0) * 100).toFixed(1);
    const failurePercent = ((rate.failure || 0) * 100).toFixed(1);
    
    let output = `**总体成功率**: ${successPercent}%\n\n`;
    output += `| 状态 | 次数 | 比例 |\n|------|------|------|\n`;
    output += `| ✅ 成功 | ${rate.successCount || 0} | ${successPercent}% |\n`;
    output += `| ❌ 失败 | ${rate.failureCount || 0} | ${failurePercent}% |\n`;
    
    if (rate.failureTypes && rate.failureTypes.length > 0) {
      output += `\n**失败类型分布**:\n`;
      rate.failureTypes.forEach((type, i) => {
        output += `${i + 1}. ${type.type}: ${type.count} 次 (${type.percentage}%)\n`;
      });
    }
    
    return output;
  }

  formatSatisfaction(sat) {
    let output = `**平均评分**: ${sat.average?.toFixed(1) || 0}/5.0\n\n`;
    output += `**反馈总数**: ${sat.feedbackCount || 0}\n\n`;
    
    if (sat.distribution) {
      output += `**评分分布**:\n`;
      output += `| 星级 | 数量 | 比例 |\n|------|------|------|\n`;
      for (let i = 5; i >= 1; i--) {
        const count = sat.distribution[i] || 0;
        const percent = sat.total ? ((count / sat.total) * 100).toFixed(1) : 0;
        const stars = '★'.repeat(i) + '☆'.repeat(5 - i);
        output += `| ${stars} | ${count} | ${percent}% |\n`;
      }
    }
    
    return output;
  }

  formatTrends(trends) {
    if (!trends || trends.length === 0) {
      return '暂无趋势数据';
    }
    
    let output = `| 日期 | 调用次数 | 成功率 | 平均评分 |\n`;
    output += `|------|----------|--------|----------|\n`;
    
    trends.forEach(trend => {
      output += `| ${trend.date} | ${trend.calls} | ${(trend.successRate * 100).toFixed(1)}% | ${trend.rating?.toFixed(1) || 'N/A'} |\n`;
    });
    
    return output;
  }

  formatInsights(insights) {
    if (!insights || insights.length === 0) {
      return '暂无关键洞察';
    }
    
    return insights.map((insight, i) => {
      const icon = insight.type === 'positive' ? '📈' : insight.type === 'warning' ? '⚠️' : '💡';
      return `${i + 1}. ${icon} ${insight.description}`;
    }).join('\n');
  }
}

/**
 * 性能分析报告
 * 分析技能的执行时间、资源消耗、瓶颈
 */
class PerformanceReport extends Report {
  constructor(data) {
    super('performance', '技能性能分析报告');
    this.addMetadata('技能名称', data.skillName || '未知');
    this.addMetadata('样本数量', data.sampleCount || 0);
    
    this.addSection('执行时间分析', this.formatExecutionTime(data.executionTime || {}));
    this.addSection('资源消耗', this.formatResourceUsage(data.resourceUsage || {}));
    this.addSection('瓶颈分析', this.formatBottlenecks(data.bottlenecks || []));
    this.addSection('性能评分', this.formatScore(data.score || {}));
    this.addSection('优化建议', this.formatRecommendations(data.recommendations || []));
  }

  formatExecutionTime(time) {
    let output = `| 指标 | 数值 | 评级 |\n|------|------|------|\n`;
    output += `| 平均执行时间 | ${time.average?.toFixed(0) || 0}ms | ${this.rateTime(time.average)} |\n`;
    output += `| P50 | ${time.p50?.toFixed(0) || 0}ms | - |\n`;
    output += `| P95 | ${time.p95?.toFixed(0) || 0}ms | ${this.rateTime(time.p95)} |\n`;
    output += `| P99 | ${time.p99?.toFixed(0) || 0}ms | ${this.rateTime(time.p99)} |\n`;
    output += `| 最慢 | ${time.max?.toFixed(0) || 0}ms | - |\n`;
    output += `| 最快 | ${time.min?.toFixed(0) || 0}ms | - |\n`;
    return output;
  }

  rateTime(ms) {
    if (!ms) return '-';
    if (ms < 100) return '🟢 优秀';
    if (ms < 500) return '🟡 良好';
    if (ms < 1000) return '🟠 一般';
    return '🔴 需优化';
  }

  formatResourceUsage(usage) {
    let output = `| 资源类型 | 使用量 | 限制 | 使用率 |\n`;
    output += `|----------|--------|------|--------|\n`;
    output += `| 内存 | ${usage.memory || 0}MB | ${usage.memoryLimit || 'N/A'}MB | ${usage.memoryPercent || 0}% |\n`;
    output += `| CPU | ${usage.cpu || 0}% | 100% | ${usage.cpu || 0}% |\n`;
    output += `| 网络请求 | ${usage.networkRequests || 0} | - | - |\n`;
    output += `| 磁盘 IO | ${usage.diskIO || 'N/A'} | - | - |\n`;
    return output;
  }

  formatBottlenecks(bottlenecks) {
    if (!bottlenecks || bottlenecks.length === 0) {
      return '未发现明显性能瓶颈 ✅';
    }
    
    return bottlenecks.map((b, i) => {
      const severity = b.severity === 'high' ? '🔴' : b.severity === 'medium' ? '🟠' : '🟡';
      return `${i + 1}. ${severity} **${b.description}**\n   - 影响：${b.impact}\n   - 建议：${b.suggestion}`;
    }).join('\n\n');
  }

  formatScore(score) {
    const overall = score.overall || 0;
    const rating = overall >= 90 ? '🟢 优秀' : overall >= 70 ? '🟡 良好' : overall >= 50 ? '🟠 一般' : '🔴 需优化';
    
    let output = `**综合性能评分**: ${overall.toFixed(1)}/100 ${rating}\n\n`;
    output += `| 维度 | 得分 | 权重 |\n|------|------|------|\n`;
    output += `| 执行速度 | ${score.speed || 0}/100 | ${(score.speedWeight || 0.4) * 100}% |\n`;
    output += `| 资源效率 | ${score.efficiency || 0}/100 | ${(score.efficiencyWeight || 0.3) * 100}% |\n`;
    output += `| 稳定性 | ${score.stability || 0}/100 | ${(score.stabilityWeight || 0.3) * 100}% |\n`;
    return output;
  }

  formatRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
      return '暂无优化建议';
    }
    
    return recommendations.map((r, i) => {
      const priority = r.priority === 'high' ? '🔴' : r.priority === 'medium' ? '🟠' : '🟢';
      return `${i + 1}. ${priority} **${r.title}**\n   - 预期收益：${r.expectedBenefit}\n   - 实施难度：${r.difficulty}\n   - 预计时间：${r.estimatedTime}`;
    }).join('\n\n');
  }
}

/**
 * 版本对比报告
 * 对比技能不同版本之间的差异
 */
class ComparisonReport extends Report {
  constructor(data) {
    super('comparison', '技能版本对比报告');
    this.addMetadata('技能名称', data.skillName || '未知');
    this.addMetadata('对比版本', `${data.versionA} vs ${data.versionB}`);
    
    this.addSection('版本信息', this.formatVersions(data.versions || {}));
    this.addSection('功能差异', this.formatDifferences(data.differences || []));
    this.addSection('性能对比', this.formatPerformanceComparison(data.performance || {}));
    this.addSection('六维评分对比', this.formatDimensionComparison(data.dimensions || {}));
    this.addSection('升级建议', this.formatUpgradeRecommendations(data.recommendations || []));
  }

  formatVersions(versions) {
    let output = `| 属性 | ${versions.a?.version || 'A'} | ${versions.b?.version || 'B'} |\n`;
    output += `|------|${'-'.repeat(versions.a?.version?.length || 5)}|${'-'.repeat(versions.b?.version?.length || 5)}|\n`;
    output += `| 发布日期 | ${versions.a?.releaseDate || 'N/A'} | ${versions.b?.releaseDate || 'N/A'} |\n`;
    output += `| 核心改进 | ${versions.a?.highlights?.join(', ') || '无'} | ${versions.b?.highlights?.join(', ') || '无'} |\n`;
    output += `| 状态 | ${versions.a?.status || 'N/A'} | ${versions.b?.status || 'N/A'} |\n`;
    return output;
  }

  formatDifferences(diffs) {
    if (!diffs || diffs.length === 0) {
      return '无功能差异';
    }
    
    let output = `| 类型 | 描述 | 影响 |\n|------|------|------|\n`;
    diffs.forEach(d => {
      const icon = d.type === 'added' ? '🆕' : d.type === 'removed' ? '❌' : d.type === 'changed' ? '🔄' : '📝';
      output += `| ${icon} ${d.type} | ${d.description} | ${d.impact} |\n`;
    });
    return output;
  }

  formatPerformanceComparison(perf) {
    let output = `| 指标 | ${perf.versionA || 'A'} | ${perf.versionB || 'B'} | 变化 |\n`;
    output += `|------|${'-'.repeat(15)}|${'-'.repeat(15)}|------|\n`;
    
    const metrics = perf.metrics || [];
    metrics.forEach(m => {
      const change = m.change > 0 ? `+${m.change}%` : `${m.change}%`;
      const arrow = m.change > 0 ? '📈' : m.change < 0 ? '📉' : '➡️';
      output += `| ${m.name} | ${m.valueA} | ${m.valueB} | ${arrow} ${change} |\n`;
    });
    
    return output;
  }

  formatDimensionComparison(dimensions) {
    let output = `| 维度 | ${dimensions.versionA || 'A'} | ${dimensions.versionB || 'B'} | 变化 |\n`;
    output += `|------|${'-'.repeat(10)}|${'-'.repeat(10)}|------|\n`;
    
    const dims = ['T', 'C', 'O', 'E', 'M', 'U'];
    const dimNames = {
      T: '技术深度',
      C: '认知增强',
      O: '编排能力',
      E: '进化能力',
      M: '商业化',
      U: '用户体验'
    };
    
    dims.forEach(d => {
      const a = dimensions.scoresA?.[d] || 0;
      const b = dimensions.scoresB?.[d] || 0;
      const change = ((b - a) * 100).toFixed(0);
      const arrow = change > 0 ? '📈' : change < 0 ? '📉' : '➡️';
      output += `| ${d} (${dimNames[d]}) | ${a.toFixed(2)} | ${b.toFixed(2)} | ${arrow} ${change > 0 ? '+' : ''}${change}% |\n`;
    });
    
    const avgA = dimensions.avgA || 0;
    const avgB = dimensions.avgB || 0;
    const avgChange = (((avgB - avgA) / avgA) * 100).toFixed(1);
    output += `| **平均** | **${avgA.toFixed(2)}** | **${avgB.toFixed(2)}** | ${avgChange > 0 ? '📈' : '📉'} ${avgChange > 0 ? '+' : ''}${avgChange}% |\n`;
    
    return output;
  }

  formatUpgradeRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
      return '暂无升级建议';
    }
    
    return recommendations.map((r, i) => {
      const priority = r.priority === 'critical' ? '🔴' : r.priority === 'important' ? '🟠' : '🟢';
      return `${i + 1}. ${priority} **${r.title}**\n   - 原因：${r.reason}\n   - 收益：${r.benefit}`;
    }).join('\n\n');
  }
}

/**
 * 进化计划报告
 * 制定技能的进化路径和时间规划
 */
class EvolutionPlanReport extends Report {
  constructor(data) {
    super('evolution-plan', '技能进化计划报告');
    this.addMetadata('技能名称', data.skillName || '未知');
    this.addMetadata('当前版本', data.currentVersion || 'v0.1.0');
    this.addMetadata('目标版本', data.targetVersion || 'v1.0.0');
    this.addMetadata('制定日期', new Date().toLocaleDateString('zh-CN'));
    
    this.addSection('当前状态评估', this.formatCurrentState(data.currentState || {}));
    this.addSection('目标状态定义', this.formatTargetState(data.targetState || {}));
    this.addSection('六维差距分析', this.formatGapAnalysis(data.gapAnalysis || {}));
    this.addSection('进化路径', this.formatEvolutionPath(data.path || []));
    this.addSection('时间规划', this.formatTimeline(data.timeline || {}));
    this.addSection('风险与应对', this.formatRisks(data.risks || []));
  }

  formatCurrentState(state) {
    let output = `**版本**: ${state.version || 'v0.1.0'}\n\n`;
    output += `**六维评分**:\n`;
    output += `| 维度 | 得分 | 评级 |\n|------|------|------|\n`;
    
    const dims = { T: '技术深度', C: '认知增强', O: '编排能力', E: '进化能力', M: '商业化', U: '用户体验' };
    Object.entries(dims).forEach(([key, name]) => {
      const score = state.scores?.[key] || 0;
      const rating = score >= 0.8 ? '🟢' : score >= 0.6 ? '🟡' : score >= 0.4 ? '🟠' : '🔴';
      output += `| ${key} (${name}) | ${score.toFixed(2)} | ${rating} |\n`;
    });
    
    output += `| **平均** | **${state.scores?.average?.toFixed(2) || 0}** | - |\n`;
    return output;
  }

  formatTargetState(state) {
    let output = `**目标版本**: ${state.version || 'v1.0.0'}\n\n`;
    output += `**目标六维评分**: 平均 ≥ ${state.targetScore || 0.8}\n\n`;
    output += `**核心目标**:\n`;
    output += (state.goals || ['无明确目标']).map((g, i) => `${i + 1}. ${g}`).join('\n');
    return output;
  }

  formatGapAnalysis(gap) {
    let output = `| 维度 | 当前 | 目标 | 差距 | 优先级 |\n`;
    output += `|------|------|------|------|--------|\n`;
    
    const dims = ['T', 'C', 'O', 'E', 'M', 'U'];
    dims.forEach(d => {
      const current = gap.current?.[d] || 0;
      const target = gap.target?.[d] || 0;
      const diff = (target - current).toFixed(2);
      const priority = Math.abs(target - current) >= 0.3 ? '🔴 高' : Math.abs(target - current) >= 0.15 ? '🟠 中' : '🟢 低';
      output += `| ${d} | ${current.toFixed(2)} | ${target.toFixed(2)} | ${diff > 0 ? '+' : ''}${diff} | ${priority} |\n`;
    });
    
    return output;
  }

  formatEvolutionPath(path) {
    if (!path || path.length === 0) {
      return '暂无进化路径规划';
    }
    
    return path.map((step, i) => {
      const phase = step.phase === 1 ? '🚀 Phase 1' : step.phase === 2 ? '📈 Phase 2' : '🎯 Phase 3';
      return `### ${phase}: ${step.name}\n\n${step.actions.map((a, j) => `- [ ] ${a}`).join('\n')}\n\n**预期成果**: ${step.expectedOutcome}\n`;
    }).join('\n---\n\n');
  }

  formatTimeline(timeline) {
    let output = `| 阶段 | 开始日期 | 结束日期 | 里程碑 |\n`;
    output += `|------|----------|----------|----------|\n`;
    
    (timeline.phases || []).forEach(p => {
      output += `| ${p.name} | ${p.startDate} | ${p.endDate} | ${p.milestone} |\n`;
    });
    
    return output;
  }

  formatRisks(risks) {
    if (!risks || risks.length === 0) {
      return '暂无已识别风险';
    }
    
    return risks.map((r, i) => {
      const severity = r.severity === 'high' ? '🔴' : r.severity === 'medium' ? '🟠' : '🟢';
      return `${i + 1}. ${severity} **${r.title}**\n   - 概率：${r.probability}\n   - 影响：${r.impact}\n   - 应对措施：${r.mitigation}`;
    }).join('\n\n');
  }
}

/**
 * 报告工厂类
 * 统一创建各类报告
 */
class ReportFactory {
  /**
   * 创建报告
   * @param {string} type - 报告类型
   * @param {Object} data - 报告数据
   * @returns {Report} 报告实例
   */
  static create(type, data) {
    switch (type) {
      case 'usage':
        return new UsageReport(data);
      case 'performance':
        return new PerformanceReport(data);
      case 'comparison':
        return new ComparisonReport(data);
      case 'evolution-plan':
        return new EvolutionPlanReport(data);
      default:
        throw new Error(`Unknown report type: ${type}. Available types: usage, performance, comparison, evolution-plan`);
    }
  }

  /**
   * 获取可用的报告类型
   * @returns {Array} 报告类型列表
   */
  static getAvailableTypes() {
    return [
      { type: 'usage', name: '使用分析报告', description: '分析技能使用频率、成功率、满意度' },
      { type: 'performance', name: '性能分析报告', description: '分析执行时间、资源消耗、瓶颈' },
      { type: 'comparison', name: '版本对比报告', description: '对比不同版本的功能和性能差异' },
      { type: 'evolution-plan', name: '进化计划报告', description: '制定技能进化路径和时间规划' }
    ];
  }
}

module.exports = {
  Report,
  UsageReport,
  PerformanceReport,
  ComparisonReport,
  EvolutionPlanReport,
  ReportFactory
};

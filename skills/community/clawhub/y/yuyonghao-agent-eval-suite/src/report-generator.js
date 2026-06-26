/**
 * ReportGenerator - 报告生成器
 * 提供测试报告、对比报告、趋势报告和建议生成
 */

class ReportGenerator {
  constructor(options = {}) {
    this.options = {
      format: options.format || 'json',
      includeCharts: options.includeCharts !== false,
      includeDetails: options.includeDetails !== false,
      ...options
    };
  }

  /**
   * 生成测试报告
   * @param {object} results - 测试结果
   * @param {object} options - 报告选项
   */
  generateTestReport(results, options = {}) {
    const report = {
      title: options.title || 'Agent Evaluation Test Report',
      generatedAt: new Date().toISOString(),
      summary: this.generateSummary(results),
      details: this.options.includeDetails ? results : undefined,
      recommendations: this.generateRecommendations(results)
    };

    if (this.options.format === 'markdown') {
      return this.toMarkdown(report);
    } else if (this.options.format === 'html') {
      return this.toHTML(report);
    }

    return report;
  }

  /**
   * 生成对比报告
   * @param {object} baseline - 基线结果
   * @param {object} current - 当前结果
   * @param {object} options - 报告选项
   */
  generateComparisonReport(baseline, current, options = {}) {
    const comparison = this.compareResults(baseline, current);
    
    const report = {
      title: options.title || 'Performance Comparison Report',
      generatedAt: new Date().toISOString(),
      baseline: {
        version: options.baselineVersion || 'baseline',
        timestamp: options.baselineTimestamp
      },
      current: {
        version: options.currentVersion || 'current',
        timestamp: options.currentTimestamp
      },
      comparison,
      summary: this.generateComparisonSummary(comparison),
      recommendations: this.generateComparisonRecommendations(comparison)
    };

    if (this.options.format === 'markdown') {
      return this.toMarkdown(report, 'comparison');
    } else if (this.options.format === 'html') {
      return this.toHTML(report, 'comparison');
    }

    return report;
  }

  /**
   * 生成趋势报告
   * @param {object} trends - 趋势数据
   * @param {object} options - 报告选项
   */
  generateTrendReport(trends, options = {}) {
    const report = {
      title: options.title || 'Performance Trend Report',
      generatedAt: new Date().toISOString(),
      period: options.period || 'last-10',
      trends: this.analyzeTrends(trends),
      summary: this.generateTrendSummary(trends),
      predictions: this.generatePredictions(trends),
      recommendations: this.generateTrendRecommendations(trends)
    };

    if (this.options.format === 'markdown') {
      return this.toMarkdown(report, 'trend');
    } else if (this.options.format === 'html') {
      return this.toHTML(report, 'trend');
    }

    return report;
  }

  /**
   * 生成摘要
   */
  generateSummary(results) {
    const summary = {
      totalTests: 0,
      passed: 0,
      failed: 0,
      warnings: 0,
      duration: 0,
      metrics: {}
    };

    for (const [key, value] of Object.entries(results)) {
      if (value && typeof value === 'object') {
        if (value.summary) {
          summary.totalTests += value.summary.total || 0;
          summary.passed += value.summary.passed || 0;
          summary.failed += value.summary.failed || 0;
          summary.warnings += value.summary.warnings || 0;
        }
        
        // 收集关键指标
        if (value.metrics) {
          summary.metrics[key] = this.extractKeyMetrics(value.metrics);
        }
      }
    }

    summary.status = summary.failed > 0 ? 'failed' : summary.warnings > 0 ? 'warning' : 'passed';
    summary.passRate = summary.totalTests > 0 
      ? Math.round((summary.passed / summary.totalTests) * 10000) / 100 
      : 0;

    return summary;
  }

  /**
   * 提取关键指标
   */
  extractKeyMetrics(metrics) {
    const keyMetrics = {};
    
    if (metrics.mean !== undefined) keyMetrics.mean = metrics.mean;
    if (metrics.p95 !== undefined) keyMetrics.p95 = metrics.p95;
    if (metrics.successRate !== undefined) keyMetrics.successRate = metrics.successRate;
    if (metrics.errorRate !== undefined) keyMetrics.errorRate = metrics.errorRate;
    
    return keyMetrics;
  }

  /**
   * 生成建议
   */
  generateRecommendations(results) {
    const recommendations = [];

    for (const [key, value] of Object.entries(results)) {
      if (value && typeof value === 'object') {
        // 基准测试建议
        if (key === 'benchmark' && value.metrics) {
          for (const [testName, metrics] of Object.entries(value.metrics)) {
            if (metrics.successRate < 0.95) {
              recommendations.push({
                type: 'warning',
                test: testName,
                message: `Success rate ${(metrics.successRate * 100).toFixed(1)}% is below 95% threshold`,
                action: 'Investigate failure causes and improve error handling'
              });
            }
            if (metrics.p95 > 1000) {
              recommendations.push({
                type: 'performance',
                test: testName,
                message: `P95 latency ${metrics.p95.toFixed(0)}ms is high`,
                action: 'Consider optimization or caching strategies'
              });
            }
          }
        }

        // A/B 测试建议
        if (key === 'abTest' && value.winner) {
          if (value.winner === 'treatment' && value.isSignificant) {
            recommendations.push({
              type: 'ab-test',
              experiment: value.experimentName,
              message: `Treatment shows ${(value.improvement * 100).toFixed(2)}% improvement`,
              action: 'Consider deploying treatment to production'
            });
          }
        }

        // 回归检测建议
        if (key === 'regression' && Array.isArray(value)) {
          for (const regression of value) {
            recommendations.push({
              type: 'regression',
              severity: regression.severity,
              metric: regression.metric,
              message: `${regression.metric} degraded by ${(regression.change * 100).toFixed(2)}%`,
              action: regression.recommendation
            });
          }
        }
      }
    }

    return recommendations;
  }

  /**
   * 对比结果
   */
  compareResults(baseline, current) {
    const comparison = {};

    for (const [key, currentValue] of Object.entries(current)) {
      const baselineValue = baseline[key];
      
      if (baselineValue !== undefined && typeof currentValue === 'object') {
        comparison[key] = this.compareMetrics(baselineValue, currentValue);
      }
    }

    return comparison;
  }

  /**
   * 对比指标
   */
  compareMetrics(baseline, current) {
    const result = {};

    for (const [metric, currentValue] of Object.entries(current)) {
      const baselineValue = baseline[metric];
      
      if (baselineValue !== undefined && typeof currentValue === 'number' && typeof baselineValue === 'number') {
        const change = baselineValue !== 0 
          ? ((currentValue - baselineValue) / baselineValue) 
          : 0;
        
        result[metric] = {
          baseline: baselineValue,
          current: currentValue,
          change: Math.round(change * 10000) / 10000,
          changePercent: Math.round(change * 10000) / 100,
          status: Math.abs(change) > 0.1 ? 'significant' : 'stable'
        };
      }
    }

    return result;
  }

  /**
   * 生成对比摘要
   */
  generateComparisonSummary(comparison) {
    let improved = 0;
    let degraded = 0;
    let stable = 0;

    for (const metrics of Object.values(comparison)) {
      for (const metric of Object.values(metrics)) {
        if (metric.change > 0.1) {
          degraded++;
        } else if (metric.change < -0.1) {
          improved++;
        } else {
          stable++;
        }
      }
    }

    return {
      total: improved + degraded + stable,
      improved,
      degraded,
      stable,
      status: degraded > improved ? 'regression' : improved > degraded ? 'improvement' : 'stable'
    };
  }

  /**
   * 生成对比建议
   */
  generateComparisonRecommendations(comparison) {
    const recommendations = [];

    for (const [category, metrics] of Object.entries(comparison)) {
      for (const [metric, data] of Object.entries(metrics)) {
        if (data.change > 0.2) {
          recommendations.push({
            type: 'critical',
            category,
            metric,
            message: `${metric} degraded by ${data.changePercent.toFixed(2)}%`,
            action: 'Immediate investigation required'
          });
        } else if (data.change > 0.1) {
          recommendations.push({
            type: 'warning',
            category,
            metric,
            message: `${metric} degraded by ${data.changePercent.toFixed(2)}%`,
            action: 'Schedule investigation'
          });
        } else if (data.change < -0.1) {
          recommendations.push({
            type: 'improvement',
            category,
            metric,
            message: `${metric} improved by ${Math.abs(data.changePercent).toFixed(2)}%`,
            action: 'Document the improvement'
          });
        }
      }
    }

    return recommendations;
  }

  /**
   * 分析趋势
   */
  analyzeTrends(trends) {
    const analysis = {};

    for (const [metric, data] of Object.entries(trends)) {
      if (data && data.data && data.data.length >= 2) {
        const values = data.data.map(d => d.value);
        const trend = this.calculateTrendDirection(values);
        
        analysis[metric] = {
          direction: trend.direction,
          slope: trend.slope,
          volatility: this.calculateVolatility(values),
          recentAvg: values.slice(-5).reduce((a, b) => a + b, 0) / Math.min(5, values.length)
        };
      }
    }

    return analysis;
  }

  /**
   * 计算趋势方向
   */
  calculateTrendDirection(values) {
    if (values.length < 2) {
      return { direction: 'insufficient', slope: 0 };
    }

    const n = values.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    
    for (let i = 0; i < n; i++) {
      sumX += i;
      sumY += values[i];
      sumXY += i * values[i];
      sumX2 += i * i;
    }

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const avgValue = sumY / n;
    const slopePercent = avgValue !== 0 ? slope / avgValue : 0;

    let direction;
    if (Math.abs(slopePercent) < 0.01) {
      direction = 'stable';
    } else if (slopePercent > 0) {
      direction = 'increasing';
    } else {
      direction = 'decreasing';
    }

    return { direction, slope: Math.round(slope * 1000) / 1000 };
  }

  /**
   * 计算波动率
   */
  calculateVolatility(values) {
    if (values.length < 2) return 0;
    
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);
    
    return mean !== 0 ? Math.round((stdDev / mean) * 10000) / 10000 : 0;
  }

  /**
   * 生成趋势摘要
   */
  generateTrendSummary(trends) {
    const summary = {
      totalMetrics: Object.keys(trends).length,
      improving: 0,
      degrading: 0,
      stable: 0
    };

    const analysis = this.analyzeTrends(trends);
    for (const metric of Object.values(analysis)) {
      if (metric.direction === 'increasing') {
        summary.degrading++;
      } else if (metric.direction === 'decreasing') {
        summary.improving++;
      } else {
        summary.stable++;
      }
    }

    return summary;
  }

  /**
   * 生成预测
   */
  generatePredictions(trends) {
    const predictions = {};

    for (const [metric, data] of Object.entries(trends)) {
      if (data && data.data && data.data.length >= 3) {
        const values = data.data.map(d => d.value);
        const trend = this.calculateTrendDirection(values);
        
        // 简单线性预测
        const lastValue = values[values.length - 1];
        const predictedValue = lastValue + trend.slope * 5; // 预测5个周期后的值
        
        predictions[metric] = {
          current: lastValue,
          predicted: Math.round(predictedValue * 100) / 100,
          confidence: this.calculatePredictionConfidence(values, trend.slope)
        };
      }
    }

    return predictions;
  }

  /**
   * 计算预测置信度
   */
  calculatePredictionConfidence(values, slope) {
    if (values.length < 3) return 0.5;
    
    const volatility = this.calculateVolatility(values);
    // 波动率越低，置信度越高
    const confidence = Math.max(0.3, Math.min(0.95, 1 - volatility));
    
    return Math.round(confidence * 100) / 100;
  }

  /**
   * 生成趋势建议
   */
  generateTrendRecommendations(trends) {
    const recommendations = [];
    const analysis = this.analyzeTrends(trends);

    for (const [metric, data] of Object.entries(analysis)) {
      if (data.direction === 'increasing' && data.volatility > 0.2) {
        recommendations.push({
          type: 'warning',
          metric,
          message: `${metric} is trending upward with high volatility`,
          action: 'Investigate causes of instability'
        });
      } else if (data.direction === 'stable' && data.volatility < 0.05) {
        recommendations.push({
          type: 'info',
          metric,
          message: `${metric} is stable and predictable`,
          action: 'No action needed'
        });
      }
    }

    return recommendations;
  }

  /**
   * 转换为 Markdown
   */
  toMarkdown(report, type = 'test') {
    let md = `# ${report.title}\n\n`;
    md += `**Generated:** ${report.generatedAt}\n\n`;

    if (type === 'test') {
      md += this.markdownTestReport(report);
    } else if (type === 'comparison') {
      md += this.markdownComparisonReport(report);
    } else if (type === 'trend') {
      md += this.markdownTrendReport(report);
    }

    return md;
  }

  /**
   * Markdown 测试报告
   */
  markdownTestReport(report) {
    let md = '## Summary\n\n';
    const s = report.summary;
    md += `- **Status:** ${s.status.toUpperCase()}\n`;
    md += `- **Total Tests:** ${s.totalTests}\n`;
    md += `- **Passed:** ${s.passed} (${s.passRate}%)\n`;
    md += `- **Failed:** ${s.failed}\n`;
    md += `- **Warnings:** ${s.warnings}\n\n`;

    if (report.recommendations && report.recommendations.length > 0) {
      md += '## Recommendations\n\n';
      for (const rec of report.recommendations) {
        md += `### ${rec.type.toUpperCase()}: ${rec.message}\n\n`;
        md += `**Action:** ${rec.action}\n\n`;
      }
    }

    return md;
  }

  /**
   * Markdown 对比报告
   */
  markdownComparisonReport(report) {
    let md = '## Summary\n\n';
    const s = report.summary;
    md += `- **Status:** ${s.status.toUpperCase()}\n`;
    md += `- **Total Metrics:** ${s.total}\n`;
    md += `- **Improved:** ${s.improved}\n`;
    md += `- **Degraded:** ${s.degraded}\n`;
    md += `- **Stable:** ${s.stable}\n\n`;

    md += '## Comparison Details\n\n';
    for (const [category, metrics] of Object.entries(report.comparison)) {
      md += `### ${category}\n\n`;
      md += '| Metric | Baseline | Current | Change | Status |\n';
      md += '|--------|----------|---------|--------|--------|\n';
      for (const [metric, data] of Object.entries(metrics)) {
        const changeStr = data.change > 0 ? `+${data.changePercent}%` : `${data.changePercent}%`;
        md += `| ${metric} | ${data.baseline} | ${data.current} | ${changeStr} | ${data.status} |\n`;
      }
      md += '\n';
    }

    return md;
  }

  /**
   * Markdown 趋势报告
   */
  markdownTrendReport(report) {
    let md = '## Summary\n\n';
    const s = report.summary;
    md += `- **Total Metrics:** ${s.totalMetrics}\n`;
    md += `- **Improving:** ${s.improving}\n`;
    md += `- **Degrading:** ${s.degrading}\n`;
    md += `- **Stable:** ${s.stable}\n\n`;

    md += '## Trend Analysis\n\n';
    for (const [metric, data] of Object.entries(report.trends)) {
      md += `### ${metric}\n\n`;
      md += `- **Direction:** ${data.direction}\n`;
      md += `- **Slope:** ${data.slope}\n`;
      md += `- **Volatility:** ${data.volatility}\n\n`;
    }

    return md;
  }

  /**
   * 转换为 HTML
   */
  toHTML(report, type = 'test') {
    // 简化版 HTML 生成
    const md = this.toMarkdown(report, type);
    return `<!DOCTYPE html>
<html>
<head>
  <title>${report.title}</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1 { color: #333; }
    h2 { color: #666; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
    table { border-collapse: collapse; width: 100%; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f5f5f5; }
    .passed { color: green; }
    .failed { color: red; }
    .warning { color: orange; }
  </style>
</head>
<body>
  ${md.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>').replace(/^# (.*)$/m, '<h1>$1</h1>').replace(/^## (.*)$/m, '<h2>$1</h2>').replace(/^### (.*)$/m, '<h3>$1</h3>')}
</body>
</html>`;
  }
}

module.exports = { ReportGenerator };

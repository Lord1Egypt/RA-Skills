/**
 * RegressionDetector - 性能回归检测
 * 提供历史性能对比、回归告警、性能趋势图和根因分析
 */

class RegressionDetector {
  constructor(options = {}) {
    this.options = {
      threshold: options.threshold || 0.1,  // 10% 性能下降阈值
      baseline: options.baseline || null,
      warningThreshold: options.warningThreshold || 0.05,  // 5% 警告阈值
      criticalThreshold: options.criticalThreshold || 0.2,  // 20% 严重阈值
      historySize: options.historySize || 100,
      ...options
    };
    this.history = new Map();  // metric -> array of records
    this.baselines = new Map(); // metric -> baseline value
  }

  /**
   * 设置基线
   * @param {string} version - 基线版本
   * @param {object} metrics - 基线指标
   */
  setBaseline(version, metrics) {
    for (const [metric, value] of Object.entries(metrics)) {
      this.baselines.set(metric, {
        version,
        value,
        timestamp: Date.now()
      });
    }
  }

  /**
   * 记录性能数据
   * @param {string} metric - 指标名称
   * @param {object} data - 性能数据
   */
  record(metric, data) {
    if (!this.history.has(metric)) {
      this.history.set(metric, []);
    }

    const records = this.history.get(metric);
    const record = {
      version: data.version || 'unknown',
      value: data.value,
      timestamp: data.timestamp || Date.now(),
      metadata: data.metadata || {}
    };

    records.push(record);

    // 限制历史记录大小
    if (records.length > this.options.historySize) {
      records.shift();
    }
  }

  /**
   * 批量记录性能数据
   */
  recordBatch(version, metrics) {
    for (const [metric, value] of Object.entries(metrics)) {
      this.record(metric, { version, value });
    }
  }

  /**
   * 检测回归
   * @param {string} metric - 指定指标，不指定则检测所有
   */
  detect(metric) {
    const metricsToCheck = metric ? [metric] : Array.from(this.history.keys());
    const regressions = [];

    for (const m of metricsToCheck) {
      const records = this.history.get(m);
      if (!records || records.length < 2) {
        continue;
      }

      const baseline = this.baselines.get(m);
      const current = records[records.length - 1];
      const previous = records[records.length - 2];

      const regression = this.analyzeRegression(m, baseline, current, previous, records);
      if (regression) {
        regressions.push(regression);
      }
    }

    return regressions;
  }

  /**
   * 分析回归
   */
  analyzeRegression(metric, baseline, current, previous, records) {
    const comparisonBase = baseline || previous;
    if (!comparisonBase || comparisonBase.value === 0) {
      return null;
    }

    const change = (current.value - comparisonBase.value) / comparisonBase.value;
    const absChange = Math.abs(change);

    if (absChange < this.options.warningThreshold) {
      return null;  // 变化太小，不认为是回归
    }

    const severity = this.determineSeverity(absChange);
    const trend = this.analyzeTrend(records);
    
    return {
      metric,
      severity,
      change: Math.round(change * 10000) / 10000,
      changePercent: Math.round(change * 10000) / 100,
      currentValue: current.value,
      baselineValue: comparisonBase.value,
      baselineVersion: comparisonBase.version,
      currentVersion: current.version,
      timestamp: current.timestamp,
      trend,
      possibleCauses: this.inferPossibleCauses(metric, change, trend),
      recommendation: this.generateRecommendation(severity, change, trend)
    };
  }

  /**
   * 确定严重程度
   */
  determineSeverity(absChange) {
    if (absChange >= this.options.criticalThreshold) {
      return 'critical';
    } else if (absChange >= this.options.threshold) {
      return 'high';
    } else if (absChange >= this.options.warningThreshold) {
      return 'warning';
    }
    return 'none';
  }

  /**
   * 分析趋势
   */
  analyzeTrend(records) {
    if (records.length < 3) {
      return { direction: 'insufficient_data', slope: 0 };
    }

    // 使用最近的数据点进行线性回归
    const recentRecords = records.slice(-10);
    const n = recentRecords.length;
    
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    for (let i = 0; i < n; i++) {
      sumX += i;
      sumY += recentRecords[i].value;
      sumXY += i * recentRecords[i].value;
      sumX2 += i * i;
    }

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const avgValue = recentRecords.reduce((a, b) => a + b.value, 0) / n;
    const slopePercent = avgValue !== 0 ? slope / avgValue : 0;

    let direction;
    if (Math.abs(slopePercent) < 0.01) {
      direction = 'stable';
    } else if (slopePercent > 0) {
      direction = 'increasing';
    } else {
      direction = 'decreasing';
    }

    return {
      direction,
      slope: Math.round(slope * 1000) / 1000,
      slopePercent: Math.round(slopePercent * 10000) / 100
    };
  }

  /**
   * 推断可能原因
   */
  inferPossibleCauses(metric, change, trend) {
    const causes = [];

    if (change > 0) {
      causes.push('Performance degradation detected');
      
      if (metric.includes('memory')) {
        causes.push('Possible memory leak');
        causes.push('Increased data processing');
      } else if (metric.includes('time') || metric.includes('duration') || metric.includes('latency')) {
        causes.push('Slower algorithm or implementation');
        causes.push('Increased computational complexity');
        causes.push('Resource contention');
      } else if (metric.includes('error') || metric.includes('failure')) {
        causes.push('Increased error rate - check error handling');
        causes.push('External dependency issues');
      }
    } else {
      causes.push('Performance improvement detected');
      
      if (metric.includes('time') || metric.includes('duration')) {
        causes.push('Optimization effective');
        causes.push('Reduced computational load');
      }
    }

    if (trend.direction === 'increasing' && change > 0) {
      causes.push('Consistent degradation trend - requires immediate attention');
    }

    return causes;
  }

  /**
   * 生成建议
   */
  generateRecommendation(severity, change, trend) {
    if (severity === 'critical') {
      return 'CRITICAL: Immediate rollback or hotfix required. Performance has degraded significantly.';
    } else if (severity === 'high') {
      return 'HIGH: Investigate and address before next release. Consider temporary mitigation.';
    } else if (severity === 'warning') {
      return 'WARNING: Monitor closely. Schedule investigation in next sprint.';
    }
    
    if (change < 0) {
      return 'Performance improved. Document changes for future reference.';
    }
    
    return 'No action required.';
  }

  /**
   * 获取趋势数据
   * @param {string} metric - 指标名称
   * @param {number} points - 数据点数量
   */
  getTrend(metric, points = 10) {
    const records = this.history.get(metric);
    if (!records || records.length === 0) {
      return null;
    }

    const recentRecords = records.slice(-points);
    
    return {
      metric,
      data: recentRecords.map(r => ({
        version: r.version,
        value: r.value,
        timestamp: r.timestamp
      })),
      statistics: this.calculateTrendStatistics(recentRecords)
    };
  }

  /**
   * 计算趋势统计
   */
  calculateTrendStatistics(records) {
    if (records.length === 0) {
      return null;
    }

    const values = records.map(r => r.value);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const min = Math.min(...values);
    const max = Math.max(...values);
    
    const sorted = [...values].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    
    const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);

    return {
      mean: Math.round(mean * 100) / 100,
      median: Math.round(median * 100) / 100,
      min: Math.round(min * 100) / 100,
      max: Math.round(max * 100) / 100,
      stdDev: Math.round(stdDev * 100) / 100,
      count: values.length
    };
  }

  /**
   * 获取所有指标的历史
   */
  getAllTrends(points = 10) {
    const trends = {};
    for (const metric of this.history.keys()) {
      trends[metric] = this.getTrend(metric, points);
    }
    return trends;
  }

  /**
   * 导出历史数据
   */
  exportHistory() {
    const data = {};
    for (const [metric, records] of this.history.entries()) {
      data[metric] = records;
    }
    return {
      baselines: Object.fromEntries(this.baselines),
      history: data,
      exportedAt: Date.now()
    };
  }

  /**
   * 导入历史数据
   */
  importHistory(data) {
    if (data.baselines) {
      for (const [metric, baseline] of Object.entries(data.baselines)) {
        this.baselines.set(metric, baseline);
      }
    }
    
    if (data.history) {
      for (const [metric, records] of Object.entries(data.history)) {
        this.history.set(metric, records);
      }
    }
  }

  /**
   * 清空历史
   */
  clearHistory(metric) {
    if (metric) {
      this.history.delete(metric);
      this.baselines.delete(metric);
    } else {
      this.history.clear();
      this.baselines.clear();
    }
  }

  /**
   * 获取指标列表
   */
  getMetrics() {
    return Array.from(this.history.keys());
  }
}

module.exports = { RegressionDetector };
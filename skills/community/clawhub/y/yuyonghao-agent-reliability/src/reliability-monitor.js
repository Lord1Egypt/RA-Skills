/**
 * ReliabilityMonitor - 可靠性监控模块
 * 实时追踪错误率、历史趋势分析和异常检测
 */

const EventEmitter = require('events');

class ReliabilityMonitor extends EventEmitter {
  /**
   * @param {Object} options - 配置选项
   * @param {number} options.errorThreshold - 错误率阈值 (默认 0.15)
   * @param {number} options.confidenceThreshold - 置信度阈值 (默认 0.85)
   * @param {number} options.historyWindow - 历史窗口大小 (默认 100)
   * @param {boolean} options.enableLogging - 是否启用日志 (默认 true)
   */
  constructor(options = {}) {
    super();
    
    this.errorThreshold = options.errorThreshold ?? 0.15;
    this.confidenceThreshold = options.confidenceThreshold ?? 0.85;
    this.historyWindow = options.historyWindow ?? 100;
    this.enableLogging = options.enableLogging ?? true;
    
    // 存储执行记录
    this.records = [];
    
    // 按步骤统计
    this.stepStats = new Map();
    
    // 错误分类统计
    this.errorCategories = new Map();
    
    // 告警状态
    this.alertState = {
      errorRateAlert: false,
      confidenceAlert: false,
      lastAlertTime: null
    };
    
    this._log('ReliabilityMonitor initialized', { 
      errorThreshold: this.errorThreshold,
      confidenceThreshold: this.confidenceThreshold,
      historyWindow: this.historyWindow
    });
  }
  
  /**
   * 记录执行结果
   * @param {Object} record - 执行记录
   * @param {string} record.stepId - 步骤ID
   * @param {boolean} record.success - 是否成功
   * @param {number} record.confidence - 置信度 (0-1)
   * @param {number} record.duration - 执行时长(ms)
   * @param {string} record.errorType - 错误类型 (失败时)
   * @param {string} record.errorMessage - 错误信息 (失败时)
   * @param {Object} record.metadata - 额外元数据
   */
  record(record) {
    const entry = {
      timestamp: Date.now(),
      stepId: record.stepId || 'unknown',
      success: record.success ?? true,
      confidence: record.confidence ?? 0.5,
      duration: record.duration ?? 0,
      errorType: record.errorType || null,
      errorMessage: record.errorMessage || null,
      metadata: record.metadata || {}
    };
    
    // 添加到历史记录
    this.records.push(entry);
    
    // 维护窗口大小
    if (this.records.length > this.historyWindow) {
      const removed = this.records.shift();
      this._updateStepStats(removed, true);
    }
    
    // 更新统计
    this._updateStepStats(entry, false);
    
    // 更新错误分类
    if (!entry.success && entry.errorType) {
      this._categorizeError(entry.errorType);
    }
    
    // 检查阈值告警
    this._checkThresholds(entry);
    
    // 触发事件
    this.emit('record', entry);
    
    this._log('Record added', { 
      stepId: entry.stepId, 
      success: entry.success, 
      confidence: entry.confidence 
    });
    
    return entry;
  }
  
  /**
   * 更新步骤统计
   * @private
   */
  _updateStepStats(entry, isRemoval) {
    const stats = this.stepStats.get(entry.stepId) || {
      total: 0,
      success: 0,
      failure: 0,
      totalConfidence: 0,
      totalDuration: 0
    };
    
    const multiplier = isRemoval ? -1 : 1;
    
    stats.total += multiplier;
    if (entry.success) {
      stats.success += multiplier;
    } else {
      stats.failure += multiplier;
    }
    stats.totalConfidence += entry.confidence * multiplier;
    stats.totalDuration += entry.duration * multiplier;
    
    // 计算派生指标
    stats.successRate = stats.total > 0 ? stats.success / stats.total : 0;
    stats.errorRate = stats.total > 0 ? stats.failure / stats.total : 0;
    stats.avgConfidence = stats.total > 0 ? stats.totalConfidence / stats.total : 0;
    stats.avgDuration = stats.total > 0 ? stats.totalDuration / stats.total : 0;
    
    this.stepStats.set(entry.stepId, stats);
  }
  
  /**
   * 错误分类统计
   * @private
   */
  _categorizeError(errorType) {
    const count = this.errorCategories.get(errorType) || 0;
    this.errorCategories.set(errorType, count + 1);
  }
  
  /**
   * 检查阈值告警
   * @private
   */
  _checkThresholds(entry) {
    const score = this.getReliabilityScore();
    
    // 错误率告警
    if (score.overall.errorRate > this.errorThreshold && !this.alertState.errorRateAlert) {
      this.alertState.errorRateAlert = true;
      this.alertState.lastAlertTime = Date.now();
      this.emit('alert', {
        type: 'error-rate',
        threshold: this.errorThreshold,
        current: score.overall.errorRate,
        message: `Error rate ${(score.overall.errorRate * 100).toFixed(1)}% exceeds threshold ${(this.errorThreshold * 100).toFixed(1)}%`
      });
    } else if (score.overall.errorRate <= this.errorThreshold) {
      this.alertState.errorRateAlert = false;
    }
    
    // 置信度告警
    if (score.overall.avgConfidence < this.confidenceThreshold && !this.alertState.confidenceAlert) {
      this.alertState.confidenceAlert = true;
      this.alertState.lastAlertTime = Date.now();
      this.emit('alert', {
        type: 'confidence',
        threshold: this.confidenceThreshold,
        current: score.overall.avgConfidence,
        message: `Confidence ${(score.overall.avgConfidence * 100).toFixed(1)}% below threshold ${(this.confidenceThreshold * 100).toFixed(1)}%`
      });
    } else if (score.overall.avgConfidence >= this.confidenceThreshold) {
      this.alertState.confidenceAlert = false;
    }
  }
  
  /**
   * 获取可靠性评分
   * @returns {Object} 可靠性评分
   */
  getReliabilityScore() {
    const total = this.records.length;
    
    if (total === 0) {
      return {
        overall: {
          successRate: 0,
          errorRate: 0,
          avgConfidence: 0,
          avgDuration: 0,
          total: 0
        },
        byStep: {},
        trend: 'neutral'
      };
    }
    
    const success = this.records.filter(r => r.success).length;
    const totalConfidence = this.records.reduce((sum, r) => sum + r.confidence, 0);
    const totalDuration = this.records.reduce((sum, r) => sum + r.duration, 0);
    
    // 计算趋势
    const trend = this._calculateTrend();
    
    // 构建步骤统计
    const byStep = {};
    for (const [stepId, stats] of this.stepStats.entries()) {
      byStep[stepId] = {
        successRate: stats.successRate,
        errorRate: stats.errorRate,
        avgConfidence: stats.avgConfidence,
        avgDuration: stats.avgDuration,
        total: stats.total
      };
    }
    
    return {
      overall: {
        successRate: success / total,
        errorRate: (total - success) / total,
        avgConfidence: totalConfidence / total,
        avgDuration: totalDuration / total,
        total
      },
      byStep,
      trend
    };
  }
  
  /**
   * 计算趋势
   * @private
   */
  _calculateTrend() {
    if (this.records.length < 20) {
      return 'insufficient-data';
    }
    
    // 分两半比较
    const half = Math.floor(this.records.length / 2);
    const firstHalf = this.records.slice(0, half);
    const secondHalf = this.records.slice(half);
    
    const firstSuccessRate = firstHalf.filter(r => r.success).length / firstHalf.length;
    const secondSuccessRate = secondHalf.filter(r => r.success).length / secondHalf.length;
    
    const diff = secondSuccessRate - firstSuccessRate;
    
    if (diff > 0.05) return 'improving';
    if (diff < -0.05) return 'degrading';
    return 'stable';
  }
  
  /**
   * 获取错误分类统计
   * @returns {Object} 错误分类
   */
  getErrorCategories() {
    const result = {};
    for (const [type, count] of this.errorCategories.entries()) {
      result[type] = count;
    }
    return result;
  }
  
  /**
   * 获取历史记录
   * @param {number} limit - 限制数量
   * @returns {Array} 历史记录
   */
  getHistory(limit = null) {
    if (limit) {
      return this.records.slice(-limit);
    }
    return [...this.records];
  }
  
  /**
   * 获取特定步骤的统计
   * @param {string} stepId - 步骤ID
   * @returns {Object|null} 步骤统计
   */
  getStepStats(stepId) {
    const stats = this.stepStats.get(stepId);
    if (!stats) return null;
    
    return {
      successRate: stats.successRate,
      errorRate: stats.errorRate,
      avgConfidence: stats.avgConfidence,
      avgDuration: stats.avgDuration,
      total: stats.total
    };
  }
  
  /**
   * 重置监控器
   */
  reset() {
    this.records = [];
    this.stepStats.clear();
    this.errorCategories.clear();
    this.alertState = {
      errorRateAlert: false,
      confidenceAlert: false,
      lastAlertTime: null
    };
    this.emit('reset');
    this._log('Monitor reset');
  }
  
  /**
   * 清理旧数据
   * @param {number} olderThan - 清理多久前的数据(ms)
   */
  cleanup(olderThan) {
    const cutoff = Date.now() - olderThan;
    const beforeLength = this.records.length;
    
    // 过滤记录
    this.records = this.records.filter(r => r.timestamp >= cutoff);
    
    // 重新计算统计
    this.stepStats.clear();
    this.errorCategories.clear();
    
    for (const entry of this.records) {
      this._updateStepStats(entry, false);
      if (!entry.success && entry.errorType) {
        this._categorizeError(entry.errorType);
      }
    }
    
    const removed = beforeLength - this.records.length;
    this._log('Cleanup completed', { removed, remaining: this.records.length });
    
    return { removed, remaining: this.records.length };
  }
  
  /**
   * 日志记录
   * @private
   */
  _log(message, data = null) {
    if (!this.enableLogging) return;
    
    const timestamp = new Date().toISOString();
    if (data) {
      console.log(`[${timestamp}] [ReliabilityMonitor] ${message}:`, data);
    } else {
      console.log(`[${timestamp}] [ReliabilityMonitor] ${message}`);
    }
  }
}

module.exports = ReliabilityMonitor;

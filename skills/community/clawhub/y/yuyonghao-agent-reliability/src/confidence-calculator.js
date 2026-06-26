/**
 * ConfidenceCalculator - 置信度计算模块
 * 单步置信度计算、累积置信度追踪、阈值告警和置信度可视化
 */

const EventEmitter = require('events');

class ConfidenceCalculator extends EventEmitter {
  /**
   * @param {Object} options - 配置选项
   * @param {number} options.defaultConfidence - 默认置信度 (默认 0.5)
   * @param {number} options.minConfidence - 最小置信度 (默认 0.0)
   * @param {number} options.maxConfidence - 最大置信度 (默认 1.0)
   * @param {number} options.threshold - 告警阈值 (默认 0.85)
   * @param {number} options.decayFactor - 历史衰减因子 (默认 0.95)
   * @param {boolean} options.enableLogging - 是否启用日志 (默认 true)
   */
  constructor(options = {}) {
    super();
    
    this.defaultConfidence = options.defaultConfidence ?? 0.5;
    this.minConfidence = options.minConfidence ?? 0.0;
    this.maxConfidence = options.maxConfidence ?? 1.0;
    this.threshold = options.threshold ?? 0.85;
    this.decayFactor = options.decayFactor ?? 0.95;
    this.enableLogging = options.enableLogging ?? true;
    
    // 置信度历史
    this.confidenceHistory = [];
    
    // 累积置信度
    this.cumulativeConfidence = 1.0;
    
    // 步骤置信度
    this.stepConfidence = new Map();
    
    // 告警状态
    this.alertState = {
      belowThreshold: false,
      lastAlertTime: null
    };
    
    // 统计
    this.stats = {
      totalCalculations: 0,
      belowThresholdCount: 0,
      avgConfidence: 0
    };
    
    this._log('ConfidenceCalculator initialized', {
      defaultConfidence: this.defaultConfidence,
      threshold: this.threshold,
      decayFactor: this.decayFactor
    });
  }
  
  /**
   * 计算单步置信度
   * @param {Object} factors - 置信度因子
   * @param {number} factors.baseConfidence - 基础置信度 (0-1)
   * @param {number} factors.dataQuality - 数据质量 (0-1)
   * @param {number} factors.modelAccuracy - 模型准确率 (0-1)
   * @param {number} factors.historicalSuccess - 历史成功率 (0-1)
   * @param {number} factors.uncertainty - 不确定性 (0-1, 越高越不确定)
   * @param {Object} factors.weights - 权重配置
   * @returns {number} 计算后的置信度 (0-1)
   */
  calculate(factors = {}) {
    this.stats.totalCalculations++;
    
    const weights = factors.weights || {
      base: 0.3,
      dataQuality: 0.2,
      modelAccuracy: 0.2,
      historicalSuccess: 0.2,
      uncertainty: -0.1 // 负权重
    };
    
    // 获取各因子值
    const baseConfidence = factors.baseConfidence ?? this.defaultConfidence;
    const dataQuality = factors.dataQuality ?? 0.5;
    const modelAccuracy = factors.modelAccuracy ?? 0.5;
    const historicalSuccess = factors.historicalSuccess ?? 0.5;
    const uncertainty = factors.uncertainty ?? 0.0;
    
    // 计算加权置信度
    let confidence = (
      baseConfidence * weights.base +
      dataQuality * weights.dataQuality +
      modelAccuracy * weights.modelAccuracy +
      historicalSuccess * weights.historicalSuccess +
      (1 - uncertainty) * Math.abs(weights.uncertainty)
    );
    
    // 归一化权重
    const totalWeight = Math.abs(weights.base) + Math.abs(weights.dataQuality) + 
                       Math.abs(weights.modelAccuracy) + Math.abs(weights.historicalSuccess) + 
                       Math.abs(weights.uncertainty);
    confidence = confidence / totalWeight;
    
    // 边界限制
    confidence = Math.max(this.minConfidence, Math.min(this.maxConfidence, confidence));
    
    // 记录历史
    const record = {
      timestamp: Date.now(),
      confidence,
      factors: {
        baseConfidence,
        dataQuality,
        modelAccuracy,
        historicalSuccess,
        uncertainty
      }
    };
    this.confidenceHistory.push(record);
    
    // 更新累积置信度
    this._updateCumulativeConfidence(confidence);
    
    // 更新统计
    this._updateStats(confidence);
    
    // 检查阈值
    this._checkThreshold(confidence);
    
    // 触发事件
    this.emit('calculated', record);
    
    this._log('Confidence calculated', { confidence, factors: record.factors });
    
    return confidence;
  }
  
  /**
   * 计算累积置信度 (多步链式乘积)
   * @param {Array<number>} stepConfidences - 各步骤置信度数组
   * @returns {number} 累积置信度
   */
  calculateCumulative(stepConfidences) {
    if (!Array.isArray(stepConfidences) || stepConfidences.length === 0) {
      return this.defaultConfidence;
    }
    
    // 累积置信度 = 各步骤置信度的乘积
    let cumulative = 1.0;
    for (const conf of stepConfidences) {
      cumulative *= Math.max(0, Math.min(1, conf));
    }
    
    this.cumulativeConfidence = cumulative;
    
    this._log('Cumulative confidence calculated', { 
      steps: stepConfidences.length, 
      cumulative,
      individual: stepConfidences 
    });
    
    this.emit('cumulative-calculated', { 
      cumulative, 
      steps: stepConfidences.length,
      stepConfidences 
    });
    
    return cumulative;
  }
  
  /**
   * 更新累积置信度
   * @private
   */
  _updateCumulativeConfidence(confidence) {
    // 使用衰减因子更新累积置信度
    this.cumulativeConfidence = 
      (this.cumulativeConfidence * this.decayFactor) + 
      (confidence * (1 - this.decayFactor));
    
    // 确保在有效范围内
    this.cumulativeConfidence = Math.max(0, Math.min(1, this.cumulativeConfidence));
  }
  
  /**
   * 更新统计
   * @private
   */
  _updateStats(confidence) {
    if (confidence < this.threshold) {
      this.stats.belowThresholdCount++;
    }
    
    // 重新计算平均置信度
    const total = this.confidenceHistory.length;
    const sum = this.confidenceHistory.reduce((acc, r) => acc + r.confidence, 0);
    this.stats.avgConfidence = total > 0 ? sum / total : this.defaultConfidence;
  }
  
  /**
   * 检查阈值
   * @private
   */
  _checkThreshold(confidence) {
    if (confidence < this.threshold && !this.alertState.belowThreshold) {
      this.alertState.belowThreshold = true;
      this.alertState.lastAlertTime = Date.now();
      
      this.emit('alert', {
        type: 'below-threshold',
        threshold: this.threshold,
        current: confidence,
        message: `Confidence ${(confidence * 100).toFixed(1)}% below threshold ${(this.threshold * 100).toFixed(1)}%`
      });
      
      this._log('Alert: Confidence below threshold', { 
        confidence, 
        threshold: this.threshold 
      });
    } else if (confidence >= this.threshold) {
      this.alertState.belowThreshold = false;
    }
  }
  
  /**
   * 记录步骤置信度
   * @param {string} stepId - 步骤ID
   * @param {number} confidence - 置信度
   * @param {Object} metadata - 元数据
   */
  recordStepConfidence(stepId, confidence, metadata = {}) {
    const record = {
      timestamp: Date.now(),
      confidence,
      metadata
    };
    
    if (!this.stepConfidence.has(stepId)) {
      this.stepConfidence.set(stepId, []);
    }
    
    this.stepConfidence.get(stepId).push(record);
    
    this._log('Step confidence recorded', { stepId, confidence });
    this.emit('step-recorded', { stepId, record });
  }
  
  /**
   * 获取步骤置信度历史
   * @param {string} stepId - 步骤ID
   * @returns {Array|null} 置信度历史
   */
  getStepConfidenceHistory(stepId) {
    return this.stepConfidence.get(stepId) || null;
  }
  
  /**
   * 获取步骤平均置信度
   * @param {string} stepId - 步骤ID
   * @returns {number|null} 平均置信度
   */
  getStepAverageConfidence(stepId) {
    const history = this.stepConfidence.get(stepId);
    if (!history || history.length === 0) return null;
    
    const sum = history.reduce((acc, r) => acc + r.confidence, 0);
    return sum / history.length;
  }
  
  /**
   * 获取当前累积置信度
   * @returns {number} 累积置信度
   */
  getCumulativeConfidence() {
    return this.cumulativeConfidence;
  }
  
  /**
   * 获取置信度历史
   * @param {number} limit - 限制数量
   * @returns {Array} 置信度历史
   */
  getHistory(limit = null) {
    if (limit) {
      return this.confidenceHistory.slice(-limit);
    }
    return [...this.confidenceHistory];
  }
  
  /**
   * 获取置信度趋势
   * @param {number} windowSize - 窗口大小
   * @returns {Object} 趋势信息
   */
  getTrend(windowSize = 10) {
    if (this.confidenceHistory.length < windowSize * 2) {
      return {
        direction: 'insufficient-data',
        change: 0,
        current: this.cumulativeConfidence
      };
    }
    
    const recent = this.confidenceHistory.slice(-windowSize);
    const previous = this.confidenceHistory.slice(-windowSize * 2, -windowSize);
    
    const recentAvg = recent.reduce((acc, r) => acc + r.confidence, 0) / recent.length;
    const previousAvg = previous.reduce((acc, r) => acc + r.confidence, 0) / previous.length;
    
    const change = recentAvg - previousAvg;
    let direction = 'stable';
    if (change > 0.05) direction = 'increasing';
    if (change < -0.05) direction = 'decreasing';
    
    return {
      direction,
      change,
      current: recentAvg,
      previous: previousAvg
    };
  }
  
  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      currentCumulative: this.cumulativeConfidence,
      threshold: this.threshold,
      totalHistory: this.confidenceHistory.length,
      belowThresholdRate: this.stats.totalCalculations > 0 
        ? this.stats.belowThresholdCount / this.stats.totalCalculations 
        : 0
    };
  }
  
  /**
   * 生成置信度可视化数据
   * @param {Object} options - 选项
   * @param {number} options.buckets - 分桶数量 (默认 10)
   * @returns {Object} 可视化数据
   */
  getVisualizationData(options = {}) {
    const buckets = options.buckets || 10;
    const bucketSize = 1 / buckets;
    
    const distribution = new Array(buckets).fill(0);
    
    for (const record of this.confidenceHistory) {
      const bucketIndex = Math.min(
        Math.floor(record.confidence / bucketSize),
        buckets - 1
      );
      distribution[bucketIndex]++;
    }
    
    const labels = [];
    for (let i = 0; i < buckets; i++) {
      const start = (i * bucketSize * 100).toFixed(0);
      const end = ((i + 1) * bucketSize * 100).toFixed(0);
      labels.push(`${start}%-${end}%`);
    }
    
    return {
      distribution,
      labels,
      buckets,
      total: this.confidenceHistory.length,
      threshold: this.threshold,
      avgConfidence: this.stats.avgConfidence
    };
  }
  
  /**
   * 重置计算器
   */
  reset() {
    this.confidenceHistory = [];
    this.cumulativeConfidence = 1.0;
    this.stepConfidence.clear();
    this.alertState = {
      belowThreshold: false,
      lastAlertTime: null
    };
    this.stats = {
      totalCalculations: 0,
      belowThresholdCount: 0,
      avgConfidence: 0
    };
    
    this._log('Calculator reset');
    this.emit('reset');
  }
  
  /**
   * 清理旧数据
   * @param {number} olderThan - 清理多久前的数据(ms)
   */
  cleanup(olderThan) {
    const cutoff = Date.now() - olderThan;
    const beforeLength = this.confidenceHistory.length;
    
    this.confidenceHistory = this.confidenceHistory.filter(r => r.timestamp >= cutoff);
    
    // 清理步骤数据
    for (const [stepId, history] of this.stepConfidence.entries()) {
      const filtered = history.filter(r => r.timestamp >= cutoff);
      if (filtered.length === 0) {
        this.stepConfidence.delete(stepId);
      } else {
        this.stepConfidence.set(stepId, filtered);
      }
    }
    
    const removed = beforeLength - this.confidenceHistory.length;
    this._log('Cleanup completed', { removed, remaining: this.confidenceHistory.length });
    
    return { removed, remaining: this.confidenceHistory.length };
  }
  
  /**
   * 日志记录
   * @private
   */
  _log(message, data = null) {
    if (!this.enableLogging) return;
    
    const timestamp = new Date().toISOString();
    if (data) {
      console.log(`[${timestamp}] [ConfidenceCalculator] ${message}:`, data);
    } else {
      console.log(`[${timestamp}] [ConfidenceCalculator] ${message}`);
    }
  }
}

module.exports = ConfidenceCalculator;
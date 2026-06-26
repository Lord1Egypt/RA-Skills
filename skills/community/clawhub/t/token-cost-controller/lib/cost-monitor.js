/**
 * Cost Monitor - 成本监控与异常检测
 * 使用动态阈值和变异系数进行智能异常检测
 */
const fs = require('fs');
const path = require('path');

/**
 * 简单的统计计算器
 */
class StatsCalculator {
  constructor() {
    this.values = [];
    this.cache = null;
    this.cacheTime = 0;
    this.cacheTTL = 5 * 60 * 1000; // 5分钟缓存
  }

  add(value) {
    this.values.push(value);
    this.cache = null; // 清除缓存
  }

  /**
   * 计算平均值
   */
  mean() {
    if (this.cache && Date.now() - this.cacheTime < this.cacheTTL) {
      return this.cache.mean;
    }
    if (this.values.length === 0) return 0;
    const mean = this.values.reduce((a, b) => a + b, 0) / this.values.length;
    this.cache = { ...this.cache, mean };
    this.cacheTime = Date.now();
    return mean;
  }

  /**
   * 计算标准差
   */
  std() {
    if (this.values.length === 0) return 0;
    const avg = this.mean();
    const variance = this.values.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / this.values.length;
    return Math.sqrt(variance);
  }

  /**
   * 计算变异系数 (CV)
   */
  coefficientOfVariation() {
    const avg = this.mean();
    if (avg === 0) return 1;
    return this.std() / avg;
  }

  /**
   * 动态计算异常阈值
   */
  dynamicThreshold() {
    const cv = this.coefficientOfVariation();
    const avg = this.mean();

    // CV越高，说明波动越大，阈值应该更宽松
    const multiplier = 1.5 + cv;
    return avg * multiplier;
  }
}

class CostMonitor {
  constructor(config = {}) {
    this.config = config;
    this.history = new Map(); // skill -> StatsCalculator
    this.alerts = [];
    this.spikeMultiplier = config.spikeMultiplier || 2.5;
    this.dataDir = config.dataDir || path.join(__dirname, '..', '.openclaw', 'data');

    this.loadHistory();
  }

  /**
   * 记录一次成本消耗
   */
  record(skillName, cost, tokens = {}) {
    if (!this.history.has(skillName)) {
      this.history.set(skillName, new StatsCalculator());
    }

    const stats = this.history.get(skillName);
    stats.add(cost);

    // 检查异常
    const alert = this.checkAnomaly(skillName, cost, stats);
    if (alert) {
      this.alerts.push(alert);
    }

    this.saveHistory();
    return alert;
  }

  /**
   * 检查异常
   */
  checkAnomaly(skillName, cost, stats) {
    const avg = stats.mean();
    const threshold = stats.dynamicThreshold();

    if (cost > threshold && avg > 0) {
      const spike = ((cost - avg) / avg * 100).toFixed(0);
      return {
        skill: skillName,
        cost,
        avg: avg.toFixed(4),
        spike: spike + '%',
        timestamp: new Date().toISOString(),
        severity: cost > threshold * 2 ? 'high' : 'medium'
      };
    }
    return null;
  }

  /**
   * 获取技能统计
   */
  getStats(skillName) {
    const stats = this.history.get(skillName);
    if (!stats) return null;

    return {
      mean: stats.mean().toFixed(4),
      std: stats.std().toFixed(4),
      cv: stats.coefficientOfVariation().toFixed(2),
      threshold: stats.dynamicThreshold().toFixed(4),
      samples: stats.values.length
    };
  }

  /**
   * 获取Top消耗技能
   */
  getTopSkills(limit = 5) {
    const results = [];

    for (const [skill, stats] of this.history) {
      results.push({
        skill,
        avgCost: stats.mean().toFixed(4),
        samples: stats.values.length
      });
    }

    return results
      .sort((a, b) => parseFloat(b.avgCost) - parseFloat(a.avgCost))
      .slice(0, limit);
  }

  /**
   * 获取所有警报
   */
  getAlerts() {
    return this.alerts.slice(-50); // 最近50条
  }

  /**
   * 清除警报
   */
  clearAlerts() {
    this.alerts = [];
  }

  /**
   * 加载历史记录
   */
  loadHistory() {
    try {
      const file = path.join(this.dataDir, 'cost-history.json');
      if (fs.existsSync(file)) {
        const data = JSON.parse(fs.readFileSync(file, 'utf8'));
        for (const [skill, values] of Object.entries(data)) {
          const stats = new StatsCalculator();
          values.forEach(v => stats.add(v));
          this.history.set(skill, stats);
        }
      }
    } catch (e) {
      // 忽略
    }
  }

  /**
   * 保存历史记录
   */
  saveHistory() {
    try {
      const data = {};
      for (const [skill, stats] of this.history) {
        data[skill] = stats.values.slice(-1000); // 保留最近1000条
      }
      fs.mkdirSync(this.dataDir, { recursive: true });
      fs.writeFileSync(
        path.join(this.dataDir, 'cost-history.json'),
        JSON.stringify(data)
      );
    } catch (e) {
      // 忽略
    }
  }
}

module.exports = CostMonitor;

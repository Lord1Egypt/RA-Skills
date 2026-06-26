/**
 * Proactive Monitor - 主动监控与管控
 * 使用 Ring Buffer 追踪异常历史，支持技能管控
 */
const fs = require('fs');
const path = require('path');

/**
 * Ring Buffer for anomaly history
 */
class RingBuffer {
  constructor(size) {
    this.size = size;
    this.buffer = [];
    this.index = 0;
  }

  push(item) {
    if (this.buffer.length < this.size) {
      this.buffer.push(item);
    } else {
      this.buffer[this.index] = item;
    }
    this.index = (this.index + 1) % this.size;
  }

  toArray() {
    if (this.buffer.length < this.size) {
      return [...this.buffer];
    }
    return [...this.buffer.slice(this.index), ...this.buffer.slice(0, this.index)];
  }
}

class ProactiveMonitor {
  constructor(config = {}) {
    this.config = config;
    this.anomalyHistory = new RingBuffer(100);
    this.disabledSkills = new Set();
    this.pausedPlans = new Set();
    this.maxCostPerSkill = new Map();
    this.skillCosts = new Map();
    this.dataDir = config.dataDir || path.join(__dirname, '..', '.openclaw', 'data');

    this.loadControls();
  }

  /**
   * 记录异常事件
   */
  recordAnomaly(skillName, details) {
    this.anomalyHistory.push({
      skill: skillName,
      ...details,
      timestamp: Date.now()
    });
  }

  /**
   * 禁用技能
   */
  disableSkill(skillName) {
    this.disabledSkills.add(skillName);
    this.saveControls();
    return `已禁用技能: ${skillName}`;
  }

  /**
   * 启用技能
   */
  enableSkill(skillName) {
    this.disabledSkills.delete(skillName);
    this.saveControls();
    return `已启用技能: ${skillName}`;
  }

  /**
   * 设置技能成本上限
   */
  setMaxCost(skillName, maxCost) {
    this.maxCostPerSkill.set(skillName, maxCost);
    this.skillCosts.set(skillName, 0);
    this.saveControls();
    return `已设置 ${skillName} 成本上限: $${maxCost}`;
  }

  /**
   * 记录技能消耗
   */
  recordCost(skillName, cost) {
    if (this.disabledSkills.has(skillName)) {
      return { allowed: false, reason: '技能已被禁用' };
    }

    const current = this.skillCosts.get(skillName) || 0;
    const max = this.maxCostPerSkill.get(skillName);

    if (max !== undefined && current + cost > max) {
      return {
        allowed: false,
        reason: `超过成本上限 ($ ${max})`
      };
    }

    this.skillCosts.set(skillName, current + cost);
    return { allowed: true };
  }

  /**
   * 暂停计划
   */
  pausePlan(planName) {
    this.pausedPlans.add(planName);
    this.saveControls();
    return `已暂停计划: ${planName}`;
  }

  /**
   * 恢复计划
   */
  resumePlan(planName) {
    this.pausedPlans.delete(planName);
    this.saveControls();
    return `已恢复计划: ${planName}`;
  }

  /**
   * 获取管控状态
   */
  getControls() {
    return {
      disabledSkills: [...this.disabledSkills],
      pausedPlans: [...this.pausedPlans],
      maxCostPerSkill: Object.fromEntries(this.maxCostPerSkill),
      skillCosts: Object.fromEntries(this.skillCosts),
      recentAnomalies: this.anomalyHistory.toArray().slice(-10)
    };
  }

  /**
   * 加载管控配置
   */
  loadControls() {
    try {
      const file = path.join(this.dataDir, 'controls.json');
      if (fs.existsSync(file)) {
        const data = JSON.parse(fs.readFileSync(file, 'utf8'));
        this.disabledSkills = new Set(data.disabledSkills || []);
        this.pausedPlans = new Set(data.pausedPlans || []);
        this.maxCostPerSkill = new Map(Object.entries(data.maxCostPerSkill || {}));
        this.skillCosts = new Map(Object.entries(data.skillCosts || {}));
      }
    } catch (e) {
      // 忽略
    }
  }

  /**
   * 保存管控配置
   */
  saveControls() {
    try {
      fs.mkdirSync(this.dataDir, { recursive: true });
      const file = path.join(this.dataDir, 'controls.json');
      fs.writeFileSync(file, JSON.stringify({
        disabledSkills: [...this.disabledSkills],
        pausedPlans: [...this.pausedPlans],
        maxCostPerSkill: Object.fromEntries(this.maxCostPerSkill),
        skillCosts: Object.fromEntries(this.skillCosts)
      }, null, 2));
    } catch (e) {
      // 忽略
    }
  }
}

module.exports = ProactiveMonitor;

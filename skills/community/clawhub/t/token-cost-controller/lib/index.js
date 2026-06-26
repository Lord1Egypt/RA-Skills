/**
 * OpenClaw Token省钱管家 - 主入口
 */
const ModelRouter = require('./model-router');
const CacheManager = require('./cache-manager');
const CostMonitor = require('./cost-monitor');
const ProactiveMonitor = require('./proactive-monitor');

class TokenCostController {
  constructor(config = {}) {
    this.config = config;
    this.modelRouter = new ModelRouter(config);
    this.cacheManager = new CacheManager(config);
    this.costMonitor = new CostMonitor(config);
    this.proactiveMonitor = new ProactiveMonitor(config);
  }

  /**
   * 记录成本
   */
  recordCost(skillName, cost, tokens = {}) {
    // 检查是否允许
    const check = this.proactiveMonitor.recordCost(skillName, cost);
    if (!check.allowed) {
      return { blocked: true, reason: check.reason };
    }

    // 记录到监控器
    const alert = this.costMonitor.record(skillName, cost, tokens);

    // 如果有异常告警
    if (alert) {
      this.proactiveMonitor.recordAnomaly(skillName, alert);
    }

    return { blocked: false, alert };
  }

  /**
   * 获取报告
   */
  getReport() {
    return {
      topSkills: this.costMonitor.getTopSkills(5),
      alerts: this.costMonitor.getAlerts(),
      controls: this.proactiveMonitor.getControls(),
      cache: this.cacheManager.getStats()
    };
  }

  /**
   * 禁用技能
   */
  disableSkill(skillName) {
    return this.proactiveMonitor.disableSkill(skillName);
  }

  /**
   * 设置成本上限
   */
  setMaxCost(skillName, maxCost) {
    return this.proactiveMonitor.setMaxCost(skillName, maxCost);
  }

  /**
   * 选择最优模型
   */
  async selectModel(task) {
    return await this.modelRouter.selectModel(task);
  }

  /**
   * 获取缓存
   */
  getCache(key) {
    return this.cacheManager.get(key);
  }

  /**
   * 设置缓存
   */
  setCache(key, value) {
    this.cacheManager.set(key, value);
  }
}

module.exports = TokenCostController;

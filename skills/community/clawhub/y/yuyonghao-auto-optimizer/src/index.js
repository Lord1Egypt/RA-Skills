/**
 * Auto Optimizer - 自动性能优化工具
 * 主入口文件
 */

const { PerformanceMonitor } = require('./monitor');
const { BottleneckAnalyzer } = require('./analyzer');
const { OptimizationEngine } = require('./optimizer');
const { OptimizationApplier } = require('./applier');

class AutoOptimizer {
  constructor(options = {}) {
    this.monitor = new PerformanceMonitor(options.monitor);
    this.analyzer = new BottleneckAnalyzer(options.analyzer);
    this.optimizer = new OptimizationEngine(options.optimizer);
    this.applier = new OptimizationApplier(options.applier);
    this.options = options;
  }

  /**
   * 监控技能执行
   * @param {string} operationId - 操作ID
   * @param {string} skillName - 技能名称
   * @param {Function} operation - 要执行的操作
   * @returns {Promise<Object>} 执行结果和指标
   */
  async monitorOperation(operationId, skillName, operation) {
    this.monitor.startOperation(operationId, skillName);
    
    try {
      const result = await operation();
      const metrics = this.monitor.endOperation(operationId, result);
      return { result, metrics };
    } catch (error) {
      const metrics = this.monitor.endOperation(operationId, null, error);
      throw { error, metrics };
    }
  }

  /**
   * 分析技能性能
   * @param {string} skillName - 技能名称
   * @returns {Object} 分析结果
   */
  analyzeSkill(skillName) {
    const history = this.monitor.getHistory();
    const skillMetrics = history.filter(m => m.skillName === skillName);
    return this.analyzer.analyzeSkill(skillName, skillMetrics);
  }

  /**
   * 分析所有技能
   * @returns {Object} 分析结果
   */
  analyzeAllSkills() {
    const allHistory = this.monitor.getHistory();
    const skillsData = {};
    
    for (const metric of allHistory) {
      if (!skillsData[metric.skillName]) {
        skillsData[metric.skillName] = [];
      }
      skillsData[metric.skillName].push(metric);
    }
    
    return this.analyzer.analyzeMultipleSkills(skillsData);
  }

  /**
   * 生成优化方案
   * @param {string} skillName - 技能名称
   * @returns {Object} 优化方案
   */
  generatePlan(skillName) {
    const analysis = this.analyzeSkill(skillName);
    return this.optimizer.generateOptimizationPlan(analysis);
  }

  /**
   * 应用优化方案
   * @param {Object} plan - 优化方案
   * @param {Object} context - 上下文
   * @returns {Promise<Object>} 应用结果
   */
  async applyPlan(plan, context = {}) {
    return this.applier.applyOptimizationPlan(plan, context);
  }

  /**
   * 完整的优化流程
   * @param {string} skillName - 技能名称
   * @param {Object} context - 上下文
   * @returns {Promise<Object>} 优化结果
   */
  async optimizeSkill(skillName, context = {}) {
    // 1. 分析
    const analysis = this.analyzeSkill(skillName);
    
    if (analysis.status === 'insufficient_data') {
      return {
        skillName,
        status: 'skipped',
        reason: 'insufficient_data',
        message: analysis.message
      };
    }

    if (analysis.status === 'healthy') {
      return {
        skillName,
        status: 'healthy',
        analysis,
        message: 'No bottlenecks detected'
      };
    }

    // 2. 生成优化方案
    const plan = this.optimizer.generateOptimizationPlan(analysis);

    // 3. 应用优化
    const application = await this.applyPlan(plan, context);

    return {
      skillName,
      status: 'optimized',
      analysis,
      plan,
      application
    };
  }

  /**
   * 获取监控统计
   * @returns {Object} 统计信息
   */
  getStats() {
    return this.monitor.getAllStats();
  }

  /**
   * 导出报告
   * @param {string} format - 格式
   * @returns {string} 报告内容
   */
  exportReport(format = 'json') {
    return this.monitor.exportReport(format);
  }
}

module.exports = {
  AutoOptimizer,
  PerformanceMonitor,
  BottleneckAnalyzer,
  OptimizationEngine,
  OptimizationApplier
};

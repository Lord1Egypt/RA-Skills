/**
 * skill-health-monitor - 技能健康监控器
 * 
 * 设计模式应用：
 * 1. 单例模式（Singleton）- 确保全局只有一个监控实例
 * 2. 责任链模式（Chain of Responsibility）- 多级健康检查处理器
 * 3. 模板方法模式（Template Method）- 定义健康检查标准流程
 */

// ============================================
// 单例模式实现
// ============================================

class HealthMonitorInstance {
  constructor() {
    if (HealthMonitorInstance._instance) {
      return HealthMonitorInstance._instance;
    }
    HealthMonitorInstance._instance = this;
    
    this.checks = new Map();
    this.alerts = [];
    this.thresholds = {
      warning: 0.70,
      critical: 0.50,
      emergency: 0.30
    };
  }
}

// ============================================
// 责任链模式 - 健康检查处理器
// ============================================

class HealthCheckHandler {
  constructor() {
    this.nextHandler = null;
  }

  setNext(handler) {
    this.nextHandler = handler;
    return handler;
  }

  handle(skillData) {
    const result = this.processCheck(skillData);
    
    if (this.nextHandler && !result.shouldStop) {
      return this.nextHandler.handle(skillData);
    }
    
    return result;
  }

  processCheck(skillData) {
    // 子类实现
    return { level: 'ok', message: '检查通过', shouldStop: false };
  }
}

class EmergencyCheckHandler extends HealthCheckHandler {
  processCheck(skillData) {
    const score = skillData.healthScore || 1.0;
    
    if (score < 0.30) {
      return {
        level: 'emergency',
        message: `紧急：技能健康度 ${score.toFixed(2)} < 0.30，需要立即干预`,
        shouldStop: true,
        recommendations: ['立即停止服务', '回滚到上一版本', '通知维护者']
      };
    }
    
    return { level: 'ok', shouldStop: false };
  }
}

class CriticalCheckHandler extends HealthCheckHandler {
  processCheck(skillData) {
    const score = skillData.healthScore || 1.0;
    
    if (score < 0.50) {
      return {
        level: 'critical',
        message: `严重：技能健康度 ${score.toFixed(2)} < 0.50，需要尽快修复`,
        shouldStop: true,
        recommendations: ['安排紧急修复', '增加监控频率', '准备回滚方案']
      };
    }
    
    return { level: 'ok', shouldStop: false };
  }
}

class WarningCheckHandler extends HealthCheckHandler {
  processCheck(skillData) {
    const score = skillData.healthScore || 1.0;
    
    if (score < 0.70) {
      return {
        level: 'warning',
        message: `警告：技能健康度 ${score.toFixed(2)} < 0.70，建议优化`,
        shouldStop: false,
        recommendations: ['分析短板维度', '制定优化计划', '安排改进时间']
      };
    }
    
    return { level: 'ok', shouldStop: false };
  }
}

// ============================================
// 模板方法模式 - 健康检查流程
// ============================================

class HealthCheckTemplate {
  constructor() {
    this.monitor = new HealthMonitorInstance();
    
    // 构建责任链
    this.chain = new EmergencyCheckHandler()
      .setNext(new CriticalCheckHandler())
      .setNext(new WarningCheckHandler());
  }

  /**
   * 模板方法：定义健康检查的标准流程
   */
  async checkSkillHealth(skillName, metrics) {
    // 步骤 1: 收集数据（具体实现由子类决定）
    const skillData = this.collectSkillData(skillName, metrics);
    
    // 步骤 2: 计算健康分数
    const healthScore = this.calculateHealthScore(skillData);
    skillData.healthScore = healthScore;
    
    // 步骤 3: 执行责任链检查
    const checkResult = this.chain.handle(skillData);
    
    // 步骤 4: 记录结果
    this.recordCheckResult(skillName, healthScore, checkResult);
    
    // 步骤 5: 生成报告
    const report = this.generateReport(skillName, skillData, checkResult);
    
    return report;
  }

  collectSkillData(skillName, metrics) {
    return {
      name: skillName,
      timestamp: new Date().toISOString(),
      metrics: metrics || {},
      healthScore: 1.0
    };
  }

  calculateHealthScore(skillData) {
    const metrics = skillData.metrics;
    
    // 六维评估加权平均
    const dimensions = {
      T: metrics.technicalDepth || 0.70,      // 技术深度
      C: metrics.cognitiveEnhancement || 0.70, // 认知增强
      O: metrics.orchestration || 0.70,        // 编排能力
      E: metrics.evolution || 0.70,            // 进化能力
      M: metrics.commercialization || 0.70,    // 商业化
      U: metrics.userExperience || 0.70        // 用户体验
    };
    
    // 计算平均分
    const scores = Object.values(dimensions);
    const average = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    return average;
  }

  recordCheckResult(skillName, healthScore, checkResult) {
    this.monitor.checks.set(skillName, {
      score: healthScore,
      level: checkResult.level,
      timestamp: new Date().toISOString()
    });
    
    if (checkResult.level !== 'ok') {
      this.monitor.alerts.push({
        skill: skillName,
        level: checkResult.level,
        message: checkResult.message,
        timestamp: new Date().toISOString()
      });
    }
  }

  generateReport(skillName, skillData, checkResult) {
    const dimensions = skillData.metrics;
    
    return {
      skillName,
      healthScore: skillData.healthScore,
      level: checkResult.level,
      message: checkResult.message,
      recommendations: checkResult.recommendations || [],
      dimensions: {
        technicalDepth: dimensions.T,
        cognitiveEnhancement: dimensions.C,
        orchestration: dimensions.O,
        evolution: dimensions.E,
        commercialization: dimensions.M,
        userExperience: dimensions.U
      },
      timestamp: skillData.timestamp
    };
  }
}

// ============================================
// 导出
// ============================================

module.exports = {
  HealthMonitor: HealthMonitorInstance,
  HealthCheckHandler,
  EmergencyCheckHandler,
  CriticalCheckHandler,
  WarningCheckHandler,
  HealthCheckTemplate
};

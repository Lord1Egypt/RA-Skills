/**
 * AlertManager - 告警管理器
 * 
 * 功能:
 * - 阈值告警（Counter/Gauge/Histogram）
 * - 规则引擎（支持复杂条件）
 * - 多渠道通知（Console/File/Webhook）
 * - 告警抑制和恢复
 * - 告警历史记录
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 * @date 2026-03-20
 */

class AlertRule {
  constructor(config) {
    this.id = config.id || `rule-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.name = config.name || 'Unnamed Rule';
    this.description = config.description || '';
    
    // 告警条件
    this.metric = config.metric; // 指标名称
    this.metricType = config.metricType || 'gauge'; // counter/gauge/histogram
    this.condition = config.condition || 'gt'; // gt/lt/eq/gte/lte
    this.threshold = config.threshold; // 阈值
    this.duration = config.duration || 0; // 持续时间（毫秒），0表示立即触发
    
    // 告警级别
    this.severity = config.severity || 'warning'; // critical/warning/info
    
    // 通知配置
    this.channels = config.channels || ['console']; // console/file/webhook
    this.webhookUrl = config.webhookUrl || null;
    
    // 抑制配置
    this.cooldown = config.cooldown || 300000; // 默认5分钟冷却
    this.maxAlerts = config.maxAlerts || 10; // 最大告警次数
    
    // 状态
    this.state = 'normal'; // normal/pending/firing/recovered
    this.lastAlertTime = null;
    this.alertCount = 0;
    this.pendingSince = null;
    this.recoveryTime = null;
  }

  /**
   * 检查是否满足告警条件
   */
  check(value) {
    const conditions = {
      gt: (v, t) => v > t,
      lt: (v, t) => v < t,
      eq: (v, t) => v === t,
      gte: (v, t) => v >= t,
      lte: (v, t) => v <= t,
      neq: (v, t) => v !== t
    };

    const checkFn = conditions[this.condition];
    if (!checkFn) {
      throw new Error(`Unknown condition: ${this.condition}`);
    }

    return checkFn(value, this.threshold);
  }

  /**
   * 是否可以发送告警（冷却检查）
   */
  canAlert() {
    if (this.alertCount >= this.maxAlerts) {
      return false;
    }
    
    if (!this.lastAlertTime) {
      return true;
    }
    
    return Date.now() - this.lastAlertTime >= this.cooldown;
  }

  /**
   * 记录告警
   */
  recordAlert() {
    this.lastAlertTime = Date.now();
    this.alertCount++;
    this.state = 'firing';
  }

  /**
   * 记录恢复
   */
  recordRecovery() {
    this.recoveryTime = Date.now();
    this.state = 'recovered';
    this.pendingSince = null;
  }

  /**
   * 重置状态
   */
  reset() {
    this.state = 'normal';
    this.lastAlertTime = null;
    this.alertCount = 0;
    this.pendingSince = null;
    this.recoveryTime = null;
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      metric: this.metric,
      metricType: this.metricType,
      condition: this.condition,
      threshold: this.threshold,
      severity: this.severity,
      state: this.state,
      lastAlertTime: this.lastAlertTime,
      alertCount: this.alertCount,
      recoveryTime: this.recoveryTime
    };
  }
}

class AlertManager {
  constructor(options = {}) {
    this.options = {
      enabled: options.enabled !== false,
      checkInterval: options.checkInterval || 30000, // 默认30秒检查一次
      maxHistory: options.maxHistory || 1000,
      logAlerts: options.logAlerts !== false,
      ...options
    };

    this.rules = new Map(); // id -> AlertRule
    this.history = []; // 告警历史
    this.notifications = []; // 待发送通知队列
    this.metricsCollector = options.metricsCollector || null;
    this.logger = options.logger || null;

    // 通知处理器
    this.notificationHandlers = {
      console: this._notifyConsole.bind(this),
      file: this._notifyFile.bind(this),
      webhook: this._notifyWebhook.bind(this)
    };

    // 启动检查循环
    if (this.options.enabled) {
      this.start();
    }
  }

  /**
   * 启动告警管理器
   */
  start() {
    if (this.checkIntervalId) {
      return;
    }

    this.checkIntervalId = setInterval(() => {
      this._checkAllRules();
    }, this.options.checkInterval);

    this.logger?.info('[AlertManager] Started', {
      checkInterval: this.options.checkInterval
    });
  }

  /**
   * 停止告警管理器
   */
  stop() {
    if (this.checkIntervalId) {
      clearInterval(this.checkIntervalId);
      this.checkIntervalId = null;
    }

    this.logger?.info('[AlertManager] Stopped');
  }

  /**
   * 添加告警规则
   */
  addRule(config) {
    const rule = new AlertRule(config);
    this.rules.set(rule.id, rule);
    
    this.logger?.info(`[AlertManager] Rule added: ${rule.name}`, {
      ruleId: rule.id,
      metric: rule.metric,
      threshold: rule.threshold
    });

    return rule.id;
  }

  /**
   * 删除告警规则
   */
  removeRule(ruleId) {
    const rule = this.rules.get(ruleId);
    if (rule) {
      this.rules.delete(ruleId);
      this.logger?.info(`[AlertManager] Rule removed: ${rule.name}`, { ruleId });
      return true;
    }
    return false;
  }

  /**
   * 获取规则
   */
  getRule(ruleId) {
    return this.rules.get(ruleId);
  }

  /**
   * 获取所有规则
   */
  getAllRules() {
    return Array.from(this.rules.values()).map(r => r.toJSON());
  }

  /**
   * 触发告警（手动）
   */
  fireAlert(ruleId, value, message = null) {
    const rule = this.rules.get(ruleId);
    if (!rule) {
      this.logger?.warn(`[AlertManager] Rule not found: ${ruleId}`);
      return false;
    }

    const alert = {
      id: `alert-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      ruleId: rule.id,
      ruleName: rule.name,
      severity: rule.severity,
      value,
      threshold: rule.threshold,
      condition: rule.condition,
      message: message || `${rule.name}: ${value} ${rule.condition} ${rule.threshold}`,
      timestamp: Date.now(),
      channels: rule.channels
    };

    // 添加到历史
    this._addToHistory(alert);

    // 发送通知
    this._sendNotification(alert, rule);

    // 记录规则状态
    rule.recordAlert();

    this.logger?.warn(`[ALERT FIRING] ${alert.message}`, {
      alertId: alert.id,
      ruleId: rule.id,
      severity: rule.severity,
      value,
      threshold: rule.threshold
    });

    return alert;
  }

  /**
   * 解除告警
   */
  resolveAlert(ruleId, message = null) {
    const rule = this.rules.get(ruleId);
    if (!rule) {
      return false;
    }

    if (rule.state === 'firing') {
      const recovery = {
        id: `recovery-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        ruleId: rule.id,
        ruleName: rule.name,
        type: 'recovery',
        message: message || `${rule.name} has recovered`,
        timestamp: Date.now()
      };

      this._addToHistory(recovery);
      rule.recordRecovery();

      this.logger?.info(`[ALERT RECOVERED] ${recovery.message}`, {
        ruleId: rule.id,
        recoveryId: recovery.id
      });

      return recovery;
    }

    return null;
  }

  /**
   * 检查所有规则
   */
  _checkAllRules() {
    if (!this.metricsCollector) {
      return;
    }

    const metrics = this.metricsCollector.getMetrics();

    for (const rule of this.rules.values()) {
      this._checkRule(rule, metrics);
    }
  }

  /**
   * 检查单个规则
   */
  _checkRule(rule, metrics) {
    let value = null;

    // 根据指标类型获取值
    switch (rule.metricType) {
      case 'counter':
        value = metrics.counters[rule.metric]?.value;
        break;
      case 'gauge':
        value = metrics.gauges[rule.metric]?.value;
        break;
      case 'histogram':
        // 对于 histogram，检查平均值或P99
        const hist = metrics.histograms[rule.metric];
        if (hist) {
          value = hist.avg; // 或者使用 hist.percentiles.p99
        }
        break;
    }

    if (value === undefined || value === null) {
      return;
    }

    const shouldFire = rule.check(value);

    if (shouldFire) {
      // 需要触发告警
      if (rule.state === 'normal') {
        // 进入 pending 状态
        if (rule.duration > 0) {
          rule.state = 'pending';
          rule.pendingSince = Date.now();
        } else {
          // 立即触发
          if (rule.canAlert()) {
            this.fireAlert(rule.id, value);
          }
        }
      } else if (rule.state === 'pending') {
        // 检查是否满足持续时间
        if (Date.now() - rule.pendingSince >= rule.duration) {
          if (rule.canAlert()) {
            this.fireAlert(rule.id, value);
          }
        }
      }
    } else {
      // 不满足条件，检查是否需要恢复
      if (rule.state === 'firing' || rule.state === 'pending') {
        this.resolveAlert(rule.id);
      }
    }
  }

  /**
   * 添加到历史记录
   */
  _addToHistory(alert) {
    this.history.push(alert);
    
    if (this.history.length > this.options.maxHistory) {
      this.history.shift();
    }
  }

  /**
   * 发送通知
   */
  _sendNotification(alert, rule) {
    for (const channel of alert.channels) {
      const handler = this.notificationHandlers[channel];
      if (handler) {
        try {
          handler(alert, rule);
        } catch (error) {
          this.logger?.error(`[AlertManager] Failed to send ${channel} notification`, {
            alertId: alert.id,
            error: error.message
          });
        }
      }
    }
  }

  /**
   * Console 通知
   */
  _notifyConsole(alert, rule) {
    const severityColors = {
      critical: '\x1b[31m', // Red
      warning: '\x1b[33m',  // Yellow
      info: '\x1b[36m'      // Cyan
    };
    const resetColor = '\x1b[0m';
    const color = severityColors[alert.severity] || '';
    
    console.log(`${color}[ALERT ${alert.severity.toUpperCase()}] ${alert.message}${resetColor}`);
  }

  /**
   * File 通知
   */
  _notifyFile(alert, rule) {
    // 通过 logger 记录
    if (this.logger) {
      const level = alert.severity === 'critical' ? 'error' : 'warn';
      this.logger[level](`[ALERT] ${alert.message}`, {
        alertId: alert.id,
        ruleId: rule.id,
        severity: alert.severity,
        value: alert.value,
        threshold: alert.threshold
      });
    }
  }

  /**
   * Webhook 通知
   */
  async _notifyWebhook(alert, rule) {
    if (!rule.webhookUrl) {
      return;
    }

    try {
      const payload = {
        alert: alert,
        rule: rule.toJSON(),
        timestamp: new Date().toISOString()
      };

      // 使用 fetch 发送 webhook
      const fetch = global.fetch || require('node-fetch');
      await fetch(rule.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
    } catch (error) {
      this.logger?.error('[AlertManager] Webhook notification failed', {
        alertId: alert.id,
        webhookUrl: rule.webhookUrl,
        error: error.message
      });
    }
  }

  /**
   * 获取告警历史
   */
  getHistory(options = {}) {
    let history = [...this.history];
    
    if (options.since) {
      history = history.filter(h => h.timestamp >= options.since);
    }
    
    if (options.ruleId) {
      history = history.filter(h => h.ruleId === options.ruleId);
    }
    
    if (options.severity) {
      history = history.filter(h => h.severity === options.severity);
    }
    
    if (options.limit) {
      history = history.slice(-options.limit);
    }
    
    return history;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const now = Date.now();
    const last24h = now - 24 * 60 * 60 * 1000;
    
    const recentAlerts = this.history.filter(h => 
      h.timestamp >= last24h && !h.type
    );
    
    const recentRecoveries = this.history.filter(h => 
      h.timestamp >= last24h && h.type === 'recovery'
    );

    return {
      totalRules: this.rules.size,
      firingRules: Array.from(this.rules.values()).filter(r => r.state === 'firing').length,
      pendingRules: Array.from(this.rules.values()).filter(r => r.state === 'pending').length,
      totalAlerts24h: recentAlerts.length,
      totalRecoveries24h: recentRecoveries.length,
      historySize: this.history.length
    };
  }

  /**
   * 重置所有规则
   */
  reset() {
    for (const rule of this.rules.values()) {
      rule.reset();
    }
    this.history = [];
    
    this.logger?.info('[AlertManager] All rules reset');
  }

  /**
   * 创建常用告警规则
   */
  createDefaultRules() {
    // 高延迟告警
    this.addRule({
      name: 'High Latency Alert',
      description: 'Triggered when average latency exceeds 1000ms',
      metric: 'agent.calls.latency',
      metricType: 'histogram',
      condition: 'gt',
      threshold: 1000,
      severity: 'warning',
      channels: ['console', 'file'],
      cooldown: 60000 // 1分钟冷却
    });

    // 错误率告警
    this.addRule({
      name: 'High Error Rate',
      description: 'Triggered when error count exceeds 10',
      metric: 'agent.errors.total',
      metricType: 'counter',
      condition: 'gt',
      threshold: 10,
      severity: 'critical',
      channels: ['console', 'file'],
      cooldown: 30000 // 30秒冷却
    });

    // LLM Token 使用量告警
    this.addRule({
      name: 'High Token Usage',
      description: 'Triggered when token usage exceeds 10000',
      metric: 'agent.llm.tokens.total',
      metricType: 'counter',
      condition: 'gt',
      threshold: 10000,
      severity: 'warning',
      channels: ['console'],
      cooldown: 300000 // 5分钟冷却
    });

    // MCP 错误告警
    this.addRule({
      name: 'MCP Tool Errors',
      description: 'Triggered when MCP tool errors exceed 5',
      metric: 'agent.mcp.errors.total',
      metricType: 'counter',
      condition: 'gt',
      threshold: 5,
      severity: 'warning',
      channels: ['console', 'file'],
      cooldown: 60000
    });

    this.logger?.info('[AlertManager] Default rules created');
  }
}

module.exports = { AlertManager, AlertRule };

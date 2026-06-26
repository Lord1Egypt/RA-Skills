#!/usr/bin/env node

/**
 * 企微 Agent Ops Center v2.2 — 资源指标采集引擎
 * 架构位置：L2 核心监控引擎
 *
 * 职责：
 * 1. 接收适配器推送的资源快照（CPU/内存/队列/磁盘）
 * 2. 存储时序资源数据到 StateStore
 * 3. 阈值告警：CPU>80% / 内存>90% / 队列深度>10 / 磁盘>90%
 * 4. 趋势分析：持续上升/下降检测
 * 5. 提供 HTTP API 供仪表板查询
 *
 * 数据流：
 *   Adapter 'resource' event → ResourceCollector.report()
 *     → StateStore.addResourceSnapshot() → 持久化
 *     → 阈值检查 → NotifyEngine.resourceAlertCard() → 企微推送
 *     → Dashboard API → 仪表板渲染
 */

const DEFAULTS = {
  thresholds: {
    cpu:        80,   // CPU 使用率告警阈值 (%)
    memory:     90,   // 内存使用率告警阈值 (%)
    queueDepth: 10,   // 队列深度告警阈值
    disk:       90,   // 磁盘使用率告警阈值 (%，仅 OpenClaw 自托管)
  },
  maxHistory: 1440,     // 每个 Agent 最多保留资源快照数（24h * 60min）
  trendWindow: 10,      // 趋势分析窗口（最近 N 个快照）
  alertCooldown: 600_000, // 同类型告警冷却（10 分钟）
};

class ResourceCollector {
  constructor(config) {
    this.config     = { ...DEFAULTS, ...(config || {}) };
    this.stateStore = config.stateStore || null;
    this.notifyEngine = config.notifyEngine || null;
    this._alertThrottle = new Map(); // agentId:metric → lastAlertTime
    this.stats = {
      totalSnapshots: 0,
      totalAlerts: 0,
      lastSnapshot: null,
    };
  }

  // ─── 公开 API ──────────────────────────────────────────────

  /**
   * 接收并处理资源快照
   * 由适配器 'resource' 事件调用，或由 HTTP POST /api/resources/report 调用
   *
   * @param {object} data — 来自适配器的事件数据
   * @param {string} data.agentId
   * @param {string} data.agentName
   * @param {string} data.adapterType
   * @param {number} data.timestamp
   * @param {number} [data.cpu]         — CPU 使用率 %
   * @param {number} [data.memory]      — 内存使用率 %
   * @param {number} [data.memoryUsed]  — 已用 MB
   * @param {number} [data.memoryTotal] — 总 MB
   * @param {number} [data.queueDepth]  — 队列深度
   * @param {number} [data.concurrency] — 并发数
   * @param {boolean} [data.selfHosted] — 是否自托管
   * @param {object} [data.disk]        — 磁盘信息 { usedPercent, available, size, used }
   */
  async report(data) {
    const { agentId, agentName, adapterType, timestamp } = data;

    // 1. 构建快照
    const snapshot = {
      agentId,
      agentName: agentName || agentId,
      adapterType: adapterType || 'unknown',
      timestamp: timestamp || Date.now(),
      cpu:         this._n(data.cpu),
      memory:      this._n(data.memory),
      memoryUsed:  this._n(data.memoryUsed),
      memoryTotal: this._n(data.memoryTotal),
      queueDepth:  this._n(data.queueDepth),
      concurrency: this._n(data.concurrency),
      disk: data.disk || null,
      selfHosted: data.selfHosted || false,
    };

    // 2. 存入 StateStore
    if (this.stateStore) {
      this.stateStore.addResourceSnapshot(agentId, snapshot);
    }

    // 3. 检查阈值
    const alerts = this._checkThresholds(snapshot);

    // 4. 趋势分析
    const trend = this._analyzeTrend(agentId, snapshot);

    // 5. 发送告警
    for (const alert of alerts) {
      await this._sendAlert(alert);
    }

    // 6. 趋势异常（连续上升且接近阈值）
    if (trend.rising && trend.nearThreshold) {
      await this._sendAlert({
        agentId, agentName,
        type: 'trend_warning',
        metric: trend.metric,
        message: `${_metricLabel(trend.metric)}持续上升：${trend.values.join(' → ')}%，接近告警阈值`,
        severity: 'warning',
        value: trend.current,
        threshold: this.config.thresholds[trend.metric],
      });
    }

    // 7. 更新统计
    this.stats.totalSnapshots++;
    this.stats.lastSnapshot = Date.now();

    return { snapshot, alerts, trend };
  }

  /**
   * 查询资源历史
   * @param {string} agentId
   * @param {number} limit — 最多返回条数
   */
  getHistory(agentId, limit = 60) {
    if (!this.stateStore) return [];
    return this.stateStore.getResourceHistory(agentId, limit);
  }

  /**
   * 获取最新资源快照
   * @param {string} agentId
   */
  getLatest(agentId) {
    if (!this.stateStore) return null;
    return this.stateStore.getLatestResources(agentId);
  }

  /**
   * 获取全局资源统计
   */
  getStats() {
    if (!this.stateStore) {
      return { totalSnapshots: this.stats.totalSnapshots, byAgent: {} };
    }

    const agentStats = this.stateStore.getResourceStats();
    return {
      ...agentStats,
      totalSnapshots: this.stats.totalSnapshots,
      totalAlerts: this.stats.totalAlerts,
      lastSnapshot: this.stats.lastSnapshot,
    };
  }

  // ─── 阈值检查 ──────────────────────────────────────────────

  _checkThresholds(snap) {
    const alerts = [];
    const t = this.config.thresholds;
    const { agentId, agentName } = snap;

    // CPU
    if (snap.cpu !== null && snap.cpu > t.cpu) {
      alerts.push({
        agentId, agentName,
        type: 'threshold',
        metric: 'cpu',
        message: `CPU 使用率过高：${snap.cpu.toFixed(1)}%（阈值 ${t.cpu}%）`,
        severity: snap.cpu > 95 ? 'critical' : 'warning',
        value: snap.cpu,
        threshold: t.cpu,
      });
    }

    // 内存
    if (snap.memory !== null && snap.memory > t.memory) {
      alerts.push({
        agentId, agentName,
        type: 'threshold',
        metric: 'memory',
        message: `内存使用率过高：${snap.memory.toFixed(1)}%（阈值 ${t.memory}%）`,
        severity: snap.memory > 98 ? 'critical' : 'warning',
        value: snap.memory,
        threshold: t.memory,
      });
    }

    // 队列深度
    if (snap.queueDepth !== null && snap.queueDepth > t.queueDepth) {
      alerts.push({
        agentId, agentName,
        type: 'threshold',
        metric: 'queue',
        message: `任务队列堆积：${snap.queueDepth} 个（阈值 ${t.queueDepth}）`,
        severity: snap.queueDepth > t.queueDepth * 2 ? 'critical' : 'warning',
        value: snap.queueDepth,
        threshold: t.queueDepth,
      });
    }

    // 磁盘（仅自托管）
    if (snap.disk && snap.disk.usedPercent > t.disk) {
      alerts.push({
        agentId, agentName,
        type: 'threshold',
        metric: 'disk',
        message: `磁盘空间不足：已用 ${snap.disk.usedPercent}%，剩余 ${snap.disk.available}`,
        severity: snap.disk.usedPercent > 95 ? 'critical' : 'warning',
        value: snap.disk.usedPercent,
        threshold: t.disk,
      });
    }

    return alerts;
  }

  // ─── 趋势分析 ──────────────────────────────────────────────

  _analyzeTrend(agentId, latest) {
    if (!this.stateStore) return { rising: false };

    const metrics = ['cpu', 'memory', 'queueDepth'];
    const trends = {};

    const t = this.config.thresholds;

    for (const metric of metrics) {
      const history = this.stateStore.getResourceHistory(agentId, this.config.trendWindow);
      // 只取有该指标的记录
      const values = history.map(h => h[metric]).filter(v => v !== null && v !== undefined);

      if (values.length < 3) {
        trends[metric] = { rising: false };
        continue;
      }

      // 简单线性趋势：最近 N 个点的方向
      const recent = values.slice(-5); // 最近 5 个
      const isRising = recent.length >= 3 &&
        recent[recent.length - 1] > recent[0] &&
        recent[recent.length - 1] > recent[Math.floor(recent.length / 2)];

      const current = latest[metric] || recent[recent.length - 1] || 0;
      const threshold = t[metric] || 80;
      const nearThreshold = isRising && current > threshold * 0.8;

      trends[metric] = {
        rising: isRising,
        nearThreshold,
        current,
        values: recent.map(v => Math.round(v)),
        threshold,
      };
    }

    // 返回最值得关注的趋势
    for (const [metric, t] of Object.entries(trends)) {
      if (t.rising && t.nearThreshold) {
        return { ...t, metric };
      }
    }

    return { rising: false, metric: null };
  }

  // ─── 告警发送 ──────────────────────────────────────────────

  async _sendAlert(alert) {
    const { agentId, metric, severity } = alert;

    // 冷却检查
    const throttleKey = `${agentId}:${metric}`;
    const lastTime = this._alertThrottle.get(throttleKey);
    if (lastTime && Date.now() - lastTime < this.config.alertCooldown) {
      return; // 冷却中
    }
    this._alertThrottle.set(throttleKey, Date.now());
    this.stats.totalAlerts++;

    // 通过 NotifyEngine 发送企微卡片
    if (this.notifyEngine) {
      const card = this.notifyEngine.resourceAlertCard(alert);
      if (card) {
        try {
          await this.notifyEngine._send(card);
        } catch (err) {
          console.error(`[ResourceCollector] Alert send failed: ${err.message}`);
        }
      }
    }
  }

  // ─── 关闭 ─────────────────────────────────────────────────

  async shutdown() {
    // 清理告警冷却记录
    this._alertThrottle.clear();
    console.log('[ResourceCollector] Shutdown');
  }

  // ─── 内部工具 ──────────────────────────────────────────────

  _n(v) {
    return (v !== undefined && v !== null) ? v : null;
  }
}

// ─── 工具函数 ────────────────────────────────────────────────

function _metricLabel(metric) {
  const map = {
    cpu: 'CPU',
    memory: '内存',
    queueDepth: '任务队列',
    disk: '磁盘',
  };
  return map[metric] || metric;
}

module.exports = { ResourceCollector };

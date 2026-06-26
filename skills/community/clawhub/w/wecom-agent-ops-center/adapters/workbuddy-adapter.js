#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — WorkBuddy 适配器
 * 架构位置：L0 数据源适配层
 *
 * 专为 WorkBuddy 桌面应用设计
 * 监控维度：
 *   - 健康检查：WorkBuddy 本地 API 端点
 *   - 任务追踪：WorkBuddy 任务事件 HTTP 回调
 *   - 资源采集：CPU/内存/队列（通过 WorkBuddy API）
 *
 * ClawHub 分发：作为 Skill 安装，用户 2 分钟接入
 */

const { BaseAdapter } = require('./base-adapter');

const DEFAULTS = {
  healthPath: '/health',
  healthInterval: 30_000,
  healthTimeout: 10_000,
  resourceInterval: 60_000,   // 资源采集间隔
};

class WorkBuddyAdapter extends BaseAdapter {
  constructor(config) {
    super(config);
    this.options = { ...DEFAULTS, ...(config.options || {}) };
    this.apiKey  = config.apiKey || config.agent?.apiKey || '';
    this.healthUrl = config.healthUrl || `${this.endpoint}/health`;

    // WorkBuddy 特有信息
    this.version = config.agent?.version || 'unknown';
  }

  // ─── 健康检查 ──────────────────────────────────────────────

  setupHealthCheck() {
    const interval = this.options.healthInterval;
    console.log(`[WorkBuddyAdapter:${this.id}] Health check every ${interval / 1000}s → ${this.healthUrl}`);

    this._addInterval(async () => {
      const result = await this._httpHealthCheck(this.healthUrl, this.options.healthTimeout);
      this.emit('health', {
        agentId: this.agentId,
        agentName: this.agentName,
        adapterType: this.type,
        healthy: result.healthy,
        latency: result.latency,
        status: result.status,
        statusCode: result.statusCode,
        error: result.error,
        version: this.version,
      });
    }, interval);
  }

  // ─── 资源采集 ──────────────────────────────────────────────

  setupResourceCollector() {
    const interval = this.options.resourceInterval;
    if (!this.endpoint) {
      console.log(`[WorkBuddyAdapter:${this.id}] No endpoint configured, skipping resource collection`);
      return;
    }

    console.log(`[WorkBuddyAdapter:${this.id}] Resource collection every ${interval / 1000}s`);

    this._addInterval(async () => {
      try {
        const res = await this._fetchResourceMetrics();
        if (res) {
          this.emit('resource', {
            agentId: this.agentId,
            agentName: this.agentName,
            adapterType: this.type,
            timestamp: Date.now(),
            ...res,
          });
        }
      } catch (err) {
        // 静默失败 — 资源采集不是关键路径
        console.debug(`[WorkBuddyAdapter:${this.id}] Resource fetch failed: ${err.message}`);
      }
    }, interval);
  }

  // ─── 任务监听 ──────────────────────────────────────────────

  /**
   * WorkBuddy 的任务事件通过 HTTP POST 推送到 TaskTracker API
   * 不需要适配器主动监听 — TaskTracker 提供通用 API
   * 此方法保留用于未来 WorkBuddy 主动回调场景
   */
  setupTaskListener() {
    // WorkBuddy 的任务事件由 TaskTracker 的 HTTP API 接收
    // 适配器不需要额外监听
    console.log(`[WorkBuddyAdapter:${this.id}] Task events handled by TaskTracker API`);
  }

  // ─── Agent 信息查询 ────────────────────────────────────────

  async queryAgentInfo() {
    const base = await super.queryAgentInfo();
    return {
      ...base,
      version: this.version,
      platform: 'workbuddy-desktop',
      features: ['health_check', 'task_tracking', 'resource_monitoring'],
    };
  }

  // ─── 内部方法 ──────────────────────────────────────────────

  /**
   * 从 WorkBuddy 本地 API 获取资源指标
   */
  async _fetchResourceMetrics() {
    const headers = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    // 尝试多个可能的资源端点
    const endpoints = [
      `${this.endpoint}/api/resources`,
      `${this.endpoint}/api/stats`,
      `${this.endpoint}/status`,
    ];

    for (const url of endpoints) {
      try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(url, {
          method: 'GET',
          headers,
          signal: controller.signal,
        });
        clearTimeout(timer);

        if (response.ok) {
          const data = await response.json();
          return {
            cpu: data.cpu || data.cpuPercent || null,
            memory: data.memory || data.memPercent || null,
            memoryUsed: data.memoryUsed || data.memUsed || null,
            memoryTotal: data.memoryTotal || data.memTotal || null,
            queueDepth: data.queueDepth || data.queue || null,
            concurrency: data.concurrency || data.concurrent || null,
            uptime: data.uptime || null,
            raw: data,
          };
        }
      } catch (err) {
        // 尝试下一个端点
        continue;
      }
    }

    return null;
  }
}

module.exports = { WorkBuddyAdapter };

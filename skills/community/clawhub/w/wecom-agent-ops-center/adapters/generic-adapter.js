#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 通用 HTTP 适配器
 * 架构位置：L0 数据源适配层
 *
 * 最简适配器：只做 HTTP 健康检查
 * 适用于任何暴露 HTTP 端点的 Agent（不限定类型）
 */

const { BaseAdapter } = require('./base-adapter');

const DEFAULTS = {
  healthPath: '/health',
  healthInterval: 30_000,   // 健康检查间隔
  healthTimeout: 10_000,    // HTTP 超时
};

class GenericAdapter extends BaseAdapter {
  constructor(config) {
    super(config);
    this.options = { ...DEFAULTS, ...(config.options || {}) };
    this.healthUrl = config.healthUrl || `${this.endpoint}${this.options.healthPath}`;
  }

  // ─── 健康检查 ──────────────────────────────────────────────

  setupHealthCheck() {
    const interval = this.options.healthInterval;
    console.log(`[GenericAdapter:${this.id}] Health check every ${interval / 1000}s → ${this.healthUrl}`);

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
      });
    }, interval);
  }

  // ─── Generic 适配器不做任务/资源 ──────────────────────────
}

module.exports = { GenericAdapter };

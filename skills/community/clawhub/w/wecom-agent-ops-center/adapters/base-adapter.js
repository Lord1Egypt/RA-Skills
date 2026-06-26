#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 适配器基类
 * 架构位置：L0 数据源适配层
 *
 * 所有适配器继承此基类，实现以下生命周期：
 *   register(config)     → 注册 Agent 到监控中心
 *   start()              → 启动健康检查 / 资源采集 / 任务监听
 *   stop()               → 优雅关闭
 *
 * 事件（通过 EventEmitter）：
 *   'health'   → { agentId, healthy, latency, status }
 *   'task'     → { agentId, event: 'start'|'progress'|'complete'|'fail', data }
 *   'resource' → { agentId, cpu, memory, queueDepth }
 *   'error'    → { agentId, error, context }
 */

const EventEmitter = require('events');

class BaseAdapter extends EventEmitter {
  /**
   * @param {object} config — 适配器配置
   * @param {string} config.id — 适配器唯一标识
   * @param {string} config.type — 适配器类型
   * @param {object} config.agent — Agent 信息 { id, name, endpoint }
   */
  constructor(config) {
    super();
    this.id         = config.id;
    this.type       = config.type;
    this.agentInfo  = config.agent || {};
    this.agentId    = this.agentInfo.id || this.id;
    this.agentName  = this.agentInfo.name || `Agent-${this.id}`;
    this.endpoint   = this.agentInfo.endpoint || '';
    this.status     = 'stopped';  // stopped | starting | running | degraded | stopped
    this._intervals = [];
  }

  // ─── 生命周期（子类必须实现）───────────────────────────────

  /**
   * 注册 Agent 到监控中心
   * 子类可覆写，进行额外初始化（如 API 密钥验证）
   */
  async register() {
    this.status = 'registered';
    this.emit('agent_registered', {
      agentId: this.agentId,
      agentName: this.agentName,
      adapterType: this.type,
      endpoint: this.endpoint,
    });
    return {
      agentId: this.agentId,
      agentName: this.agentName,
      adapterType: this.type,
    };
  }

  /**
   * 设置健康检查（子类实现）
   * 必须周期性 emit('health', {...})
   */
  setupHealthCheck() {
    // 子类实现：HTTP GET / TCP ping / ADP API / Claw API
    throw new Error('setupHealthCheck() must be implemented by subclass');
  }

  /**
   * 设置任务事件监听（子类实现，可选）
   * 如果 Agent 支持推送任务事件，在此设置 HTTP 路由或 WebSocket 监听
   */
  setupTaskListener() {
    // 可选实现 — generic-adapter 不需要，workbuddy/openclaw 需要
  }

  /**
   * 设置资源采集（子类实现，可选）
   * 周期性采集 CPU/内存/队列等指标
   */
  setupResourceCollector() {
    // 可选实现
  }

  /**
   * 查询 Agent 信息（子类实现，可选）
   * 返回 Agent 的版本、配置等静态信息
   */
  async queryAgentInfo() {
    return {
      agentId: this.agentId,
      agentName: this.agentName,
      adapterType: this.type,
      endpoint: this.endpoint,
    };
  }

  // ─── 启动 / 停止 ──────────────────────────────────────────

  /**
   * 启动适配器
   */
  async start() {
    if (this.status === 'running') {
      console.log(`[BaseAdapter:${this.id}] Already running`);
      return;
    }

    this.status = 'starting';
    console.log(`[BaseAdapter:${this.id}] Starting ${this.type} adapter for ${this.agentName}`);

    await this.register();

    // 启动各采集模块（子类实现）
    this.setupHealthCheck();
    this.setupTaskListener();
    this.setupResourceCollector();

    this.status = 'running';
    console.log(`[BaseAdapter:${this.id}] Started`);
  }

  /**
   * 停止适配器
   */
  async stop() {
    this.status = 'stopping';

    // 清理所有定时器
    for (const timer of this._intervals) {
      clearInterval(timer);
    }
    this._intervals = [];

    // 清理事件监听器
    this.removeAllListeners();

    this.status = 'stopped';
    console.log(`[BaseAdapter:${this.id}] Stopped`);
  }

  // ─── 工具方法 ─────────────────────────────────────────────

  /**
   * 安全的 HTTP 健康检查
   */
  async _httpHealthCheck(url, timeout = 5000) {
    const start = Date.now();
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        method: 'GET',
        signal: controller.signal,
      });
      clearTimeout(timer);

      const latency = Date.now() - start;
      const healthy = response.ok;

      return { healthy, latency, status: healthy ? 'healthy' : 'degraded', statusCode: response.status };
    } catch (err) {
      const latency = Date.now() - start;
      return { healthy: false, latency, status: 'offline', error: err.message };
    }
  }

  /**
   * 添加可追踪的定时器
   */
  _addInterval(fn, ms) {
    const id = setInterval(fn, ms);
    this._intervals.push(id);
    return id;
  }

  /**
   * 获取适配器状态摘要
   */
  getStatus() {
    return {
      id: this.id,
      type: this.type,
      agentId: this.agentId,
      agentName: this.agentName,
      endpoint: this.endpoint,
      status: this.status,
    };
  }
}

module.exports = { BaseAdapter };

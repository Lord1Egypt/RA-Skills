#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — Agent 监控模块
 * 职责：Agent 注册、周期性健康检查、超时检测、状态事件发射
 *
 * 架构位置：L2 监控通知层
 */

const axios = require('axios');
const EventEmitter = require('events');

// ─── 默认配置 ───────────────────────────────────────────────
const DEFAULTS = {
  heartbeatInterval: 30_000,    // 心跳间隔（毫秒）
  healthTimeout: 5_000,         // 健康检查 HTTP 超时
  offlineThreshold: 3,          // 连续失败几次标记为 offline
  maxHistory: 100,              // 每个 Agent 最多保留多少条心跳记录
};

// ─── Agent 状态常量 ──────────────────────────────────────────
const STATUS = {
  UNKNOWN:   'unknown',    // 还未检查过
  HEALTHY:   'healthy',    // 健康检查通过
  DEGRADED:  'degraded',   // 偶尔失败但没到 offline 阈值
  OFFLINE:   'offline',    // 连续失败超过阈值
  REGISTERED: 'registered', // 已注册但未开始检查
};

// ─── 事件名 ─────────────────────────────────────────────────
const EVENTS = {
  AGENT_ONLINE:    'agent:online',      // Agent 从 offline 变为 healthy
  AGENT_OFFLINE:   'agent:offline',     // Agent 变为 offline
  AGENT_DEGRADED:  'agent:degraded',    // Agent 变为 degraded
  HEALTH_RESULT:   'agent:health',      // 每次健康检查结果
  HEARTBEAT:       'agent:heartbeat',   // 每次心跳
  STATE_CHANGE:    'agent:state_change', // 任意状态变化
};

/**
 * Agent 监控器
 *
 * 使用方式：
 *   const monitor = new AgentMonitor(stateStore, config);
 *   monitor.registerAgent('my-agent', { name: 'AI客服', endpoint: 'http://localhost:3001/health' });
 *   monitor.start();  // 开始周期心跳
 *
 * 事件监听：
 *   monitor.on('agent:offline', ({ agentId, prevStatus, failCount }) => { ... });
 *   monitor.on('agent:online',  ({ agentId, prevStatus }) => { ... });
 */
class AgentMonitor extends EventEmitter {
  constructor(stateStore, config) {
    super();
    this.stateStore = stateStore;
    this.config  = { ...DEFAULTS, ...(config || {}) };
    this.agents  = new Map();    // agentId → { id, name, endpoint, ... }
    this.timers  = new Map();    // agentId → setInterval handle
    this.running = false;
  }

  // ─── Agent 管理 ───────────────────────────────────────────

  /**
   * 注册一个 Agent
   * @param {string} id — 唯一标识
   * @param {object} opts — { name, endpoint, type, description, version, source, tenant_id }
   */
  registerAgent(id, opts = {}) {
    const agent = {
      id,
      name:        opts.name        || id,
      endpoint:    opts.endpoint    || null,
      host:        opts.host        || null,
      port:        opts.port        || null,
      type:        opts.type        || 'http',
      description: opts.description || '',
      version:     opts.version     || '',
      source:      opts.source      || 'manual',
      tenant_id:    opts.tenant_id   || 'default',
      platform:    opts.platform    || 'unknown',   // 新增：平台来源
      registeredAt: Date.now(),
    };
    this.agents.set(id, agent);

    // 初始化状态
    this.stateStore.setAgentState(id, {
      status: STATUS.REGISTERED,
      failStreak: 0,
      lastCheck: null,
      lastOnline: null,
      totalChecks: 0,
      totalFailures: 0,
      avgLatency: 0,
    });

    this._log(`Registered: ${agent.name} (${id})${opts.endpoint ? ' → ' + opts.endpoint : ''}`);
    return agent;
  }

  /**
   * 批量注册/更新 Agent（从 scanner 推送）
   * 已存在的 agent 只更新元数据，不重置状态
   * @param {Array} list — [{id, name, type, description?, version?, tenant_id?, platform?}]
   * @param {string} [tenantId] — 可选，批量指定租户（否则从每项读取）
   * @param {string} [platform] — 可选，批量指定平台（否则从每项读取）
   * @returns {{ created: number, updated: number, total: number }}
   */
  bulkRegister(list, tenantId = null, platform = null) {
    let created = 0, updated = 0;
    for (const item of list) {
      if (!item.id) continue;
      const existing = this.agents.get(item.id);
      const tid = item.tenant_id || tenantId || 'default';
      const plt = item.platform || platform || 'unknown';
      if (existing) {
        // 更新元数据（不重置状态）
        Object.assign(existing, {
          name:        item.name        || existing.name,
          type:        item.type        || existing.type,
          description: item.description || existing.description,
          version:     item.version     || existing.version,
          source:      item.source      || existing.source || 'scanner',
          tenant_id:    tid,
          platform:     plt,  // 更新平台
        });
        this.agents.set(item.id, existing);
        updated++;
      } else {
        this.registerAgent(item.id, { ...item, tenant_id: tid, platform: plt });
        created++;
      }
    }
    this._log(`Bulk register: ${created} created, ${updated} updated, ${list.length} total (tenant=${tenantId || 'mixed'}, platform=${platform || 'mixed'})`);
    return { created, updated, total: list.length };
  }

  /**
   * 批量心跳上报（Push 模式）
   * Scanner 守护进程每 30 秒推一次所有 agent 状态
   * @param {Array} beats — [{id, status, message?, latency?}]
   * @param {string} [tenantId] — 可选，指定租户（否则从 agent 元数据读取）
   * @param {string} [platform] — 可选，指定平台来源
   * @returns {{ accepted: number, rejected: number }}
   */
  bulkHeartbeat(beats, tenantId = null, platform = null) {
    let accepted = 0, rejected = 0;
    const now = Date.now();

    for (const beat of beats) {
      if (!beat.id) { rejected++; continue; }

      // 确保 agent 已注册
      if (!this.agents.has(beat.id)) {
        this.registerAgent(beat.id, {
          name: beat.id,
          type: 'scanner',
          source: 'heartbeat_auto',
          tenant_id: tenantId || 'default',
          platform: platform || 'unknown',
        });
      } else if (platform) {
        // 已存在：更新 platform（如果提供了新的且原值是 unknown）
        const existing = this.agents.get(beat.id);
        if (!existing.platform || existing.platform === 'unknown') {
          existing.platform = platform;
          this.agents.set(beat.id, existing);
        }
      }

      const prevState = this.stateStore.getAgentState(beat.id);
      const prevStatus = prevState ? prevState.status : STATUS.UNKNOWN;

      // 映射状态
      const heartbeatStatus = beat.status || 'healthy';
      const newStatus = (heartbeatStatus === 'healthy') ? STATUS.HEALTHY
        : (heartbeatStatus === 'degraded') ? STATUS.DEGRADED
        : (heartbeatStatus === 'offline') ? STATUS.OFFLINE
        : STATUS.UNKNOWN;

      const failStreak = (newStatus === STATUS.HEALTHY) ? 0
        : (prevState ? prevState.failStreak + 1 : 1);

      const totalChecks = (prevState ? prevState.totalChecks : 0) + 1;
      const totalFailures = (prevState ? prevState.totalFailures : 0) + (newStatus === STATUS.HEALTHY ? 0 : 1);

      this.stateStore.setAgentState(beat.id, {
        status: newStatus,
        failStreak,
        lastCheck: now,
        lastOnline: newStatus === STATUS.HEALTHY ? now : (prevState ? prevState.lastOnline : null),
        totalChecks,
        totalFailures,
        avgLatency: this._rollingAvg(
          prevState ? prevState.avgLatency : 0,
          beat.latency || 0,
          totalChecks
        ),
      });

      this.stateStore.addHistory(beat.id, {
        ts: now,
        healthy: newStatus === STATUS.HEALTHY,
        latency: beat.latency || 0,
        status: newStatus,
        message: beat.message || '',
      });

      // 状态变化事件
      if (newStatus !== prevStatus) {
        const agent = this.agents.get(beat.id);
        this.emit(EVENTS.STATE_CHANGE, {
          agentId: beat.id, agent,
          from: prevStatus, to: newStatus,
          failStreak, detail: beat.message || null,
        });
        if (newStatus === STATUS.OFFLINE) {
          this.emit(EVENTS.AGENT_OFFLINE, { agentId: beat.id, agent, prevStatus, failCount: failStreak, error: beat.message });
        } else if (newStatus === STATUS.HEALTHY && prevStatus !== STATUS.HEALTHY) {
          this.emit(EVENTS.AGENT_ONLINE, { agentId: beat.id, agent, prevStatus });
        }
      }

      accepted++;
    }

    return { accepted, rejected };
  }

  /**
   * 注销一个 Agent（需验证租户权限）
   * @param {string} id
   * @param {string} [tenantId] — 可选，验证权限
   */
  unregisterAgent(id, tenantId = null) {
    const agent = this.agents.get(id);
    if (!agent) return;
    // 租户权限检查
    if (tenantId && agent.tenant_id && agent.tenant_id !== tenantId) {
      this._log(`Unregister denied: ${id} belongs to ${agent.tenant_id}, not ${tenantId}`);
      return;
    }
    this.stopAgent(id);
    this.agents.delete(id);
    this.stateStore.removeAgent(id);
    this._log(`Unregistered: ${id}`);
  }

  /**
   * 从配置批量注册
   */
  registerFromConfig(agentList) {
    if (!Array.isArray(agentList)) return;
    for (const cfg of agentList) {
      this.registerAgent(cfg.id, cfg);
    }
    this._log(`Bulk registered ${agentList.length} agents`);
  }

  // ─── 心跳生命周期 ─────────────────────────────────────────

  /**
   * 启动所有 Agent 的周期心跳
   */
  start() {
    if (this.running) return;
    this.running = true;

    for (const [id] of this.agents) {
      this._startHeartbeat(id);
    }

    this._log(`Monitor started — watching ${this.agents.size} agents (interval: ${this.config.heartbeatInterval}ms)`);
  }

  /**
   * 停止所有心跳
   */
  stop() {
    this.running = false;
    for (const [id] of this.timers) {
      this.stopAgent(id);
    }
    this._log('Monitor stopped');
  }

  /**
   * 停止单个 Agent 心跳
   */
  stopAgent(id) {
    const timer = this.timers.get(id);
    if (timer) {
      clearInterval(timer);
      this.timers.delete(id);
    }
  }

  /**
   * 处理适配器推送的健康事件（v2.1）
   * 适配器已完成健康检查，监控中心只需处理状态变更
   * @param {object} data — { agentId, agentName, adapterType, healthy, latency, status, statusCode, error }
   */
  _handleHealthEvent(data) {
    const { agentId, agentName, adapterType, healthy, latency, status: healthStatus, error } = data;

    // 确保 Agent 已注册
    if (!this.agents.has(agentId)) {
      this.registerAgent(agentId, {
        id: agentId,
        name: agentName || agentId,
        type: adapterType || 'unknown',
      });
    }

    const prevState = this.stateStore.getAgentState(agentId);
    const prevStatus = prevState ? prevState.status : STATUS.UNKNOWN;

    const newFailStreak = healthy ? 0 : (prevState ? prevState.failStreak + 1 : 1);
    const newStatus = this._deriveStatus(newFailStreak);

    const now = Date.now();
    const totalChecks = (prevState ? prevState.totalChecks : 0) + 1;
    const totalFailures = (prevState ? prevState.totalFailures : 0) + (healthy ? 0 : 1);

    const statePatch = {
      status: newStatus,
      failStreak: newFailStreak,
      lastCheck: now,
      lastOnline: healthy ? now : (prevState ? prevState.lastOnline : null),
      totalChecks,
      totalFailures,
      avgLatency: this._rollingAvg(prevState ? prevState.avgLatency : 0, latency || 0, totalChecks),
    };

    this.stateStore.setAgentState(agentId, statePatch);
    this.stateStore.addHistory(agentId, {
      healthy,
      latency: latency || 0,
      status: newStatus,
    });

    // 发送事件
    if (prevStatus !== newStatus) {
      if (newStatus === STATUS.HEALTHY) {
        this.emit(EVENTS.AGENT_ONLINE, {
          agentId,
          agent: this.agents.get(agentId),
          prevStatus,
          from: prevStatus,
          to: newStatus,
        });
      } else if (newStatus === STATUS.OFFLINE) {
        this.emit(EVENTS.AGENT_OFFLINE, {
          agentId,
          agent: this.agents.get(agentId),
          prevStatus,
          failCount: newFailStreak,
          error,
        });
      } else if (newStatus === STATUS.DEGRADED) {
        this.emit(EVENTS.AGENT_DEGRADED, {
          agentId,
          agent: this.agents.get(agentId),
          prevStatus,
          failCount: newFailStreak,
          error,
        });
      }
    }

    this.emit(EVENTS.HEALTH_RESULT, {
      agentId,
      healthy,
      latency: latency || 0,
      status: newStatus,
    });
  }

  _startHeartbeat(id) {
    // 先停掉旧的
    this.stopAgent(id);

    // 立即执行一次
    this._checkHealth(id);

    // 周期执行
    const timer = setInterval(() => {
      if (!this.running) {
        clearInterval(timer);
        return;
      }
      this._checkHealth(id);
    }, this.config.heartbeatInterval);

    this.timers.set(id, timer);
  }

  // ─── 健康检查 ─────────────────────────────────────────────

  async _checkHealth(id) {
    const agent = this.agents.get(id);
    if (!agent) return;

    const start = Date.now();
    let result;

    try {
      result = await this._doHealthCheck(agent);
    } catch (err) {
      result = {
        healthy: false,
        latency: Date.now() - start,
        error: err.code || err.message,
      };
    }

    const latency = result.latency || (Date.now() - start);

    // 更新状态
    const prevState = this.stateStore.getAgentState(id);
    const prevStatus = prevState ? prevState.status : STATUS.UNKNOWN;

    const newFailStreak = result.healthy ? 0 : (prevState ? prevState.failStreak + 1 : 1);
    const newStatus = this._deriveStatus(newFailStreak);

    const now = Date.now();
    const totalChecks = (prevState ? prevState.totalChecks : 0) + 1;
    const totalFailures = (prevState ? prevState.totalFailures : 0) + (result.healthy ? 0 : 1);

    const statePatch = {
      status: newStatus,
      failStreak: newFailStreak,
      lastCheck: now,
      lastOnline: result.healthy ? now : (prevState ? prevState.lastOnline : null),
      totalChecks,
      totalFailures,
      avgLatency: this._rollingAvg(prevState ? prevState.avgLatency : 0, latency, totalChecks),
    };

    this.stateStore.setAgentState(id, statePatch);

    // 记录历史
    this.stateStore.addHistory(id, {
      ts: now,
      healthy: result.healthy,
      latency,
      status: newStatus,
    });

    // 发射事件
    this.emit(EVENTS.HEALTH_RESULT, { agentId: id, agent, result, latency, status: newStatus });
    this.emit(EVENTS.HEARTBEAT, { agentId: id, agent, healthy: result.healthy, latency, timestamp: now });

    // 状态变化事件
    if (newStatus !== prevStatus) {
      this.emit(EVENTS.STATE_CHANGE, {
        agentId: id, agent,
        from: prevStatus,
        to: newStatus,
        failStreak: newFailStreak,
        detail: result.error || null,
      });

      if (newStatus === STATUS.OFFLINE) {
        this.emit(EVENTS.AGENT_OFFLINE, { agentId: id, agent, prevStatus, failCount: newFailStreak, error: result.error });
      } else if (newStatus === STATUS.DEGRADED) {
        this.emit(EVENTS.AGENT_DEGRADED, { agentId: id, agent, prevStatus, failStreak: newFailStreak });
      } else if (newStatus === STATUS.HEALTHY && prevStatus !== STATUS.HEALTHY) {
        this.emit(EVENTS.AGENT_ONLINE, { agentId: id, agent, prevStatus });
      }
    }
  }

  /**
   * 执行一次健康检查
   * 支持 HTTP 和 TCP 两种方式
   */
  async _doHealthCheck(agent) {
    const timeout = this.config.healthTimeout;

    if (agent.type === 'tcp' || (!agent.endpoint && agent.host)) {
      // TCP ping
      return this._tcpPing(agent, timeout);
    }

    if (agent.endpoint) {
      // HTTP GET
      const res = await axios.get(agent.endpoint, { timeout, validateStatus: () => true });
      return {
        healthy: res.status >= 200 && res.status < 500,
        latency: res.headers['x-response-time'] ? parseInt(res.headers['x-response-time']) : undefined,
        statusCode: res.status,
      };
    }

    return { healthy: false, error: 'No endpoint configured' };
  }

  async _tcpPing(agent, timeout) {
    const net = require('net');
    return new Promise((resolve) => {
      const start = Date.now();
      const socket = new net.Socket();
      socket.setTimeout(timeout);

      socket.on('connect', () => {
        const latency = Date.now() - start;
        socket.destroy();
        resolve({ healthy: true, latency });
      });

      socket.on('timeout', () => {
        socket.destroy();
        resolve({ healthy: false, latency: Date.now() - start, error: 'timeout' });
      });

      socket.on('error', (err) => {
        socket.destroy();
        resolve({ healthy: false, latency: Date.now() - start, error: err.code || 'connection_refused' });
      });

      socket.connect(agent.port || 80, agent.host);
    });
  }

  // ─── 状态推导 ─────────────────────────────────────────────

  _deriveStatus(failStreak) {
    if (failStreak === 0) return STATUS.HEALTHY;
    if (failStreak < this.config.offlineThreshold) return STATUS.DEGRADED;
    return STATUS.OFFLINE;
  }

  _rollingAvg(prev, next, n) {
    // Welford 近似
    return prev + (next - prev) / Math.max(n, 1);
  }

  // ─── 查询接口 ─────────────────────────────────────────────

  /**
   * 获取所有 Agent 的当前状态快照
   * @param {string} [tenantId] — 可选，只返回该租户的 agent
   */
  getSnapshot(tenantId = null) {
    const agents = [];
    for (const [id, agent] of this.agents) {
      // 按 tenant_id 过滤
      if (tenantId && agent.tenant_id !== tenantId) continue;

      const state = this.stateStore.getAgentState(id);
      agents.push({
        id,
        name: agent.name,
        type: agent.type,
        endpoint: agent.endpoint,
        tenant_id: agent.tenant_id || 'default',
        ...(state || {}),
        platform:  agent.platform  || 'unknown',  // 平台来源（放 state 之后防止覆盖）
      });
    }
    return {
      timestamp: Date.now(),
      tenant_id: tenantId || 'all',
      total: agents.length,
      healthy:  agents.filter(a => a.status === STATUS.HEALTHY).length,
      degraded: agents.filter(a => a.status === STATUS.DEGRADED).length,
      offline:  agents.filter(a => a.status === STATUS.OFFLINE).length,
      agents,
    };
  }

  /**
   * 获取单个 Agent 详情
   * @param {string} id
   * @param {string} [tenantId] — 可选，验证租户权限
   */
  getAgentDetail(id, tenantId = null) {
    const agent = this.agents.get(id);
    if (!agent) return null;
    // 租户隔离检查
    if (tenantId && agent.tenant_id && agent.tenant_id !== tenantId) {
      return null; // 无权访问
    }
    const state = this.stateStore.getAgentState(id);
    const history = this.stateStore.getAgentHistory(id);
    return { agent, state, history };
  }

  // ─── 工具 ─────────────────────────────────────────────────

  _log(msg) {
    console.log(`[AgentMonitor] ${msg}`);
  }
}

module.exports = { AgentMonitor, STATUS, EVENTS };

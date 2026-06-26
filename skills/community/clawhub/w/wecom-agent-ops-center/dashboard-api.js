#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 仪表板 API
 * 职责：为监控仪表板 HTML 提供 RESTful JSON 数据端点
 *
 * 端点设计：
 *   GET /api/monitor/snapshot     — 所有 Agent 实时状态快照
 *   GET /api/monitor/:id           — 单个 Agent 详情 + 心跳历史
 *   GET /api/monitor/:id/history   — 心跳历史（可指定条数）
 *   GET /api/monitor/stats         — 全局统计
 *   GET /api/monitor/events        — 最近告警事件
 *
 *   GET /api/tasks/active          — 活跃任务列表 (v2.1)
 *   GET /api/tasks/:id             — 任务详情 (v2.1)
 *   GET /api/tasks/agent/:agentId  — Agent 任务列表 (v2.1)
 *   GET /api/tasks/stats           — 任务统计 (v2.1)
 *
 *   GET /api/resources/:agentId     — 资源历史 (v2.2)
 *   GET /api/resources/stats        — 全局资源统计 (v2.2)
 *
 *   GET /api/audit/search?...        — 多条件搜索 (v2.3)
 *   GET /api/audit/:taskId           — 任务审计轨迹 (v2.3)
 *   GET /api/audit/stats             — 审计统计 (v2.3)
 *
 * 架构位置：L2 核心监控引擎 → 仪表板 UI
 */

const url = require('url');

class DashboardAPI {
  constructor(monitor, stateStore, notifyEngine, taskTracker = null, resourceCollector = null, auditLogger = null, lifecycleMgr = null, secretsScanner = null, networkGuard = null) {
    this.monitor = monitor;
    this.stateStore = stateStore;
    this.notifyEngine = notifyEngine;
    this.taskTracker = taskTracker;       // v2.1
    this.resourceCollector = resourceCollector; // v2.2
    this.auditLogger = auditLogger;       // v2.3
    this.lifecycleMgr = lifecycleMgr;     // v2.4
    this.secretsScanner = secretsScanner; // v2.4
    this.networkGuard = networkGuard;     // v2.4

    // 最近事件缓冲（最新 100 条）
    this.events = [];
    this.maxEvents = 100;

    // 订阅监控事件
    this._subscribe();
  }

  _subscribe() {
    const ALL_EVENTS = [
      'agent:online',
      'agent:offline',
      'agent:degraded',
      'agent:state_change',
    ];

    for (const ev of ALL_EVENTS) {
      this.monitor.on(ev, (data) => {
        this._pushEvent(ev, data);
      });
    }
  }

  _pushEvent(type, data) {
    const event = {
      id: `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      type,
      timestamp: Date.now(),
      agentId: data.agentId,
      agentName: data.agent ? data.agent.name : data.agentId,
      detail: { ...data },
    };
    this.events.unshift(event);

    if (this.events.length > this.maxEvents) {
      this.events.length = this.maxEvents;
    }
  }

  // ─── 路由处理 ──────────────────────────────────────────────

  async handle(req, res) {
    const parsed = url.parse(req.url, true);
    const path = parsed.pathname;
    const method = req.method;

    // 提取 Tenant ID（从请求头，用于多租户隔离）
    const tenantId = (req.headers['x-tenant-id'] || req.headers['x-tenant_id'] || '').trim() || null;

    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Tenant-ID, X-Tenant-Id, X-Platform');

    if (method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    try {
      // GET /api/monitor/snapshot
      if (path === '/api/monitor/snapshot' && method === 'GET') {
        const snap = this.monitor.getSnapshot(tenantId);
        this._json(res, 200, snap);
        return;
      }

      // GET /api/monitor/stats
      if (path === '/api/monitor/stats' && method === 'GET') {
        const stats = this.stateStore.getGlobalStats(tenantId);
        const snap = this.monitor.getSnapshot(tenantId);
        this._json(res, 200, { ...stats, snapshot: snap });
        return;
      }

      // GET /api/monitor/events?limit=20
      if (path === '/api/monitor/events' && method === 'GET') {
        const limit = parseInt(parsed.query.limit) || 20;
        this._json(res, 200, this.events.slice(0, limit));
        return;
      }

      // GET /api/monitor/:id
      const detailMatch = path.match(/^\/api\/monitor\/([^/]+)$/);
      if (detailMatch && method === 'GET') {
        const agentId = detailMatch[1];
        const detail = this.monitor.getAgentDetail(agentId, tenantId);
        if (!detail) {
          this._json(res, 404, { error: `Agent '${agentId}' not found or access denied` });
          return;
        }
        this._json(res, 200, detail);
        return;
      }

      // GET /api/monitor/:id/history?limit=50
      const histMatch = path.match(/^\/api\/monitor\/([^/]+)\/history$/);
      if (histMatch && method === 'GET') {
        const agentId = histMatch[1];
        const state = this.stateStore.getAgentState(agentId);
        if (!state) {
          this._json(res, 404, { error: `Agent '${agentId}' not found` });
          return;
        }
        const limit = parseInt(parsed.query.limit) || 50;
        const history = this.stateStore.getAgentHistory(agentId, limit);
        this._json(res, 200, { agentId, history });
        return;
      }

      // ─── 任务 API（v2.1）────────────────────────────────

      // GET /api/tasks/active
      if (path === '/api/tasks/active' && method === 'GET') {
        const agentId = parsed.query.agentId || null;
        const tasks = this.stateStore.getActiveTasks(agentId);
        this._json(res, 200, { tasks, count: tasks.length });
        return;
      }

      // GET /api/tasks/stats
      if (path === '/api/tasks/stats' && method === 'GET') {
        const stats = this.stateStore.getTaskStats();
        this._json(res, 200, stats);
        return;
      }

      // GET /api/tasks/agent/:agentId
      const agentTasksMatch = path.match(/^\/api\/tasks\/agent\/([^/]+)$/);
      if (agentTasksMatch && method === 'GET') {
        const agentId = agentTasksMatch[1];
        const limit = parseInt(parsed.query.limit) || 50;
        const tasks = this.stateStore.getAgentTasks(agentId, limit);
        this._json(res, 200, { agentId, tasks, count: tasks.length });
        return;
      }

      // GET /api/tasks/:id
      const tasksMatch = path.match(/^\/api\/tasks\/([^/]+)$/);
      if (tasksMatch && method === 'GET') {
        const taskId = tasksMatch[1];
        const task = this.stateStore.getTask(taskId);
        if (!task) {
          this._json(res, 404, { error: `Task '${taskId}' not found` });
          return;
        }
        this._json(res, 200, task);
        return;
      }

      // ─── 资源 API（v2.2）────────────────────────────────

      // GET /api/resources/stats
      if (path === '/api/resources/stats' && method === 'GET') {
        const stats = this.resourceCollector
          ? this.resourceCollector.getStats()
          : this.stateStore.getResourceStats();
        this._json(res, 200, stats);
        return;
      }

      // GET /api/resources/:agentId?limit=60
      const resMatch = path.match(/^\/api\/resources\/([^/]+)$/);
      if (resMatch && method === 'GET') {
        const agentId = resMatch[1];
        const limit = parseInt(parsed.query.limit) || 60;
        const history = this.stateStore.getResourceHistory(agentId, limit);
        const latest = this.stateStore.getLatestResources(agentId);
        this._json(res, 200, { agentId, latest, history, count: history.length });
        return;
      }

      // ─── 审计 API（v2.3）────────────────────────────────

      // GET /api/audit/stats
      if (path === '/api/audit/stats' && method === 'GET') {
        const stats = this.auditLogger
          ? this.auditLogger.getStats()
          : this.stateStore.getAuditStats();
        this._json(res, 200, stats);
        return;
      }

      // GET /api/audit/search?agentId=...&taskId=...&type=...&keyword=...&startTime=...&endTime=...&limit=50&offset=0
      if (path === '/api/audit/search' && method === 'GET') {
        const query = {
          agentId: parsed.query.agentId,
          taskId: parsed.query.taskId,
          type: parsed.query.type,
          keyword: parsed.query.keyword,
          startTime: parsed.query.startTime ? parseInt(parsed.query.startTime) : undefined,
          endTime: parsed.query.endTime ? parseInt(parsed.query.endTime) : undefined,
          limit: parseInt(parsed.query.limit) || 50,
          offset: parseInt(parsed.query.offset) || 0,
        };
        const result = this.auditLogger
          ? this.auditLogger.search(query)
          : this.stateStore.searchAudit(query);
        this._json(res, 200, result);
        return;
      }

      // GET /api/audit/:taskId — 查某任务的审计轨迹
      const auditTaskMatch = path.match(/^\/api\/audit\/([^/]+)$/);
      if (auditTaskMatch && method === 'GET') {
        const taskId = auditTaskMatch[1];
        const entries = this.auditLogger
          ? this.auditLogger.getTaskAudit(taskId)
          : this.stateStore.getTaskAudit(taskId);
        const task = this.stateStore.getTask(taskId);

        // 如果请求参数 includeSummary=true，返回完整报告
        if (parsed.query.summary === 'true' && this.auditLogger) {
          const summary = this.auditLogger.generateSummary(taskId);
          this._json(res, 200, { taskId, entries, task: task || null, summary, count: entries.length });
          return;
        }

        this._json(res, 200, { taskId, entries, task: task || null, count: entries.length });
        return;
      }

      // ─── v2.4 生命周期管理 API ────────────────────────────

      // GET /api/lifecycle/processes
      if (path === '/api/lifecycle/processes' && method === 'GET') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        const list = this.lifecycleMgr.status(); // 无参 = 所有进程
        this._json(res, 200, { processes: list, count: list.length });
        return;
      }

      // GET /api/lifecycle/:id
      const lifecycleDetailMatch = path.match(/^\/api\/lifecycle\/([^/]+)$/);
      if (lifecycleDetailMatch && method === 'GET') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        const procId = lifecycleDetailMatch[1];
        try {
          const proc = this.lifecycleMgr.status(procId);
          this._json(res, 200, proc);
        } catch (e) {
          this._json(res, 404, { error: e.message });
        }
        return;
      }

      // POST /api/lifecycle/:id/start
      const lifecycleStartMatch = path.match(/^\/api\/lifecycle\/([^/]+)\/start$/);
      if (lifecycleStartMatch && method === 'POST') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        const procId = lifecycleStartMatch[1];
        try {
          const body = await this._readBody(req);
          const result = await this.lifecycleMgr.start(procId);
          this._json(res, result.ok ? 200 : 409, result);
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // POST /api/lifecycle/:id/stop
      const lifecycleStopMatch = path.match(/^\/api\/lifecycle\/([^/]+)\/stop$/);
      if (lifecycleStopMatch && method === 'POST') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        const procId = lifecycleStopMatch[1];
        try {
          const body = await this._readBody(req);
          let graceful = true;
          if (body) { try { graceful = JSON.parse(body).graceful !== false; } catch {} }
          const result = await this.lifecycleMgr.stop(procId, graceful);
          this._json(res, result.ok ? 200 : 409, result);
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // POST /api/lifecycle/:id/restart
      const lifecycleRestartMatch = path.match(/^\/api\/lifecycle\/([^/]+)\/restart$/);
      if (lifecycleRestartMatch && method === 'POST') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        const procId = lifecycleRestartMatch[1];
        try {
          const result = await this.lifecycleMgr.restart(procId);
          this._json(res, result.ok ? 200 : 409, result);
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // POST /api/lifecycle/ensure
      if (path === '/api/lifecycle/ensure' && method === 'POST') {
        if (!this.lifecycleMgr) { this._json(res, 501, { error: 'LifecycleManager not enabled' }); return; }
        try {
          const body = await this._readBody(req);
          let procId = null;
          if (body) { try { procId = JSON.parse(body).procId || null; } catch {} }
          const results = await this.lifecycleMgr.ensure(procId);
          this._json(res, 200, { ensured: true, results, count: results.length });
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // ─── v2.4 敏感信息扫描 API ────────────────────────────

      // GET /api/secrets/stats
      if (path === '/api/secrets/stats' && method === 'GET') {
        if (!this.secretsScanner) { this._json(res, 501, { error: 'SecretsScanner not enabled' }); return; }
        const stats = this.secretsScanner.getStats();
        this._json(res, 200, stats);
        return;
      }

      // GET /api/secrets/rules
      if (path === '/api/secrets/rules' && method === 'GET') {
        if (!this.secretsScanner) { this._json(res, 501, { error: 'SecretsScanner not enabled' }); return; }
        // 返回规则摘要（不含完整正则对象）
        const rules = this.secretsScanner.getRules ? this.secretsScanner.getRules() : [];
        this._json(res, 200, { rules, count: rules.length });
        return;
      }

      // POST /api/secrets/test
      if (path === '/api/secrets/test' && method === 'POST') {
        if (!this.secretsScanner) { this._json(res, 501, { error: 'SecretsScanner not enabled' }); return; }
        try {
          const body = await this._readBody(req);
          if (!body) { this._json(res, 400, { error: 'Request body required: { text: "..." }' }); return; }
          const { text, context } = JSON.parse(body);
          if (!text) { this._json(res, 400, { error: 'text field is required' }); return; }
          const result = this.secretsScanner.process(text, context || {});
          this._json(res, 200, result);
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // ─── v2.4 网络守卫 API ──────────────────────────────────

      // GET /api/network/status
      if (path === '/api/network/status' && method === 'GET') {
        if (!this.networkGuard) { this._json(res, 501, { error: 'NetworkGuard not enabled' }); return; }
        const status = this.networkGuard.getStats();
        const allowed = this.networkGuard.getAllowedList();
        this._json(res, 200, { ...status, allowed });
        return;
      }

      // POST /api/network/test
      if (path === '/api/network/test' && method === 'POST') {
        if (!this.networkGuard) { this._json(res, 501, { error: 'NetworkGuard not enabled' }); return; }
        try {
          const body = await this._readBody(req);
          if (!body) { this._json(res, 400, { error: 'Request body required: { url: "..." }' }); return; }
          const { url } = JSON.parse(body);
          if (!url) { this._json(res, 400, { error: 'url field is required' }); return; }
          const result = this.networkGuard.check(url);
          this._json(res, 200, result);
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // ─── v2.4 Agent 注册/心跳 API（Scanner Push 模式）─────

      // POST /api/agents/bulk-register — 一次性批量注册 agent
      if (path === '/api/agents/bulk-register' && method === 'POST') {
        try {
          const body = await this._readBody(req);
          if (!body) { this._json(res, 400, { error: 'Request body required: { agents: [...] }' }); return; }
          const parsed = JSON.parse(body);
          const { agents, tenant_id, platform } = parsed;
          if (!Array.isArray(agents) || agents.length === 0) {
            this._json(res, 400, { error: 'agents must be a non-empty array' });
            return;
          }
          // tenant_id：body > header > default
          const tid = tenant_id || tenantId || 'default';
          // platform：body > header > default
          const plt = platform || (req.headers['x-platform'] || '').trim() || 'unknown';
          const result = this.monitor.bulkRegister(agents, tid, plt);
          this._json(res, 200, { ok: true, tenant_id: tid, platform: plt, ...result });
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // POST /api/agents/heartbeat-bulk — 批量心跳上报
      if (path === '/api/agents/heartbeat-bulk' && method === 'POST') {
        try {
          const body = await this._readBody(req);
          if (!body) { this._json(res, 400, { error: 'Request body required: { heartbeats: [...] }' }); return; }
          const parsed = JSON.parse(body);
          const { heartbeats, tenant_id, platform } = parsed;
          if (!Array.isArray(heartbeats) || heartbeats.length === 0) {
            this._json(res, 400, { error: 'heartbeats must be a non-empty array' });
            return;
          }
          // tenant_id：body > header > default
          const tid = tenant_id || tenantId || 'default';
          // platform：body > header > default
          const plt = platform || (req.headers['x-platform'] || '').trim() || 'unknown';
          const result = this.monitor.bulkHeartbeat(heartbeats, tid, plt);
          this._json(res, 200, { ok: true, tenant_id: tid, platform: plt, ...result });
        } catch (err) {
          this._json(res, 500, { error: err.message });
        }
        return;
      }

      // 404
      this._json(res, 404, { error: `Not found: ${path}` });
    } catch (err) {
      this._json(res, 500, { error: err.message });
    }
  }

  _json(res, status, data) {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data, null, process.env.NODE_ENV === 'development' ? 2 : 0));
  }

  /**
   * 读取请求 body（Promise 封装）
   * @param {import('http').IncomingMessage} req
   * @returns {Promise<string>}
   */
  _readBody(req) {
    return new Promise((resolve, reject) => {
      let body = '';
      req.on('data', chunk => { body += chunk.toString(); });
      req.on('end', () => resolve(body));
      req.on('error', err => reject(err));
    });
  }
}

module.exports = { DashboardAPI };

#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 状态存储模块
 * 职责：Agent 运行状态的内存缓存 + JSON 持久化
 *
 * 架构位置：L2 监控通知层（AgentMonitor 的数据后端）
 *
 * 数据结构：
 *   agents: Map<agentId, { status, failStreak, lastCheck, ... }>
 *   history: Map<agentId, [{ ts, healthy, latency, status }, ...]>
 *   tasks:   Map<taskId, { taskId, agentId, type, name, status, nodes, ... }>
 *   resources: Map<agentId, [{ timestamp, cpu, memory, memoryUsed, memoryTotal, queueDepth, concurrency, disk }, ...]>
 *   audit:   Map<auditId, { auditId, taskId, agentId, type, summary, input, output, decisionPoints }>
 *
 * 持久化：
 *   每次状态更新后异步写入 JSON 文件
 *   启动时从 JSON 恢复
 *
 * TaskRecord 数据结构 (v2.1):
 *   {
 *     taskId: string,          // UUID
 *     agentId: string,         // 所属 Agent
 *     adapterType: string,     // agent 适配器类型
 *     type: string,            // 任务类型 (report_gen / data_analysis / ...)
 *     name: string,            // 任务名称
 *     status: 'pending' | 'running' | 'completed' | 'failed',
 *     startTime: number,       // 任务开始时间戳
 *     endTime: number|null,    // 任务结束时间戳
 *     duration: number|null,   // 总耗时 ms
 *     nodes: [{                // 执行节点
 *       name: string,          // 节点名
 *       status: 'done'|'running'|'pending'|'failed',
 *       timestamp: number,
 *     }],
 *     result: any,             // 任务输出
 *     error: string|null,      // 错误信息
 *     metadata: object,        // 扩展信息
 *   }
 */

const fs = require('fs');
const path = require('path');

const DEFAULTS = {
  maxHistory: 100,     // 每个 Agent 最多保留历史记录数
  persistPath: null,   // 持久化文件路径（null = 不持久化）
  persistInterval: 10_000, // 批量写入间隔（毫秒）
};

class StateStore {
  constructor(config) {
    this.config = { ...DEFAULTS, ...(config || {}) };
    this.agents  = new Map();  // agentId → state object
    this.history = new Map();  // agentId → array of history entries
    this.tasks     = new Map();  // taskId → TaskRecord (v2.1)
    this.resources = new Map();  // agentId → resource snapshots[] (v2.2)
    this.audit     = new Map();  // auditId → AuditEntry (v2.3)
    this._dirty    = false;
    this._persistTimer = null;

    // 从文件恢复
    if (this.config.persistPath) {
      this._load();
    }
  }

  // ─── Agent 状态读写 ────────────────────────────────────────

  /**
   * 设置 Agent 当前状态（部分更新）
   */
  setAgentState(agentId, patch) {
    const current = this.agents.get(agentId) || {
      status: 'unknown',
      failStreak: 0,
      lastCheck: null,
      lastOnline: null,
      totalChecks: 0,
      totalFailures: 0,
      avgLatency: 0,
    };

    const updated = { ...current, ...patch };
    this.agents.set(agentId, updated);
    this._dirty = true;

    return updated;
  }

  /**
   * 获取 Agent 当前状态
   */
  getAgentState(agentId) {
    return this.agents.get(agentId) || null;
  }

  /**
   * 删除 Agent 状态
   */
  removeAgent(agentId) {
    this.agents.delete(agentId);
    this.history.delete(agentId);
    // 清理该 Agent 的任务
    for (const [taskId, t] of this.tasks) {
      if (t.agentId === agentId) this.tasks.delete(taskId);
    }
    this._dirty = true;
  }

  /**
   * 获取所有 Agent 状态
   */
  getAllAgentStates() {
    const result = {};
    for (const [id, state] of this.agents) {
      result[id] = state;
    }
    return result;
  }

  // ─── 历史记录 ─────────────────────────────────────────────

  /**
   * 添加一条心跳历史记录
   */
  addHistory(agentId, entry) {
    let hist = this.history.get(agentId);
    if (!hist) {
      hist = [];
      this.history.set(agentId, hist);
    }

    const record = {
      ts: entry.ts || Date.now(),
      healthy: entry.healthy,
      latency: entry.latency,
      status: entry.status,
    };
    hist.push(record);

    // 裁剪
    if (hist.length > this.config.maxHistory) {
      hist.splice(0, hist.length - this.config.maxHistory);
    }
  }

  /**
   * 获取 Agent 心跳历史
   */
  getAgentHistory(agentId, limit = 20) {
    const hist = this.history.get(agentId);
    if (!hist) return [];
    return limit ? hist.slice(-limit) : [...hist];
  }

  /**
   * 获取全局统计（所有 Agent 聚合）
   */
  getGlobalStats() {
    let totalChecks = 0;
    let totalFailures = 0;
    let totalLatency = 0;
    let latencyCount = 0;

    for (const [id, state] of this.agents) {
      totalChecks += state.totalChecks || 0;
      totalFailures += state.totalFailures || 0;
      if (state.avgLatency > 0) {
        totalLatency += state.avgLatency;
        latencyCount++;
      }
    }

    return {
      totalChecks,
      totalFailures,
      avgLatency: latencyCount > 0 ? totalLatency / latencyCount : 0,
      agentCount: this.agents.size,
    };
  }

  // ─── 任务记录（v2.1）──────────────────────────────────────

  /**
   * 创建或更新任务记录
   */
  setTask(taskId, record) {
    const existing = this.tasks.get(taskId) || {};
    const merged = { ...existing, ...record, taskId };
    this.tasks.set(taskId, merged);
    this._dirty = true;
    return merged;
  }

  /**
   * 更新任务进度节点
   * @param {string} taskId
   * @param {string} nodeName - 节点名
   * @param {string} status - 'done'|'running'|'failed'
   */
  addTaskNode(taskId, nodeName, status) {
    const task = this.tasks.get(taskId);
    if (!task) return null;

    // 标记所有 running 节点为 done
    if (task.nodes) {
      for (const n of task.nodes) {
        if (n.status === 'running') n.status = 'done';
      }
    }

    const node = {
      name: nodeName,
      status,
      timestamp: Date.now(),
    };

    if (!task.nodes) task.nodes = [];
    task.nodes.push(node);
    this._dirty = true;
    return node;
  }

  /**
   * 完成任务
   */
  completeTask(taskId, result) {
    const task = this.tasks.get(taskId);
    if (!task) return null;

    task.status = 'completed';
    task.result = result;
    task.endTime = Date.now();
    task.duration = task.endTime - task.startTime;
    this._dirty = true;
    return task;
  }

  /**
   * 标记任务失败
   */
  failTask(taskId, error) {
    const task = this.tasks.get(taskId);
    if (!task) return null;

    task.status = 'failed';
    task.error = error;
    task.endTime = Date.now();
    task.duration = task.endTime - task.startTime;
    this._dirty = true;
    return task;
  }

  /**
   * 获取单个任务
   */
  getTask(taskId) {
    return this.tasks.get(taskId) || null;
  }

  /**
   * 获取某个 Agent 的所有任务（按时间倒序）
   */
  getAgentTasks(agentId, limit = 50) {
    const tasks = [];
    for (const [id, t] of this.tasks) {
      if (t.agentId === agentId) tasks.push(t);
    }
    tasks.sort((a, b) => b.startTime - a.startTime);
    return limit ? tasks.slice(0, limit) : tasks;
  }

  /**
   * 获取当前活跃任务（running 状态）
   */
  getActiveTasks(agentId = null) {
    const tasks = [];
    for (const [id, t] of this.tasks) {
      if (t.status === 'running') {
        if (!agentId || t.agentId === agentId) {
          tasks.push(t);
        }
      }
    }
    tasks.sort((a, b) => b.startTime - a.startTime);
    return tasks;
  }

  /**
   * 获取所有任务（支持分页）
   */
  getAllTasks(limit = 100, offset = 0) {
    const tasks = Array.from(this.tasks.values());
    tasks.sort((a, b) => b.startTime - a.startTime);
    return tasks.slice(offset, offset + limit);
  }

  /**
   * 获取任务统计（按类型/状态聚合）
   */
  getTaskStats() {
    const stats = {
      total: this.tasks.size,
      byStatus: { pending: 0, running: 0, completed: 0, failed: 0 },
      byType: {},
      avgDuration: 0,
    };

    let durationSum = 0;
    let durationCount = 0;

    for (const [id, t] of this.tasks) {
      stats.byStatus[t.status] = (stats.byStatus[t.status] || 0) + 1;
      stats.byType[t.type] = (stats.byType[t.type] || 0) + 1;
      if (t.duration) {
        durationSum += t.duration;
        durationCount++;
      }
    }

    stats.avgDuration = durationCount > 0 ? durationSum / durationCount : 0;
    return stats;
  }

  // ─── 资源快照（v2.2）──────────────────────────────────────

  /**
   * 添加一条资源快照
   */
  addResourceSnapshot(agentId, snapshot) {
    let list = this.resources.get(agentId);
    if (!list) {
      list = [];
      this.resources.set(agentId, list);
    }
    list.push(snapshot);

    // 裁剪：保留时间窗口内的记录（默认 120 分钟）
    const maxAge = 120 * 60 * 1000;
    const cutoff = Date.now() - maxAge;
    while (list.length > 0 && list[0].timestamp < cutoff) {
      list.shift();
    }
    // 兜底上限
    if (list.length > 1440) {
      list.splice(0, list.length - 1440);
    }
    this._dirty = true;
    return snapshot;
  }

  /**
   * 获取 Agent 资源历史
   */
  getResourceHistory(agentId, limit = 60) {
    const list = this.resources.get(agentId);
    if (!list) return [];
    return limit ? list.slice(-limit) : [...list];
  }

  /**
   * 获取最新一条资源快照
   */
  getLatestResources(agentId) {
    const list = this.resources.get(agentId);
    if (!list || list.length === 0) return null;
    return list[list.length - 1];
  }

  /**
   * 获取全局资源统计
   */
  getResourceStats() {
    const byAgent = {};
    for (const [agentId, list] of this.resources) {
      const latest = list.length > 0 ? list[list.length - 1] : null;
      byAgent[agentId] = {
        snapshotCount: list.length,
        latest: latest ? {
          cpu: latest.cpu,
          memory: latest.memory,
          queueDepth: latest.queueDepth,
          disk: latest.disk,
          timestamp: latest.timestamp,
        } : null,
      };
    }
    return { byAgent, agentCount: this.resources.size };
  }

  // ─── 审计记录（v2.3）──────────────────────────────────────

  /**
   * 添加一条审计记录
   * @param {object} entry — { auditId, taskId, agentId, type, summary, input, output, decisionPoints, needsHumanReview }
   */
  setAuditEntry(entry) {
    const record = {
      ...entry,
      timestamp: entry.timestamp || Date.now(),
    };
    this.audit.set(entry.auditId, record);
    this._dirty = true;
    return record;
  }

  /**
   * 获取一条审计记录
   */
  getAuditEntry(auditId) {
    return this.audit.get(auditId) || null;
  }

  /**
   * 获取某个任务的所有审计记录
   */
  getTaskAudit(taskId) {
    const entries = [];
    for (const [id, e] of this.audit) {
      if (e.taskId === taskId) entries.push(e);
    }
    entries.sort((a, b) => a.timestamp - b.timestamp);
    return entries;
  }

  /**
   * 获取某个 Agent 的所有审计记录
   */
  getAgentAudit(agentId, limit = 50) {
    const entries = [];
    for (const [id, e] of this.audit) {
      if (e.agentId === agentId) entries.push(e);
    }
    entries.sort((a, b) => b.timestamp - a.timestamp);
    return limit ? entries.slice(0, limit) : entries;
  }

  /**
   * 多条件搜索审计记录
   * @param {object} query — { agentId, taskId, type, keyword, startTime, endTime, limit, offset }
   * keyword 在 summary + decisionPoints 中模糊匹配
   */
  searchAudit(query = {}) {
    const { agentId, taskId, type, keyword, startTime, endTime, limit = 50, offset = 0 } = query;
    let entries = Array.from(this.audit.values());

    if (agentId) entries = entries.filter(e => e.agentId === agentId);
    if (taskId)  entries = entries.filter(e => e.taskId === taskId);
    if (type)    entries = entries.filter(e => e.type === type);
    if (startTime) entries = entries.filter(e => e.timestamp >= startTime);
    if (endTime)   entries = entries.filter(e => e.timestamp <= endTime);

    if (keyword) {
      const kw = keyword.toLowerCase();
      entries = entries.filter(e => {
        const summary = (e.summary || '').toLowerCase();
        const input = JSON.stringify(e.input || {}).toLowerCase();
        const output = JSON.stringify(e.output || {}).toLowerCase();
        const dp = JSON.stringify(e.decisionPoints || []).toLowerCase();
        return summary.includes(kw) || input.includes(kw) || output.includes(kw) || dp.includes(kw);
      });
    }

    entries.sort((a, b) => b.timestamp - a.timestamp);
    const total = entries.length;
    const paged = entries.slice(offset, offset + limit);
    return { entries: paged, total, limit, offset };
  }

  /**
   * 获取审计统计
   */
  getAuditStats() {
    const stats = {
      total: this.audit.size,
      byType: {},
      byAgent: {},
      needsReview: 0,
    };

    for (const [id, e] of this.audit) {
      stats.byType[e.type] = (stats.byType[e.type] || 0) + 1;
      stats.byAgent[e.agentId] = (stats.byAgent[e.agentId] || 0) + 1;
      if (e.needsHumanReview) stats.needsReview++;
    }

    return stats;
  }

  // ─── 持久化 ───────────────────────────────────────────────

  /**
   * 启动定期持久化
   */
  startPersistence() {
    if (!this.config.persistPath) return;
    if (this._persistTimer) return;

    this._persistTimer = setInterval(() => {
      if (this._dirty) {
        this._save();
      }
    }, this.config.persistInterval);
  }

  /**
   * 停止持久化并强制保存
   */
  async stop() {
    if (this._persistTimer) {
      clearInterval(this._persistTimer);
      this._persistTimer = null;
    }
    if (this._dirty) {
      this._save();
    }
  }

  _save() {
    if (!this.config.persistPath) return;
    try {
      const dir = path.dirname(this.config.persistPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      const data = {
        savedAt: Date.now(),
        agents: Object.fromEntries(this.agents),
        history: Object.fromEntries(
          Array.from(this.history.entries()).map(([k, v]) => [k, v.slice(-50)]) // 只保存最近50条
        ),
        tasks: Object.fromEntries(
          Array.from(this.tasks.entries()).slice(-200) // 只保存最近200个任务
        ),
        resources: Object.fromEntries(
          Array.from(this.resources.entries()).map(([k, v]) => [k, v.slice(-60)]) // 只保存最近60条资源快照
        ),
        audit: Object.fromEntries(
          Array.from(this.audit.entries()).slice(-200) // 只保存最近200条审计记录
        ),
      };

      fs.writeFileSync(this.config.persistPath, JSON.stringify(data, null, 2), 'utf-8');
      this._dirty = false;
    } catch (err) {
      console.error(`[StateStore] Failed to persist: ${err.message}`);
    }
  }

  _load() {
    try {
      if (!fs.existsSync(this.config.persistPath)) return;

      const raw = fs.readFileSync(this.config.persistPath, 'utf-8');
      const data = JSON.parse(raw);

      if (data.agents) {
        for (const [id, state] of Object.entries(data.agents)) {
          this.agents.set(id, state);
        }
      }
      if (data.history) {
        for (const [id, hist] of Object.entries(data.history)) {
          this.history.set(id, hist);
        }
      }
      if (data.tasks) {
        for (const [id, task] of Object.entries(data.tasks)) {
          this.tasks.set(id, task);
        }
      }
      if (data.resources) {
        for (const [id, list] of Object.entries(data.resources)) {
          this.resources.set(id, list);
        }
      }
      if (data.audit) {
        for (const [id, entry] of Object.entries(data.audit)) {
          this.audit.set(id, entry);
        }
      }

      console.log(`[StateStore] Restored ${this.agents.size} agents, ${this.tasks.size} tasks, ${this.resources.size} resource sets, ${this.audit.size} audit records from ${this.config.persistPath}`);
    } catch (err) {
      console.error(`[StateStore] Failed to load: ${err.message}`);
    }
  }

  // ─── 重置 ─────────────────────────────────────────────────

  /**
   * 清空所有数据（测试用）
   */
  reset() {
    this.agents.clear();
    this.history.clear();
    this.tasks.clear();
    this.resources.clear();
    this.audit.clear();
    this._dirty = false;
  }
}

module.exports = { StateStore };

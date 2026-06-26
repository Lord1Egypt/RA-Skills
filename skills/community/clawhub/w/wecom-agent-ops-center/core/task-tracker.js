#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 任务生命周期追踪引擎
 * 架构位置：L2 核心监控引擎
 *
 * 职责：
 * 1. 接收 Agent 推送的任务事件（HTTP API）
 * 2. 管理任务状态机：pending → running → completed/failed
 * 3. 触发 NotifyEngine 推送企微群进度卡片
 * 4. 状态持久化到 StateStore
 *
 * API 端点：
 *   POST /api/tasks/start     → 开始新任务
 *   POST /api/tasks/progress  → 推送进度节点
 *   POST /api/tasks/complete  → 任务完成
 *   POST /api/tasks/fail      → 任务失败
 *   GET  /api/tasks/active    → 获取活跃任务列表
 *   GET  /api/tasks/:id       → 获取任务详情
 */

const crypto = require('crypto');

const DEFAULTS = {
  maxActiveTasks: 50,       // 最大活跃任务数
  taskTimeout: 3600_000,    // 任务超时（1小时）
  cleanupInterval: 60_000,  // 清理检查间隔
};

class TaskTracker {
  /**
   * @param {object} config
   * @param {StateStore} config.stateStore — 状态存储实例
   * @param {NotifyEngine} config.notifyEngine — 通知引擎实例
   * @param {object} [config.options] — 覆盖默认配置
   */
  constructor(config) {
    this.stateStore   = config.stateStore;
    this.notifyEngine = config.notifyEngine;
    this.options      = { ...DEFAULTS, ...(config.options || {}) };

    // 活跃任务跟踪（内存级，用于超时检测）
    this._activeTasks = new Map();  // taskId → { timer, agentId }

    // 启动过期任务清理
    this._cleanupTimer = setInterval(() => this._cleanupStaleTasks(), this.options.cleanupInterval);
  }

  // ─── 任务事件处理 ──────────────────────────────────────────

  /**
   * 开始新任务
   * POST /api/tasks/start
   * Body: { agentId, type, name, metadata? }
   */
  async startTask(body) {
    const { agentId, type, name, metadata } = body;
    if (!agentId || !type || !name) {
      throw new Error('Missing required fields: agentId, type, name');
    }

    const taskId = `task_${crypto.randomUUID().slice(0, 8)}`;
    const now = Date.now();

    const task = {
      taskId,
      agentId,
      type,
      name,
      status: 'running',
      startTime: now,
      endTime: null,
      duration: null,
      nodes: [],
      result: null,
      error: null,
      metadata: metadata || {},
    };

    // 持久化
    this.stateStore.setTask(taskId, task);

    // 跟踪活跃任务
    this._activeTasks.set(taskId, { agentId, startTime: now });

    // 超时检测
    const timer = setTimeout(() => this._handleTimeout(taskId), this.options.taskTimeout);
    this._activeTasks.get(taskId).timer = timer;

    // 推送企微卡片：任务开始
    if (this.notifyEngine) {
      try {
        await this.notifyEngine.sendTaskStartedCard(task);
      } catch (err) {
        console.error(`[TaskTracker] Failed to send task_started card: ${err.message}`);
      }
    }

    console.log(`[TaskTracker] Task started: ${taskId} (${type}: ${name}) on ${agentId}`);
    return task;
  }

  /**
   * 推送进度节点
   * POST /api/tasks/progress
   * Body: { taskId, nodeName, status }
   */
  async progressTask(body) {
    const { taskId, nodeName, status } = body;
    if (!taskId || !nodeName || !status) {
      throw new Error('Missing required fields: taskId, nodeName, status');
    }

    const task = this.stateStore.getTask(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }
    if (task.status !== 'running') {
      throw new Error(`Task ${taskId} is not running (current: ${task.status})`);
    }

    // 添加进度节点
    const node = this.stateStore.addTaskNode(taskId, nodeName, status);

    // 推送企微卡片：任务进度
    if (this.notifyEngine) {
      try {
        await this.notifyEngine.sendTaskProgressCard(task, node);
      } catch (err) {
        console.error(`[TaskTracker] Failed to send task_progress card: ${err.message}`);
      }
    }

    console.log(`[TaskTracker] Task progress: ${taskId} → ${nodeName} (${status})`);
    return node;
  }

  /**
   * 完成任务
   * POST /api/tasks/complete
   * Body: { taskId, result }
   */
  async completeTask(body) {
    const { taskId, result } = body;
    if (!taskId) {
      throw new Error('Missing required field: taskId');
    }

    const task = this.stateStore.completeTask(taskId, result);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    // 清理活跃任务跟踪
    this._clearActiveTask(taskId);

    // 推送企微卡片：任务完成
    if (this.notifyEngine) {
      try {
        await this.notifyEngine.sendTaskCompletedCard(task);
      } catch (err) {
        console.error(`[TaskTracker] Failed to send task_completed card: ${err.message}`);
      }
    }

    console.log(`[TaskTracker] Task completed: ${taskId} (${task.duration}ms)`);
    return task;
  }

  /**
   * 任务失败
   * POST /api/tasks/fail
   * Body: { taskId, error }
   */
  async failTask(body) {
    const { taskId, error } = body;
    if (!taskId || !error) {
      throw new Error('Missing required fields: taskId, error');
    }

    const task = this.stateStore.failTask(taskId, error);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    // 清理活跃任务跟踪
    this._clearActiveTask(taskId);

    // 推送企微卡片：任务失败
    if (this.notifyEngine) {
      try {
        await this.notifyEngine.sendTaskFailedCard(task);
      } catch (err) {
        console.error(`[TaskTracker] Failed to send task_failed card: ${err.message}`);
      }
    }

    console.log(`[TaskTracker] Task failed: ${taskId} — ${error}`);
    return task;
  }

  // ─── 查询 ──────────────────────────────────────────────────

  /**
   * 获取活跃任务列表
   */
  getActiveTasks(agentId = null) {
    return this.stateStore.getActiveTasks(agentId);
  }

  /**
   * 获取任务详情
   */
  getTask(taskId) {
    return this.stateStore.getTask(taskId);
  }

  /**
   * 获取 Agent 任务列表
   */
  getAgentTasks(agentId, limit = 20) {
    return this.stateStore.getAgentTasks(agentId, limit);
  }

  // ─── 内部方法 ──────────────────────────────────────────────

  /**
   * 清理活跃任务跟踪
   */
  _clearActiveTask(taskId) {
    const entry = this._activeTasks.get(taskId);
    if (entry) {
      if (entry.timer) clearTimeout(entry.timer);
      this._activeTasks.delete(taskId);
    }
  }

  /**
   * 处理任务超时
   */
  async _handleTimeout(taskId) {
    const task = this.stateStore.getTask(taskId);
    if (!task) return;
    if (task.status !== 'running') return;

    const error = `Task timed out after ${this.options.taskTimeout / 1000}s`;
    console.warn(`[TaskTracker] ${error}: ${taskId}`);

    this.stateStore.failTask(taskId, error);
    this._activeTasks.delete(taskId);

    if (this.notifyEngine) {
      try {
        await this.notifyEngine.sendTaskFailedCard(task);
      } catch (err) {
        console.error(`[TaskTracker] Failed to send timeout alert: ${err.message}`);
      }
    }
  }

  /**
   * 清理过期活跃任务（没有心跳的僵尸任务）
   */
  _cleanupStaleTasks() {
    const now = Date.now();
    for (const [taskId, entry] of this._activeTasks) {
      const age = now - entry.startTime;
      if (age > this.options.taskTimeout * 2) {
        console.warn(`[TaskTracker] Cleaning up stale task: ${taskId} (age: ${Math.round(age / 1000)}s)`);
        const task = this.stateStore.getTask(taskId);
        if (task && task.status === 'running') {
          this.stateStore.failTask(taskId, 'Stale task cleaned up');
        }
        if (entry.timer) clearTimeout(entry.timer);
        this._activeTasks.delete(taskId);
      }
    }
  }

  /**
   * 优雅关闭
   */
  async shutdown() {
    if (this._cleanupTimer) {
      clearInterval(this._cleanupTimer);
      this._cleanupTimer = null;
    }

    // 清理所有超时计时器
    for (const [taskId, entry] of this._activeTasks) {
      if (entry.timer) clearTimeout(entry.timer);
    }
    this._activeTasks.clear();

    console.log('[TaskTracker] Shutdown complete');
  }
}

module.exports = { TaskTracker };

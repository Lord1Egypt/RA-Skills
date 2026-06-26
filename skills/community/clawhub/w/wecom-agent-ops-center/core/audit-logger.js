#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 审计日志模块 (v2.3)
 *
 * 职责：
 * 1. 接收任务完成/失败事件，保存完整审计记录
 * 2. 决策点结构化记录（关键决策的选项+理由）
 * 3. 支持按时间段/Agent/任务类型检索
 * 4. 生成审计摘要报告（输入→决策→输出 的完整链路）
 *
 * 架构位置：L2 核心监控引擎
 *
 * 数据模型（AuditEntry）:
 *   {
 *     auditId: string,        // UUID
 *     taskId: string,         // 关联任务
 *     agentId: string,        // 所属 Agent
 *     timestamp: number,
 *     type: 'task_complete' | 'task_fail' | 'decision_point' | 'error' | 'handoff' | 'state_change',
 *     summary: string,        // 一句话描述
 *     input: object,          // 任务输入
 *     output: object,         // 任务输出
 *     decisionPoints: [{ point, choice, reason, alternatives }],
 *     needsHumanReview: boolean,
 *     metadata: object,       // 扩展信息
 *   }
 *
 * 推送：
 *   emit('audit:recorded', auditEntry)
 *     → NotifyEngine.auditSummaryCard()
 *     → 企微群收到执行摘要报告
 */

const crypto = require('crypto');

const DEFAULTS = {
  maxAuditAge: 7 * 24 * 3600 * 1000, // 审计记录保留 7 天
};

class AuditLogger {
  constructor(config) {
    this.config = { ...DEFAULTS, ...(config || {}) };
    this.stateStore = config.stateStore || null;
    this.notifyEngine = config.notifyEngine || null;
    this.listeners = [];
  }

  /**
   * 记录一条审计信息
   * @param {object} entry — 审计记录（auditId 可选，不提供则自动生成）
   */
  async log(entry) {
    if (!entry.agentId) throw new Error('agentId is required');
    if (!entry.type) throw new Error('type is required');

    const auditId = entry.auditId || `audit_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;

    const record = {
      auditId,
      taskId: entry.taskId || null,
      agentId: entry.agentId,
      timestamp: entry.timestamp || Date.now(),
      type: entry.type,
      summary: entry.summary || '',
      input: entry.input || {},
      output: entry.output || {},
      decisionPoints: entry.decisionPoints || [],
      needsHumanReview: entry.needsHumanReview || false,
      metadata: entry.metadata || {},
    };

    if (this.stateStore) {
      this.stateStore.setAuditEntry(record);
    }

    // 发射事件 → NotifyEngine 生成审计卡片
    this._emit('audit:recorded', record);

    return record;
  }

  /**
   * 从任务完成事件自动生成审计记录
   * @param {object} task — TaskRecord
   * @param {object} opts — { decisionPoints, metadata }
   */
  async logFromTask(task, opts = {}) {
    const isFail = task.status === 'failed';
    const auditEntry = {
      agentId: task.agentId,
      taskId: task.taskId,
      type: isFail ? 'task_fail' : 'task_complete',
      summary: isFail
        ? `任务执行失败: ${task.name} - ${task.error || '未知错误'}`
        : `任务执行成功: ${task.name}，共 ${task.nodes ? task.nodes.length : 0} 个节点`,
      input: {
        taskType: task.type,
        taskName: task.name,
        startTime: task.startTime,
      },
      output: {
        status: task.status,
        duration: task.duration,
        nodeCount: task.nodes ? task.nodes.length : 0,
        result: task.result || null,
        error: task.error || null,
        nodes: task.nodes ? task.nodes.map(n => ({ name: n.name, status: n.status })) : [],
      },
      decisionPoints: opts.decisionPoints || [],
      needsHumanReview: isFail || (opts.needsHumanReview || false),
      metadata: {
        adapterType: task.adapterType || 'unknown',
        ...(opts.metadata || {}),
      },
    };

    return this.log(auditEntry);
  }

  /**
   * 记录一个决策点（独立于任务完成事件）
   */
  async logDecision(agentId, taskId, decision) {
    return this.log({
      agentId,
      taskId: taskId || null,
      type: 'decision_point',
      summary: `${decision.point}: 选择「${decision.choice}」`,
      decisionPoints: [decision],
      timestamp: decision.timestamp || Date.now(),
    });
  }

  /**
   * 生成任务的执行摘要报告（Markdown）
   */
  generateSummary(taskId) {
    const entries = this.stateStore
      ? this.stateStore.getTaskAudit(taskId)
      : [];
    const task = this.stateStore
      ? this.stateStore.getTask(taskId)
      : null;

    if (!task && entries.length === 0) return null;

    const lines = [];
    lines.push(`## 📋 任务执行摘要`);
    lines.push('');

    if (task) {
      const statusIcon = task.status === 'completed' ? '✅' : task.status === 'failed' ? '💥' : '🔄';
      lines.push(`**${statusIcon} ${task.name}**`);
      lines.push('');
      lines.push(`| 项目 | 详情 |`);
      lines.push(`|------|------|`);
      lines.push(`| 任务 ID | \`${task.taskId}\` |`);
      lines.push(`| 执行 Agent | ${task.agentId} |`);
      lines.push(`| 任务类型 | \`${task.type}\` |`);
      lines.push(`| 状态 | ${task.status} |`);
      if (task.duration) {
        lines.push(`| 耗时 | ${_fmtDuration(task.duration)} |`);
      }
      lines.push('');
    }

    // 决策点
    const allDecisions = [];
    for (const e of entries) {
      if (e.decisionPoints && e.decisionPoints.length > 0) {
        allDecisions.push(...e.decisionPoints.map(dp => ({
          ...dp,
          auditId: e.auditId,
          timestamp: e.timestamp,
        })));
      }
    }

    if (allDecisions.length > 0) {
      lines.push('### 🧠 关键决策点');
      lines.push('');
      for (const dp of allDecisions) {
        lines.push(`**${dp.point}**`);
        lines.push(`- 选择：**${dp.choice}**`);
        lines.push(`- 理由：${dp.reason}`);
        if (dp.alternatives && dp.alternatives.length > 0) {
          lines.push(`- 备选：${dp.alternatives.join(' / ')}`);
        }
        lines.push('');
      }
    }

    // 执行节点
    if (task && task.nodes && task.nodes.length > 0) {
      lines.push('### 📊 执行节点');
      lines.push('');
      for (const n of task.nodes) {
        const icon = n.status === 'done' ? '✅' : n.status === 'failed' ? '❌' : n.status === 'running' ? '🔄' : '⏳';
        lines.push(`- ${icon} **${n.name}** — ${_nodeLabel(n.status)}`);
      }
      lines.push('');
    }

    // 审计记录
    if (entries.length > 0) {
      lines.push('### 📝 审计记录');
      lines.push('');
      for (const e of entries) {
        const time = new Date(e.timestamp).toLocaleTimeString('zh-CN', { hour12: false });
        const typeIcon = _typeIcon(e.type);
        lines.push(`- \`${time}\` ${typeIcon} ${e.summary}`);
      }
    }

    return lines.join('\n');
  }

  /**
   * 按任务 ID 搜索审计记录
   */
  getTaskAudit(taskId) {
    return this.stateStore
      ? this.stateStore.getTaskAudit(taskId)
      : [];
  }

  /**
   * 多条件搜索
   */
  search(query) {
    return this.stateStore
      ? this.stateStore.searchAudit(query)
      : { entries: [], total: 0, limit: query.limit || 50, offset: query.offset || 0 };
  }

  /**
   * 获取统计
   */
  getStats() {
    return this.stateStore
      ? this.stateStore.getAuditStats()
      : { total: 0, byType: {}, byAgent: {}, needsReview: 0 };
  }

  // ─── 事件系统 ─────────────────────────────────────────────

  on(event, handler) {
    this.listeners.push({ event, handler });
  }

  _emit(event, data) {
    for (const l of this.listeners) {
      if (l.event === event || l.event === '*') {
        try { l.handler(data); } catch (err) {
          console.error(`[AuditLogger] Listener error for ${event}: ${err.message}`);
        }
      }
    }
  }

  // ─── 清理 ─────────────────────────────────────────────────

  /**
   * 清理过期审计记录
   */
  async cleanup() {
    if (!this.stateStore) return 0;

    const cutoff = Date.now() - this.config.maxAuditAge;
    let removed = 0;

    for (const [id, entry] of this.stateStore.audit) {
      if (entry.timestamp < cutoff) {
        this.stateStore.audit.delete(id);
        removed++;
      }
    }

    if (removed > 0) {
      console.log(`[AuditLogger] Cleaned up ${removed} expired audit records`);
    }

    return removed;
  }

  async shutdown() {
    await this.cleanup();
    this.listeners = [];
  }
}

// ─── 工具函数 ────────────────────────────────────────────────

function _fmtDuration(ms) {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  const sec = Math.round(ms / 1000);
  if (sec < 60) return `${sec} 秒`;
  const min = Math.floor(sec / 60);
  return `${min} 分 ${sec % 60} 秒`;
}

function _nodeLabel(status) {
  const map = { done: '已完成', running: '执行中', pending: '等待中', failed: '失败' };
  return map[status] || status;
}

function _typeIcon(type) {
  const map = {
    task_complete: '✅',
    task_fail: '💥',
    decision_point: '🧠',
    error: '🚨',
    handoff: '🤝',
    state_change: '🔄',
  };
  return map[type] || '📌';
}

module.exports = { AuditLogger };

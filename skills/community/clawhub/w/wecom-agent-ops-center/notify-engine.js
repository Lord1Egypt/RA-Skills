#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 通知引擎
 * 职责：根据监控事件生成富卡片通知，支持三种卡片类型
 *
 * 架构位置：L2 监控通知层 → L3 企微 UI 层
 *
 * 三种卡片类型：
 *   1. health_report   — 心跳正常，定期推送（绿色）
 *   2. alert           — 异常告警（红色/橙色）
 *   3. daily_summary   — 每日状态汇总（蓝色）
 */

// ─── 卡片模板常量 ────────────────────────────────────────────

const COLORS = {
  healthy:  'info',      // 绿色/蓝色
  warning:  'warning',   // 橙色
  critical: 'warning',   // 红色告警
};

const EMOJI = {
  online:    '🟢',
  offline:   '🔴',
  degraded:  '🟡',
  unknown:   '⚪',
  health:    '💚',
  alert:     '🚨',
  report:    '📊',
  clock:     '🕐',
  latency:   '⏱️',
  check:     '✅',
  cross:     '❌',
  info:      'ℹ️',
  brain:     '🧠',
  robot:     '🤖',
  task:      '📋',
  play:      '▶️',
  done:      '✅',
  fail:      '💥',
  progress:  '🔄',
  rocket:    '🚀',
  pin:       '📌',
  cpu:       '🔥',
  memory:    '💾',
  disk:      '💿',
  queue:     '📊',
};

// ─── 通知引擎 ───────────────────────────────────────────────

class NotifyEngine {
  constructor(config) {
    this.config = config || {};
    this.alertThrottle = new Map();  // agentId → lastAlertTime（防抖）
    this.alertCooldown  = config.alertCooldown || 300_000; // 5 分钟冷却
    this._sender = config.cardSender || null; // 卡片发送回调 (v2.1)
    this._chatId = config.chatId || null;     // 默认推送群 (v2.1)
  }

  /**
   * 设置卡片发送回调
   * @param {function} sender — async (cardPayload) => void
   */
  setSender(sender) {
    this._sender = sender;
  }

  // ─── 内部发送 ─────────────────────────────────────────────

  async _send(card) {
    if (!card) return;
    if (this._sender) {
      try {
        await this._sender(card);
      } catch (err) {
        console.error(`[NotifyEngine] Card send failed: ${err.message}`);
      }
    }
  }

  // ─── 公开 API ─────────────────────────────────────────────

  /**
   * 生成心跳正常的定期通知卡片
   */
  healthReportCard(snapshot) {
    const lines = [];

    lines.push(`## ${EMOJI.health} Agent 健康报告`);
    lines.push(`> 更新时间：${_fmtTime(snapshot.timestamp)}`);
    lines.push('');

    if (snapshot.total === 0) {
      lines.push(`${EMOJI.info} 当前没有注册的 Agent。`);
      lines.push('');
      lines.push('请在配置中添加 Agent 端点。');
      return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
    }

    // 状态摘要条
    const statusBar = [
      `${EMOJI.online} **${snapshot.healthy}** 正常`,
      `${EMOJI.degraded} **${snapshot.degraded}** 降级`,
      `${EMOJI.offline} **${snapshot.offline}** 离线`,
    ];
    lines.push(statusBar.join('  |  '));
    lines.push('');

    // 每个 Agent 的状态
    lines.push('---');
    for (const a of snapshot.agents) {
      const icon = _statusIcon(a.status);
      const name = a.name || a.id;
      const latency = a.avgLatency ? ` — ${EMOJI.latency} ${Math.round(a.avgLatency)}ms` : '';
      const fail = a.failStreak > 0 ? ` (连续失败 ${a.failStreak} 次)` : '';
      lines.push(`- ${icon} **${name}**${latency}${fail}`);
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 生成异常告警卡片
   */
  alertCard(event) {
    const { agentId, agent, prevStatus, failCount, error } = event;
    const isOffline = failCount >= 3;
    const severity = isOffline ? 'critical' : 'warning';
    const icon = isOffline ? EMOJI.offline : EMOJI.degraded;
    const name = agent ? agent.name : agentId;

    const lines = [];

    lines.push(`## ${EMOJI.alert} ${isOffline ? 'Agent 离线告警' : 'Agent 健康降级'}`);
    lines.push(`> ${_fmtTime(Date.now())}`);
    lines.push('');

    // 告警详情
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| Agent | **${name}** (${agentId}) |`);
    lines.push(`| 之前状态 | ${_statusLabel(prevStatus)} |`);
    lines.push(`| 当前状态 | ${icon} **${isOffline ? '离线' : '降级'}** |`);
    lines.push(`| 连续失败 | ${failCount} 次 |`);
    if (error) {
      lines.push(`| 错误信息 | \`${_trunc(error)}\` |`);
    }

    // 端点信息
    if (agent && agent.endpoint) {
      lines.push(`| 检查端点 | \`${agent.endpoint}\` |`);
    }
    lines.push('');

    // 操作建议
    lines.push('---');
    lines.push('**🔧 建议操作：**');
    if (isOffline) {
      lines.push('1. 检查 Agent 进程是否在运行');
      lines.push('2. 确认端口未被防火墙屏蔽');
      lines.push(`3. 手动测试：\`curl ${agent ? agent.endpoint || (agent.host + ':' + agent.port) : '???'}\``);
    } else {
      lines.push('1. 观察是否自动恢复（可能是网络抖动）');
      lines.push('2. 如持续降级，检查 Agent 响应延迟');
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 生成每日状态汇总卡片
   */
  dailySummaryCard(snapshot, stats) {
    const lines = [];
    const total = snapshot.total;
    const healthy = snapshot.healthy;
    const healthyRate = total > 0 ? ((healthy / total) * 100).toFixed(1) : 0;

    lines.push(`## ${EMOJI.report} Agent 日报 — ${_fmtDate()}`);
    lines.push(`> ${_fmtTime(Date.now())}`);
    lines.push('');

    // 总体指标
    lines.push(`### 📈 总体健康度`);
    lines.push(`| 指标 | 数值 |`);
    lines.push(`|------|------|`);
    lines.push(`| 总 Agent 数 | ${total} |`);
    lines.push(`| 健康 Agent | ${EMOJI.online} ${healthy} (${healthyRate}%) |`);
    lines.push(`| 降级 Agent | ${EMOJI.degraded} ${snapshot.degraded} |`);
    lines.push(`| 离线 Agent | ${EMOJI.offline} ${snapshot.offline} |`);

    if (stats) {
      if (stats.totalChecks) lines.push(`| 今日检查次数 | ${stats.totalChecks} |`);
      if (stats.totalFailures) lines.push(`| 今日失败次数 | ${stats.totalFailures} |`);
      if (stats.avgLatency) lines.push(`| 平均延迟 | ${Math.round(stats.avgLatency)}ms |`);
    }
    lines.push('');

    // 每个 Agent 详情
    if (total > 0) {
      lines.push('---');
      lines.push(`### ${EMOJI.robot} Agent 详情`);
      lines.push('');
      for (const a of snapshot.agents) {
        const icon = _statusIcon(a.status);
        const name = a.name || a.id;
        const latency = a.avgLatency ? ` ${Math.round(a.avgLatency)}ms` : '';
        const uptime = a.totalChecks ? `${a.totalChecks - (a.totalFailures || 0)}/${a.totalChecks}` : '';
        lines.push(`- ${icon} **${name}**${latency} — 成功率 ${uptime}`);
      }
    }

    // 趋势
    if (snapshot.offline > 0) {
      lines.push('');
      lines.push(`> ${EMOJI.alert} **注意**：${snapshot.offline} 个 Agent 离线，请及时处理！`);
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 生成状态变化通知卡片（Agent 上线/下线）
   */
  stateChangeCard(event) {
    const { agentId, agent, from, to } = event;
    const name = agent ? agent.name : agentId;

    if (to === 'healthy' && from !== 'healthy') {
      // Agent 恢复了！
      return {
        msgtype: 'markdown',
        markdown: {
          content: [
            `## ${EMOJI.online} Agent 已恢复`,
            `> ${_fmtTime(Date.now())}`,
            '',
            `**${name}** (${agentId}) 已从 **${_statusLabel(from)}** 恢复为 **正常**。`,
          ].join('\n'),
        },
      };
    }

    return null; // 其他的由 alertCard 处理
  }

  // ─── 任务进度卡片（v2.1）───────────────────────────────────

  /**
   * 任务开始卡片
   */
  taskStartedCard(task) {
    const lines = [];
    lines.push(`## ${EMOJI.play} 任务开始`);
    lines.push(`> ${_fmtTime(task.startTime)}`);
    lines.push('');
    lines.push(`**${task.name}**`);
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| 任务类型 | \`${task.type}\` |`);
    lines.push(`| 执行 Agent | ${task.agentId} |`);
    lines.push(`| 任务 ID | \`${task.taskId}\` |`);
    if (task.metadata && task.metadata.estimatedDuration) {
      lines.push(`| 预计耗时 | ${_fmtDuration(task.metadata.estimatedDuration)} |`);
    }
    lines.push('');
    lines.push(`${EMOJI.progress} 任务进行中...`);
    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 任务进度节点卡片
   */
  taskProgressCard(task, node) {
    const lines = [];
    const nodeEmoji = node.status === 'done' ? EMOJI.check : node.status === 'failed' ? EMOJI.cross : EMOJI.progress;
    const elapsed = _fmtDuration(Date.now() - task.startTime);

    lines.push(`## ${EMOJI.progress} 任务进度更新`);
    lines.push(`> ${_fmtTime(Date.now())} | 已运行 ${elapsed}`);
    lines.push('');
    lines.push(`**${task.name}**`);
    lines.push('');
    lines.push(`${nodeEmoji} **${node.name}** — ${_nodeStatusLabel(node.status)}`);
    lines.push('');

    // 展示所有已完成节点
    if (task.nodes && task.nodes.length > 1) {
      lines.push(`### 已完成步骤`);
      const doneNodes = task.nodes.filter(n => n.status === 'done');
      for (const n of doneNodes) {
        lines.push(`- ${EMOJI.check} ${n.name}`);
      }
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 任务完成卡片
   */
  taskCompletedCard(task) {
    const lines = [];
    const duration = task.duration || (task.endTime - task.startTime);

    lines.push(`## ${EMOJI.done} 任务完成`);
    lines.push(`> ${_fmtTime(Date.now())}`);
    lines.push('');
    lines.push(`**${task.name}** 已成功完成`);
    lines.push('');
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| 任务类型 | \`${task.type}\` |`);
    lines.push(`| 执行 Agent | ${task.agentId} |`);
    lines.push(`| 总耗时 | ${_fmtDuration(duration)} |`);
    lines.push(`| 执行节点 | ${task.nodes ? task.nodes.length : 0} 个 |`);

    if (task.result) {
      const resultStr = typeof task.result === 'string' ? task.result : JSON.stringify(task.result);
      const summary = _trunc(resultStr, 200);
      lines.push(`| 结果摘要 | ${summary} |`);
    }
    lines.push('');
    lines.push(`${EMOJI.rocket} 任务完成，辛苦了！`);

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  /**
   * 任务失败卡片
   */
  taskFailedCard(task) {
    const lines = [];
    const duration = task.duration || (task.endTime ? task.endTime - task.startTime : null);

    lines.push(`## ${EMOJI.fail} 任务失败`);
    lines.push(`> ${_fmtTime(Date.now())}`);
    lines.push('');
    lines.push(`**${task.name}** 执行失败`);
    lines.push('');
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| 任务类型 | \`${task.type}\` |`);
    lines.push(`| 执行 Agent | ${task.agentId} |`);
    if (duration) lines.push(`| 失败时间 | 运行 ${_fmtDuration(duration)} 后 |`);
    if (task.nodes && task.nodes.length > 0) {
      const lastNode = task.nodes[task.nodes.length - 1];
      lines.push(`| 最后节点 | ${lastNode.name} (${_nodeStatusLabel(lastNode.status)}) |`);
    }
    lines.push(`| 错误信息 | \`${_trunc(task.error || '未知错误', 150)}\` |`);

    if (task.nodes && task.nodes.length > 1) {
      lines.push('');
      lines.push(`### 已执行步骤`);
      for (const n of task.nodes) {
        const icon = n.status === 'done' ? EMOJI.check : n.status === 'failed' ? EMOJI.cross : EMOJI.progress;
        lines.push(`- ${icon} ${n.name}`);
      }
    }
    lines.push('');
    lines.push(`> ${EMOJI.alert} 请检查 Agent 日志并重试。`);

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  // ─── 资源告警卡片（v2.2）───────────────────────────────────

  /**
   * 生成资源阈值告警卡片
   * @param {object} alert — { agentId, agentName, metric, message, severity, value, threshold }
   */
  resourceAlertCard(alert) {
    const { agentId, agentName, metric, message, severity, value, threshold } = alert;
    const isCritical = severity === 'critical';
    const metricEmoji = EMOJI[metric] || '📈';
    const icon = isCritical ? EMOJI.alert : EMOJI.info;

    const lines = [];

    lines.push(`## ${icon} ${isCritical ? '严重资源告警' : '资源使用预警'}`);
    lines.push(`> ${_fmtTime(Date.now())}`);
    lines.push('');

    // 告警详情
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| Agent | **${agentName}** (${agentId}) |`);
    lines.push(`| 指标 | ${metricEmoji} ${_metricLabel(metric)} |`);
    lines.push(`| 当前值 | **${typeof value === 'number' ? value.toFixed(1) : value}**${_metricUnit(metric)} |`);
    lines.push(`| 告警阈值 | ${threshold}${_metricUnit(metric)} |`);
    lines.push(`| 严重程度 | ${isCritical ? '🔴 严重' : '🟡 警告'} |`);
    lines.push(`| 消息 | ${message} |`);
    lines.push('');

    // 操作建议
    lines.push('---');
    lines.push('**🔧 建议操作：**');
    for (const tip of _resourceTips(metric, isCritical)) {
      lines.push(`- ${tip}`);
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  // ─── 发送封装（v2.1）───────────────────────────────────────

  async sendTaskStartedCard(task) {
    await this._send(this.taskStartedCard(task));
  }

  async sendTaskProgressCard(task, node) {
    await this._send(this.taskProgressCard(task, node));
  }

  async sendTaskCompletedCard(task) {
    await this._send(this.taskCompletedCard(task));
  }

  async sendTaskFailedCard(task) {
    await this._send(this.taskFailedCard(task));
  }

  // ─── 审计摘要卡片（v2.3）───────────────────────────────────

  /**
   * 生成审计摘要卡片 — 任务执行报告（输入→决策→输出）
   * @param {object} auditEntry — AuditEntry from AuditLogger
   * @param {object} task — 可选，关联的 TaskRecord（展示节点信息）
   */
  auditSummaryCard(auditEntry, task) {
    const lines = [];
    const isFail = auditEntry.type === 'task_fail';
    const icon = isFail ? '💥' : '✅';
    const title = isFail ? '任务执行报告 — 失败' : '任务执行报告 — 完成';

    lines.push(`## ${icon} ${title}`);
    lines.push(`> ${_fmtTime(auditEntry.timestamp)}`);
    lines.push('');

    // 基本信息
    lines.push(`| 项目 | 详情 |`);
    lines.push(`|------|------|`);
    lines.push(`| 审计 ID | \`${auditEntry.auditId}\` |`);
    if (auditEntry.taskId) {
      lines.push(`| 关联任务 | \`${auditEntry.taskId}\` |`);
    }
    lines.push(`| 执行 Agent | ${auditEntry.agentId} |`);
    if (auditEntry.output && auditEntry.output.duration) {
      lines.push(`| 耗时 | ${_fmtDuration(auditEntry.output.duration)} |`);
    }
    lines.push(`| 状态 | ${isFail ? '失败' : '成功'} |`);
    lines.push('');

    // 摘要
    if (auditEntry.summary) {
      lines.push(`### ${_fmtLevelIcon('info')} 执行摘要`);
      lines.push(auditEntry.summary);
      lines.push('');
    }

    // 决策点
    if (auditEntry.decisionPoints && auditEntry.decisionPoints.length > 0) {
      lines.push(`### 🧠 关键决策点`);
      lines.push('');
      for (const dp of auditEntry.decisionPoints) {
        lines.push(`**${dp.point}**`);
        lines.push(`> ✅ 选择：**${dp.choice}**`);
        lines.push(`> 💡 理由：${dp.reason}`);
        if (dp.alternatives && dp.alternatives.length > 0) {
          lines.push(`> 🔄 备选：${dp.alternatives.join(' / ')}`);
        }
        lines.push('');
      }
    }

    // 执行节点
    if (task && task.nodes && task.nodes.length > 0) {
      lines.push(`### 📊 执行节点`);
      lines.push('');
      for (const n of task.nodes) {
        const nIcon = n.status === 'done' ? '✅' : n.status === 'failed' ? '❌' : n.status === 'running' ? '🔄' : '⏳';
        lines.push(`- ${nIcon} **${n.name}**`);
      }
      lines.push('');
    }

    // 输出摘要
    if (auditEntry.output) {
      lines.push(`### 📤 输出`);
      const out = auditEntry.output;
      if (out.result) {
        const resultStr = typeof out.result === 'string' ? out.result : JSON.stringify(out.result);
        lines.push(`> ${_trunc(resultStr, 200)}`);
      }
      if (out.nodeCount !== undefined) {
        lines.push(`- 执行节点：${out.nodeCount} 个`);
      }
      if (out.error) {
        lines.push(`- 错误信息：\`${_trunc(out.error, 150)}\``);
      }
      lines.push('');
    }

    // 操作建议
    if (isFail) {
      lines.push('---');
      lines.push('**🔧 建议操作：**');
      lines.push('1. 查看完整审计记录（仪表板 → 审计查询）');
      lines.push('2. 检查失败节点的具体错误信息');
      lines.push('3. 根据决策点确认是否需要人工介入');
    }

    if (auditEntry.needsHumanReview) {
      lines.push('');
      lines.push(`> ⚠️ **本条记录需要人工复核**`);
    }

    return { msgtype: 'markdown', markdown: { content: lines.join('\n') } };
  }

  async sendAuditSummaryCard(auditEntry, task) {
    await this._send(this.auditSummaryCard(auditEntry, task));
  }

  // ─── 防抖 ─────────────────────────────────────────────────

  /**
   * 判断是否应该发送告警（5分钟内不重复）
   */
  shouldAlert(agentId) {
    const last = this.alertThrottle.get(agentId);
    if (last && Date.now() - last < this.alertCooldown) {
      return false;
    }
    this.alertThrottle.set(agentId, Date.now());
    return true;
  }
}

// ─── 工具函数 ────────────────────────────────────────────────

function _fmtTime(ts) {
  const d = new Date(ts);
  return d.toLocaleString('zh-CN', { hour12: false });
}

function _fmtDate() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

function _statusIcon(status) {
  const map = { healthy: EMOJI.online, degraded: EMOJI.degraded, offline: EMOJI.offline, unknown: EMOJI.unknown, registered: EMOJI.unknown };
  return map[status] || EMOJI.unknown;
}

function _statusLabel(status) {
  const map = { healthy: '正常', degraded: '降级', offline: '离线', unknown: '未知', registered: '已注册' };
  return map[status] || status;
}

function _trunc(s, max = 60) {
  return s.length > max ? s.slice(0, max) + '...' : s;
}

function _fmtDuration(ms) {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  const sec = Math.round(ms / 1000);
  if (sec < 60) return `${sec} 秒`;
  const min = Math.floor(sec / 60);
  const remainSec = sec % 60;
  if (min < 60) return `${min} 分 ${remainSec} 秒`;
  const hours = Math.floor(min / 60);
  const remainMin = min % 60;
  return `${hours} 小时 ${remainMin} 分`;
}

function _nodeStatusLabel(status) {
  const map = { done: '已完成', running: '执行中', pending: '等待中', failed: '失败' };
  return map[status] || status;
}

function _metricLabel(metric) {
  const map = { cpu: 'CPU 使用率', memory: '内存使用率', queue: '任务队列深度', disk: '磁盘使用率' };
  return map[metric] || metric;
}

function _metricUnit(metric) {
  const map = { cpu: '%', memory: '%', queue: ' 个', disk: '%' };
  return map[metric] || '';
}

function _resourceTips(metric, isCritical) {
  const tips = {
    cpu: [
      '检查是否有异常进程占用 CPU',
      '考虑减少并发 Agent 任务数',
      isCritical ? '⚠️ 立即停止非关键任务，排查死循环' : '观察 5 分钟，如不下降再介入',
    ],
    memory: [
      '检查 Agent 是否有内存泄漏',
      '考虑重启 Agent 进程释放内存',
      isCritical ? '⚠️ 立即重启 Agent，防止 OOM' : '观察内存趋势，如持续上升需调查',
    ],
    queue: [
      '检查 Agent 处理速度是否下降',
      '考虑增加 Agent 实例分摊负载',
      isCritical ? '⚠️ 暂停新任务入队，先消化积压' : '观察队列消化速度',
    ],
    disk: [
      '清理日志文件和临时文件',
      '检查是否有异常大文件写入',
      isCritical ? '⚠️ 立即清理磁盘，防止服务中断' : '安排定期清理计划',
    ],
  };
  return tips[metric] || ['检查相关指标', '必要时手动介入'];
}

function _fmtLevelIcon(level) {
  const map = { info: 'ℹ️', warning: '⚠️', critical: '🚨' };
  return map[level] || '📌';
}

module.exports = { NotifyEngine };

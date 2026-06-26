#!/usr/bin/env node
/**
 * Work Monitor — 全量工作监控脚本
 * 
 * 功能：
 * 1. 扫描所有 agent 的活跃会话
 * 2. 检测超时/卡死/失败的会话
 * 3. 检测子会话（childSessions）状态
 * 4. 检测未完成的工作流
 * 5. 输出监控报告
 * 
 * 用法:
 *   node work-monitor.js              # 全量检查
 *   node work-monitor.js --agents     # 只看 agent 状态
 *   node work-monitor.js --cron       # 只看 cron 任务
 *   node work-monitor.js --children   # 只看子会话
 *   node work-monitor.js --json       # JSON 输出
 *
 * 此脚本设计为被 OpenClaw agent 通过 exec 调用，
 * agent 读取输出后决定是否需要人工介入或自动恢复。
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const STATE_FILE = path.join(WORKSPACE, 'skills/work-progress/state.json');
const TODAY = new Date().toISOString().slice(0, 10);
const NOW = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

// ============================================================================
// 超时配置（毫秒）
// ============================================================================
const TIMEOUT = {
  cron_normal: 60_000,       // cron 任务正常上限：1 分钟
  cron_warning: 120_000,     // cron 任务警告阈值：2 分钟
  cron_critical: 300_000,    // cron 任务严重超时：5 分钟
  session_idle: 600_000,     // 会话空闲上限：10 分钟无活动
  child_session: 1800_000,   // 子会话运行上限：30 分钟
};

// ============================================================================
// 工具函数
// ============================================================================

function runOpenClaw(args) {
  try {
    return JSON.parse(execSync(`openclaw ${args} --json 2>/dev/null`, {
      encoding: 'utf8',
      timeout: 15000,
    }));
  } catch (e) {
    return null;
  }
}

function fmtDuration(ms) {
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m${s % 60}s`;
  const h = Math.floor(m / 60);
  return `${h}h${m % 60}m`;
}

function isTimedOut(session, nowMs) {
  const started = session.startedAt || 0;
  const elapsed = nowMs - started;
  
  const label = session.label || session.displayName || '';
  const isCron = label.includes('Cron') || session.kind === 'other';
  
  if (isCron && elapsed > TIMEOUT.cron_critical) return 'critical';
  if (isCron && elapsed > TIMEOUT.cron_warning) return 'warning';
  if (elapsed > TIMEOUT.child_session) return 'critical';
  if (elapsed > TIMEOUT.session_idle && session.status === 'running') return 'warning';
  
  return null;
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { tasks: {}, evicted: [], lastCheck: null, version: 1 };
  }
}

function saveState(state) {
  state.lastCheck = new Date().toISOString();
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ============================================================================
// 核心监控逻辑
// ============================================================================

function scanAllSessions() {
  const data = runOpenClaw('sessions list --all-agents --active 60');
  if (!data || !data.sessions) return [];
  return data.sessions;
}

function analyzeSessions(sessions) {
  const now = Date.now();
  const state = loadState();
  const report = {
    timestamp: NOW,
    summary: {
      total: sessions.length,
      running: 0,
      done: 0,
      failed: 0,
      idle: 0,
      timed_out: 0,
    },
    agents: {},
    cron_tasks: [],
    child_sessions: [],
    issues: [],
    recoverable: [],
  };

  for (const s of sessions) {
    const agentId = s.key?.split(':')[1] || 'unknown';
    const elapsed = now - (s.startedAt || now);
    const timeoutLevel = isTimedOut(s, now);

    // 按 agent 分组
    if (!report.agents[agentId]) {
      report.agents[agentId] = { sessions: 0, running: 0, issues: [] };
    }
    report.agents[agentId].sessions++;

    // 分类统计
    if (s.status === 'running') {
      report.summary.running++;
      report.agents[agentId].running++;
    } else if (s.status === 'failed') {
      report.summary.failed++;
    } else if (s.status === 'done') {
      report.summary.done++;
    }

    // Cron 任务分析
    if (s.label?.includes('Cron')) {
      const cronInfo = {
        key: s.key,
        label: s.label,
        agent: agentId,
        status: s.status,
        elapsed: fmtDuration(elapsed),
        elapsedMs: elapsed,
        totalTokens: s.totalTokens || 0,
        cost: s.estimatedCostUsd || 0,
      };

      if (timeoutLevel) {
        cronInfo.timeout = timeoutLevel;
        report.summary.timed_out++;
        report.issues.push({
          type: 'cron_timeout',
          severity: timeoutLevel,
          session: s.key,
          label: s.label,
          elapsed: cronInfo.elapsed,
        });
        report.recoverable.push({
          type: 'restart_cron',
          key: s.key,
          label: s.label,
          reason: `${timeoutLevel} 超时 (${cronInfo.elapsed})`,
        });
      }

      report.cron_tasks.push(cronInfo);
    }

    // 子会话分析
    if (s.childSessions?.length > 0) {
      for (const childKey of s.childSessions) {
        report.child_sessions.push({
          parent: s.key,
          child: childKey,
          status: s.status,
        });
      }
    }

    // 失败会话检测
    if (s.status === 'failed') {
      report.issues.push({
        type: 'session_failed',
        severity: 'critical',
        session: s.key,
        label: s.label || s.displayName,
        elapsed: fmtDuration(elapsed),
      });
      report.recoverable.push({
        type: 'investigate_failed',
        key: s.key,
        label: s.label || s.displayName,
        reason: `会话失败，运行时长 ${fmtDuration(s.runtimeMs || elapsed)}`,
      });
    }

    // 空闲检测
    if (s.status === 'running' && timeoutLevel === 'warning' && !timeoutLevel) {
      report.summary.idle++;
    }
  }

  // 更新状态机
  for (const s of sessions) {
    if (s.key && !state.tasks[s.key]) {
      state.tasks[s.key] = {
        id: s.key,
        status: s.status,
        label: s.label || s.displayName,
        firstSeen: new Date().toISOString(),
        lastSeen: new Date().toISOString(),
        timeouts: 0,
      };
    } else if (state.tasks[s.key]) {
      state.tasks[s.key].status = s.status;
      state.tasks[s.key].lastSeen = new Date().toISOString();
    }
  }

  // 标记消失的会话
  const currentKeys = new Set(sessions.map(s => s.key));
  for (const [key, task] of Object.entries(state.tasks)) {
    if (!currentKeys.has(key) && task.status === 'running') {
      task.status = 'disappeared';
      report.issues.push({
        type: 'session_disappeared',
        severity: 'warning',
        session: key,
        label: task.label,
        reason: '会话消失（可能崩溃或被杀死）',
      });
    }
  }

  saveState(state);
  return report;
}

function formatReport(report) {
  const lines = [];
  
  lines.push(`🔍 全量工作监控报告 (${report.timestamp})`);
  lines.push('═'.repeat(50));
  lines.push('');
  
  // 摘要
  const s = report.summary;
  lines.push(`📊 会话摘要: 总计 ${s.total} | 运行 ${s.running} | 完成 ${s.done} | 失败 ${s.failed} | 超时 ${s.timed_out}`);
  lines.push('');

  if (report.issues.length === 0) {
    lines.push('✅ 一切正常，无异常会话');
    lines.push('NO_REPLY');
    return lines.join('\n');
  }

  // 问题详情
  lines.push(`⚠️ 发现 ${report.issues.length} 个问题:`);
  lines.push('');
  for (const issue of report.issues) {
    const icon = issue.severity === 'critical' ? '🔴' : issue.severity === 'warning' ? '🟡' : '🔵';
    lines.push(`${icon} [${issue.severity.toUpperCase()}] ${issue.type}`);
    lines.push(`   会话: ${issue.session}`);
    if (issue.label) lines.push(`   标签: ${issue.label}`);
    if (issue.elapsed) lines.push(`   时长: ${issue.elapsed}`);
    if (issue.reason) lines.push(`   原因: ${issue.reason}`);
    lines.push('');
  }

  // 可恢复项
  if (report.recoverable.length > 0) {
    lines.push('🔄 建议恢复操作:');
    for (const r of report.recoverable) {
      lines.push(`   • ${r.type}: ${r.label} — ${r.reason}`);
    }
    lines.push('');
  }

  // Agent 状态
  lines.push('📋 Agent 状态:');
  for (const [agent, info] of Object.entries(report.agents)) {
    const status = info.running > 0 ? `🟢 ${info.running} running` : '⚪ idle';
    lines.push(`   ${agent}: ${info.sessions} 会话, ${status}`);
  }

  lines.push('');
  lines.push('═'.repeat(50));
  
  return lines.join('\n');
}

// ============================================================================
// 主入口
// ============================================================================

function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const mode = args.find(a => a.startsWith('--')) || '--all';

  const sessions = scanAllSessions();
  const report = analyzeSessions(sessions);

  if (jsonMode) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  console.log(formatReport(report));
}

main();

#!/usr/bin/env node
/**
 * Work Progress Check — 工作进度检查
 * 
 * 功能：
 * 1. 状态同步 — 发现/注册子代理任务
 * 2. 进度检查 — 增量输出追踪
 * 3. 待办事项 — 日常检查
 * 4. 终态 GC — 自动清理完成任务
 * 
 * 用法:
 *   node check-progress.js              # 全量检查
 *   node check-progress.js --json       # JSON 输出
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const STATE_FILE = path.join(WORKSPACE, 'skills/work-progress/state.json');
const TODAY = new Date().toISOString().slice(0, 10);
const NOW = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
const DAILY_PATH = path.join(WORKSPACE, 'memory/daily', TODAY + '.md');
const LOG_FILE = path.join(WORKSPACE, 'memory/error.md');

// ============================================================================
// 工具函数
// ============================================================================

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

function runOpenClaw(args) {
  try {
    return JSON.parse(execSync(`openclaw ${args} --json 2>/dev/null`, {
      encoding: 'utf8',
      timeout: 15000,
    }));
  } catch {
    return null;
  }
}

// ============================================================================
// 1. 状态同步
// ============================================================================

function syncState() {
  const data = runOpenClaw('sessions list --all-agents --active 30');
  const state = loadState();
  const sessions = data?.sessions || [];
  const issues = [];

  const currentKeys = new Set();

  for (const s of sessions) {
    if (!s.key) continue;
    currentKeys.add(s.key);

    if (!state.tasks[s.key]) {
      state.tasks[s.key] = {
        id: s.key,
        status: s.status,
        label: s.label || s.displayName,
        firstSeen: new Date().toISOString(),
        lastSeen: new Date().toISOString(),
        timeouts: 0,
      };
    } else {
      const prev = state.tasks[s.key].status;
      state.tasks[s.key].status = s.status;
      state.tasks[s.key].lastSeen = new Date().toISOString();

      if (prev === 'running' && (s.status === 'failed' || s.status === 'done')) {
        issues.push({
          type: 'task_completed',
          key: s.key,
          label: s.label,
          status: s.status,
        });
      }
    }
  }

  // 标记消失的会话
  for (const [key, task] of Object.entries(state.tasks)) {
    if (!currentKeys.has(key) && task.status === 'running') {
      task.status = 'disappeared';
      issues.push({
        type: 'session_disappeared',
        key,
        label: task.label,
      });
    }
  }

  saveState(state);
  return { sessions: sessions.length, issues };
}

// ============================================================================
// 2. 进度检查
// ============================================================================

function checkProgress() {
  const state = loadState();
  const issues = [];
  const now = Date.now();

  for (const [key, task] of Object.entries(state.tasks)) {
    if (task.status !== 'running') continue;

    const started = new Date(task.firstSeen).getTime();
    const elapsed = (now - started) / 1000 / 60; // 分钟

    if (elapsed > 30) {
      task.timeouts = (task.timeouts || 0) + 1;
      issues.push({
        type: 'timeout_warning',
        key,
        label: task.label,
        elapsed: Math.floor(elapsed) + '分钟',
        timeouts: task.timeouts,
      });
    }
  }

  saveState(state);
  return issues;
}

// ============================================================================
// 3. 待办事项检查
// ============================================================================

function checkTodos() {
  if (!fs.existsSync(DAILY_PATH)) {
    return { found: false, count: 0, todos: [] };
  }

  const content = fs.readFileSync(DAILY_PATH, 'utf8');
  const todos = content.match(/^- \[ \] .+/gm) || [];
  const done = content.match(/^- \[x\] .+/gm) || [];

  return {
    found: true,
    count: todos.length,
    done: done.length,
    todos: todos.map(t => t.replace(/^- \[ \] /, '')),
  };
}

// ============================================================================
// 4. 终态 GC
// ============================================================================

function gcTerminal() {
  const state = loadState();
  const terminal = new Set(['completed', 'failed', 'killed', 'disappeared', 'done']);
  const graceMs = 5 * 60 * 1000; // 5 分钟
  const now = Date.now();
  let cleaned = 0;

  for (const [key, task] of Object.entries(state.tasks)) {
    if (!terminal.has(task.status)) continue;

    if (!task.notified) {
      task.notified = true;
      task.notifiedAt = new Date().toISOString();
    } else if (task.notifiedAt) {
      const notifiedTime = new Date(task.notifiedAt).getTime();
      if (now - notifiedTime > graceMs) {
        if (!state.evicted) state.evicted = [];
        state.evicted.push({ id: key, evictedAt: new Date().toISOString() });
        delete state.tasks[key];
        cleaned++;
      }
    }
  }

  // 只保留最近 50 条 evicted
  if (state.evicted && state.evicted.length > 50) {
    state.evicted = state.evicted.slice(-50);
  }

  saveState(state);
  return cleaned;
}

// ============================================================================
// 主流程
// ============================================================================

function main() {
  const jsonMode = process.argv.includes('--json');

  const sync = syncState();
  const progress = checkProgress();
  const todos = checkTodos();
  const gc = gcTerminal();

  const hasIssues = sync.issues.length > 0 || progress.length > 0 || todos.count > 0;

  if (jsonMode) {
    console.log(JSON.stringify({
      timestamp: NOW,
      sync,
      progress,
      todos,
      gc,
    }, null, 2));
    return;
  }

  if (!hasIssues) {
    console.log('NO_REPLY');
    return;
  }

  const lines = [];
  lines.push(`🔍 工作进度检查 (${NOW})`);
  lines.push('═'.repeat(40));

  if (sync.issues.length > 0) {
    lines.push(`\n⚠️ ${sync.issues.length} 个状态变化:`);
    for (const issue of sync.issues) {
      lines.push(`  • [${issue.type}] ${issue.label || issue.key}`);
    }
  }

  if (progress.length > 0) {
    lines.push(`\n⏱️ ${progress.length} 个超时任务:`);
    for (const p of progress) {
      lines.push(`  • [${p.label}] 已运行 ${p.elapsed} (超时 ${p.timeouts} 次)`);
    }
  }

  if (todos.count > 0) {
    lines.push(`\n📋 ${todos.count} 个待办未完成:`);
    for (const t of todos.todos.slice(0, 5)) {
      lines.push(`  • ${t}`);
    }
  }

  if (gc > 0) {
    lines.push(`\n🧹 已清理 ${gc} 个终态任务`);
  }

  lines.push('');
  console.log(lines.join('\n'));
}

main();

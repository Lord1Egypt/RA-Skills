#!/usr/bin/env node
/**
 * Auto Recover — 超时任务自动恢复
 * 
 * 功能：
 * 1. 检查 state.json 中超时/消失的任务
 * 2. 记录到 error.md
 * 3. 建议恢复操作
 * 
 * 用法:
 *   node auto-recover.js
 *   node auto-recover.js --dry-run
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const STATE_FILE = path.join(WORKSPACE, 'skills/work-progress/state.json');
const LOG_FILE = path.join(WORKSPACE, 'memory/error.md');
const NOW = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { tasks: {}, evicted: [], lastCheck: null, version: 1 };
  }
}

function main() {
  const dryRun = process.argv.includes('--dry-run');
  const state = loadState();
  const tasks = state.tasks || {};

  const recoverable = [];

  for (const [key, task] of Object.entries(tasks)) {
    if (task.status === 'disappeared' || task.status === 'failed') {
      recoverable.push({ key, label: task.label, status: task.status });
    }
    if (task.status === 'running' && (task.timeouts || 0) >= 2) {
      recoverable.push({ key, label: task.label, status: 'timeout', timeouts: task.timeouts });
    }
  }

  if (recoverable.length === 0) {
    console.log('NO_REPLY');
    return;
  }

  console.log(`🔄 发现 ${recoverable.length} 个可恢复任务:`);
  console.log('');

  for (const r of recoverable) {
    console.log(`  • [${r.status}] ${r.label || r.key}`);

    if (!dryRun) {
      // 记录到 error.md
      const entry = `\n### [${NOW}] 任务异常 - ${r.label || r.key}\n状态: ${r.status}\n建议: 重新执行\n\n---\n`;
      fs.appendFileSync(LOG_FILE, entry);
    }
  }

  console.log('');
  if (dryRun) {
    console.log('[DRY RUN] 未执行恢复操作');
  } else {
    console.log('✅ 已记录到 error.md');
  }
}

main();

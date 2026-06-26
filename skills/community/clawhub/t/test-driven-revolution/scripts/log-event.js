#!/usr/bin/env node
/**
 * log-event.js - 事件日志写入工具
 * 追加式 JSONL 日志，方便审计和调试
 */

const fs = require('fs');
const path = require('path');

const LOGS_DIR = path.join(__dirname, '..', 'logs');
const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * 写入事件日志
 * @param {string} event - 事件类型
 * @param {object} data - 附加数据
 */
function logEvent(event, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    ...data
  };
  
  const line = JSON.stringify(entry) + '\n';
  fs.appendFileSync(EVENTS_LOG, line);
  
  return entry;
}

// 主程序
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('用法：');
  console.log('  node log-event.js <event> [key=value...]');
  console.log('');
  console.log('示例：');
  console.log('  node log-event.js task_created task_id=task-001 status=queued');
  console.log('  node log-event.js status_changed task_id=task-001 from=pending to=reviewing');
  console.log('');
  console.log('事件类型：');
  console.log('  task_created, task_activated, status_changed, review_completed,');
  console.log('  execution_started, execution_completed, execution_failed,');
  console.log('  force_unlock, task_unblocked, skill_packaged');
  process.exit(0);
}

const event = args[0];
const data = {};

// 解析 key=value 参数
for (let i = 1; i < args.length; i++) {
  const arg = args[i];
  const match = arg.match(/^([^=]+)=(.*)$/);
  if (match) {
    const [, key, value] = match;
    // 尝试解析为 JSON（数字、布尔值等）
    try {
      data[key] = JSON.parse(value);
    } catch {
      data[key] = value;
    }
  }
}

const entry = logEvent(event, data);
console.log('✅ 事件已记录：');
console.log(JSON.stringify(entry, null, 2));

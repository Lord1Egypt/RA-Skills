#!/usr/bin/env node
/**
 * Session History Share - 安装脚本
 * 
 * 自动完成以下操作：
 * 1. 复制 hook 文件到 ~/.openclaw/hooks/session-history-share/
 * 2. 在 openclaw.json 中注册 hook
 * 3. 创建 cron 定时任务
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const HOOK_DIR = path.join(process.env.HOME, '.openclaw', 'hooks', 'session-history-share');
const CONFIG_FILE = path.join(process.env.HOME, '.openclaw', 'openclaw.json');
const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname);
const HOOK_SRC = path.join(SCRIPT_DIR, '..', 'hook');

function log(msg) {
  console.log(`[install] ${msg}`);
}

function error(msg) {
  console.error(`[install] ERROR: ${msg}`);
  process.exit(1);
}

// 1. 复制 hook 文件
function installHook() {
  log('复制 hook 文件...');
  
  if (!fs.existsSync(HOOK_DIR)) {
    fs.mkdirSync(HOOK_DIR, { recursive: true });
  }
  
  const files = ['HOOK.md', 'handler.js'];
  for (const file of files) {
    const src = path.join(HOOK_SRC, file);
    const dst = path.join(HOOK_DIR, file);
    fs.copyFileSync(src, dst);
    log(`  ✓ ${file}`);
  }
}

// 2. 注册 hook 到 openclaw.json
function registerHook() {
  log('注册 hook 到 openclaw.json...');
  
  let config;
  try {
    const raw = fs.readFileSync(CONFIG_FILE, 'utf-8');
    config = JSON.parse(raw);
  } catch (err) {
    error(`无法读取 openclaw.json: ${err.message}`);
  }
  
  // 确保 hooks.internal.enabled
  if (!config.hooks) config.hooks = {};
  if (!config.hooks.internal) config.hooks.internal = { enabled: true };
  if (!config.hooks.internal.entries) config.hooks.internal.entries = {};
  
  config.hooks.internal.entries['session-history-share'] = { enabled: true };
  
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  log('  ✓ 已注册 session-history-share');
}

// 3. 创建 cron 定时任务
function createCronJob() {
  log('创建 cron 定时任务...');
  
  try {
    execSync(`openclaw cron add \
      --name "定时压缩活跃会话" \
      --cron "30 3 * * *" \
      --tz "Asia/Shanghai" \
      --session isolated \
      --message "执行以下步骤压缩所有活跃会话：\n\n1. 使用 sessions_list 获取所有活跃 session（排除 cron 和 subagent）\n2. 对每个 session 的 transcriptPath（JSONL 文件），执行以下步骤：\n   a. 使用 read 读取 JSONL 文件尾部（用 limit 从 offset 读取，不要读完整文件）\n   b. 从最后一条消息向前查找，找到最近的 compaction 事件（type=compaction）\n   c. 如果找到 compaction：提取 compaction.summary 字段的纯文本值\n   d. 如果没找到 compaction：提取最近 200 条 user/assistant 消息，生成简要摘要\n   e. 将摘要内容写入 .session_history/<safeSessionKey>/<safeSessionKey>-<YYYY-MM-DD>.md\n      - safeSessionKey 是把 sessionKey 中的冒号替换为下划线\n   f. 生成的摘要在**不丢失关键内容**的情况下尽可能的**简短**\n1. **文件内容只包含摘要正文纯文本，不要写任何 metadata header（不要 Session Key、Date、分隔线、标题等）**\n2. 每个 sessionKey 只保留最近 3 个存档文件，删除旧的\n3. 完成后回复 NO_REPLY"`, {
      stdio: 'inherit'
    });
    log('  ✓ Cron 任务已创建');
  } catch (err) {
    log(`  ⚠ Cron 创建失败，请手动创建`);
  }
}

// 主流程
try {
  installHook();
  registerHook();
  createCronJob();
  
  log('');
  log('安装完成！重启 OpenClaw 生效：');
  log('  openclaw gateway restart');
} catch (err) {
  error(`安装失败: ${err.message}`);
}

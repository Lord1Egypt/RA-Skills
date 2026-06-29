#!/usr/bin/env node
/**
 * Session History Share - 卸载脚本
 * 
 * 自动完成以下操作：
 * 1. 删除 hook 目录
 * 2. 从 openclaw.json 移除 hook 注册
 * 3. 删除 cron 定时任务
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const HOOK_DIR = path.join(process.env.HOME, '.openclaw', 'hooks', 'session-history-share');
const CONFIG_FILE = path.join(process.env.HOME, '.openclaw', 'openclaw.json');

function log(msg) {
  console.log(`[uninstall] ${msg}`);
}

function error(msg) {
  console.error(`[uninstall] ERROR: ${msg}`);
  process.exit(1);
}

// 1. 删除 hook 目录
function removeHook() {
  log('删除 hook 目录...');
  
  if (fs.existsSync(HOOK_DIR)) {
    fs.rmSync(HOOK_DIR, { recursive: true, force: true });
    log('  ✓ 已删除');
  } else {
    log('  ℹ hook 目录不存在');
  }
}

// 2. 从 openclaw.json 移除注册
function unregisterHook() {
  log('从 openclaw.json 移除 hook...');
  
  let config;
  try {
    const raw = fs.readFileSync(CONFIG_FILE, 'utf-8');
    config = JSON.parse(raw);
  } catch (err) {
    error(`无法读取 openclaw.json: ${err.message}`);
  }
  
  if (config.hooks?.internal?.entries?.['session-history-share']) {
    delete config.hooks.internal.entries['session-history-share'];
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
    log('  ✓ 已移除');
  } else {
    log('  ℹ hook 未注册');
  }
}

// 3. 删除 cron 定时任务
function removeCronJob() {
  log('删除 cron 定时任务...');
  
  try {
    const output = execSync('openclaw cron list', { encoding: 'utf-8' });
    const lines = output.split('\n');
    
    for (const line of lines) {
      if (line.includes('定时压缩活跃会话')) {
        const match = line.match(/^(\w+)\s+/);
        if (match) {
          execSync(`openclaw cron remove ${match[1]}`, { stdio: 'inherit' });
          log('  ✓ 已删除');
          return;
        }
      }
    }
    log('  ℹ 未找到对应 cron 任务');
  } catch (err) {
    log(`  ⚠ Cron 删除失败，请手动删除`);
  }
}

// 主流程
try {
  removeHook();
  unregisterHook();
  removeCronJob();
  
  log('');
  log('卸载完成！重启 OpenClaw 生效：');
  log('  openclaw gateway restart');
} catch (err) {
  error(`卸载失败: ${err.message}`);
}

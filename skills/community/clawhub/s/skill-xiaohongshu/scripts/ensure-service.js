#!/usr/bin/env node
/**
 * XHS MCP Service Manager
 * 检查、启动、停止 MCP 服务
 */

import { spawn, exec } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_ROOT = join(__dirname, '..');
const SERVICE_URL = process.env.XHS_SERVICE_URL || 'http://localhost:18060';

// 检查服务是否运行
async function checkService() {
  return new Promise((resolve) => {
    const req = http.request(`${SERVICE_URL}/health`, { method: 'GET', timeout: 2000 }, (res) => {
      if (res.statusCode === 200) {
        resolve(true);
      } else {
        resolve(false);
      }
    });

    req.on('error', () => resolve(false));
    req.on('timeout', () => {
      req.destroy();
      resolve(false);
    });
    req.end();
  });
}

// 启动服务
async function startService() {
  const isRunning = await checkService();
  if (isRunning) {
    console.log('✅ 服务已在运行');
    return true;
  }

  console.log('🚀 启动 XHS MCP 服务...');

  // 使用 spawn 启动后台服务
  const child = spawn('node', [join(__dirname, 'index.js')], {
    cwd: SKILL_ROOT,
    detached: true,
    stdio: 'ignore',
    env: { ...process.env }
  });

  child.unref();

  // 等待服务启动
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 1000));
    if (await checkService()) {
      console.log('✅ 服务启动成功');
      return true;
    }
  }

  console.error('❌ 服务启动超时');
  return false;
}

// 停止服务（Windows）
async function stopService() {
  return new Promise((resolve) => {
    exec('taskkill /F /IM node.exe /FI "WINDOWTITLE eq *xhs*"', (error) => {
      if (error) {
        console.log('⚠️ 未找到运行中的服务');
      } else {
        console.log('✅ 服务已停止');
      }
      resolve(!error);
    });
  });
}

// 主入口
const command = process.argv[2] || 'status';

switch (command) {
  case 'status':
    const running = await checkService();
    if (running) {
      console.log('✅ XHS MCP 服务运行中');
    } else {
      console.log('❌ XHS MCP 服务未运行');
    }
    process.exit(running ? 0 : 1);

  case 'start':
    const started = await startService();
    process.exit(started ? 0 : 1);

  case 'stop':
    await stopService();
    process.exit(0);

  case 'ensure':
    // 确保服务运行（用于技能自动调用）
    const ensured = await startService();
    process.exit(ensured ? 0 : 1);

  default:
    console.log(`用法: node ensure-service.js [status|start|stop|ensure]`);
    process.exit(1);
}

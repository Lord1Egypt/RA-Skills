#!/usr/bin/env node

/**
 * OpenClaw 健康检查脚本
 */

import http from 'http';
import fs from 'fs/promises';

const CONFIG = {
  gateway: { host: 'localhost', port: 18789, path: '/health', timeout: 5000 }
};

// 检查网关
async function checkGateway() {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: CONFIG.gateway.host,
      port: CONFIG.gateway.port,
      path: CONFIG.gateway.path,
      method: 'GET',
      timeout: CONFIG.gateway.timeout
    }, (res) => {
      if (res.statusCode === 200) {
        resolve({ status: 'ok', message: 'Gateway is running' });
      } else {
        resolve({ status: 'error', message: `HTTP ${res.statusCode}` });
      }
    });

    req.on('error', () => resolve({ status: 'error', message: 'Connection failed' }));
    req.on('timeout', () => { req.destroy(); resolve({ status: 'error', message: 'Timeout' }); });
    req.end();
  });
}

// 检查磁盘
async function checkDisk() {
  try {
    const stats = await fs.statfs(process.cwd());
    const free = (stats.bfree * stats.bsize / 1024 / 1024 / 1024).toFixed(2);
    return { status: 'ok', message: `${free} GB free` };
  } catch (e) {
    return { status: 'error', message: e.message };
  }
}

// 检查内存
async function checkMemory() {
  try {
    const used = process.memoryUsage();
    return { status: 'ok', message: `${(used.heapUsed / 1024 / 1024).toFixed(2)} MB used` };
  } catch (e) {
    return { status: 'error', message: e.message };
  }
}

// 主函数
async function main() {
  console.log('\n🔍 OpenClaw Health Check\n');
  console.log('=' .repeat(40));

  const checks = [
    { name: 'Gateway', fn: checkGateway },
    { name: 'Disk', fn: checkDisk },
    { name: 'Memory', fn: checkMemory }
  ];

  let allOk = true;

  for (const check of checks) {
    process.stdout.write(`${check.name}... `);
    const result = await check.fn();
    
    if (result.status === 'ok') {
      console.log(`✅ OK (${result.message})`);
    } else {
      console.log(`❌ ERROR: ${result.message}`);
      allOk = false;
    }
  }

  console.log('=' .repeat(40));
  console.log(allOk ? '\n✅ All healthy!' : '\n⚠️  Some issues found');
  process.exit(allOk ? 0 : 1);
}

main();

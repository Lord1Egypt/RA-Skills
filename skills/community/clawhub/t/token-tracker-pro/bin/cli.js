#!/usr/bin/env node

// Token Tracker 全局命令入口
const { execSync } = require('child_process');
const path = require('path');

// 获取 token-tracker CLI 的路径
const cliPath = path.join(__dirname, '..', 'token-tracker-cli.ts');

// 获取所有参数
const args = process.argv.slice(2);

// 执行 CLI 命令
try {
  execSync(`npx tsx ${cliPath} ${args.join(' ')}`, {
    stdio: 'inherit',
    cwd: __dirname
  });
} catch (error) {
  process.exit(1);
}

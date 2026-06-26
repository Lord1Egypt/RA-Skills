#!/usr/bin/env node
/**
 * Work Progress Skill - 安装脚本
 * 用法：node scripts/install.js
 *
 * 原为 install.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = path.join(__dirname, '..');
const WORKSPACE = path.join(process.env.HOME, '.openclaw', 'workspace');

console.log('🔧 安装 work-progress 技能...');
console.log('================================\n');

// 创建必要的目录
const dirs = [
  path.join(WORKSPACE, 'memory', 'daily'),
  path.join(WORKSPACE, 'memory', 'weekly'),
];

for (const dir of dirs) {
  fs.mkdirSync(dir, { recursive: true });
  console.log(`✅ ${path.relative(WORKSPACE, dir)}/`);
}

console.log('\n🔧 安装完成！');
console.log('请确认 openclaw cron list 中包含 work-progress 相关定时任务');

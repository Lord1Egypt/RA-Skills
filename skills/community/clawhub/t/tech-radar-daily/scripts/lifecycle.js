#!/usr/bin/env node

/**
 * 技能生命周期管理
 */

const fs = require('fs');
const path = require('path');

// 技能安装时
async function onInstall() {
  console.log('📦 安装 Tech Radar Daily...');
  
  // 确保目录存在
  const dirs = ['data', 'logs', 'logs/daily'];
  dirs.forEach(dir => {
    const fullPath = path.join(__dirname, '..', dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      console.log(` ✅ 创建目录：${dir}`);
    }
  });
  
  // 初始化数据文件
  const seenReposPath = path.join(__dirname, '../data/seen_repos.json');
  if (!fs.existsSync(seenReposPath)) {
    fs.writeFileSync(seenReposPath, '{}');
    console.log(' ✅ 初始化去重数据库');
  }
  
  console.log('✅ 安装完成！');
}

// 技能卸载时
async function onUninstall() {
  console.log('🗑️ 卸载 Tech Radar Daily...');
  // 保留数据，只是提示
  console.log(' ℹ️ 数据文件已保留在 data/ 目录');
}

// 根据命令行参数执行
const command = process.argv[2];
if (command === 'install') {
  onInstall();
} else if (command === 'uninstall') {
  onUninstall();
}

module.exports = { onInstall, onUninstall };

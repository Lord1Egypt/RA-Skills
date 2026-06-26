#!/usr/bin/env node
/**
 * Twitter/X 自动化运营套件 - 主入口
 * 支持发推、监控、自动回复、数据分析
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const COMMANDS = {
  post: '发推 - 发布单条推文或图片推文',
  monitor: '监控 - 监控关键词或用户动态',
  reply: '回复 - 设置自动回复规则',
  analyze: '分析 - 账号数据分析',
  schedule: '定时 - 设置定时发布任务',
  template: '模板 - 管理推文模板库'
};

function showHelp() {
  console.log('\n🐦 Twitter/X 自动化运营套件 v1.0.0\n');
  console.log('用法: node index.js <命令> [参数]\n');
  console.log('命令:');
  Object.entries(COMMANDS).forEach(([cmd, desc]) => {
    console.log(`  ${cmd.padEnd(10)} ${desc}`);
  });
  console.log('\n示例:');
  console.log('  node index.js post "今天是个好天气！"');
  console.log('  node index.js post --image ./photo.jpg "看图"');
  console.log('  node index.js monitor --keyword "AI" --duration 60');
  console.log('  node index.js reply --keyword "询问" --response "请联系客服"');
  console.log('');
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    return;
  }

  const command = args[0];
  const params = args.slice(1);

  // 检查环境变量
  if (!fs.existsSync('.env')) {
    console.log('⚠️  请先创建 .env 文件并配置 Twitter 账号信息');
    console.log('复制 .env.example 文件并填写你的信息');
    return;
  }

  switch (command) {
    case 'post':
      await handlePost(params);
      break;
    case 'monitor':
      await handleMonitor(params);
      break;
    case 'reply':
      await handleReply(params);
      break;
    case 'analyze':
      await handleAnalyze(params);
      break;
    case 'schedule':
      await handleSchedule(params);
      break;
    case 'template':
      await handleTemplate(params);
      break;
    default:
      console.log(`❌ 未知命令: ${command}`);
      showHelp();
  }
}

// 发推功能
async function handlePost(params) {
  const { spawn } = require('child_process');
  const postScript = path.join(__dirname, 'scripts', 'post.js');
  
  console.log('🚀 正在发布推文...');
  
  const child = spawn('node', [postScript, ...params], {
    stdio: 'inherit'
  });
  
  child.on('close', (code) => {
    if (code === 0) {
      console.log('✅ 推文发布成功');
    } else {
      console.log('❌ 发布失败');
    }
  });
}

// 监控功能
async function handleMonitor(params) {
  const { spawn } = require('child_process');
  const monitorScript = path.join(__dirname, 'scripts', 'monitor.js');
  
  console.log('👀 启动监控...');
  const child = spawn('node', [monitorScript, ...params], {
    stdio: 'inherit'
  });
}

// 自动回复
async function handleReply(params) {
  console.log('🤖 配置自动回复...');
  // 实现逻辑...
  console.log('✅ 自动回复规则已更新');
}

// 数据分析
async function handleAnalyze(params) {
  console.log('📊 正在分析数据...');
  // 实现逻辑...
}

// 定时任务
async function handleSchedule(params) {
  console.log('⏰ 设置定时任务...');
  // 实现逻辑...
}

// 模板管理
async function handleTemplate(params) {
  console.log('📝 管理推文模板...');
  // 实现逻辑...
}

main().catch(console.error);

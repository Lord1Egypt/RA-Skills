#!/usr/bin/env node

/**
 * Token Tracker Global CLI
 * Global command for easy token tracking
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const SCRIPT_DIR = path.dirname(__filename);

/**
 * Execute command and return output
 */
function executeCommand(command) {
  try {
    return execSync(command, {
      cwd: SCRIPT_DIR,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
  } catch (error) {
    console.error('执行命令失败:', error.message);
    process.exit(1);
  }
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
📊 Token Tracker - Global CLI

Usage:
  token-tracker [command] [options]

Commands:
  today           查看今日 Token 消耗统计
  w / week        查看本周 Token 消耗统计
  a / total       查看累计 Token 消耗统计
  h / history     查看历史记录
  s / save        获取节省 Token 的建议
  export          导出数据为 CSV/JSON/Markdown 格式
  i / interactive 进入交互式菜单
  help            显示帮助信息

Options:
  -h, --help      显示帮助信息
  -v, --version   显示版本信息

Examples:
  token-tracker today
  token-tracker w
  token-tracker a
  token-tracker h
  token-tracker s
  token-tracker i

Quick Aliases:
  t → today
  w → week
  a → total
  h → history
  s → save
  i → interactive

Global Install:
  npm install -g token-tracker

Or use npx:
  npx token-tracker today
`);
}

/**
 * Show version information
 */
function showVersion() {
  const packageJson = JSON.parse(
    fs.readFileSync(path.join(SCRIPT_DIR, 'package.json'), 'utf8')
  );
  console.log(`Token Tracker v${packageJson.version}`);
  console.log('Global CLI for OpenClaw token tracking');
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  // Show help if no command or help flag
  if (!command || command === 'help' || command === '-h' || command === '--help') {
    showHelp();
    return;
  }

  // Show version if version flag
  if (command === 'version' || command === '-v' || command === '--version') {
    showVersion();
    return;
  }

  // Map commands to npm scripts
  const commandMap = {
    'today': 'token:today',
    'w': 'token:w',
    'week': 'token:w',
    'a': 'token:a',
    'total': 'token:a',
    'h': 'token:h',
    'history': 'token:h',
    's': 'token:s',
    'save': 'token:s',
    'i': 'token:i',
    'interactive': 'token:i',
    'cleanup': 'token:cleanup',
    'reset': 'token:reset',
    'export': 'token:export'
  };

  const npmScript = commandMap[command];

  if (!npmScript) {
    console.error(`未知命令: ${command}`);
    console.log('使用 "token-tracker help" 查看帮助信息');
    process.exit(1);
  }

  // Execute the command
  const commandOutput = executeCommand(`npm run ${npmScript}`);

  // Print output
  console.log(commandOutput);

  // Exit with appropriate code
  process.exit(0);
}

// Run main function
if (require.main === module) {
  main();
}

module.exports = { main, showHelp, showVersion };

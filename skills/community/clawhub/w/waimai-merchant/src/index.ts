#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import { registerCommands } from './commands';
import { getDataDir, closeDatabase } from './db';

const program = new Command();

program
  .name('waimai-merchant')
  .description('外卖商家管理 CLI - 支持商家注册、商品管理、价格修改和配送时间设置')
  .version('1.0.0');

// 注册所有命令
registerCommands(program);

// 数据目录命令
program
  .command('data')
  .description('查看数据存储位置')
  .action(() => {
    console.log(chalk.bold('\n📁 数据存储位置\n'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log(getDataDir());
    console.log(chalk.gray('─'.repeat(50)));
  });

// 处理未捕获的错误
process.on('exit', () => {
  closeDatabase();
});

process.on('SIGINT', () => {
  closeDatabase();
  process.exit(0);
});

process.on('SIGTERM', () => {
  closeDatabase();
  process.exit(0);
});

// 解析命令行参数
program.parse();

// 如果没有提供命令，显示帮助
if (!process.argv.slice(2).length) {
  program.outputHelp();
}

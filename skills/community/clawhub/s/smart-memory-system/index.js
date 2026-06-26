#!/usr/bin/env node
/**
 * Smart Memory System - 主入口文件
 * 检索增强智能记忆系统 for OpenClaw
 */

const fs = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

console.log(`
🧠 Smart Memory System v1.0.0
===============================
检索增强智能记忆系统 for OpenClaw

功能特性：
• 智能语义搜索 (80% token减少)
• 对话上下文增强
• 记忆自动组织管理
• 实时性能优化
`);

// 加载配置
const configPath = path.join(__dirname, 'config/smart_memory.json');
let config = {};
try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (error) {
    console.error('❌ 无法加载配置文件:', error.message);
    process.exit(1);
}

// 命令行接口
const argv = yargs(hideBin(process.argv))
    .scriptName('smart-memory')
    .usage('🧠 $0 <命令> [选项]')
    .command('init', '初始化智能记忆系统', {}, () => {
        console.log('🚀 初始化智能记忆系统...');
        require('./scripts/init').initialize();
    })
    .command('load', '加载现有记忆到索引', {}, () => {
        console.log('📚 加载记忆文件...');
        require('./scripts/loader').loadMemories();
    })
    .command('search <query>', '语义搜索记忆', {}, (argv) => {
        console.log(`🔍 搜索: "${argv.query}"`);
        require('./scripts/searcher').search(argv.query);
    })
    .command('enhance <query>', '增强对话上下文', {}, (argv) => {
        console.log(`🧠 增强对话: "${argv.query}"`);
        require('./scripts/enhancer').enhance(argv.query);
    })
    .command('status', '显示系统状态', {}, () => {
        console.log('📊 系统状态:');
        require('./scripts/monitor').showStatus();
    })
    .command('test', '运行系统测试', {}, () => {
        console.log('🧪 运行系统测试...');
        require('./scripts/tester').runTests();
    })
    .command('optimize', '优化记忆索引', {}, () => {
        console.log('⚡ 优化记忆索引...');
        require('./scripts/optimizer').optimize();
    })
    .command('backup', '备份系统数据', {}, () => {
        console.log('💾 备份系统数据...');
        require('./scripts/backup').backup();
    })
    .command('restore', '恢复系统数据', {}, () => {
        console.log('🔄 恢复系统数据...');
        require('./scripts/restore').restore();
    })
    .command('clean', '清理缓存文件', {}, () => {
        console.log('🧹 清理缓存文件...');
        require('./scripts/cleaner').clean();
    })
    .option('verbose', {
        alias: 'v',
        type: 'boolean',
        description: '详细输出模式'
    })
    .option('config', {
        alias: 'c',
        type: 'string',
        description: '自定义配置文件路径'
    })
    .demandCommand(1, '❌ 需要指定一个命令')
    .help()
    .alias('help', 'h')
    .version(config.version || '1.0.0')
    .alias('version', 'V')
    .epilogue(`
📖 更多信息:
• 文档: https://github.com/openclaw-community/smart-memory-system
• 问题: https://github.com/openclaw-community/smart-memory-system/issues
• 社区: https://discord.gg/openclaw

💡 示例:
  $ smart-memory search "OpenClaw配置"
  $ smart-memory enhance "如何优化记忆系统"
  $ smart-memory status
    `)
    .argv;

// 如果没有命令被处理，显示帮助
if (!argv._[0]) {
    yargs.showHelp();
    process.exit(0);
}
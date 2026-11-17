#!/usr/bin/env node
/**
 * zhihu.js — 知乎自动化 Skill 统一 CLI 入口
 *
 * 用法:
 *   node zhihu.js --help              # 帮助信息
 *   node zhihu.js --version           # 版本信息
 *   node zhihu.js setup               # 首次配置引导
 *   node zhihu.js publish article ... # 发布文章
 *   node zhihu.js publish thought ... # 发布想法
 *   node zhihu.js answer ...          # 回答问题
 *   node zhihu.js ask ...             # 提问
 *   node zhihu.js interact ...        # 互动
 *   node zhihu.js extract ...         # 数据提取
 *   node zhihu.js hot-list            # 热榜
 *   node zhihu.js search ...          # 搜索
 *   node zhihu.js cookie-check        # Cookie 检测
 *   node zhihu.js export-cookie       # 导出 Cookie
 *   node zhihu.js smoke-test          # 冒烟测试
 *   node zhihu.js e2e-test            # 端到端集成测试
 *
 * P2-5: 统一 CLI 入口
 *
 * @module zhihu-cli
 */

import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { cliLog } from './scripts/zhihu-logger.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkg = JSON.parse(readFileSync(resolve(__dirname, 'package.json'), 'utf-8'));

/**
 * @typedef {object} CommandDef
 * @property {string} desc - 描述
 * @property {(args: string[]) => Promise<void>} runner - 执行函数
 */

/** @type {Record<string, CommandDef>} 命令注册表 */
const COMMANDS = {
  'setup':         { desc: '首次配置引导',          runner: () => import('./scripts/setup.js').then(m => m.main()) },
  'publish':       { desc: '发布文章/想法',          runner: (args) => import('./scripts/zhihu-publish.js').then(m => {
    const type = args[0];
    if (!type || !['article', 'thought'].includes(type)) throw new Error('用法: node zhihu.js publish <article|thought> [选项]');
    return m.main(type, args.slice(1));
  })},
  'answer':        { desc: '回答问题',               runner: (args) => import('./scripts/zhihu-answer.js').then(m => m.main(args)) },
  'ask':           { desc: '提问',                   runner: (args) => import('./scripts/zhihu-ask.js').then(m => m.main(args)) },
  'interact':      { desc: '点赞/评论/关注',          runner: (args) => import('./scripts/zhihu-interact.js').then(m => m.main(args)) },
  'extract':       { desc: '数据提取 (热榜/搜索/用户)', runner: (args) => import('./scripts/zhihu-extract.js').then(m => m.main(args)) },
  'hot-list':      { desc: '获取热榜',               runner: () => import('./scripts/zhihu-extract.js').then(m => m.main(['--type', 'hot-list'])) },
  'search':        { desc: '搜索内容',               runner: (args) => import('./scripts/zhihu-extract.js').then(m => m.main(['--type', 'search', '--query', args.join(' ')])) },
  'cookie-check':  { desc: '检查 Cookie 有效期',     runner: () => import('./tests/cookie-check.js').then(m => m.main ? m.main() : null) },
  'export-cookie': { desc: '导出/刷新 Cookie',       runner: () => import('./scripts/zhihu-export-cookie.js').then(m => m.main()) },
  'smoke-test':    { desc: '选择器冒烟测试',         runner: () => import('./tests/smoke-test.js').then(m => m.runSmokeTests()) },
  'e2e-test':      { desc: '端到端集成测试',          runner: () => {
    process.env.ZHIHU_TEST_MODE = 'sandbox';
    return import('./tests/e2e-test.js').then(m => m.main ? m.main() : null);
  }},
};

/**
 * 显示帮助信息
 * @returns {void}
 */
function showHelp() {
  console.log(`\n🤖 知乎自动化 Skill v${pkg.version}`);
  console.log('━'.repeat(50));
  console.log('\n用法: node zhihu.js <命令> [选项]\n');
  console.log('命令列表:');
  const maxLen = Math.max(...Object.keys(COMMANDS).map(c => c.length));
  for (const [cmd, info] of Object.entries(COMMANDS)) {
    console.log(`  ${cmd.padEnd(maxLen + 2)} ${info.desc}`);
  }
  console.log('\n选项:');
  console.log('  --help, -h     显示帮助');
  console.log('  --version, -v  显示版本');
  console.log('\n示例:');
  console.log('  node zhihu.js setup');
  console.log('  node zhihu.js publish article --title "我的文章" --content-file article.md');
  console.log('  node zhihu.js publish thought --content "今天天气真好"');
  console.log('  node zhihu.js hot-list --limit 5');
  console.log('  node zhihu.js cookie-check');
  console.log('');
  process.exit(0);
}

/**
 * CLI 主入口
 * @returns {Promise<void>}
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    return showHelp();
  }
  if (args[0] === '--version' || args[0] === '-v') {
    console.log(`v${pkg.version}`);
    return process.exit(0);
  }

  const command = args[0];
  const commandArgs = args.slice(1);
  const cmd = COMMANDS[command];

  if (!cmd) {
    cliLog.error(`未知命令: "${command}"`);
    console.error('   运行 node zhihu.js --help 查看可用命令');
    process.exit(1);
  }

  try {
    await cmd.runner(commandArgs);
  } catch (err) {
    cliLog.error('执行失败', err);
    process.exit(1);
  }
}

main();

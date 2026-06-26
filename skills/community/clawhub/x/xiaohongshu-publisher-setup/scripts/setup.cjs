#!/usr/bin/env node
/**
 * 小红书发布团队 - OpenClaw 部署工具
 * 部署 2 个小红书专属 Agent（灵格/星阑）+ xhs_publish.cjs 脚本
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const TEAM_NAME = 'workspace-xiaohongshu-publisher';
const OPENCLAW_DIR = process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw');
const TEAM_DIR = path.join(OPENCLAW_DIR, TEAM_NAME);
const SCRIPT_DIR = __dirname;
const TEMPLATE_DIR = path.join(SCRIPT_DIR, '..', 'templates');

const AGENTS = [
  { id: 'lingge',  name: '灵格', label: '灵格-小红书排版设计师', desc: '小红书排版设计师 - XHS格式排版与内容包生成' },
  { id: 'xinglan', name: '星阑', label: '星阑-小红书运营发布师', desc: '小红书运营发布师 - 自动化发布与数据分析' },
];

function runCommand(args) {
  try {
    return { code: 0, output: execSync(args.join(' '), { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'], shell: true }) };
  } catch (e) {
    return { code: e.status || 1, output: e.stderr || e.stdout || e.message };
  }
}

function main() {
  console.log('=========================================');
  console.log('  小红书发布团队 - OpenClaw 部署工具');
  console.log('=========================================\n');

  // 1. 环境检查
  if (runCommand(['openclaw', '--version']).code !== 0) {
    console.log('❌ 未检测到 OpenClaw');
    process.exit(1);
  }

  // 检查 content-creation 是否已部署
  const existing = runCommand(['openclaw', 'agents', 'list']).output || '';
  if (!existing.includes('mobai') || !existing.includes('jinshu')) {
    console.log('⚠️  内容创作团队未部署，请先运行 /content-creation');
    process.exit(1);
  }

  // 检查 Playwright 是否安装
  const playwrightCheck = runCommand(['node', '-e', '"require(\'playwright\')"']);
  if (playwrightCheck.code !== 0) {
    console.log('⚠️  Playwright 未安装（小红书发布需要浏览器自动化）');
    console.log('   请运行以下命令安装：');
    console.log('     npm install playwright');
    console.log('     npx playwright install chromium');
    console.log('   安装完成后重新运行 setup.cjs');
    process.exit(1);
  }

  console.log('✅ 环境检查通过\n');

  // 2. 部署 workspace 文件
  console.log('📁 部署 workspace 文件...');
  AGENTS.forEach((agent, i) => {
    console.log(`  → [${i + 1}/2] 部署 ${agent.label} (${agent.id})`);
    const destDir = path.join(TEAM_DIR, agent.id);
    fs.mkdirSync(destDir, { recursive: true });
    const srcDir = path.join(TEMPLATE_DIR, agent.id);
    if (!fs.existsSync(srcDir)) { console.log(`  ⚠️  模板目录不存在：${srcDir}`); return; }
    for (const f of fs.readdirSync(srcDir).filter(f => f.endsWith('.md'))) {
      const dest = path.join(destDir, f);
      if (!fs.existsSync(dest)) fs.copyFileSync(path.join(srcDir, f), dest);
    }
  });

  // 复制脚本到 workspace
  const scriptsDest = path.join(TEAM_DIR, 'scripts');
  fs.mkdirSync(scriptsDest, { recursive: true });
  const publishScript = path.join(SCRIPT_DIR, 'xhs_publish.cjs');
  const destScript = path.join(scriptsDest, 'xhs_publish.cjs');
  if (fs.existsSync(publishScript) && !fs.existsSync(destScript)) {
    fs.copyFileSync(publishScript, destScript);
  }
  console.log('  → 脚本已部署到 workspace/scripts/');

  // 创建 session 目录
  const sessionDir = path.join(TEAM_DIR, '.session');
  fs.mkdirSync(sessionDir, { recursive: true });
  console.log('  → session 目录已创建');

  // 3. 注册 Agent
  console.log('\n⚙️  注册 Agent...');
  for (const agent of AGENTS) {
    if (existing.includes(agent.id)) {
      console.log(`  → ${agent.id} 已存在，跳过`);
    } else {
      const { code, output } = runCommand([
        'openclaw', 'agents', 'add', agent.id,
        '--name', `"${agent.name}"`,
        '--workspace', `"${path.join(TEAM_DIR, agent.id)}"`,
        '--description', `"${agent.desc}"`,
      ]);
      console.log(code === 0 ? `  → ${agent.id} 注册成功` : `  ⚠️  ${agent.id} 注册失败：${output.trim()}`);
    }
  }

  // 4. 完成
  console.log(`\n✅ 小红书发布团队部署完成！\n   团队目录：${TEAM_DIR}\n`);
  console.log('下一步：');
  console.log('  1. 初始化登录（扫码）：');
  console.log(`     node ${path.join(TEAM_DIR, 'scripts', 'xhs_publish.cjs')} login`);
  console.log('  2. 使用 /xiaohongshu-publish-workflow 启动小红书发布流水线');
}

main();

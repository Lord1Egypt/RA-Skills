#!/usr/bin/env node
/**
 * 微信发布团队 - OpenClaw 部署工具
 * 部署 2 个微信专属 Agent（画境/数澜）+ wechat_publish.cjs 脚本
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const TEAM_NAME = 'workspace-wechat-publisher';
const OPENCLAW_DIR = process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw');
const TEAM_DIR = path.join(OPENCLAW_DIR, TEAM_NAME);
const SCRIPT_DIR = __dirname;
const TEMPLATE_DIR = path.join(SCRIPT_DIR, '..', 'templates');

const AGENTS = [
  { id: 'huajing', name: '画境', label: '画境-视觉设计师', desc: '微信视觉设计师 - 封面设计与排版美化' },
  { id: 'shulan',  name: '数澜', label: '数澜-运营分析师', desc: '微信运营分析师 - API发布与数据分析' },
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
  console.log('  微信发布团队 - OpenClaw 部署工具');
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
  const publishScript = path.join(SCRIPT_DIR, 'wechat_publish.cjs');
  const destScript = path.join(scriptsDest, 'wechat_publish.cjs');
  if (fs.existsSync(publishScript) && !fs.existsSync(destScript)) {
    fs.copyFileSync(publishScript, destScript);
  }
  console.log('  → 脚本已部署到 workspace/scripts/');

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
  console.log(`\n✅ 微信发布团队部署完成！\n   团队目录：${TEAM_DIR}\n`);
  console.log('下一步：');
  console.log('  1. 配置微信 API 凭证（在部署 Skill 交互中完成）');
  console.log('  2. 使用 /wechat-publish-workflow 启动微信发布流水线');
}

main();

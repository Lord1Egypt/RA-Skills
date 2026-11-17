#!/usr/bin/env node
/**
 * setup.js — 首次配置引导脚本
 *
 * 一键完成：
 * 1. 检查运行环境 (Node.js / Playwright / Python)
 * 2. 安装依赖
 * 3. 生成加密密钥
 * 4. 引导登录知乎
 * 5. 验证配置
 *
 * P2-4 | UE-1
 *
 * @module setup
 */

import { execSync } from 'child_process';
import { existsSync, writeFileSync, readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';
import { setupLog } from './zhihu-logger.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
/** @type {string} 项目根目录 */
const ROOT = resolve(__dirname, '..');
const pkg = JSON.parse(readFileSync(resolve(ROOT, 'package.json'), 'utf-8'));

// ── 工具 ──────────────────────────────────

/**
 * 读取用户输入
 * @param {string} query - 提示文本
 * @returns {Promise<string>} 用户输入
 */
function rlQuestion(query) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(query, answer => { rl.close(); resolve(answer.trim()); }));
}

/**
 * 检查最低版本要求
 * @param {string} cmd - 命令路径
 * @param {string} label - 显示名称
 * @param {string} minVer - 最低版本
 * @returns {{ ok: boolean, version: string, required?: string }}
 */
function checkMinVersion(cmd, label, minVer) {
  try {
    const out = execSync(`${cmd} --version`, { encoding: 'utf-8', timeout: 5000 });
    const ver = out.trim().replace(/^v/i, '');
    const m = minVer.replace(/^[>=^~]+/, '');
    const vp = ver.split('.').map(Number);
    const mp = m.split('.').map(Number);
    for (let i = 0; i < Math.max(vp.length, mp.length); i++) {
      const a = vp[i] || 0, b = mp[i] || 0;
      if (a < b) return { ok: false, version: ver, required: minVer };
      if (a > b) break;
    }
    return { ok: true, version: ver };
  } catch {
    return { ok: false, version: '未安装', required: minVer };
  }
}

// ── 步骤状态 ──────────────────────────────

/** @type {number} */
let passed = 0;
/** @type {number} */
let failed = 0;
/** @type {number} */
let warnings = 0;

/**
 * 记录步骤结果
 * @param {string} name - 步骤名
 * @param {boolean} ok - 是否成功
 * @param {string} [detail=''] - 详情
 */
function step(name, ok, detail = '') {
  if (ok) { passed++; console.log(`  ✅ ${name}`); }
  else { failed++; console.log(`  ❌ ${name}${detail ? ': ' + detail : ''}`); }
}

/**
 * 记录警告
 * @param {string} name - 名称
 * @param {string} detail - 详情
 */
function warnx(name, detail) { warnings++; console.log(`  ⚠️  ${name}: ${detail}`); }

// ── 步骤 1: 环境检查 ──────────────────────

/**
 * 检查运行环境
 * @returns {Promise<void>}
 */
async function checkEnvironment() {
  console.log('\n📋 步骤 1/5: 环境检查\n');

  const nc = checkMinVersion('node', 'Node.js', '>=18.0.0');
  step('Node.js >= 18.0.0', nc.ok, `当前: ${nc.version}`);

  const np = checkMinVersion('npm', 'npm', '>=8.0.0');
  step('npm >= 8.0.0', np.ok, np.version);

  const pc = checkMinVersion('python3', 'Python 3', '>=3.8');
  if (pc.ok) step('Python 3 >= 3.8', true, pc.version);
  else warnx('Python 3', '未安装，zhihu_bot.py 桥接不可用');

  try {
    const pw = execSync('npx playwright --version', { encoding: 'utf-8', timeout: 10000 }).trim();
    step('Playwright 已安装', true, pw);
  } catch {
    warnx('Playwright', '将在下一步安装');
  }

  console.log(`\n  结果: ${passed} ✅ / ${failed} ❌ / ${warnings} ⚠️`);
  if (failed > 0) {
    console.error('  请先修复上述失败项后重试');
    process.exit(1);
  }
}

// ── 步骤 2: 安装依赖 ──────────────────────

/**
 * 安装项目依赖
 * @returns {Promise<void>}
 */
async function installDeps() {
  console.log('\n📋 步骤 2/5: 安装依赖\n');

  if (existsSync(resolve(ROOT, 'node_modules'))) {
    console.log('  ✅ node_modules 已存在');
  } else {
    console.log('  ⏳ npm install...');
    execSync('npm install', { cwd: ROOT, stdio: 'inherit', timeout: 120000 });
    console.log('  ✅ 依赖安装完成');
  }

  console.log('  ⏳ 安装 Playwright Chromium...');
  execSync('npx playwright install chromium', { cwd: ROOT, stdio: 'inherit', timeout: 120000 });
  console.log('  ✅ Playwright Chromium 安装完成');
  passed++;
}

// ── 步骤 3: 生成加密密钥 ──────────────────

/**
 * 设置加密密钥
 * @returns {Promise<void>}
 */
async function setupKey() {
  console.log('\n📋 步骤 3/5: 加密密钥配置\n');

  if (process.env.ZHIHU_COOKIE_KEY) {
    console.log('  ✅ 环境变量 ZHIHU_COOKIE_KEY 已设置');
    passed++;
    return;
  }

  const envPath = resolve(ROOT, '.env');
  if (existsSync(envPath) && readFileSync(envPath, 'utf-8').includes('ZHIHU_COOKIE_KEY=')) {
    console.log('  ✅ .env 文件中已配置');
    passed++;
    return;
  }

  try {
    const key = execSync('openssl rand -hex 32', { encoding: 'utf-8' }).trim();
    const content = [
      '# 知乎自动化 Skill 环境变量',
      '# 首次 setup 自动生成，可手动修改',
      '',
      `ZHIHU_COOKIE_KEY="${key}"`,
      '# 可选: 知乎 OpenAPI (zhihu_bot.py)',
      '# ZHIHU_APP_KEY=',
      '# ZHIHU_APP_SECRET=',
      '# 可选: 代理',
      '# ZHIHU_PROXY=',
      '# 可选: 沙箱模式 (sandbox / production)',
      '# ZHIHU_TEST_MODE=sandbox',
      '',
    ].join('\n');
    writeFileSync(envPath, content);
    setupLog.info('密钥已生成并保存到 .env');
    console.log(`  🔑 密钥: ${key}`);
    console.log('  💡 建议添加到 shell 配置:');
    console.log(`     echo 'export ZHIHU_COOKIE_KEY="${key}"' >> ~/.zshrc`);
    passed++;
  } catch (e) {
    setupLog.error('密钥生成失败', e);
    console.log('  请手动设置:');
    console.log('  export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"');
    failed++;
  }
}

// ── 步骤 4: 登录引导 ──────────────────────

/**
 * 引导用户登录知乎
 * @returns {Promise<void>}
 */
async function guideLogin() {
  console.log('\n📋 步骤 4/5: 登录知乎\n');
  console.log('  即将打开浏览器，请手动登录知乎。');
  console.log('  登录成功后 Cookie 将自动加密保存。\n');

  const answer = await rlQuestion('  是否继续？(y/n): ');
  if (answer.toLowerCase() !== 'y') {
    console.log('  ⏭️  跳过，可随时运行: node zhihu.js export-cookie');
    warnings++;
    return;
  }

  try {
    const { main: exportMain } = await import('./zhihu-export-cookie.js');
    await exportMain();
    passed++;
  } catch (err) {
    setupLog.error('登录失败', err);
    console.log('  可手动运行: node zhihu.js export-cookie');
    failed++;
  }
}

// ── 步骤 5: 验证配置 ──────────────────────

/**
 * 验证配置完整性
 * @returns {Promise<void>}
 */
async function verify() {
  console.log('\n📋 步骤 5/5: 验证配置\n');

  step('package.json 有效', !!pkg.name);
  step('Playwright 依赖已声明', !!pkg.dependencies?.playwright);

  const configFiles = ['config/selectors.json', 'config/api-endpoints.json', 'SKILL.md', 'zhihu.js', 'scripts/setup.js'];
  for (const f of configFiles) {
    step(`文件 ${f} 存在`, existsSync(resolve(ROOT, f)));
  }

  console.log('\n' + '━'.repeat(50));
  console.log(`📊 总计: ${passed} ✅ / ${failed} ❌ / ${warnings} ⚠️`);
  console.log('━'.repeat(50));

  if (failed === 0) {
    console.log('\n🎉 配置完成！可用的命令:');
    console.log('  node zhihu.js publish article --title "标题" --content "正文"');
    console.log('  node zhihu.js publish thought --content "想法内容"');
    console.log('  node zhihu.js hot-list');
    console.log('  node zhihu.js cookie-check');
    console.log('  node zhihu.js export-cookie');
  } else {
    console.log('\n⚠️ 有步骤失败，请根据提示修复后重试');
  }
}

// ── 主入口 ──────────────────────────────────

/**
 * 主入口
 * @returns {Promise<void>}
 */
async function main() {
  console.log('\n🤖 知乎自动化 Skill v' + pkg.version);
  console.log('首次配置引导');
  console.log('━'.repeat(50));

  await checkEnvironment();
  await installDeps();
  await setupKey();
  await guideLogin();
  await verify();
}

export { main };
if (process.argv[1] && (process.argv[1].endsWith('setup.js'))) main();

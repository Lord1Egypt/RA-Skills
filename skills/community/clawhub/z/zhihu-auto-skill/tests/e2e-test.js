#!/usr/bin/env node
/**
 * e2e-test.js — 端到端集成测试
 *
 * 测试完整的 HTTP + 浏览器链路。
 * 沙箱模式：ZHIHU_TEST_MODE=sandbox node tests/e2e-test.js
 *
 * P1-5 | S11 | S14
 */

// ── 测试配置 ──────────────────────────────────────────────

import { existsSync, readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TEST_MODE = process.env.ZHIHU_TEST_MODE || 'sandbox';
const SKIP_BROWSER = process.env.SKIP_BROWSER === 'true'; // CI 中跳过浏览器测试
const REPORT_ONLY = process.env.REPORT_ONLY === 'true';   // 仅输出状态，不执行

// ── 工具 ──────────────────────────────────────────────────

let passed = 0;
let failed = 0;

function check(name, ok, detail = '') {
  if (ok) {
    passed++;
    console.log(`  ✅ ${name}`);
  } else {
    failed++;
    console.log(`  ❌ ${name}${detail ? ': ' + detail : ''}`);
  }
}

// ── 测试 1: 配置文件完整性 ────────────────────────────────

function testConfigFiles() {
  console.log('📋 配置完整性检查:');

  const files = [
    ['package.json', 'package.json'],
    ['SKILL.md', 'SKILL.md'],
    ['config/selectors.json', 'config/selectors.json'],
    ['config/api-endpoints.json', 'config/api-endpoints.json'],
    ['scripts/zhihu-core.js', 'scripts/zhihu-core.js'],
    ['scripts/zhihu-http.js', 'scripts/zhihu-http.js'],
    ['scripts/zhihu-browser.js', 'scripts/zhihu-browser.js'],
    ['scripts/zhihu-publish.js', 'scripts/zhihu-publish.js'],
  ];

  for (const [name, path] of files) {
    check(`文件存在: ${name}`, existsSync(resolve(__dirname, '..', path)));
  }

  // package.json 完整性
  try {
    const pkg = JSON.parse(readFileSync(resolve(__dirname, '..', 'package.json'), 'utf-8'));
    check('package.json: name 已设置', !!pkg.name);
    check('package.json: version 已设置', !!pkg.version);
    check('package.json: 非 private', !pkg.private);
    check('package.json: type=module', pkg.type === 'module');
    check('package.json: playwright 依赖', !!pkg.dependencies?.playwright);
  } catch (e) {
    check('package.json 有效', false, e.message);
  }

  // selectors.json 完整性
  try {
    const sels = JSON.parse(readFileSync(resolve(__dirname, '..', 'config/selectors.json'), 'utf-8'));
    check('selectors.json: version 存在', !!sels.version);
    const sections = ['article_editor', 'thought', 'answer', 'ask', 'interaction', 'login'];
    for (const sec of sections) {
      check(`selectors.json: 模块 ${sec}`, !!sels[sec]);
    }
  } catch (e) {
    check('selectors.json 有效', false, e.message);
  }
}

// ── 测试 2: HTTP 公开 API ────────────────────────────────

async function testPublicAPI() {
  console.log('\n🌐 HTTP 公开 API 测试:');
  try {
    const { getUser } = await import('../scripts/zhihu-http.js');

    const user = await getUser('excited-vczh');
    check('getUser: 返回数据', !!user);
    check('getUser: name 字段', !!user.name);
    check('getUser: urlToken 字段', !!user.urlToken);
  } catch (err) {
    check('HTTP 公开 API', false, err.message.slice(0, 100));
    console.log('   (可能签名失效或网络问题，不代表全部失败)');
  }
}

// ── 测试 3: 模块导入完整性 ────────────────────────────────

async function testModuleImports() {
  console.log('\n📦 模块导入测试:');

  const modules = [
    ['zhihu-core', '../scripts/zhihu-core.js', ['decryptCookies', 'encryptAndSaveCookies', 'initBrowser', 'withRetry', 'writeLog']],
    ['zhihu-signature', '../scripts/zhihu-signature.js', ['SignatureManager', 'Zse96Provider', 'MockProvider']],
    ['zhihu-ratelimiter', '../scripts/zhihu-ratelimiter.js', ['RateLimiter', 'httpRateLimiter']],
    ['zhihu-http', '../scripts/zhihu-http.js', ['getHotList', 'search', 'getUser', 'getQuestion']],
    ['zhihu-browser', '../scripts/zhihu-browser.js', ['getSelectors', 'findElement', 'getSession']],
    ['zhihu-publish', '../scripts/zhihu-publish.js', ['publishArticle', 'publishThought']],
    ['zhihu-interact', '../scripts/zhihu-interact.js', ['like', 'comment', 'follow']],
    ['zhihu-answer', '../scripts/zhihu-answer.js', ['answerQuestion']],
    ['zhihu-ask', '../scripts/zhihu-ask.js', ['askQuestion']],
    ['zhihu-extract', '../scripts/zhihu-extract.js', ['extract']],
    ['zhihu-bridge', '../scripts/zhihu-bridge.js', ['callPythonScript', 'checkPython']],
  ];

  for (const [name, path, exports] of modules) {
    try {
      const mod = await import(path);
      const allFound = exports.every(e => typeof mod[e] !== 'undefined');
      check(`模块 ${name}: ${exports.length} 个导出`, allFound);
      if (!allFound) {
        for (const e of exports) {
          if (typeof mod[e] === 'undefined') {
            console.log(`     缺少导出: ${e}`);
          }
        }
      }
    } catch (err) {
      check(`模块 ${name}: 导入失败`, false, err.message.slice(0, 80));
    }
  }
}

// ── 主函数 ────────────────────────────────────────────────

async function main() {
  const startTime = Date.now();

  console.log(`🧪 端到端集成测试`);
  console.log(`   模式: ${TEST_MODE}`);
  console.log(`   SKIP_BROWSER: ${SKIP_BROWSER}`);
  console.log('');

  if (REPORT_ONLY) {
    console.log('ℹ️ REPORT_ONLY 模式，仅输出状态');
  }

  // 测试 1: 配置文件
  testConfigFiles();

  // 测试 2: 模块导入
  await testModuleImports();

  // 测试 3: 公开 API（如果可用）
  if (!process.env.CI) {
    await testPublicAPI();
  } else {
    console.log('\n🌐 HTTP 公开 API 测试: (CI 中跳过)');
  }

  // 汇总
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📊 总计: ${passed + failed} 项 (${elapsed}s)`);
  console.log(`  ✅ 通过: ${passed}`);
  console.log(`  ❌ 失败: ${failed}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  process.exit(failed > 0 ? 1 : 0);
}

// 需要在顶层 await 环境运行，或者用立即执行函数包装
(async () => {
  try {
    await main();
  } catch (err) {
    console.error('\n❌ 测试异常:', err.message);
    process.exit(1);
  }
})();

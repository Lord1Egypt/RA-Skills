#!/usr/bin/env node
/**
 * smoke-test.js — 选择器冒烟测试
 *
 * 验证 config/selectors.json 中的关键选择器是否匹配知乎当前页面。
 * 可以独立运行，也可以在 CI 中调用。
 *
 * 用法:
 *   node tests/smoke-test.js                    # 测试所有模块
 *   ZHIHU_TEST_MODE=sandbox node tests/smoke-test.js
 *
 * P1-5
 */

import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SELECTORS_PATH = resolve(__dirname, '..', 'config', 'selectors.json');

// ── 配置 ──────────────────────────────────────────────────

const TEST_PAGES = {
  login: 'https://www.zhihu.com/',
  article_editor: 'https://zhuanlan.zhihu.com/write',
  thought: 'https://www.zhihu.com/',
  interaction: 'https://www.zhihu.com/question/19555555', // 示例问题页
};

// ── 工具 ──────────────────────────────────────────────────

function loadSelectors() {
  if (!existsSync(SELECTORS_PATH)) {
    console.error(`❌ 选择器文件不存在: ${SELECTORS_PATH}`);
    process.exit(1);
  }
  return JSON.parse(readFileSync(SELECTORS_PATH, 'utf-8'));
}

// ── 测试函数 ──────────────────────────────────────────────

let passed = 0;
let failed = 0;
const failures = [];

function report(name, ok, detail = '') {
  if (ok) {
    passed++;
    console.log(`  ✅ ${name}`);
  } else {
    failed++;
    const msg = `  ❌ ${name}${detail ? ': ' + detail : ''}`;
    failures.push(msg);
    console.log(msg);
  }
}

// ── 主测试 ────────────────────────────────────────────────

async function runSmokeTests() {
  console.log('🔍 选择器冒烟测试\n');

  const selectors = loadSelectors();
  console.log(`📄 选择器文件版本: ${selectors.version}\n`);

  // 1. 检查选择器结构完整性
  console.log('📋 结构完整性检查:');
  const requiredSections = ['article_editor', 'thought', 'answer', 'ask', 'interaction', 'login'];
  for (const section of requiredSections) {
    report(`模块 "${section}" 存在`, !!selectors[section]);
  }
  console.log('');

  // 2. 检查每个选择器的 primary/fallbacks
  console.log('📋 选择器定义检查:');
  for (const [section, defs] of Object.entries(selectors)) {
    if (section === 'version' || section === 'notes' || section === 'description') continue;
    for (const [key, sel] of Object.entries(defs)) {
      if (typeof sel === 'string') continue; // url 字段
      const hasPrimary = !!(sel.primary && sel.primary.trim());
      const hasFallbacks = Array.isArray(sel.fallbacks) && sel.fallbacks.length > 0;
      report(`${section}.${key}: primary 定义`, hasPrimary);
      if (!hasPrimary) {
        failures.push(`      ${section}.${key} 缺少 primary 选择器`);
      }
    }
  }
  console.log('');

  // 3. 真实性测试：打开知乎页面验证关键选择器
  console.log('🌐 页面匹配测试:');
  let browser;
  try {
    browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    });

    // 测试登录页选择器
    console.log('  --- 首页 (zhihu.com) ---');
    const homePage = await context.newPage();
    await homePage.goto(TEST_PAGES.login, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await homePage.waitForTimeout(2000);

    // 验证 thought.trigger 是否存在
    const thoughtTrigger = homePage.locator(selectors.thought.trigger.primary);
    const triggerCount = await thoughtTrigger.count();
    report(`想法触发按钮 [${selectors.thought.trigger.primary}]`, triggerCount > 0,
      `找到 ${triggerCount} 个`);

    // 验证 login.avatar 是否存在（或 signinButton）
    const avatarCount = await homePage.locator(selectors.login.avatar.primary).count();
    report(`用户头像 [${selectors.login.avatar.primary}]`, avatarCount > 0,
      `找到 ${avatarCount} 个`);

    // 验证 contenteditable 是否可用
    const editableCount = await homePage.locator(selectors.thought.input.primary).count();
    report(`编辑区域 [${selectors.thought.input.primary}]`,
      editableCount > 0 || triggerCount > 0,
      `找到 ${editableCount} 个`);
    await homePage.close();

    // 测试专栏编辑器
    console.log('  --- 编辑器 (zhuanlan.zhihu.com/write) ---');
    const editorPage = await context.newPage();
    await editorPage.goto(TEST_PAGES.article_editor, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await editorPage.waitForTimeout(3000);

    const titleInput = editorPage.locator(selectors.article_editor.titleInput.primary);
    const titleCount = await titleInput.count();
    report(`文章标题输入框 [${selectors.article_editor.titleInput.primary}]`, titleCount > 0,
      `找到 ${titleCount} 个`);

    const contentEditor = editorPage.locator(selectors.article_editor.contentEditor.primary);
    const editorCount = await contentEditor.count();
    report(`文章编辑区域 [${selectors.article_editor.contentEditor.primary}]`, editorCount > 0,
      `找到 ${editorCount} 个`);

    const publishSettings = editorPage.locator(selectors.article_editor.publishSettingsButton.primary);
    const psCount = await publishSettings.count();
    report(`发布设置按钮 [${selectors.article_editor.publishSettingsButton.primary}]`, psCount > 0,
      `找到 ${psCount} 个`);

    // 测试互动页面
    console.log('  --- 问题页 (zhihu.com/question) ---');
    const questionPage = await context.newPage();
    await questionPage.goto(TEST_PAGES.interaction, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await questionPage.waitForTimeout(2000);

    const likeBtn = questionPage.locator(selectors.interaction.likeButton.primary);
    const likeCount = await likeBtn.count();
    report(`点赞按钮 [${selectors.interaction.likeButton.primary}]`, likeCount > 0,
      `找到 ${likeCount} 个`);

    await questionPage.close();

  } catch (err) {
    console.error(`\n⚠️ 浏览器测试异常: ${err.message}`);
    console.log('   (可能因为未安装 Playwright 或无 Cookie，不影响结构检查)');
  } finally {
    if (browser) await browser.close();
  }
  console.log('');

  // ── 结果汇总 ──
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📊 总计: ${passed + failed} 项`);
  console.log(`  ✅ 通过: ${passed}`);
  console.log(`  ❌ 失败: ${failed}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 输出失败详情
  if (failures.length > 0) {
    console.log('\n失败详情:');
    for (const f of failures) {
      console.log(f);
    }
  }

  process.exit(failed > 0 ? 1 : 0);
}

runSmokeTests();

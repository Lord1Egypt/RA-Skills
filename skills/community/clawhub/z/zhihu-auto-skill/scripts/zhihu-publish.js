#!/usr/bin/env node
/**
 * zhihu-publish.js — 知乎内容发布模块
 *
 * 支持：
 * - 发布专栏文章
 * - 发布想法
 *
 * CLI 用法:
 *   node scripts/zhihu-publish.js article --title "标题" --content "正文.md" [--draft] [--preview]
 *   node scripts/zhihu-publish.js thought --content "内容" [--image path] [--preview]
 *
 * I2 | I3
 *
 * @module zhihu-publish
 */

import { readFileSync } from 'fs';
import readline from 'readline';
import { getSession, navigateTo, clickElement, findElement, typeLikeHuman, markdownToZhihuHTML, humanDelay, sleep, withCrashRecovery, getSelectors } from './zhihu-browser.js';
import { publishLog } from './zhihu-logger.js';

// ──────────────────────────────────────────
// 进度反馈
// ──────────────────────────────────────────

/** @type {number} 总步骤数 */
const TOTAL_STEPS = 5;
/** @type {number} 当前步骤 */
let _currentStep = 0;

/**
 * 显示进度条步骤
 * @param {string} stepName - 步骤名称
 * @returns {void}
 */
function progress(stepName) {
  _currentStep++;
  const bar = [];
  for (let i = 1; i <= TOTAL_STEPS; i++) {
    bar.push(i <= _currentStep ? '━' : '─');
  }
  publishLog.info(`[${_currentStep}/${TOTAL_STEPS}] ${stepName}`);
  console.log(`  ┃${bar.join('')}┃ ${Math.round((_currentStep / TOTAL_STEPS) * 100)}%`);
}

/**
 * 重置进度计数器
 * @returns {void}
 */
function progressReset() {
  _currentStep = 0;
}

// ──────────────────────────────────────────
// 工具函数
// ──────────────────────────────────────────

/**
 * 沙箱模式检查：ZHIHU_TEST_MODE=sandbox 时，不实际发布到知乎，
 * 而是保存为本地草稿文件，用于测试发布流程而不污染线上环境。
 *
 * @param {'article'|'thought'} type - 发布类型
 * @param {{ title?: string, content: string, imagePath?: string }} params - 发布参数
 * @returns {Promise<{ status: string, file: string, title?: string }>} 沙箱结果
 */
async function saveAsLocalDraft(type, { title, content, imagePath }) {
  const { writeFile, mkdir } = await import('fs/promises');
  const path = await import('path');
  const draftDir = path.join(process.env.HOME, '.hermes', 'drafts');
  await mkdir(draftDir, { recursive: true });
  const ts = Date.now();
  const safeName = (title || 'draft').replace(/[^a-zA-Z0-9\u4e00-\u9fff_-]/g, '_').slice(0, 40);
  const draftFile = path.join(draftDir, `${safeName}-${ts}.md`);

  const body = [
    `# ${title || '沙箱测试 - 想法'}`,
    `> 类型: ${type === 'article' ? '文章' : '想法'}`,
    `> 沙箱草稿，未实际发布到知乎`,
    `> 创建时间: ${new Date().toISOString()}`,
    imagePath ? `> 配图: ${imagePath}` : '',
    '',
    content,
  ].filter(Boolean).join('\n');

  await writeFile(draftFile, body, 'utf-8');
  publishLog.info('沙箱模式: 内容已保存为本地草稿');
  publishLog.info(`  📄 ${draftFile}`);
  return { status: 'sandbox_draft', file: draftFile, title };
}

/**
 * 检查是否为沙箱模式
 * @returns {boolean}
 */
function isSandboxMode() {
  return process.env.ZHIHU_TEST_MODE === 'sandbox';
}

/**
 * 预览模式：显示内容并等待用户确认
 *
 * @param {'article'|'thought'} type - 发布类型
 * @param {{ title?: string, content: string, imagePath?: string }} params - 发布参数
 * @returns {Promise<boolean|string>} true = 确认发布，false = 取消，'draft' = 保存草稿
 */
async function confirmPublishPreview(type, { title, content, imagePath }) {
  console.log('\n📋 发布预览');
  console.log('═'.repeat(60));
  console.log(`类型: ${type === 'article' ? '文章' : '想法'}`);
  if (title) console.log(`标题: ${title}`);
  console.log(`内容长度: ${content.length} 字符`);
  if (imagePath) console.log(`配图: ${imagePath}`);
  console.log('─'.repeat(60));
  console.log('内容预览:');
  console.log(content.length > 500 ? content.substring(0, 500) + '...' : content);
  console.log('═'.repeat(60));
  console.log('');
  console.log('确认发布？');
  console.log('  y = 确认发布');
  console.log('  n = 取消（保存为草稿）');
  console.log('  q = 退出不保存');
  console.log('');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question('请选择 (y/n/q): ', (answer) => {
      rl.close();
      const a = answer.trim().toLowerCase();
      if (a === 'y') {
        publishLog.info('用户确认发布');
        resolve(true);
      } else if (a === 'n') {
        publishLog.info('用户选择保存为草稿');
        resolve('draft');
      } else {
        publishLog.info('用户取消发布');
        resolve(false);
      }
    });
  });
}

// ──────────────────────────────────────────
// 发布文章
// ──────────────────────────────────────────

/**
 * @typedef {object} PublishResult
 * @property {string} status - 状态 (published|draft_saved|cancelled|sandbox_draft)
 * @property {string} [url] - 发布后的 URL
 * @property {string} [title] - 文章标题
 */

/**
 * 发布专栏文章
 *
 * @param {{ title: string, content: string, draft?: boolean, preview?: boolean }} params - 文章参数
 * @returns {Promise<PublishResult>} 发布结果
 */
async function publishArticle({ title, content, draft = false, preview = false }) {
  progressReset();
  publishLog.info(`发布${draft ? '草稿' : '文章'}: ${title}`);

  // 🔒 沙箱模式：跳过实际发布，保存为本地草稿
  if (isSandboxMode()) {
    publishLog.info('沙箱模式已启用 — 不会实际发布到知乎');
    return await saveAsLocalDraft('article', { title, content });
  }

  // 预览模式：显示内容并等待确认
  if (preview) {
    const confirm = await confirmPublishPreview('article', { title, content });
    if (confirm === false) {
      return { status: 'cancelled', title };
    } else if (confirm === 'draft') {
      draft = true;
      publishLog.info('将保存为草稿...');
    }
  }

  return await withCrashRecovery(async () => {
    const { context, page } = await getSession();
    const selectors = getSelectors();
    const editor = selectors.article_editor;

    // [1/5] 导航到编辑器
    progress('导航到专栏编辑器');
    await navigateTo(page, editor.url);
    await humanDelay(3000, 4000);

    // [2/5] 填写标题
    progress('填写文章标题');
    const titleInput = page.locator(editor.titleInput.primary);
    if (await titleInput.count() > 0) {
      await titleInput.click();
      await sleep(300);
      await titleInput.fill(title);
      publishLog.info('  ✅ 标题已填写');
    } else {
      const titleEl = await findElement(page, editor.titleInput);
      if (titleEl) {
        await titleEl.click();
        await sleep(300);
        await titleEl.fill(title);
      }
    }
    await humanDelay(500, 1000);

    // [3/5] 填写正文
    progress('填写文章正文');
    const contentEl = await findElement(page, editor.contentEditor);
    if (contentEl) {
      await contentEl.click();
      await sleep(1500);
      
      // 方法1: ClipboardEvent paste（最快，~25ms）
      const pasted = await page.evaluate((text) => {
        const ed = document.querySelector('[contenteditable]');
        if (!ed) return false;
        ed.focus();
        try {
          const dt = new DataTransfer();
          dt.setData('text/plain', text);
          const ev = new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true });
          ed.dispatchEvent(ev);
          return true;
        } catch {
          return false;
        }
      }, content);
      
      if (pasted) {
        await sleep(500);
        publishLog.info('  ✅ 内容已批量粘贴');
      } else {
        publishLog.warn('批量粘贴不可用，回退到逐字输入');
        await page.keyboard.type(content, { delay: 0 });
        await sleep(500);
        publishLog.info('  ✅ 内容已通过键盘输入');
      }
    }

    if (draft) {
      publishLog.info('  ⏳ 文章已自动保存为草稿');
      return { status: 'draft_saved', title };
    }

    // [4/5] 打开发布设置
    progress('打开发布设置');
    const settingsBtn = page.locator(editor.publishSettingsButton.primary);
    await settingsBtn.waitFor({ timeout: 5000, state: 'visible' }).catch(() => {});
    if (await settingsBtn.isVisible().catch(() => false)) {
      await settingsBtn.click();
      publishLog.info('  ⏳ 发布设置弹窗已打开');
      await sleep(2000);
    }

    // [5/5] 点击发布
    progress('点击发布按钮');
    const confirmBtn = page.locator('button:has-text("发布")').last();
    await confirmBtn.waitFor({ timeout: 8000, state: 'visible' }).catch(() => {});
    if (await confirmBtn.isVisible().catch(() => false)) {
      await confirmBtn.click();
      await sleep(3000);
      const currentUrl = page.url();
      publishLog.info('文章已发布', { url: currentUrl, title });
      return { status: 'published', url: currentUrl, title };
    }

    throw new Error('未找到发布按钮，发布失败');
  }, 'publish_article');
}

// ──────────────────────────────────────────
// 发布想法
// ──────────────────────────────────────────

/**
 * 发布想法
 *
 * @param {{ content: string, imagePath?: string|null, preview?: boolean }} params - 想法参数
 * @returns {Promise<PublishResult>} 发布结果
 */
async function publishThought({ content, imagePath = null, preview = false }) {
  progressReset();
  publishLog.info('发布想法');

  // 🔒 沙箱模式：跳过实际发布，保存为本地草稿
  if (isSandboxMode()) {
    publishLog.info('沙箱模式已启用 — 不会实际发布到知乎');
    return await saveAsLocalDraft('thought', { content, imagePath });
  }

  // 预览模式：显示内容并等待确认
  if (preview) {
    const confirm = await confirmPublishPreview('thought', { content, imagePath });
    if (confirm === false) {
      return { status: 'cancelled', type: 'thought' };
    } else if (confirm === 'draft') {
      publishLog.info('想法将保存为草稿...');
      const fs = await import('fs/promises');
      const path = await import('path');
      const draftDir = path.join(process.env.HOME, '.hermes', 'drafts');
      await fs.mkdir(draftDir, { recursive: true });
      const draftFile = path.join(draftDir, `thought-${Date.now()}.txt`);
      await fs.writeFile(draftFile, content, 'utf-8');
      publishLog.info(`📝 想法已保存为本地草稿: ${draftFile}`);
      return { status: 'draft_saved', file: draftFile };
    }
  }

  return await withCrashRecovery(async () => {
    const { context, page } = await getSession();
    const selectors = getSelectors();
    const thought = selectors.thought;

    // [1/5] 导航到首页
    progress('导航到知乎首页');
    await navigateTo(page, 'https://www.zhihu.com/');
    await humanDelay(1500, 2500);

    // [2/5] 打开想法编辑框
    progress('打开想法编辑框');
    const triggerBtn = page.locator(thought.trigger.primary);
    const triggerCount = await triggerBtn.count();
    if (triggerCount > 0 && await triggerBtn.isVisible()) {
      await triggerBtn.click();
      publishLog.info('  ✅ 已点击"发想法"按钮');
      await humanDelay(2000, 3000);
    } else {
      const trigger = await findElement(page, thought.trigger);
      if (trigger) {
        await trigger.click();
        publishLog.info('  ✅ 已打开想法编辑框');
        await humanDelay(2000, 3000);
      } else {
        throw new Error('未找到想法触发按钮');
      }
    }

    // [3/5] 填写想法内容
    progress('填写想法内容');
    const editorSel = thought.input.primary;
    const editor = await page.locator(editorSel).first().waitFor({ timeout: 8000 }).catch(() => null);
    if (editor) {
      await editor.click();
      await sleep(500);
      try {
        await editor.fill(content);
      } catch {
        await editor.click();
        await page.keyboard.type(content, { delay: 30 });
      }
      await humanDelay(1000, 1500);
      publishLog.info('  ✅ 想法内容已填写');
    } else {
      // 直接注入文本
      await page.evaluate((text) => {
        const ed = document.querySelector('[contenteditable="true"]');
        if (ed) {
          ed.focus();
          document.execCommand('insertText', false, text);
        }
      }, content);
      await humanDelay(1000, 2000);
      publishLog.info('  ✅ 想法内容已通过注入填写');
    }

    // [4/5] (可选)上传图片
    if (imagePath) {
      progress('上传配图');
      const fileInput = await page.$('input[type="file"]');
      if (fileInput) {
        await fileInput.setInputFiles(imagePath);
        publishLog.info('图片已选择，等待上传...');
        await page.waitForTimeout(3000);
      }
    }

    // [5/5] 点击发布
    progress('点击发布按钮');
    await sleep(1000);
    const publishBtnLoc = page.locator('button:has-text("发布")').first();
    await publishBtnLoc.waitFor({ timeout: 10000, state: 'visible' }).catch(() => null);
    if (await publishBtnLoc.isVisible().catch(() => false)) {
      await publishBtnLoc.click();
      await sleep(3000);
      publishLog.info('想法已发布');
      return { status: 'published', type: 'thought' };
    }

    throw new Error('未找到发布按钮');
  }, 'publish_thought');
}

// ──────────────────────────────────────────
// CLI 入口
// ──────────────────────────────────────────

/**
 * CLI 主入口
 * @returns {void}
 */
function main() {
  const args = process.argv.slice(2);
  const type = args[0];

  if (!type || (type !== 'article' && type !== 'thought')) {
    publishLog.error('用法: node scripts/zhihu-publish.js <article|thought> [选项]');
    publishLog.error('');
    publishLog.error('文章:');
    publishLog.error('  node scripts/zhihu-publish.js article --title "标题" --content "正文" [--draft] [--preview]');
    publishLog.error('  node scripts/zhihu-publish.js article --title "标题" --content-file "path.md" [--preview]');
    publishLog.error('');
    publishLog.error('想法:');
    publishLog.error('  node scripts/zhihu-publish.js thought --content "内容" [--image "图片路径"] [--preview]');
    process.exit(1);
  }

  const options = {};
  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--title': options.title = args[++i]; break;
      case '--content': options.content = args[++i]; break;
      case '--content-file':
        options.content = readFileSync(args[++i], 'utf-8');
        break;
      case '--image': options.imagePath = args[++i]; break;
      case '--draft': options.draft = true; break;
      case '--preview': options.preview = true; break;
    }
  }

  if (!options.content) {
    publishLog.error('错误: 需要 --content 或 --content-file');
    process.exit(1);
  }

  if (type === 'article' && !options.title) {
    publishLog.error('错误: 文章需要 --title');
    process.exit(1);
  }

  const fn = type === 'article' ? publishArticle(options) : publishThought(options);
  fn.then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }).catch(err => {
    publishLog.error('发布失败', err);
    process.exit(1);
  });
}

if (import.meta.filename ? process.argv[1] === import.meta.filename : process.argv[1]?.endsWith('zhihu-publish.js')) {
  main();
}

export { publishArticle, publishThought };

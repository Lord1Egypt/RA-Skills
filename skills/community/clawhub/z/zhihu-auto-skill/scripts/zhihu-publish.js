#!/usr/bin/env node
/**
 * zhihu-publish.js — 知乎内容发布模块
 *
 * 支持：
 * - 发布专栏文章
 * - 发布想法
 *
 * CLI 用法:
 *   node scripts/zhihu-publish.js article --title "标题" --content "正文.md" [--draft]
 *   node scripts/zhihu-publish.js thought --content "内容" [--image path]
 *
 * I2 | I3
 */

import { readFileSync } from 'fs';
import { getSession, navigateTo, clickElement, findElement, typeLikeHuman, markdownToZhihuHTML, humanDelay, sleep, withCrashRecovery, getSelectors } from './zhihu-browser.js';

// ──────────────────────────────────────────
// 发布文章
// ──────────────────────────────────────────

async function publishArticle({ title, content, draft = false }) {
  console.log(`\n📝 发布${draft ? '草稿' : '文章'}: ${title}`);

  return await withCrashRecovery(async () => {
    const { context, page } = await getSession();
    const selectors = getSelectors();
    const editor = selectors.article_editor;

    // 导航到专栏编辑器
    await navigateTo(page, editor.url);
    await humanDelay(3000, 4000);

    // 填写标题（textarea）
    const titleInput = page.locator(editor.titleInput.primary);
    if (await titleInput.count() > 0) {
      await titleInput.click();
      await sleep(300);
      await titleInput.fill(title);
      console.log('✅ 标题已填写');
    } else {
      const titleEl = await findElement(page, editor.titleInput);
      if (titleEl) {
        await titleEl.click();
        await sleep(300);
        await titleEl.fill(title);
      }
    }
    await humanDelay(500, 1000);

    // 填写正文：批量粘贴（优先 ClipboardEvent，兜底 keyboard.type）
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
        // 等待 Draft.js 处理粘贴事件
        await sleep(500);
        console.log('✅ 内容已批量粘贴');
      } else {
        // 方法2: keyboard.type（慢但可靠）
        console.log('⚠️ 批量粘贴不可用，回退到逐字输入');
        await page.keyboard.type(content, { delay: 0 });
        await sleep(500);
        console.log('✅ 内容已通过键盘输入');
      }
    }

    if (draft) {
      console.log('⏳ 文章已自动保存为草稿');
      return { status: 'draft_saved', title };
    }

    // 第一步：点击"发布设置"按钮
    const settingsBtn = page.locator(editor.publishSettingsButton.primary);
    await settingsBtn.waitFor({ timeout: 5000, state: 'visible' }).catch(() => {});
    if (await settingsBtn.isVisible().catch(() => false)) {
      await settingsBtn.click();
      console.log('⏳ 打开发布设置...');
      await sleep(2000);
    }

    // 第二步：在弹窗中点击"发布"
    const confirmBtn = page.locator('button:has-text("发布")').last();
    await confirmBtn.waitFor({ timeout: 8000, state: 'visible' }).catch(() => {});
    if (await confirmBtn.isVisible().catch(() => false)) {
      await confirmBtn.click();
      await sleep(3000);
      const currentUrl = page.url();
      console.log(`✅ 文章已发布`);
      return { status: 'published', url: currentUrl, title };
    }

    throw new Error('未找到发布按钮，发布失败');
  }, 'publish_article');
}

// ──────────────────────────────────────────
// 发布想法
// ──────────────────────────────────────────

async function publishThought({ content, imagePath = null }) {
  console.log(`\n💭 发布想法`);

  return await withCrashRecovery(async () => {
    const { context, page } = await getSession();
    const selectors = getSelectors();
    const thought = selectors.thought;

    // 导航到首页
    await navigateTo(page, 'https://www.zhihu.com/');
    await humanDelay(1500, 2500);

    // 找到并点击"发想法"按钮
    const triggerBtn = page.locator(thought.trigger.primary);
    const triggerCount = await triggerBtn.count();
    if (triggerCount > 0 && await triggerBtn.isVisible()) {
      console.log('点击"发想法"按钮...');
      await triggerBtn.click();
      await humanDelay(2000, 3000);
    } else {
      const trigger = await findElement(page, thought.trigger);
      if (trigger) {
        console.log('点击想法触发按钮...');
        await trigger.click();
        await humanDelay(2000, 3000);
      } else {
        throw new Error('未找到想法触发按钮');
      }
    }

    // 输入想法内容
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
    }

    // 上传图片（可选）
    if (imagePath) {
      const fileInput = await page.$('input[type="file"]');
      if (fileInput) {
        await fileInput.setInputFiles(imagePath);
        console.log('📷 图片已选择，等待上传...');
        await page.waitForTimeout(3000);
      }
    }

    // 点击发布 - 等待按钮可用
    await sleep(1000);
    const publishBtnLoc = page.locator('button:has-text("发布")').first();
    await publishBtnLoc.waitFor({ timeout: 10000, state: 'visible' }).catch(() => null);
    if (await publishBtnLoc.isVisible().catch(() => false)) {
      await publishBtnLoc.click();
      await sleep(3000);
      console.log('✅ 想法已发布');
      return { status: 'published', type: 'thought' };
    }

    throw new Error('未找到发布按钮');
  }, 'publish_thought');
}

// ──────────────────────────────────────────
// CLI 入口
// ──────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const type = args[0];

  if (!type || (type !== 'article' && type !== 'thought')) {
    console.error('用法: node scripts/zhihu-publish.js <article|thought> [选项]');
    console.error('');
    console.error('文章:');
    console.error('  node scripts/zhihu-publish.js article --title "标题" --content "正文" [--draft]');
    console.error('  node scripts/zhihu-publish.js article --title "标题" --content-file "path.md"');
    console.error('');
    console.error('想法:');
    console.error('  node scripts/zhihu-publish.js thought --content "内容" [--image "图片路径"]');
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
    }
  }

  if (!options.content) {
    console.error('错误: 需要 --content 或 --content-file');
    process.exit(1);
  }

  if (type === 'article' && !options.title) {
    console.error('错误: 文章需要 --title');
    process.exit(1);
  }

  const fn = type === 'article' ? publishArticle(options) : publishThought(options);
  fn.then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }).catch(err => {
    console.error(`❌ 发布失败:`, err.message);
    process.exit(1);
  });
}

if (import.meta.filename ? process.argv[1] === import.meta.filename : process.argv[1]?.endsWith('zhihu-publish.js')) {
  main();
}

export { publishArticle, publishThought };

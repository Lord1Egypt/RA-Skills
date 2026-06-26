#!/usr/bin/env node
/**
 * zhihu-ask.js — 知乎提问模块
 *
 * 在知乎上提出新问题。
 *
 * CLI:
 *   node scripts/zhihu-ask.js --title "问题标题" [--detail "补充说明"]
 */

import { getSession, navigateTo, findElement, typeLikeHuman, humanDelay, sleep, withCrashRecovery, getSelectors } from './zhihu-browser.js';

// ──────────────────────────────────────────
// 提问
// ──────────────────────────────────────────

async function askQuestion(title, detail = '') {
  console.log(`\n❓ 提问: ${title}`);

  return await withCrashRecovery(async () => {
    const { page } = await getSession();
    const selectors = getSelectors();

    // 导航到提问页面
    await navigateTo(page, 'https://www.zhihu.com/question/create');
    await humanDelay(2000, 3000);

    // 输入问题标题
    const titleInput = await findElement(page, selectors.ask.titleInput);
    if (titleInput) {
      await titleInput.click();
      await sleep(300);
      await typeLikeHuman(page, selectors.ask.titleInput.primary, title);
      await humanDelay(500, 1000);
    }

    // 输入补充说明（可选）
    if (detail) {
      const detailInput = await findElement(page, selectors.ask.detailInput);
      if (detailInput) {
        await detailInput.click();
        await sleep(300);
        await typeLikeHuman(page, selectors.ask.detailInput.primary || '[contenteditable="true"]', detail);
        await humanDelay(500, 1500);
      }
    }

    // 提交问题
    const submitBtn = await findElement(page, selectors.ask.submitButton);
    if (submitBtn) {
      await submitBtn.click();
      await humanDelay(2000, 4000);

      // 等待页面跳转（成功后跳转到问题页）  
      await sleep(2000);
      const currentUrl = page.url();
      console.log('✅ 问题已提交');
      return { status: 'submitted', title, url: currentUrl || 'https://www.zhihu.com/question/' };
    }

    throw new Error('未找到提交按钮');
  }, 'ask');
}

// ──────────────────────────────────────────
// CLI
// ──────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  let title = '', detail = '';

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--title':
        title = args[++i];
        break;
      case '--detail':
        detail = args[++i];
        break;
    }
  }

  if (!title) {
    console.error('用法: node scripts/zhihu-ask.js --title "问题标题" [--detail "补充说明"]');
    process.exit(1);
  }

  try {
    const result = await askQuestion(title, detail);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (err) {
    console.error(`❌ 提问失败:`, err.message);
    process.exit(1);
  }
}

if (import.meta.filename ? process.argv[1] === import.meta.filename : process.argv[1]?.endsWith('zhihu-ask.js')) {
  main();
}

export { askQuestion };

#!/usr/bin/env node
/**
 * zhihu-answer.js — 知乎回答问题模块
 *
 * 搜索问题并撰写/提交回答。
 *
 * CLI:
 *   node scripts/zhihu-answer.js --question-id "问题ID" --content "回答内容"
 *   node scripts/zhihu-answer.js --search "关键词" --content "回答内容"
 *
 * @module zhihu-answer
 */

import { getSession, navigateTo, findElement, typeLikeHuman, humanDelay, sleep, withCrashRecovery, getSelectors } from './zhihu-browser.js';
import { answerLog } from './zhihu-logger.js';

// ──────────────────────────────────────────
// 回答问题
// ──────────────────────────────────────────

/**
 * 回答问题
 *
 * @param {number|string} questionId - 问题 ID
 * @param {string} content - 回答内容
 * @returns {Promise<{ status: string, questionId: string, url: string }>} 提交结果
 */
async function answerQuestion(questionId, content) {
  const url = `https://www.zhihu.com/question/${questionId}`;
  answerLog.info(`回答问题: ${url}`);

  return await withCrashRecovery(async () => {
    const { page } = await getSession();
    const selectors = getSelectors();

    await navigateTo(page, url);
    await humanDelay(2000, 3000);

    // 滚动到回答区域
    await sleep(1000);

    // 查找回答编辑器
    const editor = await findElement(page, selectors.answer.editor);
    if (!editor) {
      // 可能要先点击"写回答"按钮
      const writeBtn = await page.locator('button:has-text("写回答")').first().waitFor({ timeout: 5000 }).catch(() => null);
      if (writeBtn) {
        await writeBtn.click();
        await humanDelay(1000, 2000);
      }
    }

    // 填写回答内容
    const answerEditor = await findElement(page, selectors.answer.editor);
    if (answerEditor) {
      await answerEditor.click();
      await sleep(500);
      await typeLikeHuman(page, selectors.answer.editor.primary || '[contenteditable="true"]', content);
      await humanDelay(1000, 2000);
    }

    // 提交回答
    const submitBtn = await findElement(page, selectors.answer.submit);
    if (submitBtn) {
      await submitBtn.click();
      await humanDelay(2000, 4000);
      answerLog.info('✅ 回答已提交');
      return { status: 'submitted', questionId, url };
    }

    throw new Error('未找到提交按钮');
  }, 'answer');
}

// ──────────────────────────────────────────
// CLI
// ──────────────────────────────────────────

/**
 * CLI 主入口
 * @returns {Promise<void>}
 */
async function main() {
  const args = process.argv.slice(2);
  let questionId, content;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--question-id':
      case '--id':
        questionId = args[++i];
        break;
      case '--content':
        content = args[++i];
        break;
    }
  }

  if (!questionId || !content) {
    answerLog.error('用法: node scripts/zhihu-answer.js --question-id "问题ID" --content "回答内容"');
    process.exit(1);
  }

  try {
    const result = await answerQuestion(questionId, content);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (err) {
    answerLog.error('回答失败', err);
    process.exit(1);
  }
}

if (import.meta.filename ? process.argv[1] === import.meta.filename : process.argv[1]?.endsWith('zhihu-answer.js')) {
  main();
}

export { answerQuestion };

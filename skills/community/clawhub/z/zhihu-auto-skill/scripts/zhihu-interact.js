#!/usr/bin/env node
/**
 * zhihu-interact.js — 知乎互动模块
 *
 * 支持：点赞、评论、关注、收藏
 *
 * CLI:
 *   node scripts/zhihu-interact.js like --url "内容链接"
 *   node scripts/zhihu-interact.js comment --url "链接" --content "评论"
 *   node scripts/zhihu-interact.js follow --user "用户ID"
 *
 * @module zhihu-interact
 */

import { getSession, navigateTo, findElement, clickElement, typeLikeHuman, humanDelay, sleep, withCrashRecovery, getSelectors } from './zhihu-browser.js';
import { interactLog } from './zhihu-logger.js';

// ──────────────────────────────────────────
// 点赞/取消点赞
// ──────────────────────────────────────────

/**
 * 点赞或取消点赞内容
 *
 * @param {string} url - 内容链接
 * @param {boolean} [unlike=false] - 是否取消点赞
 * @returns {Promise<{ status: string, action: string }>} 操作结果
 */
async function like(url, unlike = false) {
  const action = unlike ? '取消点赞' : '点赞';
  interactLog.info(`${action}: ${url}`);

  return await withCrashRecovery(async () => {
    const { page } = await getSession();
    const selectors = getSelectors();

    await navigateTo(page, url);
    await humanDelay(2000, 3000);

    const likeBtn = await findElement(page, selectors.interaction.likeButton);
    if (!likeBtn) {
      throw new Error('未找到点赞按钮');
    }

    const currentClass = await likeBtn.getAttribute('class') || '';
    const isLiked = currentClass.includes('is-active') || currentClass.includes('active');

    if ((unlike && isLiked) || (!unlike && !isLiked)) {
      await likeBtn.click();
      await humanDelay(1000, 2000);
      interactLog.info(`✅ ${action}成功`);
      return { status: 'success', action };
    }

    interactLog.info(`ℹ️ 已是目标状态 (${unlike ? '已取消' : '已点赞'})`);
    return { status: 'already', action };
  }, 'like');
}

// ──────────────────────────────────────────
// 评论
// ──────────────────────────────────────────

/**
 * 发布评论
 *
 * @param {string} url - 内容链接
 * @param {string} content - 评论内容
 * @returns {Promise<{ status: string, action: string }>} 操作结果
 */
async function comment(url, content) {
  interactLog.info(`评论: ${url}`);

  return await withCrashRecovery(async () => {
    const { page } = await getSession();
    const selectors = getSelectors();

    await navigateTo(page, url);
    await humanDelay(2000, 3000);

    // 点击评论输入框
    await sleep(1000);
    const commentInput = await findElement(page, selectors.interaction.commentInput);
    if (!commentInput) {
      throw new Error('未找到评论输入框');
    }

    await commentInput.click();
    await humanDelay(500, 1000);

    // 输入评论内容
    await typeLikeHuman(page, selectors.interaction.commentInput.primary, content);
    await humanDelay(500, 1500);

    // 点击发布评论
    const submitBtn = await findElement(page, selectors.interaction.commentSubmit);
    if (submitBtn) {
      await submitBtn.click();
      await humanDelay(2000, 3000);
      interactLog.info('✅ 评论发布成功');
      return { status: 'success', action: 'comment' };
    }

    throw new Error('未找到评论提交按钮');
  }, 'comment');
}

// ──────────────────────────────────────────
// 关注用户
// ──────────────────────────────────────────

/**
 * 关注用户
 *
 * @param {string} userId - 用户 ID 或 url_token
 * @returns {Promise<{ status: string, action: string }>} 操作结果
 */
async function follow(userId) {
  const url = `https://www.zhihu.com/people/${userId}`;
  interactLog.info(`关注用户: ${userId}`);

  return await withCrashRecovery(async () => {
    const { page } = await getSession();
    const selectors = getSelectors();

    await navigateTo(page, url);
    await humanDelay(2000, 3000);

    const followBtn = await findElement(page, selectors.interaction.followButton);
    if (followBtn) {
      const text = await followBtn.textContent() || '';
      if (text.includes('已关注')) {
        interactLog.info('ℹ️ 已关注该用户');
        return { status: 'already', action: 'follow' };
      }
      await followBtn.click();
      await humanDelay(1000, 2000);
      interactLog.info('✅ 关注成功');
      return { status: 'success', action: 'follow' };
    }

    throw new Error('未找到关注按钮');
  }, 'follow');
}

// ──────────────────────────────────────────
// CLI
// ──────────────────────────────────────────

/**
 * CLI 主入口
 * @returns {void}
 */
function main() {
  const args = process.argv.slice(2);
  const action = args[0];

  if (!action) {
    interactLog.error('用法: node scripts/zhihu-interact.js <like|unlike|comment|follow> [选项]');
    interactLog.error('');
    interactLog.error('  like/unlike:  --url "内容链接"');
    interactLog.error('  comment:      --url "链接" --content "评论"');
    interactLog.error('  follow:       --user "用户ID"');
    process.exit(1);
  }

  const opts = {};
  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--url': opts.url = args[++i]; break;
      case '--content': opts.content = args[++i]; break;
      case '--user': opts.user = args[++i]; break;
    }
  }

  let promise;
  switch (action) {
    case 'like': promise = like(opts.url); break;
    case 'unlike': promise = like(opts.url, true); break;
    case 'comment':
      if (!opts.content) { interactLog.error('评论需要 --content'); process.exit(1); }
      promise = comment(opts.url, opts.content);
      break;
    case 'follow':
      if (!opts.user) { interactLog.error('关注需要 --user'); process.exit(1); }
      promise = follow(opts.user);
      break;
    default:
      interactLog.error(`未知操作: ${action}`);
      process.exit(1);
  }

  promise.then(r => {
    console.log(JSON.stringify(r, null, 2));
    process.exit(0);
  }).catch(err => {
    interactLog.error('操作失败', err);
    process.exit(1);
  });
}

if (import.meta.filename ? process.argv[1] === import.meta.filename : process.argv[1]?.endsWith('zhihu-interact.js')) {
  main();
}

export { like, comment, follow };

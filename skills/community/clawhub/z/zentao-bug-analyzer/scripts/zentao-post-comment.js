#!/usr/bin/env node
/**
 * zentao-post-comment.js — 在禅道 Bug 下发布评论
 *
 * 用法:
 *   node zentao-post-comment.js --ws=<wsEndpoint> --bug-id=<id> --comment-file=<path>
 *     [--zentao-url=http://zentao.gxatek.com:20080]
 *
 *   node zentao-post-comment.js --ws=<wsEndpoint> --bug-id=<id> --comment="纯文本内容"
 *     ⚠️ --comment 仅限极简手动测试，生产环境禁用（shell 转义会导致 HTML 截断/损坏）
 *     [--zentao-url=http://zentao.gxatek.com:20080]
 *
 * comment-file 参数从文件读取 HTML（推荐，避免 shell 转义问题）。
 * comment 参数传入纯文本（仅限测试），脚本自动做 URL 编码。
 * 两者互斥，comment-file 优先。
 *
 * 例如: --comment-file=bugs/1433003/comment.html
 *
 * 输出 (stdout):
 *   OK 或 FAIL
 *
 * 需要先启动 zentao-login.js 获取 WS endpoint。
 */

const { parseArgs, connectAndGetPage } = require('./zentao-utils');
const fs = require('fs');

async function main() {
  const config = parseArgs();

  if (!config.wsEndpoint) {
    console.error('[ERROR] 缺少 --ws 参数（WS endpoint）');
    process.exit(1);
  }
  if (!config.bugId) {
    console.error('[ERROR] 缺少 --bug-id 参数');
    process.exit(1);
  }
  if (!config.comment && !config.commentFile) {
    console.error('[ERROR] 缺少 --comment 或 --comment-file 参数');
    process.exit(1);
  }

  if (config.comment && config.commentFile) {
    console.error('[ERROR] --comment 和 --comment-file 不能同时使用');
    process.exit(1);
  }

  if (config.commentFile) {
    if (!fs.existsSync(config.commentFile)) {
      console.error(`[ERROR] comment-file 不存在: ${config.commentFile}`);
      process.exit(1);
    }
    config.comment = fs.readFileSync(config.commentFile, 'utf-8').trim();
    console.error(`[INFO] 从文件读取评论: ${config.commentFile} (${config.comment.length} 字符)`);
  }

  console.error(`[INFO] 连接到浏览器: ${config.wsEndpoint}`);

  const { page } = await connectAndGetPage(config.wsEndpoint);

  console.error(`[INFO] 发布 Bug #${config.bugId} 评论...`);

  const ok = await page.evaluate(async ({ bugId, comment, zentaoUrl }) => {
    const resp = await fetch(`${zentaoUrl}/action-comment-bug-${bugId}.html`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      credentials: 'include',
      body: `comment=${encodeURIComponent(comment)}`,
    });
    return resp.ok;
  }, { bugId: config.bugId, comment: config.comment, zentaoUrl: config.zentaoUrl });

  if (ok) {
    console.log('OK');
    console.error('[INFO] 评论发布成功');
  } else {
    console.log('FAIL');
    console.error('[ERROR] 评论发布失败');
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});

#!/usr/bin/env node
/**
 * xhs.js - 小红书 Windows 命令行工具
 * 用法:
 *   node xhs.js status              检查登录状态
 *   node xhs.js login               扫码/账号登录
 *   node xhs.js search <关键词>      搜索笔记
 *   node xhs.js detail <笔记URL>     获取帖子详情
 *   node xhs.js publish              发布笔记（交互式）
 *   node xhs.js track <关键词>       生成话题热点报告
 */

const { login, search, getNoteDetail, publishNote, checkStatus } = require('./xhs-core');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const [,, cmd, ...args] = process.argv;

function printHelp() {
  console.log(`
小红书 Windows 工具 v1.0
========================
用法: node xhs.js <命令> [参数]

命令:
  status                    检查登录状态
  login                     登录小红书（弹出浏览器扫码）
  search <关键词> [数量]     搜索笔记（默认20条）
  detail <笔记URL>           获取帖子详情和评论
  publish                   发布图文笔记（交互式）
  track <关键词> [数量]      生成话题热点 Markdown 报告

示例:
  node xhs.js search qclaw 20
  node xhs.js detail https://www.xiaohongshu.com/explore/xxx
  node xhs.js track qclaw 10
`);
}

async function cmdSearch(keyword, limit = 20) {
  if (!keyword) { console.error('[!] 请提供搜索关键词'); process.exit(1); }
  const results = await search(keyword, parseInt(limit));

  if (!results || results.length === 0) {
    console.log('[!] 未找到相关内容');
    return;
  }

  console.log(`\n搜索结果: "${keyword}" (${results.length} 条)\n`);
  console.log('='.repeat(60));

  results.forEach((item, i) => {
    // 兼容 API 拦截格式和 DOM 解析格式
    const title = item.noteCard?.displayTitle || item.title || '(无标题)';
    const author = item.noteCard?.user?.nickname || item.author || '未知';
    const likes = item.noteCard?.interactInfo?.likedCount || item.likes || '0';
    const comments = item.noteCard?.interactInfo?.commentCount || '-';
    const collects = item.noteCard?.interactInfo?.collectedCount || '-';
    const id = item.id || '';
    const url = item.url || (id ? `https://www.xiaohongshu.com/explore/${id}` : '');

    console.log(`${i + 1}. ${title}`);
    console.log(`   作者: ${author}  |  ❤️ ${likes}  💬 ${comments}  ⭐ ${collects}`);
    if (url) console.log(`   链接: ${url}`);
    console.log('');
  });

  // 保存结果到文件
  const outFile = path.join(process.env.USERPROFILE, '.xiaohongshu-win', `search_${keyword}_${Date.now()}.json`);
  fs.writeFileSync(outFile, JSON.stringify(results, null, 2), 'utf8');
  console.log(`[*] 完整数据已保存: ${outFile}`);
}

async function cmdDetail(noteUrl) {
  if (!noteUrl) { console.error('[!] 请提供笔记 URL'); process.exit(1); }
  const detail = await getNoteDetail(noteUrl);

  if (!detail) { console.log('[!] 获取失败'); return; }

  const note = detail.noteCard || detail;
  console.log('\n' + '='.repeat(60));
  console.log(`标题: ${note.displayTitle || detail.title || '(无标题)'}`);
  console.log(`作者: ${note.user?.nickname || detail.author || '未知'}`);
  console.log(`点赞: ${note.interactInfo?.likedCount || detail.likes || '0'}`);
  console.log(`收藏: ${note.interactInfo?.collectedCount || detail.collects || '0'}`);
  console.log(`\n正文:\n${note.desc || detail.desc || ''}`);

  const comments = detail.comments || [];
  if (comments.length > 0) {
    console.log(`\n评论 (${comments.length} 条):`);
    comments.slice(0, 10).forEach(c => {
      const user = c.userInfo?.nickname || c.user || '匿名';
      const content = c.content || '';
      const likes = c.likeCount || c.likes || 0;
      console.log(`  [${user}] ${content}  (❤️ ${likes})`);
    });
  }
}

async function cmdPublish() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q) => new Promise(resolve => rl.question(q, resolve));

  console.log('\n发布小红书笔记\n' + '='.repeat(40));
  const title = await ask('标题 (≤20字): ');
  const content = await ask('正文 (≤1000字): ');
  const imgInput = await ask('图片路径 (多个用逗号分隔，留空跳过): ');
  rl.close();

  const images = imgInput.trim() ? imgInput.split(',').map(s => s.trim()).filter(Boolean) : [];
  await publishNote(title.trim(), content.trim(), images);
}

async function cmdTrack(keyword, limit = 10) {
  if (!keyword) { console.error('[!] 请提供话题关键词'); process.exit(1); }
  console.log(`[*] 生成话题报告: ${keyword}`);

  const results = await search(keyword, parseInt(limit));
  if (!results || results.length === 0) {
    console.log('[!] 未找到相关内容'); return;
  }

  const now = new Date().toLocaleString('zh-CN');
  let totalLikes = 0, totalComments = 0, totalCollects = 0;

  let report = `# 🔥 小红书话题报告\n\n`;
  report += `**话题:** ${keyword}  \n**生成时间:** ${now}  \n**笔记数:** ${results.length}\n\n---\n\n`;
  report += `## 📊 数据概览\n\n`;

  const rows = results.map((item, i) => {
    const title = item.noteCard?.displayTitle || item.title || '(无标题)';
    const author = item.noteCard?.user?.nickname || item.author || '未知';
    const likes = parseInt(item.noteCard?.interactInfo?.likedCount || item.likes || 0);
    const comments = parseInt(item.noteCard?.interactInfo?.commentCount || 0);
    const collects = parseInt(item.noteCard?.interactInfo?.collectedCount || 0);
    const id = item.id || '';
    const url = item.url || (id ? `https://www.xiaohongshu.com/explore/${id}` : '');
    totalLikes += likes; totalComments += comments; totalCollects += collects;
    return { rank: i + 1, title, author, likes, comments, collects, url };
  });

  report += `| 指标 | 数值 |\n|------|------|\n`;
  report += `| 总笔记数 | ${results.length} |\n`;
  report += `| 总点赞 | ${totalLikes.toLocaleString()} |\n`;
  report += `| 总评论 | ${totalComments.toLocaleString()} |\n`;
  report += `| 总收藏 | ${totalCollects.toLocaleString()} |\n\n---\n\n`;
  report += `## 📝 热帖排行\n\n`;

  // 按点赞排序
  rows.sort((a, b) => b.likes - a.likes);
  rows.forEach(r => {
    report += `### ${r.rank}. ${r.title}\n\n`;
    report += `**作者:** ${r.author}  |  ❤️ ${r.likes} 赞  💬 ${r.comments} 评论  ⭐ ${r.collects} 收藏\n`;
    if (r.url) report += `**链接:** ${r.url}\n`;
    report += `\n---\n\n`;
  });

  const heatLevel = totalLikes > 10000 ? '🔥🔥🔥 极高' : totalLikes > 1000 ? '🔥🔥 高' : totalLikes > 100 ? '🔥 中' : '💤 低';
  report += `## 📈 趋势分析\n\n- **热度:** ${heatLevel}\n- **互动活跃度:** ${totalComments > 100 ? '非常活跃' : totalComments > 20 ? '活跃' : '一般'}\n\n`;
  report += `*由 OpenClaw 小红书 Windows 工具自动生成*\n`;

  const outFile = path.join(process.env.USERPROFILE, '.xiaohongshu-win', `report_${keyword}_${Date.now()}.md`);
  fs.writeFileSync(outFile, report, 'utf8');
  console.log(report);
  console.log(`\n[*] 报告已保存: ${outFile}`);
}

// ── 主入口 ────────────────────────────────────────────────────────────────
(async () => {
  switch (cmd) {
    case 'status':  checkStatus(); break;
    case 'login':   await login(); break;
    case 'search':  await cmdSearch(args[0], args[1]); break;
    case 'detail':  await cmdDetail(args[0]); break;
    case 'publish': await cmdPublish(); break;
    case 'track':   await cmdTrack(args[0], args[1]); break;
    default:        printHelp();
  }
})().catch(err => {
  console.error('[ERROR]', err.message);
  process.exit(1);
});

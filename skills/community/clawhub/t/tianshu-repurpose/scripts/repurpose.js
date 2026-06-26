#!/usr/bin/env node
/**
 * 一文多发：长文 → 多平台长度版本
 * node repurpose.js --file article.md
 */

const fs = require('fs');
const path = require('path');

const LIMITS = {
  xhs: 900,
  douyin: 280,
  weibo: 200,
  gh_summary: 120,
  gh_title_max: 64,
};

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { file: null, text: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if ((a === '--file' || a === '-f') && args[i + 1]) out.file = args[++i];
    else if ((a === '--text' || a === '-t') && args[i + 1]) out.text = args[++i];
  }
  return out;
}

function readAll(opts) {
  if (opts.file) {
    const p = path.resolve(opts.file);
    if (!fs.existsSync(p)) {
      console.error('文件不存在:', p);
      process.exit(1);
    }
    return fs.readFileSync(p, 'utf-8');
  }
  if (opts.text) return opts.text;
  console.error('用法: node repurpose.js --file <path> | --text "长文"');
  process.exit(1);
}

/** 去掉 Markdown 简单标记，便于字数统计与截断 */
function stripMd(s) {
  return s
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`[^`]+`/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]+\)/g, ' ')
    .replace(/\[[^\]]*\]\([^)]+\)/g, '$1')
    .replace(/^#+\s+/gm, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function clipByChars(s, maxChars) {
  const arr = [...s];
  if (arr.length <= maxChars) return s.trim();
  return arr.slice(0, maxChars - 1).join('') + '…';
}

function firstParagraph(plain) {
  const parts = plain.split(/[。！？\n]/).filter((x) => x.trim());
  return parts[0] ? parts[0].trim() + '。' : plain.slice(0, 80);
}

function titleIdeas(plain) {
  const p = firstParagraph(plain).replace(/。$/, '');
  const base = p.slice(0, 24);
  return [
    base.length > 18 ? base.slice(0, 18) + '…' : base,
    base.length > 10 ? base.slice(0, 10) + '｜一文读懂' : base + '｜建议收藏',
    base.length > 8 ? base.slice(0, 8) + '…后续更新' : base,
  ].filter((x, i, a) => x && a.indexOf(x) === i);
}

function main() {
  const raw = readAll(parseArgs());
  const plain = stripMd(raw);
  if (!plain) {
    console.error('正文为空');
    process.exit(1);
  }

  const douyinFirstLine = clipByChars(plain.replace(/\s/g, ''), 28);
  const lines = [];

  lines.push('## 一文多发 · 多平台草稿\n');
  lines.push('> 以下为规则裁剪，发布前请按各平台最新规范与品牌调性人工润色。\n');

  lines.push('### 小红书（正文建议 ≤ ' + LIMITS.xhs + ' 字）\n');
  lines.push(clipByChars(plain, LIMITS.xhs));
  lines.push('\n*首图建议：对比图 / 清单图 / 大字报封面。*\n');

  lines.push('### 抖音配文（约 ' + LIMITS.douyin + ' 字，首行可做「黄金一行」）\n');
  lines.push(douyinFirstLine + '\n\n' + clipByChars(plain, LIMITS.douyin - douyinFirstLine.length - 2));
  lines.push('\n*可另配口播脚本：见 tianshu-short-script。*\n');

  lines.push('### 微博短讯（约 ' + LIMITS.weibo + ' 字）\n');
  lines.push(clipByChars(plain, LIMITS.weibo));
  lines.push('\n*视情况补充 1～3 个话题 #。*\n');

  lines.push('### 公众号\n');
  lines.push('**标题备选（每条 ≤ ' + LIMITS.gh_title_max + ' 字）**\n');
  titleIdeas(plain).forEach((t, i) => lines.push(`${i + 1}. ${clipByChars(t, LIMITS.gh_title_max)}`));
  lines.push('\n**摘要（约 ' + LIMITS.gh_summary + ' 字）**\n');
  lines.push(clipByChars(firstParagraph(plain), LIMITS.gh_summary));

  lines.push('\n---\n**完整纯文本字数（粗略）：** ' + [...plain.replace(/\s/g, '')].length + ' 字');

  process.stdout.write(lines.join('\n') + '\n');
}

main();

#!/usr/bin/env node
/**
 * 小红书笔记结构化：标题备选、分段、话题词、自检
 * node pack_note.js --file draft.txt | --text "..."
 */

const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { file: null, text: null, maxBody: 900 };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if ((a === '--file' || a === '-f') && args[i + 1]) out.file = args[++i];
    else if ((a === '--text' || a === '-t') && args[i + 1]) out.text = args[++i];
    else if ((a === '--max-body' || a === '-m') && args[i + 1])
      out.maxBody = Math.max(200, parseInt(args[++i], 10) || 900);
  }
  return out;
}

function readBody(opts) {
  if (opts.file) {
    const p = path.resolve(opts.file);
    if (!fs.existsSync(p)) {
      console.error('文件不存在:', p);
      process.exit(1);
    }
    return fs.readFileSync(p, 'utf-8');
  }
  if (opts.text) return opts.text;
  console.error('用法: node pack_note.js --file <path> | --text "正文" [--max-body 900]');
  process.exit(1);
}

function clipChars(s, max) {
  const arr = [...s];
  if (arr.length <= max) return s.trim();
  return arr.slice(0, max - 1).join('') + '…';
}

/** 从正文抽词作 #话题 草稿（按片段频次，非分词器） */
function hashtagCandidates(text) {
  const parts = text
    .split(/[。！？，、；：\s\n\r《》「」【】]+/)
    .map((x) => x.trim())
    .filter((x) => x.length >= 2 && x.length <= 12);
  const freq = new Map();
  for (const p of parts) {
    freq.set(p, (freq.get(p) || 0) + 1);
  }
  return [...freq.entries()]
    .sort((a, b) => b[1] - a[1] || b[0].length - a[0].length)
    .slice(0, 10)
    .map(([w]) => w);
}

function titleIdeas(plain) {
  const lines = plain.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const first = lines[0] || plain;
  const oneLine = plain.replace(/\s+/g, ' ').trim();
  const ideas = new Set();

  if (first.length >= 6 && first.length <= 20) ideas.add(first);
  if (first.length > 20) ideas.add(clipChars(first, 18) + '…');

  const core = clipChars(oneLine.replace(/^#+\s*/, ''), 16);
  ideas.add(core);
  ideas.add(core.length >= 8 ? core.slice(0, 8) + '…｜建议收藏' : core + '｜干货');
  ideas.add(core.length >= 6 ? core.slice(0, 6) + '…｜一文讲清' : '分享｜' + core);

  return [...ideas].filter(Boolean).slice(0, 5);
}

function paragraphize(plain, maxBody) {
  const sentences = plain
    .replace(/\r\n/g, '\n')
    .split(/(?<=[。！？])\s*/)
    .map((s) => s.trim())
    .filter(Boolean);
  if (sentences.length === 0) return clipChars(plain, maxBody);

  const paras = [];
  let buf = '';
  let total = 0;
  for (const sent of sentences) {
    if (total + sent.length > maxBody) break;
    if ((buf + sent).length > 180 && buf) {
      paras.push(buf.trim());
      buf = sent;
    } else {
      buf = buf ? buf + sent : sent;
    }
    total += sent.length;
  }
  if (buf) paras.push(buf.trim());
  if (paras.length === 0) return clipChars(plain, maxBody);
  return paras.join('\n\n');
}

function main() {
  const opts = parseArgs();
  let plain = readBody(opts).trim();
  plain = plain.replace(/^\uFEFF/, '');

  if (!plain) {
    console.error('正文为空');
    process.exit(1);
  }

  const hashtags = hashtagCandidates(plain);
  const titles = titleIdeas(plain);
  const body = paragraphize(plain, opts.maxBody);
  const charCount = [...body.replace(/\s/g, '')].length;

  const out = [];
  out.push('## 小红书笔记结构稿\n');
  out.push('### 标题备选（建议 20 字内择一）\n');
  titles.forEach((t, i) => out.push(`${i + 1}. ${t}`));
  out.push('\n### 正文（已按约 ' + opts.maxBody + ' 字内分段，当前约 ' + charCount + ' 字）\n');
  out.push(body);
  out.push('\n### 话题标签草稿（从正文高频片段生成，请删改）\n');
  out.push(hashtags.map((h) => '#' + h.replace(/^#/, '')).join(' '));
  out.push('\n### 发布前自检\n');
  out.push('- [ ] 是否夸大疗效、绝对化用语（如「最好」「100%」），需按广告法自查');
  out.push('- [ ] 是否涉及医疗/金融等需资质的内容');
  out.push('- [ ] 首图是否清晰、3 秒内能看懂主题');
  out.push('- [ ] 正文是否有分段与 emoji（按需自行添加，避免整篇堆砌）');
  out.push('- [ ] 评论置顶是否准备答疑或引导');

  process.stdout.write(out.join('\n') + '\n');
}

main();

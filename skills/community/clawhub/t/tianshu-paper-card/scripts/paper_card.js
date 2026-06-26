#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { file: null, text: null, title: null };
  for (let i = 0; i < a.length; i++) {
    if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
    else if ((a[i] === '--text' || a[i] === '-t') && a[i + 1]) o.text = a[++i];
    else if ((a[i] === '--title' || a[i] === '-n') && a[i + 1]) o.title = a[++i];
  }
  return o;
}

function readIn(o) {
  if (o.file) {
    const p = path.resolve(o.file);
    if (!fs.existsSync(p)) {
      console.error('文件不存在:', p);
      process.exit(1);
    }
    return fs.readFileSync(p, 'utf-8').replace(/^\uFEFF/, '').trim();
  }
  if (o.text) return o.text.replace(/^\uFEFF/, '').trim();
  console.error('用法: node paper_card.js --file <path> | --text "摘要" [--title "题目"]');
  process.exit(1);
}

function sentences(s) {
  return s
    .split(/(?<=[.。!！?？])\s*/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function main() {
  const opts = parseArgs();
  let body = readIn(opts);
  let title = opts.title || '（请补全文题）';
  const lines = body.split(/\r?\n/).map((l) => l.trim());
  if (!opts.title && lines[0] && lines[0].length < 120 && !/[。.!?？!]/.test(lines[0])) {
    title = lines[0];
    body = lines.slice(1).join('\n').trim() || body;
  }

  const sens = sentences(body.replace(/\n/g, ' '));
  const n = sens.length;
  const q = sens.slice(0, Math.max(1, Math.ceil(n * 0.25))).join('');
  const m = sens.slice(Math.floor(n * 0.25), Math.floor(n * 0.55)).join(' ') || '（请根据全文补：方法/数据/实验设置）';
  const r = sens.slice(Math.floor(n * 0.55), Math.floor(n * 0.85)).join(' ') || '（请根据全文补：主要结果）';
  const l = sens.slice(Math.floor(n * 0.85)).join(' ') || '（未在摘要中体现，见 Discussion 限制）';

  const out = [];
  out.push('## 文献速读卡片\n');
  out.push(`### 题目\n${title}\n`);
  out.push('### 研究问题 / 动机\n' + (q || '（请手填）'));
  out.push('\n### 方法要点\n' + m);
  out.push('\n### 主要结论\n' + r);
  out.push('\n### 局限与可待验证点\n' + l);
  out.push('\n### 引用句草稿（务必核对原文页码）\n> ' + (sens[0] ? sens[0].slice(0, 200) + (sens[0].length > 200 ? '…' : '') : '（无）'));
  out.push('\n---\n*摘要分段为启发式拆分，精读请以 PDF 为准。*');
  process.stdout.write(out.join('\n') + '\n');
}

main();

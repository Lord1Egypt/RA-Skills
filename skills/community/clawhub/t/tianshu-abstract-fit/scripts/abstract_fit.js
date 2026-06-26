#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { file: null, text: null, max: 300 };
  for (let i = 0; i < a.length; i++) {
    if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
    else if ((a[i] === '--text' || a[i] === '-t') && a[i + 1]) o.text = a[++i];
    else if ((a[i] === '--max' || a[i] === '-m') && a[i + 1]) o.max = parseInt(a[++i], 10) || 300;
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
  if (o.text) return o.text.trim();
  console.error('用法: node abstract_fit.js --file p | --text "…" [--max 300]');
  process.exit(1);
}

function sentences(s) {
  return s
    .replace(/\n/g, ' ')
    .split(/(?<=[.。!！?？;；])\s*/)
    .map((x) => x.trim())
    .filter(Boolean);
}

function main() {
  const o = parseArgs();
  const body = readIn(o);
  const chars = [...body.replace(/\s/g, '')].length;
  const sens = sentences(body);
  const n = sens.length;
  const i1 = Math.max(1, Math.ceil(n * 0.25));
  const i2 = Math.max(i1 + 1, Math.ceil(n * 0.5));
  const i3 = Math.max(i2 + 1, Math.ceil(n * 0.75));
  const bg = sens.slice(0, i1).join('');
  const method = sens .slice(i1, i2).join('');
  const result = sens.slice(i2, i3).join('');
  const concl = sens.slice(i3).join('') || '（结论句不足请手填）';

  const out = [];
  out.push('## 摘要结构草稿（启发式）\n');
  out.push(`- **去空白字数约：** ${chars}（建议上限 ${o.max}，仅作提示）`);
  out.push(chars > o.max ? `- **提示：** 超过建议上限，可在「结果」或「背景」中压缩从句。\n` : '\n');
  out.push('### 背景与问题\n> ' + bg);
  out.push('\n### 方法\n> ' + (method || '（请补）'));
  out.push('\n### 结果\n> ' + (result || '（请补）'));
  out.push('\n### 结论\n> ' + concl);
  out.push('\n---\n*分段按句序比例切分，正式提交前请按学院格式重写。*');
  process.stdout.write(out.join('\n') + '\n');
}

main();

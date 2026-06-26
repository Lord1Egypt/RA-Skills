#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { file: null, text: null, template: false, rows: 15 };
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--template') o.template = true;
    else if ((a[i] === '--rows' || a[i] === '-r') && a[i + 1]) o.rows = Math.max(3, parseInt(a[++i], 10) || 15);
    else if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
    else if ((a[i] === '--text' || a[i] === '-t') && a[i + 1]) o.text = a[++i];
  }
  return o;
}

function readLines(o) {
  if (o.file) {
    const p = path.resolve(o.file);
    if (!fs.existsSync(p)) {
      console.error('文件不存在:', p);
      process.exit(1);
    }
    return fs.readFileSync(p, 'utf-8').split(/\r?\n/);
  }
  if (o.text) return o.text.split(/\r?\n/);
  return [];
}

function main() {
  const o = parseArgs();
  const lines = [];

  lines.push('## 错题记录表\n');
  lines.push('| 题目/来源 | 错因 | 知识点 | 下次复习 |');
  lines.push('| --- | --- | --- | --- |');

  if (o.template) {
    for (let i = 0; i < o.rows; i++) {
      lines.push(`|  |  |  |  |`);
    }
    lines.push('\n*在「下次复习」填日期或打勾。*');
    process.stdout.write(lines.join('\n') + '\n');
    return;
  }

  const raw = readLines(o);
  if (raw.length === 0) {
    console.error('用法: mistake_sheet.js --template [--rows 15] | --file f | --text "a|b|c"');
    process.exit(1);
  }

  for (const row of raw) {
    const s = row.trim();
    if (!s || s.startsWith('#')) continue;
    const parts = s.split(/\s*[|｜]\s*/).map((x) => x.trim());
    const q = parts[0] || '';
    const why = parts[1] || '';
    const tag = parts[2] || '';
    lines.push(`| ${q} | ${why} | ${tag} |  |`);
  }

  if (lines.length <= 4) {
    lines.push('|  |  |  |  |');
  }
  process.stdout.write(lines.join('\n') + '\n');
}

main();

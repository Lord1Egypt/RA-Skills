#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { file: null, text: null };
  for (let i = 0; i < a.length; i++) {
    if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
    else if ((a[i] === '--text' || a[i] === '-t') && a[i + 1]) o.text = a[++i];
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
    return fs.readFileSync(p, 'utf-8');
  }
  if (o.text) return o.text;
  console.error('用法: node split_hw.js --file <path> | --text "..."');
  process.exit(1);
}

function splitTasks(raw) {
  let t = raw.replace(/^\uFEFF/, '').trim();
  const blocks = t.split(/\n{2,}/).map((s) => s.trim()).filter(Boolean);
  const items = [];
  const lineSplit = t.split(/\n/).map((s) => s.trim()).filter(Boolean);

  const numbered = lineSplit.filter((l) => /^\d+[\.\)、]/.test(l) || /^[（(]\d+[)）]/.test(l));
  if (numbered.length >= 2) {
    for (const l of numbered) items.push(l.replace(/^\d+[\.\)、]\s*/, '').replace(/^[（(]\d+[)）]\s*/, ''));
  } else {
    for (const b of blocks) {
      if (b.length > 500) continue;
      if (/作业|完成|提交|截止|DDL|复习|阅读|练习|实验|报告|章/.test(b)) items.push(b.replace(/\n/g, ' '));
    }
  }

  if (items.length === 0) {
    for (const l of lineSplit) {
      if (l.length < 8 || l.length > 200) continue;
      if (/^[#\-*\s]+$/.test(l)) continue;
      items.push(l.replace(/^[-*]\s*/, ''));
    }
  }

  const seen = new Set();
  const uniq = [];
  for (const it of items) {
    const k = it.slice(0, 80);
    if (seen.has(k)) continue;
    seen.add(k);
    uniq.push(it);
  }
  return uniq.slice(0, 40);
}

function main() {
  const raw = readIn(parseArgs());
  const tasks = splitTasks(raw);
  const lines = [];
  lines.push('## 学习任务清单\n');
  lines.push(`> 由原文自动拆分，请按实际截止时间与老师要求核对。\n`);
  lines.push('### 任务项\n');
  if (tasks.length === 0) {
    lines.push('- [ ] （未能识别条目）请手动把要求拆成多条，或改用分点粘贴。');
  } else {
    for (const t of tasks) lines.push(`- [ ] ${t}`);
  }
  lines.push('\n### 文末自检');
  lines.push('- [ ] 是否标出每条的截止日期');
  lines.push('- [ ] 是否区分「必做 / 选做」');
  process.stdout.write(lines.join('\n') + '\n');
}

main();

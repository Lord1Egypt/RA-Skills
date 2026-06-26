#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const OFFSETS = [0, 1, 2, 4, 7, 15];

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { file: null, start: null, perDay: 20 };
  for (let i = 0; i < a.length; i++) {
    if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
    else if ((a[i] === '--start' || a[i] === '-s') && a[i + 1]) o.start = a[++i];
    else if ((a[i] === '--per-day' || a[i] === '-n') && a[i + 1]) o.perDay = Math.max(1, parseInt(a[++i], 10) || 20);
  }
  return o;
}

function parseStart(s) {
  if (s) {
    const d = new Date(s + 'T12:00:00');
    if (!isNaN(d)) return d;
  }
  const t = new Date();
  t.setHours(12, 0, 0, 0);
  return t;
}

function addDays(d, n) {
  const x = new Date(d);
  x.setDate(x.getDate() + n);
  return x;
}

function fmt(d) {
  return d.toISOString().slice(0, 10);
}

function main() {
  const o = parseArgs();
  if (!o.file) {
    console.error('用法: node vocab_plan.js --file words.txt [--start YYYY-MM-DD] [--per-day 20]');
    process.exit(1);
  }
  const p = path.resolve(o.file);
  if (!fs.existsSync(p)) {
    console.error('文件不存在:', p);
    process.exit(1);
  }
  const words = fs
    .readFileSync(p, 'utf-8')
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));

  const start = parseStart(o.start);
  const batches = [];
  for (let i = 0; i < words.length; i += o.perDay) {
    batches.push(words.slice(i, i + o.perDay));
  }

  const dayMap = new Map();
  function addTask(dayKey, text) {
    if (!dayMap.has(dayKey)) dayMap.set(dayKey, { learn: [], review: [] });
    const e = dayMap.get(dayKey);
    if (text.startsWith('[复习]')) e.review.push(text.slice(4));
    else e.learn.push(text);
  }

  batches.forEach((batch, bi) => {
    const learnDay = addDays(start, bi);
    const key = fmt(learnDay);
    batch.forEach((w) => addTask(key, w));
    OFFSETS.slice(1).forEach((off) => {
      const rk = fmt(addDays(learnDay, off));
      addTask(rk, '[复习]' + batch.join('、'));
    });
  });

  const keys = [...dayMap.keys()].sort();
  const lines = [];
  lines.push('## 单词间隔复习计划（简化艾宾浩斯）\n');
  lines.push(`> 新词节奏：每天 ${o.perDay} 词；复习日巩固 +1 / +2 / +4 / +7 / +15 天批次。\n`);
  lines.push(`> 起始日：**${fmt(start)}**；词表共 **${words.length}** 条，分 **${batches.length}** 天学完新词。\n`);
  lines.push('| 日期 | 新学 | 复习批次 |');
  lines.push('| --- | --- | --- |');
  for (const k of keys) {
    const { learn, review } = dayMap.get(k);
    lines.push(
      `| ${k} | ${learn.length ? learn.join('；') : '—'} | ${review.length ? review.join('；') : '—'} |`
    );
  }
  lines.push('\n### 使用提示');
  lines.push('- 复习列过长时，可只口头过一遍本批词义再做真题。');
  lines.push('- 可按个人遗忘曲线把 OFFSETS 改密（需自行改脚本常量）。');
  process.stdout.write(lines.join('\n') + '\n');
}

main();

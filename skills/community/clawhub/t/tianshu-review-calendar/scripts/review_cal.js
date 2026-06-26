#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const a = process.argv.slice(2);
  const o = { exam: null, days: 14, topics: null, file: null };
  for (let i = 0; i < a.length; i++) {
    if ((a[i] === '--exam' || a[i] === '-e') && a[i + 1]) o.exam = a[++i];
    else if ((a[i] === '--days' || a[i] === '-d') && a[i + 1]) o.days = Math.max(1, parseInt(a[++i], 10) || 14);
    else if ((a[i] === '--topics' || a[i] === '-t') && a[i + 1]) o.topics = a[++i];
    else if ((a[i] === '--file' || a[i] === '-f') && a[i + 1]) o.file = a[++i];
  }
  return o;
}

function parseTopics(o) {
  if (o.file) {
    const p = path.resolve(o.file);
    if (!fs.existsSync(p)) {
      console.error('文件不存在:', p);
      process.exit(1);
    }
    return fs
      .readFileSync(p, 'utf-8')
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter((l) => l && !l.startsWith('#'));
  }
  if (o.topics) {
    return o.topics
      .split(/[,，;；]/)
      .map((s) => s.trim())
      .filter(Boolean);
  }
  return [];
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
  if (!o.exam) {
    console.error('用法: node review_cal.js --exam YYYY-MM-DD --topics "a,b,c" | --file topics.txt [--days 14]');
    process.exit(1);
  }
  const exam = new Date(o.exam + 'T12:00:00');
  if (isNaN(exam)) {
    console.error('日期格式错误:', o.exam);
    process.exit(1);
  }
  const topics = parseTopics(o);
  if (topics.length === 0) {
    console.error('请提供 --topics 或 --file');
    process.exit(1);
  }

  const start = addDays(exam, -o.days);
  const lines = [];
  lines.push('## 考前复习排期\n');
  lines.push(`- **考试日：** ${fmt(exam)}`);
  lines.push(`- **计划跨度：** ${fmt(start)} 起，共 ${o.days} 天（至考前一天）\n`);
  lines.push('| 日期 | 建议复习 | 备注 |');
  lines.push('| --- | --- | --- |');

  for (let i = 0; i < o.days; i++) {
    const day = addDays(start, i);
    const k = (i % topics.length + Math.floor(i / topics.length)) % topics.length;
    const focus = topics[(i * 7 + k * 3) % topics.length];
    const second = topics[(i * 3 + 1) % topics.length];
    lines.push(`| ${fmt(day)} | ${focus}；浏览 ${second} | 做题/背诵 45–90min |`);
  }

  lines.push('\n### 使用说明');
  lines.push('- 表内「建议」为均衡轮换，薄弱科目请手动连续加栏。');
  lines.push('- 考试前一天建议只做错题与框架，不新开大块内容。');
  process.stdout.write(lines.join('\n') + '\n');
}

main();

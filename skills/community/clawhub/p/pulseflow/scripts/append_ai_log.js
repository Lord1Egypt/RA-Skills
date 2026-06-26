#!/usr/bin/env node
const path = require('path');
const { ensureDir, formatDateInTimeZone } = require('./_common');
const fs = require('fs');

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const value = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    out[key] = value;
  }
  return out;
}

function formatOffset(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const abs = Math.abs(offsetMinutes);
  const hh = String(Math.floor(abs / 60)).padStart(2, '0');
  const mm = String(abs % 60).padStart(2, '0');
  return `${sign}${hh}:${mm}`;
}

function localIso(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hour = String(date.getHours()).padStart(2, '0');
  const minute = String(date.getMinutes()).padStart(2, '0');
  const second = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day}T${hour}:${minute}:${second}${formatOffset(date)}`;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const agent = String(args.agent || '').trim();
  const reportsDir = String(args['reports-dir'] || '').trim();
  const task = String(args.task || '').trim().replace(/\s*\n\s*/g, ' ');
  const ts = args.ts ? String(args.ts).trim() : localIso(new Date());
  const timeZone = String(args.timezone || process.env.AI_WORKLOG_TIMEZONE || 'Asia/Shanghai').trim();
  const tokens = Number.isFinite(Number(args.tokens)) ? Math.max(0, parseInt(args.tokens, 10) || 0) : 0;

  if (!agent) throw new Error('Missing --agent');
  if (!reportsDir) throw new Error('Missing --reports-dir');
  if (!task) throw new Error('Missing --task');

  const date = formatDateInTimeZone(new Date(ts), timeZone);
  const logPath = path.join(reportsDir, `${agent}-ai-log-${date}.jsonl`);
  ensureDir(reportsDir);
  const entry = JSON.stringify({ ts, agent, task, tokens });
  fs.appendFileSync(logPath, `${entry}\n`, 'utf8');

  process.stdout.write(`${JSON.stringify({ ok: true, path: logPath, entry: JSON.parse(entry) }, null, 2)}\n`);
}

main();

#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = '/home/zqh2333/.openclaw/workspace';
const LEARN = path.join(ROOT, '.learnings');
const OUT = path.join(LEARN, 'INDEX.md');

function parseField(text, label){
  const re = new RegExp(`\\*\\*${label}\\*\\*:\\s*(.+)`);
  const m = text.match(re);
  return m ? m[1].trim() : '';
}

const files = fs.readdirSync(LEARN).filter(f => f.endsWith('.md') && f !== 'INDEX.md').sort();
const rows = [];
for (const file of files) {
  const full = path.join(LEARN, file);
  const text = fs.readFileSync(full, 'utf8');
  const id = (text.match(/## \[([^\]]+)\]/) || [,''])[1];
  const area = parseField(text, 'Area');
  const priority = parseField(text, 'Priority');
  const status = parseField(text, 'Status');
  const logged = parseField(text, 'Logged');
  const summary = ((text.match(/### Summary\n([^\n]+)/) || [,''])[1] || '').trim();
  rows.push({id, area, priority, status, logged, summary, file});
}

let out = '# Learnings Index\n\n';
out += '| ID | Priority | Status | Area | Logged | File | Summary |\n';
out += '|---|---|---|---|---|---|---|\n';
for (const r of rows) {
  out += `| ${r.id} | ${r.priority} | ${r.status} | ${r.area} | ${r.logged} | ${r.file} | ${r.summary.replace(/\|/g,'/')} |\n`;
}
fs.writeFileSync(OUT, out);
console.log(JSON.stringify({indexed: rows.length, out: OUT}, null, 2));

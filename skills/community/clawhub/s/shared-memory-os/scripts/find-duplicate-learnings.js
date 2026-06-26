#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const ROOT = '/home/zqh2333/.openclaw/workspace';
const LEARN = path.join(ROOT, '.learnings');
const files = fs.readdirSync(LEARN).filter(f => f.endsWith('.md') && f !== 'INDEX.md').sort();
function summary(text){ return ((text.match(/### Summary\n([^\n]+)/) || [,''])[1] || '').trim(); }
function normalize(s){ return String(s||'').toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g,' ').trim(); }
const map = new Map();
for (const file of files) {
  const text = fs.readFileSync(path.join(LEARN, file), 'utf8');
  const key = normalize(summary(text));
  if (!key) continue;
  if (!map.has(key)) map.set(key, []);
  map.get(key).push(file);
}
const duplicates = [...map.entries()]
  .filter(([, arr]) => arr.length > 1)
  .map(([normalizedKey, files]) => ({
    normalizedKey,
    files,
    reason: 'The same normalized learning summary appears in multiple learning files.',
    evidence: [`normalized summary matched ${files.length} files`, ...files],
    confidence: files.length >= 3 ? 'high' : 'medium',
    suggestedLifecycle: 'merge-or-supersede'
  }));
console.log(JSON.stringify({ duplicateGroups: duplicates.length, duplicates }, null, 2));
process.exitCode = duplicates.length ? 1 : 0;

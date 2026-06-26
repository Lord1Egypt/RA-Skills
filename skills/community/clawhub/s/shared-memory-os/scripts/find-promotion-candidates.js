#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const ROOT = '/home/zqh2333/.openclaw/workspace';
const LEARN = path.join(ROOT, '.learnings');
const MEMORY = path.join(ROOT, 'MEMORY.md');
const files = fs.readdirSync(LEARN).filter(f => f.endsWith('.md') && f !== 'INDEX.md').sort();
const memoryText = fs.existsSync(MEMORY) ? fs.readFileSync(MEMORY, 'utf8').toLowerCase() : '';
function summary(text){ return ((text.match(/### Summary\n([^\n]+)/) || [,''])[1] || '').trim(); }
function suggested(text){ return ((text.match(/### Suggested Action\n([\s\S]*?)(\n## |$)/) || [,''])[1] || '').trim(); }
function normalize(s){ return String(s||'').toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g,' ').trim(); }
const seen = new Map();
for (const file of files) {
  const text = fs.readFileSync(path.join(LEARN, file), 'utf8');
  const key = normalize(summary(text));
  if (!key) continue;
  if (!seen.has(key)) seen.set(key, []);
  seen.get(key).push({ file, summary: summary(text), suggested: suggested(text) });
}
const candidates = [];
for (const [key, arr] of seen.entries()) {
  if (arr.length >= 2 && !memoryText.includes(key)) {
    candidates.push({
      summary: arr[0].summary,
      occurrences: arr.length,
      files: arr.map(x => x.file),
      suggested: arr[0].suggested,
      reason: 'Repeated reusable lesson has not yet been promoted into durable memory.',
      evidence: [`repeated ${arr.length} times`, `not found in durable memory: ${key}`],
      confidence: arr.length >= 3 ? 'high' : 'medium',
      suggestedLifecycle: 'candidate-for-promotion',
      reviewStatus: 'pending-review'
    });
  }
}
console.log(JSON.stringify({ promotionCandidates: candidates.length, candidates }, null, 2));

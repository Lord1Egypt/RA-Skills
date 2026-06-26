#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const ROOT = '/home/zqh2333/.openclaw/workspace';
const MEMORY = path.join(ROOT, 'MEMORY.md');
const text = fs.existsSync(MEMORY) ? fs.readFileSync(MEMORY, 'utf8') : '';
const lines = text.split(/\n/).filter(x => x.trim().startsWith('- '));
const stale = lines.filter(x => /2026-04-07|2026-04-08/.test(x)).map(line => ({
  line,
  reason: 'Dated durable-memory entry should be reviewed for continued validity.',
  evidence: ['contains explicit date marker', 'durable memory should prefer long-lived rules over date-bound state'],
  confidence: 'low',
  suggestedLifecycle: 'review-for-active-or-archive',
  lastValidatedAt: null
}));
console.log(JSON.stringify({ candidates: stale.length, entries: stale }, null, 2));

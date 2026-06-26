#!/usr/bin/env node
/**
 * OpenClaw Docs Index Status
 */

const fs = require('fs');
const path = require('path');

const INDEX_DIR = path.join(process.env.HOME, '.openclaw/docs-index');
const INDEX_PATH = path.join(INDEX_DIR, 'openclaw-docs.sqlite');
const META_PATH = path.join(INDEX_DIR, 'index-meta.json');

console.log('📊 OpenClaw Docs Index Status\n');

if (!fs.existsSync(META_PATH)) {
  console.log('❌ Index not found');
  console.log('   Run: node ~/.openclaw/skills/search-openclaw-docs/scripts/docs-index.js rebuild\n');
  process.exit(1);
}

const meta = JSON.parse(fs.readFileSync(META_PATH, 'utf8'));

console.log(`Files indexed: ${meta.filesIndexed}`);
console.log(`Indexed at: ${meta.indexedAt}`);
console.log(`Build time: ${meta.buildTimeSeconds}s`);

if (fs.existsSync(INDEX_PATH)) {
  const stats = fs.statSync(INDEX_PATH);
  console.log(`Index size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
}

const indexDate = new Date(meta.indexedAt);
const now = new Date();
const daysSinceIndex = Math.floor((now - indexDate) / (1000 * 60 * 60 * 24));

if (daysSinceIndex > 7) {
  console.log(`\n⚠️  Index is ${daysSinceIndex} days old - consider rebuilding`);
}

console.log(`\nSearch mode: 📝 FTS5 keyword search (fully offline)`);

console.log('\n' + '─'.repeat(40));
if (fs.existsSync(INDEX_PATH) && meta.filesIndexed > 0) {
  console.log('✅ Index ready');
} else {
  console.log('❌ Index needs rebuild');
}

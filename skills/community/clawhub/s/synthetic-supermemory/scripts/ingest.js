#!/usr/bin/env node
/**
 * Ingest markdown files from a directory into Supermemory.
 * Uses customId for upsert — unchanged files are skipped, changed files
 * are updated in-place rather than creating duplicate documents.
 *
 * Usage:
 *   node ingest.js --dir /path/to/workspace --container my-agent
 *   node ingest.js --file /path/to/file.md --container my-agent
 *   node ingest.js --dir . --container my-agent --force   # re-ingest all
 */

const Supermemory = require('supermemory').default;
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };
const has = (flag) => args.includes(flag);

const dir = get('--dir');
const file = get('--file');
const container = get('--container') || get('-c');
const force = has('--force');

if (!container) { console.error('Error: --container is required'); process.exit(1); }
if (!dir && !file) { console.error('Error: --dir or --file is required'); process.exit(1); }

const apiKey = process.env.SUPERMEMORY_API_KEY;
if (!apiKey) { console.error('Error: SUPERMEMORY_API_KEY not set'); process.exit(1); }

const client = new Supermemory({ apiKey });

// State tracks: filePath -> { mtime, documentId }
const stateFile = path.join(path.dirname(__filename), '.ingest-state.json');

function loadState() {
  try { return JSON.parse(fs.readFileSync(stateFile, 'utf8')); }
  catch { return {}; }
}

function saveState(state) {
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
}

function mtime(p) {
  try { return fs.statSync(p).mtimeMs; }
  catch { return 0; }
}

// Skip directories that should never be ingested
const SKIP_DIRS = new Set(['node_modules', '.git', 'skills', 'scripts', 'projects', 'tmp', 'dist', 'build', 'extensions']);

function collectFiles(dirPath, exts = ['.md', '.txt'], depth = 0) {
  if (depth > 3) return []; // safety limit
  const results = [];
  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) {
        results.push(...collectFiles(full, exts, depth + 1));
      }
    } else if (entry.isFile() && exts.some(e => entry.name.endsWith(e))) {
      results.push(full);
    }
  }
  return results;
}

// Stable customId: container + sanitized file path (no secrets in the ID)
function customId(filePath, containerTag) {
  const sanitized = filePath.replace(/[^a-zA-Z0-9_\-./]/g, '_').slice(-80);
  return `${containerTag}__${sanitized}`.replace(/[^a-zA-Z0-9_:-]/g, '_').slice(0, 100);
}

async function ingestFile(filePath, containerTag, state) {
  const mt = mtime(filePath);
  const key = filePath;
  const entry = state[key] || {};

  if (!force && entry.mtime === mt) return 'skip'; // unchanged

  const content = fs.readFileSync(filePath, 'utf8').trim();
  if (!content) return 'empty';

  const label = path.basename(filePath);
  const cid = customId(filePath, containerTag);
  const docContent = `[${label}]\n\n${content}`;
  const metadata = { source: 'file', path: filePath, updatedAt: new Date().toISOString() };

  if (entry.documentId && !force) {
    // UPDATE existing document in-place — no new document created
    console.log(`🔄 [${containerTag}] ${label} (updated)`);
    await client.documents.update(entry.documentId, {
      content: docContent,
      containerTag,
      metadata,
    });
    state[key] = { mtime: mt, documentId: entry.documentId };
  } else {
    // CREATE with customId so future updates can find it
    console.log(`📥 [${containerTag}] ${label} (new)`);
    const result = await client.documents.add({
      content: docContent,
      containerTag,
      customId: cid,
      metadata,
    });
    state[key] = { mtime: mt, documentId: result.id };
  }

  await new Promise(r => setTimeout(r, 300)); // gentle rate limit
  return 'ingested';
}

async function main() {
  const state = loadState();
  let created = 0, updated = 0, skipped = 0;

  const files = file ? [file] : collectFiles(dir);

  for (const f of files) {
    const result = await ingestFile(f, container, state);
    if (result === 'ingested') {
      const isNew = !(state[f]?.documentId);
      isNew ? created++ : updated++;
    } else if (result === 'skip') {
      skipped++;
    }
  }

  saveState(state);

  if (created + updated > 0) {
    console.log(`\n✨ ${created} new, ${updated} updated, ${skipped} unchanged — container: ${container}`);
  } else {
    console.log(`✓ All ${skipped} file(s) unchanged (container: ${container})`);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });

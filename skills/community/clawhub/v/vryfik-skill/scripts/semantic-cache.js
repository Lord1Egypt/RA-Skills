#!/usr/bin/env node
'use strict';

/**
 * Semantic Cache — Vector similarity cache backed by local JSON file
 *
 * ClawHub Security: FILE SYSTEM ONLY.
 * Read/write limited to CACHE_DIR (default: ~/.antigravity/search-cache/).
 * No network access. No eval. No dynamic code.
 *
 * Commands:
 *   node scripts/semantic-cache.js check '{"query":"...","intent":"..."}'
 *   node scripts/semantic-cache.js write '{"query":"...","intent":"...","result":"..."}'
 *   node scripts/semantic-cache.js evict   (remove expired/LRU entries)
 *   node scripts/semantic-cache.js stats
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const CACHE_DIR      = path.join(os.homedir(), '.antigravity', 'search-cache');
const CACHE_FILE     = path.join(CACHE_DIR, 'index.json');
const SIMILARITY_THRESHOLD = 0.82;   // minimum cosine similarity for a hit
const TTL_MS         = 24 * 60 * 60 * 1000;  // 24 hours
const MAX_ENTRIES    = 1000;
const MAX_RESULT_LEN = 8000;  // chars — prevents unbounded cache growth

// ---------------------------------------------------------------------------
// TF-IDF bag-of-words vector (no external deps)
// ---------------------------------------------------------------------------
const STOPWORDS = new Set([
  'a','an','the','is','are','was','were','be','been','being','have','has','had',
  'do','does','did','will','would','could','should','may','might','shall','can',
  'to','of','in','for','on','with','at','by','from','up','about','as','into',
  'through','during','including','until','before','after','since','without',
  'under','within','along','following','across','behind','beyond','plus',
  'except','and','or','but','not','no','nor','so','yet','both','either',
  'how','what','when','where','who','why','which','that','this','these','those',
  '的','了','在','是','我','有','和','就','不','人','都','一','一个','上','也','很',
  '到','说','要','去','你','会','着','没有','看','好','自己','这'
]);

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff\s]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length > 1 && !STOPWORDS.has(t));
}

function buildVector(tokens) {
  const freq = {};
  for (const t of tokens) freq[t] = (freq[t] || 0) + 1;
  return freq;
}

function cosineSimilarity(vecA, vecB) {
  const keysA = Object.keys(vecA);
  if (keysA.length === 0) return 0;

  let dot = 0, magA = 0, magB = 0;
  for (const k of keysA) {
    dot  += vecA[k] * (vecB[k] || 0);
    magA += vecA[k] ** 2;
  }
  for (const v of Object.values(vecB)) magB += v ** 2;

  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

function queryToVector(query, intent) {
  const composite = `${intent} ${query}`;
  return buildVector(tokenize(composite));
}

// ---------------------------------------------------------------------------
// Cache I/O
// ---------------------------------------------------------------------------
function ensureCacheDir() {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true, mode: 0o700 });
  }
}

function loadCache() {
  ensureCacheDir();
  if (!fs.existsSync(CACHE_FILE)) return [];
  try {
    const raw = fs.readFileSync(CACHE_FILE, 'utf8');
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function saveCache(entries) {
  ensureCacheDir();
  // Atomic write: write to temp file then rename
  const tmp = `${CACHE_FILE}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(entries, null, 0), { mode: 0o600 });
  fs.renameSync(tmp, CACHE_FILE);
}

// ---------------------------------------------------------------------------
// Operations
// ---------------------------------------------------------------------------
function checkCache(query, intent) {
  const entries = loadCache();
  const now     = Date.now();
  const qVec    = queryToVector(query, intent);
  let   best    = null;
  let   bestSim = 0;

  for (const entry of entries) {
    // Skip expired
    if (now - entry.ts > TTL_MS) continue;
    // Skip wrong intent
    if (entry.intent !== intent) continue;

    const sim = cosineSimilarity(qVec, entry.vec);
    if (sim > bestSim) {
      bestSim = sim;
      best    = entry;
    }
  }

  if (best && bestSim >= SIMILARITY_THRESHOLD) {
    return { hit: true, result: best.result, similarity: +bestSim.toFixed(4), age_ms: now - best.ts };
  }
  return { hit: false, similarity: +bestSim.toFixed(4) };
}

function writeCache(query, intent, result) {
  const entries = loadCache();
  const now     = Date.now();

  // Evict expired
  const active = entries.filter(e => now - e.ts <= TTL_MS);

  // LRU evict if at capacity
  if (active.length >= MAX_ENTRIES) {
    active.sort((a, b) => b.ts - a.ts);  // newest first
    active.splice(MAX_ENTRIES - 1);
  }

  active.push({
    query:  query.slice(0, 300),
    intent,
    vec:    queryToVector(query, intent),
    result: String(result).slice(0, MAX_RESULT_LEN),
    ts:     now
  });

  saveCache(active);
  return { written: true, totalEntries: active.length };
}

function evictCache() {
  const entries = loadCache();
  const now     = Date.now();
  const active  = entries.filter(e => now - e.ts <= TTL_MS);
  saveCache(active);
  return { removed: entries.length - active.length, remaining: active.length };
}

function statsCache() {
  const entries = loadCache();
  const now     = Date.now();
  const active  = entries.filter(e => now - e.ts <= TTL_MS);
  const byIntent = {};
  for (const e of active) byIntent[e.intent] = (byIntent[e.intent] || 0) + 1;
  return { total: entries.length, active: active.length, byIntent };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const cmd = process.argv[2];
  const arg = process.argv[3];

  switch (cmd) {
    case 'check': {
      const { query, intent } = JSON.parse(arg);
      console.log(JSON.stringify(checkCache(query, intent)));
      break;
    }
    case 'write': {
      const { query, intent, result } = JSON.parse(arg);
      console.log(JSON.stringify(writeCache(query, intent, result)));
      break;
    }
    case 'evict':
      console.log(JSON.stringify(evictCache()));
      break;
    case 'stats':
      console.log(JSON.stringify(statsCache()));
      break;
    default:
      console.error('Usage: node scripts/semantic-cache.js <check|write|evict|stats> [json]');
      process.exit(1);
  }
}

main();

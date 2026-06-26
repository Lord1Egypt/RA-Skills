#!/usr/bin/env node
/**
 * supermemory — AI Memory Engine CLI
 *
 * Usage:
 *   node sm.mjs add "Customer fact or insight"
 *   node sm.mjs search "query about customers"
 *   node sm.mjs list [type] [--limit N]
 *   node sm.mjs forget <id>
 *   node sm.mjs stats
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

const MEMORY_DIR = join(process.env.OPENCLAW_HOME || join(process.env.HOME, '.openclaw'), 'memory', 'vectors');

// Ensure directory exists
if (!existsSync(MEMORY_DIR)) mkdirSync(MEMORY_DIR, { recursive: true });

const MEMORY_TYPES = ['customer_fact', 'conversation_insight', 'market_signal', 'effective_script'];
const TTL_DAYS = { customer_fact: null, conversation_insight: 90, market_signal: 30, effective_script: null };

function generateId(text) {
  return createHash('sha256').update(text + Date.now()).digest('hex').slice(0, 12);
}

function addMemory(text, type = 'conversation_insight', metadata = {}) {
  const id = generateId(text);
  const memory = {
    id,
    text,
    type,
    metadata,
    created_at: new Date().toISOString(),
    ttl_days: TTL_DAYS[type] || null,
  };

  writeFileSync(join(MEMORY_DIR, `${id}.json`), JSON.stringify(memory, null, 2));
  console.log(`Added memory: ${id} (${type})`);
  return id;
}

function searchMemories(query, limit = 5) {
  // Simple keyword search fallback (replace with vector search when embedding provider is configured)
  const queryWords = query.toLowerCase().split(/\s+/);
  const results = [];

  for (const file of readdirSync(MEMORY_DIR).filter(f => f.endsWith('.json'))) {
    try {
      const memory = JSON.parse(readFileSync(join(MEMORY_DIR, file), 'utf-8'));

      // Check TTL
      if (memory.ttl_days) {
        const age = (Date.now() - new Date(memory.created_at).getTime()) / 86400000;
        if (age > memory.ttl_days) continue;
      }

      // Simple relevance scoring
      const textLower = memory.text.toLowerCase();
      const score = queryWords.reduce((s, w) => s + (textLower.includes(w) ? 1 : 0), 0);
      if (score > 0) results.push({ ...memory, score });
    } catch { /* skip corrupt files */ }
  }

  return results.sort((a, b) => b.score - a.score).slice(0, limit);
}

function listMemories(type, limit = 20) {
  const memories = [];
  for (const file of readdirSync(MEMORY_DIR).filter(f => f.endsWith('.json'))) {
    try {
      const memory = JSON.parse(readFileSync(join(MEMORY_DIR, file), 'utf-8'));
      if (!type || memory.type === type) memories.push(memory);
    } catch { /* skip */ }
  }
  return memories
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, limit);
}

function forgetMemory(id) {
  const path = join(MEMORY_DIR, `${id}.json`);
  if (existsSync(path)) {
    const { unlinkSync } = await import('fs');
    unlinkSync(path);
    console.log(`Deleted: ${id}`);
  } else {
    console.error(`Not found: ${id}`);
    process.exit(1);
  }
}

function stats() {
  const files = readdirSync(MEMORY_DIR).filter(f => f.endsWith('.json'));
  const counts = {};
  for (const file of files) {
    try {
      const { type } = JSON.parse(readFileSync(join(MEMORY_DIR, file), 'utf-8'));
      counts[type] = (counts[type] || 0) + 1;
    } catch { /* skip */ }
  }
  console.log(`Total memories: ${files.length}`);
  for (const [type, count] of Object.entries(counts)) {
    console.log(`  ${type}: ${count}`);
  }
}

// CLI
const [,, command, ...args] = process.argv;
switch (command) {
  case 'add':
    addMemory(args[0], args[1] || 'conversation_insight');
    break;
  case 'search':
    console.log(JSON.stringify(searchMemories(args[0], parseInt(args[1]) || 5), null, 2));
    break;
  case 'list':
    console.log(JSON.stringify(listMemories(args[0], parseInt(args[1]) || 20), null, 2));
    break;
  case 'forget':
    forgetMemory(args[0]);
    break;
  case 'stats':
    stats();
    break;
  default:
    console.log('Usage: sm.mjs <add|search|list|forget|stats> [args]');
}

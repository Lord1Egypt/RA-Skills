/**
 * Memory Trace - 决策追溯链
 * 
 * 功能:
 * - 追溯记忆的来源和决策背景
 * - 显示决策链条（A → B → C）
 * - 支持时间线视图
 * 
 * Ported from memory_trace.py
 */

import { existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const MEMORIES_FILE = join(MEMORY_DIR, 'memories.json');
const TRACE_FILE = join(MEMORY_DIR, 'decision_traces.json');

// ============================================================
// Utilities
// ============================================================

/**
 * Load traces from file
 * @returns {{ traces: object, chains: Array }}
 */
export function loadTraces() {
  if (existsSync(TRACE_FILE)) {
    try {
      return JSON.parse(readFileSync(TRACE_FILE, 'utf-8'));
    } catch {
      // ignore
    }
  }
  return { traces: {}, chains: [] };
}

/**
 * Save traces to file
 * @param {{ traces: object, chains: Array }} traces
 */
export function saveTraces(traces) {
  // Ensure directory exists
  const { mkdirSync } = require('fs');
  mkdirSync(MEMORY_DIR, { recursive: true });
  require('fs').writeFileSync(TRACE_FILE, JSON.stringify(traces, null, 2), 'utf-8');
}

/**
 * Find a memory by ID (partial match)
 * @param {Array} memories
 * @param {string} memId
 * @returns {object|null}
 */
export function findMemoryById(memories, memId) {
  for (const m of memories) {
    const id = m.id || '';
    if (id.startsWith(memId) || id.includes(memId) || memId.includes(id.slice(-8))) {
      return m;
    }
  }
  return null;
}

/**
 * Find related memories based on keywords and time
 * @param {Array} memories
 * @param {object} mem
 * @returns {Array<object>}
 */
export function findRelatedMemories(memories, mem) {
  const related = [];
  const text = mem.text || '';
  
  // Extract Chinese keywords (simplified)
  const keywords = new Set();
  const chineseRegex = /[\u4e00-\u9fff]+/g;
  let match;
  while ((match = chineseRegex.exec(text)) !== null) {
    keywords.add(match[0]);
  }

  for (const m of memories) {
    if ((m.id || '') === (mem.id || '')) continue;

    const mText = m.text || '';
    const mKeywords = new Set();
    while ((match = chineseRegex.exec(mText)) !== null) {
      mKeywords.add(match[0]);
    }

    // Keyword overlap count
    const overlap = new Set([...keywords].filter(k => mKeywords.has(k))).size;
    if (overlap >= 2) {
      m.relevance = overlap;
      related.push(m);
    }
  }

  // Sort by relevance descending
  related.sort((a, b) => (b.relevance || 0) - (a.relevance || 0));
  return related.slice(0, 5);
}

// ============================================================
// Core Trace Functions
// ============================================================

/**
 * Trace a memory's origin and related chain
 * @param {string} memId
 * @returns {object}
 */
export function traceMemory(memId) {
  const memories = getAllMemories();
  const traces = loadTraces();

  const mem = findMemoryById(memories, memId);
  if (!mem) {
    return { error: `未找到记忆: ${memId}` };
  }

  // Find related memories
  const related = findRelatedMemories(memories, mem);

  // Build trace chain
  /** @type {object} */
  const chain = {
    target: {
      id: mem.id,
      text: (mem.text || '').slice(0, 100),
      timestamp: mem.timestamp || mem.created_at || '',
      category: mem.category
    },
    related: related.map(m => ({
      id: m.id,
      text: (m.text || '').slice(0, 60),
      relevance: m.relevance
    })),
    timeline: []
  };

  // Timeline (sorted by time)
  /** @type {Array} */
  const timelineMemories = [mem, ...related];
  timelineMemories.sort((a, b) => {
    const ta = a.timestamp || a.created_at || '';
    const tb = b.timestamp || b.created_at || '';
    return ta.localeCompare(tb);
  });

  for (const m of timelineMemories) {
    chain.timeline.push({
      timestamp: m.timestamp || m.created_at || '',
      text: (m.text || '').slice(0, 50),
      id: m.id
    });
  }

  return chain;
}

/**
 * Show decision timeline
 * @param {number} limit
 * @returns {Array<object>}
 */
export function showTimeline(limit = 10) {
  const memories = getAllMemories();

  // Filter decision category memories
  const decisions = memories
    .filter(m => m.category === 'decision')
    .sort((a, b) => {
      const ta = a.timestamp || a.created_at || '';
      const tb = b.timestamp || b.created_at || '';
      return tb.localeCompare(ta); // newest first
    })
    .slice(0, limit);

  return decisions.map((d, i) => ({
    order: i + 1,
    timestamp: d.timestamp || d.created_at || '',
    text: (d.text || '').slice(0, 80),
    id: d.id
  }));
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string|null} memId
 * @param {object} args
 * @returns {object}
 */
export function cmdTrace(memId, args = {}) {
  const { timeline = false, limit = 10 } = args;

  if (timeline) {
    const tl = showTimeline(parseInt(limit));
    const lines = ['📅 决策时间线\n'];
    if (tl.length === 0) {
      lines.push('  暂无决策记录');
    } else {
      for (const t of tl) {
        lines.push(`  [${t.order}] ${t.timestamp.slice(0, 10)}`);
        lines.push(`      ${t.text}...`);
        lines.push('');
      }
    }
    return { type: 'text', text: lines.join('\n') };
  }

  if (!memId) {
    return {
      type: 'text',
      text: 'Usage: trace <memory-id> [--timeline] [--limit N]'
    };
  }

  const chain = traceMemory(memId);

  if (chain.error) {
    return { type: 'text', text: `❌ ${chain.error}` };
  }

  const lines = [`🔍 追溯记忆: ${memId}\n`];
  lines.push('📍 目标记忆:');
  lines.push(`   ${chain.target.text}...`);
  lines.push(`   ID: ${chain.target.id}`);
  lines.push(`   时间: ${chain.target.timestamp}`);

  if (chain.related && chain.related.length > 0) {
    lines.push('\n🔗 相关记忆:');
    for (const r of chain.related) {
      lines.push(`   [${r.relevance} 关键词] ${r.text}...`);
    }
  }

  if (chain.timeline && chain.timeline.length > 1) {
    lines.push('\n📅 时间线:');
    for (const t of chain.timeline) {
      lines.push(`   ${t.timestamp.slice(0, 10)} | ${t.text}...`);
    }
  }

  return { type: 'text', text: lines.join('\n') };
}

export default {
  getAllMemories,
  loadTraces,
  saveTraces,
  findMemoryById,
  findRelatedMemories,
  traceMemory,
  showTimeline,
  cmdTrace
};

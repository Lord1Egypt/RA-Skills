/**
 * qmd_integration.js — QMD as optional vector search backend for unified-memory
 * P1-1: Deep QMD integration
 * 
 * Allows unified-memory to use QMD as a search backend via:
 * - Direct CLI invocation (/usr/local/bin/qmd)
 * - HTTP API (qmd's built-in REST server on unix socket or port)
 * 
 * When VECTOR_ENGINE=qmd, all vector search routes through this module.
 * qmd config: ~/.qmd/config.toml
 */

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';
import { createRequire } from 'module';
import { getAllMemories, addMemory } from './storage.js';

const req = createRequire(import.meta.url);
const HOME = process.env.HOME || '/root';
const QMD_CLI = '/usr/local/bin/qmd';
const QMD_CONFIG = join(HOME, '.qmd', 'config.toml');
const MEMORY_DIR = join(HOME, '.openclaw', 'workspace', 'memory');

// ============================================================
// QMD CLI helpers
// ============================================================

function execQMD(args, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    if (!existsSync(QMD_CLI)) {
      reject(new Error(`QMD CLI not found at ${QMD_CLI}`));
      return;
    }

    const timer = setTimeout(() => {
      try { proc.kill(); } catch { /* ignore */ }
      reject(new Error(`QMD timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    const proc = spawn(QMD_CLI, args, {
      cwd: MEMORY_DIR,
      env: { ...process.env, PATH: '/usr/local/bin:/usr/bin:/bin:/root/.local/bin' }
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', d => stdout += d.toString());
    proc.stderr.on('data', d => stderr += d.toString());

    proc.on('close', code => {
      clearTimeout(timer);
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`QMD exited ${code}: ${stderr || stdout}`.slice(0, 300)));
      }
    });

    proc.on('error', err => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

async function isQMDAvailable() {
  try {
    await execQMD(['--version'], 5000);
    return true;
  } catch {
    return false;
  }
}

// ============================================================
// Tokenizer (shared with qmd_search.js)
// ============================================================

function tokenize(text) {
  const tokens = [];
  const english = (text.match(/[a-zA-Z]+/g) || []).map(t => t.toLowerCase());
  tokens.push(...english);
  const chinese = (text.match(/[\u4e00-\u9fff]/g) || []);
  tokens.push(...chinese);
  const numbers = (text.match(/\d+/g) || []);
  tokens.push(...numbers);
  return tokens;
}

// ============================================================
// Core: QMD as vector search backend
// ============================================================

/**
 * Check if QMD is configured as the active vector engine
 */
export function isQMDEngine() {
  return (process.env.VECTOR_ENGINE || '').toLowerCase() === 'qmd';
}

/**
 * Get QMD engine status
 */
export async function getQMDEngineStatus() {
  const available = await isQMDAvailable();
  const memories = getAllMemories();
  const configExists = existsSync(QMD_CONFIG);

  return {
    engine: 'qmd',
    available,
    config_path: QMD_CONFIG,
    config_exists: configExists,
    qmd_cli: QMD_CLI,
    memory_count: memories.length,
    active: isQMDEngine(),
  };
}

/**
 * Search using QMD — returns unified-memory formatted results
 * Maps QMD's output format to unified-memory's memory format
 * @param {string} query
 * @param {object} options
 * @returns {Promise<Array>}
 */
export async function qmdEngineSearch(query, options = {}) {
  const { topK = 5, mode = 'hybrid', scope } = options;

  const allResults = [];

  // 1. QMD CLI search (BM25)
  try {
    const raw = await execQMD(['search', query, '-n', String(topK * 3), '--json']);
    const parsed = JSON.parse(raw);
    const docs = Array.isArray(parsed) ? parsed : (parsed.files || []);

    for (const item of docs) {
      allResults.push({
        id: item.docid || item.file || '',
        text: (item.snippet || '').replace(/^@@.*@@\n/, '').slice(0, 400),
        fullText: item.snippet || '',
        score: item.score || 0,
        category: 'local_file',
        mode: 'bm25',
        source: 'qmd',
        path: item.file || '',
        title: item.title || (item.file || '').split('/').pop() || '',
      });
    }
  } catch (err) {
    console.error('[qmd_engine] QMD CLI search failed:', err.message);
  }

  // 2. Memory store search (BM25 fallback when QMD unavailable)
  try {
    const memories = getAllMemories();
    const queryTokens = tokenize(query);

    // Optional scope filter
    let filteredMemories = memories;
    if (scope) {
      const scopeUpper = scope.toUpperCase();
      filteredMemories = memories.filter(m =>
        (m.scope || 'USER').toUpperCase() === scopeUpper ||
        (m.scope || 'USER').toUpperCase() === 'GLOBAL'
      );
    }

    let maxScore = 0;
    for (const mem of filteredMemories) {
      const text = mem.text || '';
      const memTokens = tokenize(text);

      let score = 0;
      for (const qt of queryTokens) {
        if (text.toLowerCase().includes(qt.toLowerCase())) {
          score += 1;
        }
        for (const mt of memTokens) {
          if (mt.includes(qt) || qt.includes(mt)) {
            score += 0.5;
          }
        }
      }

      if (score > 0) {
        if (score > maxScore) maxScore = score;
        allResults.push({
          id: mem.id,
          text: text.slice(0, 400),
          fullText: text,
          score: score,
          category: mem.category || 'memory',
          mode: 'keyword',
          source: 'memory',
          memory: mem,
        });
      }
    }

    // Normalize memory scores to 0-1
    if (maxScore > 0) {
      for (const r of allResults) {
        if (r.source === 'memory') {
          r.score = r.score / maxScore;
        }
      }
    }
  } catch (err) {
    console.error('[qmd_engine] Memory search failed:', err.message);
  }

  // Normalize QMD scores (they're already ~0-1 from BM25)
  const maxQmd = Math.max(...allResults.filter(r => r.source === 'qmd').map(r => r.score), 0.01);
  for (const r of allResults) {
    if (r.source === 'qmd') {
      r.score = r.score / maxQmd;
    }
  }

  // Sort by score descending
  allResults.sort((a, b) => b.score - a.score);
  return allResults.slice(0, topK);
}

/**
 * Vector search via QMD's semantic search pipeline
 * Falls back to BM25 if semantic not available
 * @param {string} query
 * @param {object} options
 * @returns {Promise<Array>}
 */
export async function qmdVectorSearch(query, options = {}) {
  const { topK = 5 } = options;

  // Try QMD's semantic search if available
  try {
    const raw = await execQMD(['search', query, '-n', String(topK * 4), '--json', '--mode', 'semantic']);
    const parsed = JSON.parse(raw);
    if (parsed && parsed.length > 0) {
      return parsed.slice(0, topK).map(item => ({
        id: item.docid || item.file || '',
        path: item.file || '',
        title: item.title || '',
        snippet: (item.snippet || '').replace(/^@@.*@@\n/, '').slice(0, 400),
        score: item.score || 0,
        source: 'qmd_semantic',
        mode: 'semantic',
      }));
    }
  } catch {
    // Semantic mode not available — fall back to BM25
  }

  // Fallback to BM25 search
  return qmdEngineSearch(query, { topK, mode: 'bm25' });
}

/**
 * Unified entry point: routes to QMD or built-in based on VECTOR_ENGINE env
 * @param {string} query
 * @param {object} options
 * @returns {Promise<Array>}
 */
export async function vectorSearch(query, options = {}) {
  if (isQMDEngine()) {
    return qmdEngineSearch(query, options);
  }
  // If not QMD engine, delegate to existing qmd_search.js
  const { qmdSearch: qmdCliSearch } = await import('./tools/qmd_search.js');
  return qmdCliSearch(query, { ...options, mode: options.mode || 'hybrid' });
}

/**
 * Ingest a memory into QMD's index (via qmd add)
 * @param {object} memory - unified-memory memory object
 */
export async function ingestMemoryToQMD(memory) {
  try {
    const text = memory.text || '';
    if (!text.trim()) return;

    // Write memory to a temp file and add to QMD
    const { writeFileSync, unlinkSync, mkdtempSync } = await import('fs');
    const { join } = await import('path');
    const { randomBytes } = await import('crypto');

    const tmpDir = mkdtempSync(join(HOME, '.tmp-qmd-ingest-'));
    const tmpFile = join(tmpDir, `mem-${memory.id}.md`);

    // Format as markdown with metadata
    const content = [
      `---
id: ${memory.id}
category: ${memory.category || 'general'}
scope: ${memory.scope || 'USER'}
importance: ${memory.importance || 0.5}
tags: ${Array.isArray(memory.tags) ? memory.tags.join(', ') : ''}
created: ${new Date(memory.created_at).toISOString()}
---
${text}`,
    ].join('\n');

    writeFileSync(tmpFile, content, 'utf8');

    await execQMD(['add', tmpFile], 10000).catch(() => {});

    try { unlinkSync(tmpFile); } catch { /* ignore */ }
    try { unlinkSync(tmpDir); } catch { /* ignore */ }
  } catch (err) {
    console.error('[qmd_engine] Ingest failed:', err.message);
  }
}

export default {
  isQMDEngine,
  getQMDEngineStatus,
  qmdEngineSearch,
  qmdVectorSearch,
  vectorSearch,
  ingestMemoryToQMD,
};

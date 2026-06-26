/**
 * qmd_search.js - QMD-style search integration
 * Calls external QMD CLI at /usr/local/bin/qmd
 * 
 * Features:
 * - BM25 keyword search (local, no LLM)
 * - Ollama vector semantic search (nomic-embed-text, local)
 * - Hybrid fusion (BM25 + vector)
 * - Snippet-level return (save tokens)
 */

import { spawn } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';

const OLLAMA_BASE = 'http://192.168.2.155:11434';
const EMBED_MODEL = 'nomic-embed-text';

// ============ Ollama Embedding ============

async function getOllamaEmbedding(text) {
  try {
    const response = await fetch(`${OLLAMA_BASE}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: EMBED_MODEL, prompt: text }),
      signal: AbortSignal.timeout(15000),
    });
    if (!response.ok) throw new Error(`Ollama ${response.status}`);
    const data = await response.json();
    return data.embedding || [];
  } catch (err) {
    console.error('[Ollama Embed] error:', err.message);
    return null;
  }
}

function cosineSimilarity(a, b) {
  if (!a || !b || a.length !== b.length) return 0;
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}

async function ollamaVectorSearch(query, docs, topK = 5) {
  const queryEmb = await getOllamaEmbedding(query);
  if (!queryEmb) return docs.slice(0, topK);
  
  const scored = docs.map(doc => ({
    ...doc,
    vectorScore: cosineSimilarity(queryEmb, doc.embedding || []),
  }));
  
  scored.sort((a, b) => b.vectorScore - a.vectorScore);
  return scored.slice(0, topK);
}

const QMD_CLI = '/usr/local/bin/qmd';
const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw/workspace/memory');

/**
 * Execute QMD CLI command
 */
function execQMD(args) {
  return new Promise((resolve, reject) => {
    if (!existsSync(QMD_CLI)) {
      reject(new Error(`QMD CLI not found at ${QMD_CLI}`));
      return;
    }

    const proc = spawn(QMD_CLI, args, {
      cwd: MEMORY_DIR,
      timeout: 10000,
      env: { ...process.env, PATH: '/usr/local/bin:/usr/bin:/bin:/root/.local/bin' }
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', d => stdout += d.toString());
    proc.stderr.on('data', d => stderr += d.toString());

    proc.on('close', code => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`QMD exited with code ${code}: ${stderr || stdout}`));
      }
    });

    proc.on('error', reject);
  });
}

/**
 * Execute QMD CLI command with hard timeout
 */
function execQMDTimed(args, timeoutMs = 8000) {
  return new Promise((resolve, reject) => {
    process.stderr.write(`[QMD DEBUG] execQMDTimed: args=${JSON.stringify(args)}\n`);
    
    if (!existsSync(QMD_CLI)) {
      process.stderr.write(`[QMD DEBUG] QMD CLI not found at ${QMD_CLI}\n`);
      reject(new Error(`QMD CLI not found at ${QMD_CLI}`));
      return;
    }

    const timer = setTimeout(() => {
      process.stderr.write('[QMD DEBUG] QMD timed out\n');
      try { proc.kill(); } catch {}
      reject(new Error(`QMD timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    const proc = spawn(QMD_CLI, args, { cwd: MEMORY_DIR, env: { ...process.env, PATH: '/usr/local/bin:/usr/bin:/bin:/root/.local/bin' } });
    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', d => stdout += d.toString());
    proc.stderr.on('data', d => stderr += d.toString());

    proc.on('close', code => {
      clearTimeout(timer);
      process.stderr.write(`[QMD DEBUG] QMD close: code=${code}, stdout_len=${stdout.length}, stderr=${stderr?.slice(0,100)}\n`);
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`QMD exited ${code}: ${stderr || stdout}`.slice(0, 200)));
      }
    });

    proc.on('error', err => {
      clearTimeout(timer);
      process.stderr.write(`[QMD DEBUG] QMD error: ${err.message}\n`);
      reject(err);
    });
  });
}

/**
 * Check if QMD CLI is available
 */
export async function isQMDAvailable() {
  try {
    await execQMD(['--version']);
    return true;
  } catch {
    return false;
  }
}

/**
 * Search using QMD CLI — searches both local files AND memory store
 * @param {string} query - Search query
 * @param {object} options - Search options
 * @returns {Promise<Array>} Search results from both sources
 */
export async function qmdSearch(query, options = {}) {
  const {
    topK = 5,
    mode = 'hybrid', // 'bm25', 'vector', 'hybrid'
    snippetSize = 200
  } = options;

  const allResults = [];

  // 1. Search local files via QMD CLI (BM25 mode, fast, no LLM needed)
  try {
    const available = await isQMDAvailable();
    console.error('[QMD Search] QMD available:', available);
    if (available) {
      // Use qmd search (BM25 keyword) instead of qmd query (needs LLM/HyDE)
      console.error('[QMD Search] Running QMD CLI with args:', ['search', query, '-n', String(topK * 2), '--json']);
      const raw = await execQMDTimed(['search', query, '-n', String(topK * 2), '--json']);
      console.error('[QMD Search] QMD raw output length:', raw.length);
      const parsed = JSON.parse(raw);
      
      // QMD returns a top-level array directly
      const docs = Array.isArray(parsed) ? parsed : (parsed.files || []);
      for (const item of docs) {
        allResults.push({
          id: item.docid || item.file || item.title || '',
          text: (item.snippet || '').replace(/^@@.*@@\n/, '').slice(0, snippetSize),
          fullText: item.snippet || '',
          score: (item.score || 0) * 10, // Scale QMD BM25 (0-1) to comparable range
          category: 'local_file',
          mode: 'bm25',
          source: 'qmd',
          path: item.file || '',
          title: item.title || (item.file || '').split('/').pop() || '',
        });
      }
    }
  } catch (err) {
    console.error('[QMD Search] QMD CLI error (local files):', err.message);
  }

  // 2. Also search memory store (unified-memory)
  let maxMemoryScore = 0;
  try {
    const memories = getAllMemories();
    const queryTokens = tokenize(query);

    for (const mem of memories) {
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
        if (score > maxMemoryScore) maxMemoryScore = score;
        allResults.push({
          id: mem.id,
          text: text.slice(0, snippetSize),
          fullText: text,
          score,  // raw score, will normalize after
          category: mem.category || 'memory',
          mode: 'keyword',
          source: 'memory',
          memory: mem,
        });
      }
    }
  } catch (err) {
    console.error('[QMD Search] Memory search error:', err.message);
  }

  // Normalize: QMD scores are already 0-1, memory scores need normalization
  const maxQ = Math.max(...allResults.filter(r => r.source === 'qmd').map(r => r.score), 0.01);
  for (const r of allResults) {
    if (r.source === 'qmd') {
      r.score = r.score / maxQ; // Normalize QMD to relative
    } else {
      r.score = r.score / maxMemoryScore; // Normalize memory to 0-1
    }
  }

  // Sort combined normalized results by score
  allResults.sort((a, b) => b.score - a.score);
  return allResults.slice(0, topK);
}

/**
 * Fallback search when QMD CLI is unavailable
 */
function fallbackSearch(query, topK) {
  const memories = getAllMemories();
  
  if (memories.length === 0) {
    return [];
  }

  const queryTokens = tokenize(query.toLowerCase());
  const results = [];

  for (const mem of memories) {
    const text = (mem.text || '').toLowerCase();
    const memTokens = tokenize(text);
    
    let score = 0;
    for (const qt of queryTokens) {
      if (text.includes(qt)) {
        score += 1;
      }
      for (const mt of memTokens) {
        if (mt.includes(qt) || qt.includes(mt)) {
          score += 0.5;
        }
      }
    }

    if (score > 0) {
      results.push({
        id: mem.id,
        text: (mem.text || '').slice(0, 200),
        score: score,
        category: mem.category || 'general',
        mode: 'fallback',
        memory: mem
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, topK);
}

/**
 * Simple tokenizer (supports Chinese + English)
 */
function tokenize(text) {
  const tokens = [];
  // English words
  const english = text.match(/[a-zA-Z]+/g) || [];
  tokens.push(...english.map(t => t.toLowerCase()));
  // Chinese characters
  const chinese = text.match(/[\u4e00-\u9fff]/g) || [];
  tokens.push(...chinese);
  // Numbers
  const numbers = text.match(/\d+/g) || [];
  tokens.push(...numbers);
  return tokens;
}

/**
 * Get context for a query (optimized for token limits)
 */
export async function getQMDContext(query, maxChars = 2000) {
  const results = await qmdSearch(query, { topK: 10, snippetSize: 200 });
  
  const parts = [];
  let total = 0;

  for (const r of results) {
    const snippet = r.text || '';
    if (total + snippet.length > maxChars) {
      break;
    }
    parts.push(`- [${r.category}|${r.mode}] ${snippet}`);
    total += snippet.length;
  }

  return parts.join('\n');
}

/**
 * Get QMD status
 */
export async function getQMDStatus() {
  const available = await isQMDAvailable();
  const memories = getAllMemories();
  
  return {
    qmd_available: available,
    qmd_path: QMD_CLI,
    documents: memories.length,
    mode: 'local'
  };
}

/**
 * Get a single document content by path
 * @param {string} path - Document path (qmd://workspace/... or relative)
 * @param {object} options - Options
 * @returns {Promise<object>} Document content
 */
export async function qmdGet(path, options = {}) {
  const { maxLines = 100, offset = 0 } = options;
  
  try {
    const available = await isQMDAvailable();
    if (!available) {
      return { error: 'QMD not available' };
    }
    
    // Build path:line range
    const range = offset > 0 ? `-l ${maxLines} -o ${offset}` : `-l ${maxLines}`;
    const raw = await execQMDTimed(['get', path, ...range.split(' ').filter(Boolean), '--json'], 10000);
    
    try {
      const parsed = JSON.parse(raw);
      return {
        path,
        content: parsed.content || raw,
        lines: parsed.lines || 0,
        truncated: (parsed.lines || 0) > maxLines,
        source: 'qmd',
      };
    } catch {
      // Fallback: raw text return
      return {
        path,
        content: raw,
        lines: raw.split('\n').length,
        truncated: false,
        source: 'qmd',
      };
    }
  } catch (err) {
    return { error: err.message, path };
  }
}

/**
 * Vector semantic search: QMD BM25 candidates → Ollama embeddings rerank
 * @param {string} query - Search query
 * @param {object} options - Options
 * @returns {Promise<Array>} Re-ranked results
 */
export async function qmdVSearch(query, options = {}) {
  const { topK = 5 } = options;
  
  try {
    const available = await isQMDAvailable();
    if (!available) {
      return { error: 'QMD not available' };
    }
    
    // QMD BM25 search — skip slow embedding re-ranking, QMD's own score is good enough
    // Old: QMD search → fetch 6 docs → Ollama embed all 6 → cosine re-rank (~3.3s)
    // New: QMD search → return results directly (~300ms)
    const raw = await execQMDTimed(['search', query, '-n', String(topK * 4), '--json'], 10000);
    const parsed = JSON.parse(raw);
    if (!parsed.length) return [];
    
    return parsed.slice(0, topK).map(item => ({
      id: item.docid || item.file || '',
      path: item.file || '',
      title: item.title || item.file?.split('/').pop() || '',
      snippet: item.snippet || '',
      score: item.score || 0,
      source: 'qmd_bm25',
    }));
  } catch (err) {
    return { error: err.message };
  }
}

/**
 * List indexed files in QMD collection
 * @param {string} pattern - Optional glob pattern
 * @param {number} limit - Max results
 * @returns {Promise<Array>} File list
 */
export async function qmdListFiles(pattern = '', limit = 20) {
  try {
    const available = await isQMDAvailable();
    if (!available) {
      return { error: 'QMD not available' };
    }
    
    // Use multi-get with --files to list file paths (text output, not JSON)
    const glob = pattern || '**/*.md';
    const raw = await execQMDTimed(['multi-get', glob, '-n', String(limit), '--files'], 10000);
    
    // Parse text output: "path/to/file.md\npath/to/file2.md\n..."
    const files = raw.split('\n')
      .map(l => l.trim())
      .filter(l => l && !l.includes('[SKIPPED]'))
      .slice(0, limit)
      .map(path => ({
        path,
        title: path.split('/').pop() || path,
        source: 'qmd',
      }));
    
    return { files, count: files.length };
  } catch (err) {
    return { error: err.message };
  }
}

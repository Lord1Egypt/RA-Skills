/**
 * Concurrent Search - 并发查询 v1.0
 * 
 * 功能:
 * - 并行多条件搜索
 * - 结果合并排序
 * - 超时控制
 * - 性能追踪
 * 
 * Ported from concurrent_search.py
 */

import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';

const HOME = homedir();
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';

const MAX_WORKERS = 4;
const DEFAULT_TIMEOUT = 30000;

// ============================================================
// Utilities
// ============================================================

function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length) return 0.0;

  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dot += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  const dA = Math.sqrt(normA);
  const dB = Math.sqrt(normB);

  return dA > 0 && dB > 0 ? dot / (dA * dB) : 0.0;
}

async function getEmbedding(text) {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }),
      signal: AbortSignal.timeout(10000),
    });
    if (response.ok) {
      const data = await response.json();
      return data.embedding || null;
    }
  } catch {}
  return null;
}

// ============================================================
// Concurrent Search
// ============================================================

export class ConcurrentSearch {
  constructor() {
    this.memories = this._loadMemories();
    this.stats = { searches: 0, total_time_ms: 0, concurrent_searches: 0 };
  }

  _loadMemories() {
    const memories = [];
    const file = join(MEMORY_DIR, 'memories.json');

    if (existsSync(file)) {
      try {
        const content = readFileSync(file, 'utf-8');
        const data = JSON.parse(content);
        if (Array.isArray(data)) {
          return data;
        }
        if (data.memories) {
          return data.memories;
        }
      } catch {}
    }

    return memories;
  }

  async _searchSingle(query, topK = 5) {
    const queryLower = query.toLowerCase();
    const results = [];

    // Text matching
    for (const mem of this.memories) {
      const text = (mem.text || '').toLowerCase();
      if (text.includes(queryLower)) {
        const score = (text.split(queryLower).length - 1) / text.length + 0.5;
        results.push({
          memory: mem,
          score: score,
          match_type: 'text',
        });
      }
    }

    // Vector search (optional)
    const queryVec = await getEmbedding(query);
    if (queryVec) {
      for (const mem of this.memories) {
        const memVec = mem.embedding;
        if (memVec) {
          const sim = cosineSimilarity(queryVec, memVec);
          if (sim > 0.7) {
            results.push({
              memory: mem,
              score: sim,
              match_type: 'vector',
            });
          }
        }
      }
    }

    // Deduplicate and sort
    const seen = new Set();
    const unique = [];
    for (const r of results.sort((a, b) => b.score - a.score)) {
      const memId = r.memory?.id;
      if (memId && !seen.has(memId)) {
        seen.add(memId);
        unique.push(r);
      }
    }

    return unique.slice(0, topK);
  }

  /**
   * Search with multiple queries concurrently
   * @param {string[]} queries
   * @param {number} topK
   * @param {number} timeout
   * @returns {Promise<Object[]>}
   */
  async searchMultiple(queries, topK = 5, timeout = DEFAULT_TIMEOUT) {
    const startTime = Date.now();
    this.stats.concurrent_searches++;

    const tasks = queries.map(async (query) => {
      const result = await Promise.race([
        this._searchSingle(query, topK),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Search timeout')), timeout)
        ),
      ]);
      return { query, results: result };
    });

    try {
      const results = await Promise.allSettled(tasks);
      const elapsed = Date.now() - startTime;

      this.stats.searches += queries.length;
      this.stats.total_time_ms += elapsed;

      return results
        .filter((r) => r.status === 'fulfilled')
        .flatMap((r) => r.value.results);
    } catch (e) {
      console.warn(`Search failed: ${e.message}`);
      return [];
    }
  }

  /**
   * Multi-condition search
   * @param {Object} conditions
   * @param {string} conditions.text
   * @param {string[]} conditions.tags
   * @param {string} conditions.category
   * @param {number} topK
   * @returns {Promise<Object[]>}
   */
  async multiSearch(conditions, topK = 10) {
    const { text, tags = [], category } = conditions;
    const startTime = Date.now();

    // Search by text
    const textResults = text ? await this._searchSingle(text, topK * 2) : [];

    // Filter by tags and category
    let filtered = textResults;

    if (tags.length > 0) {
      filtered = filtered.filter((r) => {
        const memTags = r.memory.tags || [];
        return tags.some((t) => memTags.includes(t));
      });
    }

    if (category) {
      filtered = filtered.filter((r) => r.memory.category === category);
    }

    const elapsed = Date.now() - startTime;
    this.stats.searches++;
    this.stats.total_time_ms += elapsed;

    return filtered.slice(0, topK);
  }

  getStats() {
    return {
      ...this.stats,
      avg_time_ms: this.stats.searches > 0
        ? (this.stats.total_time_ms / this.stats.searches).toFixed(2)
        : 0,
      memory_count: this.memories.length,
    };
  }
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  const searcher = new ConcurrentSearch();

  if (command === 'stats') {
    const stats = searcher.getStats();
    console.log('📊 Search Statistics:');
    console.log(`  Total searches: ${stats.searches}`);
    console.log(`  Total time: ${stats.total_time_ms}ms`);
    console.log(`  Avg time: ${stats.avg_time_ms}ms`);
    console.log(`  Memories loaded: ${stats.memory_count}`);
    return;
  }

  if (command === 'search') {
    const queriesArg = args.find((a) => a.startsWith('--queries='))?.split('=')[1];
    const topK = parseInt(args.find((a) => a.startsWith('--top-k='))?.split('=')[1] || '5');

    if (!queriesArg) {
      console.error('❌ 请指定 --queries=query1,query2,...');
      process.exit(1);
    }

    const queries = queriesArg.split(',').map((q) => q.trim());
    console.log(`🔍 Searching for: ${queries.join(', ')}`);

    const results = await searcher.searchMultiple(queries, topK);
    console.log(`\n✅ Found ${results.length} results:`);

    for (let i = 0; i < Math.min(results.length, 10); i++) {
      const r = results[i];
      console.log(`   [${(r.score * 100).toFixed(0)}%] ${(r.memory.text || '').slice(0, 60)}...`);
    }
    return;
  }

  if (command === 'multi') {
    const textArg = args.find((a) => a.startsWith('--text='))?.split('=')[1] || '';
    const tagsArg = args.find((a) => a.startsWith('--tags='))?.split('=')[1];
    const catArg = args.find((a) => a.startsWith('--category='))?.split('=')[1];
    const topK = parseInt(args.find((a) => a.startsWith('--top-k='))?.split('=')[1] || '10');

    const conditions = {
      text: textArg,
      tags: tagsArg ? tagsArg.split(',').map((t) => t.trim()) : [],
      category: catArg,
    };

    console.log(`🔍 Multi-condition search...`);
    const results = await searcher.multiSearch(conditions, topK);
    console.log(`\n✅ Found ${results.length} results:`);

    for (const r of results.slice(0, 10)) {
      console.log(`   [${(r.score * 100).toFixed(0)}%] ${(r.memory.text || '').slice(0, 60)}...`);
    }
    return;
  }

  if (command === 'benchmark') {
    console.log('📊 Running benchmark...');

    const testQueries = ['项目', '飞书', '任务', '进度', 'AI'];

    const startTime = Date.now();
    const results = await searcher.searchMultiple(testQueries, 10);
    const elapsed = Date.now() - startTime;

    console.log(`\n✅ Benchmark complete:`);
    console.log(`   Queries: ${testQueries.length}`);
    console.log(`   Results: ${results.length}`);
    console.log(`   Time: ${elapsed}ms`);
    console.log(`   Avg: ${(elapsed / testQueries.length).toFixed(2)}ms/query`);

    const stats = searcher.getStats();
    console.log(`\n📈 Overall stats:`);
    console.log(`   Searches: ${stats.searches}`);
    console.log(`   Total time: ${stats.total_time_ms}ms`);
    return;
  }

  console.log('Usage:');
  console.log('  node concurrent_search.js search --queries="飞书,微信" --top-k=5');
  console.log('  node concurrent_search.js multi --text="项目" --tags="重要" --category="决策"');
  console.log('  node concurrent_search.js benchmark');
  console.log('  node concurrent_search.js stats');
}

const isMain = process.argv[1]?.endsWith('concurrent_search.js') || process.argv[1]?.endsWith('concurrent_search.mjs');
if (isMain) {
  main().catch(console.error);
}

export default { ConcurrentSearch };

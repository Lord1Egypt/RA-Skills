/**
 * Memory Agent - Agent 专用内存接口
 * Ported from Python memory_agent.py
 * 
 * 功能:
 * - 快速上下文加载
 * - 预测性加载
 * - 增量更新
 * - 批量操作
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { hybridSearch } from '../fusion.js';
import { addMemory, getMemory, getAllMemories } from '../storage.js';
import { config } from '../config.js';
import { vectorSearch } from '../vector.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const CACHE_FILE = join(MEMORY_DIR, 'cache', 'agent_context.json');

// Ensure cache dir exists
if (!existsSync(join(MEMORY_DIR, 'cache'))) {
  mkdirSync(join(MEMORY_DIR, 'cache'), { recursive: true });
}

/**
 * 获取文本的向量嵌入
 * @param {string} text
 * @returns {Promise<number[]|null>}
 */
async function getEmbedding(text) {
  try {
    const response = await fetch(`${config.ollamaUrl}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: config.embedModel, prompt: text }),
    });
    if (response.ok) {
      const data = await response.json();
      return data.embedding || null;
    }
  } catch {
    // ignore
  }
  return null;
}

/**
 * 快速加载上下文
 * @param {string} [query='']
 * @param {number} [topK=10]
 * @returns {Promise<object>}
 */
export async function loadContext(query = '', topK = 10) {
  /** @type {object} */
  const result = {
    memories: [],
    stats: {},
    suggestions: [],
    load_time_ms: 0
  };

  const start = Date.now();

  try {
    // Use our hybrid search for retrieval
    const memories = await hybridSearch(query, topK, query ? 'hybrid' : 'bm25');
    
    result.memories = memories.map(r => ({
      id: r.memory?.id || r.memory?.text?.slice(0, 20),
      text: r.memory?.text || r.memory?.content || '',
      category: r.memory?.category || 'general',
      importance: r.memory?.importance || 0.5,
      _score: r.fusionScore || 0
    }));

    result.stats = {
      total: getAllMemories().length,
      loaded: result.memories.length
    };

    // 生成建议
    const categories = {};
    for (const m of result.memories) {
      const cat = m.category || 'unknown';
      categories[cat] = (categories[cat] || 0) + 1;
    }

    if (Object.keys(categories).length > 0) {
      const topCat = Object.entries(categories).sort((a, b) => b[1] - a[1])[0];
      result.suggestions.push(`主要关注: ${topCat[0]} (${topCat[1]}条)`);
    }

  } catch (e) {
    result.error = e.message;
  }

  result.load_time_ms = Date.now() - start;
  return result;
}

/**
 * 预测性加载 - 预测下一步可能需要的记忆
 * @param {string} [currentContext='']
 * @returns {string[]}
 */
export function predictLoad(currentContext = '') {
  const predictions = [];

  // 基于当前上下文预测
  const keywords = {
    '项目': ['进度', '状态', '负责人', '时间'],
    '会议': ['时间', '地点', '参与者', '议题'],
    '任务': ['截止', '优先级', '状态', '负责人'],
    '用户': ['偏好', '习惯', '联系方式', '历史'],
  };

  if (currentContext) {
    for (const [key, related] of Object.entries(keywords)) {
      if (currentContext.includes(key)) {
        predictions.push(...related);
      }
    }
  }

  return [...new Set(predictions)];
}

/**
 * 快速存储
 * @param {string} text
 * @param {string} [category='general']
 * @returns {Promise<boolean>}
 */
export async function quickStore(text, category = 'general') {
  try {
    // Get embedding
    const embedding = await getEmbedding(text);

    // Add to main storage
    addMemory({
      text,
      category,
      importance: 0.6,
      tags: ['quick-store']
    });

    // Note: Vector DB integration would go here if configured
    // For now we rely on the main storage.js which handles file-based storage

    return true;
  } catch (e) {
    console.error(`❌ 存储失败: ${e.message}`);
    return false;
  }
}

/**
 * 批量更新
 * @param {Array<object>} updates
 * @returns {Promise<object>}
 */
export async function batchUpdate(updates) {
  /** @type {{success: number, failed: number}} */
  const results = { success: 0, failed: 0 };

  for (const update of updates) {
    const text = update.text || '';
    const category = update.category || 'general';

    if (await quickStore(text, category)) {
      results.success++;
    } else {
      results.failed++;
    }
  }

  return results;
}

/**
 * 获取单条记忆
 * @param {string} memoryId
 * @returns {object|null}
 */
export function getMemoryById(memoryId) {
  const mem = getMemory(memoryId);
  if (!mem) return null;
  
  return {
    id: mem.id,
    text: mem.text || mem.content || '',
    category: mem.category || 'general',
    importance: mem.importance || 0.5,
    timestamp: mem.created_at ? new Date(mem.created_at).toISOString() : ''
  };
}

/**
 * MemoryAgent - Agent专用内存查询接口
 */
export class MemoryAgent {
  /**
   * 记忆召回（查询）
   * @param {string} query
   * @param {number} [topK=10]
   * @returns {Promise<object>}
   */
  async recall(query, topK = 10) {
    return await loadContext(query, topK);
  }

  /**
   * 存储记忆
   * @param {object} memory - { text, category?, importance?, tags? }
   * @returns {Promise<boolean>}
   */
  async store(memory) {
    return await quickStore(memory.text, memory.category || 'general');
  }

  /**
   * 反思 - 触发记忆系统的自我反思
   * @returns {Promise<object>}
   */
  async reflect() {
    // Check freshness
    const allMemories = getAllMemories();
    const now = Date.now();
    const weekAgo = now - 7 * 24 * 60 * 60 * 1000;
    
    /** @type {object[]} */
    const stale = [];
    for (const m of allMemories) {
      const age = m.updated_at || m.created_at || now;
      if (age < weekAgo) {
        stale.push(m);
      }
    }

    return {
      total_memories: allMemories.length,
      stale_memories: stale.length,
      recommendations: stale.length > 0
        ? ['部分记忆较旧，建议刷新或删除']
        : ['记忆状态良好']
    };
  }
}

/**
 * CLI entry
 */
export async function cmdMemoryAgent(args) {
  const { command, query, topK = 10, category = 'general', id } = args;

  if (command === 'load') {
    const result = await loadContext(query || '', topK);
    console.log(`⚡ 加载完成 (${result.load_time_ms}ms)`);
    console.log(`   记忆: ${result.stats.loaded}/${result.stats.total}`);

    if (result.suggestions?.length > 0) {
      console.log(`\n💡 建议:`);
      for (const s of result.suggestions) {
        console.log(`   ${s}`);
      }
    }

    if (result.memories?.length > 0) {
      console.log(`\n📚 记忆:`);
      for (const m of result.memories.slice(0, 5)) {
        console.log(`   [${m.category}] ${(m.text || '').slice(0, 40)}...`);
      }
    }
  } else if (command === 'context') {
    if (existsSync(CACHE_FILE)) {
      try {
        const cached = JSON.parse(readFileSync(CACHE_FILE, 'utf8'));
        console.log(`📦 缓存上下文 (${cached.length} 条)`);
      } catch {
        console.log('📦 无缓存上下文');
      }
    } else {
      console.log('📦 无缓存上下文，使用 load 命令加载');
    }
  } else if (command === 'quick-store') {
    if (!query) {
      console.log('请提供内容');
      return;
    }
    if (await quickStore(query, category)) {
      console.log(`✅ 已存储: ${query.slice(0, 40)}...`);
    } else {
      console.log('❌ 存储失败');
    }
  } else if (command === 'get') {
    const memoryId = id || query;
    if (!memoryId) {
      console.log('请提供记忆 ID');
      return;
    }
    const m = getMemoryById(memoryId);
    if (m) {
      console.log(JSON.stringify(m, null, 2));
    } else {
      console.log('❌ 未找到');
    }
  } else if (command === 'predict') {
    const predictions = predictLoad(query || '');
    if (predictions.length > 0) {
      console.log('🔮 预测相关:');
      for (const p of predictions) {
        console.log(`   - ${p}`);
      }
    } else {
      console.log('暂无预测');
    }
  }
}

// Export a singleton agent instance
export const memoryAgent = new MemoryAgent();

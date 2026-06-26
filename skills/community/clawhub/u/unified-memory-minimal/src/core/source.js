/**
 * Memory Source Tracker - 记忆来源溯源系统
 * 
 * 功能:
 * - 记录记忆来源Agent
 * - 追溯记忆创建者
 * - 冲突时确认来源
 * - 来源统计分析
 * 
 * Ported from memory_source.py
 */

import { existsSync, readFileSync, appendFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const SOURCE_DIR = join(MEMORY_DIR, 'source');
const SOURCE_FILE = join(SOURCE_DIR, 'sources.jsonl');

// ============================================================
// Utilities
// ============================================================

function ensureDirs() {
  if (!existsSync(SOURCE_DIR)) {
    mkdirSync(SOURCE_DIR, { recursive: true });
  }
  if (!existsSync(SOURCE_FILE)) {
    writeFileSync(SOURCE_FILE, '', 'utf-8');
  }
}

/**
 * Generate a short memory ID from text + timestamp
 * @param {string} text
 * @param {string} timestamp
 * @returns {string}
 */
function generateMemoryId(text, timestamp) {
  const hash = createHash('md5');
  hash.update(timestamp + text);
  return hash.digest('hex').slice(0, 12);
}

// ============================================================
// Core Functions
// ============================================================

/**
 * Store a memory with source tracking
 * @param {string} text
 * @param {string} agent
 * @param {string} category
 * @param {object} metadata
 * @returns {object}
 */
export function storeWithSource(text, agent, category = 'other', metadata = null) {
  ensureDirs();

  const timestamp = new Date().toISOString();
  const memoryId = generateMemoryId(text, timestamp);

  /** @type {object} */
  const sourceEntry = {
    memory_id: memoryId,
    timestamp,
    text,
    source_agent: agent,
    category,
    metadata: metadata || {},
    verified: false,
    conflicts: []
  };

  appendFileSync(SOURCE_FILE, JSON.stringify(sourceEntry, null, 2) + '\n', 'utf-8');

  return sourceEntry;
}

/**
 * Trace a memory's source
 * @param {string} memoryId
 * @returns {object|null}
 */
export function traceMemory(memoryId) {
  ensureDirs();

  const lines = readFileSync(SOURCE_FILE, 'utf-8').split('\n').filter(Boolean);
  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.memory_id === memoryId) {
        return entry;
      }
    } catch {
      continue;
    }
  }
  return null;
}

/**
 * Find memories by source agent
 * @param {string} agent
 * @param {number} limit
 * @returns {Array<object>}
 */
export function findByAgent(agent, limit = 20) {
  ensureDirs();

  const memories = [];
  const lines = readFileSync(SOURCE_FILE, 'utf-8').split('\n').filter(Boolean);

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.source_agent === agent) {
        memories.push(entry);
      }
    } catch {
      continue;
    }
  }

  memories.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  return memories.slice(0, limit);
}

/**
 * Find memories with conflicts
 * @returns {Array<object>}
 */
export function findConflicts() {
  ensureDirs();

  const conflicts = [];
  const lines = readFileSync(SOURCE_FILE, 'utf-8').split('\n').filter(Boolean);

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.conflicts && entry.conflicts.length > 0) {
        conflicts.push(entry);
      }
    } catch {
      continue;
    }
  }

  return conflicts;
}

/**
 * Verify a memory
 * @param {string} memoryId
 * @param {string} verifiedBy
 * @returns {object}
 */
export function verifyMemory(memoryId, verifiedBy) {
  ensureDirs();

  const lines = readFileSync(SOURCE_FILE, 'utf-8').split('\n').filter(Boolean);
  /** @type {string[]} */
  const entries = [];
  let verifiedEntry = null;

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      if (entry.memory_id === memoryId) {
        entry.verified = true;
        entry.verified_by = verifiedBy;
        entry.verified_at = new Date().toISOString();
        verifiedEntry = entry;
      }
      entries.push(entry);
    } catch {
      // keep invalid lines as-is
      entries.push(line);
    }
  }

  if (verifiedEntry) {
    writeFileSync(SOURCE_FILE, entries.map(e => typeof e === 'string' ? e : JSON.stringify(e)).join('\n') + '\n', 'utf-8');
  }

  return verifiedEntry || {};
}

/**
 * Get source statistics
 * @returns {object}
 */
export function getStats() {
  ensureDirs();

  /** @type {object} */
  const stats = {
    total: 0,
    by_agent: {},
    by_category: {},
    verified: 0,
    unverified: 0,
    conflicts: 0
  };

  const lines = readFileSync(SOURCE_FILE, 'utf-8').split('\n').filter(Boolean);

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      stats.total++;

      // By agent
      const agent = entry.source_agent || 'unknown';
      stats.by_agent[agent] = (stats.by_agent[agent] || 0) + 1;

      // By category
      const category = entry.category || 'other';
      stats.by_category[category] = (stats.by_category[category] || 0) + 1;

      // Verified
      if (entry.verified) {
        stats.verified++;
      } else {
        stats.unverified++;
      }

      // Conflicts
      if (entry.conflicts && entry.conflicts.length > 0) {
        stats.conflicts++;
      }
    } catch {
      continue;
    }
  }

  return stats;
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdSource(command, args) {
  switch (command) {
    case 'store': {
      const { text, agent, category = 'other' } = args;
      if (!text || !agent) {
        return { error: '缺少参数: --text, --agent' };
      }
      const entry = storeWithSource(text, agent, category);
      if (args.json) {
        return { type: 'json', data: entry };
      }
      return {
        type: 'text',
        text: `📝 存储记忆: [${entry.memory_id}] [${entry.source_agent}] ${entry.text.slice(0, 50)}...`
      };
    }

    case 'trace': {
      const { memoryId } = args;
      if (!memoryId) {
        return { error: '缺少参数: --memory-id' };
      }
      const entry = traceMemory(memoryId);
      if (!entry) {
        return { error: `❌ 记忆不存在: ${memoryId}` };
      }
      if (args.json) {
        return { type: 'json', data: entry };
      }
      return {
        type: 'text',
        text: `🔍 记忆来源: [${entry.memory_id}]\n` +
          `   来源Agent: ${entry.source_agent}\n` +
          `   时间: ${entry.timestamp}\n` +
          `   类别: ${entry.category}\n` +
          `   内容: ${entry.text.slice(0, 100)}...\n` +
          `   已验证: ${entry.verified ? '✅' : '❌'}`
      };
    }

    case 'find': {
      const { agent, limit = 20 } = args;
      if (!agent) {
        return { error: '缺少参数: --agent' };
      }
      const memories = findByAgent(agent, parseInt(limit));
      if (args.json) {
        return { type: 'json', data: memories };
      }
      return {
        type: 'text',
        text: `📋 [${agent}] 的记忆 (共 ${memories.length} 条)\n` +
          memories.map(m => `  [${m.memory_id}] ${m.text.slice(0, 50)}...`).join('\n')
      };
    }

    case 'conflicts': {
      const conflicts = findConflicts();
      if (args.json) {
        return { type: 'json', data: conflicts };
      }
      return {
        type: 'text',
        text: `⚠️ 冲突记忆 (共 ${conflicts.length} 条)\n` +
          conflicts.map(m => `  [${m.memory_id}] ${m.text.slice(0, 50)}...\n      冲突: ${JSON.stringify(m.conflicts)}`).join('\n')
      };
    }

    case 'verify': {
      const { memoryId, verifiedBy } = args;
      if (!memoryId || !verifiedBy) {
        return { error: '缺少参数: --memory-id, --verified-by' };
      }
      const entry = verifyMemory(memoryId, verifiedBy);
      if (args.json) {
        return { type: 'json', data: entry };
      }
      return {
        type: 'text',
        text: entry.memory_id
          ? `✅ 验证记忆: [${entry.memory_id}] 由 ${entry.verified_by} 验证`
          : `❌ 记忆不存在: ${memoryId}`
      };
    }

    case 'stats': {
      const stats = getStats();
      if (args.json) {
        return { type: 'json', data: stats };
      }
      return {
        type: 'text',
        text: `📊 来源统计\n` +
          `   总计: ${stats.total}\n` +
          `   按Agent: ${JSON.stringify(stats.by_agent)}\n` +
          `   按类别: ${JSON.stringify(stats.by_category)}\n` +
          `   已验证: ${stats.verified}\n` +
          `   未验证: ${stats.unverified}\n` +
          `   冲突数: ${stats.conflicts}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default {
  storeWithSource,
  traceMemory,
  findByAgent,
  findConflicts,
  verifyMemory,
  getStats,
  cmdSource
};

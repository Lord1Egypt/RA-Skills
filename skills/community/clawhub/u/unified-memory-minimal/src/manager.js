/**
 * manager.js - 统一记忆管理 v2.0
 * 
 * 整合功能:
 * - 记忆去重与合并
 * - 重要性衰减
 * - 记忆清理
 * - 统计报告
 * - 健康检查
 * 
 * 协调各个独立工具
 */

import { getAllMemories, saveMemories, loadMemories } from './storage.js';
import { config, log } from './utils/logger.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// 衰减配置
const DECAY_HALF_LIFE = 30;       // 30天半衰期
const DECAY_MIN_IMPORTANCE = 0.1; // 最低重要性

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const SNAPSHOT_DIR = join(MEMORY_DIR, 'snapshots');

// ============================================================
// 工具函数
// ============================================================

/**
 * 文本相似度（简单 Jaccard）
 * @param {string} s1
 * @param {string} s2
 * @returns {number}
 */
function textSimilarity(s1, s2) {
  const set1 = new Set(s1);
  const set2 = new Set(s2);
  const intersection = new Set([...set1].filter(x => set2.has(x)));
  const union = new Set([...set1, ...set2]);
  return union.size === 0 ? 0 : intersection.size / union.size;
}

// ============================================================
// 去重
// ============================================================

/**
 * 查找相似记忆对
 * @param {Array<object>} memories
 * @param {number} [threshold=0.85]
 * @returns {Array<{keep: object, remove: object, similarity: number}>}
 */
export function findDuplicates(memories, threshold = 0.85) {
  log('INFO', '开始查找重复记忆...');

  /** @type {Array<{keep: object, remove: object, similarity: number}>} */
  const duplicates = [];

  // 按类别分组
  /** @type {Map<string, Array<{idx: number, mem: object}>>} */
  const byCategory = new Map();
  for (let i = 0; i < memories.length; i++) {
    const cat = memories[i].category || 'general';
    if (!byCategory.has(cat)) {
      byCategory.set(cat, []);
    }
    byCategory.get(cat).push({ idx: i, mem: memories[i] });
  }

  // 检查每个类别内的重复
  for (const [category, items] of byCategory) {
    if (items.length < 2) continue;

    for (let i = 0; i < items.length; i++) {
      for (let j = i + 1; j < items.length; j++) {
        const m1 = items[i].mem;
        const m2 = items[j].mem;

        const sim = textSimilarity(m1.text || m1.content || '', m2.text || m2.content || '');

        if (sim > 0.6) {
          // 保留重要性更高的
          const [keep, remove] = m1.importance >= m2.importance
            ? [items[i], items[j]]
            : [items[j], items[i]];

          duplicates.push({
            keep: memories[keep.idx],
            remove: memories[remove.idx],
            similarity: sim
          });
        }
      }
    }
  }

  return duplicates;
}

/**
 * 执行去重
 * @param {object} args - { dryRun: boolean }
 * @returns {Promise<object>}
 */
export async function cmdDedup(args = { dryRun: true }) {
  const { dryRun = true } = args;
  const memories = getAllMemories();

  if (memories.length < 2) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: '记忆少于2条，无需去重', count: memories.length }, null, 2)
      }]
    };
  }

  const duplicates = findDuplicates(memories);

  if (duplicates.length === 0) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: '没有发现重复记忆', count: memories.length }, null, 2)
      }]
    };
  }

  // 执行删除（非 dry run）
  if (!dryRun) {
    const removeIds = new Set(duplicates.map(d => d.remove.id));
    const kept = memories.filter(m => !removeIds.has(m.id));
    saveMemories(kept);
  }

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: dryRun
          ? `发现 ${duplicates.length} 对重复记忆（预览模式）`
          : `已删除 ${duplicates.length} 条重复记忆`,
        total_memories: memories.length,
        duplicates_found: duplicates.length,
        duplicates: duplicates.slice(0, 10),
        action: dryRun ? 'preview' : 'applied'
      }, null, 2)
    }]
  };
}

// ============================================================
// 衰减
// ============================================================

/**
 * 应用重要性衰减
 * @param {object} args - { dryRun: boolean }
 * @returns {Promise<object>}
 */
export async function cmdDecay(args = { dryRun: true }) {
  const { dryRun = true } = args;
  const memories = getAllMemories();

  if (memories.length === 0) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: '没有记忆需要衰减' }, null, 2)
      }]
    };
  }

  const now = Date.now();
  /** @type {Array<{memory: object, old_importance: number, new_importance: number, days_old: number}>} */
  const decayed = [];

  for (const m of memories) {
    const createdAt = m.created_at || m.timestamp;
    if (!createdAt) continue;

    const daysOld = Math.floor((now - createdAt) / (1000 * 60 * 60 * 24));

    // 指数衰减
    const decayFactor = Math.pow(0.5, daysOld / DECAY_HALF_LIFE);
    const newImportance = Math.max(DECAY_MIN_IMPORTANCE, (m.importance || 0.5) * decayFactor);

    if (newImportance < (m.importance || 0.5) - 0.05) {
      decayed.push({
        memory: m,
        old_importance: m.importance || 0.5,
        new_importance: Math.round(newImportance * 100) / 100,
        days_old: daysOld
      });
    }
  }

  if (decayed.length === 0) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: '没有需要衰减的记忆' }, null, 2)
      }]
    };
  }

  // 执行更新（非 dry run）
  if (!dryRun) {
    for (const d of decayed) {
      const mem = memories.find(m => m.id === d.memory.id);
      if (mem) {
        mem.importance = d.new_importance;
        mem.updated_at = now;
      }
    }
    saveMemories(memories);
  }

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: dryRun
          ? `需要衰减 ${decayed.length} 条记忆（预览模式）`
          : `已更新 ${decayed.length} 条记忆的重要性`,
        total_memories: memories.length,
        decayed_count: decayed.length,
        samples: decayed.slice(0, 10),
        action: dryRun ? 'preview' : 'applied'
      }, null, 2)
    }]
  };
}

// ============================================================
// 清理
// ============================================================

/**
 * 清理过期记忆文件
 * @param {object} args - { days: number, dryRun: boolean }
 * @returns {Promise<object>}
 */
export async function cmdClean(args = { days: 30, dryRun: true }) {
  const { days = 30, dryRun = true } = args;
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;

  if (!existsSync(SNAPSHOT_DIR)) {
    mkdirSync(SNAPSHOT_DIR, { recursive: true });
  }

  /** @type {Array<{file: string, date: Date}>} */
  const toClean = [];

  try {
    const files = readdirSync(MEMORY_DIR);
    for (const file of files) {
      if (!file.endsWith('.md')) continue;
      
      // 跳过特殊目录和文件
      if (file === 'snapshots' || file === 'vector_cache') continue;
      
      const filePath = join(MEMORY_DIR, file);
      const stats = statSync(filePath);
      
      // 检查是否是文件（非目录）
      if (!stats.isFile()) continue;
      
      // 解析日期
      const dateStr = file.replace('.md', '');
      const fileDate = new Date(dateStr);
      
      if (!isNaN(fileDate.getTime()) && fileDate.getTime() < cutoff) {
        toClean.push({ file, date: fileDate });
      }
    }
  } catch (e) {
    log('WARN', '清理时读取目录失败:', e.message);
  }

  if (toClean.length === 0) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: `没有需要清理的记忆 (保留 ${days} 天)` }, null, 2)
      }]
    };
  }

  // 执行清理（非 dry run）
  if (!dryRun) {
    const { moveFile } = await import('./storage.js').catch(() => ({ moveFile: null }));
    for (const { file } of toClean) {
      try {
        // 简单移动到 snapshots 目录
        const src = join(MEMORY_DIR, file);
        const dst = join(SNAPSHOT_DIR, file);
        const { copyFileSync, unlinkSync } = await import('fs');
        copyFileSync(src, dst);
        unlinkSync(src);
      } catch (e) {
        log('WARN', `移动文件失败 ${file}:`, e.message);
      }
    }
  }

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: dryRun
          ? `发现 ${toClean.length} 个过期文件（预览模式）`
          : `已移动 ${toClean.length} 个文件到 snapshots`,
        files: toClean.map(f => ({ file: f.file, date: f.date.toISOString().slice(0, 10) })),
        action: dryRun ? 'preview' : 'applied'
      }, null, 2)
    }]
  };
}

// ============================================================
// 统计
// ============================================================

/**
 * 显示统计报告
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdStats(args = {}) {
  const memories = getAllMemories();

  // 基本统计
  const byCategory = new Map();
  let totalImportance = 0;

  for (const m of memories) {
    const cat = m.category || 'general';
    byCategory.set(cat, (byCategory.get(cat) || 0) + 1);
    totalImportance += m.importance || 0.5;
  }

  // 标签统计
  const tagCounts = new Map();
  for (const m of memories) {
    for (const tag of m.tags || []) {
      tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
    }
  }

  // 重要性分布
  const high = memories.filter(m => (m.importance || 0.5) > 0.6).length;
  const medium = memories.filter(m => {
    const imp = m.importance || 0.5;
    return imp >= 0.3 && imp <= 0.6;
  }).length;
  const low = memories.filter(m => (m.importance || 0.5) < 0.3).length;

  // 向量数据库检查
  let vectorCount = 0;
  try {
    const vectorCacheFile = join(VECTOR_DB_DIR, 'vectors.json');
    if (existsSync(vectorCacheFile)) {
      const data = JSON.parse(readFileSync(vectorCacheFile, 'utf8'));
      vectorCount = Array.isArray(data) ? data.length : (data.vectors?.length || 0);
    }
  } catch {
    // 向量数据库可能未初始化
  }

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        summary: {
          total_memories: memories.length,
          avg_importance: memories.length > 0 ? Math.round(totalImportance / memories.length * 100) / 100 : 0
        },
        by_category: Object.fromEntries(byCategory),
        by_tag: Object.fromEntries([...tagCounts.entries()].slice(0, 20)),
        importance_distribution: {
          high: high,
          medium: medium,
          low: low
        },
        vector_database: {
          count: vectorCount,
          coverage: memories.length > 0 ? Math.round(vectorCount / memories.length * 100) + '%' : '0%'
        }
      }, null, 2)
    }]
  };
}

// ============================================================
// 健康检查
// ============================================================

/**
 * 健康检查
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdHealth(args = {}) {
  /** @type {string[]} */
  const issues = [];
  const memories = getAllMemories();

  // 1. 检查向量覆盖率
  let vectorCount = 0;
  try {
    const vectorCacheFile = join(VECTOR_DB_DIR, 'vectors.json');
    if (existsSync(vectorCacheFile)) {
      const data = JSON.parse(readFileSync(vectorCacheFile, 'utf8'));
      vectorCount = Array.isArray(data) ? data.length : (data.vectors?.length || 0);
    }
  } catch {
    issues.push('向量数据库未初始化');
  }

  if (memories.length > 0) {
    const coverage = vectorCount / memories.length;
    if (coverage < 0.8) {
      issues.push(`向量覆盖率低: ${Math.round(coverage * 100)}% (${vectorCount}/${memories.length})`);
    }
  }

  // 2. 检查分类一致性
  const standardCategories = new Set(['profile', 'preferences', 'entities', 'events', 'cases', 'patterns', 'fact', 'learning', 'decision']);
  const categories = new Set(memories.map(m => m.category).filter(Boolean));
  const nonStandard = [...categories].filter(c => !standardCategories.has(c) && !c.startsWith('T='));
  if (nonStandard.length > 0) {
    issues.push(`非标准分类: ${nonStandard.join(', ')}`);
  }

  // 3. 检查过期记忆（超过90天）
  const oldCutoff = Date.now() - 90 * 24 * 60 * 60 * 1000;
  const oldMemories = memories.filter(m => {
    const created = m.created_at || m.timestamp;
    return created && created < oldCutoff;
  });
  if (oldMemories.length > 0) {
    issues.push(`超过90天的记忆: ${oldMemories.length} 条`);
  }

  // 4. 检查低重要性记忆
  const lowImportance = memories.filter(m => (m.importance || 0.5) < 0.2);
  if (lowImportance.length > 0) {
    issues.push(`低重要性记忆 (<0.2): ${lowImportance.length} 条`);
  }

  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        status: issues.length === 0 ? 'healthy' : 'issues_found',
        issue_count: issues.length,
        issues,
        recommendations: issues.length > 0
          ? [
              '运行 manager.cmdDedup({ dryRun: false }) 进行去重',
              '运行 manager.cmdDecay({ dryRun: false }) 应用衰减',
              '运行 manager.cmdClean({ days: 30, dryRun: false }) 清理过期'
            ]
          : []
      }, null, 2)
    }]
  };
}

// ============================================================
// 主入口
// ============================================================

/**
 * 统一管理命令（协调所有工具）
 * @param {object} args - { command: 'dedup'|'decay'|'clean'|'stats'|'health', ... }
 * @returns {Promise<object>}
 */
export async function cmdManager(args = {}) {
  const { command, ...rest } = args;

  switch (command) {
    case 'dedup':
      return cmdDedup(rest);
    case 'decay':
      return cmdDecay(rest);
    case 'clean':
      return cmdClean(rest);
    case 'stats':
      return cmdStats(rest);
    case 'health':
      return cmdHealth(rest);
    default:
      // Run all checks
      const [dedupResult, decayResult, statsResult, healthResult] = await Promise.all([
        cmdDedup({ dryRun: true }),
        cmdDecay({ dryRun: true }),
        cmdStats({}),
        cmdHealth({})
      ]);

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            message: 'Memory Manager 完整报告',
            dedup: JSON.parse(dedupResult.content[0].text),
            decay: JSON.parse(decayResult.content[0].text),
            stats: JSON.parse(statsResult.content[0].text),
            health: JSON.parse(healthResult.content[0].text)
          }, null, 2)
        }]
      };
  }
}

export default {
  findDuplicates,
  cmdDedup,
  cmdDecay,
  cmdClean,
  cmdStats,
  cmdHealth,
  cmdManager
};
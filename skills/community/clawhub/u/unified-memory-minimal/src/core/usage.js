/**
 * Memory Usage Analyzer - 记忆使用分析
 * 
 * 站在 AI Agent 用户角度，回答：
 * - 哪些记忆最有用？（访问频率）
 * - 哪些记忆浪费空间？（从未访问）
 * - 哪些记忆可能过时？（时效性）
 * - 记忆分布是否合理？（分类统计）
 * 
 * Ported from memory_usage.py
 */

import { existsSync, readFileSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const ACCESS_LOG_FILE = join(MEMORY_DIR, 'access_history.json');
const USAGE_REPORT_FILE = join(MEMORY_DIR, 'usage_report.json');

// ============================================================
// MemoryUsageAnalyzer
// ============================================================

export class MemoryUsageAnalyzer {
  constructor() {
    /** @type {Array<object>} */
    this.memories = this._loadMemories();
    /** @type {{ accesses: Array, co_occurrences: object }} */
    this.accessLog = this._loadAccessLog();
  }

  /**
   * Load memories from storage
   * @returns {Array<object>}
   */
  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      return getAllMemories();
    } catch {
      // Fallback: try loading from file
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          return Array.isArray(data) ? data : (data.memories || []);
        } catch {
          // ignore
        }
      }
    }
    return [];
  }

  /**
   * Load access log
   * @returns {{ accesses: Array, co_occurrences: object }}
   */
  _loadAccessLog() {
    if (existsSync(ACCESS_LOG_FILE)) {
      try {
        return JSON.parse(readFileSync(ACCESS_LOG_FILE, 'utf-8'));
      } catch {
        // ignore
      }
    }
    return { accesses: [], co_occurrences: {} };
  }

  /**
   * Full analysis
   * @returns {object}
   */
  analyze() {
    const result = {
      total: this.memories.length,
      categories: {},
      access_stats: {},
      stale_memories: [],
      unused_memories: [],
      top_memories: [],
      recommendations: []
    };

    // 1. Category counts
    for (const m of this.memories) {
      const cat = m.category || 'general';
      result.categories[cat] = (result.categories[cat] || 0) + 1;
    }

    // 2. Access counts
    /** @type {Map<string, number>} */
    const accessCounts = new Map();
    for (const acc of this.accessLog.accesses || []) {
      const id = acc.id || acc.memory_id || '';
      accessCounts.set(id, (accessCounts.get(id) || 0) + 1);
    }

    // 3. Most accessed memories
    const sortedByAccess = [...accessCounts.entries()].sort((a, b) => b[1] - a[1]);
    for (const [memId, count] of sortedByAccess.slice(0, 5)) {
      const mem = this.memories.find(m => m.id === memId);
      if (mem) {
        result.top_memories.push({
          id: memId,
          text: (mem.text || '').slice(0, 50) + '...',
          access_count: count,
          category: mem.category
        });
      }
    }

    // 4. Never accessed memories
    for (const mem of this.memories) {
      if (!accessCounts.has(mem.id)) {
        result.unused_memories.push({
          id: mem.id,
          text: (mem.text || '').slice(0, 50) + '...',
          category: mem.category || 'general',
          importance: mem.importance || 0.5
        });
      }
    }

    // 5. Stale memories (>30 days old + low importance)
    const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
    for (const mem of this.memories) {
      const created = mem.created_at || mem.timestamp;
      if (!created) continue;
      const createdMs = typeof created === 'number' ? created : new Date(created).getTime();
      if (createdMs < cutoff && (mem.importance || 0.5) < 0.5) {
        const ageDays = Math.floor((Date.now() - createdMs) / (24 * 60 * 60 * 1000));
        result.stale_memories.push({
          id: mem.id,
          text: (mem.text || '').slice(0, 50) + '...',
          age_days: ageDays,
          importance: mem.importance || 0.5
        });
      }
    }

    // 6. Recommendations
    if (result.unused_memories.length > this.memories.length * 0.3) {
      result.recommendations.push({
        type: 'cleanup',
        message: `有 ${result.unused_memories.length} 条记忆从未被访问，建议清理或降低重要性`
      });
    }
    if (result.stale_memories.length > 5) {
      result.recommendations.push({
        type: 'archive',
        message: `有 ${result.stale_memories.length} 条记忆可能已过时，建议归档`
      });
    }
    if (result.top_memories.length === 0) {
      result.recommendations.push({
        type: 'usage',
        message: '没有访问记录，建议开始使用记忆系统'
      });
    }

    // 7. Access stats summary
    result.access_stats = {
      total_accesses: (this.accessLog.accesses || []).length,
      unique_accessed: accessCounts.size,
      never_accessed: this.memories.length - accessCounts.size,
      avg_access_per_memory: this.memories.length > 0
        ? Math.round((this.accessLog.accesses || []).length / Math.max(accessCounts.size, 1) * 100) / 100
        : 0
    };

    return result;
  }

  /**
   * Cleanup suggestions
   * @returns {object}
   */
  cleanupSuggest() {
    const analysis = this.analyze();

    /** @type {object} */
    const suggestions = {
      can_delete: [],
      can_archive: [],
      can_merge: [],
      can_boost: []
    };

    // Can delete: low importance + never accessed + >30 days
    for (const mem of analysis.unused_memories) {
      if (mem.importance < 0.3) {
        suggestions.can_delete.push(mem);
      }
    }

    // Can archive: stale
    suggestions.can_archive = analysis.stale_memories;

    // Can merge: similar content (simple keyword overlap)
    const texts = this.memories.map(m => ({ id: m.id, text: m.text || '' }));
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) {
        const words1 = new Set(texts[i].text.split(/\s+/));
        const words2 = new Set(texts[j].text.split(/\s+/));
        const intersection = new Set([...words1].filter(w => words2.has(w)));
        const union = new Set([...words1, ...words2]);
        const overlap = union.size > 0 ? intersection.size / union.size : 0;
        if (overlap > 0.6) {
          suggestions.can_merge.push({
            id1: texts[i].id,
            id2: texts[j].id,
            similarity: Math.round(overlap * 100) / 100,
            text1: texts[i].text.slice(0, 30) + '...',
            text2: texts[j].text.slice(0, 30) + '...'
          });
        }
      }
    }

    // Can boost: high access but low importance
    /** @type {Map<string, number>} */
    const accessCounts = new Map();
    for (const acc of this.accessLog.accesses || []) {
      const id = acc.id || acc.memory_id || '';
      accessCounts.set(id, (accessCounts.get(id) || 0) + 1);
    }
    for (const [memId, count] of accessCounts) {
      if (count > 3) {
        const mem = this.memories.find(m => m.id === memId);
        if (mem && (mem.importance || 0.5) < 0.7) {
          suggestions.can_boost.push({
            id: memId,
            text: (mem.text || '').slice(0, 50) + '...',
            current_importance: Math.round((mem.importance || 0.5) * 100) / 100,
            suggested_importance: Math.round(Math.min(0.9, (mem.importance || 0.5) + 0.2) * 100) / 100,
            access_count: count
          });
        }
      }
    }

    return suggestions;
  }

  /**
   * Usage report for recent N days
   * @param {number} days
   * @returns {object}
   */
  usageReport(days = 7) {
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;

    /** @type {Array} */
    const recentAccesses = [];
    for (const acc of this.accessLog.accesses || []) {
      const accTime = acc.timestamp || acc.access_time;
      if (!accTime) continue;
      const accMs = typeof accTime === 'number' ? accTime : new Date(accTime).getTime();
      if (accMs > cutoff) {
        recentAccesses.push(acc);
      }
    }

    // Daily access counts
    /** @type {Map<string, number>} */
    const dailyAccess = new Map();
    for (const acc of recentAccesses) {
      const ts = acc.timestamp || acc.access_time;
      if (!ts) continue;
      const dateStr = new Date(ts).toISOString().slice(0, 10);
      dailyAccess.set(dateStr, (dailyAccess.get(dateStr) || 0) + 1);
    }

    // Category access
    /** @type {Map<string, number>} */
    const categoryAccess = new Map();
    for (const acc of recentAccesses) {
      const memId = acc.id || acc.memory_id;
      const mem = this.memories.find(m => m.id === memId);
      if (mem) {
        const cat = mem.category || 'general';
        categoryAccess.set(cat, (categoryAccess.get(cat) || 0) + 1);
      }
    }

    // Most active day
    let mostActiveDay = null;
    let maxCount = 0;
    for (const [date, count] of dailyAccess) {
      if (count > maxCount) {
        maxCount = count;
        mostActiveDay = date;
      }
    }

    return {
      period_days: days,
      total_accesses: recentAccesses.length,
      daily_access: Object.fromEntries([...dailyAccess.entries()].sort()),
      category_access: Object.fromEntries([...categoryAccess.entries()].sort()),
      avg_daily: Math.round(recentAccesses.length / days * 10) / 10,
      most_active_day: mostActiveDay
    };
  }

  /**
   * Get score for a single memory
   * @param {string} memId
   * @returns {object}
   */
  getMemoryScore(memId) {
    const mem = this.memories.find(m => m.id === memId);
    if (!mem) {
      return { error: 'Memory not found' };
    }

    // Access count
    let accessCount = 0;
    let recentAccess = null;
    const accesses = this.accessLog.accesses || [];
    for (let i = accesses.length - 1; i >= 0; i--) {
      const acc = accesses[i];
      if ((acc.id || acc.memory_id || '') === memId) {
        accessCount++;
        if (!recentAccess) {
          recentAccess = acc.timestamp || acc.access_time;
        }
      }
    }

    // Memory age
    const created = mem.created_at || mem.timestamp;
    const ageDays = created
      ? Math.floor((Date.now() - (typeof created === 'number' ? created : new Date(created).getTime())) / (24 * 60 * 60 * 1000))
      : 0;

    // Composite score
    const importance = mem.importance || 0.5;
    const accessScore = Math.min(accessCount / 10, 1) * 0.3;
    const freshnessScore = (1 - Math.min(ageDays / 365, 1)) * 0.3;
    const score = importance * 0.4 + accessScore + freshnessScore;

    const grade = score > 0.7 ? 'A' : score > 0.5 ? 'B' : score > 0.3 ? 'C' : 'D';

    return {
      id: memId,
      text: (mem.text || '').slice(0, 50) + '...',
      importance: Math.round(importance * 100) / 100,
      access_count: accessCount,
      age_days: ageDays,
      recent_access: recentAccess,
      score: Math.round(score * 1000) / 1000,
      grade
    };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdUsage(command, args) {
  const analyzer = new MemoryUsageAnalyzer();

  switch (command) {
    case 'analyze': {
      const result = analyzer.analyze();
      if (args.json) return { type: 'json', data: result };
      const lines = ['📊 记忆使用分析', '', `总记忆: ${result.total} 条`, '', '分类分布:'];
      for (const [cat, count] of Object.entries(result.categories)) {
        lines.push(`   ${cat || '未分类'}: ${count} 条`);
      }
      lines.push('', '访问统计:');
      const stats = result.access_stats;
      lines.push(`   总访问: ${stats.total_accesses} 次`);
      lines.push(`   已访问: ${stats.unique_accessed} 条`);
      lines.push(`   从未访问: ${stats.never_accessed} 条`);
      if (result.top_memories.length > 0) {
        lines.push('', '🔥 最常访问:');
        result.top_memories.forEach((m, i) => {
          lines.push(`   ${i + 1}. [${m.access_count}次] ${m.text}`);
        });
      }
      if (result.recommendations.length > 0) {
        lines.push('', '💡 建议:');
        result.recommendations.forEach(r => {
          lines.push(`   [${r.type}] ${r.message}`);
        });
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'cleanup-suggest': {
      const result = analyzer.cleanupSuggest();
      if (args.json) return { type: 'json', data: result };
      const lines = ['🧹 清理建议', ''];
      lines.push(`可删除: ${result.can_delete.length} 条`);
      result.can_delete.slice(0, 3).forEach(m => lines.push(`   - ${m.text}`));
      lines.push(`\n可归档: ${result.can_archive.length} 条`);
      result.can_archive.slice(0, 3).forEach(m => lines.push(`   - ${m.text}`));
      lines.push(`\n可合并: ${result.can_merge.length} 对`);
      result.can_merge.slice(0, 3).forEach(p => lines.push(`   - ${p.text1} ↔ ${p.text2}`));
      lines.push(`\n可提升重要性: ${result.can_boost.length} 条`);
      result.can_boost.slice(0, 3).forEach(m => lines.push(`   - ${m.text} (${m.current_importance} → ${m.suggested_importance})`));
      return { type: 'text', text: lines.join('\n') };
    }

    case 'usage-report': {
      const result = analyzer.usageReport(parseInt(args.days) || 7);
      if (args.json) return { type: 'json', data: result };
      const lines = [`📈 使用报告 (最近 ${result.period_days} 天)`, '', `总访问: ${result.total_accesses} 次`];
      lines.push(`日均: ${result.avg_daily} 次`);
      lines.push(`最活跃: ${result.most_active_day || 'N/A'}`);
      lines.push('\n每日访问:');
      for (const [date, count] of Object.entries(result.daily_access || {})) {
        const bar = '█'.repeat(Math.min(count, 20));
        lines.push(`   ${date}: ${bar} ${count}`);
      }
      lines.push('\n分类访问:');
      for (const [cat, count] of Object.entries(result.category_access || {})) {
        lines.push(`   ${cat || '未分类'}: ${count} 次`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'score': {
      if (!args.id) return { error: '请提供 --id' };
      const result = analyzer.getMemoryScore(args.id);
      if (result.error) return { error: result.error };
      if (args.json) return { type: 'json', data: result };
      return {
        type: 'text',
        text: `📊 记忆评分\n\n内容: ${result.text}\n` +
          `评分: ${result.score} (${result.grade})\n\n` +
          `重要性: ${result.importance}\n` +
          `访问次数: ${result.access_count}\n` +
          `记忆年龄: ${result.age_days} 天`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default {
  MemoryUsageAnalyzer,
  cmdUsage
};

/**
 * Memory Optimization - 记忆优化建议系统
 * 
 * 功能:
 * - 自动发现记忆问题
 * - 提供可操作的优化建议
 * - 生成优化报告
 * 
 * Ported from memory_optimization.py
 */

import { existsSync, readFileSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const ACCESS_LOG = join(MEMORY_DIR, 'access_history.json');

// ============================================================
// MemoryOptimizer
// ============================================================

export class MemoryOptimizer {
  constructor() {
    this.memories = this._loadMemories();
    this.accessLog = this._loadAccessLog();
  }

  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      return getAllMemories();
    } catch {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          return Array.isArray(data) ? data : (data.memories || []);
        } catch { /* ignore */ }
      }
      return [];
    }
  }

  _loadAccessLog() {
    if (existsSync(ACCESS_LOG)) {
      try {
        return JSON.parse(readFileSync(ACCESS_LOG, 'utf-8'));
      } catch { /* ignore */ }
    }
    return { accesses: [], co_occurrences: {} };
  }

  analyzeIssues() {
    /** @type {object} */
    const issues = {
      duplicates: [],
      low_importance_unused: [],
      stale: [],
      missing_category: [],
      too_short: [],
      inconsistent_formatting: []
    };

    // 1. Duplicate memories
    /** @type {Map<string, Array>} */
    const textCount = new Map();
    for (const m of this.memories) {
      const text = m.text || '';
      if (!textCount.has(text)) textCount.set(text, []);
      textCount.get(text).push(m);
    }
    for (const [text, mems] of textCount) {
      if (mems.length > 1) {
        issues.duplicates.push({
          text: text.slice(0, 100) + (text.length > 100 ? '...' : ''),
          count: mems.length,
          ids: mems.map(m => m.id)
        });
      }
    }

    // 2. Low importance + unused
    /** @type {Set<string>} */
    const accessedIds = new Set();
    for (const acc of (this.accessLog.accesses || [])) {
      accessedIds.add(acc.id || acc.memory_id);
    }
    for (const mem of this.memories) {
      if ((mem.importance || 0.5) < 0.3 && !accessedIds.has(mem.id)) {
        issues.low_importance_unused.push({
          id: mem.id,
          text: ((mem.text || '').slice(0, 100)) + ((mem.text || '').length > 100 ? '...' : ''),
          importance: mem.importance || 0.5
        });
      }
    }

    // 3. Stale memories (> 180 days)
    const cutoff = Date.now() - 180 * 24 * 60 * 60 * 1000;
    for (const mem of this.memories) {
      const ts = mem.created_at || mem.timestamp;
      if (!ts) continue;
      const tsMs = typeof ts === 'number' ? ts : new Date(ts).getTime();
      if (tsMs < cutoff) {
        const ageDays = Math.floor((Date.now() - tsMs) / (24 * 60 * 60 * 1000));
        issues.stale.push({
          id: mem.id,
          text: ((mem.text || '').slice(0, 100)) + ((mem.text || '').length > 100 ? '...' : ''),
          age_days: ageDays,
          importance: mem.importance || 0.5
        });
      }
    }

    // 4. Missing category
    for (const mem of this.memories) {
      if (!mem.category || mem.category === '') {
        issues.missing_category.push({
          id: mem.id,
          text: ((mem.text || '').slice(0, 100)) + ((mem.text || '').length > 100 ? '...' : '')
        });
      }
    }

    // 5. Too short
    for (const mem of this.memories) {
      if ((mem.text || '').length < 10) {
        issues.too_short.push({ id: mem.id, text: mem.text || '' });
      }
    }

    // 6. Stats
    /** @type {Map<string, number>} */
    const categories = new Map();
    for (const m of this.memories) {
      const cat = m.category || 'general';
      categories.set(cat, (categories.get(cat) || 0) + 1);
    }
    const totalImportance = this.memories.reduce((s, m) => s + (m.importance || 0.5), 0);

    return {
      total: this.memories.length,
      issues,
      stats: {
        categories: Object.fromEntries(categories),
        avg_importance: this.memories.length > 0
          ? Math.round(totalImportance / this.memories.length * 100) / 100
          : 0,
        total_accesses: (this.accessLog.accesses || []).length,
        unique_accessed: accessedIds.size
      }
    };
  }

  generateSuggestions() {
    const analysis = this.analyzeIssues();
    const issues = analysis.issues;
    /** @type {Array} */
    const suggestions = [];

    if (issues.duplicates.length > 0) {
      suggestions.push({
        priority: 'high',
        type: 'deduplicate',
        title: '合并重复记忆',
        description: `发现 ${issues.duplicates.length} 组重复记忆`,
        action: "运行 'mem optimize dedup' 自动处理",
        impact: `可减少 ${issues.duplicates.reduce((s, d) => s + d.count - 1, 0)} 条记忆`
      });
    }

    if (issues.low_importance_unused.length > 0) {
      suggestions.push({
        priority: 'medium',
        type: 'cleanup',
        title: '清理低价值记忆',
        description: `有 ${issues.low_importance_unused.length} 条低重要性且未使用的记忆`,
        action: "运行 'mem optimize cleanup' 审查后删除",
        impact: '提高记忆检索质量'
      });
    }

    if (issues.stale.length > 0) {
      suggestions.push({
        priority: 'medium',
        type: 'archive',
        title: '归档过时记忆',
        description: `有 ${issues.stale.length} 条记忆超过6个月未更新`,
        action: "运行 'mem optimize archive' 移至归档",
        impact: '减少活跃记忆负担'
      });
    }

    if (issues.missing_category.length > 0) {
      suggestions.push({
        priority: 'low',
        type: 'categorize',
        title: '标记未分类记忆',
        description: `有 ${issues.missing_category.length} 条记忆缺少分类`,
        action: "运行 'mem optimize tag' 添加适当分类",
        impact: '改善记忆组织结构'
      });
    }

    if (issues.too_short.length > 0) {
      suggestions.push({
        priority: 'low',
        type: 'enrich',
        title: '充实过短记忆',
        description: `有 ${issues.too_short.length} 条记忆过短（<10字符）`,
        action: '考虑补充信息或删除无价值内容',
        impact: '提高记忆信息密度'
      });
    }

    return suggestions;
  }

  getOptimizationReport() {
    const issues = this.analyzeIssues();
    const suggestions = this.generateSuggestions();

    const totalIssues = Object.values(issues.issues).reduce((s, v) => s + v.length, 0);
    const maxPossible = this.memories.length * 6;
    const healthScore = maxPossible > 0
      ? Math.max(0, 100 - Math.round((totalIssues / maxPossible) * 100))
      : 100;

    const priorityOrder = { high: 3, medium: 2, low: 1 };

    return {
      timestamp: new Date().toISOString(),
      health_score: healthScore,
      total_memories: issues.total,
      issues_summary: Object.fromEntries(
        Object.entries(issues.issues).map(([k, v]) => [k, v.length])
      ),
      suggestions,
      stats: issues.stats,
      recommended_actions: suggestions
        .sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority])
        .slice(0, 3)
        .map(s => s.action)
    };
  }

  applyOptimization(action) {
    const issues = this.analyzeIssues().issues;

    switch (action) {
      case 'dedup':
        return {
          action,
          success: true,
          details: {
            duplicate_groups: issues.duplicates.length,
            total_duplicates: issues.duplicates.reduce((s, d) => s + d.count - 1, 0)
          },
          message: `发现 ${issues.duplicates.length} 组重复，建议人工审查后合并`
        };
      case 'cleanup':
        return {
          action,
          success: true,
          details: { candidates: issues.low_importance_unused.length },
          message: `发现 ${issues.low_importance_unused.length} 条低价值记忆候选项，建议人工确认后删除`
        };
      case 'archive':
        return {
          action,
          success: true,
          details: { stale_count: issues.stale.length },
          message: `发现 ${issues.stale.length} 条过时记忆，建议归档至冷存储`
        };
      case 'stats':
        return {
          action,
          success: true,
          details: this.analyzeIssues().stats,
          message: '统计信息已生成'
        };
      default:
        return { action, success: false, message: `未知操作: ${action}` };
    }
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
export function cmdOptimization(command, args) {
  const optimizer = new MemoryOptimizer();

  switch (command) {
    case 'analyze': {
      const result = optimizer.analyzeIssues();
      const lines = [`🔍 记忆问题分析`, '', `总记忆: ${result.total} 条`, ''];
      for (const [issueType, items] of Object.entries(result.issues)) {
        if (items.length > 0) {
          lines.push(`${issueType}: ${items.length} 个`);
          for (const item of items.slice(0, 3)) {
            const text = typeof item === 'object' ? (item.text || JSON.stringify(item)) : String(item);
            lines.push(`   - ${text.slice(0, 60)}...`);
          }
        }
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'suggest': {
      const suggestions = optimizer.generateSuggestions();
      if (suggestions.length === 0) {
        return { type: 'text', text: '💡 优化建议\n   暂无建议，记忆状态良好！' };
      }
      const emoji = { high: '🔴', medium: '🟡', low: '🟢' };
      const lines = ['💡 优化建议'];
      suggestions.forEach((s, i) => {
        lines.push(`\n${i + 1}. ${emoji[s.priority]} ${s.title}`);
        lines.push(`   ${s.description}`);
        lines.push(`   行动: ${s.action}`);
        lines.push(`   影响: ${s.impact}`);
      });
      return { type: 'text', text: lines.join('\n') };
    }

    case 'report': {
      const report = optimizer.getOptimizationReport();
      const lines = [
        '📊 记忆优化报告',
        '',
        `健康分数: ${report.health_score}/100`,
        `总记忆: ${report.total_memories} 条`,
        '',
        '问题分布:'
      ];
      for (const [issue, count] of Object.entries(report.issues_summary)) {
        if (count > 0) lines.push(`   ${issue}: ${count}`);
      }
      if (report.recommended_actions.length > 0) {
        lines.push('\n📋 建议行动:');
        report.recommended_actions.forEach((a, i) => lines.push(`   ${i + 1}. ${a}`));
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'optimize': {
      if (!args.action) return { error: '请提供 --action (dedup/cleanup/archive/stats)' };
      const result = optimizer.applyOptimization(args.action);
      return {
        type: 'text',
        text: result.success
          ? `✅ ${result.message}\n   详情: ${JSON.stringify(result.details)}`
          : `❌ ${result.message}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { MemoryOptimizer, cmdOptimization };

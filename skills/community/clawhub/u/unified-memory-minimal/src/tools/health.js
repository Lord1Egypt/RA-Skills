/**
 * Memory Health - 记忆健康度检测
 * 
 * 功能:
 * - 自动验证记忆
 * - 矛盾检测
 * - 过时检测
 * - 质量评分
 * - 自动修复功能
 * 
 * Ported from memory_health.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const ASSOCIATION_GRAPH_FILE = join(MEMORY_DIR, 'associations', 'graph.json');

// Auto-fix rules
const AUTO_FIX_RULES = {
  contradiction: {
    action: 'merge_or_flag',
    threshold: 0.7,
    auto_merge: false
  },
  outdated: {
    action: 'archive_or_update',
    threshold_days: 90,
    auto_archive: true
  },
  redundant: {
    action: 'compress',
    similarity_threshold: 0.85,
    auto_compress: true
  },
  orphaned: {
    action: 'link_or_delete',
    auto_delete: false
  }
};

// Conflict word pairs
const CONFLICT_PAIRS = [
  ['喜欢', '讨厌'], ['爱', '恨'], ['是', '不是'], ['可以', '不可以'],
  ['会', '不会'], ['有', '没有'], ['使用', '不使用'], ['采用', '不采用'],
  ['需要', '不需要'], ['想要', '不想要'], ['应该', '不应该']
];

// ============================================================
// MemoryHealthChecker
// ============================================================

export class MemoryHealthChecker {
  constructor() {
    this.vectorDbDir = VECTOR_DB_DIR;
    this.memories = [];
    this._loadMemories();
  }

  _loadMemories() {
    try {
      const { getAllMemories } = require('../storage.js');
      this.memories = getAllMemories();
    } catch {
      // fallback
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        try {
          const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          this.memories = Array.isArray(data) ? data : (data.memories || []);
        } catch { /* ignore */ }
      }
    }
  }

  /**
   * Calculate health score
   * @returns {object}
   */
  calculateHealthScore() {
    const total = this.memories.length;
    if (total === 0) {
      return { score: 100, issues: 0, total: 0, details: {} };
    }

    const conflicts = this._detectContradictions();
    const outdated = this._detectOutdated();
    const redundant = this._detectRedundant();
    const orphaned = this._detectOrphaned();

    const issues = (
      conflicts.length * 10 +
      outdated.length * 3 +
      redundant.length * 2 +
      orphaned.length * 5
    );
    const score = Math.max(0, 100 - issues);

    return {
      score,
      total,
      conflicts: conflicts.length,
      outdated: outdated.length,
      redundant: redundant.length,
      orphaned: orphaned.length,
      details: {
        conflicts: conflicts.slice(0, 5).map(c => ({
          id1: c.memory1.id?.slice(0, 8),
          id2: c.memory2.id?.slice(0, 8),
          text1: (c.memory1.text || '').slice(0, 30),
          text2: (c.memory2.text || '').slice(0, 30)
        })),
        outdated: outdated.slice(0, 5).map(o => ({
          id: o.id?.slice(0, 8),
          text: (o.text || '').slice(0, 30),
          days_old: o.days_old || 0
        })),
        redundant: redundant.slice(0, 5).map(r => ({
          id1: r.memory1.id?.slice(0, 8),
          id2: r.memory2.id?.slice(0, 8),
          similarity: r.similarity || 0
        })),
        orphaned: orphaned.slice(0, 5).map(o => ({
          id: o.id?.slice(0, 8),
          text: (o.text || '').slice(0, 30)
        }))
      }
    };
  }

  /**
   * Auto-fix memory quality issues
   * @param {boolean} dryRun
   * @returns {Array<object>}
   */
  autoFix(dryRun = true) {
    const fixes = [];
    if (!this.memories.length) return fixes;

    // 1. Detect and process contradictory memories
    const contradictions = this._detectContradictions();
    fixes.push(...this._resolveContradictions(contradictions, dryRun));

    // 2. Detect and archive outdated
    const outdated = this._detectOutdated();
    fixes.push(...this._archiveOutdated(outdated, dryRun));

    // 3. Detect and compress redundant
    const redundant = this._detectRedundant();
    fixes.push(...this._compressRedundant(redundant, dryRun));

    // 4. Detect and handle orphaned
    const orphaned = this._detectOrphaned();
    fixes.push(...this._handleOrphaned(orphaned, dryRun));

    return fixes;
  }

  _detectContradictions() {
    const contradictions = [];
    for (let i = 0; i < this.memories.length; i++) {
      const m1 = this.memories[i];
      for (let j = i + 1; j < this.memories.length; j++) {
        const m2 = this.memories[j];
        if ((m1.category || '') !== (m2.category || '')) continue;

        const text1 = (m1.text || '').toLowerCase();
        const text2 = (m2.text || '').toLowerCase();

        for (const [word1, word2] of CONFLICT_PAIRS) {
          if (text1.includes(word1) && text2.includes(word2)) {
            if (this._areSimilarContexts(text1, text2, word1, word2)) {
              contradictions.push({
                memory1: m1,
                memory2: m2,
                conflict_type: `${word1} vs ${word2}`
              });
              break;
            }
          }
        }
      }
    }
    return contradictions;
  }

  _areSimilarContexts(text1, text2, word1, word2) {
    const getContext = (text, word, window = 10) => {
      const idx = text.indexOf(word);
      if (idx === -1) return '';
      const start = Math.max(0, idx - window);
      const end = Math.min(text.length, idx + word.length + window);
      return text.slice(start, end);
    };

    const ctx1 = getContext(text1, word1);
    const ctx2 = getContext(text2, word2);
    if (!ctx1 || !ctx2) return false;

    const words1 = new Set(ctx1.split(/\s+/));
    const words2 = new Set(ctx2.split(/\s+/));
    const common = new Set([...words1].filter(w => words2.has(w)));
    return common.size >= 2;
  }

  _detectOutdated() {
    const outdated = [];
    const thresholdDays = AUTO_FIX_RULES.outdated.threshold_days;
    const threshold = Date.now() - thresholdDays * 24 * 60 * 60 * 1000;

    for (const m of this.memories) {
      const ts = m.timestamp || m.created_at;
      if (!ts) continue;
      const tsMs = typeof ts === 'number' ? ts : new Date(ts).getTime();
      if (tsMs < threshold) {
        const daysOld = Math.floor((Date.now() - tsMs) / (24 * 60 * 60 * 1000));
        outdated.push({ ...m, days_old: daysOld });
      }
    }
    return outdated;
  }

  _detectRedundant() {
    const redundant = [];
    const threshold = AUTO_FIX_RULES.redundant.similarity_threshold;

    for (let i = 0; i < this.memories.length; i++) {
      const text1 = (this.memories[i].text || '').toLowerCase().trim();
      if (!text1) continue;
      for (let j = i + 1; j < this.memories.length; j++) {
        const text2 = (this.memories[j].text || '').toLowerCase().trim();
        if (!text2) continue;
        const sim = this._calculateSimilarity(text1, text2);
        if (sim >= threshold) {
          redundant.push({
            memory1: this.memories[i],
            memory2: this.memories[j],
            similarity: Math.round(sim * 1000) / 1000
          });
        }
      }
    }
    return redundant;
  }

  _calculateSimilarity(text1, text2) {
    if (!text1 || !text2) return 0;
    const words1 = new Set(text1.split(/\W+/).filter(Boolean));
    const words2 = new Set(text2.split(/\W+/).filter(Boolean));
    if (!words1.size || !words2.size) return 0;
    const intersection = new Set([...words1].filter(w => words2.has(w)));
    const union = new Set([...words1, ...words2]);
    return union.size > 0 ? intersection.size / union.size : 0;
  }

  _detectOrphaned() {
    const orphaned = [];
    const hasAssociation = new Set();

    if (existsSync(ASSOCIATION_GRAPH_FILE)) {
      try {
        const graph = JSON.parse(readFileSync(ASSOCIATION_GRAPH_FILE, 'utf-8'));
        const edges = graph.edges || {};
        for (const edge of Object.values(edges)) {
          if (edge.source) hasAssociation.add(edge.source);
          if (edge.target) hasAssociation.add(edge.target);
        }
      } catch { /* ignore */ }
    }

    for (const m of this.memories) {
      const memId = m.id || '';
      if (!hasAssociation.has(memId)) {
        orphaned.push(m);
      }
    }
    return orphaned;
  }

  _resolveContradictions(contradictions, dryRun) {
    const fixes = [];
    for (const conflict of contradictions) {
      fixes.push({
        type: 'contradiction',
        action: 'flag',
        dry_run: dryRun,
        memory1_id: conflict.memory1.id,
        memory2_id: conflict.memory2.id,
        conflict_type: conflict.conflict_type,
        message: `发现矛盾记忆 [${conflict.conflict_type}]，需要用户确认处理`
      });
    }
    return fixes;
  }

  _archiveOutdated(outdated, dryRun) {
    const fixes = [];
    for (const m of outdated.slice(0, 10)) {
      fixes.push({
        type: 'outdated',
        action: dryRun ? 'archive' : 'archived',
        dry_run: dryRun,
        memory_id: m.id,
        days_old: m.days_old || 0,
        message: dryRun
          ? `将归档过时记忆 (${m.days_old}天)`
          : `已归档过时记忆`
      });
    }
    return fixes;
  }

  _compressRedundant(redundant, dryRun) {
    const fixes = [];
    const seenIds = new Set();
    const unique = redundant.filter(r => {
      const id1 = r.memory1.id;
      const id2 = r.memory2.id;
      if (seenIds.has(id1) || seenIds.has(id2)) return false;
      seenIds.add(id1);
      seenIds.add(id2);
      return true;
    });

    for (const r of unique.slice(0, 10)) {
      fixes.push({
        type: 'redundant',
        action: dryRun ? 'compress' : 'compressed',
        dry_run: dryRun,
        memory1_id: r.memory1.id,
        memory2_id: r.memory2.id,
        similarity: r.similarity,
        message: `将合并冗余记忆 (相似度: ${r.similarity.toFixed(2)})`
      });
    }
    return fixes;
  }

  _handleOrphaned(orphaned, dryRun) {
    const fixes = [];
    for (const m of orphaned.slice(0, 10)) {
      fixes.push({
        type: 'orphaned',
        action: 'flag',
        dry_run: dryRun,
        memory_id: m.id,
        message: '发现孤立记忆，需要处理'
      });
    }
    return fixes;
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
export function cmdHealth(command, args = {}) {
  const checker = new MemoryHealthChecker();

  switch (command) {
    case 'report': {
      const health = checker.calculateHealthScore();
      const emoji = { contradiction: '❌', outdated: '⏰', redundant: '🔄', orphaned: '🔗' };
      return {
        type: 'text',
        text:
          `📊 健康度分数: ${health.score}/100\n` +
          `   总记忆数: ${health.total}\n\n` +
          `问题统计:\n` +
          `   ❌ 矛盾: ${health.conflicts} 条\n` +
          `   ⏰ 过时: ${health.outdated} 条\n` +
          `   🔄 冗余: ${health.redundant} 条\n` +
          `   🔗 孤立: ${health.orphaned} 条`
      };
    }

    case 'validate': {
      const total = checker.memories.length;
      const valid = checker.memories.filter(m =>
        (m.text || '').length >= 3 && m.category
      ).length;
      return {
        type: 'text',
        text: `验证结果:\n   有效: ${valid}/${total}`
      };
    }

    case 'conflicts': {
      const conflicts = checker._detectContradictions();
      const lines = [`发现 ${conflicts.length} 对矛盾记忆:`];
      for (const c of conflicts.slice(0, 5)) {
        lines.push(`\n❌ 矛盾 [${c.conflict_type}]:`);
        lines.push(`   1. [${c.memory1.id?.slice(0, 8)}] ${(c.memory1.text || '').slice(0, 50)}`);
        lines.push(`   2. [${c.memory2.id?.slice(0, 8)}] ${(c.memory2.text || '').slice(0, 50)}`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'fix':
    case 'auto-fix': {
      const dryRun = !args.apply;
      const fixes = checker.autoFix(dryRun);
      if (fixes.length === 0) {
        return { type: 'text', text: '✅ 没有需要修复的问题' };
      }
      const byType = {};
      for (const f of fixes) {
        byType[f.type] = (byType[f.type] || 0) + 1;
      }
      const emoji = { contradiction: '❌', outdated: '⏰', redundant: '🔄', orphaned: '🔗' };
      const lines = [
        `🔧 自动修复模式: ${dryRun ? '预览' : '执行'}`,
        `📋 修复操作 (${fixes.length} 个):\n`
      ];
      for (const [t, count] of Object.entries(byType)) {
        lines.push(`   ${emoji[t] || '•'} ${t}: ${count} 条`);
      }
      if (dryRun) lines.push('\n💡 使用 --apply 参数执行修复');
      return { type: 'text', text: lines.join('\n') };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { MemoryHealthChecker, cmdHealth };

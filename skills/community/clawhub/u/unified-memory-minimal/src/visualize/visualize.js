/**
 * Memory Visualize - 记忆可视化
 * 
 * Ported from memory_visualize.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VIZ_DIR = join(MEMORY_DIR, 'visualizations');

// ============================================================
// Visualizer
// ============================================================

export class MemoryVisualizer {
  constructor() {
    mkdirSync(VIZ_DIR, { recursive: true });
  }

  /**
   * Generate ASCII visualization of memory categories
   * @param {Array} memories
   * @returns {string}
   */
  asciiCategories(memories) {
    /** @type {Map<string, number>} */
    const categoryCount = new Map();
    for (const m of memories) {
      const cat = m.category || 'general';
      categoryCount.set(cat, (categoryCount.get(cat) || 0) + 1);
    }

    const sorted = [...categoryCount.entries()].sort((a, b) => b[1] - a[1]);
    const maxCount = sorted.length > 0 ? sorted[0][1] : 0;

    const lines = ['📊 记忆分类分布', ''];
    for (const [cat, count] of sorted) {
      const barLen = Math.round((count / Math.max(maxCount, 1)) * 30);
      const bar = '█'.repeat(barLen);
      const pct = Math.round((count / Math.max(memories.length, 1)) * 100);
      lines.push(`  ${cat.padEnd(12)} ${bar.padEnd(30)} ${count} (${pct}%)`);
    }

    return lines.join('\n');
  }

  /**
   * Generate ASCII timeline
   * @param {Array} memories
   * @returns {string}
   */
  asciiTimeline(memories) {
    /** @type {Map<string, Array>} */
    const byMonth = new Map();
    for (const m of memories) {
      const ts = m.created_at || m.timestamp;
      if (!ts) continue;
      const month = ts.slice(0, 7); // YYYY-MM
      if (!byMonth.has(month)) byMonth.set(month, []);
      byMonth.get(month).push(m);
    }

    const sorted = [...byMonth.entries()].sort((a, b) => b[0].localeCompare(a[0])).slice(0, 12);
    const maxCount = sorted.length > 0 ? Math.max(...sorted.map(([, m]) => m.length)) : 0;

    const lines = ['📅 记忆时间线', ''];
    for (const [month, mems] of sorted) {
      const barLen = Math.round((mems.length / Math.max(maxCount, 1)) * 40);
      const bar = '▓'.repeat(barLen);
      lines.push(`  ${month} ${bar} ${mems.length} 条`);
    }

    return lines.join('\n');
  }

  /**
   * Generate ASCII importance distribution
   * @param {Array} memories
   * @returns {string}
   */
  asciiImportance(memories) {
    const buckets = { '0.0-0.2': 0, '0.2-0.4': 0, '0.4-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0 };
    for (const m of memories) {
      const imp = m.importance || 0.5;
      if (imp < 0.2) buckets['0.0-0.2']++;
      else if (imp < 0.4) buckets['0.2-0.4']++;
      else if (imp < 0.6) buckets['0.4-0.6']++;
      else if (imp < 0.8) buckets['0.6-0.8']++;
      else buckets['0.8-1.0']++;
    }

    const maxCount = Math.max(...Object.values(buckets), 1);
    const lines = ['⭐ 重要性分布', ''];
    for (const [range, count] of Object.entries(buckets)) {
      const barLen = Math.round((count / maxCount) * 40);
      const bar = '◆'.repeat(barLen);
      lines.push(`  ${range.padEnd(10)} ${bar.padEnd(40)} ${count}`);
    }

    return lines.join('\n');
  }

  /**
   * Generate text-based graph visualization
   * @param {object} graph
   * @returns {string}
   */
  asciiGraph(graph) {
    const nodes = graph.nodes || {};
    const edges = graph.edges || {};

    const lines = ['🕸️ 记忆关联图', ''];
    for (const [nodeId, node] of Object.entries(nodes)) {
      const text = (node.text || node.name || nodeId).slice(0, 20);
      lines.push(`  ● ${text} [${node.category || '?'}]`);
    }

    if (Object.keys(edges).length > 0) {
      lines.push('');
      for (const [edgeKey, edge] of Object.entries(edges).slice(0, 20)) {
        const sourceText = ((nodes[edge.source] || {}).text || edge.source || '').slice(0, 15);
        const targetText = ((nodes[edge.target] || {}).text || edge.target || '').slice(0, 15);
        const weight = edge.weight || 1;
        lines.push(`  ${sourceText} ─${'─'.repeat(weight)}▶ ${targetText} (${weight})`);
      }
    }

    return lines.join('\n');
  }

  /**
   * Generate full ASCII dashboard
   * @param {object} data
   * @returns {string}
   */
  dashboard(data) {
    const memories = data.memories || [];
    const graph = data.graph || {};
    const stats = data.stats || {};

    const separator = '─'.repeat(50);
    const lines = [
      '',
      `  ╔${separator}╗`,
      `  ║ 记忆可视化仪表板${' '.repeat(Math.max(0, 37 - 12))}║`,
      `  ╚${separator}╝`,
      '',
      `  📊 统计概览`,
      `  ─${'─'.repeat(49)}`,
      `  总记忆数:   ${memories.length}`,
      `  分类数:    ${stats.categoryCount || 0}`,
      `  关联边数:  ${Object.keys(graph.edges || {}).length}`,
      '',
      this.asciiCategories(memories),
      '',
      separator,
      this.asciiTimeline(memories),
      '',
      separator,
      this.asciiImportance(memories),
      '',
    ];

    if (Object.keys(graph.nodes || {}).length > 0) {
      lines.push(separator);
      lines.push(this.asciiGraph(graph));
    }

    lines.push('');
    return lines.join('\n');
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
export function cmdVisualize(command, args) {
  const visualizer = new MemoryVisualizer();

  // Load memories for visualization
  /** @type {Array} */
  let memories = [];
  try {
    const { getAllMemories } = require('../storage.js');
    memories = getAllMemories();
  } catch {
    const memoryFile = join(MEMORY_DIR, 'memories.json');
    if (existsSync(memoryFile)) {
      try {
        const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
        memories = Array.isArray(data) ? data : (data.memories || []);
      } catch { /* ignore */ }
    }
  }

  switch (command) {
    case 'categories': {
      return { type: 'text', text: visualizer.asciiCategories(memories) };
    }

    case 'timeline': {
      return { type: 'text', text: visualizer.asciiTimeline(memories) };
    }

    case 'importance': {
      return { type: 'text', text: visualizer.asciiImportance(memories) };
    }

    case 'graph': {
      // Try to load association graph
      let graph = {};
      try {
        const associationGraphFile = join(MEMORY_DIR, 'associations', 'graph.json');
        if (existsSync(associationGraphFile)) {
          graph = JSON.parse(readFileSync(associationGraphFile, 'utf-8'));
        }
      } catch { /* ignore */ }
      return { type: 'text', text: visualizer.asciiGraph(graph) };
    }

    case 'dashboard': {
      const stats = {};
      const cats = new Set(memories.map(m => m.category));
      stats.categoryCount = cats.size;

      let graph = {};
      try {
        const gFile = join(MEMORY_DIR, 'associations', 'graph.json');
        if (existsSync(gFile)) graph = JSON.parse(readFileSync(gFile, 'utf-8'));
      } catch { /* ignore */ }

      return { type: 'text', text: visualizer.dashboard({ memories, graph, stats }) };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { MemoryVisualizer, cmdVisualize };

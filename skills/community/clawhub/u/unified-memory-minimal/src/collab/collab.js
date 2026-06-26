/**
 * Memory Collab - 协作效率可视化
 * 
 * Ported from memory_collab.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const COLLAB_DIR = join(WORKSPACE, 'collab');
const TASKS_DIR = join(WORKSPACE, 'tasks');
const STATS_FILE = join(MEMORY_DIR, 'collab_stats.json');

// ============================================================
// CollabAnalyzer
// ============================================================

export class CollabAnalyzer {
  constructor() {
    mkdirSync(COLLAB_DIR, { recursive: true });
  }

  /**
   * Load JSON files from a directory
   * @param {string} dir
   * @param {number} days
   */
  loadJsonFiles(dir, days = 7) {
    /** @type {Array} */
    const files = [];
    if (!existsSync(dir)) return files;

    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
    const entries = require('fs').readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.isFile() && entry.name.endsWith('.json')) {
        try {
          const stat = require('fs').statSync(join(dir, entry.name));
          if (stat.mtimeMs > cutoff) {
            const data = JSON.parse(readFileSync(join(dir, entry.name), 'utf-8'));
            files.push({ ...data, _file: entry.name, _mtime: stat.mtime.toISOString() });
          }
        } catch { /* skip invalid files */ }
      }
    }
    return files;
  }

  /**
   * Collect collaboration statistics
   * @param {number} days
   */
  collectStats(days = 7) {
    /** @type {object} */
    const stats = {
      period: `最近${days}天`,
      generated_at: new Date().toISOString(),
      agents: {
        xiaozhi: { tasks_completed: 0, tasks_created: 0, handovers_sent: 0 },
        xiaoliu: { tasks_completed: 0, tasks_created: 0, handovers_sent: 0 }
      },
      collaboration: {
        total_handovers: 0,
        avg_response_time_hours: 0,
        success_rate: 0
      },
      tasks: { total: 0, completed: 0, in_progress: 0 },
      timeline: []
    };

    // Load task files
    const taskFiles = this.loadJsonFiles(TASKS_DIR, days);
    for (const task of taskFiles) {
      stats.tasks.total++;
      if (task.status === 'completed') stats.tasks.completed++;
      else if (task.status === 'in_progress') stats.tasks.in_progress++;
    }

    // Load handover files
    const handoverFiles = this.loadJsonFiles(join(WORKSPACE, 'handover'), days);
    stats.collaboration.total_handovers = handoverFiles.length;

    // Save stats
    writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2), 'utf-8');

    return stats;
  }

  /**
   * Generate ASCII report
   * @param {object} stats
   */
  asciiReport(stats) {
    const lines = [
      '',
      '  ╔══════════════════════════════════════════════╗',
      '  ║        协作效率报告                         ║',
      '  ╚══════════════════════════════════════════════╝',
      '',
      `  📅 统计周期: ${stats.period}`,
      `  📊 总任务: ${stats.tasks.total} | 已完成: ${stats.tasks.completed} | 进行中: ${stats.tasks.in_progress}`,
      '',
      '  🤖 Agent 统计:'
    ];

    for (const [agent, data] of Object.entries(stats.agents || {})) {
      lines.push(`     ${agent}: 完成 ${data.tasks_completed} | 创建 ${data.tasks_created} | 交接 ${data.handover || 0}`);
    }

    lines.push('');
    lines.push(`  🔄 协作统计:`);
    lines.push(`     总交接: ${stats.collaboration.total_handovers}`);

    const rate = stats.tasks.total > 0
      ? Math.round((stats.tasks.completed / stats.tasks.total) * 100)
      : 0;
    lines.push(`     完成率: ${rate}%`);

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
export function cmdCollab(command, args) {
  const analyzer = new CollabAnalyzer();
  const days = parseInt(args.period) || 7;

  switch (command) {
    case 'stats': {
      const stats = analyzer.collectStats(days);
      if (args.json) return { type: 'json', data: stats };
      return { type: 'text', text: analyzer.asciiReport(stats) };
    }

    case 'report': {
      const stats = analyzer.collectStats(days);
      if (args.html) {
        // Simple HTML report
        const html = `<html><body><h1>协作效率报告</h1><pre>${analyzer.asciiReport(stats)}</pre></body></html>`;
        return { type: 'text', text: html };
      }
      return { type: 'text', text: analyzer.asciiReport(stats) };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { CollabAnalyzer, cmdCollab };

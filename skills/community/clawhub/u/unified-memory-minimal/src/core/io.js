/**
 * Memory Import/Export - 数据导出导入
 * 
 * 功能:
 * - 导出记忆为多种格式 (JSON/CSV/Markdown)
 * - 导入记忆数据
 * - 重置记忆系统
 * - 创建备份
 * 
 * Ported from memory_io.py
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = join(MEMORY_DIR, 'vector');
const BACKUP_DIR = join(MEMORY_DIR, 'backups');

// ============================================================
// MemoryIO
// ============================================================

export class MemoryIO {
  constructor() {
    /** @type {Array<object>} */
    this.memories = this._loadMemories();
    mkdirSync(BACKUP_DIR, { recursive: true });
  }

  /**
   * Load memories from storage
   * @returns {Array<object>}
   */
  _loadMemories() {
    const memories = [];

    try {
      // Try loading from JSON file
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        const data = JSON.parse(readFileSync(memoryFile, 'utf-8'));
        if (Array.isArray(data)) {
          return data;
        }
        if (data.memories && Array.isArray(data.memories)) {
          return data.memories;
        }
      }

      // Try loading from day-based markdown files
      const files = readdirSync(MEMORY_DIR).filter(f => f.endsWith('.md'));
      for (const file of files) {
        if (file === 'snapshots' || file === 'vector_cache') continue;
        try {
          const content = readFileSync(join(MEMORY_DIR, file), 'utf-8');
          const lines = content.split('\n');
          for (const line of lines) {
            if (line.startsWith('- [')) {
              // Parse markdown memory entry
              const match = line.match(/^- \[([^\]]+)\] (?:\[T=([^\]]+)\] )?\[([^\]]+)\] \[([^\]]+)\](?: \[I=([^\]]+)\])? (.+)/);
              if (match) {
                const [, timestamp, tags, category, scope, importance, text] = match;
                memories.push({
                  id: `mem_${Buffer.from(timestamp + text.slice(0, 10)).toString('base64').slice(0, 12)}`,
                  timestamp,
                  tags: tags ? tags.split(',') : [],
                  category,
                  scope,
                  importance: parseFloat(importance) || 0.5,
                  text
                });
              }
            }
          }
        } catch {
          // skip unreadable files
        }
      }
    } catch (e) {
      console.error(`⚠️ 加载记忆失败: ${e.message}`);
    }

    return memories;
  }

  /**
   * Export memories to JSON
   * @param {string} outputPath
   * @returns {{ success: boolean, message: string }}
   */
  exportJson(outputPath) {
    try {
      const exportData = {
        version: '0.0.7',
        exported_at: new Date().toISOString(),
        total_memories: this.memories.length,
        memories: this.memories
      };
      writeFileSync(outputPath, JSON.stringify(exportData, null, 2), 'utf-8');
      return { success: true, message: `✅ 已导出到 ${outputPath}` };
    } catch (e) {
      return { success: false, message: `❌ 导出失败: ${e.message}` };
    }
  }

  /**
   * Export memories to CSV
   * @param {string} outputPath
   * @returns {{ success: boolean, message: string }}
   */
  exportCsv(outputPath) {
    try {
      if (this.memories.length === 0) {
        return { success: false, message: '⚠️ 没有记忆可导出' };
      }

      const fields = ['id', 'text', 'category', 'importance', 'timestamp'];
      const header = fields.join(',');
      const rows = this.memories.map(m =>
        fields.map(f => {
          const val = (m[f] || m[f.replace('_', '')] || '').toString();
          return `"${val.replace(/"/g, '""')}"`;
        }).join(',')
      );

      writeFileSync(outputPath, [header, ...rows].join('\n'), 'utf-8');
      return { success: true, message: `✅ 已导出到 ${outputPath}` };
    } catch (e) {
      return { success: false, message: `❌ 导出失败: ${e.message}` };
    }
  }

  /**
   * Export memories to Markdown
   * @param {string} outputPath
   * @returns {{ success: boolean, message: string }}
   */
  exportMarkdown(outputPath) {
    try {
      const lines = [
        '# Memory Export',
        '',
        `**Version**: 0.0.7`,
        `**Exported**: ${new Date().toISOString()}`,
        `**Total Memories**: ${this.memories.length}`,
        '',
        '---',
        ''
      ];

      // Group by category
      /** @type {Map<string, Array>} */
      const byCategory = new Map();
      for (const mem of this.memories) {
        const cat = mem.category || 'other';
        if (!byCategory.has(cat)) byCategory.set(cat, []);
        byCategory.get(cat).push(mem);
      }

      for (const [category, mems] of byCategory) {
        lines.push(`## ${category.charAt(0).toUpperCase() + category.slice(1)}`);
        lines.push('');

        for (const mem of mems) {
          const importance = mem.importance || 0.5;
          const stars = '⭐'.repeat(Math.round(importance * 5));
          const text = mem.text || '';
          const created = mem.timestamp || mem.created_at || 'unknown';

          lines.push(`### ${(mem.id || 'unknown').slice(0, 8)}`);
          lines.push(`- **Importance**: ${importance.toFixed(2)} ${stars}`);
          lines.push(`- **Created**: ${created}`);
          lines.push(`- **Content**: ${text}`);
          lines.push('');
        }

        lines.push('---');
        lines.push('');
      }

      writeFileSync(outputPath, lines.join('\n'), 'utf-8');
      return { success: true, message: `✅ 已导出到 ${outputPath}` };
    } catch (e) {
      return { success: false, message: `❌ 导出失败: ${e.message}` };
    }
  }

  /**
   * Import memories from a file
   * @param {string} filePath
   * @param {boolean} merge
   * @returns {{ imported: number, message: string }}
   */
  importData(filePath, merge = true) {
    try {
      const content = readFileSync(filePath, 'utf-8');
      let data;
      try {
        data = JSON.parse(content);
      } catch {
        return { imported: 0, message: '❌ 无效的 JSON 文件' };
      }

      let memories = [];
      if (Array.isArray(data)) {
        memories = data;
      } else if (data.memories && Array.isArray(data.memories)) {
        memories = data.memories;
      } else {
        return { imported: 0, message: '❌ 无效的数据格式' };
      }

      if (merge) {
        const existingIds = new Set(this.memories.map(m => m.id).filter(Boolean));
        memories = memories.filter(m => !existingIds.has(m.id));
      }

      if (memories.length === 0) {
        return { imported: 0, message: '⚠️ 没有新记忆需要导入' };
      }

      // Try to save via storage module
      try {
        const { addMemory } = require('../storage.js');
        for (const mem of memories) {
          addMemory({
            text: mem.text || mem.content || '',
            category: mem.category || 'general',
            importance: mem.importance || 0.5,
            tags: mem.tags || []
          });
        }
      } catch {
        // Fallback: just add to in-memory list
        this.memories.push(...memories);
      }

      return { imported: memories.length, message: `✅ 已导入 ${memories.length} 条记忆` };
    } catch (e) {
      return { imported: 0, message: `❌ 读取文件失败: ${e.message}` };
    }
  }

  /**
   * Reset memory system
   * @param {boolean} confirm
   * @returns {{ success: boolean, message: string }}
   */
  reset(confirm = false) {
    if (!confirm) {
      return {
        success: false,
        message: '⚠️ 这将删除所有记忆数据！使用 --confirm 确认重置'
      };
    }

    try {
      // Create backup
      const backupName = `backup_${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}`;
      const backupPath = join(BACKUP_DIR, backupName);
      mkdirSync(backupPath, { recursive: true });

      // Copy vector DB if exists
      if (existsSync(VECTOR_DB_DIR)) {
        this._copyDir(VECTOR_DB_DIR, join(backupPath, 'vector'));
      }

      // Clear vector DB
      if (existsSync(VECTOR_DB_DIR)) {
        const { rmSync } = require('fs');
        rmSync(VECTOR_DB_DIR, { recursive: true });
        mkdirSync(VECTOR_DB_DIR, { recursive: true });
      }

      return { success: true, message: `✅ 已重置记忆系统（备份在 ${backupPath}）` };
    } catch (e) {
      return { success: false, message: `❌ 重置失败: ${e.message}` };
    }
  }

  /**
   * Create a backup
   * @returns {string}
   */
  createBackup() {
    const backupName = `memory_backup_${new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)}.json`;
    const backupPath = join(BACKUP_DIR, backupName);
    this.exportJson(backupPath);
    return backupPath;
  }

  /**
   * Copy directory recursively
   * @param {string} src
   * @param {string} dst
   */
  _copyDir(src, dst) {
    mkdirSync(dst, { recursive: true });
    try {
      const entries = readdirSync(src, { withFileTypes: true });
      for (const entry of entries) {
        const srcPath = join(src, entry.name);
        const dstPath = join(dst, entry.name);
        if (entry.isDirectory()) {
          this._copyDir(srcPath, dstPath);
        } else {
          writeFileSync(dstPath, readFileSync(srcPath));
        }
      }
    } catch {
      // ignore
    }
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * Execute IO command
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdIO(command, args) {
  const io = new MemoryIO();

  switch (command) {
    case 'export': {
      const { format = 'json', output } = args;
      if (!output) {
        const ext = format === 'md' ? 'md' : format;
        const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        args.output = `memories_export_${ts}.${ext}`;
      }
      if (format === 'json') return io.exportJson(args.output);
      if (format === 'csv') return io.exportCsv(args.output);
      if (format === 'md') return io.exportMarkdown(args.output);
      return { success: false, message: `❌ 未知格式: ${format}` };
    }

    case 'import': {
      const { file } = args;
      if (!file) return { success: false, message: '❌ 请指定 --file' };
      if (!existsSync(file)) return { success: false, message: `❌ 文件不存在: ${file}` };
      const result = io.importData(file, args.merge !== false);
      return result;
    }

    case 'reset':
      return io.reset(args.confirm === true);

    case 'backup': {
      const backupPath = io.createBackup();
      return { success: true, message: `✅ 备份已创建: ${backupPath}` };
    }

    default:
      return { success: false, message: `❌ 未知命令: ${command}` };
  }
}

export default {
  MemoryIO,
  cmdIO
};

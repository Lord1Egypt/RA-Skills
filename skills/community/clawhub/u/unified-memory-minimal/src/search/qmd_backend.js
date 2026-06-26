/**
 * src/search/qmd_backend.js
 * QMD 搜索后端集成
 * 当 config.qmd.enabled=true 时，优先使用 QMD CLI 进行搜索
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { config } from '../config.js';
import { log as logger } from '../logger.js';

export class QMDSearchBackend {
  constructor(cfg = {}) {
    this.enabled = cfg.enabled ?? config.qmd?.enabled ?? false;
    this.collections = cfg.collections ?? config.qmd?.collections ?? [
      'workspace', 'daily-logs', 'projects', 'intelligence'
    ];
    this.limit = cfg.limit ?? 10;
  }

  /**
   * 检查 QMD CLI 是否可用
   */
  isAvailable() {
    try {
      execSync('qmd --version', { encoding: 'utf-8', stdio: 'pipe' });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 使用 QMD CLI 搜索
   * @param {Object} params
   * @param {string} params.query - 搜索查询
   * @param {string[]} [params.collections] - 搜索的集合
   * @param {number} [params.limit] - 结果数
   * @returns {Promise<{results: Array, backend: string}>}
   */
  async search({ query, collections, limit = this.limit } = {}) {
    if (!this.enabled) {
      return { results: [], backend: 'qmd', skipped: 'disabled' };
    }

    if (!this.isAvailable()) {
      logger.warn('QMD CLI not available, falling back to built-in search');
      return { results: [], backend: 'qmd', skipped: 'unavailable' };
    }

    const cols = collections || this.collections;
    const colsStr = cols.join(',');

    try {
      const escapedQuery = query.replace(/"/g, '\\"');
      const cmd = `qmd search --query "${escapedQuery}" --collections ${colsStr} --limit ${limit} --json`;
      
      let result;
      try {
        result = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
      } catch (execErr) {
        // QMD 可能不支持 --json，尝试不用 --json
        result = execSync(`qmd search --query "${escapedQuery}" --collections ${colsStr} --limit ${limit}`, 
          { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
      }

      let parsed;
      try {
        parsed = JSON.parse(result);
      } catch {
        // 解析失败，尝试逐行解析
        const lines = result.split('\n').filter(Boolean);
        parsed = lines.map(line => {
          try { return JSON.parse(line); }
          catch { return { content: line, source: 'qmd' }; }
        });
      }

      const results = Array.isArray(parsed) ? parsed : (parsed.results || [parsed]);
      
      return {
        results: results.map(r => ({
          content: r.content || r.text || r.snippet || String(r),
          score: r.score || r.relevance || 0.5,
          source: r.source || 'qmd',
          collection: r.collection || cols[0],
        })),
        backend: 'qmd',
        count: results.length,
      };
    } catch (err) {
      logger.error(`QMD search failed: ${err.message}`);
      return { results: [], backend: 'qmd', error: err.message };
    }
  }

  /**
   * 获取 QMD 集合列表
   */
  async listCollections() {
    if (!this.isAvailable()) return [];
    try {
      const out = execSync('qmd list-collections', { encoding: 'utf-8' });
      return out.split('\n').filter(Boolean);
    } catch {
      return this.collections;
    }
  }
}

// 导出单例
export const qmdBackend = new QMDSearchBackend();

/**
 * 统一搜索入口：QMD 优先，降级到 null（让调用方用内置搜索）
 */
export async function qmdSearchIfEnabled({ query, collections, limit } = {}) {
  if (!qmdBackend.enabled) return null;
  return qmdBackend.search({ query, collections, limit });
}

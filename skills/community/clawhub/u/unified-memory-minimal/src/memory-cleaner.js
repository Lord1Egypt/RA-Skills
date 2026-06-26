/**
 * memory-cleaner.js — 本地数据清理器
 * 
 * 借鉴 memory-tencentdb 的 LocalMemoryCleaner 实现：
 * - 按 retentionDays 保留天数清理 L0/L1 数据
 * - 每日定时清理（默认 03:00）
 * - 支持向量数据库清理
 * - 自然日保留策略
 */

import fs from 'fs/promises';
import path from 'path';
import { log } from './logger.js';

// ─── 配置 ───────────────────────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  retentionDays: 0,           // 保留天数，0 = 禁用清理
  cleanTime: '03:00',         // 每日清理时间 (HH:mm)
  allowAggressiveCleanup: false, // 是否允许 1-2 天的高风险清理
  l0Dir: 'conversations',     // L0 目录名
  l1Dir: 'records',           // L1 目录名
};

// ─── 清理器类 ─────────────────────────────────────────────────────────────

export class LocalMemoryCleaner {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    this.baseDir = options.baseDir || process.env.MEMORY_DIR || './memory';
    this.timer = null;
    this.destroyed = false;
    this.vectorStore = options.vectorStore || null;
    
    // 统计
    this.stats = {
      lastRun: null,
      totalRuns: 0,
      totalFilesDeleted: 0,
      totalRecordsDeleted: 0,
    };
  }
  
  /**
   * 设置向量存储实例
   */
  setVectorStore(vectorStore) {
    this.vectorStore = vectorStore;
  }
  
  /**
   * 启动清理器
   */
  start() {
    if (this.destroyed) return;
    
    const { retentionDays, cleanTime } = this.config;
    
    if (!(retentionDays > 0)) {
      log('info', `[MemoryCleaner] Disabled: retentionDays=${retentionDays}`);
      return;
    }
    
    // 验证 retentionDays
    if (retentionDays < 3 && !this.config.allowAggressiveCleanup) {
      log('warn', `[MemoryCleaner] retentionDays < 3 requires allowAggressiveCleanup=true`);
      return;
    }
    
    log('info', `[MemoryCleaner] Enabled: retentionDays=${retentionDays}, cleanTime=${cleanTime}`);
    
    this.scheduleNext();
  }
  
  /**
   * 停止清理器
   */
  destroy() {
    if (this.destroyed) return;
    this.destroyed = true;
    
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    
    log('info', '[MemoryCleaner] Stopped');
  }
  
  /**
   * 手动执行一次清理
   */
  async runOnce(nowMs = Date.now()) {
    if (this.destroyed) return;
    
    const { retentionDays } = this.config;
    if (!(retentionDays > 0)) {
      log('debug', `[MemoryCleaner] Skip: retentionDays=${retentionDays}`);
      return;
    }
    
    const cutoffMs = this.computeCutoffMs(nowMs, retentionDays);
    const cutoffDate = new Date(cutoffMs).toISOString().split('T')[0];
    
    log('info', `[MemoryCleaner] Running cleanup: cutoff=${cutoffDate}, retentionDays=${retentionDays}`);
    
    const results = {
      l0: { scanned: 0, deleted: 0, failed: 0 },
      l1: { scanned: 0, deleted: 0, failed: 0 },
      vector: { l0Deleted: 0, l1Deleted: 0 },
    };
    
    // 清理 L0 目录
    const l0Dir = path.join(this.baseDir, this.config.l0Dir);
    const l0Result = await this.cleanDirectory(l0Dir, cutoffMs);
    results.l0 = l0Result;
    
    // 清理 L1 目录
    const l1Dir = path.join(this.baseDir, this.config.l1Dir);
    const l1Result = await this.cleanDirectory(l1Dir, cutoffMs);
    results.l1 = l1Result;
    
    // 清理向量数据库
    if (this.vectorStore) {
      try {
        const cutoffIso = new Date(cutoffMs).toISOString();
        
        // 删除过期的 L0 记录
        if (this.vectorStore.deleteL0ExpiredByRecordedAt) {
          results.vector.l0Deleted = this.vectorStore.deleteL0ExpiredByRecordedAt(cutoffIso);
        }
        
        // 删除过期的 L1 记录
        if (this.vectorStore.deleteL1ExpiredByUpdatedTime) {
          results.vector.l1Deleted = this.vectorStore.deleteL1ExpiredByUpdatedTime(cutoffIso);
        }
        
        log('info', `[MemoryCleaner] Vector cleanup: l0Deleted=${results.vector.l0Deleted}, l1Deleted=${results.vector.l1Deleted}`);
      } catch (err) {
        log('error', `[MemoryCleaner] Vector cleanup failed: ${err.message}`);
      }
    }
    
    // 更新统计
    this.stats.lastRun = new Date().toISOString();
    this.stats.totalRuns += 1;
    this.stats.totalFilesDeleted += results.l0.deleted + results.l1.deleted;
    this.stats.totalRecordsDeleted += results.vector.l0Deleted + results.vector.l1Deleted;
    
    log('info', `[MemoryCleaner] Cleanup done: l0=${results.l0.deleted} files, l1=${results.l1.deleted} files, vector=${results.vector.l0Deleted + results.vector.l1Deleted} records`);
    
    return results;
  }
  
  /**
   * 获取清理器状态
   */
  getStatus() {
    return {
      enabled: this.config.retentionDays > 0,
      config: this.config,
      stats: this.stats,
      nextRun: this.timer ? new Date(this.nextRunTime).toISOString() : null,
    };
  }
  
  /**
   * 更新配置
   */
  updateConfig(newConfig) {
    Object.assign(this.config, newConfig);
    
    // 重新调度
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    
    if (this.config.retentionDays > 0) {
      this.scheduleNext();
    }
  }
  
  // ─── 内部方法 ─────────────────────────────────────────────────────────────
  
  /**
   * 清理单个目录
   */
  async cleanDirectory(dirPath, cutoffMs) {
    const result = { scanned: 0, deleted: 0, failed: 0 };
    
    try {
      const entries = await fs.readdir(dirPath, { withFileTypes: true });
      
      for (const entry of entries) {
        if (!entry.isFile()) continue;
        if (!this.isJsonLikeFile(entry.name)) continue;
        
        result.scanned += 1;
        
        // 提取日期分片
        const shard = this.extractShardDate(entry.name);
        if (!shard) {
          log('debug', `[MemoryCleaner] Skip non-shard file: ${entry.name}`);
          continue;
        }
        
        // 检查是否过期
        const dayEndMs = this.localDayEndMs(shard.year, shard.month, shard.day);
        if (dayEndMs < cutoffMs) {
          const filePath = path.join(dirPath, entry.name);
          try {
            await fs.unlink(filePath);
            result.deleted += 1;
            log('info', `[MemoryCleaner] Deleted: ${filePath}`);
          } catch (err) {
            result.failed += 1;
            log('warn', `[MemoryCleaner] Failed to delete ${filePath}: ${err.message}`);
          }
        }
      }
    } catch (err) {
      if (err.code !== 'ENOENT') {
        log('warn', `[MemoryCleaner] Directory scan failed: ${dirPath} - ${err.message}`);
      }
    }
    
    return result;
  }
  
  /**
   * 调度下一次清理
   */
  scheduleNext() {
    const nowMs = Date.now();
    const nextMs = this.nextRunAt(this.config.cleanTime, nowMs);
    const delayMs = Math.max(0, nextMs - nowMs);
    
    this.nextRunTime = nextMs;
    
    log('info', `[MemoryCleaner] Scheduled: nextRun=${new Date(nextMs).toISOString()}, delay=${Math.round(delayMs / 1000 / 60)}min`);
    
    this.timer = setTimeout(async () => {
      if (this.destroyed) return;
      
      log('info', `[MemoryCleaner] Timer fired at ${new Date().toISOString()}`);
      
      try {
        await this.runOnce();
      } catch (err) {
        log('error', `[MemoryCleaner] Cleanup failed: ${err.message}`);
      }
      
      // 重新调度
      if (!this.destroyed) {
        this.scheduleNext();
      }
    }, delayMs);
  }
  
  /**
   * 计算截止时间（自然日策略）
   */
  computeCutoffMs(nowMs, retentionDays) {
    const now = new Date(nowMs);
    const keepStart = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
    keepStart.setDate(keepStart.getDate() - (retentionDays - 1));
    return keepStart.getTime();
  }
  
  /**
   * 计算下一次运行时间
   */
  nextRunAt(cleanTime, nowMs) {
    const [hour, minute] = cleanTime.split(':').map(Number);
    
    const now = new Date(nowMs);
    const next = new Date(nowMs);
    next.setHours(hour, minute, 0, 0);
    
    if (next.getTime() <= now.getTime()) {
      next.setDate(next.getDate() + 1);
    }
    
    return next.getTime();
  }
  
  /**
   * 提取文件名中的日期分片
   */
  extractShardDate(fileName) {
    // 支持格式: YYYY-MM-DD.jsonl | YYYY-MM-DD.json
    const m = /^(\d{4})-(\d{2})-(\d{2})\.(?:jsonl|json)$/.exec(fileName);
    if (!m) return null;
    
    const year = Number(m[1]);
    const month = Number(m[2]);
    const day = Number(m[3]);
    
    // 验证日期有效性
    const probe = new Date(year, month - 1, day);
    if (
      probe.getFullYear() !== year ||
      probe.getMonth() !== month - 1 ||
      probe.getDate() !== day
    ) {
      return null;
    }
    
    return { year, month, day };
  }
  
  /**
   * 计算本地日期的结束时间（毫秒）
   */
  localDayEndMs(year, month, day) {
    return new Date(year, month - 1, day, 23, 59, 59, 999).getTime();
  }
  
  /**
   * 检查是否是 JSON 文件
   */
  isJsonLikeFile(name) {
    return name.endsWith('.jsonl') || name.endsWith('.json');
  }
}

// ─── 单例实例 ─────────────────────────────────────────────────────────────

let cleanerInstance = null;

export function getCleaner(options) {
  if (!cleanerInstance) {
    cleanerInstance = new LocalMemoryCleaner(options);
  }
  return cleanerInstance;
}

export function initCleaner(options) {
  if (cleanerInstance) {
    cleanerInstance.destroy();
  }
  cleanerInstance = new LocalMemoryCleaner(options);
  return cleanerInstance;
}

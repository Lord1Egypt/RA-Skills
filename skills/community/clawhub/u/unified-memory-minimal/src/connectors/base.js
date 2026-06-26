/**
 * Base Connector - 连接器基类
 * 
 * 为外部数据源（GitHub、Notion、飞书等）提供统一的同步接口
 * 
 * 功能：
 * - sync(): 全量同步数据
 * - watch(): 增量监听变更
 * - 统一的数据格式转换
 */

import { log } from '../logger.js';
import { config } from '../config.js';

// ─── 连接器状态 ───────────────────────────────────────────────────────────────
const ConnectorStatus = {
  IDLE: 'idle',
  SYNCING: 'syncing',
  WATCHING: 'watching',
  ERROR: 'error',
  DISABLED: 'disabled',
};

// ─── BaseConnector 基类 ────────────────────────────────────────────────────────

/**
 * 连接器基类
 * 所有具体连接器应继承此类
 */
export class BaseConnector {
  /**
   * @param {object} options
   * @param {string} options.name - 连接器名称
   * @param {string} options.type - 连接器类型（github, notion, feishu 等）
   * @param {object} [options.config] - 连接器配置
   */
  constructor(options = {}) {
    this.name = options.name || 'base-connector';
    this.type = options.type || 'base';
    this.config = options.config || {};
    this.status = ConnectorStatus.IDLE;
    this.lastSync = null;
    this.errorCount = 0;
    this.watcher = null;
    
    // 统计信息
    this.stats = {
      totalSyncs: 0,
      totalItems: 0,
      totalErrors: 0,
      lastSyncDuration: 0,
    };
  }
  
  /**
   * 初始化连接器
   * 子类应重写此方法进行初始化
   */
  async initialize() {
    log('info', `[${this.name}] Initializing connector`);
    return true;
  }
  
  /**
   * 测试连接
   * 子类应重写此方法测试连接是否正常
   */
  async testConnection() {
    log('debug', `[${this.name}] Testing connection`);
    return true;
  }
  
  /**
   * 全量同步
   * 子类应重写此方法实现具体同步逻辑
   * @returns {Promise<{ items: Array, stats: object }>}
   */
  async sync() {
    log('info', `[${this.name}] Starting full sync`);
    
    const startTime = Date.now();
    this.status = ConnectorStatus.SYNCING;
    
    try {
      // 子类实现具体同步逻辑
      const items = await this._doSync();
      
      // 更新统计
      this.lastSync = new Date().toISOString();
      this.stats.totalSyncs++;
      this.stats.totalItems += items.length;
      this.stats.lastSyncDuration = Date.now() - startTime;
      this.status = ConnectorStatus.IDLE;
      
      log('info', `[${this.name}] Sync complete: ${items.length} items, ${this.stats.lastSyncDuration}ms`);
      
      return {
        items,
        stats: { ...this.stats },
      };
    } catch (e) {
      this.status = ConnectorStatus.ERROR;
      this.errorCount++;
      this.stats.totalErrors++;
      
      log('error', `[${this.name}] Sync failed: ${e.message}`);
      
      throw e;
    }
  }
  
  /**
   * 实际同步逻辑（子类重写）
   */
  async _doSync() {
    throw new Error('Subclass must implement _doSync()');
  }
  
  /**
   * 启动增量监听
   * 子类可重写此方法实现增量监听
   * @param {function} callback - 变更回调函数
   */
  async watch(callback) {
    if (this.watcher) {
      log('warn', `[${this.name}] Watcher already running`);
      return;
    }
    
    log('info', `[${this.name}] Starting watch mode`);
    this.status = ConnectorStatus.WATCHING;
    
    // 默认实现：定时轮询
    const interval = this.config.pollInterval || 60000; // 默认 1 分钟
    
    this.watcher = setInterval(async () => {
      try {
        const items = await this._doSync();
        if (items.length > 0 && callback) {
          callback({
            type: 'update',
            items,
            source: this.name,
          });
        }
      } catch (e) {
        log('error', `[${this.name}] Watch poll failed: ${e.message}`);
      }
    }, interval);
    
    return {
      stop: () => this.unwatch(),
    };
  }
  
  /**
   * 停止监听
   */
  unwatch() {
    if (this.watcher) {
      clearInterval(this.watcher);
      this.watcher = null;
      this.status = ConnectorStatus.IDLE;
      log('info', `[${this.name}] Watcher stopped`);
    }
  }
  
  /**
   * 将外部数据转换为统一格式
   * 子类应重写此方法
   * @param {any} rawData - 原始数据
   * @returns {object} - 统一格式的数据
   */
  normalize(rawData) {
    return {
      id: rawData.id || rawData._id,
      type: 'item',
      content: rawData.content || rawData.text || '',
      metadata: {
        source: this.name,
        sourceType: this.type,
        createdAt: rawData.createdAt || rawData.created_at || new Date().toISOString(),
        updatedAt: rawData.updatedAt || rawData.updated_at || new Date().toISOString(),
        url: rawData.url || rawData.html_url,
        ...rawData.metadata,
      },
      raw: rawData,
    };
  }
  
  /**
   * 获取连接器状态
   */
  getStatus() {
    return {
      name: this.name,
      type: this.type,
      status: this.status,
      lastSync: this.lastSync,
      errorCount: this.errorCount,
      stats: { ...this.stats },
    };
  }
  
  /**
   * 销毁连接器
   */
  async destroy() {
    this.unwatch();
    this.status = ConnectorStatus.DISABLED;
    log('info', `[${this.name}] Connector destroyed`);
  }
}

export default BaseConnector;

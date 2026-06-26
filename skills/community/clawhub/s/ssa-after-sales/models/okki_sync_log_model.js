/**
 * OKKI 同步日志模型
 * 记录投诉/返单同步到 OKKI 的历史
 */

const fs = require('fs');
const path = require('path');

// 日志存储路径
const LOGS_DIR = path.join(__dirname, '../data/okki_sync_logs');
const LOG_FILE = path.join(LOGS_DIR, 'okki_sync_logs.json');

// 内存缓存
let syncLogs = [];
let initialized = false;

/**
 * 初始化日志存储
 */
function init() {
  if (initialized) return;
  
  try {
    // 创建目录
    if (!fs.existsSync(LOGS_DIR)) {
      fs.mkdirSync(LOGS_DIR, { recursive: true });
    }
    
    // 加载现有日志
    if (fs.existsSync(LOG_FILE)) {
      const content = fs.readFileSync(LOG_FILE, 'utf8');
      syncLogs = JSON.parse(content);
    }
    
    initialized = true;
  } catch (error) {
    console.error('初始化 OKKI 同步日志失败:', error);
    syncLogs = [];
  }
}

/**
 * 保存日志到文件
 */
function saveToFile() {
  try {
    if (!fs.existsSync(LOGS_DIR)) {
      fs.mkdirSync(LOGS_DIR, { recursive: true });
    }
    fs.writeFileSync(LOG_FILE, JSON.stringify(syncLogs, null, 2), 'utf8');
  } catch (error) {
    console.error('保存 OKKI 同步日志失败:', error);
  }
}

/**
 * OKKI 同步日志类
 */
class OkkiSyncLog {
  constructor(data) {
    this.id = data.id || `OKKI-LOG-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.complaintId = data.complaintId || null;
    this.repeatOrderId = data.repeatOrderId || null;
    this.companyId = data.companyId || null;
    this.trailId = data.trailId || null;
    this.status = data.status || 'pending'; // pending, success, failed
    this.syncType = data.syncType || 'complaint'; // complaint, repeat_order
    this.matchType = data.matchType || null; // customer_id, customer_name, manual
    this.errorMessage = data.errorMessage || null;
    this.syncedAt = data.syncedAt || new Date().toISOString();
    this.retryCount = data.retryCount || 0;
    this.metadata = data.metadata || {};
  }

  toObject() {
    return { ...this };
  }

  /**
   * 更新日志状态
   */
  updateStatus(status, errorMessage = null) {
    this.status = status;
    this.errorMessage = errorMessage;
    this.syncedAt = new Date().toISOString();
  }

  /**
   * 增加重试次数
   */
  incrementRetry() {
    this.retryCount++;
    this.syncedAt = new Date().toISOString();
  }
}

/**
 * 创建同步日志
 * @param {object} data - 日志数据
 * @returns {OkkiSyncLog}
 */
function create(data) {
  init();
  
  const log = new OkkiSyncLog(data);
  syncLogs.push(log.toObject());
  
  // 同步保存（确保数据持久化）
  saveToFile();
  
  return log;
}

/**
 * 根据投诉 ID 获取日志
 * @param {string} complaintId - 投诉 ID
 * @returns {Array<OkkiSyncLog>}
 */
function getByComplaintId(complaintId) {
  init();
  
  return syncLogs
    .filter(log => log.complaintId === complaintId)
    .sort((a, b) => new Date(b.syncedAt) - new Date(a.syncedAt))
    .map(log => new OkkiSyncLog(log));
}

/**
 * 根据返单 ID 获取日志
 * @param {string} repeatOrderId - 返单 ID
 * @returns {Array<OkkiSyncLog>}
 */
function getByRepeatOrderId(repeatOrderId) {
  init();
  
  return syncLogs
    .filter(log => log.repeatOrderId === repeatOrderId)
    .sort((a, b) => new Date(b.syncedAt) - new Date(a.syncedAt))
    .map(log => new OkkiSyncLog(log));
}

/**
 * 根据 OKKI trail ID 获取日志
 * @param {string} trailId - OKKI trail ID
 * @returns {OkkiSyncLog|null}
 */
function getByTrailId(trailId) {
  init();
  
  const log = syncLogs.find(log => log.trailId === trailId);
  return log ? new OkkiSyncLog(log) : null;
}

/**
 * 根据 ID 获取日志（通用）
 * @param {string} id - 日志 ID 或业务 ID
 * @returns {OkkiSyncLog|null}
 */
function getById(id) {
  init();
  
  const log = syncLogs.find(log => 
    log.id === id || 
    log.complaintId === id || 
    log.repeatOrderId === id
  );
  return log ? new OkkiSyncLog(log) : null;
}

/**
 * 获取最近的同步日志
 * @param {number} limit - 数量限制
 * @returns {Array<OkkiSyncLog>}
 */
function getRecent(limit = 10) {
  init();
  
  return syncLogs
    .sort((a, b) => new Date(b.syncedAt) - new Date(a.syncedAt))
    .slice(0, limit)
    .map(log => new OkkiSyncLog(log));
}

/**
 * 获取失败的同步日志
 * @returns {Array<OkkiSyncLog>}
 */
function getFailed() {
  init();
  
  return syncLogs
    .filter(log => log.status === 'failed')
    .sort((a, b) => new Date(b.syncedAt) - new Date(a.syncedAt))
    .map(log => new OkkiSyncLog(log));
}

/**
 * 更新日志
 * @param {string} logId - 日志 ID
 * @param {object} updates - 更新数据
 * @returns {boolean}
 */
function update(logId, updates) {
  init();
  
  const index = syncLogs.findIndex(log => log.id === logId);
  if (index === -1) return false;
  
  syncLogs[index] = { ...syncLogs[index], ...updates };
  saveToFile();
  return true;
}

/**
 * 删除日志
 * @param {string} logId - 日志 ID
 * @returns {boolean}
 */
function remove(logId) {
  init();
  
  const index = syncLogs.findIndex(log => log.id === logId);
  if (index === -1) return false;
  
  syncLogs.splice(index, 1);
  saveToFile();
  return true;
}

/**
 * 清除所有日志
 */
function clear() {
  init();
  syncLogs = [];
  saveToFile();
}

/**
 * 导出日志为 JSON
 * @returns {string}
 */
function exportToJson() {
  init();
  return JSON.stringify(syncLogs, null, 2);
}

// 初始化
init();

module.exports = {
  OkkiSyncLog,
  create,
  getByComplaintId,
  getByRepeatOrderId,
  getByTrailId,
  getById,
  getRecent,
  getFailed,
  update,
  remove,
  clear,
  exportToJson
};

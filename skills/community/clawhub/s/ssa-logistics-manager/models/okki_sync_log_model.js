// logistics/models/okki_sync_log_model.js
/**
 * OKKI 同步日志模型
 * 
 * 用于记录物流记录同步到 OKKI CRM 的日志
 * 包含同步时间、状态、错误信息等
 */

const fs = require('fs');
const path = require('path');

// 日志文件路径
const LOG_FILE_PATH = path.join(__dirname, '../data/okki_sync_logs.json');

/**
 * 确保数据目录存在
 */
function ensureDataDir() {
  const dataDir = path.join(__dirname, '../data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
}

/**
 * 读取日志数据
 * @returns {Array<object>}
 */
function readLogs() {
  ensureDataDir();
  try {
    if (!fs.existsSync(LOG_FILE_PATH)) {
      return [];
    }
    const content = fs.readFileSync(LOG_FILE_PATH, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    console.warn('读取 OKKI 同步日志失败:', e.message);
    return [];
  }
}

/**
 * 写入日志数据
 * @param {Array<object>} logs - 日志列表
 */
function writeLogs(logs) {
  ensureDataDir();
  try {
    fs.writeFileSync(LOG_FILE_PATH, JSON.stringify(logs, null, 2), 'utf-8');
  } catch (e) {
    console.error('写入 OKKI 同步日志失败:', e.message);
  }
}

/**
 * OKKI 同步日志记录类
 */
class OKKISyncLog {
  constructor(data) {
    this.id = data.id || `SYNC-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.logistics_id = data.logistics_id;
    this.company_id = data.company_id || null;
    this.trail_id = data.trail_id || null;
    this.sync_time = data.sync_time || new Date().toISOString();
    this.status = data.status || 'pending'; // pending, success, failed
    this.match_type = data.match_type || null; // order_id_search, customer_name_search
    this.error_message = data.error_message || null;
    this.retry_count = data.retry_count || 0;
  }

  /**
   * 转换为纯对象
   */
  toObject() {
    return {
      id: this.id,
      logistics_id: this.logistics_id,
      company_id: this.company_id,
      trail_id: this.trail_id,
      sync_time: this.sync_time,
      status: this.status,
      match_type: this.match_type,
      error_message: this.error_message,
      retry_count: this.retry_count
    };
  }
}

/**
 * 创建同步日志
 * @param {object} data - 日志数据
 * @returns {OKKISyncLog}
 */
async function create(data) {
  const logs = readLogs();
  const newLog = new OKKISyncLog(data);
  logs.push(newLog.toObject());
  writeLogs(logs);
  return newLog;
}

/**
 * 根据物流 ID 查询日志
 * @param {string} logisticsId - 物流 ID
 * @returns {Array<OKKISyncLog>}
 */
async function findByLogisticsId(logisticsId) {
  const logs = readLogs();
  return logs
    .filter(log => log.logistics_id === logisticsId)
    .sort((a, b) => new Date(b.sync_time) - new Date(a.sync_time));
}

/**
 * 根据 ID 查询日志
 * @param {string} logId - 日志 ID
 * @returns {OKKISyncLog|null}
 */
async function findById(logId) {
  const logs = readLogs();
  const log = logs.find(l => l.id === logId);
  return log ? new OKKISyncLog(log) : null;
}

/**
 * 更新日志状态
 * @param {string} logId - 日志 ID
 * @param {object} updates - 更新数据
 * @returns {OKKISyncLog|null}
 */
async function update(logId, updates) {
  const logs = readLogs();
  const index = logs.findIndex(l => l.id === logId);
  if (index === -1) {
    return null;
  }
  
  logs[index] = { ...logs[index], ...updates };
  writeLogs(logs);
  return new OKKISyncLog(logs[index]);
}

/**
 * 删除日志
 * @param {string} logId - 日志 ID
 * @returns {boolean}
 */
async function remove(logId) {
  const logs = readLogs();
  const filtered = logs.filter(l => l.id !== logId);
  if (filtered.length === logs.length) {
    return false;
  }
  writeLogs(filtered);
  return true;
}

/**
 * 获取所有日志
 * @param {object} filters - 过滤条件
 * @returns {Array<OKKISyncLog>}
 */
async function findAll(filters = {}) {
  let logs = readLogs();
  
  if (filters.status) {
    logs = logs.filter(l => l.status === filters.status);
  }
  
  if (filters.startDate) {
    logs = logs.filter(l => new Date(l.sync_time) >= new Date(filters.startDate));
  }
  
  if (filters.endDate) {
    logs = logs.filter(l => new Date(l.sync_time) <= new Date(filters.endDate));
  }
  
  return logs
    .sort((a, b) => new Date(b.sync_time) - new Date(a.sync_time))
    .map(l => new OKKISyncLog(l));
}

/**
 * 清理旧日志
 * @param {number} daysToKeep - 保留天数
 * @returns {number} 删除的日志数量
 */
async function cleanup(daysToKeep = 30) {
  const logs = readLogs();
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);
  
  const filtered = logs.filter(l => new Date(l.sync_time) >= cutoffDate);
  const deletedCount = logs.length - filtered.length;
  
  writeLogs(filtered);
  return deletedCount;
}

module.exports = {
  OKKISyncLog,
  create,
  findByLogisticsId,
  findById,
  update,
  remove,
  findAll,
  cleanup
};

/**
 * Exception Logger - 异常日志记录器
 * 
 * 负责将异常记录持久化到本地 JSON 文件，支持查询、标记解决、统计等功能
 */

const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(__dirname, '../logs/exceptions.json');

/**
 * 确保日志文件存在
 */
function ensureLogFile() {
  const dir = path.dirname(LOG_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  if (!fs.existsSync(LOG_FILE)) {
    fs.writeFileSync(LOG_FILE, JSON.stringify({ exceptions: [], meta: { created_at: new Date().toISOString() } }, null, 2));
  }
}

/**
 * 读取日志数据
 */
function readLogData() {
  ensureLogFile();
  try {
    const content = fs.readFileSync(LOG_FILE, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error('[ExceptionLogger] Failed to read log file:', error.message);
    return { exceptions: [], meta: { created_at: new Date().toISOString() } };
  }
}

/**
 * 写入日志数据
 */
function writeLogData(data) {
  ensureLogFile();
  try {
    fs.writeFileSync(LOG_FILE, JSON.stringify(data, null, 2));
    return true;
  } catch (error) {
    console.error('[ExceptionLogger] Failed to write log file:', error.message);
    return false;
  }
}

/**
 * 生成唯一异常 ID
 */
function generateExceptionId() {
  return `EXC-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
}

/**
 * 记录异常到文件
 * @param {Object} exception - 异常对象
 * @returns {string} 异常 ID
 */
function logException(exception) {
  const data = readLogData();
  
  const exceptionRecord = {
    id: exception.id || generateExceptionId(),
    type: exception.type || 'unknown',
    severity: exception.severity || 'info',
    timestamp: exception.timestamp || new Date().toISOString(),
    message: exception.message || '',
    context: exception.context || {},
    resolved: false,
    resolved_at: null,
    resolved_by: null,
    alert_sent: exception.alert_sent || false,
    alert_channels: exception.alert_channels || []
  };
  
  data.exceptions.push(exceptionRecord);
  writeLogData(data);
  
  console.log(`[ExceptionLogger] Logged exception: ${exceptionRecord.id} (${exceptionRecord.type})`);
  return exceptionRecord.id;
}

/**
 * 查询异常记录
 * @param {Object} filter - 过滤条件
 * @returns {Array} 异常记录列表
 */
function getExceptions(filter = {}) {
  const data = readLogData();
  let results = data.exceptions;
  
  if (filter.type) {
    results = results.filter(ex => ex.type === filter.type);
  }
  if (filter.severity) {
    results = results.filter(ex => ex.severity === filter.severity);
  }
  if (filter.resolved !== undefined) {
    results = results.filter(ex => ex.resolved === filter.resolved);
  }
  if (filter.after) {
    const afterDate = new Date(filter.after).getTime();
    results = results.filter(ex => new Date(ex.timestamp).getTime() >= afterDate);
  }
  if (filter.before) {
    const beforeDate = new Date(filter.before).getTime();
    results = results.filter(ex => new Date(ex.timestamp).getTime() <= beforeDate);
  }
  if (filter.limit) {
    results = results.slice(-filter.limit);
  }
  
  return results;
}

/**
 * 根据 ID 获取异常记录
 * @param {string} exceptionId - 异常 ID
 * @returns {Object|null} 异常记录
 */
function getExceptionById(exceptionId) {
  const data = readLogData();
  return data.exceptions.find(ex => ex.id === exceptionId) || null;
}

/**
 * 标记异常已解决
 * @param {string} exceptionId - 异常 ID
 * @param {Object} options - 解决选项
 * @returns {boolean} 是否成功
 */
function markResolved(exceptionId, options = {}) {
  const data = readLogData();
  const exception = data.exceptions.find(ex => ex.id === exceptionId);
  
  if (!exception) {
    console.error(`[ExceptionLogger] Exception not found: ${exceptionId}`);
    return false;
  }
  
  exception.resolved = true;
  exception.resolved_at = new Date().toISOString();
  exception.resolved_by = options.resolved_by || 'system';
  exception.resolution_notes = options.notes || '';
  
  writeLogData(data);
  console.log(`[ExceptionLogger] Marked exception resolved: ${exceptionId}`);
  return true;
}

/**
 * 获取异常统计
 * @returns {Object} 统计信息
 */
function getStats() {
  const data = readLogData();
  const exceptions = data.exceptions;
  
  const stats = {
    total: exceptions.length,
    by_severity: {
      critical: 0,
      warning: 0,
      info: 0
    },
    by_type: {},
    resolved: 0,
    unresolved: 0,
    last_24h: 0
  };
  
  const now = Date.now();
  const twentyFourHoursAgo = now - (24 * 60 * 60 * 1000);
  
  exceptions.forEach(ex => {
    // By severity
    if (stats.by_severity.hasOwnProperty(ex.severity)) {
      stats.by_severity[ex.severity]++;
    }
    
    // By type
    if (!stats.by_type[ex.type]) {
      stats.by_type[ex.type] = { total: 0, resolved: 0, unresolved: 0 };
    }
    stats.by_type[ex.type].total++;
    if (ex.resolved) {
      stats.by_type[ex.type].resolved++;
      stats.resolved++;
    } else {
      stats.by_type[ex.type].unresolved++;
      stats.unresolved++;
    }
    
    // Last 24h
    if (new Date(ex.timestamp).getTime() >= twentyFourHoursAgo) {
      stats.last_24h++;
    }
  });
  
  return stats;
}

/**
 * 更新异常记录
 * @param {string} exceptionId - 异常 ID
 * @param {Object} updates - 更新字段
 * @returns {boolean} 是否成功
 */
function updateException(exceptionId, updates) {
  const data = readLogData();
  const exception = data.exceptions.find(ex => ex.id === exceptionId);
  
  if (!exception) {
    console.error(`[ExceptionLogger] Exception not found: ${exceptionId}`);
    return false;
  }
  
  Object.assign(exception, updates);
  writeLogData(data);
  return true;
}

/**
 * 清理旧异常记录
 * @param {number} retentionDays - 保留天数
 * @returns {number} 删除的记录数
 */
function cleanupOldExceptions(retentionDays = 30) {
  const data = readLogData();
  const cutoffDate = Date.now() - (retentionDays * 24 * 60 * 60 * 1000);
  
  const originalCount = data.exceptions.length;
  data.exceptions = data.exceptions.filter(ex => {
    return new Date(ex.timestamp).getTime() >= cutoffDate;
  });
  
  const deletedCount = originalCount - data.exceptions.length;
  
  if (deletedCount > 0) {
    writeLogData(data);
    console.log(`[ExceptionLogger] Cleaned up ${deletedCount} old exceptions (older than ${retentionDays} days)`);
  }
  
  return deletedCount;
}

module.exports = {
  logException,
  getExceptions,
  getExceptionById,
  markResolved,
  getStats,
  updateException,
  cleanupOldExceptions,
  LOG_FILE
};

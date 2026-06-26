/**
 * 日志管理器 - 完整操作日志系统
 * 支持：多级别日志、文件存储、审计日志
 * 
 * 版本：v1.0
 * 更新日期：2026-04-02
 */

const fs = require('fs');
const path = require('path');

// ==================== 配置加载 ====================

let logConfig = null;
const CONFIG_PATH = path.join(__dirname, '../config/log_config.json');
const LOG_DIR = path.join(__dirname, '../logs');
const DATA_DIR = path.join(__dirname, '../data');

// 日志缓存（用于批量写入）
const logBuffer = [];
const FLUSH_INTERVAL = 5000; // 5秒刷新一次

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
      logConfig = JSON.parse(content);
    }
  } catch (error) {
    logConfig = getDefaultConfig();
  }
  
  // 确保日志目录存在
  ensureDirectory(LOG_DIR);
  ensureDirectory(DATA_DIR);
  
  return logConfig;
}

function getDefaultConfig() {
  return {
    enabled: true,
    level: 'info',
    levels: ['debug', 'info', 'warn', 'error'],
    transports: {
      file: { enabled: true },
      console: { enabled: true }
    }
  };
}

function ensureDirectory(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// ==================== 核心函数 ====================

const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

/**
 * 写入日志
 * @param {string} level 日志级别
 * @param {string} message 日志消息
 * @param {object} meta 元数据
 */
function log(level, message, meta = {}) {
  if (!logConfig) {
    loadConfig();
  }
  
  if (!logConfig.enabled) return;
  
  // 检查日志级别
  if (LOG_LEVELS[level] < LOG_LEVELS[logConfig.level]) {
    return;
  }
  
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level,
    message,
    ...meta
  };
  
  // 控制台输出
  if (logConfig.transports?.console?.enabled) {
    outputToConsole(logEntry);
  }
  
  // 文件输出
  if (logConfig.transports?.file?.enabled) {
    logBuffer.push(logEntry);
  }
  
  // 审计日志（特定事件）
  if (logConfig.auditLog?.enabled && logConfig.auditLog?.events?.includes(meta.event)) {
    writeAuditLog(logEntry);
  }
}

/**
 * 控制台输出
 * @param {object} entry 日志条目
 */
function outputToConsole(entry) {
  const colors = {
    debug: '\x1b[36m', // 青色
    info: '\x1b[32m',  // 绿色
    warn: '\x1b[33m',  // 黄色
    error: '\x1b[31m'  // 红色
  };
  const reset = '\x1b[0m';
  
  const color = logConfig.transports?.console?.colorize ? (colors[entry.level] || '') : '';
  const levelStr = `[${entry.level.toUpperCase()}]`.padEnd(7);
  
  console.log(`${color}${entry.timestamp} ${levelStr}${reset} ${entry.message}`);
  
  // 输出元数据
  if (entry.event || entry.accountId || entry.videoId || entry.error) {
    const meta = { ...entry };
    delete meta.timestamp;
    delete meta.level;
    delete meta.message;
    if (Object.keys(meta).length > 0) {
      console.log('  ', JSON.stringify(meta));
    }
  }
}

/**
 * 刷新日志缓冲区到文件
 */
function flushLogs() {
  if (logBuffer.length === 0) return;
  
  const today = new Date().toISOString().split('T')[0];
  const filename = `douyin-reply-${today}.log`;
  const filepath = path.join(LOG_DIR, filename);
  
  const logsToWrite = logBuffer.splice(0);
  const content = logsToWrite.map(entry => JSON.stringify(entry)).join('\n') + '\n';
  
  fs.appendFileSync(filepath, content, 'utf-8');
}

/**
 * 写入审计日志
 * @param {object} entry 日志条目
 */
function writeAuditLog(entry) {
  const today = new Date().toISOString().split('T')[0];
  const filename = `audit-${today}.log`;
  const filepath = path.join(LOG_DIR, 'audit', filename);
  
  ensureDirectory(path.join(LOG_DIR, 'audit'));
  
  fs.appendFileSync(filepath, JSON.stringify(entry) + '\n', 'utf-8');
}

// ==================== 便捷方法 ====================

function debug(message, meta) {
  log('debug', message, meta);
}

function info(message, meta) {
  log('info', message, meta);
}

function warn(message, meta) {
  log('warn', message, meta);
}

function error(message, meta) {
  log('error', message, meta);
}

// ==================== 业务日志方法 ====================

/**
 * 记录回复发送日志
 * @param {object} data 回复数据
 */
function logReplySent(data) {
  info(`回复已发送: ${data.commentId}`, {
    event: 'reply_sent',
    accountId: data.accountId,
    videoId: data.videoId,
    commentId: data.commentId,
    replyContent: data.replyContent?.substring(0, 50),
    replyType: data.replyType // 'template' | 'ai'
  });
}

/**
 * 记录回复失败日志
 * @param {object} data 失败数据
 */
function logReplyFailed(data) {
  error(`回复失败: ${data.commentId}`, {
    event: 'reply_failed',
    accountId: data.accountId,
    commentId: data.commentId,
    error: data.error
  });
}

/**
 * 记录敏感词检测日志
 * @param {object} data 检测数据
 */
function logSensitiveDetected(data) {
  warn(`敏感词检测: ${data.level}`, {
    event: 'sensitive_detected',
    commentId: data.commentId,
    level: data.level,
    matchedWords: data.matchedWords,
    action: data.action
  });
}

/**
 * 记录频率限制触发日志
 * @param {object} data 限制数据
 */
function logRateLimitTriggered(data) {
  warn(`频率限制触发: ${data.limitType}`, {
    event: 'rate_limit_triggered',
    limitType: data.limitType,
    current: data.current,
    max: data.max,
    waitMs: data.waitMs
  });
}

/**
 * 记录监控状态日志
 * @param {string} action 动作
 * @param {object} data 数据
 */
function logMonitor(action, data) {
  info(`监控${action}`, {
    event: `monitor_${action}`,
    ...data
  });
}

/**
 * 记录错误日志
 * @param {string} message 错误消息
 * @param {Error|object} error 错误对象
 */
function logError(message, error) {
  const errorData = error instanceof Error 
    ? { name: error.name, message: error.message, stack: error.stack }
    : error;
  
  error(message, {
    event: 'error_occurred',
    error: errorData
  });
}

// ==================== 日志查询 ====================

/**
 * 查询日志
 * @param {object} options 查询选项
 */
function queryLogs(options = {}) {
  const {
    startDate = new Date().toISOString().split('T')[0],
    endDate,
    level,
    event,
    limit = 100
  } = options;
  
  const results = [];
  const filesToRead = endDate ? getDateRange(startDate, endDate) : [startDate];
  
  for (const date of filesToRead) {
    const filename = `douyin-reply-${date}.log`;
    const filepath = path.join(LOG_DIR, filename);
    
    if (!fs.existsSync(filepath)) continue;
    
    const content = fs.readFileSync(filepath, 'utf-8');
    const lines = content.trim().split('\n');
    
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        
        // 过滤条件
        if (level && entry.level !== level) continue;
        if (event && entry.event !== event) continue;
        
        results.push(entry);
        
        if (results.length >= limit) break;
      } catch (e) {
        // 跳过解析失败的行
      }
    }
    
    if (results.length >= limit) break;
  }
  
  return results;
}

function getDateRange(start, end) {
  const dates = [];
  const startMs = new Date(start).getTime();
  const endMs = new Date(end).getTime();
  
  for (let ms = startMs; ms <= endMs; ms += 86400000) {
    dates.push(new Date(ms).toISOString().split('T')[0]);
  }
  
  return dates;
}

// ==================== 导出 ====================

module.exports = {
  // 基础方法
  log,
  debug,
  info,
  warn,
  error,
  
  // 业务日志
  logReplySent,
  logReplyFailed,
  logSensitiveDetected,
  logRateLimitTriggered,
  logMonitor,
  logError,
  
  // 查询
  queryLogs,
  
  // 配置
  loadConfig,
  flushLogs
};

// 初始化
loadConfig();

// 定时刷新日志缓冲区
setInterval(flushLogs, FLUSH_INTERVAL);

// 进程退出时刷新
process.on('beforeExit', flushLogs);
process.on('SIGINT', () => {
  flushLogs();
  process.exit(0);
});

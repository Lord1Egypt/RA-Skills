/**
 * logger.js - 日志工具
 */

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

const currentLevel = parseInt(process.env.MEMORY_LOG_LEVEL || '1');

export function log(level, ...args) {
  const lvl = LOG_LEVELS[level] ?? LOG_LEVELS.INFO;
  if (lvl < currentLevel) return;
  
  const timestamp = new Date().toISOString().slice(11, 23);
  const prefix = level === 'ERROR' ? '❌' : level === 'WARN' ? '⚠️' : 'ℹ️';
  console.error(`${timestamp} ${prefix} [${level}]`, ...args);
}

// 兼容新代码（有些模块 import { logger } from '../utils/logger.js'）
const logger = {
  debug: (...args) => log('DEBUG', ...args),
  info: (...args) => log('INFO', ...args),
  warn: (...args) => log('WARN', ...args),
  error: (...args) => log('ERROR', ...args),
};
export { logger };

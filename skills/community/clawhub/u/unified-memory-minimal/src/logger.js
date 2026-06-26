/**
 * Structured Logger v1.0
 * 输出 JSON 格式日志，支持 levels: debug/info/warn/error
 * 日志输出到：stdout + 文件（config.logDir/mcp-{date}.log）
 */

import { appendFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

export const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };

export class StructuredLogger {
  constructor(context = {}) {
    this.context = context;
    this.minLevel = LOG_LEVELS[process.env.LOG_LEVEL || 'info'];
    this._logDir = this._ensureLogDir();
  }

  _ensureLogDir() {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const HOME = process.env.HOME || '/root';
    const LOG_DIR = join(HOME, '.openclaw', 'workspace', 'memory', 'logs');
    if (!existsSync(LOG_DIR)) {
      mkdirSync(LOG_DIR, { recursive: true });
    }
    return LOG_DIR;
  }

  _format(level, msg, data = {}) {
    return JSON.stringify({
      ts: new Date().toISOString(),
      level,
      msg,
      pid: process.pid,
      ...this.context,
      ...data,
    });
  }

  _write(level, formatted) {
    const logFile = join(this._logDir, `mcp-${new Date().toISOString().slice(0, 10)}.log`);
    try {
      appendFileSync(logFile, formatted + '\n');
    } catch { }
    if (level === 'error' || level === 'warn') {
      console.error(formatted);
    } else {
      console.log(formatted);
    }
  }

  debug(msg, data) { if (this.minLevel <= 0) this._write('debug', this._format('debug', msg, data)); }
  info(msg, data) { if (this.minLevel <= 1) this._write('info', this._format('info', msg, data)); }
  warn(msg, data) { if (this.minLevel <= 2) this._write('warn', this._format('warn', msg, data)); }
  error(msg, data) { if (this.minLevel <= 3) this._write('error', this._format('error', msg, data)); }
}

let globalLogger = null;

export function getLogger(context = {}) {
  if (!globalLogger) {
    globalLogger = new StructuredLogger(context);
  }
  return globalLogger;
}

// 便捷函数
export const log = {
  debug: (msg, data) => getLogger().debug(msg, data),
  info: (msg, data) => getLogger().info(msg, data),
  warn: (msg, data) => getLogger().warn(msg, data),
  error: (msg, data) => getLogger().error(msg, data),
};

// 兼容旧代码（有些模块 import { logger } from '../logger.js'）
export const logger = getLogger();

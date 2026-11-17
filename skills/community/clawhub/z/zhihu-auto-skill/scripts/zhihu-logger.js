/**
 * zhihu-logger.js — 统一日志框架
 *
 * 为知乎自动化 Skill 提供结构化、分级的日志能力。
 *
 * 特性:
 * - 4 级日志: DEBUG / INFO / WARN / ERROR
 * - 控制台输出（带颜色/模块标签）
 * - JSONL 文件输出（~/.hermes/logs/zhihu/）
 * - 子日志器（模块层级继承）
 * - 全局级别动态控制
 * - 兼容 writeLog() 旧接口
 *
 * P2-1: 统一日志框架
 *
 * @module zhihu-logger
 */

import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';

// ──────────────────────────────────────────
// 日志级别定义
// ──────────────────────────────────────────

/** @enum {number} */
const LEVELS = {
  DEBUG: 0,
  INFO:  1,
  WARN:  2,
  ERROR: 3,
};

/** @type {Object<string,string>} */
const LEVEL_LABELS = {
  DEBUG: 'DEBUG',
  INFO:  'INFO',
  WARN:  'WARN',
  ERROR: 'ERROR',
};

/** @type {Object<string,number>} */
const LEVEL_COLORS = {
  DEBUG: 90,  // 灰色
  INFO:  36,  // 青色
  WARN:  33,  // 黄色
  ERROR: 31,  // 红色
};

// ──────────────────────────────────────────
// 日志目录
// ──────────────────────────────────────────

const LOG_DIR = resolve(homedir(), '.hermes', 'logs', 'zhihu');

function ensureLogDir() {
  if (!existsSync(LOG_DIR)) {
    mkdirSync(LOG_DIR, { recursive: true });
  }
}

// ──────────────────────────────────────────
// Logger 类
// ──────────────────────────────────────────

/**
 * 统一日志器
 *
 * @class
 * @example
 * const log = new Logger('zhihu-core');
 * log.info('浏览器已启动', { pid: 1234 });
 * log.warn('Cookie 即将过期', { expiresInDays: 3 });
 * log.error('初始化失败', err);
 *
 * const child = log.child('browser');
 * child.debug('导航到页面', { url: 'https://...' });
 */
class Logger {
  /**
   * @param {string} name - 模块名称（显示在日志标签中）
   * @param {object} [options] - 配置项
   * @param {number} [options.level] - 日志级别，默认继承全局级别
   * @param {boolean} [options.console=true] - 是否输出到控制台
   * @param {boolean} [options.file=true] - 是否输出到文件
   */
  constructor(name, options = {}) {
    /** @type {string} */
    this.name = name;
    /** @type {number|undefined} */
    this._level = options.level;
    /** @type {boolean} */
    this._console = options.console !== false;
    /** @type {boolean} */
    this._file = options.file !== false;
  }

  /**
   * 获取当前有效日志级别
   * @returns {number}
   */
  _effectiveLevel() {
    return this._level !== undefined ? this._level : Logger._globalLevel;
  }

  /**
   * 核心日志方法
   * @param {string} level - 级别名 (DEBUG|INFO|WARN|ERROR)
   * @param {string} message - 日志消息
   * @param {*} [data] - 附加数据（Error 对象或任意数据）
   */
  _log(level, message, data) {
    const levelNum = LEVELS[level];
    if (levelNum < this._effectiveLevel()) return;

    const timestamp = new Date().toISOString();
    const moduleTag = `[${this.name}]`;

    // ── 构造结构化日志条目 ──
    /** @type {object} */
    const entry = {
      timestamp,
      level,
      module: this.name,
      message,
      data: data instanceof Error
        ? { name: data.name, message: data.message, stack: data.stack?.split('\n').slice(0, 4).join('\n') }
        : data !== undefined ? data : undefined,
    };

    // ── 控制台输出（带颜色） ──
    if (this._console) {
      const color = LEVEL_COLORS[level] || 0;
      const label = level.padEnd(5);
      const prefix = `\x1b[${color}m${label}\x1b[0m \x1b[2m${moduleTag}\x1b[0m`;
      const line = `${prefix} ${message}`;

      if (level === 'ERROR') {
        console.error(line);
        if (data instanceof Error && data.stack) {
          console.error(`\x1b[2m  ${data.stack.split('\n').slice(1, 4).join('\n')}\x1b[0m`);
        }
      } else if (level === 'WARN') {
        console.warn(line);
      } else {
        console.log(line);
      }
    }

    // ── 文件输出（JSONL） ──
    if (this._file) {
      try {
        ensureLogDir();
        const date = timestamp.slice(0, 10);
        const logFile = resolve(LOG_DIR, `${date}.jsonl`);
        writeFileSync(logFile, JSON.stringify(entry) + '\n', { flag: 'a' });
      } catch (err) {
        // 日志写入失败时不抛异常，仅 console 提醒
        console.error(`\x1b[31mERROR\x1b[0m [zhihu-logger] 日志文件写入失败: ${err.message}`);
      }
    }
  }

  // ── 便捷方法 ────────────────────────────

  /**
   * 写 DEBUG 日志
   * @param {string} message
   * @param {*} [data]
   */
  debug(message, data) { this._log('DEBUG', message, data); }

  /**
   * 写 INFO 日志
   * @param {string} message
   * @param {*} [data]
   */
  info(message, data) { this._log('INFO', message, data); }

  /**
   * 写 WARN 日志
   * @param {string} message
   * @param {*} [data]
   */
  warn(message, data) { this._log('WARN', message, data); }

  /**
   * 写 ERROR 日志
   * @param {string} message
   * @param {*} [data]
   */
  error(message, data) { this._log('ERROR', message, data); }

  /**
   * 创建子日志器（继承父日志器的配置）
   * @param {string} subName - 子模块名称
   * @param {object} [overrides] - 覆盖配置
   * @returns {Logger}
   */
  child(subName, overrides = {}) {
    const fullName = `${this.name}:${subName}`;
    return new Logger(fullName, {
      level: this._level,
      console: this._console,
      file: this._file,
      ...overrides,
    });
  }
}

// ──────────────────────────────────────────
// 全局配置
// ──────────────────────────────────────────

/** @type {number} 全局默认日志级别 */
Logger._globalLevel = LEVELS.INFO;

/**
 * 设置全局日志级别
 * @param {string|number} level - 级别名 (DEBUG|INFO|WARN|ERROR) 或 LEVELS 数值
 */
Logger.setGlobalLevel = function setGlobalLevel(level) {
  if (typeof level === 'string') {
    const n = LEVELS[level.toUpperCase()];
    if (n !== undefined) {
      Logger._globalLevel = n;
    }
  } else if (typeof level === 'number' && level >= 0 && level <= 3) {
    Logger._globalLevel = level;
  }
};

// ──────────────────────────────────────────
// 预创建模块日志器
// ──────────────────────────────────────────

/** @type {Logger} */
const coreLog = new Logger('zhihu-core');

/** @type {Logger} */
const browserLog = new Logger('zhihu-browser');

/** @type {Logger} */
const httpLog = new Logger('zhihu-http');

/** @type {Logger} */
const publishLog = new Logger('zhihu-publish');

/** @type {Logger} */
const signatureLog = new Logger('zhihu-signature');

/** @type {Logger} */
const bridgeLog = new Logger('zhihu-bridge');

/** @type {Logger} */
const extractLog = new Logger('zhihu-extract');

/** @type {Logger} */
const interactLog = new Logger('zhihu-interact');

/** @type {Logger} */
const answerLog = new Logger('zhihu-answer');

/** @type {Logger} */
const askLog = new Logger('zhihu-ask');

/** @type {Logger} */
const ratelimiterLog = new Logger('zhihu-ratelimiter');

/** @type {Logger} */
const exportLog = new Logger('zhihu-export');

/** @type {Logger} */
const setupLog = new Logger('zhihu-setup');

/** @type {Logger} */
const testLog = new Logger('zhihu-test');

/** @type {Logger} */
const cliLog = new Logger('zhihu-cli');

// ──────────────────────────────────────────
// 兼容 writeLog 旧接口
// ──────────────────────────────────────────

/**
 * 写操作日志（JSONL 格式）— 兼容旧接口
 *
 * 旧的 writeLog 接口使用结构体 { module, operation, status, ... }
 * 此函数将其桥接到新的 Logger 体系。
 *
 * @param {object} entry - 日志条目
 * @param {string} [entry.level='INFO'] - 日志级别
 * @param {string} [entry.module='zhihu-core'] - 模块名
 * @param {string} entry.operation - 操作名
 * @param {string} [entry.status] - 操作状态
 * @param {number} [entry.duration_ms] - 耗时
 * @param {string} [entry.error] - 错误信息
 * @param {object} [entry.details] - 详情
 * @deprecated 建议直接使用 Logger 实例
 */
function writeLog(entry) {
  const level = entry.level || 'INFO';
  const moduleName = entry.module || 'zhihu-core';

  // 用模块名查找或创建临时日志器
  const loggers = {
    'zhihu-core': coreLog,
    'zhihu-http': httpLog,
    'zhihu-browser': browserLog,
    'zhihu-publish': publishLog,
    'zhihu-signature': signatureLog,
    'zhihu-bridge': bridgeLog,
  };
  const logger = loggers[moduleName] || new Logger(moduleName);

  const msg = entry.error
    ? `${entry.operation}: ${entry.error}`
    : `${entry.operation}${entry.status ? ` → ${entry.status}` : ''}`;

  const data = {
    ...(entry.details || {}),
    ...(entry.duration_ms ? { duration_ms: entry.duration_ms } : {}),
  };

  logger._log(level, msg, Object.keys(data).length > 0 ? data : undefined);
}

// ──────────────────────────────────────────
// 导出
// ──────────────────────────────────────────

export {
  Logger,
  LEVELS,
  writeLog,
  // 预创建日志器
  coreLog,
  browserLog,
  httpLog,
  publishLog,
  signatureLog,
  bridgeLog,
  extractLog,
  interactLog,
  answerLog,
  askLog,
  ratelimiterLog,
  exportLog,
  setupLog,
  testLog,
  cliLog,
};

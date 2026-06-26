#!/usr/bin/env node
/**
 * 统一常量管理
 *
 * 所有 MAGIC 数字、CONFIG 配置、LOG_SCHEMA、ERROR_CODES 集中于此，
 * 消除跨文件重复定义。
 */

const os = require('os');
const path = require('path');

// ==================== 魔法数字常量 ====================
const MAGIC = {
  // 置信度与评分
  CONFIDENCE_THRESHOLD: 0.6,
  QUERY_MAX_LENGTH: 50,
  WEIGHT_EXPLICIT: 1.0,
  WEIGHT_HIGH: 0.9,
  WEIGHT_MEDIUM_HIGH: 0.85,
  WEIGHT_MEDIUM: 0.8,
  WEIGHT_DOMAIN: 0.7,
  NEGATIVE_MULTIPLIER: 0.5,
  DOMAIN_MIN_CONFIDENCE: 0.8,
  INSTALLS_SCORE_FACTOR: 10,
  TRUSTED_SCORE: 30,
  UNTRUSTED_SCORE: 10,
  MIN_INSTALLS_SCALE: 10000,

  // 缓存
  CACHE_TTL_MS: 10 * 60 * 1000, // 10 分钟
  CACHE_MAX_SIZE: 100,
  CACHE_CLEANUP_THRESHOLD: 100,

  // 重试
  MAX_RETRIES: 3,
  RETRY_DELAY_MS: 1000,
  CLI_TIMEOUT: 60000, // 命令超时

  // 日志
  LOG_VERSION: '1.0',
  MAX_LOG_ENTRIES: 100,

  // 垃圾清理
  TRASH_CLEAN_DAYS: 7,
  TRASH_CLEAN_INTERVAL_MS: 60 * 60 * 1000, // 1 小时

  // 脱敏
  SANITIZE_MAX_DEPTH: 10
};

// ==================== 错误码 ====================
const ERROR_CODES = {
  // 分析阶段
  CONFIDENCE_TOO_LOW: 'CONFIDENCE_TOO_LOW',
  INVALID_INPUT: 'INVALID_INPUT',
  // 搜索阶段
  CLI_NOT_FOUND: 'CLI_NOT_FOUND',
  NETWORK_ERROR: 'NETWORK_ERROR',
  PARSE_FAILED: 'PARSE_FAILED',
  SEARCH_FAILED: 'SEARCH_FAILED',
  NO_RESULTS: 'NO_RESULTS',
  // 筛选阶段
  // 安装阶段
  ALREADY_INSTALLED: 'ALREADY_INSTALLED',
  INSTALL_FAILED: 'INSTALL_FAILED',
  PERMISSION_DENIED: 'PERMISSION_DENIED',
  INVALID_SKILL_FORMAT: 'INVALID_SKILL_FORMAT'
};

// ==================== 日志 Schema ====================
const LOG_SCHEMA = {
  VERSION: MAGIC.LOG_VERSION,
  ACTIONS: ['discover', 'install', 'remove', 'error', 'cache_hit', 'cache_miss'],
  REQUIRED_FIELDS: ['timestamp', 'action', 'input']
};

// ==================== CLI 配置 ====================
const CLI_CONFIG = {
  maxRetries: MAGIC.MAX_RETRIES,
  retryDelay: MAGIC.RETRY_DELAY_MS,
  timeout: MAGIC.CLI_TIMEOUT
};

// ==================== 发现引擎配置 ====================
const DISCOVER_CONFIG = {
  confidenceThreshold: MAGIC.CONFIDENCE_THRESHOLD,
  trustedOwners: ['vercel-labs', 'anthropics', 'google-labs-code', 'microsoft', 'openai', 'openclaw'],
  cache: {
    ttl: MAGIC.CACHE_TTL_MS,
    maxSize: MAGIC.CACHE_MAX_SIZE
  }
};

// ==================== ClawHub 配置 ====================
const CLAWHUB_CONFIG = {
  apiBase: 'https://clawhub.ai',
  searchEndpoint: '/api/v1/search',
  timeout: 10000,
  maxResults: 10
};

// ==================== OpenClaw Hook 配置 ====================
const HOOK_CONFIG = {
  openclawDir: process.env.OPENCLAW_DIR || path.join(os.homedir(), '.openclaw'),
  maxLogEntries: MAGIC.MAX_LOG_ENTRIES,
  trashPath: process.env.TRASH_DIR || path.join(os.homedir(), '.openclaw', '.trash')
};

Object.defineProperty(HOOK_CONFIG, 'logPath', {
  get() {
    return path.join(this.openclawDir, 'logs', 'skill-discovery-v3.json');
  }
});

// ==================== 导出 ====================
module.exports = {
  MAGIC,
  ERROR_CODES,
  LOG_SCHEMA,
  CLI_CONFIG,
  DISCOVER_CONFIG,
  CLAWHUB_CONFIG,
  HOOK_CONFIG
};

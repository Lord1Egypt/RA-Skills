/**
 * 配置管理模块
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const CONFIG_PATH = join(WORKSPACE, '.soul', 'scanner-config.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 扫描参数
  scanIntervalHours: 24,
  minConfidenceForUse: 0.7,
  minEvidenceCount: 2,
  contradictionThreshold: 0.3,
  maxProfileAgeDays: 90,
  
  // 扫描范围
  scanMemoryFiles: true,
  scanRecentDays: 30,
  includeNarrative: true,
  scanAllHistory: false,
  
  // 分析参数
  analyzeHabits: true,
  analyzeValues: true,
  analyzePreferences: true,
  analyzeCommunication: true,
  analyzeLearning: true,
  
  // 信号参数
  publishPatternSignals: true,
  publishContradictionSignals: true,
  publishProfileUpdateSignals: true,
  publishQuizSignals: true,
  
  // Quiz参数
  generateQuizzes: true,
  maxQuizzesPerSession: 3,
  quizConfidenceThreshold: 0.5,
  quizMinIntervalHours: 6,
  
  // 隐私参数
  excludeSensitiveTopics: true,
  anonymizeEvidence: false,
  requireConsentForPatterns: true,
  
  // 调试
  debugMode: false,
  logDetailedAnalysis: false,
  saveEvidenceSamples: true
};

/**
 * 加载配置
 * @returns {object} 配置对象
 */
export function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    saveConfig(DEFAULT_CONFIG);
    return { ...DEFAULT_CONFIG };
  }
  
  try {
    const userConfig = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
    // 深度合并，确保新字段有默认值
    return deepMerge(DEFAULT_CONFIG, userConfig);
  } catch (error) {
    console.error('加载配置失败，使用默认配置:', error.message);
    return { ...DEFAULT_CONFIG };
  }
}

/**
 * 保存配置
 * @param {object} config 配置对象
 */
export function saveConfig(config) {
  const dir = join(WORKSPACE, '.soul');
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  
  try {
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
    console.log('配置已保存:', CONFIG_PATH);
  } catch (error) {
    console.error('保存配置失败:', error.message);
  }
}

/**
 * 更新配置字段
 * @param {string} key 配置键（支持点表示法，如'scanParameters.intervalHours'）
 * @param {any} value 新值
 */
export function updateConfig(key, value) {
  const config = loadConfig();
  
  // 使用点表示法设置嵌套属性
  const keys = key.split('.');
  let current = config;
  
  for (let i = 0; i < keys.length - 1; i++) {
    if (!current[keys[i]] || typeof current[keys[i]] !== 'object') {
      current[keys[i]] = {};
    }
    current = current[keys[i]];
  }
  
  current[keys[keys.length - 1]] = value;
  saveConfig(config);
  
  console.log(`配置已更新: ${key} = ${JSON.stringify(value)}`);
}

/**
 * 获取配置值
 * @param {string} key 配置键
 * @param {any} defaultValue 默认值
 * @returns {any} 配置值
 */
export function getConfigValue(key, defaultValue = undefined) {
  const config = loadConfig();
  const keys = key.split('.');
  let current = config;
  
  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      return defaultValue;
    }
  }
  
  return current !== undefined ? current : defaultValue;
}

/**
 * 重置为默认配置
 */
export function resetToDefaults() {
  saveConfig(DEFAULT_CONFIG);
  console.log('配置已重置为默认值');
}

/**
 * 显示当前配置
 */
export function showConfig() {
  const config = loadConfig();
  console.log('当前配置:');
  console.log(JSON.stringify(config, null, 2));
}

/**
 * 验证配置有效性
 * @returns {Array} 问题列表
 */
export function validateConfig() {
  const config = loadConfig();
  const issues = [];
  
  // 验证数值范围
  if (config.scanIntervalHours < 1 || config.scanIntervalHours > 720) {
    issues.push(`scanIntervalHours 应在 1-720 之间，当前: ${config.scanIntervalHours}`);
  }
  
  if (config.minConfidenceForUse < 0 || config.minConfidenceForUse > 1) {
    issues.push(`minConfidenceForUse 应在 0-1 之间，当前: ${config.minConfidenceForUse}`);
  }
  
  if (config.quizConfidenceThreshold < 0 || config.quizConfidenceThreshold > 1) {
    issues.push(`quizConfidenceThreshold 应在 0-1 之间，当前: ${config.quizConfidenceThreshold}`);
  }
  
  if (config.maxQuizzesPerSession < 0 || config.maxQuizzesPerSession > 10) {
    issues.push(`maxQuizzesPerSession 应在 0-10 之间，当前: ${config.maxQuizzesPerSession}`);
  }
  
  return issues;
}

// 深度合并函数
function deepMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
}

export default {
  loadConfig,
  saveConfig,
  updateConfig,
  getConfigValue,
  resetToDefaults,
  showConfig,
  validateConfig,
  DEFAULT_CONFIG
};
/**
 * 配置管理模块
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const CONFIG_PATH = join(WORKSPACE, '.soul', 'guard-config.json');

// 默认配置
const DEFAULT_CONFIG = {
  // 监测参数
  driftThresholdL1: 0.3,    // L1观察记录阈值
  driftThresholdL2: 0.5,    // L2温和提醒阈值  
  driftThresholdL3: 0.7,    // L3严肃对话阈值
  driftThresholdL4: 0.9,    // L4强制干预阈值
  
  // 边界参数
  timeBoundaryStart: 22,    // 时间边界开始（22点）
  timeBoundaryEnd: 7,       // 时间边界结束（7点）
  energyBoundaryThreshold: 0.3, // 精力边界阈值
  privacySensitivity: 0.7,  // 隐私敏感度
  decisionAutonomyWeight: 0.8, // 决策自主权重
  
  // 干预参数
  maxDailyInterventions: 3,
  minInterventionIntervalHours: 2,
  interventionCooldownHours: 24,
  enableAutomaticInterventions: true,
  
  // 价值权重
  declaredValueWeight: 0.6,
  observedBehaviorWeight: 0.4,
  recentFactorWeight: 0.7,
  historicalFactorWeight: 0.3,
  
  // 信号参数
  publishDriftSignals: true,
  publishBoundarySignals: true,
  publishInterventionSignals: true,
  publishValueAlignmentSignals: true,
  
  // 调试
  debugMode: false,
  logDetailedAnalysis: false,
  saveRawAssessments: true
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
 * @param {string} key 配置键（支持点表示法，如'driftThresholds.L1'）
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
 * 获取当前时间边界状态
 * @returns {object} 时间边界状态
 */
export function getTimeBoundaryStatus() {
  const config = loadConfig();
  const now = new Date();
  const hour = now.getHours();
  
  const timeStart = config.timeBoundaryStart;
  const timeEnd = config.timeBoundaryEnd;
  
  let isInBoundary = false;
  
  if (timeStart <= timeEnd) {
    // 正常时间段
    isInBoundary = hour >= timeStart && hour < timeEnd;
  } else {
    // 跨夜时段
    isInBoundary = hour >= timeStart || hour < timeEnd;
  }
  
  return {
    inBoundary: isInBoundary,
    currentHour: hour,
    boundaryStart: timeStart,
    boundaryEnd: timeEnd,
    pressure: isInBoundary ? 0.8 : 0.0
  };
}

/**
 * 获取干预级别阈值
 * @returns {object} 各级别阈值
 */
export function getInterventionThresholds() {
  const config = loadConfig();
  return {
    L1: config.driftThresholdL1,
    L2: config.driftThresholdL2,
    L3: config.driftThresholdL3,
    L4: config.driftThresholdL4
  };
}

/**
 * 验证配置有效性
 * @returns {Array} 问题列表
 */
export function validateConfig() {
  const config = loadConfig();
  const issues = [];
  
  // 验证阈值顺序
  if (!(config.driftThresholdL1 <= config.driftThresholdL2 && 
        config.driftThresholdL2 <= config.driftThresholdL3 && 
        config.driftThresholdL3 <= config.driftThresholdL4)) {
    issues.push('漂移阈值必须满足: L1 ≤ L2 ≤ L3 ≤ L4');
  }
  
  // 验证阈值范围
  const thresholds = [config.driftThresholdL1, config.driftThresholdL2, 
                      config.driftThresholdL3, config.driftThresholdL4];
  for (let i = 0; i < thresholds.length; i++) {
    if (thresholds[i] < 0 || thresholds[i] > 1) {
      issues.push(`漂移阈值L${i+1}应在0-1之间，当前: ${thresholds[i]}`);
    }
  }
  
  // 验证时间边界
  if (config.timeBoundaryStart < 0 || config.timeBoundaryStart >= 24) {
    issues.push(`时间边界开始时间应在0-23之间，当前: ${config.timeBoundaryStart}`);
  }
  
  if (config.timeBoundaryEnd < 0 || config.timeBoundaryEnd > 24) {
    issues.push(`时间边界结束时间应在0-24之间，当前: ${config.timeBoundaryEnd}`);
  }
  
  // 验证能量阈值
  if (config.energyBoundaryThreshold < 0 || config.energyBoundaryThreshold > 1) {
    issues.push(`能量边界阈值应在0-1之间，当前: ${config.energyBoundaryThreshold}`);
  }
  
  // 验证权重总和
  const valueWeightSum = config.declaredValueWeight + config.observedBehaviorWeight;
  if (Math.abs(valueWeightSum - 1.0) > 0.01) {
    issues.push(`价值权重总和应为1.0，当前: ${valueWeightSum.toFixed(2)}`);
  }
  
  const timeWeightSum = config.recentFactorWeight + config.historicalFactorWeight;
  if (Math.abs(timeWeightSum - 1.0) > 0.01) {
    issues.push(`时间权重总和应为1.0，当前: ${timeWeightSum.toFixed(2)}`);
  }
  
  // 验证干预限制
  if (config.maxDailyInterventions < 0 || config.maxDailyInterventions > 10) {
    issues.push(`每日最大干预次数应在0-10之间，当前: ${config.maxDailyInterventions}`);
  }
  
  if (config.minInterventionIntervalHours < 0 || config.minInterventionIntervalHours > 24) {
    issues.push(`最小干预间隔应在0-24小时之间，当前: ${config.minInterventionIntervalHours}`);
  }
  
  return issues;
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
 * 获取配置摘要
 */
export function getConfigSummary() {
  const config = loadConfig();
  const issues = validateConfig();
  
  return {
    thresholds: {
      L1: config.driftThresholdL1,
      L2: config.driftThresholdL2,
      L3: config.driftThresholdL3,
      L4: config.driftThresholdL4
    },
    boundaries: {
      time: `${config.timeBoundaryStart}:00-${config.timeBoundaryEnd}:00`,
      energy: config.energyBoundaryThreshold,
      privacy: config.privacySensitivity
    },
    interventions: {
      maxDaily: config.maxDailyInterventions,
      minInterval: config.minInterventionIntervalHours,
      cooldown: config.interventionCooldownHours,
      enabled: config.enableAutomaticInterventions
    },
    signals: {
      drift: config.publishDriftSignals,
      boundary: config.publishBoundarySignals,
      intervention: config.publishInterventionSignals
    },
    issues: issues.length > 0 ? issues : ['无']
  };
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
  getTimeBoundaryStatus,
  getInterventionThresholds,
  validateConfig,
  resetToDefaults,
  showConfig,
  getConfigSummary,
  DEFAULT_CONFIG
};
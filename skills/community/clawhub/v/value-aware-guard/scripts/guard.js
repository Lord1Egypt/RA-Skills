#!/usr/bin/env node

/**
 * Value-Aware Guard 主执行脚本
 * 
 * 执行模式：
 * 1. --test                : 测试价值守护功能
 * 2. --check-boundaries    : 检查边界状态
 * 3. --assess-drift        : 评估价值漂移
 * 4. --update-values       : 更新价值定义
 * 5. 无参数               : 执行完整守护流程
 */

import { parseArgs } from 'node:util';
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { format, differenceInHours, parseISO } from 'date-fns';

// 配置路径
const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = join(WORKSPACE, '.soul');
const GUARD_STATE_PATH = join(SOUL_DIR, 'guard-state.json');
const VALUES_PATH = join(SOUL_DIR, 'user-values.json');
const INTERVENTIONS_PATH = join(SOUL_DIR, 'interventions.jsonl');

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
  
  // 干预参数
  maxDailyInterventions: 3,
  minInterventionIntervalHours: 2,
  interventionCooldownHours: 24,
  
  // 价值权重
  declaredValueWeight: 0.6,
  observedBehaviorWeight: 0.4,
  recentFactorWeight: 0.7,
  
  // 信号参数
  publishDriftSignals: true,
  publishBoundarySignals: true,
  publishInterventionSignals: true,
  
  // 调试
  debugMode: false,
  logDetailedAnalysis: false
};

// 干预级别定义
const INTERVENTION_LEVELS = [
  { level: 1, name: '观察记录', action: 'record_only', maxPerDay: 10 },
  { level: 2, name: '温和提醒', action: 'gentle_reminder', maxPerDay: 5 },
  { level: 3, name: '严肃对话', action: 'serious_conversation', maxPerDay: 2 },
  { level: 4, name: '强制干预', action: 'mandatory_intervention', maxPerDay: 1 }
];

// 边界类型定义
const BOUNDARY_TYPES = [
  { id: 'time', name: '时间边界', priority: 'high' },
  { id: 'energy', name: '精力边界', priority: 'medium' },
  { id: 'privacy', name: '隐私边界', priority: 'high' },
  { id: 'decision', name: '决策边界', priority: 'medium' }
];

// 确保目录存在
function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// 加载配置
function loadConfig() {
  const configPath = join(SOUL_DIR, 'guard-config.json');
  
  if (!existsSync(configPath)) {
    saveConfig(DEFAULT_CONFIG);
    return { ...DEFAULT_CONFIG };
  }
  
  try {
    const userConfig = JSON.parse(readFileSync(configPath, 'utf-8'));
    return { ...DEFAULT_CONFIG, ...userConfig };
  } catch (error) {
    console.error('加载配置失败，使用默认配置:', error.message);
    return { ...DEFAULT_CONFIG };
  }
}

// 保存配置
function saveConfig(config) {
  ensureDir(SOUL_DIR);
  const configPath = join(SOUL_DIR, 'guard-config.json');
  writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
}

// 加载守护状态
function loadState() {
  if (!existsSync(GUARD_STATE_PATH)) {
    const initialState = {
      lastCheckTime: null,
      interventionsToday: 0,
      totalInterventions: 0,
      lastInterventionTime: null,
      boundaryViolations: {},
      valueDriftHistory: [],
      config: loadConfig()
    };
    saveState(initialState);
    return initialState;
  }
  
  try {
    const state = JSON.parse(readFileSync(GUARD_STATE_PATH, 'utf-8'));
    state.config = loadConfig();
    return state;
  } catch (error) {
    console.error('加载状态文件失败:', error.message);
    return {
      lastCheckTime: null,
      interventionsToday: 0,
      totalInterventions: 0,
      lastInterventionTime: null,
      boundaryViolations: {},
      valueDriftHistory: [],
      config: loadConfig()
    };
  }
}

// 保存状态
function saveState(state) {
  ensureDir(SOUL_DIR);
  state.lastUpdated = new Date().toISOString();
  writeFileSync(GUARD_STATE_PATH, JSON.stringify(state, null, 2), 'utf-8');
}

// 加载用户价值定义
function loadUserValues() {
  if (!existsSync(VALUES_PATH)) {
    // 尝试从用户画像中获取
    const profilePath = join(SOUL_DIR, 'user-profile.json');
    let initialValues = {
      core_values: [],
      work_principles: [],
      life_priorities: [],
      boundaries: {
        time: { start: 22, end: 7, enabled: true },
        energy: { threshold: 0.3, enabled: true },
        privacy: { topics: [], enabled: true },
        decision: { autonomy_level: 'high', enabled: true }
      },
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    if (existsSync(profilePath)) {
      try {
        const profile = JSON.parse(readFileSync(profilePath, 'utf-8'));
        if (profile.profile?.values?.core_values) {
          initialValues.core_values = profile.profile.values.core_values;
        }
        if (profile.profile?.values?.work_principles) {
          initialValues.work_principles = profile.profile.values.work_principles;
        }
      } catch (error) {
        console.error('从用户画像加载价值失败:', error.message);
      }
    }
    
    saveUserValues(initialValues);
    return initialValues;
  }
  
  try {
    return JSON.parse(readFileSync(VALUES_PATH, 'utf-8'));
  } catch (error) {
    console.error('加载用户价值失败:', error.message);
    return {
      core_values: [],
      work_principles: [],
      life_priorities: [],
      boundaries: {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
  }
}

// 保存用户价值
function saveUserValues(values) {
  ensureDir(SOUL_DIR);
  values.updated_at = new Date().toISOString();
  writeFileSync(VALUES_PATH, JSON.stringify(values, null, 2), 'utf-8');
}

// 记录干预
function recordIntervention(intervention) {
  ensureDir(SOUL_DIR);
  
  const interventionRecord = {
    ...intervention,
    id: `int_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    timestamp: new Date().toISOString()
  };
  
  try {
    const line = JSON.stringify(interventionRecord);
    appendFileSync(INTERVENTIONS_PATH, line + '\n', 'utf-8');
    return interventionRecord.id;
  } catch (error) {
    console.error('记录干预失败:', error.message);
    return null;
  }
}

// 检查边界状态
function checkBoundaries(config, currentContext = {}) {
  const now = new Date();
  const hour = now.getHours();
  const boundaries = {
    time: { status: 'safe', pressure: 0, message: '' },
    energy: { status: 'safe', pressure: 0, message: '' },
    privacy: { status: 'safe', pressure: 0, message: '' },
    decision: { status: 'safe', pressure: 0, message: '' }
  };
  
  // 时间边界检查
  const timeStart = config.timeBoundaryStart;
  const timeEnd = config.timeBoundaryEnd;
  
  if (timeStart <= timeEnd) {
    // 正常时间段
    if (hour >= timeStart && hour < timeEnd) {
      boundaries.time.status = 'violated';
      boundaries.time.pressure = 0.8;
      boundaries.time.message = `当前时间 ${hour}:00 在静默时段内 (${timeStart}:00-${timeEnd}:00)`;
    }
  } else {
    // 跨夜时段
    if (hour >= timeStart || hour < timeEnd) {
      boundaries.time.status = 'violated';
      boundaries.time.pressure = 0.8;
      boundaries.time.message = `当前时间 ${hour}:00 在静默时段内 (${timeStart}:00-${timeEnd}:00)`;
    }
  }
  
  // 精力边界检查（从情绪状态获取）
  if (currentContext.energy !== undefined) {
    if (currentContext.energy < config.energyBoundaryThreshold) {
      boundaries.energy.status = 'warning';
      boundaries.energy.pressure = 1.0 - currentContext.energy;
      boundaries.energy.message = `精力水平较低 (${currentContext.energy.toFixed(2)})，建议简化交互`;
    }
  }
  
  // 隐私边界检查（简单实现）
  if (currentContext.sensitiveTopic) {
    boundaries.privacy.status = 'warning';
    boundaries.privacy.pressure = 0.6;
    boundaries.privacy.message = '检测到敏感话题讨论';
  }
  
  // 决策边界检查
  if (currentContext.decisiveTone) {
    boundaries.decision.status = 'warning';
    boundaries.decision.pressure = 0.4;
    boundaries.decision.message = '检测到决策倾向性表达';
  }
  
  // 计算总体边界压力
  const totalPressure = Object.values(boundaries)
    .reduce((sum, b) => sum + b.pressure, 0);
  const avgPressure = totalPressure / Object.keys(boundaries).length;
  
  return {
    boundaries,
    summary: {
      totalPressure,
      avgPressure,
      violated: Object.values(boundaries).filter(b => b.status === 'violated').length,
      warnings: Object.values(boundaries).filter(b => b.status === 'warning').length,
      safe: Object.values(boundaries).filter(b => b.status === 'safe').length
    }
  };
}

// 评估价值漂移
function assessValueDrift(userValues, observedBehavior, config) {
  if (!userValues.core_values || userValues.core_values.length === 0) {
    return {
      driftScore: 0,
      confidence: 0,
      details: [],
      overall: 'insufficient_data'
    };
  }
  
  const driftDetails = [];
  let totalScore = 0;
  let totalWeight = 0;
  
  // 检查每个核心价值
  for (const value of userValues.core_values) {
    let evidenceCount = 0;
    let alignmentSum = 0;
    
    // 简单匹配逻辑（实际需要更复杂的NLP分析）
    const valueKeywords = extractKeywords(value.value || value);
    const behaviorText = JSON.stringify(observedBehavior).toLowerCase();
    
    for (const keyword of valueKeywords) {
      if (behaviorText.includes(keyword)) {
        evidenceCount++;
        alignmentSum += 0.7; // 基础对齐分数
      }
    }
    
    const alignmentScore = evidenceCount > 0 ? alignmentSum / evidenceCount : 0;
    const driftScore = 1.0 - alignmentScore;
    
    driftDetails.push({
      value: value.value || value,
      alignmentScore,
      driftScore,
      evidenceCount,
      confidence: Math.min(1.0, evidenceCount / 5)
    });
    
    const weight = value.weight || 1.0;
    totalScore += driftScore * weight;
    totalWeight += weight;
  }
  
  const overallDrift = totalWeight > 0 ? totalScore / totalWeight : 0;
  
  // 确定漂移级别
  let driftLevel = 'none';
  if (overallDrift >= config.driftThresholdL4) driftLevel = 'severe';
  else if (overallDrift >= config.driftThresholdL3) driftLevel = 'high';
  else if (overallDrift >= config.driftThresholdL2) driftLevel = 'moderate';
  else if (overallDrift >= config.driftThresholdL1) driftLevel = 'low';
  
  return {
    driftScore: overallDrift,
    confidence: Math.min(1.0, driftDetails.length / 3),
    details: driftDetails,
    overall: driftLevel,
    assessment: getDriftAssessment(overallDrift, driftLevel)
  };
}

// 提取关键词（简化实现）
function extractKeywords(text) {
  if (!text) return [];
  
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 1);
  
  // 过滤常见停用词（简化版）
  const stopWords = ['the', 'and', 'for', 'with', 'that', 'this', 'have', 'from'];
  return words.filter(word => !stopWords.includes(word));
}

// 获取漂移评估描述
function getDriftAssessment(score, level) {
  const assessments = {
    insufficient_data: { message: '数据不足，无法评估价值漂移', recommendation: '需要更多用户价值定义和行为数据' },
    none: { message: '价值一致性良好', recommendation: '继续保持当前行为模式' },
    low: { message: '轻微价值漂移', recommendation: '偶尔回顾核心价值' },
    moderate: { message: '中度价值偏离', recommendation: '建议进行价值反思' },
    high: { message: '显著价值偏离', recommendation: '需要严肃价值对话' },
    severe: { message: '严重价值冲突', recommendation: '立即进行价值干预' }
  };
  
  return assessments[level] || assessments.insufficient_data;
}

// 确定干预级别
function determineInterventionLevel(driftScore, boundarySummary, state, config) {
  // 边界违规优先于价值漂移
  if (boundarySummary.violated > 0) {
    return INTERVENTION_LEVELS[3]; // L4强制干预
  }
  
  if (boundarySummary.warnings > 1) {
    return INTERVENTION_LEVELS[2]; // L3严肃对话
  }
  
  // 基于价值漂移确定级别
  if (driftScore >= config.driftThresholdL4) {
    return INTERVENTION_LEVELS[3]; // L4
  } else if (driftScore >= config.driftThresholdL3) {
    return INTERVENTION_LEVELS[2]; // L3
  } else if (driftScore >= config.driftThresholdL2) {
    return INTERVENTION_LEVELS[1]; // L2
  } else if (driftScore >= config.driftThresholdL1) {
    return INTERVENTION_LEVELS[0]; // L1
  }
  
  return null; // 不需要干预
}

// 生成干预消息
function generateInterventionMessage(level, driftAssessment, boundaryIssues) {
  const baseMessages = {
    record_only: '记录到轻微价值偏离，保持观察。',
    gentle_reminder: '注意到一些行为可能与您的核心价值不太一致，想聊聊吗？',
    serious_conversation: '检测到显著的价值偏离，建议我们深入探讨一下。',
    mandatory_intervention: '检测到边界违规或严重价值冲突，需要立即关注。'
  };
  
  let message = baseMessages[level.action] || '检测到潜在问题，建议关注。';
  
  // 添加具体细节
  const details = [];
  
  if (driftAssessment) {
    details.push(driftAssessment.message);
  }
  
  if (boundaryIssues && boundaryIssues.length > 0) {
    details.push(...boundaryIssues.map(b => b.message));
  }
  
  if (details.length > 0) {
    message += ` 具体来说：${details.join('；')}`;
  }
  
  // 确保是开放式问题
  if (!message.includes('？') && !message.includes('?')) {
    message += ' 您觉得呢？';
  }
  
  return message;
}

// 发布信号
async function publishSignal(type, payload, priority = 'medium') {
  // 使用文件系统信号管理器（复用proactive-trigger的）
  try {
    const signalManager = await import('./utils/signal-manager.js');
    return signalManager.publishSignal('value-aware-guard', type, payload, priority);
  } catch (error) {
    console.log(`[信号模拟] ${type}:`, payload);
    return `simulated_${Date.now()}`;
  }
}

// 执行完整守护流程
async function runFullGuard(context = {}) {
  console.log('=== 价值守护检查开始 ===\n');
  
  const config = loadConfig();
  const state = loadState();
  const userValues = loadUserValues();
  
  // 1. 检查边界状态
  console.log('1. 检查边界状态...');
  const boundaryCheck = checkBoundaries(config, context);
  console.log(`   边界状态: ${boundaryCheck.summary.safe}安全, ${boundaryCheck.summary.warnings}警告, ${boundaryCheck.summary.violated}违规`);
  console.log(`   总体压力: ${boundaryCheck.summary.avgPressure.toFixed(2)}`);
  
  // 2. 评估价值漂移
  console.log('\n2. 评估价值漂移...');
  const driftAssessment = assessValueDrift(userValues, context, config);
  console.log(`   价值漂移分数: ${driftAssessment.driftScore.toFixed(2)}`);
  console.log(`   漂移级别: ${driftAssessment.overall}`);
  console.log(`   评估置信度: ${driftAssessment.confidence.toFixed(2)}`);
  
  // 3. 确定干预级别
  console.log('\n3. 确定干预级别...');
  const interventionLevel = determineInterventionLevel(
    driftAssessment.driftScore,
    boundaryCheck.summary,
    state,
    config
  );
  
  if (interventionLevel) {
    console.log(`   建议干预级别: L${interventionLevel.level} - ${interventionLevel.name}`);
    console.log(`   干预动作: ${interventionLevel.action}`);
  } else {
    console.log('   无需干预，状态良好');
  }
  
  // 4. 安全检查
  console.log('\n4. 执行安全检查...');
  let canIntervene = true;
  let safetyReason = '';
  
  // 检查干预限制
  if (state.interventionsToday >= config.maxDailyInterventions) {
    canIntervene = false;
    safetyReason = `今日干预次数已达上限 (${config.maxDailyInterventions})`;
  }
  
  // 检查冷却时间
  if (state.lastInterventionTime) {
    const lastTime = parseISO(state.lastInterventionTime);
    const hoursSinceLast = differenceInHours(new Date(), lastTime);
    if (hoursSinceLast < config.minInterventionIntervalHours) {
      canIntervene = false;
      safetyReason = `距上次干预仅${hoursSinceLast.toFixed(1)}小时，需要冷却`;
    }
  }
  
  // 检查边界违规（强制干预例外）
  if (boundaryCheck.summary.violated > 0 && interventionLevel?.level < 4) {
    canIntervene = false;
    safetyReason = '存在边界违规，仅允许L4强制干预';
  }
  
  console.log(`   允许干预: ${canIntervene ? '是' : '否'}`);
  if (!canIntervene) {
    console.log(`   原因: ${safetyReason}`);
  }
  
  // 5. 生成干预消息
  let intervention = null;
  if (canIntervene && interventionLevel) {
    console.log('\n5. 生成干预消息...');
    
    // 收集边界问题
    const boundaryIssues = Object.entries(boundaryCheck.boundaries)
      .filter(([_, b]) => b.status !== 'safe')
      .map(([type, b]) => ({ type, ...b }));
    
    const message = generateInterventionMessage(
      interventionLevel,
      driftAssessment.assessment,
      boundaryIssues
    );
    
    console.log(`   干预消息: ${message}`);
    
    intervention = {
      level: interventionLevel.level,
      name: interventionLevel.name,
      action: interventionLevel.action,
      message,
      driftScore: driftAssessment.driftScore,
      boundaryIssues: boundaryIssues.length,
      timestamp: new Date().toISOString()
    };
    
    // 记录干预
    const interventionId = recordIntervention(intervention);
    if (interventionId) {
      console.log(`   干预已记录: ${interventionId}`);
    }
    
    // 更新状态
    state.interventionsToday += 1;
    state.totalInterventions += 1;
    state.lastInterventionTime = new Date().toISOString();
  }
  
  // 6. 发布信号
  console.log('\n6. 发布信号...');
  if (config.publishBoundarySignals && boundaryCheck.summary.violated > 0) {
    await publishSignal('boundary_violation', {
      violations: boundaryCheck.summary.violated,
      warnings: boundaryCheck.summary.warnings,
      pressure: boundaryCheck.summary.avgPressure
    }, 'medium');
  }
  
  if (config.publishDriftSignals && driftAssessment.driftScore > config.driftThresholdL1) {
    await publishSignal('value_drift_detected', {
      score: driftAssessment.driftScore,
      level: driftAssessment.overall,
      confidence: driftAssessment.confidence
    }, driftAssessment.driftScore > config.driftThresholdL3 ? 'high' : 'low');
  }
  
  if (config.publishInterventionSignals && intervention) {
    await publishSignal('intervention_triggered', {
      level: intervention.level,
      name: intervention.name,
      reason: intervention.boundaryIssues > 0 ? 'boundary' : 'value_drift'
    }, intervention.level >= 3 ? 'high' : 'medium');
  }
  
  // 7. 更新状态
  console.log('\n7. 更新状态...');
  state.lastCheckTime = new Date().toISOString();
  
  // 记录价值漂移历史
  state.valueDriftHistory.push({
    timestamp: new Date().toISOString(),
    score: driftAssessment.driftScore,
    level: driftAssessment.overall,
    confidence: driftAssessment.confidence
  });
  
  // 保持历史记录大小
  if (state.valueDriftHistory.length > 100) {
    state.valueDriftHistory = state.valueDriftHistory.slice(-100);
  }
  
  // 更新边界违规统计
  for (const [type, boundary] of Object.entries(boundaryCheck.boundaries)) {
    if (boundary.status !== 'safe') {
      if (!state.boundaryViolations[type]) {
        state.boundaryViolations[type] = 0;
      }
      state.boundaryViolations[type] += 1;
    }
  }
  
  saveState(state);
  
  console.log('\n=== 守护检查完成 ===');
  
  return {
    boundaries: boundaryCheck,
    drift: driftAssessment,
    intervention,
    safety: { canIntervene, reason: safetyReason },
    state: {
      interventionsToday: state.interventionsToday,
      totalInterventions: state.totalInterventions,
      lastInterventionTime: state.lastInterventionTime
    }
  };
}

// 主函数
async function main() {
  const args = parseArgs({
    options: {
      test: { type: 'boolean', short: 't' },
      'check-boundaries': { type: 'boolean' },
      'assess-drift': { type: 'boolean' },
      'update-values': { type: 'boolean' },
      help: { type: 'boolean', short: 'h' }
    },
    allowPositionals: true
  });
  
  const { values, positionals } = args;
  
  if (values.help) {
    console.log(`
Value-Aware Guard 脚本
用法:
  node guard.js [选项]

选项:
  -t, --test               测试价值守护功能
  --check-boundaries       检查边界状态
  --assess-drift           评估价值漂移
  --update-values          更新价值定义
  -h, --help               显示此帮助信息

示例:
  node guard.js --test
  node guard.js --check-boundaries
  node guard.js --assess-drift
  node guard.js --update-values
    `);
    return;
  }
  
  if (values.test) {
    console.log('测试价值守护功能...\n');
    await runFullGuard({ test: true });
    
  } else if (values['check-boundaries']) {
    const config = loadConfig();
    const boundaryCheck = checkBoundaries(config, {});
    
    console.log('边界状态检查:');
    console.log(`总体压力: ${boundaryCheck.summary.avgPressure.toFixed(2)}`);
    console.log(`安全边界: ${boundaryCheck.summary.safe}`);
    console.log(`警告边界: ${boundaryCheck.summary.warnings}`);
    console.log(`违规边界: ${boundaryCheck.summary.violated}`);
    
    for (const [type, boundary] of Object.entries(boundaryCheck.boundaries)) {
      if (boundary.status !== 'safe') {
        console.log(`\n${type}: ${boundary.status} (压力: ${boundary.pressure.toFixed(2)})`);
        console.log(`原因: ${boundary.message}`);
      }
    }
    
  } else if (values['assess-drift']) {
    const userValues = loadUserValues();
    const driftAssessment = assessValueDrift(userValues, {}, loadConfig());
    
    console.log('价值漂移评估:');
    console.log(`总体分数: ${driftAssessment.driftScore.toFixed(2)}`);
    console.log(`漂移级别: ${driftAssessment.overall}`);
    console.log(`置信度: ${driftAssessment.confidence.toFixed(2)}`);
    console.log(`评估: ${driftAssessment.assessment.message}`);
    console.log(`建议: ${driftAssessment.assessment.recommendation}`);
    
    if (driftAssessment.details.length > 0) {
      console.log('\n详细分析:');
      for (const detail of driftAssessment.details) {
        console.log(`- ${detail.value}: 对齐${detail.alignmentScore.toFixed(2)}, 漂移${detail.driftScore.toFixed(2)} (置信度: ${detail.confidence.toFixed(2)})`);
      }
    }
    
  } else if (values['update-values']) {
    console.log('更新价值定义功能（待实现）');
    console.log('当前从用户画像同步价值定义');
    
    const userValues = loadUserValues();
    console.log(`当前核心价值: ${userValues.core_values.length}个`);
    console.log(`工作原则: ${userValues.work_principles.length}个`);
    console.log(`生活优先级: ${userValues.life_priorities.length}个`);
    
  } else {
    // 默认执行测试评估
    console.log('执行默认测试评估...\n');
    await runFullGuard();
  }
}

// 执行主函数
main().catch(error => {
  console.error('脚本执行失败:', error);
  process.exit(1);
});
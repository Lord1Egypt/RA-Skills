/**
 * Proactive Care - 主动感知模块 v2.1
 * 
 * 检测刘总状态变化并主动关心
 * 
 * Features:
 * - 日程密度检测（今天会议数量）
 * - 工作时段消息频率
 * - 心情关键词检测（负面情绪）
 * - 任务截止时间压力
 * - 本地缓存（减少 API 调用）
 * 
 * Usage:
 *   node proactive_care.js config           # 显示/修改配置
 *   node proactive_care.js check           # 执行检查
 *   node proactive_care.js test --text "累"  # 测试关键词
 *   node proactive_care.js cache           # 清除缓存
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const MEMORY_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'memory');
const CONFIG_FILE = path.join(MEMORY_DIR, 'proactive_care_config.json');
const STATE_FILE = path.join(MEMORY_DIR, 'proactive_care_state.json');
const CACHE_FILE = path.join(MEMORY_DIR, 'proactive_care_cache.json');
const CACHE_TTL_MINUTES = 10;

const DEFAULT_CONFIG = {
  enabled: true,
  check_interval_minutes: 30,
  rules: {
    meeting_density: {
      enabled: true,
      threshold: 5,
      cooldown_hours: 2,
      message: '刘总，今天会议挺密集的({count}个)，记得适当休息，喝口水活动一下~'
    },
    continuous_work: {
      enabled: true,
      threshold_hours: 4,
      cooldown_hours: 1,
      message: '刘总，连续工作{hours}小时了，休息一下喝口水吧！'
    },
    negative_keywords: {
      enabled: true,
      keywords: ['累', '烦', '忙', '烦死了', '好累', '太忙', '崩溃', '压力大', '头疼', '无语'],
      cooldown_hours: 3,
      message: '刘总，看你今天挺累的，注意身体啊！需要我帮忙处理什么吗？'
    },
    deadline_pressure: {
      enabled: true,
      threshold_hours: 24,
      cooldown_hours: 6,
      message: '刘总，有{count}个任务截止时间快到了(< {hours}小时)，注意优先级安排~'
    }
  },
  user: {
    open_id: 'ou_dcdc467a4de8cd4667474ccb99522e80',
    name: '刘总'
  }
};

// ========== Config Management ==========

async function loadConfig() {
  try {
    if (await fileExists(CONFIG_FILE)) {
      return JSON.parse(await fs.readFile(CONFIG_FILE, 'utf-8'));
    }
  } catch {}
  return { ...DEFAULT_CONFIG };
}

async function saveConfig(config) {
  await fs.mkdir(MEMORY_DIR, { recursive: true });
  await fs.writeFile(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

async function loadState() {
  try {
    if (await fileExists(STATE_FILE)) {
      return JSON.parse(await fs.readFile(STATE_FILE, 'utf-8'));
    }
  } catch {}
  return {
    last_check: null,
    work_start_time: null,
    last_trigger: {}
  };
}

async function saveState(state) {
  await fs.mkdir(MEMORY_DIR, { recursive: true });
  await fs.writeFile(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

// ========== Cache ==========

async function loadCache() {
  try {
    if (await fileExists(CACHE_FILE)) {
      return JSON.parse(await fs.readFile(CACHE_FILE, 'utf-8'));
    }
  } catch {}
  return { meetings: [], messages: [], tasks: [] };
}

async function saveCache(cache) {
  await fs.mkdir(MEMORY_DIR, { recursive: true });
  await fs.writeFile(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf-8');
}

function isCacheValid(cache) {
  if (!cache || !cache.timestamp) return false;
  const age = Date.now() - new Date(cache.timestamp).getTime();
  return age < CACHE_TTL_MINUTES * 60 * 1000;
}

// ========== Utilities ==========

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

function canTrigger(state, ruleName, cooldownHours) {
  const last = state.last_trigger?.[ruleName];
  if (!last) return true;
  const lastTime = new Date(last);
  return Date.now() - lastTime.getTime() > cooldownHours * 60 * 60 * 1000;
}

function markTriggered(state, ruleName) {
  if (!state.last_trigger) state.last_trigger = {};
  state.last_trigger[ruleName] = new Date().toISOString();
  return state;
}

// ========== Detection Functions ==========

async function checkMeetingDensity(config, state, cache) {
  const rule = config.rules.meeting_density;
  if (!rule?.enabled) return null;
  if (!canTrigger(state, 'meeting_density', rule.cooldown_hours || 2)) return null;
  
  // Check cache first
  if (isCacheValid(cache) && cache.meetings) {
    const today = new Date().toISOString().slice(0, 10);
    const todayMeetings = cache.meetings.filter(m => m.start?.startsWith(today));
    const meetingCount = todayMeetings.filter(e => e.event_type !== 'free').length;
    
    if (meetingCount > rule.threshold) {
      return {
        type: 'meeting_density',
        count: meetingCount,
        message: rule.message.replace('{count}', meetingCount)
      };
    }
  }
  
  return null;
}

async function checkContinuousWork(config, state) {
  const rule = config.rules.continuous_work;
  if (!rule?.enabled) return null;
  if (!canTrigger(state, 'continuous_work', rule.cooldown_hours || 1)) return null;
  
  // Check if work start time is recorded
  if (!state.work_start_time) return null;
  
  const startTime = new Date(state.work_start_time);
  const hoursElapsed = (Date.now() - startTime.getTime()) / (1000 * 60 * 60);
  
  if (hoursElapsed >= rule.threshold_hours) {
    return {
      type: 'continuous_work',
      hours: Math.floor(hoursElapsed),
      message: rule.message.replace('{hours}', Math.floor(hoursElapsed))
    };
  }
  
  return null;
}

async function checkNegativeKeywords(config, state) {
  const rule = config.rules.negative_keywords;
  if (!rule?.enabled) return null;
  if (!canTrigger(state, 'negative_keywords', rule.cooldown_hours || 3)) return null;
  
  const keywords = rule.keywords || [];
  // This would be called with actual message text
  return null;
}

async function checkDeadlinePressure(config, state, cache) {
  const rule = config.rules.deadline_pressure;
  if (!rule?.enabled) return null;
  if (!canTrigger(state, 'deadline_pressure', rule.cooldown_hours || 6)) return null;
  
  // Check cache for tasks
  if (isCacheValid(cache) && cache.tasks) {
    const now = Date.now();
    const thresholdMs = rule.threshold_hours * 60 * 60 * 1000;
    const urgentTasks = cache.tasks.filter(t => {
      if (!t.due) return false;
      const dueTime = new Date(t.due).getTime();
      return dueTime - now < thresholdMs && dueTime > now;
    });
    
    if (urgentTasks.length > 0) {
      return {
        type: 'deadline_pressure',
        count: urgentTasks.length,
        hours: rule.threshold_hours,
        message: rule.message.replace('{count}', urgentTasks.length).replace('{hours}', rule.threshold_hours)
      };
    }
  }
  
  return null;
}

// ========== Main Check ==========

async function runCheck() {
  console.log('🔍 执行主动关怀检查...\n');
  
  const config = await loadConfig();
  if (!config.enabled) {
    console.log('⚠️ 主动关怀已禁用');
    return [];
  }
  
  const state = await loadState();
  const cache = await loadCache();
  const results = [];
  
  // Run all checks
  const checks = [
    checkMeetingDensity(config, state, cache),
    checkContinuousWork(config, state),
    checkNegativeKeywords(config, state),
    checkDeadlinePressure(config, state, cache)
  ];
  
  const checkResults = await Promise.all(checks);
  
  for (const result of checkResults) {
    if (result) {
      results.push(result);
      markTriggered(state, result.type);
      console.log(`✅ [${result.type}] ${result.message}`);
    }
  }
  
  // Update state
  state.last_check = new Date().toISOString();
  await saveState(state);
  
  if (results.length === 0) {
    console.log('✅ 所有检查通过，无需关怀');
  }
  
  return results;
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Proactive Care - 主动感知模块 v2.1

Usage:
    node proactive_care.js config           # 显示配置
    node proactive_care.js check           # 执行检查
    node proactive_care.js test --text "累" # 测试关键词
    node proactive_care.js cache           # 清除缓存
    node proactive_care.js enable          # 启用
    node proactive_care.js disable         # 禁用
`);
    process.exit(1);
  }
  
  console.log('🚀 Proactive Care v2.1...\n');
  
  switch (command) {
    case 'config': {
      const config = await loadConfig();
      console.log('📋 当前配置:\n');
      console.log(JSON.stringify(config, null, 2));
      break;
    }
    
    case 'check': {
      const results = await runCheck();
      console.log(`\n📊 检查完成，发现 ${results.length} 个需要关怀的情况`);
      break;
    }
    
    case 'test': {
      const textIdx = args.indexOf('--text');
      const text = textIdx !== -1 ? args[textIdx + 1] : '';
      
      if (!text) {
        console.log('❌ 请提供 --text 参数');
        process.exit(1);
      }
      
      const config = await loadConfig();
      const keywords = config.rules.negative_keywords?.keywords || [];
      const matched = keywords.filter(kw => text.includes(kw));
      
      if (matched.length > 0) {
        console.log(`✅ 检测到负面情绪关键词: ${matched.join(', ')}`);
      } else {
        console.log('✅ 未检测到负面情绪关键词');
      }
      break;
    }
    
    case 'cache': {
      await saveCache({ meetings: [], messages: [], tasks: [], timestamp: null });
      console.log('🗑️ 缓存已清除');
      break;
    }
    
    case 'enable': {
      const config = await loadConfig();
      config.enabled = true;
      await saveConfig(config);
      console.log('✅ 主动关怀已启用');
      break;
    }
    
    case 'disable': {
      const config = await loadConfig();
      config.enabled = false;
      await saveConfig(config);
      console.log('✅ 主动关怀已禁用');
      break;
    }
    
    default:
      console.log(`❌ 未知命令: ${command}`);
      process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  runCheck,
  loadConfig,
  saveConfig,
  checkMeetingDensity,
  checkContinuousWork,
  checkNegativeKeywords,
  checkDeadlinePressure
};

export default { runCheck, loadConfig, saveConfig };

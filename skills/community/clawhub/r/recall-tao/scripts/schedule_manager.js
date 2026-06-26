/**
 * 调度管理器 - 定时开关与时间段控制
 * 支持：工作日/周末配置、多时段控制、动作策略
 * 
 * 版本：v1.0
 * 更新日期：2026-04-02
 */

const fs = require('fs');
const path = require('path');

// ==================== 配置加载 ====================

let scheduleConfig = null;
const CONFIG_PATH = path.join(__dirname, '../config/schedule_config.json');

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
      scheduleConfig = JSON.parse(content);
    }
  } catch (error) {
    console.error('加载调度配置失败:', error.message);
    scheduleConfig = getDefaultConfig();
  }
  return scheduleConfig;
}

function getDefaultConfig() {
  return {
    enabled: true,
    timezone: 'Asia/Shanghai',
    schedules: [],
    defaultAction: 'auto_reply'
  };
}

// ==================== 核心函数 ====================

/**
 * 获取当前时间段应执行的动作
 * @returns {{ action: string, schedule: object|null, reason: string }}
 */
function getCurrentAction() {
  if (!scheduleConfig) {
    loadConfig();
  }
  
  if (!scheduleConfig.enabled) {
    return {
      action: scheduleConfig.defaultAction || 'auto_reply',
      schedule: null,
      reason: '调度功能未启用，使用默认动作'
    };
  }
  
  const now = new Date();
  const currentDay = now.getDay(); // 0=周日, 1=周一...
  const currentTime = now.getHours() * 60 + now.getMinutes(); // 当前时间的分钟数
  
  // 查找匹配的调度规则
  for (const schedule of scheduleConfig.schedules) {
    if (!schedule.enabled) continue;
    
    // 检查日期是否匹配
    if (!schedule.days.includes(currentDay)) continue;
    
    // 检查时间段
    for (const slot of schedule.timeSlots) {
      const startTime = parseTime(slot.start);
      const endTime = parseTime(slot.end);
      
      if (currentTime >= startTime && currentTime < endTime) {
        return {
          action: slot.action,
          schedule: schedule,
          timeSlot: slot,
          reason: `命中调度规则: ${schedule.name} (${slot.start}-${slot.end})`
        };
      }
    }
  }
  
  // 未匹配任何规则，使用默认动作
  return {
    action: scheduleConfig.defaultAction || 'log_only',
    schedule: null,
    reason: '未匹配任何调度规则，使用默认动作'
  };
}

/**
 * 解析时间字符串为分钟数
 * @param {string} timeStr 格式 "HH:MM"
 * @returns {number} 从午夜开始的分钟数
 */
function parseTime(timeStr) {
  const [hours, minutes] = timeStr.split(':').map(Number);
  return hours * 60 + minutes;
}

/**
 * 检查是否可以执行自动回复
 * @returns {{ canReply: boolean, reason: string, action: string }}
 */
function canAutoReply() {
  const current = getCurrentAction();
  
  return {
    canReply: current.action === 'auto_reply',
    action: current.action,
    reason: current.reason,
    schedule: current.schedule
  };
}

/**
 * 获取下一个自动回复时段
 * @returns {{ startTime: Date, endTime: Date, schedule: object }|null}
 */
function getNextReplySlot() {
  if (!scheduleConfig) {
    loadConfig();
  }
  
  const now = new Date();
  const currentDay = now.getDay();
  const currentTime = now.getHours() * 60 + now.getMinutes();
  
  // 最多查找未来7天
  for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
    const checkDay = (currentDay + dayOffset) % 7;
    
    for (const schedule of scheduleConfig.schedules) {
      if (!schedule.enabled) continue;
      if (!schedule.days.includes(checkDay)) continue;
      
      for (const slot of schedule.timeSlots) {
        if (slot.action !== 'auto_reply') continue;
        
        const startTime = parseTime(slot.start);
        
        // 如果是今天，检查是否已过
        if (dayOffset === 0 && startTime <= currentTime) continue;
        
        // 计算具体时间
        const startHour = Math.floor(startTime / 60);
        const startMin = startTime % 60;
        
        const nextStart = new Date(now);
        nextStart.setDate(nextStart.getDate() + dayOffset);
        nextStart.setHours(startHour, startMin, 0, 0);
        
        const endTime = parseTime(slot.end);
        const endHour = Math.floor(endTime / 60);
        const endMin = endTime % 60;
        
        const nextEnd = new Date(nextStart);
        nextEnd.setHours(endHour, endMin, 0, 0);
        
        return {
          startTime: nextStart,
          endTime: nextEnd,
          scheduleName: schedule.name,
          timeSlot: slot
        };
      }
    }
  }
  
  return null; // 未来7天没有自动回复时段
}

/**
 * 获取调度状态摘要
 * @returns {object}
 */
function getScheduleStatus() {
  const current = getCurrentAction();
  const nextSlot = getNextReplySlot();
  
  return {
    enabled: scheduleConfig?.enabled || false,
    currentAction: current.action,
    currentReason: current.reason,
    currentSchedule: current.schedule?.name || null,
    nextReplySlot: nextSlot ? {
      start: nextSlot.startTime.toISOString(),
      end: nextSlot.endTime.toISOString(),
      scheduleName: nextSlot.scheduleName
    } : null,
    timezone: scheduleConfig?.timezone || 'Asia/Shanghai'
  };
}

// ==================== 配置更新 ====================

/**
 * 更新调度配置
 * @param {object} newConfig 新配置
 */
function updateConfig(newConfig) {
  scheduleConfig = {
    ...scheduleConfig,
    ...newConfig,
    lastUpdated: new Date().toISOString()
  };
  
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(scheduleConfig, null, 2), 'utf-8');
  return scheduleConfig;
}

/**
 * 添加调度规则
 * @param {object} schedule 调度规则
 */
function addSchedule(schedule) {
  if (!scheduleConfig) {
    loadConfig();
  }
  
  schedule.id = schedule.id || `schedule_${Date.now()}`;
  scheduleConfig.schedules.push(schedule);
  scheduleConfig.lastUpdated = new Date().toISOString();
  
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(scheduleConfig, null, 2), 'utf-8');
  return schedule;
}

/**
 * 更新调度规则
 * @param {string} scheduleId 规则ID
 * @param {object} updates 更新内容
 */
function updateSchedule(scheduleId, updates) {
  if (!scheduleConfig) {
    loadConfig();
  }
  
  const index = scheduleConfig.schedules.findIndex(s => s.id === scheduleId);
  if (index === -1) {
    throw new Error(`调度规则 ${scheduleId} 不存在`);
  }
  
  scheduleConfig.schedules[index] = {
    ...scheduleConfig.schedules[index],
    ...updates
  };
  scheduleConfig.lastUpdated = new Date().toISOString();
  
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(scheduleConfig, null, 2), 'utf-8');
  return scheduleConfig.schedules[index];
}

// ==================== 导出 ====================

module.exports = {
  // 核心函数
  getCurrentAction,
  canAutoReply,
  getNextReplySlot,
  getScheduleStatus,
  
  // 配置管理
  loadConfig,
  updateConfig,
  addSchedule,
  updateSchedule,
  
  // 工具函数
  parseTime
};

// 初始化加载配置
loadConfig();

#!/usr/bin/env node

/**
 * Time Analyzer - CLI for time tracking and analysis
 * Usage: time-analyzer <command> [options]
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Data storage path
const DATA_DIR = path.join(os.homedir(), '.time-analyzer');
const DATA_FILE = path.join(DATA_DIR, 'records.json');
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

// Activity categories
const CATEGORIES = {
  work: { name: '工作', color: '\x1b[34m', icon: '💼' },
  study: { name: '学习', color: '\x1b[32m', icon: '📚' },
  meeting: { name: '会议', color: '\x1b[33m', icon: '👥' },
  break: { name: '休息', color: '\x1b[36m', icon: '☕' },
  exercise: { name: '运动', color: '\x1b[35m', icon: '🏃' },
  entertainment: { name: '娱乐', color: '\x1b[31m', icon: '🎮' },
  sleep: { name: '睡眠', color: '\x1b[90m', icon: '😴' },
  other: { name: '其他', color: '\x1b[37m', icon: '📌' }
};

// Ensure data directory exists
function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

// Load records
function loadRecords() {
  ensureDataDir();
  if (!fs.existsSync(DATA_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (e) {
    return [];
  }
}

// Save records
function saveRecords(records) {
  ensureDataDir();
  fs.writeFileSync(DATA_FILE, JSON.stringify(records, null, 2));
}

// Load config
function loadConfig() {
  ensureDataDir();
  if (!fs.existsSync(CONFIG_FILE)) {
    return { autoTrack: false, currentSession: null };
  }
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  } catch (e) {
    return { autoTrack: false, currentSession: null };
  }
}

// Save config
function saveConfig(config) {
  ensureDataDir();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// Format duration
function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  
  if (hours > 0) {
    return `${hours}小时${minutes % 60}分钟`;
  } else if (minutes > 0) {
    return `${minutes}分钟${seconds % 60}秒`;
  } else {
    return `${seconds}秒`;
  }
}

// Format date
function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN');
}

// Get current timestamp
function now() {
  return Date.now();
}

// Start tracking
function startTracking(category = 'other', description = '', tags = []) {
  const config = loadConfig();
  
  if (config.currentSession) {
    console.log('⚠️  已有进行中的活动，请先停止当前活动');
    console.log(`当前活动: ${config.currentSession.description || CATEGORIES[config.currentSession.category]?.name || '未分类'}`);
    console.log(`开始时间: ${formatDate(config.currentSession.startTime)}`);
    console.log(`已进行: ${formatDuration(now() - config.currentSession.startTime)}`);
    return;
  }
  
  const session = {
    id: `session_${now()}_${Math.random().toString(36).substr(2, 9)}`,
    category: category in CATEGORIES ? category : 'other',
    description: description || CATEGORIES[category]?.name || '未命名活动',
    tags: Array.isArray(tags) ? tags : [],
    startTime: now(),
    endTime: null,
    duration: 0
  };
  
  config.currentSession = session;
  config.autoTrack = true;
  saveConfig(config);
  
  const cat = CATEGORIES[session.category];
  console.log(`\n✅ 开始记录: ${cat?.icon || '📌'} ${cat?.name || '其他'}`);
  console.log(`   活动: ${session.description}`);
  if (session.tags.length > 0) {
    console.log(`   标签: ${session.tags.join(', ')}`);
  }
  console.log(`   开始时间: ${formatDate(session.startTime)}`);
}

// Stop tracking
function stopTracking() {
  const config = loadConfig();
  
  if (!config.currentSession) {
    console.log('⚠️  没有进行中的活动');
    return;
  }
  
  const session = config.currentSession;
  session.endTime = now();
  session.duration = session.endTime - session.startTime;
  
  const records = loadRecords();
  records.push(session);
  saveRecords(records);
  
  config.currentSession = null;
  config.autoTrack = false;
  saveConfig(config);
  
  const cat = CATEGORIES[session.category];
  console.log(`\n✅ 活动结束: ${cat?.icon || '📌'} ${cat?.name || '其他'}`);
  console.log(`   活动: ${session.description}`);
  console.log(`   持续时间: ${formatDuration(session.duration)}`);
  console.log(`   结束时间: ${formatDate(session.endTime)}`);
}

// Get status
function getStatus() {
  const config = loadConfig();
  const records = loadRecords();
  
  console.log('\n📊 时间分析器状态');
  console.log('==================');
  
  if (config.currentSession) {
    const session = config.currentSession;
    const cat = CATEGORIES[session.category];
    const elapsed = now() - session.startTime;
    
    console.log('\n🟢 当前活动进行中');
    console.log(`   类别: ${cat?.icon || '📌'} ${cat?.name || '其他'}`);
    console.log(`   活动: ${session.description}`);
    console.log(`   已进行: ${formatDuration(elapsed)}`);
    console.log(`   开始于: ${formatDate(session.startTime)}`);
  } else {
    console.log('\n⚪ 当前无活动记录');
  }
  
  // Today's stats
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayRecords = records.filter(r => r.startTime >= today.getTime());
  const todayDuration = todayRecords.reduce((sum, r) => sum + r.duration, 0);
  
  console.log(`\n📈 今日统计`);
  console.log(`   记录活动数: ${todayRecords.length}`);
  console.log(`   总记录时长: ${formatDuration(todayDuration)}`);
  
  // Total stats
  const totalDuration = records.reduce((sum, r) => sum + r.duration, 0);
  console.log(`\n📈 累计统计`);
  console.log(`   总活动数: ${records.length}`);
  console.log(`   总时长: ${formatDuration(totalDuration)}`);
}

// Analyze time
function analyzeTime(days = 7) {
  const records = loadRecords();
  
  if (records.length === 0) {
    console.log('\n⚠️  暂无记录数据');
    return;
  }
  
  const cutoff = now() - (days * 24 * 60 * 60 * 1000);
  const recentRecords = records.filter(r => r.startTime >= cutoff);
  
  if (recentRecords.length === 0) {
    console.log(`\n⚠️  过去${days}天暂无记录数据`);
    return;
  }
  
  console.log(`\n📊 时间分析报告 (过去${days}天)`);
  console.log('='.repeat(50));
  
  // Category analysis
  const categoryStats = {};
  let totalDuration = 0;
  
  for (const record of recentRecords) {
    const cat = record.category || 'other';
    if (!categoryStats[cat]) {
      categoryStats[cat] = { count: 0, duration: 0, activities: [] };
    }
    categoryStats[cat].count++;
    categoryStats[cat].duration += record.duration;
    categoryStats[cat].activities.push(record.description);
    totalDuration += record.duration;
  }
  
  console.log('\n📁 分类统计');
  console.log('-'.repeat(50));
  
  const sortedCategories = Object.entries(categoryStats)
    .sort((a, b) => b[1].duration - a[1].duration);
  
  for (const [cat, stats] of sortedCategories) {
    const catInfo = CATEGORIES[cat];
    const percentage = totalDuration > 0 ? (stats.duration / totalDuration * 100).toFixed(1) : 0;
    const bar = '█'.repeat(Math.round(percentage / 5));
    
    console.log(`${catInfo?.icon || '📌'} ${catInfo?.name || cat}`);
    console.log(`   次数: ${stats.count} | 时长: ${formatDuration(stats.duration)} | ${percentage}%`);
    console.log(`   ${bar}`);
  }
  
  // Daily average
  const dailyAvg = totalDuration / days;
  console.log('\n📅 日均统计');
  console.log('-'.repeat(50));
  console.log(`   日均活动数: ${(recentRecords.length / days).toFixed(1)}`);
  console.log(`   日均记录时长: ${formatDuration(dailyAvg)}`);
  
  // Peak hours
  const hourDistribution = new Array(24).fill(0);
  for (const record of recentRecords) {
    const hour = new Date(record.startTime).getHours();
    hourDistribution[hour] += record.duration;
  }
  
  const peakHour = hourDistribution.indexOf(Math.max(...hourDistribution));
  console.log(`\n⏰ 活跃时段`);
  console.log('-'.repeat(50));
  console.log(`   最活跃时段: ${peakHour}:00 - ${peakHour + 1}:00`);
  
  // Top activities
  const activityCounts = {};
  for (const record of recentRecords) {
    const desc = record.description;
    activityCounts[desc] = (activityCounts[desc] || 0) + 1;
  }
  
  const topActivities = Object.entries(activityCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);
  
  console.log('\n🔥 高频活动 TOP 5');
  console.log('-'.repeat(50));
  topActivities.forEach(([activity, count], i) => {
    console.log(`   ${i + 1}. ${activity} (${count}次)`);
  });
}

// Generate suggestions
function generateSuggestions() {
  const records = loadRecords();
  
  if (records.length === 0) {
    console.log('\n⚠️  暂无足够数据进行建议分析');
    console.log('💡 建议: 先开始记录一段时间的活动数据');
    return;
  }
  
  const days = 7;
  const cutoff = now() - (days * 24 * 60 * 60 * 1000);
  const recentRecords = records.filter(r => r.startTime >= cutoff);
  
  console.log('\n💡 时间优化建议');
  console.log('='.repeat(50));
  
  // Category analysis
  const categoryStats = {};
  let totalDuration = 0;
  
  for (const record of recentRecords) {
    const cat = record.category || 'other';
    if (!categoryStats[cat]) {
      categoryStats[cat] = { count: 0, duration: 0 };
    }
    categoryStats[cat].count++;
    categoryStats[cat].duration += record.duration;
    totalDuration += record.duration;
  }
  
  const suggestions = [];
  
  // Work-life balance
  const workDuration = (categoryStats.work?.duration || 0) + (categoryStats.meeting?.duration || 0);
  const restDuration = (categoryStats.break?.duration || 0) + (categoryStats.sleep?.duration || 0);
  const entertainmentDuration = categoryStats.entertainment?.duration || 0;
  
  const workPercentage = totalDuration > 0 ? (workDuration / totalDuration * 100) : 0;
  const restPercentage = totalDuration > 0 ? (restDuration / totalDuration * 100) : 0;
  
  if (workPercentage > 50) {
    suggestions.push({
      type: 'warning',
      title: '⚠️ 工作占比过高',
      content: `工作相关活动占${workPercentage.toFixed(1)}%，建议适当增加休息时间，避免过度疲劳。`
    });
  }
  
  if (restPercentage < 20) {
    suggestions.push({
      type: 'warning',
      title: '⚠️ 休息时间不足',
      content: `休息仅占${restPercentage.toFixed(1)}%，建议每工作1小时休息5-10分钟。`
    });
  }
  
  // Focus time
  if (categoryStats.study?.duration || categoryStats.work?.duration) {
    const focusDuration = (categoryStats.study?.duration || 0) + (categoryStats.work?.duration || 0);
    const focusHours = focusDuration / (1000 * 60 * 60);
    
    if (focusHours > 8) {
      suggestions.push({
        type: 'info',
        title: '💪 专注时间充足',
        content: `过去7天专注时间约${focusHours.toFixed(1)}小时，保持这个节奏！`
      });
    } else if (focusHours < 4) {
      suggestions.push({
        type: 'tip',
        title: '💡 提升专注时间',
        content: `专注时间约${focusHours.toFixed(1)}小时，可以尝试番茄工作法（25分钟专注+5分钟休息）。`
      });
    }
  }
  
  // Exercise
  if (!categoryStats.exercise || categoryStats.exercise.duration < 30 * 60 * 1000) {
    suggestions.push({
      type: 'tip',
      title: '💡 增加运动时间',
      content: '建议每周至少150分钟中等强度运动，可以尝试每天30分钟快走或运动。'
    });
  }
  
  // Sleep
  if (!categoryStats.sleep || categoryStats.sleep.duration < 7 * 60 * 60 * 1000 * 7) {
    suggestions.push({
      type: 'warning',
      title: '⚠️ 关注睡眠质量',
      content: '建议每天保持7-8小时睡眠，规律作息有助于提高效率。'
    });
  }
  
  // Output suggestions
  if (suggestions.length === 0) {
    console.log('\n✅ 你的时间分配看起来很平衡！继续保持！');
  } else {
    suggestions.forEach((s, i) => {
      console.log(`\n${i + 1}. ${s.title}`);
      console.log(`   ${s.content}`);
    });
  }
  
  // General tips
  console.log('\n📋 通用建议');
  console.log('-'.repeat(50));
  console.log('   • 使用 "time-analyzer start <category> <description>" 开始记录');
  console.log('   • 使用 "time-analyzer stop" 结束当前活动');
  console.log('   • 定期查看分析报告，调整时间分配');
  console.log('   • 设定每日目标，追踪完成情况');
}

// Generate report
function generateReport(days = 7) {
  const records = loadRecords();
  
  if (records.length === 0) {
    console.log('\n⚠️  暂无记录数据');
    return;
  }
  
  const cutoff = now() - (days * 24 * 60 * 60 * 1000);
  const recentRecords = records.filter(r => r.startTime >= cutoff);
  
  console.log('\n' + '='.repeat(60));
  console.log('                    时间分析报告');
  console.log('                    Time Analysis Report');
  console.log('='.repeat(60));
  console.log(`报告周期: 过去${days}天`);
  console.log(`生成时间: ${formatDate(now())}`);
  console.log('='.repeat(60));
  
  // Summary
  const totalDuration = recentRecords.reduce((sum, r) => sum + r.duration, 0);
  console.log('\n【概览】');
  console.log(`总活动数: ${recentRecords.length}`);
  console.log(`总时长: ${formatDuration(totalDuration)}`);
  console.log(`日均活动: ${(recentRecords.length / days).toFixed(1)}`);
  console.log(`日均时长: ${formatDuration(totalDuration / days)}`);
  
  // Category breakdown
  const categoryStats = {};
  for (const record of recentRecords) {
    const cat = record.category || 'other';
    if (!categoryStats[cat]) {
      categoryStats[cat] = { count: 0, duration: 0 };
    }
    categoryStats[cat].count++;
    categoryStats[cat].duration += record.duration;
  }
  
  console.log('\n【分类详情】');
  const sortedCategories = Object.entries(categoryStats)
    .sort((a, b) => b[1].duration - a[1].duration);
  
  for (const [cat, stats] of sortedCategories) {
    const catInfo = CATEGORIES[cat];
    const percentage = totalDuration > 0 ? (stats.duration / totalDuration * 100).toFixed(1) : 0;
    const hours = (stats.duration / (1000 * 60 * 60)).toFixed(1);
    console.log(`${catInfo?.icon || '📌'} ${catInfo?.name || cat}: ${hours}小时 (${percentage}%) - ${stats.count}次`);
  }
  
  // Recent activities
  console.log('\n【最近活动】');
  const recent = recentRecords.slice(-10).reverse();
  recent.forEach((r, i) => {
    const catInfo = CATEGORIES[r.category];
    const date = new Date(r.startTime).toLocaleDateString('zh-CN');
    console.log(`${i + 1}. [${date}] ${catInfo?.icon || '📌'} ${r.description} - ${formatDuration(r.duration)}`);
  });
  
  console.log('\n' + '='.repeat(60));
  console.log('报告生成完毕');
  console.log('='.repeat(60));
}

// Manual add record
function addRecord(category, description, durationMinutes, tags = []) {
  const record = {
    id: `manual_${now()}_${Math.random().toString(36).substr(2, 9)}`,
    category: category in CATEGORIES ? category : 'other',
    description: description || '手动记录',
    tags: Array.isArray(tags) ? tags : [],
    startTime: now() - (durationMinutes * 60 * 1000),
    endTime: now(),
    duration: durationMinutes * 60 * 1000
  };
  
  const records = loadRecords();
  records.push(record);
  saveRecords(records);
  
  const cat = CATEGORIES[record.category];
  console.log(`\n✅ 手动记录已添加: ${cat?.icon || '📌'} ${cat?.name || '其他'}`);
  console.log(`   活动: ${record.description}`);
  console.log(`   时长: ${formatDuration(record.duration)}`);
}

// List categories
function listCategories() {
  console.log('\n📁 可用活动分类');
  console.log('='.repeat(40));
  Object.entries(CATEGORIES).forEach(([key, info]) => {
    console.log(`  ${info.icon} ${key.padEnd(12)} - ${info.name}`);
  });
  console.log('\n使用: time-analyzer start <category> <description>');
}

// Show help
function showHelp() {
  console.log(`
⏱️  Time Analyzer - 时间分析器

用法: time-analyzer <command> [options]

命令:
  start <category> [description] [tags]  开始记录活动
  stop                                   停止当前活动
  status                                 查看当前状态
  analyze [days]                         分析时间数据 (默认7天)
  suggest                                生成优化建议
  report [days]                          生成完整报告
  add <category> <desc> <minutes>        手动添加记录
  categories                             列出所有分类
  help                                   显示帮助信息

示例:
  time-analyzer start work "写代码"       开始记录工作
  time-analyzer start study "阅读"        开始记录学习
  time-analyzer stop                      结束当前活动
  time-analyzer analyze 30                分析过去30天
  time-analyzer suggest                   获取优化建议
  time-analyzer add work "会议" 60        手动添加1小时会议记录

分类:
  work, study, meeting, break, exercise, entertainment, sleep, other
`);
}

// Main CLI handler
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'start':
      const category = args[1] || 'other';
      const description = args[2] || '';
      const tags = args[3] ? args[3].split(',') : [];
      startTracking(category, description, tags);
      break;
      
    case 'stop':
      stopTracking();
      break;
      
    case 'status':
      getStatus();
      break;
      
    case 'analyze':
      analyzeTime(parseInt(args[1]) || 7);
      break;
      
    case 'suggest':
      generateSuggestions();
      break;
      
    case 'report':
      generateReport(parseInt(args[1]) || 7);
      break;
      
    case 'add':
      const addCat = args[1] || 'other';
      const addDesc = args[2] || '手动记录';
      const addDuration = parseInt(args[3]) || 30;
      const addTags = args[4] ? args[4].split(',') : [];
      addRecord(addCat, addDesc, addDuration, addTags);
      break;
      
    case 'categories':
      listCategories();
      break;
      
    case 'help':
    case '--help':
    case '-h':
    default:
      showHelp();
      break;
  }
}

// Run main
main();

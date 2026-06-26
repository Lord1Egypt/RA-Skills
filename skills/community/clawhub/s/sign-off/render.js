#!/usr/bin/env node
/**
 * Sign-Off 变量渲染器
 * 读取 sign-off.json，自动填充变量，输出最终签名
 * Usage: node render.js [--work|--casual|--template "custom template"]
 */

const fs = require('fs');
const path = require('path');

// 获取当前时间信息
function getTimeInfo() {
  const now = new Date();
  const hour = now.getHours();
  const month = now.getMonth(); // 0-11
  
  // 季节（北半球）
  const seasons = ['冬', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋', '冬', '冬', '冬'];
  const seasonsEn = ['Winter', 'Spring', 'Spring', 'Summer', 'Summer', 'Summer', 'Autumn', 'Autumn', 'Autumn', 'Winter', 'Winter', 'Winter'];
  
  // 时段
  let time, greeting;
  if (hour >= 5 && hour < 8) { time = '清晨'; greeting = '早安'; }
  else if (hour >= 8 && hour < 11) { time = '上午'; greeting = '早安'; }
  else if (hour >= 11 && hour < 14) { time = '午间'; greeting = '午安'; }
  else if (hour >= 14 && hour < 17) { time = '午后'; greeting = '午安'; }
  else if (hour >= 17 && hour < 19) { time = '傍晚'; greeting = '傍晚好'; }
  else if (hour >= 19 && hour < 22) { time = '夜晚'; greeting = '晚安'; }
  else { time = '深夜'; greeting = '夜安'; }
  
  // 星期
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  
  // 生肖
  const zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
  const year = now.getFullYear();
  const zodiac = zodiacs[(year - 4) % 12] + '年';
  
  return {
    season: seasons[month],
    seasonEn: seasonsEn[month],
    time,
    greeting,
    dayOfWeek: days[now.getDay()],
    zodiac,
  };
}

// 渲染模板
function render(template, variables) {
  return template.replace(/\{(\w+)\}/g, (match, key) => {
    return variables[key] !== undefined ? variables[key] : match;
  });
}

// 主逻辑
function main() {
  const args = process.argv.slice(2);
  const workspaceRoot = process.env.OPENCLAW_WORKSPACE || process.cwd();
  const configPath = path.join(workspaceRoot, 'sign-off.json');
  
  let config = {};
  try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  } catch (e) {
    console.error('⚠️ sign-off.json not found, using defaults');
    config = { name: 'AI', location: '' };
  }
  
  const timeInfo = getTimeInfo();
  
  // 合并所有变量
  const variables = {
    name: config.name || 'AI',
    location: config.location || '',
    emoji: config.emoji || '',
    seal: config.seal || '',
    mood: config.mood || '',
    ...timeInfo,
  };
  
  // 选择模板
  let template = config.template || '{name} · {location}';
  
  // 检查上下文模式
  if (args.includes('--work') && config.customTemplates?.work) {
    template = config.customTemplates.work;
  } else if (args.includes('--casual') && config.customTemplates?.casual) {
    template = config.customTemplates.casual;
  } else {
    const tIdx = args.indexOf('--template');
    if (tIdx !== -1 && args[tIdx + 1]) {
      template = args[tIdx + 1];
    }
  }
  
  // 渲染
  const result = render(template, variables);
  console.log(result);
}

main();

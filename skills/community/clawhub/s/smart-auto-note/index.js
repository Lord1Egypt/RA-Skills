const fs = require('fs').promises;
const path = require('path');

// ==========================================
// 配置 (移除了 reminders.json)
// ==========================================
const BASE_DIR = '/Users/macbook/Documents/OC_club';
const PATHS = {
  workTodo: path.join(BASE_DIR, '工作待办.md'),
  lifeTodo: path.join(BASE_DIR, '生活待办.md'),
  workRecord: path.join(BASE_DIR, '工作记录.md'),
  inspiration: path.join(BASE_DIR, '灵感.md')
};

// 全局状态 (仅保留分类确认状态)
let pendingState = null;
let pendingArchiveState = null;

// ==========================================
// 初始化
// ==========================================
async function ensureFiles() {
  await fs.mkdir(BASE_DIR, { recursive: true });
  for (const key of Object.keys(PATHS)) {
    try {
      await fs.access(PATHS[key]);
    } catch {
      await fs.writeFile(PATHS[key], '');
    }
  }
}

function getNow() {
  const now = new Date();
  return { dateStr: now.toISOString().split('T')[0], timeStr: now.toTimeString().slice(0, 5), now };
}

// ==========================================
// 工具函数 (移除了时间解析、修改指令检查)
// ==========================================
function shouldTrigger(input) {
  if (!input || input.trim().length < 2) return { trigger: false };
  const negWords = ['不用', '取消', '删除', '不做了', '停止'];
  const hasNeg = negWords.some(w => input.includes(w));
  const hasQuestion = input.includes('?') || input.includes('?');
  return !((hasNeg || hasQuestion));
}

function splitContent(input) {
  return input.split(/[\n;;。]/).map(p => p.trim()).filter(p => p.length > 0);
}

function classify(input) {
  const projectClients = ['东方证券', '中国银联', '中银证券', '国智投', '银联商务', '证券', '基金', '中汇亿达', '期货', '保险', '银行', '集团', '信托'];
  const workTodoKeys = ['会议', '汇报', '对接', '项目', 'deadline', '工作待办', '准备', '评审', '标书', '合同',...projectClients];
  const lifeTodoKeys = ['买菜', '缴费', '接孩子', '生活待办', '家务', '就医', '挂号', '购物', '生日'];
  const recordKeys = ['今天做了', '已完成', '会议记录', '搞定了', '做完了', '复盘',...projectClients];
  const ideaKeys = ['灵感', '想法', '创意', '种草', '金句', '感悟', '备忘'];

  if (workTodoKeys.some(k => input.includes(k))) return { category: '工作待办', confidence: 95 };
  if (lifeTodoKeys.some(k => input.includes(k))) return { category: '生活待办', confidence: 95 };
  if (recordKeys.some(k => input.includes(k))) return { category: '工作记录', confidence: 90 };
  if (ideaKeys.some(k => input.includes(k))) return { category: '灵感', confidence: 95 };
  return { category: null, confidence: 50 };
}

function classifyArchive(content) {
  const projectClients = ['东方证券', '中国银联', '中银证券', '国智投', '银联商务', '证券', '基金', '中汇亿达', '期货', '保险', '银行', '集团', '信托'];
  if (projectClients.some(k => content.includes(k))) return { subCategory: '项目类', confidence: 95 };

  const projectKeys = ['客户', '项目', '基金', '商务', '招投标', '合同', '回款', '对接'];
  if (projectKeys.some(k => content.includes(k))) return { subCategory: '项目类', confidence: 92 };
  return { subCategory: '其他类', confidence: 85 };
}

function formatContent(content, category, subCategory = null) {
  const { dateStr, timeStr } = getNow();
  switch (category) {
    case '工作待办': case '生活待办': return `\n- [ ] ${content} #${category}`; // 移除了时间标签 ⏰
    case '工作记录': return `\n${dateStr} ${subCategory || '其他类'}记录\n* ${timeStr} | ${content}`;
    case '灵感': return `\n- 💡 ${content}(${dateStr} ${timeStr})`;
    case '归档': return `\n${dateStr} ${subCategory}记录\n* ${timeStr} | ${content}(已完成待办自动归档)`;
    default: return `\n- ${content}`;
  }
}

function getFilePath(category) {
  switch (category) {
    case '工作待办': return PATHS.workTodo;
    case '生活待办': return PATHS.lifeTodo;
    case '工作记录': return PATHS.workRecord;
    case '灵感': return PATHS.inspiration;
    default: return null;
  }
}

async function doArchive(content, subCategory) {
  await fs.appendFile(PATHS.workRecord, formatContent(content, '归档', subCategory));
  return { success: true, msg: `✅ 已完成工作待办自动归档` };
}

// ==========================================
// 主入口 (纯净版)
// ==========================================
async function main(input, context) {
  await ensureFiles();

  // 状态机1:归档分类确认
  if (pendingArchiveState) {
    const reply = input.trim();
    if (reply === '项目类' || reply === '其他类') {
      const res = await doArchive(pendingArchiveState.content, reply);
      pendingArchiveState = null;
      return res.msg;
    } else {
      pendingArchiveState = null;
      return '已取消归档操作。';
    }
  }

  // 状态机2:内容分类确认
  if (pendingState) {
    const reply = input.trim();
    const valid = ['工作待办', '生活待办', '工作记录', '灵感'];
    if (valid.includes(reply)) {
      const fp = getFilePath(reply);
      await fs.appendFile(fp, formatContent(pendingState.content, reply));
      pendingState = null;
      return `✅ 已成功记录到【${reply}】`;
    } else {
      pendingState = null;
      return '已取消操作。';
    }
  }

  // 前置触发
  if (!shouldTrigger(input)) return null;

  // 多内容拆分处理
  const items = splitContent(input);
  const results = [];

  for (const item of items) {
    const { category, confidence } = classify(item);
    if (confidence < 90) {
      pendingState = { content: item };
      return `请问这条内容你想记录为【工作待办 / 生活待办 / 工作记录 / 灵感】哪一类?\n 即将写入的内容预览:【${item}】`;
    }

    const filePath = getFilePath(category);
    await fs.appendFile(filePath, formatContent(item, category));
    results.push(`✅ 已成功记录到【${category}】`);
  }

  return results.join("\n");
}

// 初始化
ensureFiles();

// 导出 (仅保留 main)
module.exports = { main };
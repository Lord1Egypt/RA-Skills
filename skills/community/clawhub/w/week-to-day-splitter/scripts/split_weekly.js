#!/usr/bin/env node
/**
 * split_weekly.js v7 - 周工作计划拆分到日工作计划（用户拍板 v7 算法）
 *
 * v7 核心设计（用户拍板）：
 *   1. 截止日期重新定义：
 *      - 任务标题下 [截止:YYYYMMDD] = 整个项目预期完成时间（用户拍板）
 *      - 下一步子步骤 #周一/#周二/.../#待定 = 这一步最晚完成时间
 *   2. 分配原则（用户拍板，3 优先级）：
 *      - 第一优先级：沟通类/temporary 优先放前半周（周一/二/三）
 *      - 第二优先级：出差/拜访约束（同地点 ≤2）
 *      - 第三优先级：按子步骤时间标签灵活分配
 *   3. 任务整体 vs 拆分（v7 关键）：
 *      - 所有子步骤时间标签一致 → 任务整体分配
 *      - 子步骤时间标签不同 → 拆分到不同日
 *   4. 移除硬编码 swapDays（行程动态）
 *
 * 作者：小伊
 * 日期：2026-08-16 v7
 */

'use strict';

const fs = require('fs');
const path = require('path');

const WEEK_DIR = '${NOTES_DIR}/001周工作计划';
const DAY_DIR = '${NOTES_DIR}/002日工作计划';
const DAY_NAMES = ['周一', '周二', '周三', '周四', '周五'];

// ============================================================
// 1. 工具函数（同 v6）
// ============================================================

function findWeekFileByStartDate(targetStart) {
  if (!fs.existsSync(WEEK_DIR)) {
    console.error(`❌ 周计划目录不存在: ${WEEK_DIR}`);
    return null;
  }
  const files = fs.readdirSync(WEEK_DIR)
    .filter(f => f.endsWith('.md') && !f.includes('.bak'))
    .map(f => ({
      name: f,
      path: path.join(WEEK_DIR, f),
      mtime: fs.statSync(path.join(WEEK_DIR, f)).mtimeMs
    }));
  files.sort((a, b) => b.mtime - a.mtime);
  for (const f of files) {
    const match = f.name.match(/【(\d{8})-(\d{8})】/);
    if (match && match[1] === targetStart) {
      return f.path;
    }
  }
  console.error(`❌ 未找到周开始日期为 ${targetStart} 的周计划文件`);
  return null;
}

function getNextWeekStart(now = new Date()) {
  const d = new Date(now);
  const day = d.getDay();
  let daysToNextMonday;
  if (day === 0) daysToNextMonday = 1;
  else if (day === 1) daysToNextMonday = 7;
  else if (day === 2) daysToNextMonday = 6;
  else if (day === 3) daysToNextMonday = 5;
  else if (day === 4) daysToNextMonday = 4;
  else if (day === 5) daysToNextMonday = 3;
  else daysToNextMonday = 2;
  d.setDate(d.getDate() + daysToNextMonday);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}${mm}${dd}`;
}

function getDatesFromRange(start, end) {
  const dates = [];
  const startDate = new Date(
    parseInt(start.slice(0, 4)),
    parseInt(start.slice(4, 6)) - 1,
    parseInt(start.slice(6, 8))
  );
  for (let i = 0; i < 5; i++) {
    const d = new Date(startDate);
    d.setDate(startDate.getDate() + i);
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    dates.push(`${yyyy}${mm}${dd}`);
  }
  return dates;
}

function getNextDay(now = new Date()) {
  const d = new Date(now);
  d.setDate(d.getDate() + 1);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}${mm}${dd}`;
}

function getDayName(date) {
  const d = new Date(
    parseInt(date.slice(0, 4)),
    parseInt(date.slice(4, 6)) - 1,
    parseInt(date.slice(6, 8))
  );
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  return days[d.getDay()];
}

// ============================================================
// 2. 动作类型 + 时间标签 分类（v7 关键改动）
// ============================================================

const EXECUTION_TAGS = ['踏勘', '拜访', '来访', '出差'];
const DOCUMENT_TAGS = ['写方案', '拟协议', '写报告', '调研'];
const TEMPORARY_TAGS = ['沟通', '请示', '跟进', '确认', '等待', '流转'];

// 时间标签（v7 设计）
const DAY_TAGS = ['周一', '周二', '周三', '周四', '周五', '待定'];

const dayTagMap = { '周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '待定': 4 };

function isActionTag(tag) {
  return EXECUTION_TAGS.includes(tag) || DOCUMENT_TAGS.includes(tag) || TEMPORARY_TAGS.includes(tag);
}

function isDayTag(tag) {
  return DAY_TAGS.includes(tag);
}

function getActionNature(actionTag) {
  if (!actionTag) return null;
  if (EXECUTION_TAGS.includes(actionTag)) return 'execution';
  if (DOCUMENT_TAGS.includes(actionTag)) return 'document';
  if (TEMPORARY_TAGS.includes(actionTag)) return 'temporary';
  return null;
}

function getNatureFlag(nature) {
  if (nature === 'execution') return '🌍';
  if (nature === 'document') return '📝';
  if (nature === 'temporary') return '⚡';
  return '❓';
}

// ============================================================
// 3. 解析器（v7：项目整体截止 + 子步骤时间标签）
// ============================================================

function parseWeeklyPlan(content) {
  const lines = content.split('\n');
  const tasks = [];
  const constraints = [];
  let weekRange = null;
  let currentTask = null;
  let inConstraints = false;

  for (const line of lines) {
    const titleMatch = line.match(/^# 【(\d{8})-(\d{8})】/);
    if (titleMatch) {
      weekRange = `${titleMatch[1]}-${titleMatch[2]}`;
      continue;
    }

    const taskMatch = line.match(/^### (\d+)\. (.+)$/);
    if (taskMatch) {
      if (currentTask) tasks.push(currentTask);
      currentTask = {
        id: parseInt(taskMatch[1]),
        title: taskMatch[2].trim(),
        contacts: [],
        deadline: '',             // 项目整体截止（v7）
        projectDeadline: '',      // 备用字段
        type: '',
        notes: '',
        progress: '',
        nextStepLines: [],
        subSteps: [],
        actionTags: [],
        dayTags: [],              // 子步骤时间标签集合
        isCrossWeek: false,
        isBlocker: false,
        location: ''
      };
      inConstraints = false;
      continue;
    }

    // 任务标题下的标签行：@联系人 [截止:YYYYMMDD] 📍地点 ⚠️阻塞（跨周）
    if (currentTask && line.trim().match(/^`[@#⚠️📍\[\]]|^@|^⚠️|^📍/)) {
      const tagLine = line.trim();
      currentTask.contacts = extractContacts(tagLine);
      currentTask.deadline = extractDeadline(tagLine);
      currentTask.projectDeadline = extractDeadline(tagLine); // v7: 项目整体截止
      currentTask.location = extractLocation(tagLine);
      currentTask.isBlocker = tagLine.includes('⚠️');
      continue;
    }

    const fieldMatch = line.match(/^- \*\*(.+?)\*\*[：:](.+)?$/);
    if (fieldMatch && currentTask) {
      const field = fieldMatch[1];
      let value = (fieldMatch[2] || '').trim();
      value = value.replace(/^\*+/, '').replace(/\*+$/, '').trim();
      if (field === '已推进') {
        currentTask.progress = value;
      } else if (field === '下一步' || field === '下一步工作') {
        if (value && !value.startsWith('-')) {
          currentTask.nextStepLines = [value];
          const parsed = parseSubStepText(value);
          currentTask.subSteps = [{
            text: parsed.text,
            actionTag: parsed.actionTag || '',
            dayTag: parsed.dayTag || '',  // v7: 时间标签
            nature: getActionNature(parsed.actionTag) || 'unknown'
          }];
          if (parsed.actionTag && !currentTask.actionTags.includes(parsed.actionTag)) {
            currentTask.actionTags.push(parsed.actionTag);
          }
          if (parsed.dayTag && !currentTask.dayTags.includes(parsed.dayTag)) {
            currentTask.dayTags.push(parsed.dayTag);
          }
        }
      } else if (field === '任务备注' || field === '备注') {
        currentTask.notes = value;
        if (value.includes('续上周') || value.includes('跨周')) {
          currentTask.isCrossWeek = true;
        }
      } else if (field === '类型') {
        currentTask.type = value;
      } else if (field === '预计完成时间' || field === '截止') {
        currentTask.deadline = value;
        currentTask.projectDeadline = value;
      } else if (field === '联系人') {
        currentTask.contacts = extractContacts(value);
      }
      continue;
    }

    if (currentTask && line.match(/^\s+-\s+/) && !line.match(/^\s+-\s*$/)) {
      let subText = line.replace(/^\s+-\s+/, '').trim();
      subText = subText.replace(/^\*+/, '').replace(/\*+$/, '').trim();
      if (subText) {
        const parsed = parseSubStepText(subText);
        const subStep = {
          text: parsed.text,
          actionTag: parsed.actionTag || '',
          dayTag: parsed.dayTag || '',  // v7: 时间标签
          nature: getActionNature(parsed.actionTag) || 'unknown'
        };
        currentTask.nextStepLines.push(subText);
        currentTask.subSteps.push(subStep);
        if (parsed.actionTag && !currentTask.actionTags.includes(parsed.actionTag)) {
          currentTask.actionTags.push(parsed.actionTag);
        }
        if (parsed.dayTag && !currentTask.dayTags.includes(parsed.dayTag)) {
          currentTask.dayTags.push(parsed.dayTag);
        }
      }
      continue;
    }

    if (line.trim().startsWith('## 约束')) {
      inConstraints = true;
      continue;
    }
    if (inConstraints && line.trim().startsWith('- ')) {
      constraints.push(line.trim().slice(2));
    }
  }

  if (currentTask) tasks.push(currentTask);
  const dedupedTasks = deduplicateTasks(tasks);
  return { tasks: dedupedTasks, constraints, weekRange };
}

function deduplicateTasks(tasks) {
  const seen = new Map();
  const result = [];
  for (const task of tasks) {
    const key = task.title.replace(/\s+/g, ' ').trim();
    if (seen.has(key)) {
      console.log(`⚠️ 去重: 任务 ${task.id}「${task.title.slice(0, 20)}」与任务 ${seen.get(key)} 重复，跳过`);
      continue;
    }
    seen.set(key, task.id);
    result.push(task);
  }
  return result;
}

/**
 * v7: 解析子步骤文本，提取动作类型 + 时间标签
 * 输入: "调研沙滩情况 #调研 #周一"
 * 输出: { text: "调研沙滩情况", actionTag: "调研", dayTag: "周一" }
 */
function parseSubStepText(text) {
  // 提取末尾的所有 #xxx 标签
  const tagMatches = [...text.matchAll(/\s*`?#([\u4e00-\u9fffA-Za-z]+)`?\s*/g)];
  
  let actionTag = null;
  let dayTag = null;
  let cleanText = text;
  
  // 倒序遍历，提取每个标签的类型
  for (const m of tagMatches) {
    const tag = m[1];
    if (isActionTag(tag) && !actionTag) {
      actionTag = tag;
      cleanText = cleanText.replace(m[0], ' ');
    } else if (isDayTag(tag) && !dayTag) {
      dayTag = tag;
      cleanText = cleanText.replace(m[0], ' ');
    }
  }
  
  cleanText = cleanText.trim();
  
  // fallback：单 #xxx（可能是动作类型或时间标签）
  if (!actionTag && !dayTag) {
    const singleMatch = text.match(/\s*`?#([\u4e00-\u9fffA-Za-z]+?)`?\s*$/);
    if (singleMatch) {
      const tag = singleMatch[1];
      if (isActionTag(tag)) {
        actionTag = tag;
      } else if (isDayTag(tag)) {
        dayTag = tag;
      }
      cleanText = text.replace(/\s*`?#[\u4e00-\u9fffA-Za-z]+?`?\s*$/, '').trim();
    }
  }
  
  return { text: cleanText, actionTag, dayTag };
}

function extractContacts(text) {
  return text.match(/@[\u4e00-\u9fffA-Za-z]+/g) || [];
}

function extractDeadline(text) {
  const match = text.match(/\[截止[:：]([^\]]+)\]/);
  return match ? match[1].trim() : '';
}

function extractLocation(text) {
  const match = text.match(/📍([\u4e00-\u9fffA-Za-z市州区]+)/);
  return match ? match[1] : '';
}

function getTaskNature(task) {
  if (task.subSteps.length === 0) return 'unknown';
  const natures = task.subSteps.map(s => s.nature);
  if (natures.includes('execution')) return 'execution';
  if (natures.includes('document')) return 'document';
  if (natures.includes('temporary')) return 'temporary';
  return 'unknown';
}

// ============================================================
// 4. 约束检查（同 v6）
// ============================================================

function isValidDay(task, day, result) {
  const executionWithLocation = ['拜访', '来访', '出差'];
  if (task.actionTags && task.actionTags.some(t => executionWithLocation.includes(t)) && task.location) {
    const sameLocation = result[day].filter(t =>
      t.actionTags && t.actionTags.some(at => executionWithLocation.includes(at)) &&
      t.location === task.location
    );
    if (sameLocation.length >= 2) return false;
  }

  if (task.nature === 'document') {
    const docs = result[day].filter(t => t.nature === 'document');
    if (docs.length >= 2) return false;
  }

  if (task.nature === 'execution') {
    const executions = result[day].filter(t => t.nature === 'execution');
    if (executions.length >= 2) return false;
  }

  if (result[day].length >= 5) return false;
  return true;
}

function countNatures(day, result) {
  let execution = 0, document = 0, temporary = 0;
  for (const t of result[day]) {
    if (t.nature === 'execution') execution++;
    else if (t.nature === 'document') document++;
    else if (t.nature === 'temporary') temporary++;
  }
  return { execution, document, temporary };
}

// ============================================================
// 5. 拆分算法（v7：任务整体 vs 拆分 + 时间标签驱动）
// ============================================================

/**
 * v7 关键：判断任务是否需要拆分
 *   - 所有子步骤时间标签一致 → 任务整体分配
 *   - 子步骤时间标签不同 → 拆分到不同日
 */
function shouldSplit(task) {
  if (task.subSteps.length <= 1) return false;
  const dayTags = task.subSteps.map(s => s.dayTag).filter(Boolean);
  const uniqueDayTags = [...new Set(dayTags)];
  return uniqueDayTags.length > 1;
}

function assignTasks(tasks) {
  const result = {};
  DAY_NAMES.forEach(d => { result[d] = []; });

  // Step 1: 任务整体 vs 拆分
  const expanded = [];
  for (const task of tasks) {
    if (shouldSplit(task)) {
      // 子步骤时间标签不同 → 拆分到不同日
      task.subSteps.forEach((sub, idx) => {
        expanded.push({
          ...task,
          originalId: task.id,
          id: `${task.id}.${idx + 1}`,
          nextStep: sub.text,
          actionTags: sub.actionTag ? [sub.actionTag] : [],
          nature: getActionNature(sub.actionTag) || 'unknown',
          subSteps: [sub],
          subStepIdx: idx,
          subTaskCount: task.subSteps.length,
          isSubTask: true
        });
      });
    } else {
      // 任务整体（默认）
      expanded.push({
        ...task,
        isSubTask: false,
        subStepCount: 1,
        subStepIdx: 0,
        nature: getTaskNature(task),
        originalId: task.id
      });
    }
  }

  // Step 2: 排序
  // 优先级：阻塞 > 沟通类/temporary 先排 > id
  const sorted = [...expanded].sort((a, b) => {
    if (a.isBlocker && !b.isBlocker) return -1;
    if (!a.isBlocker && b.isBlocker) return 1;

    const aIsComm = a.actionTags && a.actionTags.some(t => TEMPORARY_TAGS.includes(t));
    const bIsComm = b.actionTags && b.actionTags.some(t => TEMPORARY_TAGS.includes(t));

    if (aIsComm && !bIsComm) return -1;
    if (!aIsComm && bIsComm) return 1;

    return a.id - b.id;
  });

  // Step 3: 分配
  for (const task of sorted) {
    const day = pickDay(task, result);
    result[day].push(task);
  }

  return result;
}

/**
 * v7 pickDay（用户拍板 3 优先级）
 *   - 第一优先级：沟通类/temporary 优先放前半周（周一/二/三）
 *   - 第二优先级：出差/拜访约束（同地点 ≤2）
 *   - 第三优先级：按子步骤时间标签灵活分配
 */
function pickDay(task, result) {
  // 用户拍板 v7 算法：
  //   第一优先级：按子步骤时间标签分配（用户时间标签是 用户偏好的体现）
  //   第二优先级：出差/拜访约束（已包含在 isValidDay 中）
  //   第三优先级：fallback 找最空的天
  //
  // 注：之前拍板"沟通类/temporary 优先前半周"已经被 用户时间标签反映
  //   - 用户给临时任务标 #周一/#周二/#周三 → 算法自然优先前半周
  //   - 用户给临时任务标 #周四/#周五 → 算法自然优先后半周
  //   - 算法不再硬编码"沟通类优先前半周"，让 用户时间标签决定

  // 取最晚时间标签
  let latestDayIdx = 4; // 默认周五
  for (const sub of task.subSteps) {
    if (sub.dayTag && dayTagMap[sub.dayTag] !== undefined) {
      latestDayIdx = Math.min(latestDayIdx, dayTagMap[sub.dayTag]);
    }
  }

  // 从 latestDayIdx 向前找（用户拍板：灵活分配，可以提前）
  for (let i = latestDayIdx; i >= 0; i--) {
    if (isValidDay(task, DAY_NAMES[i], result)) {
      return DAY_NAMES[i];
    }
  }

  // fallback 找最空的天
  let minDay = null;
  let minCount = Infinity;
  for (let i = 0; i < 5; i++) {
    const day = DAY_NAMES[i];
    if (isValidDay(task, day, result) && result[day].length < minCount) {
      minDay = day;
      minCount = result[day].length;
    }
  }
  return minDay || '周五';
}

// ============================================================
// 6. swapDays (v7 移除：行程动态，swap 由用户人工调整)
// ============================================================

function swapDays(assignment) {
  return { ...assignment };
}

// ============================================================
// 7. 写文件
// ============================================================

function formatDailyPlan(date, dayName, tasks, weekRange) {
  let content = `# 【${date}】${dayName}工作计划\n\n`;
  content += `> 基于【${weekRange}】周工作计划\n\n`;

  const taskGroups = new Map();
  for (const task of tasks) {
    const taskId = task.isSubTask ? task.originalId : task.id;
    if (!taskGroups.has(taskId)) {
      taskGroups.set(taskId, {
        title: task.title,
        subSteps: [],
        isCrossWeek: task.isCrossWeek,
        notes: task.notes
      });
    }
    for (const sub of task.subSteps) {
      taskGroups.get(taskId).subSteps.push({
        text: sub.text,
        actionTag: sub.actionTag,
        dayTag: sub.dayTag
      });
    }
  }

  const sortedKeys = [...taskGroups.keys()].sort((a, b) => a - b);
  for (const taskId of sortedKeys) {
    const group = taskGroups.get(taskId);
    
    let line = `### ${taskId}. ${group.title}`;
    if (group.isCrossWeek) line += '（跨周）';
    line += '：\n';
    content += line;
    
    for (const sub of group.subSteps) {
      const cleanText = sub.text.replace(/\s*`?#[\u4e00-\u9fffA-Za-z]+?`?\s*/g, '').trim();
      // 重建标签: #动作 #时间
      const tags = [];
      if (sub.actionTag) tags.push(`#${sub.actionTag}`);
      if (sub.dayTag) tags.push(`#${sub.dayTag}`);
      const tagStr = tags.length > 0 ? ' `' + tags.join(' ') + '`' : '';
      // 用户 拍板 2026-08-18:加 checkbox(默认未勾)
      content += `  - [ ] ${cleanText}${tagStr}\n`;
    }
  }

  return content;
}

function writeDailyPlans(assignment, weekRange, outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const dates = getDatesFromRange(
    weekRange.split('-')[0],
    weekRange.split('-')[1]
  );

  const swapped = swapDays(assignment);

  const written = [];
  for (let i = 0; i < 5; i++) {
    const dayName = DAY_NAMES[i];
    const date = dates[i];
    const tasks = swapped[dayName] || [];

    const content = formatDailyPlan(date, dayName, tasks, weekRange);
    const filename = `【${date}】${dayName}工作计划.md`;
    const filepath = path.join(outputDir, filename);

    safeWriteFile(filepath, content);
    written.push(filepath);
  }

  return written;
}


/**
 * 安全写文件（v1.0.2 新增）
 *
 * 1. 如果文件已存在，先备份到 .bak
 * 2. 原子写入：先写 .tmp 文件，再 rename
 * 3. 错误处理：失败时清理 .tmp
 *
 * @param {string} filepath - 目标文件路径
 * @param {string} content - 要写入的内容
 */


/**
 * 安全写文件（v1.0.2 新增）
 * 1. 备份已存在文件到 .bak
 * 2. 原子写入（先写 .tmp 再 rename）
 */
function safeWriteFile(filepath, content) {
  if (fs.existsSync(filepath)) {
    const backupPath = filepath + '.bak';
    try {
      fs.copyFileSync(filepath, backupPath);
      console.log(`[备份] 旧文件已备份到 ${backupPath}`);
    } catch (e) {
      console.warn(`[备份] 备份失败: ${e.message}`);
    }
  }
  const tmpPath = filepath + '.tmp.' + Date.now();
  try {
    fs.writeFileSync(tmpPath, content, 'utf-8');
    fs.renameSync(tmpPath, filepath);
  } catch (e) {
    if (fs.existsSync(tmpPath)) {
      try { fs.unlinkSync(tmpPath); } catch (e2) {}
    }
    throw e;
  }
}

// ============================================================
// 8. 推送单日计划（同 v6）
// ============================================================

function getDailyPlanForDate(date) {
  const dayName = getDayName(date);
  const filepath = path.join(DAY_DIR, `【${date}】${dayName}工作计划.md`);
  if (!fs.existsSync(filepath)) {
    return null;
  }
  return fs.readFileSync(filepath, 'utf-8');
}

function getNextDayPlan(now = new Date()) {
  const nextDate = getNextDay(now);
  const nextDayName = getDayName(nextDate);
  
  if (nextDayName === '周六' || nextDayName === '周日') {
    return null;
  }
  
  return {
    date: nextDate,
    dayName: nextDayName,
    content: getDailyPlanForDate(nextDate)
  };
}

// ============================================================
// 9. LLM 兜底
// ============================================================

async function assignTasksWithLLM(tasks, constraints) {
  console.log('⚠️ LLM 兜底触发（占位）');
  return assignTasks(tasks);
}

// ============================================================
// 10. 主入口
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const useLLM = args.includes('--algo') && args[args.indexOf('--algo') + 1] === 'llm';
  const pushMode = args.includes('--push');
  
  const weekStartIdx = args.indexOf('--week-start');
  let targetWeekStart = null;
  if (weekStartIdx >= 0 && weekStartIdx + 1 < args.length) {
    targetWeekStart = args[weekStartIdx + 1];
  } else {
    targetWeekStart = getNextWeekStart();
  }

  console.log('=== split_weekly.js v7 启动（v7 算法） ===');
  console.log(`时间: ${new Date().toISOString()}`);
  console.log(`模式: ${dryRun ? 'Dry-run' : '实际写入'}`);
  console.log(`算法: ${useLLM ? 'LLM' : '规则'}`);
  console.log(`目标周开始日期: ${targetWeekStart}`);
  console.log('');

  if (pushMode) {
    const nextDayPlan = getNextDayPlan();
    if (!nextDayPlan) {
      console.log('⏭️ 无需推送');
      process.exit(0);
    }
    if (!nextDayPlan.content) {
      console.error(`❌ 次日 ${nextDayPlan.date} 日计划文件不存在`);
      process.exit(1);
    }
    console.log(`📤 次日 ${nextDayPlan.date}（${nextDayPlan.dayName}）工作计划：`);
    console.log('');
    console.log('---BEGIN---');
    console.log(nextDayPlan.content);
    console.log('---END---');
    process.exit(0);
  }

  const weekFile = findWeekFileByStartDate(targetWeekStart);
  if (!weekFile) {
    console.error('❌ 没找到周计划文件');
    process.exit(1);
  }
  console.log(`📄 周计划文件: ${path.basename(weekFile)}`);

  const content = fs.readFileSync(weekFile, 'utf-8');
  const { tasks, constraints, weekRange } = parseWeeklyPlan(content);
  console.log(`📊 解析结果: ${tasks.length} 个任务（去重后）`);
  console.log(`📅 周计划范围: ${weekRange}`);
  console.log('');

  console.log('=== 任务列表（v7 项目整体截止 + 子步骤时间标签） ===');
  for (const task of tasks) {
    const nature = getTaskNature(task);
    const natureFlag = getNatureFlag(nature);
    const tags = task.actionTags.join(' ') || '(无动作类型)';
    const days = task.dayTags.join('/') || '(无时间标签)';
    const crossWeek = task.isCrossWeek ? '（跨周）' : '';
    const subCount = task.subSteps.length;
    const deadline = task.projectDeadline ? ` 截止=${task.projectDeadline}` : '';
    console.log(`${natureFlag} 任务 ${task.id}: ${task.title.slice(0, 25)}${crossWeek}${deadline} | 性质=${nature} | #${tags} | 时间=${days} | 子步骤=${subCount}`);
  }
  console.log('');

  let assignment;
  if (useLLM) {
    assignment = await assignTasksWithLLM(tasks, constraints);
  } else {
    assignment = assignTasks(tasks);
  }

  const swapped = swapDays(assignment);

  for (const day of DAY_NAMES) {
    const dayTasks = swapped[day];
    const counts = countNatures(day, swapped);
    console.log(`\n--- ${day}（${dayTasks.length} 个任务 | 🌍${counts.execution} 📝${counts.document} ⚡${counts.temporary}） ---`);
    if (dayTasks.length === 0) {
      console.log('  (空)');
    }
    for (const t of dayTasks) {
      const natureFlag = getNatureFlag(t.nature);
      const tags = t.actionTags ? t.actionTags.join(' ') : '';
      const crossWeek = t.isCrossWeek ? '（跨周）' : '';
      console.log(`  ${natureFlag} ${t.id}. ${t.title.slice(0, 30)}${crossWeek} | ${tags}`);
    }
  }

  console.log('\n=== 约束校验 ===');
  let ok = true;
  let totalSubs = 0;
  for (const day of DAY_NAMES) {
    const count = swapped[day].length;
    totalSubs += count;
    const counts = countNatures(day, swapped);
    if (count > 5) {
      console.log(`❌ ${day}: ${count} 个任务（超过 5）`);
      ok = false;
    } else if (counts.execution > 2) {
      console.log(`❌ ${day}: ${counts.execution} 个执行型（超过 2）`);
      ok = false;
    } else if (counts.document > 2) {
      console.log(`❌ ${day}: ${counts.document} 个文档型（超过 2）`);
      ok = false;
    } else {
      console.log(`✅ ${day}: ${count} 个任务 (🌍${counts.execution} 📝${counts.document} ⚡${counts.temporary})`);
    }
  }
  console.log(`📊 总任务/子步骤数: ${totalSubs}`);

  if (dryRun) {
    console.log('\n[DRY-RUN] 跳过文件写入');
    console.log('⚠️ v7 输出是算法基础分配（按时间标签）。用户可以根据行程手动调整。');
  } else {
    const written = writeDailyPlans(assignment, weekRange, DAY_DIR);
    console.log('\n=== 写入完成 ===');
    for (const f of written) {
      console.log(`✅ ${path.basename(f)}`);
    }
  }

  console.log('\n=== split_weekly.js v7 结束 ===');
}

if (require.main === module) {
  main().catch(err => {
    console.error('❌ 错误:', err);
    process.exit(1);
  });
}

module.exports = {
  parseWeeklyPlan,
  parseSubStepText,
  getActionNature,
  isActionTag,
  isDayTag,
  EXECUTION_TAGS,
  DOCUMENT_TAGS,
  TEMPORARY_TAGS,
  DAY_TAGS,
  dayTagMap,
  getTaskNature,
  isValidDay,
  assignTasks,
  shouldSplit,
  findWeekFileByStartDate,
  getNextWeekStart,
  getNextDayPlan,
  swapDays,
  getDayName,
  getDatesFromRange,
  deduplicateTasks
};

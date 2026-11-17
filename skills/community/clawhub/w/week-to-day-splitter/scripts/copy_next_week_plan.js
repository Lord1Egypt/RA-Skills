#!/usr/bin/env node
/**
 * copy_next_week_plan.js - 周五 15:00 复制下周周计划副本
 *
 * 功能：
 *   1. 找到当前周计划（mtime 最新 + 文件名匹配 【YYYYMMDD-YYYYMMDD】周工作计划）
 *   2. 复制副本到 001周工作计划/
 *   3. 改名：【下周周一日期-下周周五日期】周工作计划.md
 *   4. 智能替换：
 *      - 标题中的日期范围（# 【YYYYMMDD-YYYYMMDD】周工作计划）
 *      - 项目截止日期：旧日期 + 7 天
 *      - 时间标签：保持不变（语义不变）
 *
 * 作者：小伊
 * 日期：2026-08-16
 */

'use strict';

const fs = require('fs');
const path = require('path');

const WEEK_DIR = "${HOME} Files/我的坚果云/03_中传文创/00-工作计划/001周工作计划";
const DAY_DIR = "${HOME} Files/我的坚果云/03_中传文创/00-工作计划/002日工作计划";
const DAY_NAMES = ['周一', '周二', '周三', '周四', '周五'];

// 用户 拍板 2026-08-18:只从已有动作类型库匹配 action,不自动添加新标签
// 用户 之前手写的"已推进"里有"#进展"等不在库标签,用户 会自己改
const EXECUTION_TAGS = ['踏勘', '拜访', '来访', '出差'];
const DOCUMENT_TAGS = ['写方案', '拟协议', '写报告', '调研'];
const TEMPORARY_TAGS = ['沟通', '请示', '跟进', '确认', '等待', '流转'];
const ALL_ACTION_TAGS = [...EXECUTION_TAGS, ...DOCUMENT_TAGS, ...TEMPORARY_TAGS];
const ACTION_TAG_REGEX = new RegExp('#(' + ALL_ACTION_TAGS.join('|') + ')');

function isActionTag(tag) {
  return ALL_ACTION_TAGS.includes(tag);
}

function pad2(n) {
  return String(n).padStart(2, '0');
}

function fmtDate(d) {
  return `${d.getFullYear()}${pad2(d.getMonth() + 1)}${pad2(d.getDate())}`;
}

function addDays(yyyymmdd, days) {
  const y = parseInt(yyyymmdd.slice(0, 4));
  const m = parseInt(yyyymmdd.slice(4, 6)) - 1;
  const d = parseInt(yyyymmdd.slice(6, 8));
  const date = new Date(y, m, d);
  date.setDate(date.getDate() + days);
  return fmtDate(date);
}


// ============================================================
// TYPES_SECTION: 周计划固定的 "## 类型说明" 章节
//   来源:用户 拍板(2026-08-15/16)
//   内容:项目类型(12 个) + 动作类型(14 个,分执行型/文档型/临时型)
//   注意:任何周计划文件前面必须有这个章节,便于读者理解标签
// ============================================================
const TYPES_SECTION = `## 类型说明

### 项目类型（写在任务标题下 \`#xxx\`）

| # 标签 | 含义 |
|---|---|
| \`#设备投放\` | 智能设备投放 |
| \`#合作共建\` | 双方合作共建 |
| \`#产业导入\` | 产业基地 |
| \`#活动举办\` | 大会、活动 |
| \`#全域治理\` | 全域土地治理 |
| \`#城市更新\` | 城市更新 |
| \`#文创开发\` | 文创产品 |
| \`#乡村振兴\` | 乡村项目 |
| \`#商业运营\` | 商业运营 |
| \`#视频短剧\` | 视频短剧/漫剧 |
| \`#供应商合作\` | 与供应商合作 |
| \`#景区运营\` | 演艺、活动、招商运维、舞台演出 |

### 动作类型（写在下一步分支后 \`#xxx\`）

**🌍 执行型**（占用整天/半天，1 天最多 2 个）
- \`#踏勘\` 现场勘测
- \`#拜访\` 去别人场地面谈
- \`#来访\` 到我们场地面谈
- \`#出差\` 异地出行

**📝 文档型**（占用 1-3 小时，1 天最多 2 个）
- \`#写方案\` 方案撰写
- \`#拟协议\` 协议起草
- \`#写报告\` 报告撰写
- \`#调研\` 线上调研（搜集情报、找知名人、写调研报告）

**⚡ 临时型**（占用 30 分钟以内，1 天可多任务）
- \`#沟通\` 微信/邮件/电话
- \`#请示\` 请示上级
- \`#跟进\` 跟进进度
- \`#确认\` 信息确认
- \`#等待\` 等待对方回复
- \`#流转\` 内部流程流转

`;


// ============================================================
// checkbox 提取工具函数(用户 拍板 2026-08-18)
// ============================================================

function extractCompletedSubSteps(weekStart) {
  const result = new Map();
  if (!fs.existsSync(DAY_DIR)) return result;

  const dates = [
    { date: weekStart, day: '周一' },
    { date: addDays(weekStart, 1), day: '周二' },
    { date: addDays(weekStart, 2), day: '周三' },
    { date: addDays(weekStart, 3), day: '周四' },
    { date: addDays(weekStart, 4), day: '周五' }
  ];

  for (const { date, day } of dates) {
    const dayFile = path.join(DAY_DIR, '【' + date + '】' + day + '工作计划.md');
    if (!fs.existsSync(dayFile)) continue;
    const dayContent = fs.readFileSync(dayFile, 'utf-8');

    const blocks = dayContent.split(/(?=### )/);
    for (const block of blocks) {
      const bm = block.match(/### (\d+)\./);
      if (!bm) continue;
      const taskId = parseInt(bm[1]);

      const checkedRegex = /^\s*-\s+\[x\]\s+(.+?)\s*$/gm;
      let cm;
      while ((cm = checkedRegex.exec(block)) !== null) {
        const raw = cm[1].trim();
        const actionMatch = raw.match(ACTION_TAG_REGEX);
        const action = actionMatch ? actionMatch[1] : '';
        const text = raw.replace(/`?#[\u4e00-\u9fffA-Za-z]+`?\s*/g, '').trim();
        const fingerprint = text + '|' + action;
        if (!result.has(taskId)) result.set(taskId, []);
        result.get(taskId).push({ day, text, action, fingerprint });
      }
    }
  }
  return result;
}

function mergeCompletedIntoProgress(weekContent, completedByTask) {
  if (completedByTask.size === 0) {
    return { content: weekContent, merged: 0 };
  }

  // 收集已有 fingerprint（用于去重）
  const existing = new Set();
  const taskBlocks0 = weekContent.split(/(?=### )/);
  for (const block of taskBlocks0) {
    const bm = block.match(/### (\d+)\./);
    if (!bm) continue;
    const progressMatch = block.match(/- \*\*已推进\*\*[：:]\n?([\s\S]*?)(?=- \*\*下一步\*\*[：:]|$)/);
    if (progressMatch) {
      const body = progressMatch[1] || '';
      const lineRegex = /^\s*-\s+(.+?)(?:\s+`#([\u4e00-\u9fffA-Za-z]+)`)?\s*$/gm;
      let lm;
      while ((lm = lineRegex.exec(body)) !== null) {
        existing.add((lm[1] || '').trim() + '|' + (lm[2] || ''));
      }
    }
  }

  let mergedCount = 0;

  // 策略：逐任务块替换
  // 1. 把 weekContent 按 ### 分割成数组
  // 2. 遍历每个任务块，找到对应的 completedByTask 条目
  // 3. 在块内做精确替换
  // 4. 重新组合

  // 分割：按 '### ' 切分任务块（修复原全局正则漏掉任务14 的 bug）
  const allTaskMatches = [];
  const taskBlocks = weekContent.split(/(?=### )/);
  let searchOffset = 0;
  for (const tb of taskBlocks) {
    const bm = tb.match(/### (\d+)\./);
    if (!bm) continue;
    const taskId = parseInt(bm[1]);
    const blockStart = weekContent.indexOf(tb, searchOffset);
    if (blockStart < 0) continue;
    const blockEnd = blockStart + tb.length;
    allTaskMatches.push({ taskId, blockStart, blockEnd, blockContent: tb });
    searchOffset = blockEnd;
  }

  // 从后往前替换（从末尾开始，避免位置偏移问题）
  let newContent = weekContent;
  for (let i = allTaskMatches.length - 1; i >= 0; i--) {
    const { taskId, blockStart, blockEnd, blockContent } = allTaskMatches[i];
    const items = completedByTask.get(taskId);
    if (!items || items.length === 0) continue;

    const newItems = items.filter(it => !existing.has(it.fingerprint));
    if (newItems.length === 0) continue;

    const progressMatch = blockContent.match(/- \*\*已推进\*\*[：:]\n?([\s\S]*?)(?=- \*\*下一步\*\*[：:]|$)/);
    if (!progressMatch) continue;

    // 构建新已推进块
    const progressHeader = progressMatch[0].match(/- \*\*已推进\*\*[：:]/)[0];
    const progressBody = progressMatch[1] || '';
    const bodyTrimmed = progressBody.replace(/[ \t]+\n/, '\n').replace(/\n+$/, '');

    const newLines = newItems.map(function(it) {
      if (it.action && isActionTag(it.action)) return '  - ' + it.text + ' ' + '`#' + it.action + '`';
      return '  - ' + it.text;
    }).join('\n');

    const newProgressBlock = progressHeader + '\n' + (bodyTrimmed ? bodyTrimmed + '\n' + newLines + '\n' : newLines + '\n');

    // 找到 progressMatch[0] 在 blockContent 中的位置，然后替换
    const pmStartInBlock = blockContent.indexOf(progressMatch[0]);
    const pmEndInBlock = pmStartInBlock + progressMatch[0].length;
    const newBlockContent = blockContent.substring(0, pmStartInBlock) + newProgressBlock + blockContent.substring(pmEndInBlock);

    // 替换 newContent 中的这个块
    newContent = newContent.substring(0, blockStart) + newBlockContent + newContent.substring(blockEnd);

    for (const it of newItems) {
      existing.add(it.fingerprint);
      mergedCount++;
    }
  }

  return { content: newContent, merged: mergedCount };
}


function copyNextWeekPlan() {
  // 1. 找到当前周计划文件
  if (!fs.existsSync(WEEK_DIR)) {
    return { success: false, error: 'week_dir_not_found', path: WEEK_DIR };
  }

  const files = fs.readdirSync(WEEK_DIR)
    .filter(f => f.match(/【\d{8}-\d{8}】周工作计划\.md$/))
    .map(f => ({
      name: f,
      path: path.join(WEEK_DIR, f),
      mtime: fs.statSync(path.join(WEEK_DIR, f)).mtimeMs,
      weekRange: f.match(/【(\d{8})-(\d{8})】/)
    }))
    .sort((a, b) => b.mtime - a.mtime);

  if (files.length === 0) {
    return { success: false, error: 'no_week_plan_found' };
  }

  const currentWeek = files[0];
  const currentStart = currentWeek.weekRange[1];
  const currentEnd = currentWeek.weekRange[2];

  // 2. 计算下周日期
  const nextStart = addDays(currentStart, 7);
  const nextEnd = addDays(currentEnd, 7);
  const newFileName = `【${nextStart}-${nextEnd}】周工作计划.md`;
  const newFilePath = path.join(WEEK_DIR, newFileName);

  // 3. 检查下周周计划是否已存在
  if (fs.existsSync(newFilePath)) {
    return {
      success: false,
      error: 'next_week_plan_exists',
      fileName: newFileName,
      path: newFilePath
    };
  }

  // 4. 复制副本
  fs.copyFileSync(currentWeek.path, newFilePath);

  // 5. 智能替换
  let content = fs.readFileSync(newFilePath, 'utf-8');

  // 5-pre. checkbox 提取(用户 拍板 2026-08-18)
  const completed = extractCompletedSubSteps(currentStart);
  const mergeResult = mergeCompletedIntoProgress(content, completed);
  const mergedCurrent = mergeResult.merged;

  if (mergedCurrent > 0) {
    fs.writeFileSync(currentWeek.path, mergeResult.content, 'utf-8');
    content = mergeResult.content;
    console.log('  ✅ 已合并 ' + mergedCurrent + ' 个 checkbox 完成项到当前周计划已推进');
  } else {
    console.log('  ℹ️  本周无新完成项(- [x])');
  }


  // 5a. 替换标题：# 【YYYYMMDD-YYYYMMDD】周工作计划
  const titleRegex = new RegExp(`# 【\\d{8}-\\d{8}】周工作计划`, 'g');
  content = content.replace(titleRegex, `# 【${nextStart}-${nextEnd}】周工作计划`);

  // 5a-pre. 确保 "## 类型说明" 章节存在(用户 拍板:周计划前面要有标签解释)
  //   如果原文件没有,从 TYPES_SECTION 模板自动补上
  if (!content.includes('## 类型说明')) {
    content = TYPES_SECTION + content;
  }

  // 5b. 替换项目截止日期：原日期 + 7 天
  content = content.replace(/\[截止:(\d{8})\]/g, (match, oldDate) => {
    const newDate = addDays(oldDate, 7);
    return `[截止:${newDate}]`;
  });

  // 5c. 时间标签保持不变

  fs.writeFileSync(newFilePath, content, 'utf-8');

  return {
    success: true,
    mergedCompletedCount: mergedCurrent,
    from: {
      name: currentWeek.name,
      path: currentWeek.path,
      start: currentStart,
      end: currentEnd
    },
    to: {
      name: newFileName,
      path: newFilePath,
      start: nextStart,
      end: nextEnd
    }
  };
}

if (require.main === module) {
  const result = copyNextWeekPlan();
  console.log(JSON.stringify(result, null, 2));
  if (!result.success) {
    process.exit(1);
  }
}

module.exports = { copyNextWeekPlan, extractCompletedSubSteps, mergeCompletedIntoProgress };

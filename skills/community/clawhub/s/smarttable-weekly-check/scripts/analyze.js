/**
 * 周报分析脚本
 * 用法: node scripts/analyze.js
 * 
 * 从 smartsheet_data/w1.json ~ w5.json 读取各周提取数据，
 * 按 4 条规则检查，生成 Markdown 报告。
 */

const fs = require('fs');
const path = require('path');

// ====== 配置 ======
const DATA_DIR = path.join(__dirname, '..', 'smartsheet_data');
const OUTPUT_FILE = path.join(DATA_DIR, 'report.md');

// ====== 工具函数 ======

function countChars(text) {
  return (text.match(/[\u4e00-\u9fff\w]/g) || []).length;
}

function countTasks(text) {
  if (!text || text === '休假' || /待领导安排工作/.test(text)) return 0;
  return (text.match(/\d+[.、）)]/g) || []).length || 1;
}

// ====== 加载数据 ======

// 自动扫描 w1.json, w2.json, ... 直到文件不存在
const weeks = [];
for (let i = 1; ; i++) {
  const filePath = path.join(DATA_DIR, `w${i}.json`);
  if (!fs.existsSync(filePath)) break;
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  weeks.push(data);
}

if (weeks.length === 0) {
  console.error('错误: smartsheet_data/ 目录下没有找到任何 w*.json 文件');
  console.error('请先运行数据提取步骤（参见 SKILL.md）。');
  process.exit(1);
}

console.log(`已加载 ${weeks.length} 周数据:`);
weeks.forEach((w, i) => console.log(`  W${i + 1}: ${w.title} (${w.people.length}人)`));

// ====== 构建人员-周期矩阵 ======

const personMap = {};
weeks.forEach((week, wi) => {
  const label = `W${wi + 1}`;
  week.people.forEach(p => {
    // 忽略姓名为空或无法解析的行（空行/未填写成员）
    if (!p.name || p.name === '?' || p.name.trim() === '') return;
    if (!personMap[p.name]) personMap[p.name] = {};
    personMap[p.name][label] = { work: p.work, plan: p.plan };
  });
});

// ====== 执行检查 ======

const results = [];
const weekLabels = weeks.map((_, i) => `W${i + 1}`);
const latestLabel = weekLabels[weekLabels.length - 1];

for (const [name, personWeeks] of Object.entries(personMap)) {
  // 忽略姓名为空或 '?' 的行
  if (!name || name === '?' || name.trim() === '') continue;
  const allWorks = {};
  const allPlans = {};

  weekLabels.forEach(l => {
    if (personWeeks[l]) {
      allWorks[l] = personWeeks[l].work;
      allPlans[l] = personWeeks[l].plan;
    }
  });

  const latest = personWeeks[latestLabel];
  const issues = [];

  // 规则3: 字符数 < 50
  const workChars = countChars(latest?.work || '');
  if (workChars < 50) {
    if (!latest?.work || latest.work === '休假' || /待领导安排工作/.test(latest.work)) {
      issues.push({ rule: '规则3', level: '⚠️', detail: `文字数=${workChars}（休假/待安排，不计数）` });
    } else {
      issues.push({ rule: '规则3', level: '❌', detail: `本周工作内容仅 ${workChars} 字，<50字不合格` });
    }
  }

  // 规则4: 必填项
  if (!latest?.work || latest.work.trim() === '') {
    issues.push({ rule: '规则4', level: '❌', detail: '本周工作内容为空' });
  }
  if (!latest?.plan || latest.plan.trim() === '') {
    issues.push({ rule: '规则4', level: '❌', detail: '下周工作计划为空' });
  }

  // 规则1: 内容变动
  const uniqueWorks = new Set(Object.values(allWorks).filter(w => w));
  if (uniqueWorks.size <= 1 && Object.keys(allWorks).length >= 3 && !/待领导安排工作/.test(latest?.work || '')) {
    issues.push({ rule: '规则1', level: '⚠️', detail: `多周工作内容完全相同（${Object.keys(allWorks).join(',')}）` });
  }

  // 规则2: 描述清晰度
  if (latest?.work && latest.work.trim() !== '' && latest.work !== '休假' && !/待领导安排工作/.test(latest.work)) {
    const taskCount = countTasks(latest.work);
    if (taskCount < 3) {
      issues.push({ rule: '规则2', level: '⚠️', detail: `本周任务仅 ${taskCount} 条，可能未支撑一周工作量` });
    }
  }

  // 规则4附加: 计划重复
  const uniquePlans = new Set(Object.values(allPlans).filter(p => p));
  if (uniquePlans.size <= 1 && Object.keys(allPlans).length >= 4 && !/待领导安排工作/.test(latest?.plan || '')) {
    issues.push({ rule: '规则4(计划)', level: '❌', detail: `近${Object.keys(allPlans).length}周下周工作计划完全相同` });
  }

  // 判定
  let status = '✅';
  if (issues.some(i => i.level === '❌')) status = '❌';
  else if (issues.some(i => i.level === '⚠️')) status = '⚠️';

  results.push({ name, status, works: allWorks, plans: allPlans, workChars, issues });
}

// 排序
const order = { '❌': 0, '⚠️': 1, '✅': 2 };
results.sort((a, b) => order[a.status] - order[b.status] || a.name.localeCompare(b.name, 'zh'));

// 统计
const stats = { '❌': 0, '⚠️': 0, '✅': 0 };
results.forEach(r => stats[r.status]++);

// ====== 生成报告 ======

const now = new Date().toISOString().replace('T', ' ').substring(0, 16);
const periodDesc = weeks.map((w, i) => `W${i + 1}(${w.title})`).join(' → ');

let report = `# 📊 周报检查报告

> 检查时间：${now}
> 检查周期：${periodDesc}，共${weeks.length}周
> 检查人数：${results.length}人

## 总体概览

| 状态 | 人数 |
|------|------|
| ✅ 合格 | ${stats['✅']} |
| ⚠️ 需关注 | ${stats['⚠️']} |
| ❌ 不合格 | ${stats['❌']} |

`;

// ❌
const fail = results.filter(r => r.status === '❌');
if (fail.length > 0) {
  report += '## ❌ 不合格人员\n\n';
  fail.forEach(r => {
    report += `### ${r.name}\n\n`;
    report += '| 规则 | 问题 |\n|------|------|\n';
    r.issues.filter(i => i.level === '❌').forEach(i => {
      report += `| ${i.rule} | ${i.detail} |\n`;
    });
    if (r.issues.some(i => i.level === '⚠️')) {
      r.issues.filter(i => i.level === '⚠️').forEach(i => {
        report += `| ${i.rule} | ${i.detail} |\n`;
      });
    }
    report += '\n**多周数据对比：**\n\n';
    report += '| 周期 | 工作字数 | 本周工作内容（摘要） | 下周计划（摘要） |\n';
    report += '|------|---------|---------------------|-----------------|\n';
    Object.entries(r.works).forEach(([k, v]) => {
      const wChars = countChars(v || '');
      const wSummary = (v || '(空)').substring(0, 60).replace(/\n/g, ' ');
      const pSummary = (r.plans[k] || '(空)').substring(0, 50).replace(/\n/g, ' ');
      report += `| ${k} | ${wChars} | ${wSummary}... | ${pSummary}... |\n`;
    });
    report += '\n';
  });
}

// ⚠️
const warn = results.filter(r => r.status === '⚠️');
if (warn.length > 0) {
  report += '## ⚠️ 需关注人员\n\n';
  warn.forEach(r => {
    report += `### ${r.name}\n\n`;
    r.issues.forEach(i => {
      report += `- **${i.rule}**：${i.detail}\n`;
    });
    report += '\n';
  });
}

// ✅
const ok = results.filter(r => r.status === '✅');
if (ok.length > 0) {
  report += '## ✅ 合格人员\n\n';
  report += ok.map(r => r.name).join('、');
  report += '\n';
}

// 详细汇总表
report += '\n## 详细汇总\n\n';
report += `| 姓名 | 状态 | ${latestLabel}字数 | ${latestLabel}任务数 | 问题摘要 |\n`;
report += '|------|------|--------|---------|----------|\n';
results.forEach(r => {
  const issueSummary = r.issues.map(i => `${i.rule}: ${i.detail}`).join('; ');
  const taskCount = countTasks(r.works[latestLabel] || '');
  report += `| ${r.name} | ${r.status} | ${r.workChars} | ${taskCount} | ${issueSummary || '-'} |\n`;
});

// 输出
console.log(report);
fs.writeFileSync(OUTPUT_FILE, report, 'utf8');
console.log(`\n--- 报告已保存到 ${OUTPUT_FILE} ---`);
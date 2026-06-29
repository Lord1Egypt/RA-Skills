/**
 * 项目周报汇总脚本
 * 按项目维度汇总各成员工作内容，多人同项目合并
 * 用法: node scripts/project_summary.js [weekIdx]
 *   weekIdx: 1~N，默认取最新一周
 */
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'smartsheet_data');

// 加载周数据
const weeks = [];
for (let i = 1; i <= 5; i++) {
  const fp = path.join(DATA_DIR, `w${i}.json`);
  if (!fs.existsSync(fp)) break;
  weeks.push(JSON.parse(fs.readFileSync(fp, 'utf8')));
}
if (weeks.length === 0) { console.error('无数据'); process.exit(1); }

const weekIdx = parseInt(process.argv[2]) || weeks.length;
const week = weeks[weekIdx - 1];
if (!week) { console.error(`W${weekIdx} 不存在`); process.exit(1); }

console.log(`汇总周期：${week.title} (W${weekIdx})\n`);

// 解析项目：从 work/plan 中提取【项目名】段落
function parseProjects(text) {
  if (!text || !text.trim()) return [];
  const projects = [];
  const lines = text.split('\n');
  let currentProject = null;
  let currentTasks = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    // 匹配【项目名】开头的行（忽略前导符号如 . 、- 等）
    const match = trimmed.match(/^[.、\-\s]*【(.+?)】\s*(.*)$/);
    if (match) {
      // 保存上一个项目
      if (currentProject) {
        projects.push({ name: currentProject, tasks: currentTasks.join('\n') });
      }
      currentProject = match[1];
      currentTasks = [];
      // 【项目名】后面可能紧跟内容
      if (match[2] && match[2].trim()) currentTasks.push(match[2].trim());
    } else if (currentProject) {
      currentTasks.push(trimmed);
    } else {
      // 没有项目名的独立内容，归入"其他"
      if (!currentProject) {
        currentProject = '其他';
        currentTasks = [];
      }
      currentTasks.push(trimmed);
    }
  }
  if (currentProject) {
    projects.push({ name: currentProject, tasks: currentTasks.join('\n') });
  }
  return projects;
}

// 按项目分组汇总
const projectMap = {}; // projectName -> [{name, tasks}]

week.people.forEach(p => {
  if (!p.name || p.name === '?' || !p.name.trim()) return;
  const projects = parseProjects(p.work);
  projects.forEach(proj => {
    if (!projectMap[proj.name]) projectMap[proj.name] = [];
    projectMap[proj.name].push({ name: p.name, tasks: proj.tasks });
  });
});

// 按参与人数排序（人多的大项目排前面）
const sortedProjects = Object.entries(projectMap)
  .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], 'zh'));

// 生成 Markdown 报告
let report = `# 📋 项目周报汇总\n\n`;
report += `> 汇总周期：${week.title}\n`;
report += `> 汇总项目：${sortedProjects.length} 个\n`;
report += `> 参与人数：${week.people.filter(p => p.name && p.name !== '?' && p.name.trim()).length} 人\n\n`;

report += `## 项目概览\n\n`;
report += `| 项目 | 参与人数 | 成员 |\n`;
report += `|------|---------|------|\n`;
sortedProjects.forEach(([proj, members]) => {
  report += `| ${proj} | ${members.length} | ${members.map(m => m.name).join('、')} |\n`;
});

report += `\n---\n\n`;

sortedProjects.forEach(([proj, members]) => {
  report += `## ${proj}\n\n`;
  report += `**参与人员（${members.length}人）：** ${members.map(m => m.name).join('、')}\n\n`;
  members.forEach(m => {
    report += `### ${m.name}\n\n`;
    report += `${m.tasks}\n\n`;
  });
});

// 输出
console.log(report);

const outFile = path.join(DATA_DIR, 'project_summary.md');
fs.writeFileSync(outFile, report, 'utf8');
console.log(`\n--- 汇总报告已保存到 ${outFile} ---`);

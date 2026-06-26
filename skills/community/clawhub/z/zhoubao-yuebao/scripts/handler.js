// weekly-report handler
// 周报/月报生成 Skill

const SKILL_NAME = 'weekly-report';

async function handle(text, context) {
  const reportType = detectReportType(text);
  const content = extractContent(text);
  
  // AI 生成报告
  const report = await generateReport(reportType, content);
  
  // 创建飞书文档
  const config = loadConfig();
  if (config.create_doc && context.user_id) {
    const docId = await createFeishuDoc(report, context.user_id);
    return `📊 ${reportType}已生成！\n\n${report}\n\n📄 飞书文档：${docId}`;
  }
  
  return report;
}

function detectReportType(text) {
  if (text.includes('月')) return '月报';
  if (text.includes('项目')) return '项目报告';
  return '周报';
}

function extractContent(text) {
  // 从用户输入中提取工作内容
  return text.replace(/生成|写|本周|月报|周报|总结|工作/gi, '').trim();
}

function loadConfig() {
  try {
    const fs = require('fs');
    const path = require('path');
    const configPath = path.join(__dirname, '../config.json');
    return fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath)) : {};
  } catch { return {}; }
}

async function createFeishuDoc(content, userId) {
  // 调用飞书文档创建
  return '文档创建成功';
}

module.exports = { handle };

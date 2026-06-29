const fs = require('fs');
const path = require('path');

function toCSV(rows) {
  if (!rows || rows.length === 0) return '';
  const headers = Object.keys(rows[0]);
  const lines = [headers.join(',')];
  rows.forEach(r => {
    const line = headers.map(h => {
      const v = r[h] === undefined ? '' : String(r[h]).replace(/"/g, '""');
      return `"${v}"`;
    }).join(',');
    lines.push(line);
  });
  return lines.join('\n');
}

function makeReports(rows, config) {
  const outDir = path.resolve(process.cwd(), config.outputDir || process.env.REPORT_DIR || 'reports');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const date = new Date().toISOString().slice(0, 10);
  const prefix = config.reportFilenamePrefix || 'report';
  const csvPath = path.join(outDir, `${prefix}-${date}.csv`);
  const mdPath = path.join(outDir, `${prefix}-${date}.md`);

  const csv = toCSV(rows);
  fs.writeFileSync(csvPath, csv, 'utf8');

  const count = rows.length;
  let md = `# 每日报告 - ${date}\n\n`;
  md += `- 抓取地址: ${config.targetUrl}\n`;
  md += `- 记录数: ${count}\n\n`;

  if (count > 0) {
    md += '## 样例行（前 5 行）\n\n';
    const sample = rows.slice(0, 5);
    md += '```json\n' + JSON.stringify(sample, null, 2) + '\n```\n\n';
  } else {
    md += '未抓到表格数据，可能需要更新选择器或先人工登录后再运行。\n\n';
    md += '页面预览或需进一步分析。\n\n';
  }

  if (Array.isArray(config.numericFields) && config.numericFields.length > 0 && count > 0) {
    md += '## 数值字段汇总\n\n';
    config.numericFields.forEach(field => {
      const vals = rows.map(r => {
        const s = (r[field] || '').replace(/[^\d\.\-]/g, '');
        const n = parseFloat(s);
        return isNaN(n) ? 0 : n;
      });
      const sum = vals.reduce((a, b) => a + b, 0);
      md += `- ${field}: 合计 = ${sum}\n`;
    });
    md += '\n';
  }

  fs.writeFileSync(mdPath, md, 'utf8');

  return { csvPath, mdPath };
}

module.exports = { makeReports };

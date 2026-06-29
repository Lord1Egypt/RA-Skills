#!/usr/bin/env node
/**
 * ux-usability-auditor — generate_report.js
 *
 * Generates a structured usability audit report from inspection results
 * and a Markdown checklist file.
 *
 * Usage:
 *   node scripts/generate_report.js path/to/config.json [--checklist custom.md]
 *
 * Output:
 *   results/usability_audit_report.md
 */

const fs = require('fs');
const path = require('path');

// ── Helpers ───────────────────────────────────────────────────────────────────

function log(msg) {
  console.log(`[report] ${msg}`);
}

function loadJSON(p) {
  if (!fs.existsSync(p)) throw new Error(`File not found: ${p}`);
  return JSON.parse(fs.readFileSync(p, 'utf-8'));
}

function loadChecklist(checklistPath) {
  if (!fs.existsSync(checklistPath)) {
    log(`WARNING: Checklist not found at ${checklistPath}, skipping checklist evaluation`);
    return [];
  }
  const content = fs.readFileSync(checklistPath, 'utf-8');
  const categories = [];
  let currentCategory = null;

  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Category: ## 1. Navigation & Page Layout
    const catMatch = line.match(/^##\s+(\d+)\.\s+(.+)/);
    if (catMatch) {
      currentCategory = { index: catMatch[1], name: catMatch[2].trim(), items: [] };
      categories.push(currentCategory);
      continue;
    }

    // Item: ### 1.1 Menu Hierarchy Reasonableness
    const itemMatch = line.match(/^###\s+[\d.]+\s+(.+)/);
    if (itemMatch && currentCategory) {
      const itemName = itemMatch[1].trim();
      // Read next few lines for standard, method, severity
      let standard = '';
      let severity = '';
      for (let j = i + 1; j < Math.min(i + 6, lines.length); j++) {
        const l = lines[j];
        const stdMatch = l.match(/^\s*[-\*]\s+\*\*Standard\*\*:?\s*(.+)/i);
        if (stdMatch) { standard = stdMatch[1].trim(); }
        const sevMatch = l.match(/^\s*[-\*]\s+\*\*Severity\*\*:?\s*(.+)/i);
        if (sevMatch) { severity = sevMatch[1].trim(); }
      }
      currentCategory.items.push({ name: itemName, standard, severity });
    }
  }
  return categories;
}

// ── Evaluation Logic ──────────────────────────────────────────────────────────

function evaluateItem(item, results) {
  // This is a heuristic evaluation based on UI stats.
  // Each checklist item has specific signals in the inspection data.

  const name = item.name.toLowerCase();
  let finding = '';
;
  let status = '❓ 无法评估'; // default: can't assess

  // 1.1 Menu Hierarchy — check if pages > 50 and all flat
  if (name.includes('menu') || name.includes('层级') || name.includes('hierarchy')) {
    if (results.length > 50) {
      status = '⚠️ 存在问题';
      finding = `系统共发现 ${results.length} 个页面，菜单可能过长，建议检查菜单层级合理性`;
    } else {
      status = '✅ 通过';
      finding = `系统共 ${results.length} 个页面，数量适中`;
    }
  }

  // 1.3 Control zoning — high button/input count suggests clutter
  if (name.includes('control') || name.includes('控件') || name.includes('分区') || name.includes('zoning')) {
    const avgButtons = results.reduce((s, r) => s + (r.buttons || 0), 0) / results.length;
    const avgInputs = results.reduce((s, r) => s + (r.inputs || 0), 0) / results.length;
    if (avgButtons > 20 || avgInputs > 30) {
      status = '⚠️ 存在问题';
      finding = `部分页面按钮数(${avgButtons.toFixed(0)}平均)或输入框数(${avgInputs.toFixed(0)}平均)偏高，可能存在控件分区不明确问题`;
    } else {
      status = '✅ 基本通过';
      finding = `页面控件数量适中（按钮平均${avgButtons.toFixed(0)}个，输入框平均${avgInputs.toFixed(0)}个）`;
    }
  }

  // 1.4 Key info prominence — check breadcrumb and status color (heuristic)
  if (name.includes('visual') || name.includes('视觉') || name.includes('突出') || name.includes('prominence')) {
    const withBreadcrumb = results.filter((r) => r.breadcrumb && r.breadcrumb.length > 0).length;
    if (withBreadcrumb === 0) {
      status = '⚠️ 存在问题';
      finding = '未检测到面包屑导航，用户可能难以感知当前位置；状态字段颜色区分需人工验证';
    } else {
      status = '✅ 部分支持';
      finding = `检测到 ${withBreadcrumb}/${results.length} 页面有面包屑导航`;
    }
  }

  // 1.5 Global search
  if (name.includes('search') || name.includes('搜索') || name.includes('全局')) {
    const withSearch = results.filter((r) => r.searchArea && r.searchArea.length > 0).length;
    if (withSearch === 0) {
      status = '⚠️ 未检测到';
      finding = '未检测到全局搜索框，建议确认是否存在全局搜索功能';
    } else {
      status = '✅ 已检测';
      finding = `在 ${withSearch} 个页面检测到搜索相关元素`;
    }
  }

  // 3.5 Empty state guidance
  if (name.includes('empty') || name.includes('空状态') || name.includes('引导') || name.includes('guidance')) {
    const emptyCount = results.filter((r) => r.emptyState && r.emptyState.length > 0).length;
    const totalEmpty = results.filter((r) => (r.emptyState && r.emptyState.length > 0) || (r.url && r.status === 'ok')).length;
    // Heuristic: if many pages have "no data", check if they have guidance buttons
    const withoutGuidance = results.filter((r) => {
      if (!r.emptyState || r.emptyState.length === 0) return false;
      const hasButton = (r.actionButtons || []).length > 0;
      return !hasButton;
    }).length;

    if (withoutGuidance > 0) {
      status = '⚠️ 存在问题';
      finding = `检测到 ${withoutGuidance} 个空状态页面缺少操作引导按钮，建议增加引导文案和操作入口`;
    } else {
      status = '✅ 通过';
      finding = '空状态页面均有操作引导';
    }
  }

  // 4.1 New user guidance
  if (name.includes('guide') || name.includes('引导') || name.includes('new user') || name.includes('新用户')) {
    status = '❓ 无法评估';
    finding = '需人工验证：首次登录时是否出现引导弹窗或分步指引';
  }

  // 4.2 Help system
  if (name.includes('help') || name.includes('帮助')) {
    status = '❓ 无法评估';
    finding = '需人工验证：系统是否内置帮助中心或?帮助入口';
  }

  // 6.2 High-risk operation confirmation
  if (name.includes('confirm') || name.includes('确认') || name.includes('delete') || name.includes('删除')) {
    status = '❓ 无法评估';
    finding = '需人工验证：点击删除/作废等高危操作按钮时，是否弹出二次确认弹窗';
  }

  return { status, finding };
}

// ── Report Generation ────────────────────────────────────────────────────────

function generateReport(config, results, categories) {
  const lines = [];
  const appName = config.name || 'Web Application';
  const auditDate = new Date().toISOString().split('T')[0];

  // Title
  lines.push(`# ${appName} — Usability Audit Report`);
  lines.push('');
  lines.push(`**Audit Date:** ${auditDate}`);
  lines.push(`**Target URL:** ${config.targetUrl}`);
  lines.push(`**Pages Inspected:** ${results.filter((r) => r.status === 'ok').length} / ${results.length}`);
  lines.push(`**Audit Tool:** ux-usability-auditor (Playwright automated)`);
  lines.push('');

  // Summary table
  lines.push('## Summary');
  lines.push('');
  lines.push('| Category | Total Items | ✅ Pass | ⚠️ Issue | ❓ N/A |');
  lines.push('|----------|-------------|---------|----------|---------|');

  let totalPass = 0, totalIssue = 0, totalNA = 0, totalItems = 0;

  const evaluated = [];

  categories.forEach((cat) => {
    let catPass = 0, catIssue = 0, catNA = 0;
    const catResults = [];

    cat.items.forEach((item) => {
      const ev = evaluateItem(item, results);
      catResults.push({ item, ...ev });
      if (ev.status.includes('✅')) catPass++;
      else if (ev.status.includes('⚠️')) catIssue++;
      else catNA++;
    });

    totalPass += catPass;
    totalIssue += catIssue;
    totalNA += catNA;
    totalItems += cat.items.length;

    lines.push(`| ${cat.name} | ${cat.items.length} | ${catPass} | ${catIssue} | ${catNA} |`);
    evaluated.push({ category: cat.name, results: catResults });
  });

  lines.push(`| **Total** | **${totalItems}** | **${totalPass}** | **${totalIssue}** | **${totalNA}** |`);
  lines.push('');

  // Priority issue list
  const allIssues = [];
  evaluated.forEach((cat) => {
    cat.results.forEach((r) => {
      if (r.status.includes('⚠️')) {
        allIssues.push({
          category: cat.category,
          item: r.item.name,
          severity: r.item.severity || 'P2',
          finding: r.finding,
        });
      }
    });
  });

  if (allIssues.length > 0) {
    lines.push('## Priority Issue List');
    lines.push('');
    const severityOrder = { P0: 0, P1: 1, P2: 2 };
    allIssues
      .sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity])
      .forEach((issue) => {
        const icon = issue.severity === 'P0' ? '🔴' : issue.severity === 'P1' ? '🟡' : '🟢';
        lines.push(`### ${icon} ${issue.severity} — ${issue.item}`);
        lines.push(`**Category:** ${issue.category}`);
        lines.push(`**Finding:** ${issue.finding}`);
        lines.push('');
      });
  }

  // Detailed findings per category
  lines.push('## Detailed Findings');
  lines.push('');

  evaluated.forEach((cat) => {
    lines.push(`### ${cat.category}`);
    lines.push('');
    cat.results.forEach((r) => {
      lines.push(`**${r.item.name}**`);
      lines.push(`- Status: ${r.status}`);
      lines.push(`- Standard: ${r.item.standard || 'N/A'}`);
      lines.push(`- Finding: ${r.finding}`);
      lines.push('');
    });
  });

  // UI Stats Summary
  lines.push('## UI Statistics Summary');
  lines.push('');
  lines.push('| Page | Buttons | Inputs | Tables | Empty State | Breadcrumb |');
  lines.push('|------|---------|--------|--------|-------------|------------|');

  results.filter((r) => r.status === 'ok').forEach((r) => {
    const pg = (r.page || '').substring(0, 20);
    lines.push(`| ${pg} | ${r.buttons || 0} | ${r.inputs || 0} | ${r.tables || 0} | ${r.emptyState ? 'Yes' : 'No'} | ${r.breadcrumb ? 'Yes' : 'No'} |`);
  });

  lines.push('');
  lines.push('---');
  lines.push(`*Report generated by ux-usability-auditor on ${auditDate}*`);

  return lines.join('\n');
}

// ── Entry Point ────────────────────────────────────────────────────────────────

async function main() {
  let configPath = null;
  let checklistPath = null;

  // Parse args
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--checklist' && args[i + 1]) {
      checklistPath = args[i + 1];
      i++;
    } else if (!args[i].startsWith('--')) {
      configPath = args[i];
    }
  }

  if (!configPath) {
    console.error('Usage: node generate_report.js path/to/config.json [--checklist custom.md]');
    process.exit(1);
  }

  const config = loadJSON(configPath);
  const outputDir = config.outputDir || './results';

  // Resolve checklist path
  if (!checklistPath) {
    checklistPath = config.checklist || path.join(__dirname, '../references/checklist-default.md');
  }
  if (!path.isAbsolute(checklistPath)) {
    checklistPath = path.resolve(process.cwd(), checklistPath);
  }

  log(`Loading checklist: ${checklistPath}`);
  const categories = loadChecklist(checklistPath);
  log(`Loaded ${categories.length} categories, ${categories.reduce((s, c) => s + c.items.length, 0)} checklist items`);

  // Load inspection results
  const resultsPath = path.join(outputDir, 'inspection_results.json');
  const results = loadJSON(resultsPath);
  log(`Loaded ${results.length} page inspection results`);

  // Generate report
  const reportMd = generateReport(config, results, categories);
  const reportPath = path.join(outputDir, 'usability_audit_report.md');
  fs.writeFileSync(reportPath, reportMd);
  log(`Report written to ${reportPath}`);

  console.log(`\n✅ Report generated: ${reportPath}`);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});

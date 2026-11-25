#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { runGeoCheck, ENGINE_VERSION } = require('../lib/engine');

const C = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  blue: '\x1b[34m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m'
};

function printHelp() {
  console.log(`
${C.bold}${C.cyan}StepOneAI GEO Check v${ENGINE_VERSION}${C.reset} — 免费开源官网 AI 搜索体检工具 (6 维度 × 28 项真机检测)

用法:
  npx stepone-geo-check <url> [选项]

选项:
  --json              输出结构化 JSON（适合 CI/CD 或 AI Agent 调用）
  --html <file>       导出本地炫酷可视化 HTML 体检报告
  --fix-out <dir>     自动导出定制修复文件 (llms.txt / robots.txt / schema-jsonld.html)
  -h, --help          显示帮助信息

在线炫酷可视化版: https://www.steponeai.com/geo-check
Powered by 基智 GEO · 北京基智科技有限公司 (StepOneAI)
`);
}

function renderBar(pct, width = 20) {
  const filled = Math.round((Math.max(0, Math.min(100, pct)) / 100) * width);
  return '█'.repeat(filled) + '░'.repeat(Math.max(0, width - filled));
}

function renderStandaloneHtml(r) {
  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const rows = r.checks.map(c => `
    <tr style="border-bottom:1px solid #1E293B;">
      <td style="padding:10px;">${c.status === 'pass' ? '✅ 通过' : (c.status === 'warn' ? '⚠️ 待优化' : '❌ 缺失')}</td>
      <td style="padding:10px;font-weight:700;">${esc(c.title)}</td>
      <td style="padding:10px;">${c.earnedPoints}/${c.maxPoints}</td>
      <td style="padding:10px;color:#CBD5E1;">${esc(c.evidence)}${c.status !== 'pass' ? '<br/><span style="color:#6EE7B7;">建议：' + esc(c.fixAdvice) + '</span>' : ''}</td>
    </tr>`).join('');
  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"/><title>${r.totalScore}分 · ${esc(r.hostname)} GEO 体检报告 | StepOneAI</title>
  <style>body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;background:#050C1D;color:#F8FAFC;margin:0;padding:28px;}
  .wrap{max-width:1020px;margin:0 auto;}.card{background:#0F1930;border:1px solid rgba(56,189,248,.22);border-radius:16px;padding:22px;margin-bottom:18px;}
  table{width:100%;border-collapse:collapse;font-size:13px;}th{text-align:left;padding:10px;color:#93C5FD;background:rgba(1,109,255,.15);}
  pre{background:#020617;padding:14px;border-radius:10px;overflow-x:auto;font-size:12px;color:#E2E8F0;}</style></head>
  <body><div class="wrap">
    <div class="card"><h1>${esc(r.hostname)} · 官网 AI 搜索体检报告 (${r.totalScore}/100 · ${esc(r.grade)} 级)</h1>
      <p style="color:#94A3B8;">网址：${esc(r.finalUrl)} ｜ 耗时：${r.durationMs}ms ｜ 通过 ${r.summaryCounts.pass} / 待优化 ${r.summaryCounts.warn} / 缺失 ${r.summaryCounts.fail}</p>
      <p style="color:#38BDF8;">在线版与完整雷达图：<a style="color:#60A5FA;" href="https://www.steponeai.com/geo-check">https://www.steponeai.com/geo-check</a></p>
    </div>
    <div class="card"><h2>28 项实测明细</h2><table><thead><tr><th>状态</th><th>指标</th><th>得分</th><th>实测证据与建议</th></tr></thead><tbody>${rows}</tbody></table></div>
    <div class="card"><h2>定制 /llms.txt 骨架</h2><pre>${esc(r.snippets.llmsTxt)}</pre><h2>定制 /robots.txt</h2><pre>${esc(r.snippets.robotsTxt)}</pre><h2>定制 JSON-LD</h2><pre>${esc(r.snippets.jsonLd)}</pre></div>
  </div></body></html>`;
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length || args.includes('-h') || args.includes('--help')) {
    printHelp();
    process.exit(0);
  }

  let targetUrl = '';
  let jsonMode = false;
  let htmlOut = '';
  let fixOutDir = '';

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--json') jsonMode = true;
    else if (a === '--html') htmlOut = args[++i] || 'geo-report.html';
    else if (a === '--fix-out') fixOutDir = args[++i] || './geo-fixes';
    else if (!a.startsWith('-')) targetUrl = a;
  }

  if (!targetUrl) {
    console.error('Error: 请提供要检测的官网网址');
    process.exit(1);
  }

  if (!jsonMode) {
    console.log(`${C.cyan}🔍 正在实时体检 ${targetUrl}（纯代码 0 Token 消耗，6 大维度 × 28 项真实探测）...${C.reset}`);
  }

  try {
    const res = await runGeoCheck(targetUrl);

    if (htmlOut) {
      const absHtml = path.resolve(htmlOut);
      fs.writeFileSync(absHtml, renderStandaloneHtml(res), 'utf8');
      if (!jsonMode) console.log(`${C.green}✓ HTML 报告已保存至: ${absHtml}${C.reset}`);
    }
    if (fixOutDir) {
      const absDir = path.resolve(fixOutDir);
      fs.mkdirSync(absDir, { recursive: true });
      fs.writeFileSync(path.join(absDir, 'llms.txt'), res.snippets.llmsTxt, 'utf8');
      fs.writeFileSync(path.join(absDir, 'robots.txt'), res.snippets.robotsTxt, 'utf8');
      fs.writeFileSync(path.join(absDir, 'schema-jsonld.html'), res.snippets.jsonLd, 'utf8');
      if (!jsonMode) console.log(`${C.green}✓ 3 套定制修复代码已导出至: ${absDir}${C.reset}`);
    }

    if (jsonMode) {
      console.log(JSON.stringify(res, null, 2));
      return;
    }

    const gradeColor = res.totalScore >= 80 ? C.green : (res.totalScore >= 60 ? C.yellow : C.red);
    console.log(`\n${C.bold}══════════════════════════════════════════════════════════${C.reset}`);
    console.log(`  官网: ${C.bold}${res.finalUrl}${C.reset}`);
    console.log(`  综合得分: ${gradeColor}${C.bold}${res.totalScore} / 100  (${res.grade} 级 · ${res.gradeLabel})${C.reset}`);
    console.log(`  检测结果: ${C.green}✓ 通过 ${res.summaryCounts.pass}${C.reset}  ${C.yellow}⚠ 待优化 ${res.summaryCounts.warn}${C.reset}  ${C.red}✕ 缺失 ${res.summaryCounts.fail}${C.reset}  (${res.durationMs}ms)`);
    console.log(`${C.bold}══════════════════════════════════════════════════════════${C.reset}\n`);

    console.log(`${C.bold}📊 六维能力分布:${C.reset}`);
    for (const d of res.dimensions) {
      const col = d.pct >= 80 ? C.green : (d.pct >= 50 ? C.yellow : C.red);
      console.log(`  ${d.name.padEnd(10, '　')} ${col}${renderBar(d.pct)}${C.reset}  ${String(d.earned).padStart(2)}/${d.max} (${d.pct}%)`);
    }

    console.log(`\n${C.bold}🤖 10 大 AI 与搜索引擎爬虫准入:${C.reset}`);
    const botLine = res.botMatrix.map(b => `${b.allowed ? C.green + '●' : C.red + '✕'} ${b.label}(${b.id})${C.reset}`).join('  ');
    console.log('  ' + botLine);

    if (res.topIssues.length) {
      console.log(`\n${C.bold}🚨 优先修复的高危扣分项:${C.reset}`);
      res.topIssues.forEach((it, i) => {
        console.log(`  ${C.red}${i + 1}. ${it.title} (-${it.lostPoints}分)${C.reset}`);
        console.log(`     ${C.dim}实测证据: ${it.evidence}${C.reset}`);
        console.log(`     ${C.cyan}整改建议: ${it.fixAdvice}${C.reset}`);
      });
    }

    console.log(`\n${C.dim}💡 在线雷达图体检 & 获取全案 GEO 提升方案: https://www.steponeai.com/geo-check${C.reset}`);
    console.log(`${C.dim}   Powered by 基智 GEO · 北京基智科技有限公司 (https://www.steponeai.com)${C.reset}\n`);
  } catch (err) {
    console.error(`${C.red}✕ 检测失败: ${err.message}${C.reset}`);
    process.exit(1);
  }
}

main();

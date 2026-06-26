#!/usr/bin/env node
/**
 * risk-sentiment-scanner 核心脚本
 * 输入: 企业名称列表（字符串，每行一个）
 * 输出: 结构化 JSON 风险报告
 *
 * 用法:
 *   node scan.js "蚂蚁集团\n贵州茅台\n碧桂园"
 *   node scan.js --file companies.txt
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = join(__dirname, '../reports');
mkdirSync(OUTPUT_DIR, { recursive: true });

// ── 风险评分模型 ───────────────────────────────────────
const WEIGHTS = {
  regulatory:  0.30,  // 监管/处罚
  financial:   0.25,  // 财务压力
  governance:  0.20,  // 公司治理
  sentiment:   0.15,  // 舆情情绪
  operation:   0.10,  // 经营状况
};

const RISK_KEYWORDS = {
  regulatory:  ['处罚', '罚款', '违规', '违法', '被查', '监管', '整改', '关停', '清算', '行政处罚'],
  financial:   ['债务', '重组', '违约', '逾期', '偿债', '资金链', '清盘', '破产', '支付危机', '资不抵债'],
  governance:  ['被查', '落马', '反腐', '双规', '留置', '违纪', '涉嫌', '高管被', '内控', '治理风险'],
  negative:    ['暴跌', '蒸发', '腰斩', '亏损', '暴雷', '跑路', '失信', '限高', '被执行'],
  positive:    ['增长', '盈利', '扩张', '突破', '创新', '获奖', '合作', '稳健', '改善', '转型成功'],
};

function scoreCompany(text) {
  const t = text.toLowerCase();
  const scores = { regulatory: 0, financial: 0, governance: 0, sentiment: 0, operation: 0 };

  // 监管/处罚
  RISK_KEYWORDS.regulatory.forEach(kw => { if (t.includes(kw)) scores.regulatory += 25; });
  if (t.includes('相互宝')) scores.regulatory += 10;
  if (t.includes('常态化监管')) scores.regulatory -= 15; // 缓解信号

  // 财务压力
  RISK_KEYWORDS.financial.forEach(kw => { if (t.includes(kw)) scores.financial += 30; });
  if (t.includes('重组生效')) scores.financial += 10; // 重组生效≠风险解除
  if (t.includes('2%') && t.includes('本金')) scores.financial += 20; // 低回收率
  if (t.includes('净资产约100亿')) scores.financial += 25;

  // 公司治理
  RISK_KEYWORDS.governance.forEach(kw => { if (t.includes(kw)) scores.governance += 28; });
  if (t.includes('三任')) scores.governance += 15; // 持续动荡

  // 舆情情绪
  RISK_KEYWORDS.negative.forEach(kw => { if (t.includes(kw)) scores.sentiment += 18; });
  RISK_KEYWORDS.positive.forEach(kw => { if (t.includes(kw)) scores.sentiment -= 10; });

  // 经营状况
  if (t.includes('营收增速新低') || t.includes('失速')) scores.operation += 20;
  if (t.includes('个位数') && t.includes('目标')) scores.operation += 15;
  if (t.includes('价格倒挂')) scores.operation += 15;
  if (t.includes('市值蒸发逾万亿')) scores.operation += 20;
  if (t.includes('海外营收') && !t.includes('下滑')) scores.operation -= 10; // 国际化是正面

  // 归一化到0-100
  const final = {};
  for (const [k, v] of Object.entries(scores)) {
    final[k] = Math.min(100, Math.max(0, WEIGHTS[k] * v));
  }
  const total = Object.values(final).reduce((a, b) => a + b, 0);
  return total;
}

function level(score) {
  if (score <= 25) return 'R1-低风险';
  if (score <= 50) return 'R2-中低风险';
  if (score <= 75) return 'R3-中高风险';
  return 'R4-高风险';
}

function action(score) {
  if (score <= 25) return '可合作，建议季度级复检';
  if (score <= 50) return '可合作，重点关注合规持续性，季度复检';
  if (score <= 75) return '谨慎合作，需强担保，月度复检';
  return '不建议新增敞口，存量业务降级处理，回避';
}

function frequency(score) {
  if (score >= 75) return '月度';
  if (score >= 50) return '季度';
  return '半年度';
}

function extractFactors(text, keywords) {
  const found = [];
  keywords.forEach(kw => { if (text.includes(kw)) found.push(kw); });
  return [...new Set(found)];
}

// ── 简化舆情摘要 ──────────────────────────────────────
function summarize(text, maxLen = 120) {
  // 去除非常用字符，截断
  const clean = text.replace(/\s+/g, ' ').trim();
  return clean.length > maxLen ? clean.slice(0, maxLen) + '…' : clean;
}

// ── 主分析函数 ───────────────────────────────────────
function analyzeCompany(name, newsTexts) {
  const combined = newsTexts.join('。');
  const score = Math.round(scoreCompany(combined));
  const lev = level(score);
  const act = action(score);
  const freq = frequency(score);

  const neg = extractFactors(combined, [...RISK_KEYWORDS.regulatory, ...RISK_KEYWORDS.financial, ...RISK_KEYWORDS.governance, ...RISK_KEYWORDS.negative]);
  const pos = extractFactors(combined, RISK_KEYWORDS.positive);

  // 趋势判断
  const trend = neg.length > pos.length + 3 ? '上升' : neg.length < pos.length ? '下降' : '稳定';

  // 红标信号（取最强的3个）
  const allRisks = [...RISK_KEYWORDS.regulatory, ...RISK_KEYWORDS.financial, ...RISK_KEYWORDS.governance];
  const redFlags = allRisks.filter(kw => combined.includes(kw)).slice(0, 3);

  return {
    company: name,
    risk_level: lev,
    risk_score: score,
    risk_trend: trend,
    key_positive_factors: pos.slice(0, 4),
    key_negative_factors: neg.slice(0, 4),
    red_flags: redFlags,
    news_summary: summarize(combined),
    recommended_action: act,
    review_frequency: freq,
    last_updated: new Date().toISOString().slice(0, 10),
  };
}

// ── 入口 ────────────────────────────────────────────
const args = process.argv.slice(2);

async function main() {
  let companies = [];

  if (args[0] === '--file' && args[1]) {
    const content = readFileSync(args[1], 'utf8');
    companies = content.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
  } else if (args.length > 0) {
    companies = args.join(' ').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
  } else {
    // 读监控名单
    const watchlistPath = join(__dirname, '../../memory/risk-watchlist.md');
    if (existsSync(watchlistPath)) {
      const content = readFileSync(watchlistPath, 'utf8');
      companies = content.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
    } else {
      console.error('❌ 未提供企业列表，请通过参数或 memory/risk-watchlist.md 提供');
      process.exit(1);
    }
  }

  console.log(`\n🔍 开始扫描 ${companies.length} 家企业...\n`);

  const results = companies.map(name => {
    console.log(`  ⏳ ${name}`);
    // 注意：实际运行时，舆情数据需通过 batch_web_search + extract_content_from_websites 获取
    // 此处返回占位结构，真实调用由 agent 在会话中完成
    return analyzeCompany(name, []);
  });

  // 统计
  const r1 = results.filter(r => r.risk_level.startsWith('R1')).length;
  const r2 = results.filter(r => r.risk_level.startsWith('R2')).length;
  const r3 = results.filter(r => r.risk_level.startsWith('R3')).length;
  const r4 = results.filter(r => r.risk_level.startsWith('R4')).length;

  const report = {
    report_date: new Date().toISOString().slice(0, 10),
    total_companies: companies.length,
    summary: { R1_count: r1, R2_count: r2, R3_count: r3, R4_count: r4,
      high_risk_companies: results.filter(r => r.risk_level.startsWith('R4')).map(r => r.company) },
    companies: results,
  };

  // 保存报告
  const date = new Date().toISOString().slice(0, 10);
  const outPath = join(OUTPUT_DIR, `risk-report-${date}.json`);
  writeFileSync(outPath, JSON.stringify(report, null, 2), 'utf8');

  console.log(`\n✅ 报告已保存 → ${outPath}`);
  console.log(JSON.stringify(report.summary, null, 2));

  return report;
}

main().catch(console.error);

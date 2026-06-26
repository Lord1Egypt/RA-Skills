#!/usr/bin/env node
/**
 * scoring-engine.js
 * 读取客户原始数据 + 分层规则，计算加权评分，输出分层结果
 * 
 * 用法:
 *   node scoring-engine.js            # 正常评分（需要 customers-raw.json）
 *   node scoring-engine.js --sample   # 用示例数据跑通流程
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const DATA_DIR = path.join(ROOT, 'data');
const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, 'config/segmentation-rules.json'), 'utf8'));

// ==================== 示例数据 ====================
function generateSampleData() {
  const now = Date.now();
  const DAY = 86400000;
  return {
    collected_at: new Date().toISOString(),
    dry_run: false,
    companies: [
      { company_id: 'C001', company_name: 'TechVision GmbH', country: 'Germany' },
      { company_id: 'C002', company_name: 'Pacific Trading Co.', country: 'USA' },
      { company_id: 'C003', company_name: 'SilkRoad Electronics', country: 'Turkey' },
      { company_id: 'C004', company_name: 'NorthStar Import', country: 'Canada' },
      { company_id: 'C005', company_name: 'Dormant Corp', country: 'UK' },
      { company_id: 'C006', company_name: 'Ghost Ltd', country: 'Spain' }
    ],
    orders: [
      // C001: VIP（高金额、高频次）
      { company_id: 'C001', order_amount: 35000, currency: 'USD', create_time: now - 10 * DAY, status: 'completed' },
      { company_id: 'C001', order_amount: 28000, currency: 'USD', create_time: now - 60 * DAY, status: 'completed' },
      { company_id: 'C001', order_amount: 22000, currency: 'USD', create_time: now - 120 * DAY, status: 'completed' },
      { company_id: 'C001', order_amount: 15000, currency: 'USD', create_time: now - 200 * DAY, status: 'completed' },
      // C002: 活跃（中等金额、中等频次）
      { company_id: 'C002', order_amount: 8500, currency: 'USD', create_time: now - 20 * DAY, status: 'completed' },
      { company_id: 'C002', order_amount: 6200, currency: 'USD', create_time: now - 90 * DAY, status: 'completed' },
      { company_id: 'C002', order_amount: 7800, currency: 'USD', create_time: now - 180 * DAY, status: 'completed' },
      // C003: 普通（少量订单）
      { company_id: 'C003', order_amount: 2500, currency: 'USD', create_time: now - 45 * DAY, status: 'completed' },
      { company_id: 'C003', order_amount: 1800, currency: 'USD', create_time: now - 150 * DAY, status: 'completed' },
      // C004: 普通偏下
      { company_id: 'C004', order_amount: 800, currency: 'USD', create_time: now - 100 * DAY, status: 'completed' },
      // C005: 休眠（很久前的订单）
      { company_id: 'C005', order_amount: 12000, currency: 'USD', create_time: now - 250 * DAY, status: 'completed' }
      // C006: 无订单（流失）
    ],
    trails: [
      // C001: 高互动
      ...Array.from({ length: 20 }, (_, i) => ({
        company_id: 'C001', trail_type: 102, create_time: (now - i * 5 * DAY) / 1000
      })),
      // C002: 中等互动
      ...Array.from({ length: 8 }, (_, i) => ({
        company_id: 'C002', trail_type: 101, create_time: (now - i * 12 * DAY) / 1000
      })),
      // C003: 少量互动
      { company_id: 'C003', trail_type: 101, create_time: (now - 30 * DAY) / 1000 },
      { company_id: 'C003', trail_type: 102, create_time: (now - 60 * DAY) / 1000 },
      // C004: 极少互动
      { company_id: 'C004', trail_type: 101, create_time: (now - 100 * DAY) / 1000 },
      // C005: 很久前互动
      { company_id: 'C005', trail_type: 101, create_time: (now - 200 * DAY) / 1000 }
      // C006: 无互动
    ]
  };
}

// ==================== 评分逻辑 ====================

function getTierScore(value, tiers) {
  for (const tier of tiers) {
    const max = tier.max === null ? Infinity : tier.max;
    if (value >= tier.min && value < max) {
      return tier.score;
    }
  }
  return 0;
}

function computeOrderMetrics(orders, companyId, windowMonths = 12) {
  const cutoff = Date.now() - windowMonths * 30 * 86400000;
  const filtered = orders.filter(o => {
    const match = (o.company_id === companyId);
    const ts = o.create_time > 1e12 ? o.create_time : o.create_time * 1000;
    return match && ts >= cutoff;
  });

  const totalAmount = filtered.reduce((sum, o) => sum + (o.order_amount || 0), 0);
  const frequency = filtered.length;

  return { totalAmount, frequency };
}

function computeTrailMetrics(trails, companyId, windowMonths = 12) {
  const now = Date.now();
  const cutoff = now - windowMonths * 30 * 86400000;

  const filtered = trails.filter(t => {
    const match = (t.company_id === companyId);
    const ts = t.create_time > 1e12 ? t.create_time : t.create_time * 1000;
    return match && ts >= cutoff;
  });

  const interactionCount = filtered.length;

  // 最近一次跟进距今天数
  let daysSinceLast = 999;
  if (filtered.length > 0) {
    const latestTs = Math.max(...filtered.map(t =>
      t.create_time > 1e12 ? t.create_time : t.create_time * 1000
    ));
    daysSinceLast = Math.floor((now - latestTs) / 86400000);
  }

  return { interactionCount, daysSinceLast };
}

function scoreCustomer(company, orders, trails, dimensions) {
  const companyId = company.company_id || company.id;

  const orderWindow = dimensions.order_amount.window_months || 12;
  const { totalAmount, frequency } = computeOrderMetrics(orders, companyId, orderWindow);
  const trailWindow = dimensions.interaction.window_months || 12;
  const { interactionCount, daysSinceLast } = computeTrailMetrics(trails, companyId, trailWindow);

  const amountScore = getTierScore(totalAmount, dimensions.order_amount.normalize.tiers);
  const freqScore = getTierScore(frequency, dimensions.order_frequency.normalize.tiers);
  const recencyScore = getTierScore(daysSinceLast, dimensions.recency.normalize.tiers);
  const interactionScore = getTierScore(interactionCount, dimensions.interaction.normalize.tiers);

  const weighted =
    amountScore * dimensions.order_amount.weight +
    freqScore * dimensions.order_frequency.weight +
    recencyScore * dimensions.recency.weight +
    interactionScore * dimensions.interaction.weight;

  const totalScore = Math.round(weighted * 100) / 100;

  return {
    company_id: companyId,
    company_name: company.company_name || company.name || 'Unknown',
    scores: {
      order_amount: { raw: totalAmount, normalized: amountScore },
      order_frequency: { raw: frequency, normalized: freqScore },
      recency: { raw: daysSinceLast, normalized: recencyScore },
      interaction: { raw: interactionCount, normalized: interactionScore }
    },
    total_score: totalScore,
    segment: null // 下面分配
  };
}

function assignSegment(scoreResult, segments) {
  for (const level of segments) {
    if (scoreResult.total_score >= level.min_score) {
      scoreResult.segment = level.name;
      scoreResult.segment_label = level.label;
      scoreResult.strategy = level.strategy;
      return scoreResult;
    }
  }
  // 兜底
  const last = segments[segments.length - 1];
  scoreResult.segment = last.name;
  scoreResult.segment_label = last.label;
  scoreResult.strategy = last.strategy;
  return scoreResult;
}

function detectChanges(current, previous) {
  const changes = [];
  const prevMap = {};
  for (const p of previous) {
    prevMap[p.company_id] = p;
  }

  for (const c of current) {
    const prev = prevMap[c.company_id];
    if (!prev) {
      changes.push({
        company_id: c.company_id,
        company_name: c.company_name,
        type: 'new',
        from: null,
        to: c.segment,
        score_from: null,
        score_to: c.total_score
      });
    } else if (prev.segment !== c.segment) {
      changes.push({
        company_id: c.company_id,
        company_name: c.company_name,
        type: c.total_score > prev.total_score ? 'upgrade' : 'downgrade',
        from: prev.segment,
        to: c.segment,
        score_from: prev.total_score,
        score_to: c.total_score
      });
    }
  }

  return changes;
}

function applyManualOverrides(results, overridesPath) {
  if (!fs.existsSync(overridesPath)) return results;

  const overrides = JSON.parse(fs.readFileSync(overridesPath, 'utf8'));
  for (const result of results) {
    const override = overrides[result.company_id];
    if (override) {
      result.manual_override = true;
      result.original_segment = result.segment;
      result.segment = override.segment;
      result.segment_label = override.label || override.segment;
      if (override.reason) result.override_reason = override.reason;
    }
  }
  return results;
}

// ==================== 主流程 ====================
async function runScoring(useSample = false) {
  console.log(`[scoring] 开始评分... (sample: ${useSample})`);
  const startTime = Date.now();

  // 1. 加载数据
  let rawData;
  if (useSample) {
    rawData = generateSampleData();
    console.log('[scoring] 使用示例数据');
  } else {
    const rawPath = path.join(DATA_DIR, CONFIG.settings.customers_raw_file.replace('data/', ''));
    if (!fs.existsSync(rawPath)) {
      console.error(`[scoring] 错误: ${rawPath} 不存在。请先运行 customer-data-collector.js`);
      process.exit(1);
    }
    rawData = JSON.parse(fs.readFileSync(rawPath, 'utf8'));
    console.log(`[scoring] 已加载原始数据 (${rawData.companies.length} 客户)`);
  }

  const { companies, orders, trails } = rawData;
  const dimensions = CONFIG.kpis.dimensions;
  const segments = CONFIG.segments.levels;

  // 2. 逐客户评分
  const results = [];
  for (const company of companies) {
    let scored = scoreCustomer(company, orders, trails, dimensions);
    scored = assignSegment(scored, segments);
    results.push(scored);
  }

  // 3. 手动覆盖
  const overridesPath = path.join(ROOT, CONFIG.settings.manual_overrides_file);
  applyManualOverrides(results, overridesPath);

  // 4. 排序（高分在前）
  results.sort((a, b) => b.total_score - a.total_score);

  // 5. 变动检测
  const prevPath = path.join(DATA_DIR, 'scores-prev.json');
  let changes = [];
  if (fs.existsSync(prevPath)) {
    const prevData = JSON.parse(fs.readFileSync(prevPath, 'utf8'));
    changes = detectChanges(results, prevData.results || []);
  } else {
    changes = results.map(r => ({
      company_id: r.company_id,
      company_name: r.company_name,
      type: 'new',
      from: null,
      to: r.segment,
      score_from: null,
      score_to: r.total_score
    }));
  }

  // 6. 汇总统计
  const summary = {
    total_customers: results.length,
    segments: {}
  };
  for (const level of segments) {
    summary.segments[level.name] = results.filter(r => r.segment === level.name).length;
  }

  // 7. 输出
  const output = {
    scored_at: new Date().toISOString(),
    sample_mode: useSample,
    duration_ms: Date.now() - startTime,
    summary,
    changes,
    results
  };

  // 写入文件（非 sample 模式始终写入；sample 模式下如果 scores-current 不存在也写入）
  const currentPath = path.join(DATA_DIR, 'scores-current.json');
  const shouldWrite = !useSample || !fs.existsSync(currentPath);
  if (shouldWrite) {
    fs.mkdirSync(DATA_DIR, { recursive: true });

    // 备份当前为 prev
    if (fs.existsSync(currentPath)) {
      fs.copyFileSync(currentPath, prevPath);
    }

    fs.writeFileSync(currentPath, JSON.stringify(output, null, 2));
    console.log(`[scoring] 结果已写入: scores-current.json`);
  }

  // 8. 打印结果
  console.log('\n========== 评分结果 ==========');
  console.log(`客户总数: ${summary.total_customers}`);
  console.log(`分层统计:`);
  for (const [seg, count] of Object.entries(summary.segments)) {
    console.log(`  ${seg}: ${count}`);
  }

  console.log(`\n变动: ${changes.length} 条`);
  for (const c of changes) {
    const arrow = c.type === 'upgrade' ? '⬆️' : c.type === 'downgrade' ? '⬇️' : '🆕';
    console.log(`  ${arrow} ${c.company_name}: ${c.from || 'N/A'} → ${c.to} (${c.score_to})`);
  }

  console.log('\n详细评分:');
  for (const r of results) {
    const override = r.manual_override ? ' [手动覆盖]' : '';
    console.log(`  ${r.company_name} (${r.company_id}): ${r.total_score} → ${r.segment_label}${override}`);
    console.log(`    订单金额=${r.scores.order_amount.raw} (${r.scores.order_amount.normalized})`);
    console.log(`    频次=${r.scores.order_frequency.raw} (${r.scores.order_frequency.normalized})`);
    console.log(`    最近活跃=${r.scores.recency.raw}天 (${r.scores.recency.normalized})`);
    console.log(`    互动=${r.scores.interaction.raw}次 (${r.scores.interaction.normalized})`);
  }

  console.log(`\n[scoring] 完成。耗时: ${Date.now() - startTime}ms`);
  return output;
}

// ==================== CLI ====================
const args = process.argv.slice(2);
const useSample = args.includes('--sample');

runScoring(useSample).catch(err => {
  console.error(`[scoring] 错误: ${err.message}`);
  process.exit(1);
});

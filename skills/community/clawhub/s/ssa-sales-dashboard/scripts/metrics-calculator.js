#!/usr/bin/env node

/**
 * metrics-calculator.js - 指标计算与异常检测
 * 
 * 功能：
 *   1. 读取 data/latest.json
 *   2. 计算转化漏斗（线索 → 询盘 → 报价 → 订单 → 回款）
 *   3. 环比/同比计算
 *   4. 阈值异常检测 → 输出告警列表
 * 
 * 用法：
 *   node metrics-calculator.js [--check-alerts] [--output data/calculated.json]
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.join(__dirname, '..');
const LATEST_PATH = path.join(BASE_DIR, 'data', 'latest.json');
const CONFIG_PATH = path.join(BASE_DIR, 'config', 'dashboard-config.json');
const SNAPSHOTS_DIR = path.join(BASE_DIR, 'data', 'snapshots');
const OUTPUT_DEFAULT = path.join(BASE_DIR, 'data', 'calculated.json');

// ============ 参数解析 ============
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { checkAlerts: false, output: OUTPUT_DEFAULT };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--check-alerts') opts.checkAlerts = true;
    if (args[i] === '--output' && args[i + 1]) opts.output = args[++i];
  }
  return opts;
}

// ============ 转化漏斗 ============
function buildFunnel(kpis) {
  const stages = [
    { name: '线索', key: 'new_leads' },
    { name: '商机', key: 'opportunity_count' },
    { name: '报价', key: 'quotation_count' },
    { name: '订单', key: 'order_count' }
  ];
  
  const funnel = [];
  for (let i = 0; i < stages.length; i++) {
    const val = kpis[stages[i].key];
    const entry = {
      stage: stages[i].name,
      count: typeof val === 'number' ? val : 'N/A'
    };
    
    // 计算转化率（相对上一阶段）
    if (i > 0) {
      const prev = kpis[stages[i - 1].key];
      if (typeof val === 'number' && typeof prev === 'number' && prev > 0) {
        entry.rate_from_prev = parseFloat((val / prev * 100).toFixed(1));
      } else {
        entry.rate_from_prev = 'N/A';
      }
    }
    
    funnel.push(entry);
  }
  
  // 整体转化率（线索到订单）
  const leads = kpis.new_leads;
  const orders = kpis.order_count;
  funnel.push({
    stage: '整体转化',
    count: typeof orders === 'number' ? orders : 'N/A',
    rate_from_prev: (typeof leads === 'number' && typeof orders === 'number' && leads > 0)
      ? parseFloat((orders / leads * 100).toFixed(1))
      : 'N/A'
  });
  
  return funnel;
}

// ============ 同比计算 ============
function calcYoY(currentMetrics) {
  // 查找去年同期快照
  const period = currentMetrics.metadata.period;
  const range = currentMetrics.metadata.date_range;
  
  if (!range || !range.start) return null;
  
  const refDate = new Date(range.start);
  refDate.setFullYear(refDate.getFullYear() - 1);
  const yoyDate = refDate.toISOString().split('T')[0];
  
  if (!fs.existsSync(SNAPSHOTS_DIR)) return null;
  
  const files = fs.readdirSync(SNAPSHOTS_DIR)
    .filter(f => f.startsWith(period + '-') && f.includes(yoyDate.substring(0, 7)))
    .sort();
  
  if (files.length === 0) return null;
  
  try {
    const prev = JSON.parse(fs.readFileSync(path.join(SNAPSHOTS_DIR, files[0]), 'utf-8'));
    const changes = {};
    const numKpis = ['new_leads', 'new_customers', 'order_count', 'order_amount', 'quotation_count', 'quotation_amount'];
    
    for (const kpi of numKpis) {
      const cur = currentMetrics.kpis[kpi];
      const pre = prev.kpis ? prev.kpis[kpi] : undefined;
      if (typeof cur === 'number' && typeof pre === 'number' && pre > 0) {
        changes[kpi] = { current: cur, previous: pre, yoy_percent: parseFloat(((cur - pre) / pre * 100).toFixed(1)) };
      }
    }
    
    return { available: true, previous_file: files[0], changes };
  } catch (_) {
    return null;
  }
}

// ============ 异常检测 ============
function detectAnomalies(metrics) {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const alerts = metrics.alerts || [];
  
  // 追加基于计算的告警
  const kpis = metrics.kpis;
  
  // 转化率过低
  if (typeof kpis.conversion_rate === 'number' && kpis.conversion_rate < 5) {
    alerts.push({
      type: 'low_conversion',
      severity: 'info',
      message: `📊 报价转订单率仅 ${kpis.conversion_rate}%`
    });
  }
  
  // 大量线索但零商机
  if (typeof kpis.new_leads === 'number' && kpis.new_leads > 10 && kpis.opportunity_count === 0) {
    alerts.push({
      type: 'leads_no_opportunity',
      severity: 'warning',
      message: `⚠️ ${kpis.new_leads} 条线索但 0 商机，需检查线索转化流程`
    });
  }
  
  // 报价无订单
  if (typeof kpis.quotation_count === 'number' && kpis.quotation_count > 5 && kpis.order_count === 0) {
    alerts.push({
      type: 'quotation_no_order',
      severity: 'warning',
      message: `⚠️ ${kpis.quotation_count} 份报价但 0 订单，需检查报价竞争力`
    });
  }
  
  return alerts;
}

// ============ 主流程 ============
function main() {
  const opts = parseArgs();
  
  if (!fs.existsSync(LATEST_PATH)) {
    console.error('data/latest.json 不存在，请先运行 data-collector.js');
    process.exit(1);
  }
  
  const metrics = JSON.parse(fs.readFileSync(LATEST_PATH, 'utf-8'));
  
  // 1. 转化漏斗
  metrics.funnel = buildFunnel(metrics.kpis);
  console.log('=== 转化漏斗 ===');
  for (const s of metrics.funnel) {
    const rate = s.rate_from_prev !== undefined ? ` (${s.rate_from_prev}%)` : '';
    console.log(`  ${s.stage}: ${s.count}${rate}`);
  }
  
  // 2. 同比
  const yoy = calcYoY(metrics);
  if (yoy) {
    metrics.yoy = yoy;
    console.log('\n=== 同比 ===');
    console.log(JSON.stringify(yoy.changes, null, 2));
  }
  
  // 3. 异常检测
  if (opts.checkAlerts) {
    metrics.alerts = detectAnomalies(metrics);
    if (metrics.alerts.length > 0) {
      console.log(`\n=== 告警 (${metrics.alerts.length}) ===`);
      for (const a of metrics.alerts) {
        console.log(`  [${a.severity}] ${a.message}`);
      }
    }
  }
  
  // 4. 保存
  const outDir = path.dirname(opts.output);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(opts.output, JSON.stringify(metrics, null, 2));
  console.log(`\n已保存: ${opts.output}`);
}

main();

#!/usr/bin/env node

/**
 * data-collector.js - 渐进式销售数据采集器
 * 
 * 数据源：
 *   必选: OKKI CRM (客户/订单/报价/线索/商机)
 *   可选: campaign-tracker (邮件发送/回复统计)
 *   可选: follow-up-engine / order-tracker / customer-segmentation / pricing-engine
 * 
 * 用法：
 *   node data-collector.js --period weekly [--date 2026-03-24] [--dry-run]
 *   node data-collector.js --period monthly [--date 2026-03-01] [--dry-run]
 * 
 * 输出：
 *   data/latest.json              (最新指标，每次覆盖)
 *   data/snapshots/{period}-{date}.json  (历史快照，永不覆盖)
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ============ 路径 ============
const BASE_DIR = path.join(__dirname, '..');
const CONFIG_PATH = path.join(BASE_DIR, 'config', 'dashboard-config.json');
const OKKI_WORKSPACE = process.env.OKKI_WORKSPACE || path.resolve(__dirname, '../../../xiaoman-okki');
const OKKI_CONFIG_PATH = path.join(OKKI_WORKSPACE, 'api/config.json');
const OKKI_TOKEN_CACHE = path.join(OKKI_WORKSPACE, 'api/token.cache');
const ENV_PATH = process.env.ENV_PATH || path.resolve(__dirname, '../../../.env');
const SNAPSHOTS_DIR = path.join(BASE_DIR, 'data', 'snapshots');
const LATEST_PATH = path.join(BASE_DIR, 'data', 'latest.json');
const LOGS_DIR = path.join(BASE_DIR, 'logs');

// ============ 参数解析 ============
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { period: 'weekly', date: null, dryRun: false };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--period' && args[i + 1]) opts.period = args[++i];
    if (args[i] === '--date' && args[i + 1]) opts.date = args[++i];
    if (args[i] === '--dry-run') opts.dryRun = true;
  }
  
  return opts;
}

// ============ 日期工具 ============
function getDateRange(period, refDate) {
  const ref = refDate ? new Date(refDate + 'T00:00:00+08:00') : new Date();
  let start, end;
  
  if (period === 'weekly') {
    // 上周一到上周日
    const dayOfWeek = ref.getDay() || 7; // 0=Sun -> 7
    end = new Date(ref);
    end.setDate(ref.getDate() - dayOfWeek); // 上周日
    start = new Date(end);
    start.setDate(end.getDate() - 6); // 上周一
  } else if (period === 'monthly') {
    // 上个月 1 日到末日
    start = new Date(ref.getFullYear(), ref.getMonth() - 1, 1);
    end = new Date(ref.getFullYear(), ref.getMonth(), 0); // 上月末
  } else {
    throw new Error(`Unknown period: ${period}`);
  }
  
  const fmt = d => d.toISOString().split('T')[0];
  return { start: fmt(start), end: fmt(end) };
}

// ============ 日志 ============
function log(level, msg, data) {
  const ts = new Date().toISOString();
  const line = `[${ts}] [${level.toUpperCase()}] ${msg}`;
  console.log(line);
  if (data) console.log(JSON.stringify(data, null, 2));
  
  try {
    if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
    const logFile = path.join(LOGS_DIR, `collector-${ts.split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify({ ts, level, msg, data }) + '\n');
  } catch (_) {}
}

// ============ .env 加载 ============
function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return;
  const lines = fs.readFileSync(ENV_PATH, 'utf-8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx < 0) continue;
    const key = trimmed.slice(0, idx).trim();
    let val = trimmed.slice(idx + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (key && val && !process.env[key]) process.env[key] = val;
  }
}

// ============ OKKI 配置 ============
function getOkkiConfig() {
  loadEnv();
  let text = fs.readFileSync(OKKI_CONFIG_PATH, 'utf-8');
  text = text.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    if (expr.includes(':-')) {
      const [name, def] = expr.split(':-');
      return process.env[name] || def;
    }
    return process.env[expr] || '';
  });
  return JSON.parse(text);
}

// ============ OKKI Token ============
async function getOkkiToken(config, forceRefresh = false) {
  // 尝试用缓存
  if (!forceRefresh && fs.existsSync(OKKI_TOKEN_CACHE)) {
    try {
      const cached = JSON.parse(fs.readFileSync(OKKI_TOKEN_CACHE, 'utf-8'));
      if (cached.expires_at > Date.now() / 1000 + 300) {
        return cached.access_token;
      }
    } catch (_) {}
  }
  
  // 请求新 token
  const postData = new URLSearchParams({
    client_id: config.clientId,
    client_secret: config.clientSecret,
    grant_type: 'client_credentials',
    scope: config.scope
  }).toString();
  
  const tokenData = await httpRequest(config.tokenUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: postData
  });
  
  tokenData.expires_at = Date.now() / 1000 + (tokenData.expires_in || 7200);
  fs.writeFileSync(OKKI_TOKEN_CACHE, JSON.stringify(tokenData));
  return tokenData.access_token;
}

// ============ HTTP 请求工具 ============
function httpRequest(url, opts = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    
    const reqOpts = {
      hostname: u.hostname,
      port: u.port,
      path: u.pathname + u.search,
      method: opts.method || 'GET',
      headers: opts.headers || {},
      timeout: 30000
    };
    
    const req = mod.request(reqOpts, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error(`JSON parse error: ${body.substring(0, 200)}`));
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    
    if (opts.body) req.write(opts.body);
    req.end();
  });
}

// ============ OKKI API 调用 ============
async function okkiGet(config, token, endpoint, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const url = `${config.baseUrl}${endpoint}${qs ? '?' + qs : ''}`;
  
  try {
    const result = await httpRequest(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // token 过期自动刷新一次
    if (result.code === 401 || result.error_code === 401) {
      const newToken = await getOkkiToken(config, true);
      return httpRequest(url, {
        headers: { Authorization: `Bearer ${newToken}` }
      });
    }
    
    return result;
  } catch (err) {
    log('error', `OKKI API call failed: ${endpoint}`, { error: err.message });
    return { error: err.message };
  }
}

/**
 * 分页获取全量数据（最多 maxPages 页）
 */
async function okkiListAll(config, token, endpoint, timeParams, maxPages = 20) {
  let allData = [];
  let page = 1;
  const pageSize = 50;
  
  while (page <= maxPages) {
    const params = {
      start_index: page,
      count: pageSize,
      ...timeParams
    };
    
    const resp = await okkiGet(config, token, endpoint, params);
    
    if (resp.error) {
      log('error', `分页获取失败 ${endpoint} page=${page}`, resp);
      break;
    }
    
    const items = resp.data || resp.list || [];
    if (!Array.isArray(items) || items.length === 0) break;
    
    allData = allData.concat(items);
    
    // 检查是否有更多
    const total = resp.total || resp.total_number || 0;
    if (allData.length >= total || items.length < pageSize) break;
    
    page++;
  }
  
  return allData;
}

// ============ OKKI 数据采集 ============
async function collectOkkiData(dateRange) {
  log('info', `采集 OKKI 数据: ${dateRange.start} ~ ${dateRange.end}`);
  const config = getOkkiConfig();
  const token = await getOkkiToken(config);
  
  const timeParams = {
    start_time: dateRange.start,
    end_time: dateRange.end,
    time_type: '2'  // 按创建时间
  };
  
  const results = {};
  
  // 1. 客户
  try {
    const customers = await okkiListAll(config, token, '/v1/company/list', timeParams);
    results.new_customers = customers.length;
    results.customers_raw = customers;
    log('info', `新客户: ${customers.length}`);
  } catch (e) {
    results.new_customers = 'N/A';
    log('error', '客户数据采集失败', { error: e.message });
  }
  
  // 2. 销售订单
  try {
    const orders = await okkiListAll(config, token, '/v1/invoices/order/list', timeParams);
    results.order_count = orders.length;
    results.order_amount = orders.reduce((sum, o) => {
      const amt = parseFloat(o.amount || o.total_amount || o.order_amount || 0);
      return sum + (isNaN(amt) ? 0 : amt);
    }, 0);
    results.orders_raw = orders;
    log('info', `订单: ${orders.length}, 金额: ${results.order_amount}`);
  } catch (e) {
    results.order_count = 'N/A';
    results.order_amount = 'N/A';
    log('error', '订单数据采集失败', { error: e.message });
  }
  
  // 3. 报价单
  try {
    const quotations = await okkiListAll(config, token, '/v1/invoices/quotation/list', timeParams);
    results.quotation_count = quotations.length;
    results.quotation_amount = quotations.reduce((sum, q) => {
      const amt = parseFloat(q.amount || q.total_amount || 0);
      return sum + (isNaN(amt) ? 0 : amt);
    }, 0);
    results.quotations_raw = quotations;
    log('info', `报价单: ${quotations.length}, 金额: ${results.quotation_amount}`);
  } catch (e) {
    results.quotation_count = 'N/A';
    results.quotation_amount = 'N/A';
    log('error', '报价数据采集失败', { error: e.message });
  }
  
  // 4. 线索
  try {
    const leads = await okkiListAll(config, token, '/v1/lead/list', timeParams);
    results.new_leads = leads.length;
    results.leads_raw = leads;
    log('info', `新线索: ${leads.length}`);
  } catch (e) {
    results.new_leads = 'N/A';
    log('error', '线索数据采集失败', { error: e.message });
  }
  
  // 5. 商机
  try {
    const opps = await okkiListAll(config, token, '/v1/opportunity/list', {
      start_time: dateRange.start,
      end_time: dateRange.end
    });
    results.opportunity_count = opps.length;
    results.opportunities_raw = opps;
    log('info', `商机: ${opps.length}`);
  } catch (e) {
    results.opportunity_count = 'N/A';
    log('error', '商机数据采集失败', { error: e.message });
  }
  
  return results;
}

// ============ Campaign Tracker 数据采集 ============
function collectCampaignData(dateRange) {
  log('info', '采集 Campaign Tracker 数据');
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const ctConfig = config.sources['campaign-tracker'];
  
  if (!ctConfig) return null;
  
  // 尝试读取最新报告
  const reportsDir = ctConfig.reports_dir;
  if (!fs.existsSync(reportsDir)) {
    log('warn', 'Campaign Tracker reports 目录不存在，跳过');
    return null;
  }
  
  // 查找 JSON 格式报告
  const files = fs.readdirSync(reportsDir)
    .filter(f => f.endsWith('.json'))
    .sort()
    .reverse();
  
  if (files.length === 0) {
    log('warn', 'Campaign Tracker 无 JSON 报告，跳过');
    return null;
  }
  
  try {
    const latest = JSON.parse(fs.readFileSync(path.join(reportsDir, files[0]), 'utf-8'));
    // 支持嵌套结构: report.metrics.sent_count 或顶层 report.sent_count
    const m = latest.metrics || latest;
    
    // reply_rate 可能是小数 (0.667) 或百分比 (66.7)，统一转为百分比
    let replyRate = m.reply_rate !== undefined ? m.reply_rate : 'N/A';
    if (typeof replyRate === 'number' && replyRate <= 1) {
      replyRate = parseFloat((replyRate * 100).toFixed(1));
    }
    
    const result = {
      email_sent: m.total_sent || m.sent_count || 'N/A',
      email_reply_rate: replyRate,
      replied_count: m.replied_count || m.reply_count || 'N/A',
      source_file: files[0]
    };
    log('info', `Campaign 数据: sent=${result.email_sent}, reply_rate=${result.email_reply_rate}%`);
    return result;
  } catch (e) {
    log('error', `读取 Campaign 报告失败: ${files[0]}`, { error: e.message });
    return null;
  }
}

// ============ 可选数据源采集 ============
function collectOptionalSource(name) {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const src = config.sources[name];
  if (!src || !src.metrics_path) return null;
  
  if (!fs.existsSync(src.metrics_path)) {
    log('info', `${name}: metrics-export.json 不存在，跳过`);
    return null;
  }
  
  try {
    const data = JSON.parse(fs.readFileSync(src.metrics_path, 'utf-8'));
    log('info', `${name}: 成功读取 metrics`);
    return data;
  } catch (e) {
    log('warn', `${name}: 读取失败`, { error: e.message });
    return null;
  }
}

// ============ 指标汇总 ============
function assembleMetrics(okkiData, campaignData, optionalSources, dateRange, period) {
  const metrics = {
    metadata: {
      period,
      date_range: dateRange,
      collected_at: new Date().toISOString(),
      sources_available: ['okki']
    },
    kpis: {
      // OKKI 数据
      new_leads: okkiData.new_leads,
      new_customers: okkiData.new_customers,
      quotation_count: okkiData.quotation_count,
      quotation_amount: okkiData.quotation_amount,
      order_count: okkiData.order_count,
      order_amount: okkiData.order_amount,
      opportunity_count: okkiData.opportunity_count,
      // 计算转化率
      conversion_rate: 'N/A'
    }
  };
  
  // 转化率计算
  if (typeof okkiData.order_count === 'number' && typeof okkiData.quotation_count === 'number' && okkiData.quotation_count > 0) {
    metrics.kpis.conversion_rate = parseFloat((okkiData.order_count / okkiData.quotation_count * 100).toFixed(2));
  }
  
  // Campaign Tracker 数据
  if (campaignData) {
    metrics.metadata.sources_available.push('campaign-tracker');
    metrics.kpis.email_sent = campaignData.email_sent;
    metrics.kpis.email_reply_rate = campaignData.email_reply_rate;
    metrics.kpis.replied_count = campaignData.replied_count;
  } else {
    metrics.kpis.email_sent = 'N/A';
    metrics.kpis.email_reply_rate = 'N/A';
    metrics.kpis.replied_count = 'N/A';
  }
  
  // 可选数据源
  for (const [name, data] of Object.entries(optionalSources)) {
    if (data) {
      metrics.metadata.sources_available.push(name);
      metrics[name] = data;
    }
  }
  
  return metrics;
}

// ============ 环比计算 ============
function calcComparison(currentMetrics) {
  // 查找上期快照
  const period = currentMetrics.metadata.period;
  const snapshotFiles = fs.existsSync(SNAPSHOTS_DIR)
    ? fs.readdirSync(SNAPSHOTS_DIR).filter(f => f.startsWith(period + '-') && f.endsWith('.json')).sort().reverse()
    : [];
  
  if (snapshotFiles.length === 0) {
    log('info', '无历史快照，跳过环比计算');
    currentMetrics.comparison = { available: false, note: '首次采集，无历史数据' };
    return currentMetrics;
  }
  
  try {
    const prevPath = path.join(SNAPSHOTS_DIR, snapshotFiles[0]);
    const prev = JSON.parse(fs.readFileSync(prevPath, 'utf-8'));
    
    const comp = { available: true, previous_snapshot: snapshotFiles[0], changes: {} };
    const numericKpis = ['new_leads', 'new_customers', 'quotation_count', 'quotation_amount', 'order_count', 'order_amount', 'opportunity_count', 'email_sent'];
    
    for (const kpi of numericKpis) {
      const cur = currentMetrics.kpis[kpi];
      const pre = prev.kpis ? prev.kpis[kpi] : undefined;
      
      if (typeof cur === 'number' && typeof pre === 'number' && pre > 0) {
        const change = parseFloat(((cur - pre) / pre * 100).toFixed(1));
        comp.changes[kpi] = { current: cur, previous: pre, change_percent: change };
      } else {
        comp.changes[kpi] = { current: cur, previous: pre || 'N/A', change_percent: 'N/A' };
      }
    }
    
    currentMetrics.comparison = comp;
    log('info', `环比计算完成，对比: ${snapshotFiles[0]}`);
  } catch (e) {
    log('error', '环比计算失败', { error: e.message });
    currentMetrics.comparison = { available: false, note: `计算失败: ${e.message}` };
  }
  
  return currentMetrics;
}

// ============ 告警检测 ============
function checkAlerts(metrics) {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  const alerts = [];
  
  // 回复率告警
  if (typeof metrics.kpis.email_reply_rate === 'number' && metrics.kpis.email_reply_rate < config.alerts.thresholds.reply_rate_min) {
    alerts.push({
      type: 'reply_rate_low',
      severity: 'warning',
      message: `⚠️ 邮件回复率 ${metrics.kpis.email_reply_rate}%，低于阈值 ${config.alerts.thresholds.reply_rate_min}%`
    });
  }
  
  // 订单金额环比下降告警
  if (metrics.comparison && metrics.comparison.available) {
    const orderChange = metrics.comparison.changes.order_amount;
    if (orderChange && typeof orderChange.change_percent === 'number' && orderChange.change_percent < -config.alerts.thresholds.order_amount_drop_max) {
      alerts.push({
        type: 'order_amount_drop',
        severity: 'critical',
        message: `🚨 订单金额环比下降 ${Math.abs(orderChange.change_percent)}%，超过阈值 ${config.alerts.thresholds.order_amount_drop_max}%`
      });
    }
  }
  
  // 零订单告警
  if (metrics.kpis.order_count === 0 && metrics.metadata.period === 'weekly') {
    alerts.push({
      type: 'zero_orders',
      severity: 'warning',
      message: '⚠️ 本周零订单'
    });
  }
  
  metrics.alerts = alerts;
  if (alerts.length > 0) {
    log('warn', `发现 ${alerts.length} 条告警`, alerts);
  }
  
  return metrics;
}

// ============ 保存数据 ============
function saveMetrics(metrics, period, dateRange, dryRun) {
  // 移除 raw 数据（不存入快照）
  const snapshot = JSON.parse(JSON.stringify(metrics));
  delete snapshot.customers_raw;
  delete snapshot.orders_raw;
  delete snapshot.quotations_raw;
  delete snapshot.leads_raw;
  delete snapshot.opportunities_raw;
  
  if (dryRun) {
    log('info', '[DRY-RUN] 不写入文件');
    console.log('\n=== 采集结果预览 ===');
    console.log(JSON.stringify(snapshot, null, 2));
    return;
  }
  
  // 确保目录存在
  if (!fs.existsSync(SNAPSHOTS_DIR)) fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true });
  
  // 1. 保存快照
  const snapshotName = `${period}-${dateRange.end}.json`;
  const snapshotPath = path.join(SNAPSHOTS_DIR, snapshotName);
  fs.writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2));
  log('info', `快照已保存: ${snapshotPath}`);
  
  // 2. 更新 latest.json
  fs.writeFileSync(LATEST_PATH, JSON.stringify(snapshot, null, 2));
  log('info', `latest.json 已更新`);
  
  return snapshotPath;
}

// ============ 主流程 ============
async function main() {
  const opts = parseArgs();
  log('info', `=== 销售数据采集开始 ===`, opts);
  
  // 计算日期范围
  const dateRange = getDateRange(opts.period, opts.date);
  log('info', `日期范围: ${dateRange.start} ~ ${dateRange.end}`);
  
  // 1. OKKI 数据（必选）
  let okkiData;
  try {
    okkiData = await collectOkkiData(dateRange);
  } catch (e) {
    log('error', 'OKKI 数据采集严重失败', { error: e.message });
    okkiData = {
      new_customers: 'N/A', order_count: 'N/A', order_amount: 'N/A',
      quotation_count: 'N/A', quotation_amount: 'N/A',
      new_leads: 'N/A', opportunity_count: 'N/A'
    };
  }
  
  // 2. Campaign Tracker 数据（可选）
  const campaignData = collectCampaignData(dateRange);
  
  // 3. 其他可选数据源
  const optionalSources = {};
  for (const name of ['follow-up-engine', 'order-tracker', 'customer-segmentation', 'pricing-engine']) {
    optionalSources[name] = collectOptionalSource(name);
  }
  
  // 4. 汇总指标
  let metrics = assembleMetrics(okkiData, campaignData, optionalSources, dateRange, opts.period);
  
  // 5. 环比计算
  metrics = calcComparison(metrics);
  
  // 6. 告警检测
  metrics = checkAlerts(metrics);
  
  // 7. 保存
  const saved = saveMetrics(metrics, opts.period, dateRange, opts.dryRun);
  
  log('info', `=== 采集完成 ===`);
  
  // 输出摘要
  const summary = {
    period: opts.period,
    range: `${dateRange.start} ~ ${dateRange.end}`,
    sources: metrics.metadata.sources_available,
    kpis: metrics.kpis,
    alerts: (metrics.alerts || []).length,
    snapshot: saved || '(dry-run)'
  };
  
  console.log('\n=== 采集摘要 ===');
  console.log(JSON.stringify(summary, null, 2));
  
  return metrics;
}

main().catch(err => {
  log('error', `采集器崩溃: ${err.message}`, { stack: err.stack });
  process.exit(1);
});

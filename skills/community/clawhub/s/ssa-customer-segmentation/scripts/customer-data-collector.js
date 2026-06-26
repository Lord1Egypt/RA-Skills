#!/usr/bin/env node
/**
 * customer-data-collector.js
 * 从 OKKI CRM 增量拉取客户+订单+跟进记录
 * 
 * 用法:
 *   node customer-data-collector.js           # 全量采集
 *   node customer-data-collector.js --dry-run  # 只拉1页，不写文件
 *   node customer-data-collector.js --period weekly  # 指定周期
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// ==================== 配置 ====================
const OKKI_WORKSPACE = process.env.OKKI_WORKSPACE || path.resolve(__dirname, '../../../xiaoman-okki');
const ENV_PATH = process.env.ENV_PATH || path.resolve(__dirname, '../../../.env');
const OKKI_CONFIG_PATH = path.join(OKKI_WORKSPACE, 'api/config.json');
const TOKEN_CACHE_PATH = path.join(OKKI_WORKSPACE, 'api/token.cache');

const CONFIG = JSON.parse(fs.readFileSync(path.join(ROOT, 'config/segmentation-rules.json'), 'utf8'));
const DATA_DIR = path.join(ROOT, 'data');
const LOGS_DIR = path.join(ROOT, 'logs');

const API_INTERVAL_MS = CONFIG.settings.api_interval_ms || 500;
const API_QUOTA_LIMIT = CONFIG.settings.api_quota_limit || 1000;

// ==================== 环境变量 ====================
function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return;
  const lines = fs.readFileSync(ENV_PATH, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx < 0) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let val = trimmed.slice(eqIdx + 1).trim();
    val = val.replace(/^["']|["']$/g, '');
    if (key && val && !process.env[key]) {
      process.env[key] = val;
    }
  }
}

function resolveEnvVars(text) {
  return text.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    if (expr.includes(':-')) {
      const [varName, defaultVal] = expr.split(':-', 2);
      return process.env[varName] || defaultVal;
    }
    return process.env[expr] || '';
  });
}

function getOkkiConfig() {
  loadEnv();
  const raw = fs.readFileSync(OKKI_CONFIG_PATH, 'utf8');
  return JSON.parse(resolveEnvVars(raw));
}

// ==================== Token 管理 ====================
async function getAccessToken(forceRefresh = false) {
  if (!forceRefresh && fs.existsSync(TOKEN_CACHE_PATH)) {
    const cached = JSON.parse(fs.readFileSync(TOKEN_CACHE_PATH, 'utf8'));
    if (cached.expires_at > Date.now() / 1000 + 300) {
      return cached.access_token;
    }
  }

  const config = getOkkiConfig();
  const body = new URLSearchParams({
    client_id: config.clientId,
    client_secret: config.clientSecret,
    grant_type: 'client_credentials',
    scope: config.scope
  });

  const resp = await fetch(config.tokenUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  if (!resp.ok) {
    throw new Error(`Token request failed: ${resp.status} ${resp.statusText}`);
  }

  const tokenData = await resp.json();
  tokenData.expires_at = Date.now() / 1000 + (tokenData.expires_in || 7200);
  fs.writeFileSync(TOKEN_CACHE_PATH, JSON.stringify(tokenData, null, 2));
  return tokenData.access_token;
}

// ==================== API 请求 ====================
let apiCallCount = 0;

async function apiRequest(method, urlPath, params = {}, token = null) {
  if (apiCallCount >= API_QUOTA_LIMIT) {
    throw new Error(`API 配额已用尽 (${API_QUOTA_LIMIT} 次)`);
  }

  const config = getOkkiConfig();
  const baseUrl = config.baseUrl;
  if (!token) token = await getAccessToken();

  let url = `${baseUrl}${urlPath}`;
  if (method === 'GET' && Object.keys(params).length > 0) {
    const qs = new URLSearchParams(params).toString();
    url += `?${qs}`;
  }

  const options = {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };

  if (method === 'POST') {
    options.body = JSON.stringify(params);
  }

  const resp = await fetch(url, options);
  apiCallCount++;

  if (resp.status === 401) {
    const newToken = await getAccessToken(true);
    options.headers['Authorization'] = `Bearer ${newToken}`;
    const retry = await fetch(url, options);
    apiCallCount++;
    if (!retry.ok) throw new Error(`API error: ${retry.status}`);
    return retry.json();
  }

  if (!resp.ok) throw new Error(`API error: ${resp.status} ${resp.statusText}`);
  return resp.json();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== 分页采集 ====================
function extractList(result) {
  // OKKI API 可能返回多种格式: { data: [...] }, { list: [...] }, { data: { list: [...] } }
  if (Array.isArray(result)) return result;
  if (result && Array.isArray(result.data)) return result.data;
  if (result && Array.isArray(result.list)) return result.list;
  if (result && result.data && Array.isArray(result.data.list)) return result.data.list;
  if (result && result.data && typeof result.data === 'object') {
    // 尝试从 data 对象中找到第一个数组属性
    for (const val of Object.values(result.data)) {
      if (Array.isArray(val)) return val;
    }
  }
  return [];
}

async function fetchAllPages(urlPath, pageSize = 20, maxPages = null, dryRun = false) {
  const allData = [];
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    if (maxPages && page > maxPages) break;

    const result = await apiRequest('GET', urlPath, {
      start_index: page,
      count: pageSize
    });

    if (dryRun) {
      console.log(`[dry-run] API 原始响应 keys: ${JSON.stringify(Object.keys(result || {}))}`);
      if (result && result.data) {
        console.log(`[dry-run] data 类型: ${typeof result.data}, isArray: ${Array.isArray(result.data)}`);
        if (typeof result.data === 'object' && !Array.isArray(result.data)) {
          console.log(`[dry-run] data keys: ${JSON.stringify(Object.keys(result.data))}`);
        }
      }
    }

    const items = extractList(result);
    if (items.length === 0) {
      hasMore = false;
    } else {
      allData.push(...items);
      if (items.length < pageSize) hasMore = false;
      page++;
    }

    if (dryRun) {
      console.log(`[dry-run] 拉取第 1 页完成，共 ${items.length} 条，停止`);
      break;
    }

    if (hasMore) await sleep(API_INTERVAL_MS);
  }

  return allData;
}

// ==================== 客户数据采集 ====================
async function collectCustomerData(dryRun = false) {
  const startTime = Date.now();
  const log = [];

  console.log(`[collector] 开始采集客户数据... (dry-run: ${dryRun})`);
  log.push(`采集开始: ${new Date().toISOString()}`);

  // 1. 拉取客户列表
  console.log('[collector] 拉取客户列表...');
  const companies = await fetchAllPages('/v1/company/list', 20, null, dryRun);
  log.push(`客户数: ${companies.length}`);
  console.log(`[collector] 客户数: ${companies.length}`);
  await sleep(API_INTERVAL_MS);

  // 2. 拉取订单列表（近12个月）
  console.log('[collector] 拉取订单列表...');
  const orders = await fetchAllPages('/v1/invoices/order/list', 20, null, dryRun);
  log.push(`订单数: ${orders.length}`);
  console.log(`[collector] 订单数: ${orders.length}`);
  await sleep(API_INTERVAL_MS);

  // 3. 拉取跟进记录（按客户聚合）
  console.log('[collector] 拉取跟进记录...');
  const trails = [];
  const companyIds = companies.map(c => c.company_id || c.id).filter(Boolean);

  if (dryRun) {
    // dry-run 只拉第一个客户的跟进
    if (companyIds.length > 0) {
      const t = await apiRequest('GET', '/v1/dynamic/trail/list', {
        company_id: companyIds[0],
        page: 1,
        limit: 20
      });
      const items = extractList(t);
      trails.push(...items.map(i => ({ ...i, company_id: companyIds[0] })));
      console.log(`[dry-run] 拉取客户 ${companyIds[0]} 跟进 ${items.length} 条`);
    }
  } else {
    for (const cid of companyIds) {
      if (apiCallCount >= API_QUOTA_LIMIT) {
        console.log(`[collector] API 配额已达上限 (${API_QUOTA_LIMIT})，停止拉取跟进`);
        break;
      }
      const t = await apiRequest('GET', '/v1/dynamic/trail/list', {
        company_id: cid,
        page: 1,
        limit: 50
      });
      const items = extractList(t);
      trails.push(...items.map(i => ({ ...i, company_id: cid })));
      await sleep(API_INTERVAL_MS);
    }
  }

  log.push(`跟进记录数: ${trails.length}`);
  console.log(`[collector] 跟进记录数: ${trails.length}`);

  // 4. 组装原始数据
  const rawData = {
    collected_at: new Date().toISOString(),
    api_calls: apiCallCount,
    duration_ms: Date.now() - startTime,
    dry_run: dryRun,
    companies,
    orders,
    trails
  };

  // 5. 写文件
  if (!dryRun) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    const outputPath = path.join(DATA_DIR, 'customers-raw.json');
    fs.writeFileSync(outputPath, JSON.stringify(rawData, null, 2));
    console.log(`[collector] 数据已写入: ${outputPath}`);

    // 更新 last-sync
    const syncInfo = {
      last_sync_at: new Date().toISOString(),
      companies_count: companies.length,
      orders_count: orders.length,
      trails_count: trails.length,
      api_calls: apiCallCount,
      duration_ms: Date.now() - startTime
    };
    fs.writeFileSync(path.join(DATA_DIR, 'last-sync.json'), JSON.stringify(syncInfo, null, 2));
    console.log(`[collector] 同步信息已更新: last-sync.json`);
  } else {
    console.log(`[dry-run] 跳过文件写入`);
    console.log(`[dry-run] 数据预览:`);
    console.log(`  客户样本: ${JSON.stringify(companies[0] || {}, null, 2).slice(0, 500)}`);
  }

  // 6. 写日志
  fs.mkdirSync(LOGS_DIR, { recursive: true });
  const logEntry = {
    timestamp: new Date().toISOString(),
    dry_run: dryRun,
    api_calls: apiCallCount,
    duration_ms: Date.now() - startTime,
    companies: companies.length,
    orders: orders.length,
    trails: trails.length,
    log
  };
  const logPath = path.join(LOGS_DIR, `collect-${new Date().toISOString().slice(0, 10)}.json`);
  fs.writeFileSync(logPath, JSON.stringify(logEntry, null, 2));

  console.log(`[collector] 完成。API 调用: ${apiCallCount}, 耗时: ${Date.now() - startTime}ms`);
  return rawData;
}

// ==================== CLI ====================
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');

collectCustomerData(dryRun).catch(err => {
  console.error(`[collector] 错误: ${err.message}`);
  process.exit(1);
});

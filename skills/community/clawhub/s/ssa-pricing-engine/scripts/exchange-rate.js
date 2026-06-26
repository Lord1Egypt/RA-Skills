/**
 * Exchange Rate Module
 * 
 * 汇率获取模块：对接免费汇率 API，支持缓存和离线降级。
 * 
 * API:
 *   getRate(from, to)              → Promise<number>
 *   convertAmount(amount, from, to) → Promise<number>
 *   refreshRates()                  → Promise<object>
 *   getAllRates()                   → Promise<object>
 * 
 * 配置:
 *   DRY_RUN=true 环境变量启用模拟汇率
 *   CACHE_TTL_MS 环境变量自定义缓存时间（默认 4h）
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ========== 路径配置 ==========
const SKILL_DIR = path.resolve(__dirname, '..');
const CACHE_FILE = path.join(SKILL_DIR, 'cache', 'exchange-rates.json');
const LOG_FILE = path.join(SKILL_DIR, 'logs', 'exchange-rate.log');

// ========== 常量 ==========
const CACHE_TTL_MS = parseInt(process.env.CACHE_TTL_MS, 10) || 4 * 60 * 60 * 1000; // 4 hours
const API_URL = 'https://open.er-api.com/v6/latest/USD';
const SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'CNY'];
const REQUEST_TIMEOUT_MS = 10000;

// ========== 模拟汇率（dry-run 模式） ==========
const MOCK_RATES = {
  base: 'USD',
  rates: {
    USD: 1.0,
    EUR: 0.92,
    GBP: 0.79,
    CNY: 7.25
  },
  fetched_at: new Date().toISOString(),
  source: 'mock'
};

// ========== 工具函数 ==========

function isDryRun() {
  return process.env.DRY_RUN === 'true' || process.env.DRY_RUN === '1';
}

function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function log(level, message) {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
  try {
    ensureDir(LOG_FILE);
    fs.appendFileSync(LOG_FILE, line, 'utf-8');
  } catch (e) {
    // 日志写入失败不影响主流程
  }
}

function normalizeCurrency(code) {
  if (typeof code !== 'string') return '';
  return code.trim().toUpperCase();
}

function validateCurrency(code) {
  const c = normalizeCurrency(code);
  if (!SUPPORTED_CURRENCIES.includes(c)) {
    throw new Error(`Unsupported currency: ${code}. Supported: ${SUPPORTED_CURRENCIES.join(', ')}`);
  }
  return c;
}

// ========== 缓存管理 ==========

function readCache() {
  try {
    if (!fs.existsSync(CACHE_FILE)) return null;
    const raw = fs.readFileSync(CACHE_FILE, 'utf-8');
    const data = JSON.parse(raw);
    return data;
  } catch (e) {
    log('warn', `Cache read failed: ${e.message}`);
    return null;
  }
}

function writeCache(data) {
  try {
    ensureDir(CACHE_FILE);
    fs.writeFileSync(CACHE_FILE, JSON.stringify(data, null, 2), 'utf-8');
    log('info', 'Cache updated successfully');
  } catch (e) {
    log('error', `Cache write failed: ${e.message}`);
  }
}

function isCacheValid(cache) {
  if (!cache || !cache.fetched_at || !cache.rates) return false;
  const age = Date.now() - new Date(cache.fetched_at).getTime();
  return age < CACHE_TTL_MS;
}

// ========== HTTP 请求 ==========

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, { timeout: REQUEST_TIMEOUT_MS }, (res) => {
      if (res.statusCode < 200 || res.statusCode >= 300) {
        reject(new Error(`HTTP ${res.statusCode} from ${url}`));
        res.resume();
        return;
      }
      let body = '';
      res.setEncoding('utf-8');
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error(`JSON parse failed: ${e.message}`));
        }
      });
    });
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`Request timeout (${REQUEST_TIMEOUT_MS}ms) for ${url}`));
    });
    req.on('error', reject);
  });
}

// ========== 核心逻辑 ==========

/**
 * 从 API 获取最新汇率
 */
async function fetchRatesFromAPI() {
  log('info', `Fetching rates from API: ${API_URL}`);
  const data = await fetchJSON(API_URL);

  if (!data.rates) {
    throw new Error('API response missing rates field');
  }

  const filtered = {};
  for (const cur of SUPPORTED_CURRENCIES) {
    if (data.rates[cur] !== undefined) {
      filtered[cur] = data.rates[cur];
    } else {
      log('warn', `Currency ${cur} not found in API response`);
    }
  }

  const result = {
    base: 'USD',
    rates: filtered,
    fetched_at: new Date().toISOString(),
    source: 'open.er-api.com',
    api_time_last_update: data.time_last_update_utc || null
  };

  log('info', `Rates fetched: ${JSON.stringify(filtered)}`);
  return result;
}

/**
 * 获取汇率数据（带缓存和降级）
 * 优先级：dry-run 模拟 → 有效缓存 → API → 过期缓存（降级）
 */
async function getRatesData() {
  // dry-run 模式
  if (isDryRun()) {
    log('info', 'Dry-run mode: using mock rates');
    return { ...MOCK_RATES, fetched_at: new Date().toISOString() };
  }

  // 检查缓存
  const cache = readCache();
  if (isCacheValid(cache)) {
    log('info', 'Using cached rates (within TTL)');
    return cache;
  }

  // 尝试 API
  try {
    const fresh = await fetchRatesFromAPI();
    writeCache(fresh);
    return fresh;
  } catch (apiErr) {
    log('error', `API fetch failed: ${apiErr.message}`);

    // 离线降级：使用过期缓存
    if (cache && cache.rates) {
      log('warn', `Offline fallback: using stale cache from ${cache.fetched_at}`);
      return { ...cache, _stale: true };
    }

    // 无缓存可用
    throw new Error(`Cannot get exchange rates: API failed (${apiErr.message}) and no cache available`);
  }
}

// ========== 公共 API ==========

/**
 * 获取汇率
 * @param {string} from 源货币代码 (USD/EUR/GBP/CNY)
 * @param {string} to   目标货币代码 (USD/EUR/GBP/CNY)
 * @returns {Promise<number>} 汇率
 */
async function getRate(from, to) {
  const fromCode = validateCurrency(from);
  const toCode = validateCurrency(to);

  if (fromCode === toCode) return 1.0;

  const data = await getRatesData();
  const fromRate = data.rates[fromCode];
  const toRate = data.rates[toCode];

  if (fromRate === undefined || toRate === undefined) {
    throw new Error(`Rate not available for ${fromCode} or ${toCode}`);
  }

  // 所有汇率基于 USD，交叉汇率 = toRate / fromRate
  const rate = toRate / fromRate;

  log('info', `getRate(${fromCode}, ${toCode}) = ${rate}`);
  return rate;
}

/**
 * 金额换算
 * @param {number} amount 金额
 * @param {string} from   源货币代码
 * @param {string} to     目标货币代码
 * @returns {Promise<number>} 换算后金额（保留 2 位小数）
 */
async function convertAmount(amount, from, to) {
  if (typeof amount !== 'number' || isNaN(amount)) {
    throw new Error(`Invalid amount: ${amount}`);
  }

  const rate = await getRate(from, to);
  const converted = Math.round(amount * rate * 100) / 100;

  log('info', `convertAmount(${amount} ${from} → ${to}) = ${converted}`);
  return converted;
}

/**
 * 强制刷新汇率（忽略缓存）
 * @returns {Promise<object>} 最新汇率数据
 */
async function refreshRates() {
  if (isDryRun()) {
    log('info', 'Dry-run mode: refresh returns mock rates');
    const mock = { ...MOCK_RATES, fetched_at: new Date().toISOString() };
    writeCache(mock);
    return mock;
  }

  log('info', 'Force refreshing rates from API');
  const fresh = await fetchRatesFromAPI();
  writeCache(fresh);
  return fresh;
}

/**
 * 获取所有支持货币的汇率
 * @returns {Promise<object>} { base, rates, fetched_at, source }
 */
async function getAllRates() {
  return getRatesData();
}

// ========== CLI 支持 ==========

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  try {
    switch (cmd) {
      case 'rate': {
        const [, from, to] = args;
        if (!from || !to) {
          console.log('Usage: exchange-rate.js rate <FROM> <TO>');
          console.log('Example: exchange-rate.js rate USD CNY');
          process.exit(1);
        }
        const rate = await getRate(from, to);
        console.log(`${from.toUpperCase()} → ${to.toUpperCase()}: ${rate}`);
        break;
      }
      case 'convert': {
        const [, amount, from, to] = args;
        if (!amount || !from || !to) {
          console.log('Usage: exchange-rate.js convert <AMOUNT> <FROM> <TO>');
          console.log('Example: exchange-rate.js convert 100 USD CNY');
          process.exit(1);
        }
        const result = await convertAmount(parseFloat(amount), from, to);
        console.log(`${amount} ${from.toUpperCase()} = ${result} ${to.toUpperCase()}`);
        break;
      }
      case 'refresh': {
        const data = await refreshRates();
        console.log('Rates refreshed:');
        console.log(JSON.stringify(data.rates, null, 2));
        break;
      }
      case 'all': {
        const data = await getAllRates();
        console.log(JSON.stringify(data, null, 2));
        break;
      }
      default:
        console.log('Exchange Rate Module');
        console.log('Commands: rate, convert, refresh, all');
        console.log('');
        console.log('  rate <FROM> <TO>             Get exchange rate');
        console.log('  convert <AMOUNT> <FROM> <TO> Convert amount');
        console.log('  refresh                      Force refresh from API');
        console.log('  all                          Show all cached rates');
        console.log('');
        console.log('Env: DRY_RUN=true for mock rates, CACHE_TTL_MS to set cache TTL');
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

// 如果直接运行则进入 CLI 模式
if (require.main === module) {
  cli();
}

// ========== 导出 ==========
module.exports = {
  getRate,
  convertAmount,
  refreshRates,
  getAllRates,
  SUPPORTED_CURRENCIES
};

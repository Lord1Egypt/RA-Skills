/**
 * copper-price-adapter.js
 * 
 * 铜价适配层：读取 copper-price-monitor 输出数据，
 * 计算不同产品 SKU 的铜材料成本。
 * 
 * 薄适配层，不重复实现铜价抓取逻辑。
 * 
 * 环境变量：
 *   DRY_RUN=true     使用模拟铜价（9500 USD/吨）
 *   COPPER_LOG=true   启用日志输出
 * 
 * API 导出：
 *   getCopperPrice()                    获取最新铜价（USD/吨）
 *   getCopperCostForProduct(sku)        计算指定 SKU 的铜材料成本（USD）
 *   getCopperCostBatch(skuList)         批量计算多个 SKU 的铜材料成本
 *   getLastUpdated()                    获取铜价数据最后更新时间
 *   refreshCache()                      强制刷新缓存
 * 
 * CLI 用法：
 *   node copper-price-adapter.js price              查看最新铜价
 *   node copper-price-adapter.js cost <SKU>          查看指定 SKU 铜成本
 *   node copper-price-adapter.js cost-all            查看全部产品铜成本
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ============================================================
// 配置
// ============================================================

const COPPER_MONITOR_OUTPUT_DIR = path.resolve(
  __dirname,
  '../../../copper-price-monitor/output'
);

const PRODUCTS_COST_FILE = path.resolve(
  __dirname,
  '../config/products-cost.json'
);

const CACHE_DIR = path.resolve(__dirname, '../cache');
const LOG_DIR = path.resolve(__dirname, '../logs');

// 默认铜价（离线降级用），单位 USD/吨
const DEFAULT_COPPER_PRICE_USD = 9200;

// 模拟铜价（dry-run 用），单位 USD/吨
const DRY_RUN_COPPER_PRICE_USD = 9500;

// 缓存有效期（毫秒），30 分钟
const CACHE_TTL_MS = 30 * 60 * 1000;

const DRY_RUN = process.env.DRY_RUN === 'true';
const LOG_ENABLED = process.env.COPPER_LOG === 'true';

// ============================================================
// 内存缓存
// ============================================================

let _cache = {
  copperPrice: null,
  source: null,
  timestamp: null,
  cachedAt: null
};

let _productsCache = null;

// ============================================================
// 工具函数
// ============================================================

function log(msg) {
  if (!LOG_ENABLED) return;
  const line = `[${new Date().toISOString()}] [copper-adapter] ${msg}`;
  console.log(line);
  try {
    if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(
      path.join(LOG_DIR, 'copper-adapter.log'),
      line + '\n'
    );
  } catch (_) {
    // 日志写入失败不阻塞主流程
  }
}

function ensureDirs() {
  [CACHE_DIR, LOG_DIR].forEach(d => {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  });
}

// ============================================================
// 读取 copper-price-monitor 输出
// ============================================================

/**
 * 扫描 copper-price-monitor/output/ 目录，
 * 找到最新的 JSON 文件并读取铜价。
 * 
 * 返回 { price: number|null, source: string, timestamp: string, raw: object }
 */
function readLatestCopperData() {
  log(`Scanning output dir: ${COPPER_MONITOR_OUTPUT_DIR}`);

  if (!fs.existsSync(COPPER_MONITOR_OUTPUT_DIR)) {
    log('Output directory not found');
    return null;
  }

  const files = fs.readdirSync(COPPER_MONITOR_OUTPUT_DIR)
    .filter(f => f.startsWith('copper_price_') && f.endsWith('.json'))
    .sort()
    .reverse();

  if (files.length === 0) {
    log('No copper price JSON files found');
    return null;
  }

  const latestFile = path.join(COPPER_MONITOR_OUTPUT_DIR, files[0]);
  log(`Reading latest file: ${files[0]}`);

  try {
    const raw = JSON.parse(fs.readFileSync(latestFile, 'utf-8'));

    // 优先读 LME 价格（USD），其次 SHFE
    let price = null;
    let source = 'unknown';

    if (raw.lme && raw.lme.price !== null && raw.lme.price !== undefined) {
      price = Number(raw.lme.price);
      source = 'LME';
    } else if (raw.shfe && raw.shfe.price !== null && raw.shfe.price !== undefined) {
      // SHFE 是 CNY/吨，需要转换为 USD
      // 粗略汇率 7.25（实际使用时应对接 exchange-rate.js）
      price = Number(raw.shfe.price) / 7.25;
      source = 'SHFE (converted)';
    }

    return {
      price,
      source,
      timestamp: raw.timestamp || new Date().toISOString(),
      raw
    };
  } catch (err) {
    log(`Failed to parse ${files[0]}: ${err.message}`);
    return null;
  }
}

// ============================================================
// 核心 API
// ============================================================

/**
 * 获取最新铜价（USD/吨）
 * 
 * 优先级：
 * 1. DRY_RUN 模式：返回模拟铜价
 * 2. 内存缓存（未过期）
 * 3. copper-price-monitor 输出文件
 * 4. 离线降级：使用默认值
 * 
 * @returns {{ price: number, source: string, currency: string, unit: string, timestamp: string, isDryRun: boolean, isFallback: boolean }}
 */
function getCopperPrice() {
  // DRY_RUN 模式
  if (DRY_RUN) {
    log('DRY_RUN mode: returning mock copper price');
    return {
      price: DRY_RUN_COPPER_PRICE_USD,
      source: 'dry-run',
      currency: 'USD',
      unit: 'per metric ton',
      timestamp: new Date().toISOString(),
      isDryRun: true,
      isFallback: false
    };
  }

  // 检查内存缓存
  if (
    _cache.copperPrice !== null &&
    _cache.cachedAt &&
    Date.now() - _cache.cachedAt < CACHE_TTL_MS
  ) {
    log('Returning cached copper price');
    return {
      price: _cache.copperPrice,
      source: _cache.source,
      currency: 'USD',
      unit: 'per metric ton',
      timestamp: _cache.timestamp,
      isDryRun: false,
      isFallback: false
    };
  }

  // 读取 copper-price-monitor 输出
  const data = readLatestCopperData();

  if (data && data.price !== null && !isNaN(data.price) && data.price > 0) {
    // 更新缓存
    _cache = {
      copperPrice: data.price,
      source: data.source,
      timestamp: data.timestamp,
      cachedAt: Date.now()
    };

    log(`Copper price loaded: $${data.price}/ton from ${data.source}`);
    return {
      price: data.price,
      source: data.source,
      currency: 'USD',
      unit: 'per metric ton',
      timestamp: data.timestamp,
      isDryRun: false,
      isFallback: false
    };
  }

  // 离线降级
  log(`Fallback: using default copper price $${DEFAULT_COPPER_PRICE_USD}/ton`);
  return {
    price: DEFAULT_COPPER_PRICE_USD,
    source: 'fallback (default)',
    currency: 'USD',
    unit: 'per metric ton',
    timestamp: new Date().toISOString(),
    isDryRun: false,
    isFallback: true
  };
}

/**
 * 加载 products-cost.json
 */
function loadProducts() {
  if (_productsCache) return _productsCache;

  if (!fs.existsSync(PRODUCTS_COST_FILE)) {
    throw new Error(`Products cost file not found: ${PRODUCTS_COST_FILE}`);
  }

  const data = JSON.parse(fs.readFileSync(PRODUCTS_COST_FILE, 'utf-8'));
  _productsCache = data.products || [];
  log(`Loaded ${_productsCache.length} products from products-cost.json`);
  return _productsCache;
}

/**
 * 根据产品 SKU 计算铜材料成本（USD）
 * 
 * 铜成本 = 铜价（USD/吨） × 铜用量（kg） / 1000
 * 
 * @param {string} sku 产品 SKU
 * @returns {{ sku: string, copperWeight_kg: number, copperPrice_usd_per_ton: number, copperCost_usd: number, priceSource: string, isDryRun: boolean, isFallback: boolean }}
 */
function getCopperCostForProduct(sku) {
  if (!sku || typeof sku !== 'string') {
    throw new Error('Invalid SKU: must be a non-empty string');
  }

  const products = loadProducts();
  const product = products.find(
    p => p.sku.toLowerCase() === sku.toLowerCase()
  );

  if (!product) {
    throw new Error(`Product not found: ${sku}. Available SKUs: ${products.map(p => p.sku).join(', ')}`);
  }

  const copperWeight = product.copper_weight_kg || 0;
  const priceInfo = getCopperPrice();
  const copperCost = (priceInfo.price * copperWeight) / 1000;

  log(`SKU ${sku}: ${copperWeight}kg × $${priceInfo.price}/ton = $${copperCost.toFixed(4)}`);

  return {
    sku: product.sku,
    model: product.model,
    category: product.category,
    copperWeight_kg: copperWeight,
    copperPrice_usd_per_ton: priceInfo.price,
    copperCost_usd: Math.round(copperCost * 10000) / 10000,
    priceSource: priceInfo.source,
    isDryRun: priceInfo.isDryRun,
    isFallback: priceInfo.isFallback
  };
}

/**
 * 批量计算多个 SKU 的铜材料成本
 * 
 * @param {string[]} skuList SKU 列表，为空则计算全部产品
 * @returns {Array}
 */
function getCopperCostBatch(skuList) {
  const products = loadProducts();
  const targets = skuList && skuList.length > 0
    ? skuList
    : products.map(p => p.sku);

  const results = [];
  const errors = [];

  for (const sku of targets) {
    try {
      results.push(getCopperCostForProduct(sku));
    } catch (err) {
      errors.push({ sku, error: err.message });
    }
  }

  return { results, errors };
}

/**
 * 获取铜价数据最后更新时间
 */
function getLastUpdated() {
  const data = readLatestCopperData();
  if (data) {
    return {
      timestamp: data.timestamp,
      source: data.source,
      hasPrice: data.price !== null && data.price > 0
    };
  }
  return {
    timestamp: null,
    source: null,
    hasPrice: false
  };
}

/**
 * 强制刷新缓存
 */
function refreshCache() {
  _cache = {
    copperPrice: null,
    source: null,
    timestamp: null,
    cachedAt: null
  };
  _productsCache = null;
  log('Cache cleared');

  // 重新加载
  const priceInfo = getCopperPrice();
  return {
    refreshed: true,
    price: priceInfo.price,
    source: priceInfo.source
  };
}

// ============================================================
// CLI 入口
// ============================================================

function cli() {
  const args = process.argv.slice(2);
  const command = args[0];

  ensureDirs();

  switch (command) {
    case 'price': {
      const info = getCopperPrice();
      console.log('\n=== 铜价查询 ===');
      console.log(`价格:    $${info.price.toFixed(2)} USD/吨`);
      console.log(`来源:    ${info.source}`);
      console.log(`时间:    ${info.timestamp}`);
      if (info.isDryRun) console.log(`模式:    DRY_RUN（模拟数据）`);
      if (info.isFallback) console.log(`⚠️  注意: 使用离线默认值`);
      console.log('');
      break;
    }

    case 'cost': {
      const sku = args[1];
      if (!sku) {
        console.error('用法: node copper-price-adapter.js cost <SKU>');
        console.error('示例: node copper-price-adapter.js cost HDMI-2.1-8K-2M');
        process.exit(1);
      }
      try {
        const result = getCopperCostForProduct(sku);
        console.log('\n=== 产品铜成本 ===');
        console.log(`SKU:       ${result.sku}`);
        console.log(`型号:      ${result.model}`);
        console.log(`分类:      ${result.category}`);
        console.log(`铜用量:    ${result.copperWeight_kg} kg`);
        console.log(`铜价:      $${result.copperPrice_usd_per_ton.toFixed(2)} USD/吨`);
        console.log(`铜成本:    $${result.copperCost_usd.toFixed(4)} USD`);
        console.log(`价格来源:  ${result.priceSource}`);
        if (result.isDryRun) console.log(`模式:      DRY_RUN`);
        if (result.isFallback) console.log(`⚠️  注意: 使用离线默认值`);
        console.log('');
      } catch (err) {
        console.error(`错误: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case 'cost-all': {
      const batch = getCopperCostBatch();
      console.log('\n=== 全部产品铜成本 ===\n');

      const priceInfo = getCopperPrice();
      console.log(`铜价: $${priceInfo.price.toFixed(2)} USD/吨 (${priceInfo.source})`);
      if (priceInfo.isDryRun) console.log('模式: DRY_RUN（模拟数据）');
      if (priceInfo.isFallback) console.log('⚠️  使用离线默认值');
      console.log('');

      // 表头
      console.log(
        'SKU'.padEnd(24) +
        '铜用量(kg)'.padEnd(14) +
        '铜成本(USD)'.padEnd(14) +
        '分类'
      );
      console.log('-'.repeat(60));

      for (const r of batch.results) {
        console.log(
          r.sku.padEnd(24) +
          r.copperWeight_kg.toFixed(3).padStart(8).padEnd(14) +
          ('$' + r.copperCost_usd.toFixed(4)).padStart(10).padEnd(14) +
          r.category
        );
      }

      if (batch.errors.length > 0) {
        console.log('\n错误:');
        for (const e of batch.errors) {
          console.log(`  ${e.sku}: ${e.error}`);
        }
      }
      console.log('');
      break;
    }

    default:
      console.log('铜价适配层 (copper-price-adapter.js)');
      console.log('');
      console.log('用法:');
      console.log('  node copper-price-adapter.js price          查看最新铜价');
      console.log('  node copper-price-adapter.js cost <SKU>     查看指定 SKU 铜成本');
      console.log('  node copper-price-adapter.js cost-all       查看全部产品铜成本');
      console.log('');
      console.log('环境变量:');
      console.log('  DRY_RUN=true     使用模拟铜价');
      console.log('  COPPER_LOG=true  启用日志');
      break;
  }
}

// ============================================================
// 导出
// ============================================================

module.exports = {
  getCopperPrice,
  getCopperCostForProduct,
  getCopperCostBatch,
  getLastUpdated,
  refreshCache,
  DEFAULT_COPPER_PRICE_USD,
  DRY_RUN_COPPER_PRICE_USD
};

// CLI 模式
if (require.main === module) {
  cli();
}

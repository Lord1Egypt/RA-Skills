/**
 * price-history.js
 * 
 * 历史报价记录模块：记录每次报价，支持按客户/产品/日期范围查询。
 * 存储格式：JSON Lines (.jsonl)，追加写入。
 * 趋势分析延后到 Phase 4，MVP 只做记录和查询。
 * 
 * 环境变量：
 *   PRICE_HISTORY_FILE   自定义 JSONL 文件路径（默认 output/price-history.jsonl）
 * 
 * API 导出：
 *   recordQuote(record) → 记录ID（如 QH-20260325-001）
 *   queryHistory(filters) → 报价历史数组
 * 
 * CLI 用法：
 *   node price-history.js record '{"sku":"HDMI-2.1-8K-2M","quantity":1000,...}'
 *   node price-history.js query --customer CUST-001 --limit 10
 *   node price-history.js query --sku HDMI-2.1-8K-2M --from 2026-03-01 --to 2026-03-31
 *   node price-history.js query --limit 5
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ============================================================
// 路径配置
// ============================================================

const OUTPUT_DIR = path.resolve(__dirname, '../output');
const DEFAULT_HISTORY_FILE = path.join(OUTPUT_DIR, 'price-history.jsonl');

function getHistoryFile() {
  return process.env.PRICE_HISTORY_FILE || DEFAULT_HISTORY_FILE;
}

// ============================================================
// 日期工具
// ============================================================

/**
 * 获取当前 ISO 时间戳（+08:00）
 */
function nowISO() {
  const now = new Date();
  const offset = 8 * 60;
  const local = new Date(now.getTime() + offset * 60000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${local.getUTCFullYear()}-${pad(local.getUTCMonth() + 1)}-${pad(local.getUTCDate())}T${pad(local.getUTCHours())}:${pad(local.getUTCMinutes())}:${pad(local.getUTCSeconds())}+08:00`;
}

/**
 * 获取当前日期 YYYYMMDD（+08:00）
 */
function todayCompact() {
  const now = new Date();
  const offset = 8 * 60;
  const local = new Date(now.getTime() + offset * 60000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${local.getUTCFullYear()}${pad(local.getUTCMonth() + 1)}${pad(local.getUTCDate())}`;
}

/**
 * 解析日期字符串为 Date 对象（支持 YYYY-MM-DD 和 ISO 格式）
 */
function parseDate(str) {
  if (!str) return null;
  // YYYY-MM-DD → 当天 00:00:00
  if (/^\d{4}-\d{2}-\d{2}$/.test(str)) {
    return new Date(str + 'T00:00:00+08:00');
  }
  return new Date(str);
}

// ============================================================
// 序号管理
// ============================================================

/**
 * 生成唯一记录ID：QH-YYYYMMDD-NNN
 * 通过扫描当天已有记录确定序号
 */
function generateRecordId() {
  const date = todayCompact();
  const prefix = `QH-${date}-`;
  const historyFile = getHistoryFile();
  
  let maxSeq = 0;
  
  if (fs.existsSync(historyFile)) {
    const content = fs.readFileSync(historyFile, 'utf8');
    const lines = content.split('\n').filter(l => l.trim());
    
    for (const line of lines) {
      try {
        const record = JSON.parse(line);
        if (record.id && record.id.startsWith(prefix)) {
          const seq = parseInt(record.id.slice(prefix.length), 10);
          if (seq > maxSeq) maxSeq = seq;
        }
      } catch (e) {
        // 跳过无效行
      }
    }
  }
  
  return `${prefix}${String(maxSeq + 1).padStart(3, '0')}`;
}

// ============================================================
// 核心 API
// ============================================================

/**
 * 记录一条报价
 * 
 * @param {Object} record 报价记录
 * @param {string} record.sku 产品型号
 * @param {number} record.quantity 数量
 * @param {string} record.customerGrade 客户等级（A/B/C/D）
 * @param {string} [record.customerId] 客户ID
 * @param {number} record.unitPrice 单价
 * @param {number} record.totalPrice 总价
 * @param {string} record.currency 币种（USD/EUR/GBP/CNY）
 * @param {number} record.marginRate 利润率（0.15 = 15%）
 * @param {string} record.method 定价方式（formula/override）
 * @returns {string} 记录ID（如 QH-20260325-001）
 */
function recordQuote(record) {
  // 参数验证
  if (!record || typeof record !== 'object') {
    throw new Error('record 必须是一个对象');
  }
  
  const required = ['sku', 'quantity', 'unitPrice', 'totalPrice', 'currency'];
  for (const field of required) {
    if (record[field] === undefined || record[field] === null) {
      throw new Error(`缺少必填字段: ${field}`);
    }
  }
  
  if (typeof record.quantity !== 'number' || record.quantity <= 0) {
    throw new Error('quantity 必须是正数');
  }
  
  if (typeof record.unitPrice !== 'number' || record.unitPrice <= 0) {
    throw new Error('unitPrice 必须是正数');
  }
  
  if (typeof record.totalPrice !== 'number' || record.totalPrice <= 0) {
    throw new Error('totalPrice 必须是正数');
  }
  
  const validCurrencies = ['USD', 'EUR', 'GBP', 'CNY'];
  const currency = (record.currency || '').toUpperCase();
  if (!validCurrencies.includes(currency)) {
    throw new Error(`不支持的币种: ${record.currency}，支持: ${validCurrencies.join('/')}`);
  }
  
  // 生成记录
  const id = generateRecordId();
  const timestamp = nowISO();
  
  const entry = {
    id,
    timestamp,
    sku: record.sku,
    quantity: record.quantity,
    customerGrade: record.customerGrade || null,
    customerId: record.customerId || null,
    unitPrice: record.unitPrice,
    totalPrice: record.totalPrice,
    currency: currency,
    marginRate: record.marginRate !== undefined ? record.marginRate : null,
    method: record.method || 'unknown'
  };
  
  // 确保输出目录存在
  const historyFile = getHistoryFile();
  const dir = path.dirname(historyFile);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // 追加写入 JSONL
  fs.appendFileSync(historyFile, JSON.stringify(entry) + '\n', 'utf8');
  
  return id;
}

/**
 * 查询报价历史
 * 
 * @param {Object} [filters] 过滤条件
 * @param {string} [filters.customerId] 按客户ID过滤
 * @param {string} [filters.sku] 按产品型号过滤（不区分大小写）
 * @param {string} [filters.dateFrom] 起始日期（YYYY-MM-DD 或 ISO）
 * @param {string} [filters.dateTo] 截止日期（YYYY-MM-DD 或 ISO）
 * @param {number} [filters.limit] 最大返回条数（默认全部）
 * @returns {Array} 报价历史数组（按时间倒序）
 */
function queryHistory(filters = {}) {
  const historyFile = getHistoryFile();
  
  if (!fs.existsSync(historyFile)) {
    return [];
  }
  
  const content = fs.readFileSync(historyFile, 'utf8');
  const lines = content.split('\n').filter(l => l.trim());
  
  let records = [];
  for (const line of lines) {
    try {
      records.push(JSON.parse(line));
    } catch (e) {
      // 跳过无效行
    }
  }
  
  // 按时间倒序
  records.sort((a, b) => {
    const ta = new Date(a.timestamp).getTime();
    const tb = new Date(b.timestamp).getTime();
    return tb - ta;
  });
  
  // 过滤：customerId
  if (filters.customerId) {
    records = records.filter(r => r.customerId === filters.customerId);
  }
  
  // 过滤：sku（不区分大小写）
  if (filters.sku) {
    const skuUpper = filters.sku.toUpperCase();
    records = records.filter(r => (r.sku || '').toUpperCase() === skuUpper);
  }
  
  // 过滤：dateFrom
  if (filters.dateFrom) {
    const from = parseDate(filters.dateFrom);
    if (from && !isNaN(from.getTime())) {
      records = records.filter(r => new Date(r.timestamp) >= from);
    }
  }
  
  // 过滤：dateTo
  if (filters.dateTo) {
    const to = parseDate(filters.dateTo);
    if (to && !isNaN(to.getTime())) {
      // dateTo 包含当天，设为当天 23:59:59
      const toEnd = new Date(to.getTime() + 24 * 60 * 60 * 1000 - 1);
      records = records.filter(r => new Date(r.timestamp) <= toEnd);
    }
  }
  
  // 限制条数
  if (filters.limit && typeof filters.limit === 'number' && filters.limit > 0) {
    records = records.slice(0, filters.limit);
  }
  
  return records;
}

// ============================================================
// CLI
// ============================================================

function printUsage() {
  console.log(`
使用方法：
  node price-history.js record '{"sku":"HDMI-2.1-8K-2M","quantity":1000,"unitPrice":4.49,"totalPrice":4490,"currency":"USD","customerGrade":"B","customerId":"CUST-001","marginRate":0.1937,"method":"formula"}'
  node price-history.js query --customer CUST-001 --limit 10
  node price-history.js query --sku HDMI-2.1-8K-2M --from 2026-03-01 --to 2026-03-31
  node price-history.js query --limit 5
  `.trim());
}

function parseCLIArgs(args) {
  const result = {};
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === '--customer' && i + 1 < args.length) {
      result.customerId = args[++i];
    } else if (arg === '--sku' && i + 1 < args.length) {
      result.sku = args[++i];
    } else if (arg === '--from' && i + 1 < args.length) {
      result.dateFrom = args[++i];
    } else if (arg === '--to' && i + 1 < args.length) {
      result.dateTo = args[++i];
    } else if (arg === '--limit' && i + 1 < args.length) {
      result.limit = parseInt(args[++i], 10);
    }
    i++;
  }
  return result;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command || command === '--help' || command === '-h') {
    printUsage();
    process.exit(0);
  }
  
  if (command === 'record') {
    const jsonStr = args[1];
    if (!jsonStr) {
      console.error('错误: record 命令需要 JSON 参数');
      printUsage();
      process.exit(1);
    }
    
    try {
      const record = JSON.parse(jsonStr);
      const id = recordQuote(record);
      console.log(JSON.stringify({ success: true, id, message: `报价已记录: ${id}` }, null, 2));
    } catch (e) {
      console.error(JSON.stringify({ success: false, error: e.message }, null, 2));
      process.exit(1);
    }
  } else if (command === 'query') {
    const filters = parseCLIArgs(args.slice(1));
    
    try {
      const results = queryHistory(filters);
      console.log(JSON.stringify({
        success: true,
        count: results.length,
        filters,
        records: results
      }, null, 2));
    } catch (e) {
      console.error(JSON.stringify({ success: false, error: e.message }, null, 2));
      process.exit(1);
    }
  } else {
    console.error(`未知命令: ${command}`);
    printUsage();
    process.exit(1);
  }
}

// ============================================================
// 模块导出
// ============================================================

module.exports = {
  recordQuote,
  queryHistory
};

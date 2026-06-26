const moment = require('moment');

// 缓存管理
const cache = new Map();
const CACHE_EXPIRY = 3600000; // 1小时缓存

function getCache(key) {
  const item = cache.get(key);
  if (!item) return null;
  
  const { data, timestamp } = item;
  if (Date.now() - timestamp > CACHE_EXPIRY) {
    cache.delete(key);
    return null;
  }
  
  return data;
}

function setCache(key, data) {
  cache.set(key, {
    data,
    timestamp: Date.now()
  });
}

// 日志处理
function log(level, message, data = {}) {
  const timestamp = moment().format('YYYY-MM-DD HH:mm:ss');
  console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`, data);
}

function validateParams(params) {
  const errors = [];
  
  if (!params || typeof params !== 'object') {
    errors.push('参数必须是对象');
    return errors;
  }
  
  if (!params.type) {
    errors.push('必须指定数据类型 type');
  } else {
    const validTypes = ['market', 'finance', 'fund_flow', 'public_opinion', 'stock_codes', 
                        'batch_sentiment', 'batch_market', 'batch_lhb', 'batch_north_flow', 'batch_financial'];
    if (!validTypes.includes(params.type)) {
      errors.push(`type 必须是 ${validTypes.join('、')} 之一`);
    }
  }
  
  const batchTypes = ['batch_sentiment', 'batch_market', 'batch_lhb', 'batch_north_flow', 'batch_financial', 'stock_codes'];
  if (!batchTypes.includes(params.type) && !params.symbol) {
    errors.push('必须指定标的代码 symbol');
  }
  
  if (params.type === 'market' && params.period && !['1m', '5m', '15m', '30m', '60m', '1d', '1w', '1M'].includes(params.period)) {
    errors.push('period 必须是 1m、5m、15m、30m、60m、1d、1w 或 1M');
  }
  
  if (params.type === 'finance' && params.report_type && !['quarter', 'year'].includes(params.report_type)) {
    errors.push('report_type 必须是 quarter 或 year');
  }
  
  return errors;
}

// 格式化日期
function formatDate(date) {
  return moment(date).format('YYYY-MM-DD');
}

// 格式化时间
function formatDateTime(date) {
  return moment(date).format('YYYY-MM-DD HH:mm:ss');
}

module.exports = {
  getCache,
  setCache,
  log,
  validateParams,
  formatDate,
  formatDateTime
};

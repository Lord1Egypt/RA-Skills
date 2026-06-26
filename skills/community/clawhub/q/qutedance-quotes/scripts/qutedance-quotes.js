#!/usr/bin/env node

/**
 * Qutedance Quotes Skill
 *
 * 利用 quotedance-service 提供的行情 API：
 * - 查看 A 股 / 期货 / 港股 实时报价
 * - 查看 A 股板块热门信息（涨跌幅榜单）
 *
 * 基础 API 参考：project/quotedance-service/docs/api.md
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.resolve(__dirname, '..');
const CONFIG = require(path.join(SKILL_DIR, 'config.json'));

const SERVICE_URL =
  CONFIG.serviceUrl ||
  'http://localhost:5000';

// API Key：优先使用 config.json 里的 apiKey，其次才看环境变量
// 这样对你来说“看文件就会改”，更简单易学
const API_KEY =
  CONFIG.apiKey ||
  process.env.QUTEDANCE_API_KEY ||
  '';

function log(msg) {
  const ts = new Date().toISOString();
  console.log('[' + ts + '] ' + msg);
}

async function fetchJson(pathname, params = {}) {
  const url = new URL(SERVICE_URL.replace(/\/+$/, '') + pathname);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      url.searchParams.set(key, String(value));
    }
  });

  const headers = {
    Accept: 'application/json'
  };

  if (API_KEY) {
    // quotedance-service 目前支持通过 X-API-Key 进行鉴权
    headers['X-API-Key'] = API_KEY;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const res = await fetch(url.toString(), {
      method: 'GET',
      headers,
      signal: controller.signal
    });
    clearTimeout(timeout);

    if (!res.ok) {
      throw new Error('HTTP ' + res.status + ' ' + (await res.text()));
    }
    return await res.json();
  } catch (e) {
    clearTimeout(timeout);
    throw e;
  }
}

function formatPercent(x) {
  if (x === null || x === undefined || isNaN(x)) return 'N/A';
  const pct = x * 100;
  const sign = pct > 0 ? '+' : '';
  return sign + pct.toFixed(2) + '%';
}

function formatNumber(x, digits = 2) {
  if (x === null || x === undefined || isNaN(x)) return 'N/A';
  return Number(x).toFixed(digits);
}

async function getQuotes(list, type) {
  const data = await fetchJson('/quotes/', {
    list,
    type
  });

  const codes = list.split(',').map(s => s.trim()).filter(Boolean);
  const lines = [];

  lines.push('### 行情报价');
  lines.push('');
  lines.push('| 代码 | 名称 | 最新价 | 涨跌幅 | 最高 | 最低 | 买一 | 卖一 |');
  lines.push('|------|------|--------|--------|------|------|------|------|');

  codes.forEach(code => {
    const q = data[code];
    if (!q) {
      lines.push(`| ${code} | - | - | - | - | - | - | - |`);
      return;
    }

    if (type === 'cn' || type === 'hk') {
      const now = q.now ?? q.current;
      const change =
        q.close && now ? (now - q.close) / q.close : undefined;
      lines.push(
        `| ${code} | ${q.name || ''} | ${formatNumber(now)} | ${formatPercent(
          change
        )} | ${formatNumber(q.high)} | ${formatNumber(
          q.low
        )} | ${formatNumber(q.buy)} | ${formatNumber(q.sell)} |`
      );
    } else {
      // futures
      const now = q.current;
      const change = q.change; // 已经是比例
      lines.push(
        `| ${code} | ${q.name || q.commodity_name || ''} | ${formatNumber(
          now
        )} | ${formatPercent(change)} | ${formatNumber(
          q.high
        )} | ${formatNumber(q.low)} | ${formatNumber(
          q.buy
        )} | ${formatNumber(q.sell)} |`
      );
    }
  });

  return lines.join('\n');
}

async function getPlateTopInfo(count) {
  const data = await fetchJson('/quotes/plate-top-info', {
    count: count || CONFIG.defaults.topPlatesCount || 10
  });

  const plates = data.plates || [];
  if (!plates.length) return '当前没有获取到板块数据。';

  const lines = [];
  lines.push('### A股板块涨跌幅榜');
  lines.push('');

  plates.forEach(plate => {
    const name = plate.plate_name;
    const pct = plate.core_avg_pcp;
    const pctStr = formatPercent(pct);
    const direction = pct > 0 ? '🚀 领涨' : pct < 0 ? '📉 领跌' : '⚖️ 平稳';
    lines.push(`- ${direction} 板块：**${name}**（平均涨跌幅：${pctStr}）`);

    const risers = plate.led_rising_stocks || [];
    const fallers = plate.led_falling_stocks || [];

    if (risers.length) {
      const r = risers[0];
      lines.push(
        `  - 领涨：${r.stock_chi_name} (${r.symbol}) ${formatPercent(
          r.change_percent
        )}，价格变动 ${formatNumber(r.price_change)}`
      );
    }
    if (fallers.length) {
      const f = fallers[0];
      lines.push(
        `  - 领跌：${f.stock_chi_name} (${f.symbol}) ${formatPercent(
          f.change_percent
        )}，价格变动 ${formatNumber(f.price_change)}`
      );
    }
    lines.push('');
  });

  return lines.join('\n');
}

async function searchQuotes(query, type, limit) {
  const data = await fetchJson('/quotes/search', {
    q: query || '',
    type: type || 'all',
    limit: limit || 20
  });

  if (!Array.isArray(data) || data.length === 0) {
    return '未找到匹配的标的。';
  }

  const lines = [];
  lines.push('### 标的搜索结果');
  lines.push('');
  lines.push('| 代码 | 名称 | 市场 | 交易所 |');
  lines.push('|------|------|------|--------|');

  data.forEach(item => {
    lines.push(
      `| ${item.code || '-'} | ${item.name || '-'} | ${item.market || '-'} | ${item.exchange || '-'} |`
    );
  });

  return lines.join('\n');
}

async function main() {
  const args = process.argv.slice(2);

  let mode = 'quotes'; // 'quotes' | 'plates' | 'search'
  let type = CONFIG.defaults.type || 'cn';
  let list = '';
  let platesCount = CONFIG.defaults.topPlatesCount || 10;
  let searchQuery = '';
  let searchLimit = 20;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--type' && i + 1 < args.length) {
      type = args[++i];
    } else if (arg === '--list' && i + 1 < args.length) {
      list = args[++i];
    } else if ((arg === '--search' || arg === '-s')) {
      mode = 'search';
    } else if ((arg === '--q' || arg === '--query') && i + 1 < args.length) {
      searchQuery = args[++i];
    } else if (arg === '--limit' && i + 1 < args.length) {
      searchLimit = parseInt(args[++i], 10) || searchLimit;
    } else if (arg === '--plates') {
      mode = 'plates';
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        platesCount = parseInt(args[++i], 10) || platesCount;
      }
    }
  }

  try {
    if (mode === 'plates') {
      log('获取 A 股板块热门信息...');
      const out = await getPlateTopInfo(platesCount);
      console.log(out);
      return;
    }

    if (mode === 'search') {
      log('搜索标的...');
      const out = await searchQuotes(searchQuery, type, searchLimit);
      console.log(out);
      return;
    }

    if (!list) {
      console.error(
        '用法示例：\n' +
          '  查看 A 股: node qutedance-quotes.js --type cn --list 000001,600000\n' +
          '  查看期货: node qutedance-quotes.js --type futures --list M2605,RB2605\n' +
        '  查看板块榜单: node qutedance-quotes.js --plates 10\n' +
        '  搜索标的: node qutedance-quotes.js --search --q 平安 --type cn --limit 10'
      );
      process.exit(1);
    }

    log(`获取 ${type} 行情，代码：${list}`);
    const out = await getQuotes(list, type);
    console.log(out);
  } catch (e) {
    console.error('获取行情数据失败：', e.message || e);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  getQuotes,
  getPlateTopInfo,
  searchQuotes,
  main
};


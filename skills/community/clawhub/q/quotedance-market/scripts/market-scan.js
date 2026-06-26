#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const CONFIG = require('../config.json');
const SKILL_DIR = path.resolve(__dirname, '..');
const MEMORY_DIR = path.join(SKILL_DIR, 'memory');
const NEWS_CACHE_FILE = path.join(MEMORY_DIR, 'source-cache.json');
const NETWORK = CONFIG.network || {};

const DEFAULT_PROXY_DOMAINS = [
  'finance.yahoo.com',
  'query1.finance.yahoo.com',
  'query2.finance.yahoo.com',
  'news.google.com',
  'bloomberg.com',
  'reuters.com',
  'wallstreetcn.com',
  'jin10.com',
  'coindesk.com',
  'theblock.co'
];

const PROXY_URL =
  NETWORK.proxyUrl ||
  process.env.HTTPS_PROXY ||
  process.env.HTTP_PROXY ||
  process.env.ALL_PROXY ||
  '';

const REQUEST_TIMEOUT_MS = Number(NETWORK.timeoutMs) || 25000;
const REQUEST_RETRIES = Number(NETWORK.requestRetries) || 2;
const ENABLE_CURL_FALLBACK = NETWORK.enableCurlFallback !== false;

let proxyDispatcher = null;
try {
  const undici = require('undici');
  if (PROXY_URL && undici && undici.ProxyAgent) {
    proxyDispatcher = new undici.ProxyAgent(PROXY_URL);
  }
} catch {}

if (!fs.existsSync(MEMORY_DIR)) {
  fs.mkdirSync(MEMORY_DIR, { recursive: true });
}

function log(msg) {
  const ts = new Date().toISOString();
  console.log('[' + ts + '] ' + msg);
}

function formatDate(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + d;
}

function formatDateTime(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  const h = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  return y + '-' + m + '-' + d + ' ' + h + ':' + min;
}

function isWeekend(date = new Date()) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

function toNumber(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function formatPrice(v) {
  const n = toNumber(v);
  if (n === null) return '-';
  return n.toLocaleString('zh-CN', { maximumFractionDigits: 4 });
}

function formatPercentValue(v) {
  const n = toNumber(v);
  if (n === null) return '-';
  return (n > 0 ? '+' : '') + n.toFixed(2) + '%';
}

function formatPercentRatio(v) {
  const n = toNumber(v);
  if (n === null) return '-';
  return formatPercentValue(n * 100);
}

function iconByValue(v) {
  const n = toNumber(v);
  if (n === null) return '⚪';
  if (n > 0) return '🟢';
  if (n < 0) return '🔴';
  return '⚪';
}

function shouldUseProxy(url) {
  if (!PROXY_URL) return false;
  if (NETWORK.useProxy === true) return true;
  if (NETWORK.useProxy === false) return false;
  try {
    const host = new URL(url).hostname.toLowerCase();
    const domains = Array.isArray(NETWORK.forceProxyDomains) && NETWORK.forceProxyDomains.length
      ? NETWORK.forceProxyDomains
      : DEFAULT_PROXY_DOMAINS;
    return domains.some(domain => host.includes(String(domain).toLowerCase()));
  } catch {
    return false;
  }
}

function fetchWithTimeout(url, headers, timeoutMs, useProxy) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  const options = {
    method: 'GET',
    headers,
    signal: controller.signal
  };
  if (useProxy && proxyDispatcher) {
    options.dispatcher = proxyDispatcher;
  }
  return fetch(url, options)
    .then(async res => {
      clearTimeout(timeout);
      if (!res.ok) {
        throw new Error('HTTP ' + res.status + ' ' + (await res.text()));
      }
      return res;
    })
    .catch(e => {
      clearTimeout(timeout);
      throw e;
    });
}

function curlFetch(url, headers, timeoutMs) {
  const args = ['-L', '--max-time', String(Math.max(5, Math.ceil(timeoutMs / 1000))), url];
  Object.entries(headers || {}).forEach(([k, v]) => {
    args.push('-H', k + ': ' + v);
  });
  if (PROXY_URL) {
    args.push('--proxy', PROXY_URL);
  }
  return execFileSync('curl', args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe']
  });
}

async function fetchJson(url, headers = {}, timeoutMs = REQUEST_TIMEOUT_MS) {
  const useProxy = shouldUseProxy(url);
  const maxTry = Math.max(1, REQUEST_RETRIES + 1);
  let lastError = null;
  for (let i = 0; i < maxTry; i++) {
    try {
      const res = await fetchWithTimeout(url, headers, timeoutMs, useProxy);
      return await res.json();
    } catch (e) {
      lastError = e;
      if (i < maxTry - 1) {
        await new Promise(r => setTimeout(r, 300 * (i + 1)));
      }
    }
  }
  if (ENABLE_CURL_FALLBACK) {
    try {
      const body = curlFetch(url, headers, timeoutMs);
      return JSON.parse(body);
    } catch (e) {
      lastError = e;
    }
  }
  throw lastError || new Error('fetch json failed');
}

async function fetchText(url, headers = {}, timeoutMs = REQUEST_TIMEOUT_MS) {
  const useProxy = shouldUseProxy(url);
  const maxTry = Math.max(1, REQUEST_RETRIES + 1);
  let lastError = null;
  for (let i = 0; i < maxTry; i++) {
    try {
      const res = await fetchWithTimeout(url, headers, timeoutMs, useProxy);
      return await res.text();
    } catch (e) {
      lastError = e;
      if (i < maxTry - 1) {
        await new Promise(r => setTimeout(r, 300 * (i + 1)));
      }
    }
  }
  if (ENABLE_CURL_FALLBACK) {
    try {
      return curlFetch(url, headers, timeoutMs);
    } catch (e) {
      lastError = e;
    }
  }
  throw lastError || new Error('fetch text failed');
}

function getServiceUrl() {
  return String(CONFIG.serviceUrl || 'http://localhost:5000').replace(/\/+$/, '');
}

function getApiHeaders() {
  const headers = { Accept: 'application/json' };
  const key = CONFIG.apiKey || process.env.QUTEDANCE_API_KEY || '';
  if (key) headers['X-API-Key'] = key;
  return headers;
}

async function fetchQuotedance(pathname, params = {}) {
  const url = new URL(getServiceUrl() + pathname);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      url.searchParams.set(k, String(v));
    }
  });
  return fetchJson(url.toString(), getApiHeaders(), 30000);
}

async function fetchYahooQuote(symbol) {
  const url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols=' + encodeURIComponent(symbol);
  const data = await fetchJson(
    url,
    {
      Accept: 'application/json',
      'User-Agent': 'Mozilla/5.0'
    },
    15000
  );
  const item = data?.quoteResponse?.result?.[0];
  if (item) {
    return {
      symbol: item.symbol || symbol,
      name: item.longName || item.shortName || symbol,
      price: toNumber(item.regularMarketPrice),
      changePercent: toNumber(item.regularMarketChangePercent)
    };
  }
  const chartUrl =
    'https://query2.finance.yahoo.com/v8/finance/chart/' +
    encodeURIComponent(symbol) +
    '?range=1d&interval=1d';
  const chartData = await fetchJson(
    chartUrl,
    {
      Accept: 'application/json',
      'User-Agent': 'Mozilla/5.0'
    },
    15000
  );
  const meta = chartData?.chart?.result?.[0]?.meta;
  if (!meta) return null;
  const regular = toNumber(meta.regularMarketPrice);
  const prev = toNumber(meta.previousClose);
  const changePercent = regular !== null && prev ? ((regular - prev) / prev) * 100 : null;
  return {
    symbol: meta.symbol || symbol,
    name: meta.shortName || symbol,
    price: regular,
    changePercent
  };
}

async function fetchStooqQuote(symbol) {
  if (!symbol || symbol.startsWith('^')) return null;
  const stooqSymbol = symbol.toLowerCase() + '.us';
  const url = 'https://stooq.com/q/l/?s=' + encodeURIComponent(stooqSymbol) + '&f=sd2t2ohlcvn&e=csv';
  const csv = await fetchText(
    url,
    {
      Accept: 'text/plain',
      'User-Agent': 'Mozilla/5.0'
    },
    15000
  );
  const lines = String(csv || '').trim().split('\n');
  if (lines.length < 2) return null;
  const parts = lines[1].split(',');
  if (parts.length < 7) return null;
  const close = toNumber(parts[6]);
  if (close === null) return null;
  return {
    symbol,
    name: symbol,
    price: close,
    changePercent: null
  };
}

async function fetchUsMarkets() {
  const symbols = Array.isArray(CONFIG.watchlist?.us) ? CONFIG.watchlist.us : [];
  const out = [];
  const missing = [];
  for (const symbol of symbols) {
    try {
      const one = await fetchYahooQuote(symbol);
      if (one) {
        out.push(one);
      } else {
        missing.push(symbol);
      }
    } catch (e) {
      log('Yahoo 获取失败: ' + symbol + ' - ' + (e.message || e));
      missing.push(symbol);
    }
  }

  if (missing.length) {
    const usSymbols = missing.filter(s => !s.startsWith('^'));
    if (usSymbols.length) {
      try {
        const payload = await fetchQuotedance('/quotes/', {
          type: 'us',
          list: usSymbols.join(',')
        });
        usSymbols.forEach(symbol => {
          const q = payload ? payload[symbol] : null;
          if (!q) return;
          const now = toNumber(q.now ?? q.current);
          const close = toNumber(q.close);
          const changePercent = now !== null && close ? ((now - close) / close) * 100 : null;
          if (now !== null) {
            out.push({
              symbol,
              name: q.name || symbol,
              price: now,
              changePercent
            });
          }
        });
      } catch (e) {
        log('quotedance 美股兜底失败: ' + (e.message || e));
      }
    }
  }

  if (missing.length) {
    for (const symbol of missing) {
      const exists = out.some(item => item.symbol === symbol);
      if (exists) continue;
      try {
        const one = await fetchStooqQuote(symbol);
        if (one) {
          out.push(one);
        } else {
          log('Stooq 无可用数据: ' + symbol);
        }
      } catch (e) {
        log('Stooq 获取失败: ' + symbol + ' - ' + (e.message || e));
      }
    }
  }
  return out;
}

async function fetchQuotedanceQuotes(type, symbols) {
  if (!symbols.length) return [];
  const payload = await fetchQuotedance('/quotes/', {
    type,
    list: symbols.join(',')
  });
  return symbols.map(symbol => {
    const q = payload ? payload[symbol] : null;
    if (!q) return null;
    if (type === 'futures') {
      return {
        symbol,
        name: q.name || q.commodity_name || symbol,
        price: toNumber(q.current),
        changeRatio: toNumber(q.change)
      };
    }
    const now = toNumber(q.now ?? q.current);
    const close = toNumber(q.close);
    const changeRatio = now !== null && close ? (now - close) / close : null;
    return {
      symbol,
      name: q.name || symbol,
      price: now,
      changeRatio
    };
  }).filter(Boolean);
}

async function fetchPlateLeaders() {
  const count = Number(CONFIG.defaults?.plateTopCount) || 10;
  const payload = await fetchQuotedance('/quotes/plate-top-info', { count });
  return Array.isArray(payload?.plates) ? payload.plates : [];
}

function decodeHtml(text) {
  return String(text || '')
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)));
}

function readNewsCache(ttlMinutes) {
  if (!fs.existsSync(NEWS_CACHE_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(NEWS_CACHE_FILE, 'utf-8'));
    if (!data || !data.timestamp || !Array.isArray(data.news)) return null;
    const ts = new Date(data.timestamp);
    if (isNaN(ts.getTime())) return null;
    const ttlMs = ttlMinutes * 60 * 1000;
    if (ttlMs > 0 && Date.now() - ts.getTime() > ttlMs) return null;
    return data.news;
  } catch {
    return null;
  }
}

function writeNewsCache(news) {
  const payload = {
    timestamp: new Date().toISOString(),
    news: Array.isArray(news) ? news : []
  };
  fs.writeFileSync(NEWS_CACHE_FILE, JSON.stringify(payload, null, 2), 'utf-8');
}

function pickRssTag(block, tagName) {
  const re = new RegExp('<' + tagName + '(?:\\s[^>]*)?>([\\s\\S]*?)<\\/' + tagName + '>', 'i');
  const m = block.match(re);
  return m ? decodeHtml(m[1].trim()) : '';
}

function parseRssItems(xmlText, sourceName, itemLimit) {
  const xml = String(xmlText || '');
  const items = xml.match(/<item\b[\s\S]*?<\/item>/gi) || [];
  return items.slice(0, itemLimit).map(block => {
    const title = pickRssTag(block, 'title') || '（无标题）';
    const link = pickRssTag(block, 'link');
    const pubDate = pickRssTag(block, 'pubDate') || pickRssTag(block, 'dc:date');
    return {
      source: sourceName,
      title,
      link,
      publishedAt: pubDate
    };
  });
}

async function fetchProfessionalNews(refresh = false) {
  const newsCount = Number(CONFIG.defaults?.newsCount) || 10;
  const ttl = Number(CONFIG.defaults?.sourceCacheTtlMinutes) || 15;
  if (!refresh) {
    const cached = readNewsCache(ttl);
    if (cached) {
      log('命中资讯缓存');
      return cached.slice(0, newsCount);
    }
  }

  const feeds = [
    {
      source: 'Bloomberg',
      urls: [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://news.google.com/rss/search?q=Bloomberg+market&hl=en-US&gl=US&ceid=US:en'
      ]
    },
    {
      source: 'Reuters',
      urls: [
        'https://feeds.reuters.com/reuters/businessNews',
        'https://news.google.com/rss/search?q=Reuters+markets&hl=en-US&gl=US&ceid=US:en'
      ]
    },
    {
      source: '华尔街见闻',
      urls: [
        'https://wallstreetcn.com/rss',
        'https://news.google.com/rss/search?q=%E5%8D%8E%E5%B0%94%E8%A1%97%E8%A7%81%E9%97%BB&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
      ]
    },
    {
      source: '金十数据',
      urls: [
        'https://www.jin10.com/rss',
        'https://news.google.com/rss/search?q=%E9%87%91%E5%8D%81%E6%95%B0%E6%8D%AE&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'
      ]
    },
    {
      source: 'CoinDesk',
      urls: ['https://www.coindesk.com/arc/outboundfeeds/rss/']
    },
    {
      source: 'The Block',
      urls: ['https://www.theblock.co/rss.xml']
    }
  ];

  const combined = [];
  for (const feed of feeds) {
    let ok = false;
    let lastError = null;
    for (const url of feed.urls) {
      try {
        const xml = await fetchText(url, {
          Accept: 'application/rss+xml, application/xml, text/xml',
          'User-Agent': 'Mozilla/5.0'
        }, 15000);
        const parsed = parseRssItems(xml, feed.source, 4);
        if (parsed.length) {
          combined.push(...parsed);
          ok = true;
          break;
        }
      } catch (e) {
        lastError = e;
      }
    }
    if (!ok && lastError) {
      log('资讯源获取失败: ' + feed.source + ' - ' + (lastError.message || lastError));
    }
  }

  const deduped = [];
  const seen = new Set();
  for (const n of combined) {
    const key = (n.link || '') + '|' + (n.title || '');
    if (!key.trim() || seen.has(key)) continue;
    seen.add(key);
    deduped.push(n);
  }
  writeNewsCache(deduped);
  return deduped.slice(0, newsCount);
}

function analyzeOpportunities(data) {
  const targetCount = Number(CONFIG.defaults?.opportunityCount) || 5;
  const opportunities = [];
  const risks = [];

  data.us.forEach(item => {
    const p = toNumber(item.changePercent);
    if (p === null) return;
    if (p >= 2) {
      opportunities.push('美股动能：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    } else if (p <= -2) {
      risks.push('美股回撤：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    }
  });

  data.cn.forEach(item => {
    const r = toNumber(item.changeRatio);
    if (r === null) return;
    const p = r * 100;
    if (p >= 1.5) {
      opportunities.push('A股走强：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    } else if (p <= -1.5) {
      risks.push('A股承压：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    }
  });

  data.futures.forEach(item => {
    const r = toNumber(item.changeRatio);
    if (r === null) return;
    const p = r * 100;
    if (p >= 2) {
      opportunities.push('期货趋势：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    } else if (p <= -2) {
      risks.push('期货波动：' + item.name + ' (' + item.symbol + ') ' + formatPercentValue(p));
    }
  });

  data.plates.slice(0, 3).forEach(plate => {
    const p = toNumber(plate.core_avg_pcp);
    if (p === null) return;
    if (p > 0) {
      opportunities.push('板块强势：' + plate.plate_name + ' ' + formatPercentRatio(p));
    }
  });
  data.plates.slice(-3).forEach(plate => {
    const p = toNumber(plate.core_avg_pcp);
    if (p === null) return;
    if (p < 0) {
      risks.push('板块回撤：' + plate.plate_name + ' ' + formatPercentRatio(p));
    }
  });

  return {
    opportunities: opportunities.slice(0, targetCount),
    risks: risks.slice(0, Math.max(targetCount, 5))
  };
}

function detectThemes(news) {
  const themes = {
    ai: 0,
    macro: 0,
    geo: 0
  };
  news.forEach(item => {
    const t = (item.title || '').toLowerCase();
    if (/ai|artificial intelligence|chip|nvidia|semiconductor|科技|算力/.test(t)) themes.ai += 1;
    if (/fed|ecb|pmi|cpi|inflation|rate|央行|利率|通胀|政策/.test(t)) themes.macro += 1;
    if (/war|tariff|sanction|oil|middle east|地缘|冲突|制裁/.test(t)) themes.geo += 1;
  });
  return themes;
}

function buildGlobalMarketSection(data) {
  const lines = [];
  lines.push('## 🌍 全球市场状态');
  lines.push('');
  lines.push('### 美股');
  if (!data.us.length) {
    lines.push('- 暂无数据');
  } else {
    data.us.forEach(item => {
      lines.push('- ' + iconByValue(item.changePercent) + ' ' + item.name + ' (' + item.symbol + ') ' + formatPrice(item.price) + ' ' + formatPercentValue(item.changePercent));
    });
  }
  lines.push('');
  lines.push('### A股');
  if (!data.cn.length) {
    lines.push('- 暂无数据');
  } else {
    data.cn.forEach(item => {
      const p = toNumber(item.changeRatio);
      lines.push('- ' + iconByValue(p) + ' ' + item.name + ' (' + item.symbol + ') ' + formatPrice(item.price) + ' ' + formatPercentRatio(item.changeRatio));
    });
  }
  lines.push('');
  lines.push('### 期货');
  if (!data.futures.length) {
    lines.push('- 暂无数据');
  } else {
    data.futures.forEach(item => {
      const p = toNumber(item.changeRatio);
      lines.push('- ' + iconByValue(p) + ' ' + item.name + ' (' + item.symbol + ') ' + formatPrice(item.price) + ' ' + formatPercentRatio(item.changeRatio));
    });
  }
  lines.push('');
  lines.push('### A股板块涨跌幅榜');
  if (!data.plates.length) {
    lines.push('- 暂无数据');
  } else {
    data.plates.forEach(plate => {
      lines.push('- ' + plate.plate_name + '：' + formatPercentRatio(plate.core_avg_pcp));
    });
  }
  lines.push('');
  return lines.join('\n');
}

function generateWeekdayReport(snapshot) {
  const now = new Date();
  const themes = detectThemes(snapshot.news);
  const lines = [];
  lines.push('📈 市场情报日报 | ' + formatDate(now));
  lines.push('更新时间：' + formatDateTime(now));
  lines.push('数据源：Yahoo + quotedance-service + Bloomberg/Reuters/华尔街见闻/金十等');
  lines.push('');
  lines.push(buildGlobalMarketSection(snapshot));
  lines.push('## 🔥 今日热点主题');
  lines.push('- AI & 科技：' + themes.ai + ' 条相关资讯');
  lines.push('- 宏观政策：' + themes.macro + ' 条相关资讯');
  lines.push('- 地缘风险：' + themes.geo + ' 条相关资讯');
  lines.push('');
  lines.push('## ⚡ 投资机会');
  if (!snapshot.analysis.opportunities.length) {
    lines.push('- 当前未识别到明确高胜率机会，建议保持仓位纪律');
  } else {
    snapshot.analysis.opportunities.forEach(item => lines.push('- ' + item));
  }
  lines.push('');
  lines.push('## ⚠️ 风险提醒');
  if (!snapshot.analysis.risks.length) {
    lines.push('- 风险信号有限，关注事件驱动和盘中波动');
  } else {
    snapshot.analysis.risks.forEach(item => lines.push('- ' + item));
  }
  lines.push('');
  lines.push('## 📝 操作策略建议');
  lines.push('- 先看强势板块能否延续，再考虑顺势加仓');
  lines.push('- 对高波动品种保持止损，避免情绪化追涨杀跌');
  lines.push('- 宏观事件前降低杠杆，优先保护回撤');
  lines.push('');
  lines.push('## 📰 专业资讯');
  snapshot.news.forEach((n, i) => {
    const link = n.link ? ' - ' + n.link : '';
    lines.push((i + 1) + '. [' + n.source + '] ' + n.title + link);
  });
  return lines.join('\n');
}

function upcomingWeekCalendar() {
  const now = new Date();
  const nextMonday = new Date(now);
  const day = nextMonday.getDay();
  const offset = day === 0 ? 1 : 8 - day;
  nextMonday.setDate(nextMonday.getDate() + offset);
  const labels = ['周一', '周二', '周三', '周四', '周五'];
  const templates = [
    '美国通胀相关数据观察',
    '中国高频经济数据跟踪',
    '美联储官员讲话窗口',
    'OPEC与能源链价格监控',
    '周度仓位与风险复盘'
  ];
  return labels.map((label, idx) => {
    const d = new Date(nextMonday);
    d.setDate(nextMonday.getDate() + idx);
    return {
      date: formatDate(d),
      label,
      event: templates[idx]
    };
  });
}

function generateWeekendReport(snapshot) {
  const now = new Date();
  const themes = detectThemes(snapshot.news);
  const calendar = upcomingWeekCalendar();
  const lines = [];
  lines.push('📈 市场情报日报 | ' + formatDate(now));
  lines.push('周期：周末休整日');
  lines.push('更新时间：' + formatDateTime(now));
  lines.push('');
  lines.push(buildGlobalMarketSection(snapshot));
  lines.push('## 📌 本周回顾');
  lines.push('- AI & 科技资讯热度：' + themes.ai + '（关注是否进入估值兑现阶段）');
  lines.push('- 宏观政策资讯热度：' + themes.macro + '（关注下周政策与数据共振）');
  lines.push('- 地缘风险资讯热度：' + themes.geo + '（关注能源与避险链条）');
  lines.push('');
  lines.push('## 🔥 本周热点主题');
  lines.push('- 科技成长与大盘风格切换');
  lines.push('- 通胀与利率预期反复');
  lines.push('- 大宗商品与周期板块弹性');
  lines.push('');
  lines.push('## 📅 下周关键节点');
  calendar.forEach(item => {
    lines.push('- ' + item.date + ' ' + item.label + '：' + item.event);
  });
  lines.push('');
  lines.push('## ⚠️ 风险雷达');
  lines.push('- 高风险：地缘事件与能源价格突发波动');
  lines.push('- 中风险：宏观数据不及预期引发风格急切换');
  lines.push('- 中风险：高位热门板块拥挤交易回撤');
  lines.push('');
  lines.push('## 💭 周末思考题');
  lines.push('- 若下周风险偏好下降，你的仓位结构是否有防守腿？');
  lines.push('- 哪个板块具备“基本面改善 + 资金增配”的双重逻辑？');
  lines.push('');
  lines.push('## 📝 操作策略建议');
  lines.push('- 先做风险预算，再做收益预期');
  lines.push('- 把仓位分成核心仓与战术仓，避免单边押注');
  lines.push('- 预设止盈止损与触发条件，提高执行一致性');
  lines.push('');
  lines.push('## 🎉 今日小彩蛋');
  lines.push('- 复盘不是为了证明自己对，而是为了下次更早发现自己错。');
  lines.push('');
  lines.push('## 📰 专业资讯');
  snapshot.news.forEach((n, i) => {
    const link = n.link ? ' - ' + n.link : '';
    lines.push((i + 1) + '. [' + n.source + '] ' + n.title + link);
  });
  return lines.join('\n');
}

function saveSnapshot(snapshot) {
  const file = path.join(MEMORY_DIR, 'market-' + formatDate() + '.json');
  fs.writeFileSync(file, JSON.stringify(snapshot, null, 2), 'utf-8');
  return file;
}

async function safeCall(label, runner, fallback) {
  try {
    return await runner();
  } catch (e) {
    log(label + '失败: ' + (e.message || e));
    return fallback;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const forceRefresh = args.includes('--refresh');
  const netDebug = args.includes('--net-debug');

  if (netDebug) {
    log('network.proxy=' + (PROXY_URL ? PROXY_URL : ''));
    log('network.useProxy=' + String(NETWORK.useProxy));
    log('network.requestRetries=' + String(REQUEST_RETRIES));
    log('network.timeoutMs=' + String(REQUEST_TIMEOUT_MS));
    log('network.enableCurlFallback=' + String(ENABLE_CURL_FALLBACK));
    log('network.proxyDispatcher=' + String(Boolean(proxyDispatcher)));
  }

  const cnSymbols = Array.isArray(CONFIG.watchlist?.cn) ? CONFIG.watchlist.cn : [];
  const futuresSymbols = Array.isArray(CONFIG.watchlist?.futures) ? CONFIG.watchlist.futures : [];

  const [us, cn, futures, plates, news] = await Promise.all([
    safeCall('美股行情', () => fetchUsMarkets(), []),
    safeCall('A股行情', () => fetchQuotedanceQuotes('cn', cnSymbols), []),
    safeCall('期货行情', () => fetchQuotedanceQuotes('futures', futuresSymbols), []),
    safeCall('板块榜', () => fetchPlateLeaders(), []),
    safeCall('专业资讯', () => fetchProfessionalNews(forceRefresh), [])
  ]);

  const analysis = analyzeOpportunities({ us, cn, futures, plates });
  const snapshot = {
    timestamp: new Date().toISOString(),
    us,
    cn,
    futures,
    plates,
    news,
    analysis
  };
  const file = saveSnapshot(snapshot);
  log('市场快照已保存: ' + file);

  const report = isWeekend() ? generateWeekendReport(snapshot) : generateWeekdayReport(snapshot);
  console.log('\n=== MARKET_REPORT_START ===');
  console.log(report);
  console.log('=== MARKET_REPORT_END ===\n');
  return report;
}

if (require.main === module) {
  main().catch(err => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = {
  main,
  fetchUsMarkets,
  fetchQuotedanceQuotes,
  fetchPlateLeaders,
  fetchProfessionalNews,
  generateWeekdayReport,
  generateWeekendReport,
  analyzeOpportunities
};

#!/usr/bin/env node

/**
 * RSS Digest Skill
 *
 * 利用 quotedance-service 的 Feeds API：
 * - 聚合当前用户订阅源的最新文章
 * - 支持“最近 N 天”过滤
 * - 支持按资讯源名称关键字过滤
 * - 本地文件缓存，避免频繁打接口
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.resolve(__dirname, '..');
const CONFIG = require(path.join(SKILL_DIR, 'config.json'));

const SERVICE_URL =
  CONFIG.serviceUrl ||
  'http://localhost:5000';

const API_KEY =
  CONFIG.apiKey ||
  process.env.QUTEDANCE_API_KEY ||
  '';

const MEMORY_DIR = path.join(SKILL_DIR, 'memory');
const SOURCE_CACHE_FILE = path.join(MEMORY_DIR, 'rss-source-cache.json');

if (!fs.existsSync(MEMORY_DIR)) {
  fs.mkdirSync(MEMORY_DIR, { recursive: true });
}

function log(msg) {
  const ts = new Date().toISOString();
  console.log('[' + ts + '] ' + msg);
}

function formatDateTime(d) {
  if (!(d instanceof Date) || isNaN(d.getTime())) return '未知时间';
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const h = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  return y + '-' + m + '-' + day + ' ' + h + ':' + min;
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
    headers['X-API-Key'] = API_KEY;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);

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

function decodeHtmlEntities(text) {
  if (!text) return '';
  return String(text)
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)));
}

function stripHtml(text) {
  return decodeHtmlEntities(String(text || '').replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
}

function pickTag(block, tagName) {
  const re = new RegExp('<' + tagName + '(?:\\s[^>]*)?>([\\s\\S]*?)<\\/' + tagName + '>', 'i');
  const m = block.match(re);
  return m ? decodeHtmlEntities(m[1].trim()) : '';
}

function pickAtomLink(block) {
  const m = block.match(/<link\b[^>]*href="([^"]+)"[^>]*\/?>/i) || block.match(/<link\b[^>]*href='([^']+)'[^>]*\/?>/i);
  return m ? decodeHtmlEntities(m[1].trim()) : '';
}

function parseRssOrAtom(xmlText, source) {
  const text = String(xmlText || '');
  const isAtom = /<feed\b/i.test(text);
  const blocks = isAtom
    ? text.match(/<entry\b[\s\S]*?<\/entry>/gi) || []
    : text.match(/<item\b[\s\S]*?<\/item>/gi) || [];

  return blocks.map(block => {
    const title = pickTag(block, 'title');
    const link = isAtom
      ? (pickAtomLink(block) || pickTag(block, 'id'))
      : (pickTag(block, 'link') || pickTag(block, 'guid'));
    const publishedAt =
      pickTag(block, 'pubDate') ||
      pickTag(block, 'published') ||
      pickTag(block, 'updated') ||
      pickTag(block, 'dc:date');
    const rawSummary =
      pickTag(block, 'description') ||
      pickTag(block, 'summary') ||
      pickTag(block, 'content:encoded') ||
      pickTag(block, 'content');
    const summary = stripHtml(rawSummary);

    return {
      title: title || '（无标题）',
      link,
      published_at: publishedAt || '',
      source_name: source.name || '',
      source_id: source.id || '',
      source_category: source.category || '',
      summary
    };
  });
}

function normalizeRssUrl(rawUrl) {
  const value = String(rawUrl || '').trim();
  if (!value) return '';
  if (/^https?:\/\//i.test(value)) return value;
  const rsshubBase = String(CONFIG.rsshubUrl || '').trim().replace(/\/+$/, '');
  if (!rsshubBase) return '';
  if (value.startsWith('/')) return rsshubBase + value;
  return rsshubBase + '/' + value;
}

async function fetchTextByUrl(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);
  try {
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8'
      },
      signal: controller.signal
    });
    clearTimeout(timeout);
    if (!res.ok) {
      throw new Error('HTTP ' + res.status + ' ' + (await res.text()));
    }
    return await res.text();
  } catch (e) {
    clearTimeout(timeout);
    throw e;
  }
}

async function mapWithConcurrency(items, concurrency, iterator) {
  const ret = [];
  let index = 0;
  const workers = Array(Math.max(1, concurrency)).fill(null).map(async () => {
    while (true) {
      const i = index++;
      if (i >= items.length) return;
      ret[i] = await iterator(items[i], i);
    }
  });
  await Promise.all(workers);
  return ret;
}

function getSourceName(article) {
  if (!article || typeof article !== 'object') return '';
  return (
    article.source_name ||
    article.sourceTitle ||
    article.feed_title ||
    (article.source && (article.source.name || article.source.title)) ||
    article.source ||
    ''
  );
}

function getArticleUrl(article) {
  if (!article || typeof article !== 'object') return '';
  return (
    article.url ||
    article.link ||
    (article.source && article.source.url) ||
    ''
  );
}

function parseArticleDate(article) {
  if (!article || typeof article !== 'object') return null;
  const candidates = [
    article.published_at,
    article.publishedAt,
    article.pubDate,
    article.date,
    article.created_at,
    article.updated_at
  ].filter(Boolean);

  for (const s of candidates) {
    const d = new Date(s);
    if (!isNaN(d.getTime())) return d;
  }
  return null;
}

function dedupeArticles(articles) {
  const seen = new Set();
  const out = [];
  for (const a of Array.isArray(articles) ? articles : []) {
    const link = getArticleUrl(a).trim();
    const title = String(a.title || '').trim();
    const d = parseArticleDate(a);
    const dateKey = d ? d.toISOString() : '';
    const key = link || (title + '|' + dateKey);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    out.push(a);
  }
  out.sort((a, b) => {
    const da = parseArticleDate(a);
    const db = parseArticleDate(b);
    return (db ? db.getTime() : 0) - (da ? da.getTime() : 0);
  });
  return out;
}

function getCacheFilePath(options) {
  const name = options.name || 'all';
  const days = options.days;
  const limit = options.limit;
  const safeName = name.replace(/[^a-zA-Z0-9_-]/g, '_') || 'all';
  const fileName = 'rss-cache-' + safeName + '-d' + days + '-l' + limit + '.json';
  return path.join(MEMORY_DIR, fileName);
}

function readSourceCache(cacheTtlMinutes) {
  if (!fs.existsSync(SOURCE_CACHE_FILE)) return null;
  try {
    const raw = fs.readFileSync(SOURCE_CACHE_FILE, 'utf-8');
    const data = JSON.parse(raw);
    if (!data || !data.timestamp) return null;
    const ts = new Date(data.timestamp);
    if (isNaN(ts.getTime())) return null;
    const ageMs = Date.now() - ts.getTime();
    const ttlMs = (cacheTtlMinutes || 0) * 60 * 1000;
    if (ttlMs > 0 && ageMs > ttlMs) {
      return null;
    }
    return Array.isArray(data.sources) ? data.sources : null;
  } catch {
    return null;
  }
}

function writeSourceCache(sources) {
  const payload = {
    timestamp: new Date().toISOString(),
    sources: Array.isArray(sources) ? sources : []
  };
  try {
    fs.writeFileSync(SOURCE_CACHE_FILE, JSON.stringify(payload, null, 2), 'utf-8');
  } catch (e) {
    log('写入订阅源缓存失败: ' + e.message);
  }
}

function clearAllCaches() {
  try {
    const files = fs.readdirSync(MEMORY_DIR);
    let removed = 0;
    for (const fileName of files) {
      if (/^rss-cache-.*\.json$/i.test(fileName) || fileName === path.basename(SOURCE_CACHE_FILE)) {
        fs.unlinkSync(path.join(MEMORY_DIR, fileName));
        removed += 1;
      }
    }
    return removed;
  } catch (e) {
    log('清理缓存失败: ' + e.message);
    return 0;
  }
}

function readCache(options, cacheTtlMinutes) {
  const filePath = getCacheFilePath(options);
  if (!fs.existsSync(filePath)) return null;

  try {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(raw);
    if (!data || !data.timestamp) return null;

    const ts = new Date(data.timestamp);
    if (isNaN(ts.getTime())) return null;

    const ageMs = Date.now() - ts.getTime();
    const ttlMs = (cacheTtlMinutes || 0) * 60 * 1000;

    if (ttlMs > 0 && ageMs > ttlMs) {
      return null;
    }

    return data.articles || [];
  } catch {
    return null;
  }
}

function writeCache(options, articles) {
  const filePath = getCacheFilePath(options);
  const payload = {
    timestamp: new Date().toISOString(),
    params: options,
    articles: articles
  };
  try {
    fs.writeFileSync(filePath, JSON.stringify(payload, null, 2), 'utf-8');
  } catch (e) {
    // 缓存失败不影响主流程
    log('写入缓存失败: ' + e.message);
  }
}

function filterArticles(articles, { days, name, limit }) {
  const now = Date.now();
  const windowMs = (days || 0) > 0 ? days * 24 * 60 * 60 * 1000 : 0;

  let filtered = Array.isArray(articles) ? articles.slice() : [];

  if (windowMs > 0) {
    filtered = filtered.filter(a => {
      const d = parseArticleDate(a);
      if (!d) return true; // 没有时间字段时不强制过滤，避免误杀
      return now - d.getTime() <= windowMs;
    });
  }

  if (name && name.trim()) {
    const keyword = name.trim().toLowerCase();
    filtered = filtered.filter(a => {
      const sourceName = getSourceName(a).toLowerCase();
      return sourceName && sourceName.includes(keyword);
    });
  }

  if (limit && filtered.length > limit) {
    filtered = filtered.slice(0, limit);
  }

  return filtered;
}

function formatDigestMarkdown(articles, { days, name }) {
  const now = new Date();
  const titleParts = ['📚 订阅资讯流汇总'];
  if (days && days > 0) {
    titleParts.push('最近 ' + days + ' 天');
  }
  if (name && name.trim()) {
    titleParts.push('（来源包含：' + name.trim() + '）');
  }

  const header = '# ' + titleParts.join(' ');

  if (!articles.length) {
    return (
      header +
      '\n\n' +
      '当前筛选条件下没有找到文章，可以尝试放宽时间范围或移除来源名称过滤。'
    );
  }

  let out = header + '\n\n';
  out += '生成时间：' + formatDateTime(now) + '\n\n';

  articles.forEach((a, idx) => {
    const articleTitle = a.title || a.subject || '（无标题）';
    const sourceName = getSourceName(a) || '未知来源';
    const d = parseArticleDate(a);
    const dateStr = d ? formatDateTime(d) : '时间未知';
    const url = getArticleUrl(a);

    out += (idx + 1) + '. **' + articleTitle + '**\n';
    out += '   - 来源：' + sourceName + '\n';
    out += '   - 时间：' + dateStr + '\n';
    if (url) {
      out += '   - 链接：' + url + '\n';
    }
    if (a.summary || a.description) {
      const summary = String(a.summary || a.description).trim();
      if (summary) {
        const short =
          summary.length > 200 ? summary.slice(0, 200) + '…' : summary;
        out += '   - 摘要：' + short + '\n';
      }
    }
    out += '\n';
  });

  return out;
}

async function getRssDigest({ days, limit, name, refreshSources, forceRefresh }) {
  const defaults = (CONFIG && CONFIG.defaults) || {};
  const effectiveDays = days || defaults.recentDays || 3;
  const effectiveLimit = limit || defaults.limit || 100;
  const cacheTtlMinutes = defaults.cacheTtlMinutes || 30;
  const sourceCacheTtlMinutes = defaults.sourceCacheTtlMinutes || 15;

  const cacheOptions = {
    days: effectiveDays,
    limit: effectiveLimit,
    name: name || ''
  };

  const cached = forceRefresh ? null : readCache(cacheOptions, cacheTtlMinutes);
  if (cached) {
    log('命中本地缓存');
    const filteredFromCache = filterArticles(cached, {
      days: effectiveDays,
      name,
      limit: effectiveLimit
    });
    return formatDigestMarkdown(filteredFromCache, {
      days: effectiveDays,
      name
    });
  }

  let sources = null;
  if (!forceRefresh && !refreshSources) {
    sources = readSourceCache(sourceCacheTtlMinutes);
    if (sources) {
      log('命中订阅源缓存');
    }
  }
  if (!sources) {
    log('从 quotedance-service 获取订阅源列表...');
    const sourcePayload = await fetchJson('/feeds/registry');
    sources = Array.isArray(sourcePayload.sources)
      ? sourcePayload.sources
      : Array.isArray(sourcePayload)
      ? sourcePayload
      : [];
    writeSourceCache(sources);
  }

  if (!sources.length) {
    return formatDigestMarkdown([], {
      days: effectiveDays,
      name
    });
  }

  const fetchResults = await mapWithConcurrency(sources, 5, async source => {
    const feedUrl = normalizeRssUrl(source.rss_url);
    if (!feedUrl) {
      log('跳过无效 rss_url：' + (source.name || source.id || 'unknown'));
      return [];
    }
    try {
      const xml = await fetchTextByUrl(feedUrl);
      const parsed = parseRssOrAtom(xml, source);
      return parsed;
    } catch (e) {
      log('抓取失败：' + (source.name || source.id || 'unknown') + ' - ' + (e.message || e));
      return [];
    }
  });

  const allArticles = dedupeArticles(fetchResults.flat());
  log('本地抓取并聚合文章数量：' + allArticles.length);

  const filtered = filterArticles(allArticles, {
    days: effectiveDays,
    name,
    limit: effectiveLimit
  });

  writeCache(cacheOptions, allArticles);

  return formatDigestMarkdown(filtered, {
    days: effectiveDays,
    name
  });
}

async function main() {
  const args = process.argv.slice(2);

  let days = CONFIG.defaults && CONFIG.defaults.recentDays
    ? CONFIG.defaults.recentDays
    : 3;
  let limit = CONFIG.defaults && CONFIG.defaults.limit
    ? CONFIG.defaults.limit
    : 100;
  let name = '';
  let refreshSources = false;
  let forceRefresh = false;
  let clearCache = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if ((arg === '--days' || arg === '-d') && i + 1 < args.length) {
      const v = parseInt(args[++i], 10);
      if (!isNaN(v) && v > 0) days = v;
    } else if ((arg === '--limit' || arg === '-l') && i + 1 < args.length) {
      const v = parseInt(args[++i], 10);
      if (!isNaN(v) && v > 0) limit = v;
    } else if ((arg === '--name' || arg === '-n') && i + 1 < args.length) {
      name = args[++i];
    } else if (arg === '--refresh-sources') {
      refreshSources = true;
    } else if (arg === '--refresh' || arg === '--force-refresh') {
      forceRefresh = true;
      refreshSources = true;
    } else if (arg === '--clear-cache') {
      clearCache = true;
      forceRefresh = true;
      refreshSources = true;
    }
  }

  try {
    if (clearCache) {
      const removed = clearAllCaches();
      log('已清理缓存文件：' + removed);
    }
    const markdown = await getRssDigest({ days, limit, name, refreshSources, forceRefresh });
    console.log(markdown);
  } catch (e) {
    console.error('获取资讯流失败：', e.message || e);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  getRssDigest,
  clearAllCaches,
  main
};

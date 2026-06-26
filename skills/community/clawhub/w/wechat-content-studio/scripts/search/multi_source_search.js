#!/usr/bin/env node

/**
 * 多来源搜索引擎
 * 使用 Brave Search（HTML 可解析，支持 site: 站内搜索）+ Hacker News API + GitHub Trending + arXiv 等
 * Google 网页版需 JS 渲染，脚本无法直接抓取；Brave 结果页含可解析的链接与标题
 * 默认经本地代理访问 search.brave.com / github.com 等（HTTPS_PROXY 或 127.0.0.1:7890）
 */

import https from 'https';
import http from 'http';
import * as cheerio from 'cheerio';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { HttpProxyAgent } from 'http-proxy-agent';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SOURCES_CONFIG = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'search_sources.json'), 'utf-8')
);

const PROXY_URL = process.env.HTTPS_PROXY || process.env.HTTP_PROXY
  || process.env.https_proxy || process.env.http_proxy
  || process.env.ALL_PROXY || process.env.all_proxy
  || 'http://127.0.0.1:7890';

const PROXY_DOMAINS = [
  'search.brave.com', 'brave.com', 'github.com', 'producthunt.com',
  'hn.algolia.com', 'huggingface.co',
];

function needsProxy(url) {
  try {
    const hostname = new URL(url).hostname;
    return PROXY_DOMAINS.some(d => hostname === d || hostname.endsWith('.' + d));
  } catch { return false; }
}

function getProxyAgent(url) {
  if (!needsProxy(url)) return undefined;
  return url.startsWith('https')
    ? new HttpsProxyAgent(PROXY_URL)
    : new HttpProxyAgent(PROXY_URL);
}

const USER_AGENTS = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
];

function randomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 通用 HTTP(S) GET，自动跟随重定向 + 智能代理，返回 { statusCode, body: string }
 */
function httpGet(url, extraHeaders = {}, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    let redirectCount = 0;

    function doRequest(currentUrl) {
      const mod = currentUrl.startsWith('https') ? https : http;
      const agent = getProxyAgent(currentUrl);
      const headers = {
        'User-Agent': randomUA(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        ...extraHeaders,
      };

      const reqOptions = { headers };
      if (agent) reqOptions.agent = agent;

      const req = mod.get(currentUrl, reqOptions, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          if (++redirectCount > maxRedirects) {
            reject(new Error('Too many redirects'));
            return;
          }
          let redirectUrl = res.headers.location;
          if (redirectUrl.startsWith('/')) {
            const u = new URL(currentUrl);
            redirectUrl = `${u.protocol}//${u.host}${redirectUrl}`;
          }
          res.resume();
          doRequest(redirectUrl);
          return;
        }
        let data = '';
        res.setEncoding('utf-8');
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
      });
      req.on('error', reject);
      req.setTimeout(30000, () => { req.destroy(); reject(new Error('Timeout')); });
    }

    doRequest(url);
  });
}

async function httpGetJSON(url, extraHeaders = {}) {
  const resp = await httpGet(url, {
    'Accept': 'application/json',
    ...extraHeaders,
  });
  return JSON.parse(resp.body);
}

// ─────────────────────────────────────────────────
// Brave Search 站内搜索 (site:domain keyword)
// ─────────────────────────────────────────────────

const BRAVE_SEARCH_URL = 'https://search.brave.com/search';

/** Brave 连续请求易 429，全局最小间隔（毫秒） */
const BRAVE_MIN_INTERVAL_MS = parseInt(process.env.BRAVE_SEARCH_MIN_INTERVAL_MS || '3200', 10);
let lastBraveRequestEnd = 0;

async function braveHttpGet(url) {
  const gap = lastBraveRequestEnd + BRAVE_MIN_INTERVAL_MS - Date.now();
  if (gap > 0) await sleep(gap);
  try {
    return await httpGet(url);
  } finally {
    lastBraveRequestEnd = Date.now();
  }
}

/**
 * 校验结果 URL 是否属于配置的 site: 域名（支持 host 或 host/path 前缀）
 */
function urlMatchesSiteDomain(pageUrl, domainSpec) {
  try {
    const u = new URL(pageUrl);
    const host = u.hostname.replace(/^www\./, '');
    const segments = domainSpec.replace(/^www\./, '').split('/').filter(Boolean);
    const targetHost = segments[0] || '';
    if (!targetHost) return false;
    if (host !== targetHost && !host.endsWith(`.${targetHost}`)) return false;
    if (segments.length > 1) {
      const prefix = `/${segments.slice(1).join('/')}`;
      if (!u.pathname.startsWith(prefix) && !u.pathname.startsWith(`${prefix}/`)) return false;
    }
    return true;
  } catch {
    return false;
  }
}

function parseBraveResults(html, maxResults, domainSpec, sourceLabel, type) {
  const $ = cheerio.load(html);
  const results = [];

  $('div.snippet[data-type="web"]').each((_, el) => {
    if (results.length >= maxResults) return false;
    const $el = $(el);
    const $link = $el.find('.result-content a[href^="http"]').first();
    const link = ($link.attr('href') || '').trim();
    if (!link || link.includes('search.brave.com') || link.includes('brave.com')) return;

    if (domainSpec && !urlMatchesSiteDomain(link, domainSpec)) return;

    let title = $el.find('.search-snippet-title').first().text().trim();
    if (!title) title = ($link.attr('title') || '').trim();
    if (!title) title = $link.text().trim().replace(/\s+/g, ' ');
    if (!title) return;

    const snippet = $el.find('.generic-snippet .content').first().text().trim().replace(/\s+/g, ' ');

    results.push({
      title,
      url: link,
      summary: snippet.substring(0, 200),
      source: sourceLabel,
      type,
    });
  });

  return results;
}

async function fetchBraveSearchPage(url, labelForLog = '') {
  const maxAttempts = 4;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const resp = await braveHttpGet(url);
    if (resp.statusCode === 200) return resp.body;
    if (resp.statusCode === 429 && attempt < maxAttempts - 1) {
      const waitMs = 8000 + Math.random() * 7000 + attempt * 5000;
      console.error(`  ⚠️  Brave 限流 (429)${labelForLog ? ` [${labelForLog}]` : ''}，约 ${Math.round(waitMs / 1000)}s 后重试 (${attempt + 1}/${maxAttempts})…`);
      await sleep(waitMs);
      continue;
    }
    return null;
  }
  return null;
}

async function searchBraveSite(keyword, domain, maxResults = 3) {
  const q = encodeURIComponent(`site:${domain} ${keyword}`);
  const url = `${BRAVE_SEARCH_URL}?q=${q}&source=web`;

  try {
    const body = await fetchBraveSearchPage(url, domain);
    if (!body) return [];

    return parseBraveResults(body, maxResults, domain, domain, 'site_search');
  } catch (error) {
    console.error(`  ⚠️  Brave 搜索 ${domain} 失败: ${error.message}`);
    return [];
  }
}

// ─────────────────────────────────────────────────
// 微信公众号搜索 (Brave: site:mp.weixin.qq.com + 账号名)
// ─────────────────────────────────────────────────

async function searchWechat(keyword, accountName, maxResults = 3) {
  const q = encodeURIComponent(`site:mp.weixin.qq.com "${accountName}" ${keyword}`);
  const url = `${BRAVE_SEARCH_URL}?q=${q}&source=web`;

  try {
    const body = await fetchBraveSearchPage(url, accountName);
    if (!body) return [];

    return parseBraveResults(
      body,
      maxResults,
      'mp.weixin.qq.com',
      accountName,
      'wechat'
    );
  } catch (error) {
    console.error(`  ⚠️  微信搜索 [${accountName}] 失败: ${error.message}`);
    return [];
  }
}

/**
 * 微信公众号全网（不限定公众号名）：site:mp.weixin.qq.com + 关键词
 */
async function searchWechatGlobal(keyword, maxResults = 5) {
  const q = encodeURIComponent(`site:mp.weixin.qq.com ${keyword}`);
  const url = `${BRAVE_SEARCH_URL}?q=${q}&source=web`;

  try {
    const body = await fetchBraveSearchPage(url, '微信公众号(全网)');
    if (!body) return [];

    return parseBraveResults(
      body,
      maxResults,
      'mp.weixin.qq.com',
      '微信公众号(全网)',
      'wechat_global'
    );
  } catch (error) {
    console.error(`  ⚠️  微信公众号全网搜索失败: ${error.message}`);
    return [];
  }
}

// ─────────────────────────────────────────────────
// Hacker News (Algolia API)
// ─────────────────────────────────────────────────

async function searchHackerNews(keyword, minScore = 100, maxResults = 5) {
  const query = encodeURIComponent(keyword);
  const url = `https://hn.algolia.com/api/v1/search?query=${query}&tags=story&numericFilters=points>=${minScore}&hitsPerPage=${maxResults}`;

  try {
    const data = await httpGetJSON(url);
    return (data.hits || []).map(hit => ({
      title: hit.title || '',
      url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
      summary: `Score: ${hit.points} | Comments: ${hit.num_comments}`,
      source: 'Hacker News',
      type: 'hackernews',
      datetime: hit.created_at || '',
      score: hit.points || 0,
    }));
  } catch (error) {
    console.error(`  ⚠️  Hacker News 搜索失败: ${error.message}`);
    return [];
  }
}

// ─────────────────────────────────────────────────
// GitHub Trending (HTML 抓取)
// ─────────────────────────────────────────────────

async function searchGitHubTrending(keyword, maxResults = 5) {
  const url = 'https://github.com/trending?since=daily&spoken_language_code=';

  try {
    const resp = await httpGet(url);
    const $ = cheerio.load(resp.body);
    const results = [];
    const lowerKw = keyword.toLowerCase();

    $('article.Box-row').each((_, el) => {
      if (results.length >= maxResults) return false;
      const $el = $(el);
      const $a = $el.find('h2 a');
      const repoPath = ($a.attr('href') || '').replace(/^\//, '');
      const desc = $el.find('p').text().trim();
      const stars = $el.find('.octicon-star').parent().text().trim();

      const text = `${repoPath} ${desc}`.toLowerCase();
      const kwParts = lowerKw.split(/\s+/).filter(Boolean);
      if (kwParts.some(p => text.includes(p))) {
        results.push({
          title: repoPath,
          url: `https://github.com/${repoPath}`,
          summary: `${desc} (⭐ ${stars})`,
          source: 'GitHub Trending',
          type: 'github_trending',
        });
      }
    });

    return results;
  } catch (error) {
    console.error(`  ⚠️  GitHub Trending 抓取失败: ${error.message}`);
    return [];
  }
}

// ─────────────────────────────────────────────────
// Product Hunt (Brave site: 搜索)
// ─────────────────────────────────────────────────

async function searchProductHunt(keyword, maxResults = 3) {
  return searchBraveSite(`${keyword} AI`, 'producthunt.com', maxResults);
}

// ─────────────────────────────────────────────────
// arXiv (OpenSearch API)
// ─────────────────────────────────────────────────

async function searchArxiv(keyword, maxResults = 5) {
  const query = encodeURIComponent(keyword);
  const url = `http://export.arxiv.org/api/query?search_query=all:${query}&sortBy=submittedDate&sortOrder=descending&max_results=${maxResults}`;

  try {
    const resp = await httpGet(url);
    const $ = cheerio.load(resp.body, { xmlMode: true });
    const results = [];

    $('entry').each((_, el) => {
      const $el = $(el);
      const title = $el.find('title').text().trim().replace(/\s+/g, ' ');
      const link = $el.find('id').text().trim();
      const summary = $el.find('summary').text().trim().replace(/\s+/g, ' ').substring(0, 200);
      const published = $el.find('published').text().trim();
      const authors = [];
      $el.find('author name').each((_, a) => authors.push($(a).text().trim()));

      if (title && link) {
        results.push({
          title,
          url: link.replace('http://', 'https://'),
          summary: `${authors.slice(0, 3).join(', ')} | ${summary}...`,
          source: 'arXiv',
          type: 'arxiv',
          datetime: published,
        });
      }
    });

    return results;
  } catch (error) {
    console.error(`  ⚠️  arXiv 搜索失败: ${error.message}`);
    return [];
  }
}

// ─────────────────────────────────────────────────
// 统一搜索调度器
// ─────────────────────────────────────────────────

async function searchSingleSource(source, keyword, maxPerSource) {
  switch (source.type) {
    case 'wechat':
      return searchWechat(keyword, source.searchName, maxPerSource);
    case 'wechat_global':
      return searchWechatGlobal(keyword, maxPerSource);
    case 'site_search':
      return searchBraveSite(keyword, source.domain, maxPerSource);
    case 'hackernews':
      return searchHackerNews(keyword, source.minScore || 100, maxPerSource);
    case 'github_trending':
      return searchGitHubTrending(keyword, maxPerSource);
    case 'producthunt':
      return searchProductHunt(keyword, maxPerSource);
    case 'arxiv':
      return searchArxiv(keyword, maxPerSource);
    default:
      if (source.domain) {
        return searchBraveSite(keyword, source.domain, maxPerSource);
      }
      return [];
  }
}

/**
 * 多来源搜索
 * @param {string} keyword - 搜索关键词
 * @param {Object} options
 * @param {string[]} [options.categories] - 要搜索的分类列表（默认使用配置的 defaultCategories）
 * @param {number} [options.maxPerSource=3] - 每个来源最大结果数
 * @param {number} [options.totalMax=20] - 总最大结果数
 * @param {boolean} [options.parallel=false] - 并行易触发 Brave 限流，默认串行；需极速时可设 true
 * @returns {Promise<Object>} { results: [], summary: {} }
 */
export async function multiSourceSearch(keyword, options = {}) {
  const {
    categories: requestedCategories,
    maxPerSource = SOURCES_CONFIG.defaults.maxPerSource,
    totalMax = SOURCES_CONFIG.defaults.totalMax,
    parallel = false,
  } = options;

  const categoriesToSearch = requestedCategories || SOURCES_CONFIG.defaults.defaultCategories;
  const allResults = [];
  const summary = { total: 0, byCat: {}, bySource: {} };

  console.log(`\n🔍 多来源搜索: "${keyword}"`);
  console.log(`📂 搜索分类: ${categoriesToSearch.join(', ')}`);
  console.log(`📊 每源上限: ${maxPerSource}, 总上限: ${totalMax}\n`);

  for (const catKey of categoriesToSearch) {
    const cat = SOURCES_CONFIG.categories[catKey];
    if (!cat) {
      console.log(`  ⚠️  未知分类: ${catKey}, 跳过`);
      continue;
    }

    console.log(`\n📂 [${cat.label}]`);
    let catResults = [];

    if (parallel) {
      const promises = cat.sources.map(source =>
        searchSingleSource(source, keyword, maxPerSource)
          .then(results => {
            if (results.length > 0) {
              console.log(`  ✅ ${source.name}: ${results.length} 篇`);
            } else {
              console.log(`  ⚠️  ${source.name}: 0 篇`);
            }
            return results.map(r => ({ ...r, category: catKey, categoryLabel: cat.label }));
          })
          .catch(err => {
            console.log(`  ❌ ${source.name}: ${err.message}`);
            return [];
          })
      );

      const batchResults = await Promise.all(promises);
      for (const batch of batchResults) {
        catResults.push(...batch);
      }
    } else {
      for (const source of cat.sources) {
        try {
          const results = await searchSingleSource(source, keyword, maxPerSource);
          if (results.length > 0) {
            console.log(`  ✅ ${source.name}: ${results.length} 篇`);
          } else {
            console.log(`  ⚠️  ${source.name}: 0 篇`);
          }
          catResults.push(...results.map(r => ({ ...r, category: catKey, categoryLabel: cat.label })));
          await sleep(900 + Math.random() * 1100);
        } catch (err) {
          console.log(`  ❌ ${source.name}: ${err.message}`);
        }
      }
    }

    summary.byCat[catKey] = catResults.length;
    allResults.push(...catResults);

    if (allResults.length >= totalMax) break;

    await sleep(1200 + Math.random() * 800);
  }

  // 去重（按 URL 归一化）
  const seen = new Set();
  const deduped = [];
  for (const r of allResults) {
    const key = r.url.replace(/\/$/, '').replace(/^https?:\/\//, '').replace(/^www\./, '');
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(r);
    }
  }

  const finalResults = deduped.slice(0, totalMax);
  summary.total = finalResults.length;

  for (const r of finalResults) {
    const src = r.source || 'unknown';
    summary.bySource[src] = (summary.bySource[src] || 0) + 1;
  }

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📊 搜索完成: 共 ${finalResults.length} 篇（去重后）`);
  for (const [cat, count] of Object.entries(summary.byCat)) {
    const label = SOURCES_CONFIG.categories[cat]?.label || cat;
    console.log(`  📂 ${label}: ${count} 篇`);
  }
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

  return { results: finalResults, summary };
}

/**
 * 获取所有可用分类 key 列表
 */
export function getAvailableCategories() {
  return Object.entries(SOURCES_CONFIG.categories).map(([key, cat]) => ({
    key,
    label: cat.label,
    priority: cat.priority,
    sourceCount: cat.sources.length,
  }));
}

/**
 * 获取默认分类
 */
export function getDefaultCategories() {
  return SOURCES_CONFIG.defaults.defaultCategories;
}

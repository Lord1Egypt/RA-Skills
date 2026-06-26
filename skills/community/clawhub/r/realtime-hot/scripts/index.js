/**
 * 实时热榜抓取脚本
 * 零依赖：只用 Node.js 内置模块（https, fs, zlib, path, url）
 */

import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const https = require('https');
const zlib = require('zlib');
const { URL } = require('url');

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_FILE = join(__dirname, 'hot-data.json');
const notifyList = {};

const USER_AGENTS = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
];
function randUA() { return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)]; }
function delay(min, max) { return new Promise(res => setTimeout(res, min + Math.random() * (max - min))); }

// ========== 通用 https GET ==========
function httpsGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: 443,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': randUA(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        ...headers
      }
    };
    const req = https.request(options, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        const enc = (res.headers['content-encoding'] || '').toLowerCase();
        let dec = buf;
        if (enc.includes('gzip')) dec = zlib.gunzipSync(buf);
        else if (enc.includes('br')) dec = zlib.brotliDecompressSync(buf);
        else if (enc.includes('deflate')) dec = zlib.inflateSync(buf);
        resolve(dec.toString('utf8'));
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

// ========== 解析函数 ==========
function parseWeibo(jsonStr) {
  try {
    const data = JSON.parse(jsonStr);
    return (data?.data?.realtime || []).slice(0, 50).map((item, i) => ({
      title: item.word || item.topic_name || '',
      url: `https://s.weibo.com/weibo?q=${encodeURIComponent(item.word || item.topic_name || '')}`,
      rank: i + 1, platform: '微博'
    })).filter(item => item.title);
  } catch { return []; }
}

function parseDouyin(jsonStr) {
  try {
    const data = JSON.parse(jsonStr);
    return (data?.data?.word_list || []).slice(0, 50).map((item, i) => ({
      title: item.word || '',
      url: `https://www.douyin.com/search/${encodeURIComponent(item.word || '')}`,
      rank: i + 1, platform: '抖音'
    })).filter(item => item.title);
  } catch { return []; }
}

function parseToutiao(jsonStr) {
  try {
    const data = JSON.parse(jsonStr);
    return (data?.data || []).slice(0, 50).map((item, i) => ({
      title: item.Title || item.title || item.word || '',
      url: item.Url || item.url || '',
      rank: i + 1, platform: '头条'
    })).filter(item => item.title);
  } catch { return []; }
}

function parseBaidu(html) {
  try {
    const start = html.indexOf('{"data":{"cards"');
    if (start === -1) return [];
    let depth = 0, end = start;
    for (let i = start; i < html.length; i++) {
      if (html[i] === '{') depth++;
      else if (html[i] === '}') { depth--; if (depth === 0) { end = i + 1; break; } }
    }
    const data = JSON.parse(html.slice(start, end));
    const hotList = data?.data?.cards?.find(c => c.component === 'hotList')?.content || [];
    return hotList.slice(0, 50).map((item, i) => ({
      title: item.word || item.raw_word || '',
      url: item.appUrl || `https://www.baidu.com/s?wd=${encodeURIComponent(item.word || '')}`,
      rank: i + 1, platform: '百度'
    })).filter(item => item.title);
  } catch { return []; }
}

// tophub HTML 解析（正则，不用 cheerio）
function parseTophub(html, layout) {
  const results = [];
  // 匹配 <a href="..." target="_blank">标题</a>
  const linkRegex = /<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>/g;
  const tdRegex = layout === '1'
    ? /<td[^>]*class="[^"]*"[^>]*>[\s\S]*?<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>[\s\S]*?<\/td>/g
    : /<td[^>]*>[\s\S]*?<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>[\s\S]*?<\/td>/g;

  // 直接找所有 rank 条目
  const itemRegex = /<tr[^>]*>[\s\S]*?<a\s+href="([^"]+)"[^>]*>([^<]+)<\/a>[\s\S]*?<\/tr>/g;
  let m;
  let count = 0;
  while ((m = itemRegex.exec(html)) !== null && count < 50) {
    const rawUrl = m[1];
    const title = m[2].trim();
    const url = rawUrl.startsWith('http') ? rawUrl : `https://tophub.today${rawUrl}`;
    if (title && !title.includes('href')) {
      results.push({ title, url, rank: count + 1 });
      count++;
    }
  }
  return results;
}

// ========== 重试包装 ==========
async function fetchWithRetry(name, fn) {
  for (let i = 0; i <= 1; i++) {
    try { return await fn(); }
    catch (e) {
      if (i < 1) await delay(1000, 2000);
      else { console.error(`[ERR] ${name}: ${e.message}`); return []; }
    }
  }
}

// ========== 主流程 ==========
async function main() {
  console.error('抓取开始...');

  await delay(300, 800);
  const weibo = await fetchWithRetry('微博', async () => {
    const html = await httpsGet('https://weibo.com/ajax/side/hotSearch', { 'Referer': 'https://weibo.com/', 'Accept': 'application/json' });
    return parseWeibo(html);
  });
  notifyList['微博'] = weibo;

  await delay(500, 1200);
  const douyin = await fetchWithRetry('抖音', async () => {
    const url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1';
    const html = await httpsGet(url, { 'Referer': 'https://www.douyin.com/' });
    return parseDouyin(html);
  });
  notifyList['抖音'] = douyin;

  await delay(800, 1800);
  const toutiao = await fetchWithRetry('头条', async () => {
    const url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc&height=1000&pd=extra&list_type=real&source=input&offset=0&category=hot_board&fr=pc_hot_board';
    const json = await httpsGet(url, { 'Referer': 'https://www.toutiao.com/' });
    return parseToutiao(json);
  });
  notifyList['头条'] = toutiao;

  await delay(1000, 2500);
  const baidu = await fetchWithRetry('百度', async () => {
    const html = await httpsGet('https://top.baidu.com/board?tab=realtime', { 'Referer': 'https://top.baidu.com/', 'Accept': 'text/html' });
    return parseBaidu(html);
  });
  notifyList['百度'] = baidu;

  // tophub：知乎、腾讯新闻
  const tophubs = [
    { id: 'mproPpoq6O', name: '知乎', layout: '1' },
    { id: 'qndg48xeLl', name: '腾讯', layout: '0' },
  ];
  for (const t of tophubs) {
    await delay(3000, 5000);
    const items = await fetchWithRetry(t.name, async () => {
      const html = await httpsGet(`https://tophub.today/n/${t.id}`, { 'Referer': 'https://tophub.today/', 'Accept': 'text/html' });
      return parseTophub(html, t.layout).map(i => ({ ...i, platform: t.name }));
    });
    notifyList[t.name] = items;
  }

  writeFileSync(OUTPUT_FILE, JSON.stringify(notifyList, null, 2), 'utf8');
  console.log(JSON.stringify(notifyList));
}

main().catch(e => { console.error('[FATAL]', e.message); process.exit(1); });

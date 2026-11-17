#!/usr/bin/env node

/**
 * twitter-apify.mjs — 通过 Apify API 获取 Twitter/X 推文内容
 *
 * 用法：
 *   APIFY_API_TOKEN=xxx node twitter-apify.mjs --url "https://x.com/user/status/123"
 *
 * 输出：
 *   /tmp/youdaonote-clip-data.json（包含 title、content、imageUrls、source）
 *   stdout：metadata JSON
 *
 * 环境变量：
 *   APIFY_API_TOKEN — Apify API Token（可选，未设置时回退到内置默认 Token）
 *   YOUDAONOTE_CLIP_DEBUG — 调试日志目录（可选，设置后开启调试并写入日志文件）
 */

import https from 'node:https';
import fs from 'node:fs';
import { createHash, randomUUID } from 'node:crypto';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

// 仅从 process.env 读取。OpenClaw 执行 skill 时会把 config 里 youdaonote-clip.env 注入为子进程环境变量。
const DEBUG_DIR = process.env.YOUDAONOTE_CLIP_DEBUG?.trim() || '';
const DEBUG = DEBUG_DIR !== '';

/** 当前请求的 debug key（main 开头设置，用于串联整条剪藏流程） */
let currentDebugKey = null;

function generateDebugKey() {
  return randomUUID().slice(0, 8);
}

function getDebugLogFile() {
  if (!DEBUG) return null;
  if (!currentDebugKey) return null;
  const logDir = join(DEBUG_DIR, currentDebugKey);
  return join(logDir, 'twitter.log');
}

function debug(...args) {
  if (!DEBUG) return;
  const timestamp = new Date().toISOString();
  const message = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
  const logLine = `[${timestamp}] ${message}\n`;
  const logFile = getDebugLogFile();
  try {
    if (logFile) {
      const logDir = join(DEBUG_DIR, currentDebugKey);
      if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
      fs.appendFileSync(logFile, logLine);
    }
  } catch { /* 日志写入失败不影响主流程 */ }
  console.log(...args);
}

const ACTOR_ID = 'nfp1fpt5gUlBwPcor';  // Twitter Scraper Unlimited

// 指数退避轮询配置（v1.4.0 优化：固定间隔 → 指数退避）
// 初始 500ms，每次增加 1.5 倍，最大 3000ms
// 预期收益：缓存命中时从 2s → 0.5s，平均节省 30-50% 等待时间
const POLL_INITIAL_MS = 500;
const POLL_MAX_MS = 3000;
const POLL_BACKOFF_FACTOR = 1.5;
const MAX_POLL_ATTEMPTS = 80;  // 增加次数但总时间相近（更灵活）

// ─────────────────────────────────────────────
// Twitter 结果缓存（C1 优化：避免重复调用 Apify）
// ─────────────────────────────────────────────

const CACHE_DIR = join(tmpdir(), 'youdaonote-clip-cache');
const CACHE_TTL_MS = 60 * 60 * 1000;  // 1 小时

function getCacheKey(url) {
  return createHash('sha256').update(url).digest('hex').slice(0, 16);
}

function readTwitterCache(url) {
  try {
    const key = 'twitter_' + getCacheKey(url);
    const cacheFile = join(CACHE_DIR, `${key}.json`);
    if (!fs.statSync(cacheFile)) return null;

    const cached = JSON.parse(fs.readFileSync(cacheFile, 'utf-8'));
    if (Date.now() - cached.timestamp > CACHE_TTL_MS) {
      fs.rmSync(cacheFile, { force: true });
      return null;
    }
    return cached.data;
  } catch {
    return null;
  }
}

function writeTwitterCache(url, data) {
  try {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    const key = 'twitter_' + getCacheKey(url);
    const cacheFile = join(CACHE_DIR, `${key}.json`);
    fs.writeFileSync(cacheFile, JSON.stringify({ timestamp: Date.now(), data }));
  } catch {
    // 缓存写入失败不影响主流程
  }
}

// ─────────────────────────────────────────────
// CLI 参数解析
// ─────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    url: null,
    output: '/tmp/youdaonote-clip-data.json',
    timeout: 120,
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--url' && args[i + 1]) {
      result.url = args[i + 1];
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      result.output = args[i + 1];
      i++;
    } else if (args[i] === '--timeout' && args[i + 1]) {
      result.timeout = parseInt(args[i + 1], 10);
      i++;
    } else if (!result.url && args[i].startsWith('http')) {
      result.url = args[i];
    }
  }

  return result;
}

// ─────────────────────────────────────────────
// HTTP 请求封装
// ─────────────────────────────────────────────

function httpsRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const reqOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      timeout: (options.timeout || 30) * 1000,
    };

    const req = https.request(reqOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`JSON 解析失败: ${e.message}`));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => reject(new Error('请求超时')));

    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

// ─────────────────────────────────────────────
// Apify API 调用
// ─────────────────────────────────────────────

async function startApifyRun(token, tweetUrl) {
  const input = {
    startUrls: [tweetUrl],
    maxItems: 1,
  };

  const url = `https://api.apify.com/v2/acts/${ACTOR_ID}/runs?token=${token}`;

  debug(`🔍 启动 Apify Actor — URL: ${tweetUrl}`);

  const result = await httpsRequest(url, {
    method: 'POST',
    body: input,
    timeout: 30,
  });

  if (!result.data || !result.data.id) {
    throw new Error(`Apify 启动失败: ${JSON.stringify(result)}`);
  }

  return result.data.id;
}

async function waitForResult(token, runId, maxAttempts = MAX_POLL_ATTEMPTS) {
  const url = `https://api.apify.com/v2/actor-runs/${runId}?token=${token}`;

  debug(`🔍 等待 Apify 结果 — Run ID: ${runId}`);

  let interval = POLL_INITIAL_MS;
  const startTime = Date.now();

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const result = await httpsRequest(url, { timeout: 10 });

    const status = result.data?.status;
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    debug(`🔍 轮询 ${attempt + 1}/${maxAttempts} — 状态: ${status}, 间隔: ${interval}ms, 已用: ${elapsed}s`);

    if (status === 'SUCCEEDED') {
      debug(`✅ Apify 完成 — 总耗时: ${elapsed}s`);
      return result.data;
    } else if (status === 'FAILED' || status === 'ABORTED' || status === 'TIMED-OUT') {
      throw new Error(`Apify 运行失败: ${status}`);
    }

    // 指数退避：等待后增加间隔
    await new Promise(resolve => setTimeout(resolve, interval));
    interval = Math.min(interval * POLL_BACKOFF_FACTOR, POLL_MAX_MS);
  }

  throw new Error(`Apify 超时：等待 ${maxAttempts} 次轮询后仍未完成`);
}

async function fetchDataset(token, datasetId) {
  const url = `https://api.apify.com/v2/datasets/${datasetId}/items?token=${token}&clean=true`;

  debug(`🔍 获取结果数据集`);

  const result = await httpsRequest(url, { timeout: 30 });

  return result || [];
}

// ─────────────────────────────────────────────
// 数据转换
// ─────────────────────────────────────────────

/**
 * 从推文数据中提取图片 URL。
 * Apify Actor 输出格式可能随版本变化，需兼容多种字段位置：
 *   - tweet.media（字符串数组 或 对象数组 {url/media_url_https}）
 *   - tweet.photos（字符串数组 或 对象数组）
 *   - tweet.extendedEntities.media / tweet.extended_entities.media
 *   - tweet.entities.media
 * 统一过滤视频，只保留静态图片。
 */
function extractImageUrls(tweet) {
  const isVideoUrl = (u) => typeof u === 'string' && u.includes('video.twimg.com');

  const extractFromMediaArray = (arr) => {
    if (!Array.isArray(arr)) return [];
    const urls = [];
    for (const item of arr) {
      if (typeof item === 'string') {
        if (!isVideoUrl(item)) urls.push(item);
      } else if (item && typeof item === 'object') {
        if (item.type === 'video' || item.type === 'animated_gif') continue;
        const url = item.media_url_https || item.media_url || item.url || item.src || '';
        if (url && !isVideoUrl(url)) urls.push(url);
      }
    }
    return urls;
  };

  // 按优先级尝试各字段
  const sources = [
    tweet.media,
    tweet.photos,
    tweet.images,
    tweet.extendedEntities?.media,
    tweet.extended_entities?.media,
    tweet.entities?.media,
  ];

  for (const src of sources) {
    const urls = extractFromMediaArray(src);
    if (urls.length > 0) {
      debug(`🔍 图片提取命中字段 — 数量: ${urls.length}`);
      return urls;
    }
  }

  debug(`🔍 未找到图片字段 — tweet keys: ${Object.keys(tweet).join(', ')}`);
  return [];
}

function transformTweetToYnoteData(tweet, sourceUrl) {
  if (!tweet) {
    throw new Error('推文数据为空');
  }

  // 提取文字内容（优先使用 text，fullText 可能被截断）
  const text = tweet.text || tweet.fullText || '';

  // 提取标题（使用前 50 个字符）
  const title = (text.substring(0, 50) + (text.length > 50 ? '...' : '')).replace(/\n/g, ' ');

  const imageUrls = extractImageUrls(tweet);

  // 构建 HTML 内容（富文本转换）
  const content = buildHtmlContent(tweet, text, imageUrls);

  return {
    title,
    content,
    imageUrls,
    source: sourceUrl,
    author: tweet.author?.name || tweet.author?.userName || 'Unknown',
    createdAt: tweet.createdAt || new Date().toISOString(),
  };
}

function buildHtmlContent(tweet, text, imageUrls = []) {
  const parts = [];

  // 作者信息（带链接）
  if (tweet.author) {
    const authorUrl = `https://x.com/${tweet.author.userName}`;
    parts.push(`<p><strong><a href="${authorUrl}">@${tweet.author.userName}</a></strong> (${tweet.author.name || ''})</p>`);
  }

  // 推文内容（富文本转换）
  const richText = convertToRichText(tweet, text);
  parts.push(`<p>${richText}</p>`);

  // 图片
  for (const imgUrl of imageUrls) {
    parts.push(`<p><img src="${imgUrl}" /></p>`);
  }

  // 时间
  if (tweet.createdAt) {
    parts.push(`<p><em>${new Date(tweet.createdAt).toLocaleString('zh-CN')}</em></p>`);
  }

  // 原推文链接
  if (tweet.url) {
    parts.push(`<p><a href="${tweet.url}">原推文链接</a></p>`);
  }

  return parts.join('\n');
}

// ─────────────────────────────────────────────
// 富文本转换
// ─────────────────────────────────────────────

function convertToRichText(tweet, text) {
  if (!text) return '';

  let result = escapeHtml(text);

  // 1. 处理 @ 提及
  if (tweet.entities?.user_mentions) {
    for (const mention of tweet.entities.user_mentions) {
      const screenName = mention.screen_name;
      result = result.replace(
        new RegExp(`@${screenName}`, 'gi'),
        `<a href="https://x.com/${screenName}">@${screenName}</a>`
      );
    }
  }

  // 2. 处理链接
  if (tweet.entities?.urls) {
    for (const urlEntity of tweet.entities.urls) {
      const displayUrl = urlEntity.display_url || urlEntity.expanded_url || urlEntity.url;
      result = result.replace(
        urlEntity.url,
        `<a href="${urlEntity.expanded_url || urlEntity.url}">${displayUrl}</a>`
      );
    }
  }

  // 3. 处理换行
  result = result.replace(/\n/g, '</p>\n<p>');

  return result;
}

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ─────────────────────────────────────────────
// 主流程
// ─────────────────────────────────────────────

async function main() {
  const args = parseArgs();
  const token = process.env.APIFY_API_TOKEN?.trim() || '';

  if (!args.url) {
    console.error('错误：缺少 --url 参数');
    process.exit(1);
  }

  if (!token) {
    console.error('错误：未设置 APIFY_API_TOKEN。请在 OpenClaw config 的 youdaonote-clip.env 中配置，或在 shell 中 export APIFY_API_TOKEN（可在 apify.com 获取 Token）。');
    process.exit(1);
  }

  // 验证 URL 格式
  if (!args.url.match(/^https?:\/\/(twitter\.com|x\.com)/i)) {
    console.error('错误：URL 必须是 Twitter/X 链接');
    process.exit(1);
  }

  try {
    currentDebugKey = DEBUG ? generateDebugKey() : null;
    debug('🔍 路径: A (twitter-apify)');

    let ynoteData;

    // Step 0: 检查缓存（C1 优化：避免重复调用 Apify）
    const cachedData = readTwitterCache(args.url);
    if (cachedData) {
      debug(`🔍 Twitter 缓存命中 — url: ${args.url}`);
      ynoteData = cachedData;
    } else {
      // Step 1: 启动 Apify
      const runId = await startApifyRun(token, args.url);
      debug(`🔍 Run ID: ${runId}`);

      // Step 2: 等待结果
      const runData = await waitForResult(token, runId, Math.ceil(args.timeout * 1000 / POLL_INITIAL_MS));

      // Step 3: 获取数据集
      const datasetId = runData.defaultDatasetId;
      const items = await fetchDataset(token, datasetId);

      if (!items || items.length === 0) {
        throw new Error('Apify 返回空结果');
      }

      // Step 4: 转换数据
      const tweet = items[0];
      debug(`🔍 RAW TWEET KEYS: ${Object.keys(tweet || {}).join(', ')}`);
      if (tweet?.noResults) {
        throw new Error('Apify Actor 无法抓取该推文（noResults）：X.com 可能要求登录验证，请配置 APIFY_TWITTER_COOKIE 环境变量');
      }
      ynoteData = transformTweetToYnoteData(tweet, args.url);

      // Step 4.5: 写入缓存
      writeTwitterCache(args.url, ynoteData);
      debug(`🔍 已缓存 Twitter 结果`);
    }

    // Step 5: 写入文件（含 _debugKey、_source 供 clip-note 串联日志与路径标识）
    ynoteData._source = 'twitter';
    if (currentDebugKey) ynoteData._debugKey = currentDebugKey;
    fs.writeFileSync(args.output, JSON.stringify(ynoteData, null, 2));
    debug(`🔍 已写入: ${args.output}`);

    // Step 6: 输出 metadata
    const metadata = {
      title: ynoteData.title,
      imageCount: ynoteData.imageUrls.length,
      source: ynoteData.source,
      contentLength: ynoteData.content.length,
      author: ynoteData.author,
    };
    console.log(JSON.stringify(metadata));

  } catch (error) {
    console.error(`❌ ${error.message}`);
    process.exit(1);
  }
}

main();

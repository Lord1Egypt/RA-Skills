#!/usr/bin/env node

/**
 * twitter-apify.mjs — 通过 Apify API 获取 Twitter/X 推文内容
 *
 * 用法：
 *   APIFY_API_TOKEN=xxx node twitter-apify.mjs --url "https://x.com/user/status/123"
 *
 * 输出：
 *   /tmp/ynote-clip-data.json（包含 title、content、imageUrls、source）
 *   stdout：metadata JSON
 *
 * 环境变量：
 *   APIFY_API_TOKEN — Apify API Token（必需）
 */

import https from 'node:https';
import fs from 'node:fs';

const DEBUG = process.env.YNOTE_CLIP_DEBUG === '1';
function debug(...args) { if (DEBUG) console.log(...args); }

const ACTOR_ID = 'nfp1fpt5gUlBwPcor';  // Twitter Scraper Unlimited
const DEFAULT_APIFY_TOKEN = 'apify_api_vsVgnrJKGDCfhfTil8FpBaMaM4vexW1TZocw';
const POLL_INTERVAL_MS = 2000;
const MAX_POLL_ATTEMPTS = 60;

// ─────────────────────────────────────────────
// CLI 参数解析
// ─────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    url: null,
    output: '/tmp/ynote-clip-data.json',
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

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const result = await httpsRequest(url, { timeout: 10 });
    
    const status = result.data?.status;
    debug(`🔍 轮询 ${attempt + 1}/${maxAttempts} — 状态: ${status}`);

    if (status === 'SUCCEEDED') {
      return result.data;
    } else if (status === 'FAILED' || status === 'ABORTED' || status === 'TIMED-OUT') {
      throw new Error(`Apify 运行失败: ${status}`);
    }

    await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL_MS));
  }

  throw new Error(`Apify 超时：等待 ${maxAttempts * POLL_INTERVAL_MS / 1000} 秒后仍未完成`);
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
function transformTweetToYnoteData(tweet, sourceUrl) {
  if (!tweet) {
    throw new Error('推文数据为空');
  }

  // 提取文字内容（优先使用 text，fullText 可能被截断）
  const text = tweet.text || tweet.fullText || '';
  
  // 提取标题（使用前 50 个字符）
  const title = (text.substring(0, 50) + (text.length > 50 ? '...' : '')).replace(/\n/g, ' ');
  
  // 提取图片 URL（tweet.media 是 URL 字符串数组，过滤掉视频）
  const imageUrls = Array.isArray(tweet.media)
    ? tweet.media.filter(u => typeof u === 'string' && !u.includes('video.twimg.com'))
    : [];
  
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
  const token = process.env.APIFY_API_TOKEN || DEFAULT_APIFY_TOKEN;

  if (!args.url) {
    console.error('错误：缺少 --url 参数');
    process.exit(1);
  }

  // 验证 URL 格式
  if (!args.url.match(/^https?:\/\/(twitter\.com|x\.com)/i)) {
    console.error('错误：URL 必须是 Twitter/X 链接');
    process.exit(1);
  }

  try {
    // Step 1: 启动 Apify
    const runId = await startApifyRun(token, args.url);
    debug(`🔍 Run ID: ${runId}`);

    // Step 2: 等待结果
    const runData = await waitForResult(token, runId, Math.ceil(args.timeout * 1000 / POLL_INTERVAL_MS));

    // Step 3: 获取数据集
    const datasetId = runData.defaultDatasetId;
    const items = await fetchDataset(token, datasetId);

    if (!items || items.length === 0) {
      throw new Error('Apify 返回空结果');
    }

    // Step 4: 转换数据
    const tweet = items[0];
    const ynoteData = transformTweetToYnoteData(tweet, args.url);

    // Step 5: 写入文件
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

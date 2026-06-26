#!/usr/bin/env node

/**
 * 智谱搜索 (Zhipu Search)
 * 调用智谱 Web Search API：POST /paas/v4/web_search
 */

const https = require('https');
const path = require('path');
const fs = require('fs');

// ── 读取 API Key ──────────────────────────────────────────────
function getApiKey() {
  // 优先环境变量
  if (process.env.ZHIPU_API_KEY) return process.env.ZHIPU_API_KEY;

  // 其次 config.json
  const configPath = path.join(__dirname, '..', 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      if (cfg.apiKey) return cfg.apiKey;
    } catch (_) {}
  }

  return null;
}

// ── 参数解析 ──────────────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = {
    query: null,
    count: 10,
    engine: 'search_std',
    freshness: 'noLimit',
    contentSize: 'medium',
    domain: null,
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--count' && args[i + 1]) {
      opts.count = parseInt(args[++i], 10);
    } else if (args[i] === '--engine' && args[i + 1]) {
      opts.engine = args[++i];
    } else if (args[i] === '--freshness' && args[i + 1]) {
      opts.freshness = args[++i];
    } else if (args[i] === '--content-size' && args[i + 1]) {
      opts.contentSize = args[++i];
    } else if (args[i] === '--domain' && args[i + 1]) {
      opts.domain = args[++i];
    } else if (!args[i].startsWith('--')) {
      opts.query = args[i];
    }
  }

  return opts;
}

// ── HTTP 请求 ─────────────────────────────────────────────────
function post(apiKey, body) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify(body);
    const options = {
      hostname: 'open.bigmodel.cn',
      path: '/api/paas/v4/web_search',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(payload),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(data) });
        } catch (e) {
          reject(new Error(`响应解析失败: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ── 主逻辑 ────────────────────────────────────────────────────
async function main() {
  const opts = parseArgs(process.argv);

  if (!opts.query) {
    console.error(JSON.stringify({
      type: 'error',
      code: 'MISSING_QUERY',
      message: '请提供搜索关键词。用法：node search.js "<关键词>" [选项]',
    }));
    process.exit(1);
  }

  const apiKey = getApiKey();
  if (!apiKey) {
    console.error(JSON.stringify({
      type: 'error',
      code: 'MISSING_API_KEY',
      message: '未找到 API Key。请设置环境变量 ZHIPU_API_KEY 或在 config.json 中填写 apiKey。',
    }));
    process.exit(1);
  }

  // 构造请求体
  const requestBody = {
    search_query: opts.query.slice(0, 70),
    search_engine: opts.engine,
    search_intent: false,
    count: Math.min(Math.max(opts.count, 1), 50),
    search_recency_filter: opts.freshness,
    content_size: opts.contentSize,
  };
  if (opts.domain) {
    requestBody.search_domain_filter = opts.domain;
  }

  let resp;
  try {
    resp = await post(apiKey, requestBody);
  } catch (err) {
    console.error(JSON.stringify({ type: 'error', code: 'NETWORK_ERROR', message: err.message }));
    process.exit(1);
  }

  if (resp.status !== 200) {
    const errBody = resp.body;
    console.error(JSON.stringify({
      type: 'error',
      code: String(resp.status),
      message: errBody?.error?.message || '请求失败',
    }));
    process.exit(1);
  }

  const data = resp.body;
  const results = (data.search_result || []).map((item, i) => ({
    index: i + 1,
    title: item.title || '',
    url: item.link || '',
    description: item.content || '',
    siteName: item.media || '',
    publishedDate: item.publish_date || '',
  }));

  console.log(JSON.stringify({
    type: 'search',
    query: opts.query,
    engine: opts.engine,
    resultCount: results.length,
    results,
  }, null, 2));
}

main();
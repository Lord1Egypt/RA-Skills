#!/usr/bin/env node
/**
 * perplexity-search-call.mjs — Perplexity Search API 网络请求层
 *
 * 本文件只负责发送 HTTP 请求和格式化响应，不访问环境变量、不读取文件。
 * API Key 和参数 JSON 均由 perplexity-search-call.sh 解析后通过 argv 传入。
 *
 * 用法（由 .sh 调用，不建议直接运行）：
 *   node perplexity-search-call.mjs <apiKey> '<json_params>'
 *
 * argv[2]: API Key（由 .sh 从 env 读取后传入）
 * argv[3]: 参数 JSON 字符串（由 .sh 从 stdin/文件/argv 解析后传入）
 *
 * 输出：results JSON 数组写到 stdout
 * 错误：写 stderr 并 exit 1
 */

// ─────────────────────────────────────────────
// 参数接收（纯 argv，无 env 访问、无文件读取）
// ─────────────────────────────────────────────

const apiKey = (process.argv[2] ?? '').trim();
if (!apiKey) {
  process.stderr.write('错误：未提供 API Key（应由 perplexity-search-call.sh 传入）\n');
  process.exit(1);
}

const argsJson = process.argv[3] ?? '{}';
let params;
try {
  params = JSON.parse(argsJson);
} catch (e) {
  if (/position \d+/.test(e.message)) {
    const lastBrace = argsJson.lastIndexOf('}');
    if (lastBrace !== -1) {
      try {
        params = JSON.parse(argsJson.slice(0, lastBrace + 1));
      } catch {
        process.stderr.write(`参数不是合法 JSON: ${e.message}\n`);
        process.exit(1);
      }
    } else {
      process.stderr.write(`参数不是合法 JSON: ${e.message}\n`);
      process.exit(1);
    }
  } else {
    process.stderr.write(`参数不是合法 JSON: ${e.message}\n`);
    process.exit(1);
  }
}

const query = params.query;
if (typeof query !== 'string' || !query.trim()) {
  process.stderr.write('参数必须包含非空字符串 query\n');
  process.exit(1);
}

const maxResults = typeof params.max_results === 'number' ? params.max_results : 10;
const validFilters = ['hour', 'day', 'week', 'month', 'year'];
const recencyFilter =
  validFilters.includes(params.search_recency_filter) ? params.search_recency_filter : 'day';

// ─────────────────────────────────────────────
// 请求
// ─────────────────────────────────────────────

const TIMEOUT_MS = 30_000;
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

try {
  const resp = await fetch('https://api.perplexity.ai/search', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: query.trim(),
      max_results: maxResults,
      search_recency_filter: recencyFilter,
    }),
    signal: controller.signal,
  });

  clearTimeout(timer);

  if (!resp.ok) {
    const body = await resp.text().catch(() => '');
    process.stderr.write(`Perplexity Search API 请求失败：HTTP ${resp.status}\n${body}\n`);
    process.exit(1);
  }

  const data = await resp.json();
  const results = Array.isArray(data.results) ? data.results : [];

  process.stdout.write(JSON.stringify(results, null, 2) + '\n');
  process.exit(0);
} catch (err) {
  clearTimeout(timer);
  if (err.name === 'AbortError') {
    process.stderr.write(`Perplexity Search API 调用超时（${TIMEOUT_MS / 1000}s）\n`);
  } else {
    process.stderr.write(`Perplexity Search API 调用异常：${err.message}\n`);
  }
  process.exit(1);
}

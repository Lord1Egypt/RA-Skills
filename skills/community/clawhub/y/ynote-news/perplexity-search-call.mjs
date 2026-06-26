#!/usr/bin/env node
/**
 * perplexity-search-call.mjs — 调用 Perplexity Search API（POST /search）
 *
 * 直接返回结构化文章列表，不经过 OpenClaw 的 web_search 抽象层（Sonar API）。
 * API 文档：https://docs.perplexity.ai/docs/search/quickstart
 *
 * 依赖：Node.js >= 18（内置 fetch）
 * 用法（推荐 stdin / 临时文件方式，避免中文经 argv 编码损坏）：
 *   echo '{"query":"AI 大模型","max_results":10}' | node perplexity-search-call.mjs
 *   node perplexity-search-call.mjs /tmp/args.json          # 传文件路径
 *   node perplexity-search-call.mjs '{"query":"keyword"}'   # argv（仅 ASCII 安全）
 *
 * 参数（JSON）：
 *   query                (string)  必填，搜索关键词
 *   max_results          (number)  可选，默认 10，最大 20
 *   search_recency_filter (string) 可选，时间范围：hour / day（默认）/ week / month / year
 *
 * 输出：results JSON 数组写到 stdout，每条包含 title、url、date、last_updated、snippet
 * 错误：写 stderr 并 exit 1
 *
 * 入参优先级：临时文件路径（shell 包装层传入）> stdin（pipe / heredoc）> 内联 JSON 字符串（仅 ASCII 安全）。
 */

import fs from 'node:fs';
import path from 'node:path';

// ─────────────────────────────────────────────
// 参数解析（支持文件路径或内联 JSON，避免 bash 传中文 argv 编码问题）
// ─────────────────────────────────────────────

const rawArg = process.argv[2] ?? '';
let argsJson;
if (rawArg) {
  try {
    const stat = fs.statSync(rawArg, { throwIfNoEntry: false });
    if (stat?.isFile()) {
      argsJson = fs.readFileSync(rawArg, 'utf8').trim();
      fs.unlinkSync(rawArg);
    } else {
      argsJson = rawArg.trim();
    }
  } catch {
    argsJson = rawArg.trim();
  }
} else if (!process.stdin.isTTY) {
  argsJson = fs.readFileSync('/dev/stdin', 'utf8').trim();
} else {
  argsJson = '{}';
}

let params;
try {
  params = JSON.parse(argsJson);
} catch (e) {
  // 若文件或 argv 带有多余尾部字符（如换行、编码残留），尝试只解析到最后一个 }
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
// API Key（优先 process.env，其次从 openclaw.json 本 Skill 的 env 读取）
// OpenClaw 执行 exec 时不会把 skill env 注入子进程，故需主动读配置。
// ─────────────────────────────────────────────

function getApiKeyFromOpenClawConfig() {
  const configPath =
    process.env.OPENCLAW_CONFIG ||
    path.join(process.env.HOME || process.env.USERPROFILE || '', '.openclaw', 'openclaw.json');
  if (!configPath || !fs.existsSync(configPath)) return null;
  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    const data = JSON.parse(raw);
    const key =
      data?.skills?.entries?.['ynote-news']?.env?.PERPLEXITY_API_KEY ||
      data?.agents?.defaults?.env?.PERPLEXITY_API_KEY;
    return typeof key === 'string' && key.trim() ? key.trim() : null;
  } catch {
    return null;
  }
}

let apiKey = process.env.PERPLEXITY_API_KEY?.trim() || null;
if (!apiKey) apiKey = getApiKeyFromOpenClawConfig();
if (!apiKey) {
  process.stderr.write(
    '错误：未设置 PERPLEXITY_API_KEY\n' +
    '配置方式：\n' +
    '  1) 在 ~/.openclaw/openclaw.json 的 skills.entries["ynote-news"].env 中添加 "PERPLEXITY_API_KEY": "pplx-..."\n' +
    '  2) 或在 shell 中 export PERPLEXITY_API_KEY="pplx-..."（Key 在 https://www.perplexity.ai/settings/api 获取）\n'
  );
  process.exit(1);
}

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

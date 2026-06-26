#!/usr/bin/env node
/**
 * websearch-call.mjs — 通过 stdio 调用 open-websearch MCP Server 的 search 工具
 *
 * 不依赖 OpenClaw 的 mcpServers 配置，直接 spawn npx open-websearch@latest，
 * 用 MCP JSON-RPC over stdio（换行分隔）完成 initialize → tools/call(search)。
 *
 * 依赖：Node.js >= 18，npx（会拉取 open-websearch@latest）
 * 用法：node websearch-call.mjs '<json_args>'
 * 示例：node websearch-call.mjs '{"query":"AI 大模型","limit":10,"engines":["duckduckgo","bing"]}'
 *
 * 参数（JSON）：
 *   query   (string)  必填，搜索关键词
 *   limit   (number)  可选，默认 10
 *   engines (string[]) 可选，默认 ["duckduckgo","bing","baidu"]
 *
 * 输出：工具返回的 content[].text（通常为 JSON 数组字符串）写到 stdout；错误写 stderr 并 exit 1。
 */

import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';

const toolName = process.argv[2];
const argsJson = process.argv[3];
if (!argsJson) {
  process.stderr.write('用法: node websearch-call.mjs search \'{"query":"关键词","limit":10}\'\n');
  process.exit(1);
}

if (toolName !== 'search') {
  process.stderr.write('当前仅支持 tool: search\n');
  process.exit(1);
}

let params;
try {
  params = JSON.parse(argsJson);
} catch (e) {
  process.stderr.write(`参数不是合法 JSON: ${e.message}\n`);
  process.exit(1);
}

const query = params.query;
if (typeof query !== 'string' || !query.trim()) {
  process.stderr.write('参数必须包含非空字符串 query\n');
  process.exit(1);
}

const limit = typeof params.limit === 'number' ? params.limit : 10;
const engines = Array.isArray(params.engines) && params.engines.length > 0
  ? params.engines
  : ['duckduckgo', 'bing', 'baidu'];

const timeoutMs = 60_000;

const child = spawn('npx', ['open-websearch@latest'], {
  env: {
    ...process.env,
    MODE: 'stdio',
    DEFAULT_SEARCH_ENGINE: 'duckduckgo',
    ALLOWED_SEARCH_ENGINES: engines.join(','),
  },
  stdio: ['pipe', 'pipe', 'inherit'],
});

let resolved = false;
const finish = (err, text) => {
  if (resolved) return;
  resolved = true;
  clearTimeout(timer);
  try {
    child.kill('SIGTERM');
  } catch (_) {}
  if (err) {
    process.stderr.write(String(err) + '\n');
    process.exit(1);
  }
  process.stdout.write(text ?? '');
  process.exit(0);
};

const timer = setTimeout(() => {
  finish(new Error('open-websearch 调用超时（' + timeoutMs / 1000 + 's）'));
}, timeoutMs);

const rl = createInterface({ input: child.stdout, crlfDelay: Infinity });

let initDone = false;
const send = (msg) => {
  child.stdin.write(JSON.stringify(msg) + '\n');
};

// 1. initialize
send({
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'ynote-news-websearch-call', version: '1.0.0' },
  },
});

rl.on('line', (line) => {
  if (!line.trim()) return;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    return;
  }
  if (msg.id === 1 && msg.result) {
    initDone = true;
    send({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} });
    send({
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: { name: toolName, arguments: { query: query.trim(), limit, engines } },
    });
    return;
  }
  if (msg.id === 2) {
    if (msg.error) {
      finish(new Error(msg.error.message || JSON.stringify(msg.error)));
      return;
    }
    const content = msg.result?.content;
    const text = Array.isArray(content)
      ? content.map((c) => (c && typeof c.text === 'string' ? c.text : '')).join('')
      : '';
    finish(null, text || '');
  }
});

child.on('error', (err) => finish(err));
child.on('exit', (code) => {
  if (!resolved) finish(new Error('子进程退出 code=' + code));
});

#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const PROTOCOL_VERSION = '2025-06-18';
const DEFAULT_TIMEOUT_MS = 15_000;
const EXPECTED_HOST = 'xiaoan.39-108-49-182.sslip.io';
const TOOL_NAME_PATTERN = /^[a-z][a-z0-9_]{0,79}$/;

function result(ok, code, message, data = {}) {
  return { ok, code, message, data };
}

function safeMessage(value) {
  return String(value ?? '')
    .replace(/(Bearer\s+)[^\s]+/gi, '$1[redacted]')
    .replace(/((?:token|key)[:=]\s*)[^\s,;]+/gi, '$1[redacted]')
    .slice(0, 500);
}

function readEndpoint() {
  const manifestPath = path.resolve(__dirname, '..', 'skill.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const endpoint = new URL(manifest?.mcp_server?.url);
  if (endpoint.protocol !== 'https:' || endpoint.hostname !== EXPECTED_HOST || endpoint.pathname !== '/mcp') {
    throw Object.assign(new Error('小安 MCP 地址不在允许范围内。'), { code: 'MCP_CONFIG_ERROR' });
  }
  endpoint.hash = '';
  return endpoint.toString();
}

function readToken() {
  if (process.env.XIAOAN_MCP_AUTH_TOKEN) return process.env.XIAOAN_MCP_AUTH_TOKEN.trim();
  const authPath = path.join(os.homedir(), '.xiaoan', 'mcp-auth.json');
  try {
    const parsed = JSON.parse(fs.readFileSync(authPath, 'utf8'));
    return typeof parsed?.token === 'string' ? parsed.token.trim() : '';
  } catch {
    return '';
  }
}

function parseEventStream(text) {
  const payloads = [];
  let lines = [];
  for (const line of String(text).split(/\r?\n/)) {
    if (!line) {
      if (lines.length) payloads.push(lines.join('\n'));
      lines = [];
    } else if (line.startsWith('data:')) {
      lines.push(line.slice(5).trimStart());
    }
  }
  if (lines.length) payloads.push(lines.join('\n'));
  for (let index = payloads.length - 1; index >= 0; index -= 1) {
    try { return JSON.parse(payloads[index]); } catch {}
  }
  throw Object.assign(new Error('MCP SSE 响应无法解析。'), { code: 'MCP_INVALID_RESPONSE' });
}

function parsePayload(text, contentType = '') {
  const source = String(text ?? '').trim();
  if (!source) throw Object.assign(new Error('MCP 返回空响应。'), { code: 'MCP_INVALID_RESPONSE' });
  if (String(contentType).includes('text/event-stream') || /^data:/m.test(source)) return parseEventStream(source);
  return JSON.parse(source);
}

function parseToolText(resultValue) {
  const item = Array.isArray(resultValue?.content)
    ? resultValue.content.find((entry) => entry?.type === 'text' && typeof entry.text === 'string')
    : null;
  if (!item) return resultValue?.structuredContent ?? resultValue;
  try { return JSON.parse(item.text); } catch { return item.text; }
}

async function rpc(method, params, { endpoint, token, timeoutMs = DEFAULT_TIMEOUT_MS } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let response;
  try {
    response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json, text/event-stream',
        'Mcp-Protocol-Version': PROTOCOL_VERSION,
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: `xiaoan-${Date.now()}-${Math.random().toString(16).slice(2, 10)}`,
        method,
        params,
      }),
      signal: controller.signal,
    });
  } catch (error) {
    const code = error?.name === 'AbortError' ? 'MCP_TIMEOUT' : 'MCP_NETWORK_ERROR';
    throw Object.assign(new Error(code === 'MCP_TIMEOUT' ? 'MCP 请求超时。' : '无法连接小安 MCP。'), { code });
  } finally {
    clearTimeout(timer);
  }
  const text = await response.text();
  if (response.status === 401) {
    throw Object.assign(new Error('小安 MCP 授权无效或已过期。'), { code: 'MCP_AUTH_REQUIRED' });
  }
  if (!response.ok) throw Object.assign(new Error(`MCP HTTP ${response.status}`), { code: 'MCP_HTTP_ERROR' });
  const payload = parsePayload(text, response.headers.get('content-type') || '');
  if (payload?.error) throw Object.assign(new Error(payload.error.message || 'MCP 调用失败。'), { code: 'MCP_RPC_ERROR' });
  return payload.result;
}

function parseCli(argv) {
  if (argv.length === 1 && argv[0] === 'list') return { command: 'list' };
  if (argv[0] !== 'call' || !TOOL_NAME_PATTERN.test(argv[1] || '')) {
    throw Object.assign(new Error('用法：list | call <toolName> [--args <jsonObject>]'), { code: 'MCP_INVALID_ARGUMENTS' });
  }
  if (argv.length === 2) return { command: 'call', tool: argv[1], args: {} };
  if (argv.length === 4 && argv[2] === '--args') {
    const args = JSON.parse(argv[3]);
    if (!args || typeof args !== 'object' || Array.isArray(args)) throw new Error('--args 必须是 JSON 对象。');
    return { command: 'call', tool: argv[1], args };
  }
  throw Object.assign(new Error('参数无效。'), { code: 'MCP_INVALID_ARGUMENTS' });
}

async function run(argv) {
  let parsed;
  try { parsed = parseCli(argv); } catch (error) {
    return result(false, error.code || 'MCP_INVALID_ARGUMENTS', safeMessage(error.message));
  }
  const token = readToken();
  if (!token) {
    return result(false, 'MCP_AUTH_REQUIRED', '未找到小安 MCP 授权。预约未创建；请由商家完成 Agent 授权，不要启动本地 mock。');
  }
  try {
    const endpoint = readEndpoint();
    if (parsed.command === 'list') {
      const value = await rpc('tools/list', {}, { endpoint, token });
      return result(true, 'MCP_TOOLS_LIST', '已获取小安 MCP 工具列表。', { tools: value?.tools ?? [] });
    }
    const value = await rpc('tools/call', { name: parsed.tool, arguments: parsed.args }, { endpoint, token });
    return result(true, 'MCP_TOOL_RESULT', '小安 MCP 工具调用完成。', {
      tool: parsed.tool,
      result: parseToolText(value),
      structuredContent: value?.structuredContent ?? null,
      isError: Boolean(value?.isError),
    });
  } catch (error) {
    return result(false, error.code || 'MCP_FAILED', safeMessage(error.message));
  }
}

run(process.argv.slice(2)).then((output) => {
  process.stdout.write(`${JSON.stringify(output)}\n`);
  process.exitCode = output.ok ? 0 : 1;
});

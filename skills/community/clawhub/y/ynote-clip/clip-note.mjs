#!/usr/bin/env node

/**
 * clip-note.mjs — 网页剪藏笔记创建（Node.js，零外部依赖）
 *
 * 替代 process-images.sh + clip-note.sh，统一处理：
 *   1. 图片并行下载 + 压缩 + base64 编码
 *   2. MCP SSE 调用（clipperSaveWithImages / createNote 自动降级）
 *
 * 图片下载直接流式落临时文件，压缩全程文件操作，仅上传前一次性读取 base64。
 *
 * 依赖：Node.js >= 18（内置 fetch、parseArgs）
 *   - macOS：使用内置 sips 压缩图片
 *   - Linux：使用 ImageMagick（convert / identify）压缩图片
 *   - 压缩工具缺失时自动降级为原图，不阻塞主流程
 * 用法：
 *   # 模式 A：分离参数（bodyHtml 已写入文件）
 *   node clip-note.mjs \
 *     --title "笔记标题" \
 *     --body-file /tmp/body.html \
 *     --image-urls '["url1","url2"]' \
 *     --source-url "https://example.com"
 *
 *   # 模式 B：数据文件（browser CLI 输出直接管道到文件，绕过 agent context）
 *   node clip-note.mjs \
 *     --data-file /tmp/youdaonote-clip-data.json \
 *     --source-url "https://example.com"
 *
 *   data-file JSON 格式：{ "title": "...", "content": "...", "imageUrls": [...], "source": "..." }
 *
 *   # 模式 C：服务端剪藏（国内网站快速路径，无需本地浏览器）
 *   node clip-note.mjs \
 *     --clip-web-page \
 *     --source-url "https://example.com"
 *
 * 环境变量：
 *   YOUDAONOTE_API_KEY      — MCP Server API Key（必需）
 *   YOUDAONOTE_MCP_URL      — MCP SSE 端点（默认 production）
 *   YOUDAONOTE_MCP_TIMEOUT  — 超时秒数（默认 120）
 *   YOUDAONOTE_CLIP_DEBUG  — 调试日志目录（可选，设置后开启调试并写入日志文件）
 */

import https from 'node:https';
import http from 'node:http';
import dns from 'node:dns';
import { URL } from 'node:url';
import { parseArgs } from 'node:util';
import {
  writeFileSync, mkdirSync, rmSync, statSync, createWriteStream, appendFileSync, existsSync, renameSync,
} from 'node:fs';
import { Readable } from 'node:stream';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash, randomUUID } from 'node:crypto';
import { marked } from './static/marked.mjs';

// ─────────────────────────────────────────────
// Configuration
// ─────────────────────────────────────────────

const MAX_IMAGES = 20;
const CONCURRENT = 5;
const MAX_DOWNLOAD_SIZE = 50 * 1024 * 1024; // 50MB per image (disk check,防止异常大文件)
const MAX_FINAL_SIZE = 512 * 1024;          // 512KB per image (服务端上传限制，不可改)
const RESIZE_WIDTH = 1920;
const COMPRESS_THRESHOLD = 512 * 1024;     // > 512KB → compress
const JPEG_QUALITIES = [80, 60, 40];       // 渐进式质量降低
const CONNECT_TIMEOUT_MS = 15_000;

// ─────────────────────────────────────────────
// Image Cache（C1 优化：避免重复下载/压缩）
// ─────────────────────────────────────────────

const CACHE_DIR = join(tmpdir(), 'youdaonote-clip-cache');
const CACHE_TTL_MS = 60 * 60 * 1000;  // 1 小时

function getCacheKey(url) {
  return createHash('sha256').update(url).digest('hex').slice(0, 16);
}

function writeImageCache(url, data) {
  try {
    mkdirSync(CACHE_DIR, { recursive: true });
    const key = getCacheKey(url);
    const cacheFile = join(CACHE_DIR, `${key}.json`);
    const { data: _omit, ...rest } = data || {};
    writeFileSync(cacheFile, JSON.stringify({ timestamp: Date.now(), data: rest }));
  } catch {
    // 缓存写入失败不影响主流程
  }
}

// 配置项：由 clip-note.sh 从 env 解析后通过 argv 传入，在 main() 的 parseArgs 中赋值。
let SSE_URL = 'https://open.mail.163.com/api/ynote/mcp/sse';
let API_KEY = '';
let MCP_TIMEOUT_MS = 120_000;
let DEBUG_DIR = '';
let DEBUG = false;

/** 当前请求的 debug key（从 data-file 读取或自生成，用于串联整条剪藏流程） */
let currentDebugKey = null;

function generateDebugKey() {
  return randomUUID().slice(0, 8);
}

// 调试日志（YOUDAONOTE_CLIP_DEBUG 路径模式：按 key 分目录，main.log）
function getDebugLogFile() {
  if (!DEBUG) return null;
  if (!currentDebugKey) return null;
  return join(DEBUG_DIR, currentDebugKey, 'main.log');
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
      if (!existsSync(logDir)) mkdirSync(logDir, { recursive: true });
      appendFileSync(logFile, logLine);
    }
  } catch { /* 日志写入失败不影响主流程 */ }
  console.log(...args);
}

/** 入口参数日志（脱敏：content/image-urls 仅记录长度/数量；大 content 写入 entry-content.txt） */
function logEntryParams(values, { content } = {}) {
  if (!DEBUG) return;
  const s = {};
  for (const [k, v] of Object.entries(values)) {
    if (k === 'content') s[k] = `[${typeof v === 'string' ? v.length : 0} chars]`;
    else if (k === 'image-urls') {
      try { s[k] = `[${(JSON.parse(v || '[]')).length} items]`; } catch { s[k] = v; }
    } else s[k] = v;
  }
  debug(`🔍 clip-note 入口 — params: ${JSON.stringify(s)}`);
  if (content && typeof content === 'string' && currentDebugKey) {
    try {
      const logDir = join(DEBUG_DIR, currentDebugKey);
      if (!existsSync(logDir)) mkdirSync(logDir, { recursive: true });
      const preview = content.length > 200 ? content.slice(0, 200) + '...' : content;
      writeFileSync(join(logDir, 'entry-content.txt'), `[${content.length} chars] ${preview}`);
    } catch { /* 写入失败不影响主流程 */ }
  }
}

/**
 * 净化笔记标题（与 ydoc/ynote-desktop 保持一致）：
 *   1. 将 Windows 文件系统禁止字符 \ / < > : * ? " 替换为 _
 *   2. 主体部分（不含后缀）超过 maxLength 时截断
 *   3. 追加 .clip 后缀
 * @param {string} raw  原始标题
 * @param {number} [maxLength=80]  主体部分最大字符数
 * @returns {string}  净化后的标题（含 .clip 后缀）
 */
function sanitizeTitle(raw, maxLength = 80) {
  const sanitized = raw.replace(/(\\|\/|<|>|:|\*|\?|")/g, '_');
  const mainPart = sanitized.length > maxLength
    ? sanitized.slice(0, maxLength)
    : sanitized;
  return mainPart + '.clip';
}

// ─────────────────────────────────────────────
// SSE Parser（from perf-test/mcp-perf-test.mjs）
// ─────────────────────────────────────────────

class SseParser {
  #eventType = '';
  #dataLines = [];
  #buffer = '';
  #onEvent;

  constructor(onEvent) { this.#onEvent = onEvent; }

  feed(chunk) {
    this.#buffer += chunk;
    const lines = this.#buffer.split('\n');
    this.#buffer = lines.pop();

    for (let line of lines) {
      line = line.replace(/\r$/, '');
      if (line === '') {
        if (this.#dataLines.length > 0) {
          this.#onEvent({ type: this.#eventType || 'message', data: this.#dataLines.join('\n') });
        }
        this.#eventType = '';
        this.#dataLines = [];
      } else if (!line.startsWith(':')) {
        const colonIdx = line.indexOf(':');
        let field, value;
        if (colonIdx === -1) { field = line; value = ''; }
        else {
          field = line.slice(0, colonIdx);
          value = line.slice(colonIdx + 1);
          if (value.startsWith(' ')) value = value.slice(1);
        }
        if (field === 'event') this.#eventType = value;
        else if (field === 'data') this.#dataLines.push(value);
      }
    }
  }
}

// ─────────────────────────────────────────────
// MCP SSE Client（simplified from perf-test）
// ─────────────────────────────────────────────

class McpClient {
  #sseUrl;
  #apiKey;
  #timeoutMs;
  #messageUrl = null;
  #pendingRequests = new Map();
  #nextId = 1;
  #request = null;
  #response = null;
  #connected = false;

  constructor(sseUrl, apiKey, timeoutMs) {
    this.#sseUrl = new URL(sseUrl);
    this.#apiKey = apiKey;
    this.#timeoutMs = timeoutMs;
  }

  connect() {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.close();
        reject(new Error(`SSE 连接超时 (${CONNECT_TIMEOUT_MS}ms)`));
      }, CONNECT_TIMEOUT_MS);

      const proto = this.#sseUrl.protocol === 'https:' ? https : http;
      const parser = new SseParser((event) => {
        if (event.type === 'endpoint') {
          this.#messageUrl = new URL(event.data, this.#sseUrl);
          this.#connected = true;
          clearTimeout(timer);
          resolve();
        } else if (event.type === 'message') {
          this.#handleMessage(event.data);
        }
      });

      this.#request = proto.request({
        hostname: this.#sseUrl.hostname,
        port: this.#sseUrl.port || (this.#sseUrl.protocol === 'https:' ? 443 : 80),
        path: this.#sseUrl.pathname + this.#sseUrl.search,
        method: 'GET',
        headers: { 'Accept': 'text/event-stream', 'Cache-Control': 'no-cache', 'x-api-key': this.#apiKey },
      }, (res) => {
        if (res.statusCode !== 200) { clearTimeout(timer); reject(new Error(`SSE HTTP ${res.statusCode}`)); return; }
        this.#response = res;
        res.setEncoding('utf-8');
        res.on('data', (chunk) => parser.feed(chunk));
        res.on('end', () => this.#onDisconnect());
        res.on('error', (err) => { clearTimeout(timer); reject(err); });
      });

      this.#request.on('error', (err) => { clearTimeout(timer); reject(err); });
      this.#request.end();
    });
  }

  #handleMessage(data) {
    try {
      const msg = JSON.parse(data);
      if (msg.id != null && this.#pendingRequests.has(msg.id)) {
        const p = this.#pendingRequests.get(msg.id);
        this.#pendingRequests.delete(msg.id);
        p.resolve(msg);
      }
    } catch { /* ignore unparsable */ }
  }

  #onDisconnect() {
    this.#connected = false;
    for (const [, p] of this.#pendingRequests) p.reject(new Error('SSE 连接断开'));
    this.#pendingRequests.clear();
  }

  async #post(body) {
    if (!this.#connected) throw new Error('未连接');
    return fetch(this.#messageUrl.toString(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'x-api-key': this.#apiKey },
      body: JSON.stringify(body),
    });
  }

  async sendRequest(method, params = {}) {
    const id = this.#nextId++;
    const rpcBody = { jsonrpc: '2.0', id, method, params };

    let resolveRes, rejectRes;
    const promise = new Promise((res, rej) => { resolveRes = res; rejectRes = rej; });
    const timer = setTimeout(() => { this.#pendingRequests.delete(id); rejectRes(new Error(`超时 ${this.#timeoutMs}ms: ${method}`)); }, this.#timeoutMs);

    this.#pendingRequests.set(id, {
      resolve: (msg) => { clearTimeout(timer); resolveRes(msg); },
      reject: (err) => { clearTimeout(timer); rejectRes(err); },
    });

    const postRes = await this.#post(rpcBody);

    // Handle direct JSON response (some Spring AI versions)
    try {
      const ct = postRes.headers.get('content-type') || '';
      if (ct.includes('application/json')) {
        const direct = await postRes.json();
        if (direct?.jsonrpc && direct.id === id && this.#pendingRequests.has(id)) {
          this.#pendingRequests.delete(id);
          clearTimeout(timer);
          resolveRes(direct);
        }
      }
    } catch { /* non-JSON, wait SSE */ }

    return promise;
  }

  async initialize() {
    const res = await this.sendRequest('initialize', {
      protocolVersion: '2024-11-05', capabilities: {},
      clientInfo: { name: 'youdaonote-clip', version: '1.3.0' },
    });
    if (res.error) throw new Error(`初始化失败: ${res.error.message}`);
    await this.#post({ jsonrpc: '2.0', method: 'notifications/initialized' });
  }

  async callTool(name, args = {}) {
    const res = await this.sendRequest('tools/call', { name, arguments: args });
    const isError = !!res.error || !!res.result?.isError;
    const text = res.result?.content?.map(c => c.text).join('') || res.error?.message || '未知响应';
    return { text, isError };
  }

  close() {
    this.#connected = false;
    if (this.#response) this.#response.destroy();
    if (this.#request) this.#request.destroy();
    for (const [, p] of this.#pendingRequests) p.reject(new Error('客户端关闭'));
    this.#pendingRequests.clear();
  }
}

// ─────────────────────────────────────────────
// Concurrency Pool
// ─────────────────────────────────────────────

async function pool(items, concurrency, fn) {
  const results = new Array(items.length);
  let idx = 0;
  const workers = Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    while (idx < items.length) {
      const i = idx++;
      try { results[i] = { ok: true, value: await fn(items[i], i) }; }
      catch (err) { results[i] = { ok: false, error: err.message, input: items[i] }; }
    }
  });
  await Promise.all(workers);
  return results;
}

// ─────────────────────────────────────────────
// Image Processing
// ─────────────────────────────────────────────

function guessMimeType(url, contentType) {
  if (contentType && contentType !== 'application/octet-stream') return contentType;
  const lower = url.toLowerCase();
  if (lower.includes('.png')) return 'image/png';
  if (lower.includes('.gif')) return 'image/gif';
  if (lower.includes('.webp')) return 'image/webp';
  if (lower.includes('.svg')) return 'image/svg+xml';
  return 'image/jpeg';
}

function mimeToExt(mimeType) {
  const map = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
  };
  return map[mimeType] ?? '.jpg';
}

async function downloadImage(url, referer, destPath) {
  try {
    return await fetchImageViaFetch(url, referer, 10_000, destPath);
  } catch (e) {
    // 仅在超时时触发通用 DNS fallback（可能是系统 DNS 被污染）
    if (e.name === 'AbortError' || (e.message && e.message.includes('timeout'))) {
      debug(`🔍 DNS fallback 触发 — url: ${url}, 原因: ${e.message}`);
      return await fetchImageWithDnsFallback(url, referer, destPath);
    }
    throw e;
  }
}

async function fetchImageViaFetch(url, referer, timeoutMs, destPath) {
  const res = await fetch(url, {
    headers: {
      'Referer': referer,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    },
    signal: AbortSignal.timeout(timeoutMs),
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const contentType = res.headers.get('content-type')?.split(';')[0]?.trim() || '';

  // 流式写文件，不把整个响应体读入内存
  // res.body 是 Web Streams API ReadableStream，通过 Readable.fromWeb 转为 Node.js 流
  await new Promise((resolve, reject) => {
    const ws = createWriteStream(destPath);
    ws.on('finish', resolve);
    ws.on('error', reject);
    Readable.fromWeb(res.body).pipe(ws);
  });

  return { destPath, contentType };
}

/**
 * 通用 DNS fallback：用 Google DNS（8.8.8.8）重新解析，再通过 IP 直连绕过系统 DNS。
 * 适用于系统 DNS 被污染导致超时的情况（不限域名）。
 * 纯 Node.js 实现（dns.Resolver + https/http），无需 dig/curl。
 */
async function fetchImageWithDnsFallback(url, referer, destPath) {
  const parsed = new URL(url);
  const hostname = parsed.hostname;

  const resolver = new dns.Resolver();
  resolver.setServers(['8.8.8.8']);
  const ip = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`DNS fallback 超时: ${hostname}`)), 5_000);
    resolver.resolve4(hostname, (err, addresses) => {
      clearTimeout(timer);
      if (err) reject(new Error(`DNS fallback 解析失败: ${hostname} — ${err.message}`));
      else if (!addresses || addresses.length === 0) reject(new Error(`DNS fallback 无结果: ${hostname}`));
      else resolve(addresses[0]);
    });
  });

  debug(`🔍 DNS fallback — ${hostname} → ${ip}，通过 IP 直连下载`);

  const proto = parsed.protocol === 'https:' ? https : http;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { req.destroy(); reject(new Error('DNS fallback 下载超时（15s）')); }, 15_000);
    const req = proto.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': referer,
      },
      lookup: (_host, _opts, cb) => cb(null, ip, 4),
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        clearTimeout(timer);
        res.resume();
        fetchImageWithDnsFallback(res.headers.location, referer, destPath).then(resolve, reject);
        return;
      }
      const ws = createWriteStream(destPath);
      res.pipe(ws);
      ws.on('finish', () => { clearTimeout(timer); resolve({ destPath, contentType: res.headers['content-type'] || '' }); });
      ws.on('error', (e) => { clearTimeout(timer); reject(e); });
    });
    req.on('error', (e) => { clearTimeout(timer); reject(e); });
  });
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────

async function main() {
  // ── CLI 参数 ──
  const { values } = parseArgs({
    options: {
      title:           { type: 'string' },   // 模式 A 专用（向后兼容）
      'body-file':     { type: 'string' },
      'data-file':     { type: 'string' },
      'image-urls':    { type: 'string', default: '[]' },
      'source-url':    { type: 'string' },
      markdown:        { type: 'boolean', default: false },
      'clip-web-page': { type: 'boolean', default: false },  // 模式 C：服务端剪藏
      'create-note':   { type: 'boolean', default: false },  // 模式 D：直接创建笔记（大内容支持）
      content:         { type: 'string' },   // 模式 D 专用：笔记内容
      'folder-id':     { type: 'string', default: '' },  // 模式 D 专用：目标文件夹
      'download-images': { type: 'boolean', default: false },
      upload:            { type: 'boolean', default: false },
      'tmp-dir':         { type: 'string' },
      'api-key':       { type: 'string' },   // 由 clip-note.sh 从 env 传入
      'sse-url':       { type: 'string' },
      'mcp-timeout':   { type: 'string' },
      'debug-dir':     { type: 'string' },
    },
    strict: true,
  });

  // 从 argv 初始化配置（由 clip-note.sh 从 env 解析后传入）
  if (values['api-key']) API_KEY = values['api-key'].trim();
  if (values['sse-url']) SSE_URL = values['sse-url'];
  if (values['mcp-timeout']) MCP_TIMEOUT_MS = parseInt(values['mcp-timeout'], 10) * 1_000;
  if (values['debug-dir']) { DEBUG_DIR = values['debug-dir'].trim(); DEBUG = DEBUG_DIR !== ''; }

  if (!API_KEY) {
    console.error('错误：未设置 YOUDAONOTE_API_KEY。请在 OpenClaw config 的 youdaonote-clip.env 中配置，或 export YOUDAONOTE_API_KEY');
    process.exit(1);
  }

  if (values['download-images']) {
    const imageUrls = JSON.parse(values['image-urls'] || '[]');
    const sourceUrl = values['source-url'] || '';
    const baseTmpDir = values['tmp-dir'];
    if (!baseTmpDir) { console.error('错误：--download-images 需要 --tmp-dir'); process.exit(1); }

    currentDebugKey = DEBUG ? generateDebugKey() : null;
    debug('🔍 模式: download-images');

    mkdirSync(baseTmpDir, { recursive: true });

    if (imageUrls.length === 0) {
      writeFileSync(join(baseTmpDir, 'manifest.json'), '[]');
      console.log(JSON.stringify({ ok: true, count: 0, failed: 0, tmpDir: baseTmpDir }));
      return;
    }

    const urls = imageUrls.slice(0, MAX_IMAGES);
    const pipelineStart = Date.now();

    const results = await pool(urls, CONCURRENT, async (url, i) => {
      const rawPath = join(baseTmpDir, `raw_${i}.bin`);
      const { contentType } = await downloadImage(url, sourceUrl, rawPath);
      const fileSize = statSync(rawPath).size;
      if (fileSize > MAX_DOWNLOAD_SIZE) {
        throw new Error(`文件过大: ${fileSize} bytes`);
      }
      const mimeType = guessMimeType(url, contentType);
      if (DEBUG) {
        const ext = mimeToExt(mimeType);
        const renamedPath = rawPath.replace(/\.bin$/, ext);
        renameSync(rawPath, renamedPath);
        return { index: i, path: renamedPath, mimeType, url, origSize: statSync(renamedPath).size };
      }
      return { index: i, path: rawPath, mimeType, url, origSize: fileSize };
    });

    const manifest = [];
    let dlFail = 0;
    for (const [i, r] of results.entries()) {
      if (!r.ok) {
        dlFail++;
        debug(`🔍 图片 [${i + 1}/${urls.length}] — url: ${r.input}, 状态: ❌ ${r.error}`);
        continue;
      }
      manifest.push(r.value);
    }

    const pipelineTime = ((Date.now() - pipelineStart) / 1000).toFixed(1);
    debug(`🔍 图片下载完成 — 成功: ${manifest.length}, 失败: ${dlFail}, ⏱ ${pipelineTime}s`);

    writeFileSync(join(baseTmpDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
    console.log(JSON.stringify({ ok: true, count: manifest.length, failed: dlFail, tmpDir: baseTmpDir }));
    return;
  }

  if (values.upload) {
    // Read complete payload from stdin
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    const payload = JSON.parse(Buffer.concat(chunks).toString('utf-8'));

    const { title, bodyHtml, sourceUrl, images, markdown: isMarkdown } = payload;
    currentDebugKey = payload._debugKey || (DEBUG ? generateDebugKey() : null);
    debug('🔍 模式: upload');

    let finalBodyHtml = bodyHtml;

    // Markdown → HTML 转换
    if (isMarkdown && finalBodyHtml) {
      debug(`🔍 Markdown → HTML 转换（marked），原文 ${finalBodyHtml.length} 字符`);
      finalBodyHtml = marked.parse(finalBodyHtml);
      debug(`🔍 转换完成，HTML ${finalBodyHtml.length} 字符`);
    }

    // Filter out skipped images, format for MCP
    // URL 中的 & 编码为 &amp; 以匹配 bodyHtml 中的 HTML entities（MCP 服务端按 URL 匹配替换）
    const validImages = (images || [])
      .filter(img => !img.skipped && img.base64Data)
      .map(img => ({ url: img.url.replace(/&/g, '&amp;'), mimeType: img.finalMime || img.mimeType, data: img.base64Data }));

    debug(`🔍 MCP 上传 — title: "${title}", body: ${(finalBodyHtml || '').length} 字符, images: ${validImages.length} 张`);

    const client = new McpClient(SSE_URL, API_KEY, MCP_TIMEOUT_MS);
    try {
      await client.connect();
      await client.initialize();

      const mcpStart = Date.now();
      let result = await client.callTool('clipperSaveWithImages', {
        title,
        bodyHtml: finalBodyHtml,
        sourceUrl,
        images: JSON.stringify(validImages),
      });
      let mcpTime = ((Date.now() - mcpStart) / 1000).toFixed(1);

      // 降级判断
      const fallbackPattern = /unknown tool|not found|not implemented|未知|不存在/i;
      if (result.isError && fallbackPattern.test(result.text)) {
        debug('🔍 clipperSaveWithImages 不可用，降级为 createNote');
        const imagesLite = validImages.map(({ url, mimeType }) => ({ url, mimeType }));
        const content = JSON.stringify({ bodyHtml: finalBodyHtml, sourceUrl, images: imagesLite });

        debug(`🔍 MCP 请求 — tool: createNote (降级), title: "${title}"`);
        const fbStart = Date.now();
        result = await client.callTool('createNote', { title, content, folderId: '' });
        mcpTime = ((Date.now() - fbStart) / 1000).toFixed(1);
      }

      debug(`🔍 MCP 响应 — ${result.text}, ⏱ ${mcpTime}s`);

      if (result.isError) {
        throw new Error(`MCP 调用失败：${result.text}`);
      }
      console.log(JSON.stringify({ ok: true, message: result.text }));
    } finally {
      client.close();
    }
    return;
  }

  // ── 模式 D：直接创建笔记（大内容支持，绕过 ARG_MAX 限制）──
  if (values['create-note']) {
    currentDebugKey = DEBUG ? generateDebugKey() : null;
    debug('🔍 路径: create-note 直接创建');
    logEntryParams(values, { content: values.content });
    const title = values.title;
    const content = values.content;
    const folderId = values['folder-id'] || '';

    if (!title) { console.error('错误：--create-note 模式需要 --title'); process.exit(1); }
    if (content === undefined) { console.error('错误：--create-note 模式需要 --content'); process.exit(1); }

    debug(`🔍 创建笔记模式 — title: "${title}", content: ${content.length} 字符, folderId: "${folderId}"`);
    const client = new McpClient(SSE_URL, API_KEY, MCP_TIMEOUT_MS);
    try {
      await client.connect();
      await client.initialize();

      const mcpStart = Date.now();
      const result = await client.callTool('createNote', { title, content, folderId });
      const mcpTime = ((Date.now() - mcpStart) / 1000).toFixed(1);
      debug(`🔍 MCP 响应 — ${result.text}, ⏱ ${mcpTime}s`);

      if (result.isError) throw new Error(`MCP 调用失败：${result.text}`);
      console.log(result.text);  // 输出笔记 ID 或成功消息
    } finally {
      client.close();
    }
    return;
  }

  // ── 模式 C：服务端剪藏（国内快速路径）──
  if (values['clip-web-page']) {
    currentDebugKey = DEBUG ? generateDebugKey() : null;
    debug('🔍 路径: B (clipWebPage 服务端剪藏)');
    logEntryParams(values);
    const sourceUrl = values['source-url'];
    if (!sourceUrl) { console.error('错误：--clip-web-page 模式需要 --source-url'); process.exit(1); }

    debug(`🔍 服务端剪藏模式 — url: ${sourceUrl}`);
    const client = new McpClient(SSE_URL, API_KEY, MCP_TIMEOUT_MS);
    try {
      await client.connect();
      await client.initialize();

      const mcpStart = Date.now();
      const result = await client.callTool('clipWebPage', { url: sourceUrl });
      const mcpTime = ((Date.now() - mcpStart) / 1000).toFixed(1);
      debug(`🔍 MCP 响应 — ${result.text}, ⏱ ${mcpTime}s`);

      if (result.isError) throw new Error(`MCP 调用失败：${result.text}`);
      console.log(JSON.stringify({ ok: true, message: result.text }));
    } finally {
      client.close();
    }
    return;
  }

}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

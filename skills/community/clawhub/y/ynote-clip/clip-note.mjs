#!/usr/bin/env node

/**
 * clip-note.mjs — 网页剪藏笔记创建（Node.js，零外部依赖）
 *
 * 替代 process-images.sh + clip-note.sh，统一处理：
 *   1. 图片并行下载 + sips 压缩 + base64 编码
 *   2. MCP SSE 调用（clipWebPageWithResources / createNote 自动降级）
 *
 * 所有大数据在内存中流转，无需中间文件（仅 sips 压缩需临时文件 I/O）。
 *
 * 依赖：Node.js >= 18（内置 fetch、parseArgs）、sips（macOS 图片压缩）
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
 *     --data-file /tmp/ynote-clip-data.json \
 *     --source-url "https://example.com"
 *
 *   data-file JSON 格式：{ "title": "...", "content": "...", "imageUrls": [...], "source": "..." }
 *
 * 环境变量：
 *   YNOTE_API_KEY      — MCP Server API Key（必需）
 *   YNOTE_MCP_URL      — MCP SSE 端点（默认 production）
 *   YNOTE_MCP_TIMEOUT  — 超时秒数（默认 120）
 */

import https from 'node:https';
import http from 'node:http';
import { URL } from 'node:url';
import { parseArgs } from 'node:util';
import {
  readFileSync, writeFileSync, mkdirSync, rmSync, statSync,
} from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { marked } from './static/marked.mjs';

// ─────────────────────────────────────────────
// Configuration
// ─────────────────────────────────────────────

const MAX_IMAGES = 20;
const CONCURRENT = 5;
const MAX_SIZE = 10 * 1024 * 1024;        // 10MB per image (download limit)
const MAX_FINAL_SIZE = 512 * 1024;        // 512KB per image (post-compress limit)
const RESIZE_WIDTH = 1920;
const COMPRESS_THRESHOLD = 512 * 1024;     // > 512KB → compress
const JPEG_QUALITIES = [80, 60, 40];       // 渐进式质量降低
const CONNECT_TIMEOUT_MS = 15_000;

const SSE_URL = process.env.YNOTE_MCP_URL || 'https://open.mail.163.com/api/ynote/mcp/sse';
const API_KEY = process.env.YNOTE_API_KEY;
const MCP_TIMEOUT_MS = (parseInt(process.env.YNOTE_MCP_TIMEOUT || '120', 10)) * 1_000;
const DEBUG = process.env.YNOTE_CLIP_DEBUG === '1';

// 调试日志（仅 YNOTE_CLIP_DEBUG=1 时输出）
function debug(...args) { if (DEBUG) console.log(...args); }

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
      clientInfo: { name: 'ynote-clip', version: '1.3.0' },
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

async function downloadImage(url, referer) {
  try {
    return await fetchImageViaFetch(url, referer, 10_000);
  } catch (e) {
    // 仅在超时时触发通用 DNS fallback（可能是系统 DNS 被污染）
    if (e.name === 'AbortError' || (e.message && e.message.includes('timeout'))) {
      debug(`🔍 DNS fallback 触发 — url: ${url}, 原因: ${e.message}`);
      return await fetchImageWithDnsFallback(url, referer);
    }
    throw e;
  }
}

async function fetchImageViaFetch(url, referer, timeoutMs) {
  const res = await fetch(url, {
    headers: {
      'Referer': referer,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    },
    signal: AbortSignal.timeout(timeoutMs),
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  const contentType = res.headers.get('content-type')?.split(';')[0]?.trim() || '';
  return { buffer, contentType };
}

/**
 * 通用 DNS fallback：用 Google DNS（8.8.8.8）重新解析，再通过 curl --resolve 绕过系统 DNS。
 * 适用于系统 DNS 被污染导致超时的情况（不限域名）。
 * dig 不可用时直接抛出，由上层 pool 标记为下载失败（graceful skip）。
 */
async function fetchImageWithDnsFallback(url, referer) {
  const parsed = new URL(url);
  const hostname = parsed.hostname;
  const port = parsed.port || (parsed.protocol === 'https:' ? '443' : '80');

  // 用 Google DNS 重新解析（dig 不可用时抛出，上层 pool 会 skip 此图片）
  let ip;
  try {
    const digOut = execFileSync('dig', [hostname, '@8.8.8.8', '+short'], { encoding: 'utf8', timeout: 5_000 });
    ip = digOut.trim().split('\n').filter(l => /^\d+\.\d+\.\d+\.\d+$/.test(l)).at(-1);
  } catch (e) {
    const isDignNotFound = e.code === 'ENOENT';
    throw new Error(isDignNotFound
      ? `DNS fallback 不可用（dig 未安装）: ${hostname}`
      : `DNS fallback dig 失败: ${hostname} — ${e.message}`);
  }
  if (!ip) throw new Error(`DNS fallback 解析失败，无有效 IP: ${hostname}`);

  debug(`🔍 DNS fallback — ${hostname} → ${ip}，通过 curl --resolve 下载`);

  // 用 curl --resolve 绕过系统 DNS
  const result = execFileSync('curl', [
    '--max-time', '15',
    '--resolve', `${hostname}:${port}:${ip}`,
    '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    '-H', `Referer: ${referer}`,
    '-L', '-s', '-o', '-',
    url,
  ], { timeout: 20_000 });

  return { buffer: result, contentType: '' };
}

/**
 * 图片压缩：宽度 > 1920 缩放，> 512KB 渐进式转 JPEG (80/60/40)。
 * gif 超 512KB 时转为静态 JPEG（提取第一帧）。
 * macOS 使用内置 sips，Linux 使用 ImageMagick（需安装 imagemagick）。
 * 工具不可用或压缩失败时，graceful 降级为原图。
 * 返回 { buffer, mimeType, compressed, skipped }，skipped=true 表示压缩后仍超 512KB。
 */
function compressImage(buffer, mimeType, tmpDir) {
  // SVG 不压缩（文本格式，体积小）
  if (mimeType === 'image/svg+xml') {
    return { buffer, mimeType, compressed: false, skipped: false };
  }

  // 已在阈值内的非 gif 图片直接返回
  if (mimeType !== 'image/gif' && buffer.length <= COMPRESS_THRESHOLD) {
    return { buffer, mimeType, compressed: false, skipped: false };
  }

  const inputPath = join(tmpDir, 'raw.bin');
  writeFileSync(inputPath, buffer);

  let compressed = false;
  let finalPath = inputPath;
  let finalMime = mimeType;

  const isMac = process.platform === 'darwin';

  try {
    if (isMac) {
      // ── macOS：使用内置 sips ──────────────────────────────────────────

      // gif → 转静态 JPEG（sips 自动取第一帧）
      if (mimeType === 'image/gif') {
        const jpgPath = join(tmpDir, 'gif2jpg.jpg');
        execFileSync('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '80', inputPath, '--out', jpgPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        if (statSync(jpgPath).size > 0) {
          finalPath = jpgPath;
          finalMime = 'image/jpeg';
          compressed = true;
          writeFileSync(inputPath, readFileSync(jpgPath));
        }
      }

      // 查询宽度
      const sipsOut = execFileSync('sips', ['-g', 'pixelWidth', finalPath], {
        encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'],
      });
      const m = sipsOut.match(/pixelWidth:\s*(\d+)/);
      const width = m ? parseInt(m[1], 10) : 0;

      // 宽度 > 1920 → 缩放
      if (width > RESIZE_WIDTH) {
        execFileSync('sips', ['--resampleWidth', String(RESIZE_WIDTH), finalPath, '--out', finalPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        compressed = true;
      }

      // 渐进式质量降低：80 → 60 → 40，直到 ≤ 512KB
      for (const quality of JPEG_QUALITIES) {
        if (statSync(finalPath).size <= MAX_FINAL_SIZE) break;
        const jpgPath = join(tmpDir, `q${quality}.jpg`);
        execFileSync('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', String(quality), finalPath, '--out', jpgPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        if (statSync(jpgPath).size > 0) {
          finalPath = jpgPath;
          finalMime = 'image/jpeg';
          compressed = true;
        }
      }
    } else {
      // ── Linux：使用 ImageMagick（convert 命令）───────────────────────

      // gif → 转静态 JPEG（取第一帧 [0]）
      if (mimeType === 'image/gif') {
        const jpgPath = join(tmpDir, 'gif2jpg.jpg');
        execFileSync('convert', [`${inputPath}[0]`, '-quality', '80', jpgPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        if (statSync(jpgPath).size > 0) {
          finalPath = jpgPath;
          finalMime = 'image/jpeg';
          compressed = true;
          writeFileSync(inputPath, readFileSync(jpgPath));
        }
      }

      // 查询宽度
      const identifyOut = execFileSync('identify', ['-format', '%w', finalPath], {
        encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'],
      });
      const width = parseInt(identifyOut.trim(), 10) || 0;

      // 宽度 > 1920 → 缩放
      if (width > RESIZE_WIDTH) {
        execFileSync('convert', [finalPath, '-resize', `${RESIZE_WIDTH}x`, finalPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        compressed = true;
      }

      // 渐进式质量降低：80 → 60 → 40，直到 ≤ 512KB
      for (const quality of JPEG_QUALITIES) {
        if (statSync(finalPath).size <= MAX_FINAL_SIZE) break;
        const jpgPath = join(tmpDir, `q${quality}.jpg`);
        execFileSync('convert', [finalPath, '-quality', String(quality), jpgPath], {
          stdio: ['pipe', 'pipe', 'pipe'],
        });
        if (statSync(jpgPath).size > 0) {
          finalPath = jpgPath;
          finalMime = 'image/jpeg';
          compressed = true;
        }
      }
    }
  } catch {
    // 工具不可用或压缩失败，使用原图
  }

  const finalBuf = readFileSync(finalPath);
  const skipped = finalBuf.length > MAX_FINAL_SIZE;
  return { buffer: finalBuf, mimeType: finalMime, compressed, skipped };
}

async function processImages(imageUrls, sourceUrl) {
  if (imageUrls.length === 0) {
    debug('🔍 图片处理完成 — 无图片需要处理');
    return [];
  }

  const urls = imageUrls.slice(0, MAX_IMAGES);
  const baseTmpDir = join(tmpdir(), `ynote-clip-${Date.now()}`);
  mkdirSync(baseTmpDir, { recursive: true });

  try {
    // Phase A: 并行下载
    const dlStart = Date.now();
    const downloaded = await pool(urls, CONCURRENT, async (url) => {
      const { buffer, contentType } = await downloadImage(url, sourceUrl);
      if (buffer.length > MAX_SIZE) throw new Error(`超过 10MB 限制 (${buffer.length} bytes)`);
      return { url, buffer, contentType };
    });
    const dlTime = ((Date.now() - dlStart) / 1000).toFixed(1);

    let dlOk = 0, dlFail = 0;
    for (const d of downloaded) { if (d.ok) dlOk++; else dlFail++; }
    debug(`🔍 下载完成 — 成功: ${dlOk}/${urls.length}, 失败: ${dlFail}, ⏱ ${dlTime}s`);

    // Phase B: 串行压缩 + base64（sips 需要文件 I/O）
    const procStart = Date.now();
    const images = [];
    let compressCount = 0, skipCount = 0;

    for (let i = 0; i < downloaded.length; i++) {
      const d = downloaded[i];
      if (!d.ok) {
        debug(`🔍 图片 [${i + 1}/${urls.length}] — url: ${d.input}, 状态: ❌ ${d.error}`);
        continue;
      }

      const { url, buffer, contentType } = d.value;
      const mimeType = guessMimeType(url, contentType);

      // 每张图片用独立子目录（避免 sips 文件冲突）
      const imgDir = join(baseTmpDir, `img_${i}`);
      mkdirSync(imgDir, { recursive: true });

      const origSize = buffer.length;
      const { buffer: finalBuf, mimeType: finalMime, compressed, skipped } = compressImage(buffer, mimeType, imgDir);
      if (skipped) {
        skipCount++;
        debug(`🔍 图片 [${i + 1}/${urls.length}] — url: ${url}, 原始: ${origSize}B, 压缩后: ${finalBuf.length}B, 状态: ⏭️ 超过 512KB 跳过`);
        continue;
      }
      if (compressed) compressCount++;

      const base64Data = finalBuf.toString('base64');
      images.push({ url, mimeType: finalMime, data: base64Data });

      const compressTag = compressed ? `, 压缩后: ${finalBuf.length}B` : '';
      debug(`🔍 图片 [${i + 1}/${urls.length}] — url: ${url}, 原始: ${origSize}B${compressTag}, mime: ${finalMime}, 状态: ✅`);
    }
    const procTime = ((Date.now() - procStart) / 1000).toFixed(1);
    debug(`🔍 图片处理完成 — 成功: ${images.length}, 跳过: ${skipCount}, 失败: ${dlFail}, 压缩: ${compressCount}, ⏱ ${procTime}s`);

    return images;
  } finally {
    rmSync(baseTmpDir, { recursive: true, force: true });
  }
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────

async function main() {
  // ── CLI 参数 ──
  const { values } = parseArgs({
    options: {
      title:        { type: 'string' },   // 模式 A 专用（向后兼容）
      'body-file':  { type: 'string' },
      'data-file':  { type: 'string' },
      'image-urls': { type: 'string', default: '[]' },
      'source-url': { type: 'string' },
      markdown:     { type: 'boolean', default: false },
    },
    strict: true,
  });

  if (!API_KEY) { console.error('错误：未设置 YNOTE_API_KEY 环境变量'); process.exit(1); }

  // ── 解析输入：data-file 模式 vs 分离参数模式 ──
  let title, bodyHtml, imageUrls, sourceUrl;

  if (values['data-file']) {
    // 模式 B：从 JSON 数据文件读取（browser CLI 输出管道到文件，绕过 agent context）
    const raw = readFileSync(values['data-file'], 'utf-8');
    const data = JSON.parse(raw);
    bodyHtml = data.content;
    imageUrls = data.imageUrls || [];
    sourceUrl = values['source-url'] || data.source || '';
    if (!data.title) { console.error('错误：data-file 中缺少 title'); process.exit(1); }
    if (!bodyHtml) { console.error('错误：data-file 中缺少 content'); process.exit(1); }
    // 内置 .clip 后缀：title 由脚本自动处理，无需通过命令行传递
    title = sanitizeTitle(data.title);
  } else {
    // 模式 A：分离参数（向后兼容）
    if (!values.title) { console.error('错误：缺少 --title'); process.exit(1); }
    if (!values['body-file']) { console.error('错误：缺少 --body-file'); process.exit(1); }
    if (!values['source-url']) { console.error('错误：缺少 --source-url'); process.exit(1); }
    title = values.title;
    bodyHtml = readFileSync(values['body-file'], 'utf-8');
    imageUrls = JSON.parse(values['image-urls']);
    sourceUrl = values['source-url'];
  }

  // ── Markdown → HTML 转换（fallback 路径）──
  if (values.markdown && bodyHtml) {
    debug(`🔍 Markdown → HTML 转换（marked），原文 ${bodyHtml.length} 字符`);
    bodyHtml = marked.parse(bodyHtml);
    debug(`🔍 转换完成，HTML ${bodyHtml.length} 字符`);
  }

  // ── Phase 1: 图片处理 ──
  const images = await processImages(imageUrls, sourceUrl);

  // ── Phase 2: MCP 连接 ──
  const client = new McpClient(SSE_URL, API_KEY, MCP_TIMEOUT_MS);
  try {
    await client.connect();
    await client.initialize();

    // ── Phase 3: clipperSaveWithImages ──
    const imgCount = images.length;
    debug(`🔍 MCP 请求 — tool: clipperSaveWithImages, title: "${title}", bodyHtml: ${bodyHtml.length} 字符, images: ${imgCount} 张`);

    const mcpStart = Date.now();
    let result = await client.callTool('clipperSaveWithImages', {
      title,
      bodyHtml,
      sourceUrl,
      images: JSON.stringify(images),   // MCP 协议要求 images 为 JSON 字符串
    });
    let mcpTime = ((Date.now() - mcpStart) / 1000).toFixed(1);

    // ── Phase 4: 降级判断 ──
    const fallbackPattern = /unknown tool|not found|not implemented|未知|不存在/i;
    if (result.isError && fallbackPattern.test(result.text)) {
      debug('🔍 clipperSaveWithImages 不可用，降级为 createNote');

      // createNote: images 去掉 data 字段（base64 太大）
      const imagesLite = images.map(({ url, mimeType }) => ({ url, mimeType }));
      const content = JSON.stringify({ bodyHtml, sourceUrl, images: imagesLite });

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
}

main().catch((err) => {
  console.error(`❌ ${err.message}`);
  process.exit(1);
});

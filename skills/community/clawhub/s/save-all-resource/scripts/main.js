import fs from 'fs';
import path from 'path';
import os from 'os';
import { URL } from 'url';
import puppeteer from 'puppeteer';

const entry = process.argv[2];

if (!entry) {
  console.error('Usage: node main.mjs <url>');
  process.exit(1);
}

const entryUrl = new URL(entry);
const origin = entryUrl.origin;
const domain = entryUrl.hostname.replace(/^www\./, '');
const outputDir = path.join(os.homedir(), 'Desktop', domain);

const savedResources = new Set();

const ALLOWED_PROTOCOLS = new Set(['http:', 'https:']);

function logInfo(...args) {
  console.log(...args);
}

function logError(...args) {
  console.error(...args);
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function sanitizeFilename(name) {
  return String(name).replace(/[<>:"\\|?*\x00-\x1F]/g, '_');
}

function getExtFromContentType(contentType = '') {
  const type = String(contentType).toLowerCase();

  if (type.includes('text/html')) return '.html';
  if (type.includes('text/css')) return '.css';
  if (type.includes('javascript') || type.includes('ecmascript')) return '.js';
  if (type.includes('application/json') || type.includes('text/json')) return '.json';
  if (type.includes('application/xml') || type.includes('text/xml')) return '.xml';
  if (type.includes('image/png')) return '.png';
  if (type.includes('image/jpeg')) return '.jpg';
  if (type.includes('image/gif')) return '.gif';
  if (type.includes('image/webp')) return '.webp';
  if (type.includes('image/svg+xml')) return '.svg';
  if (type.includes('image/x-icon')) return '.ico';
  if (type.includes('font/woff2')) return '.woff2';
  if (type.includes('font/woff')) return '.woff';
  if (type.includes('font/ttf')) return '.ttf';

  return '';
}

function isAllowedProtocol(urlObj) {
  return ALLOWED_PROTOCOLS.has(urlObj.protocol);
}

function shouldSaveUrl(urlStr) {
  try {
    const urlObj = new URL(urlStr);
    return isAllowedProtocol(urlObj) && urlObj.origin === origin;
  } catch {
    return false;
  }
}

function isTextLikeContent(contentType = '', resourceType = '') {
  const ct = String(contentType).toLowerCase();
  const rt = String(resourceType).toLowerCase();

  return (
    rt === 'document' ||
    rt === 'script' ||
    rt === 'stylesheet' ||
    rt === 'xhr' ||
    rt === 'fetch' ||
    ct.includes('text/') ||
    ct.includes('javascript') ||
    ct.includes('json') ||
    ct.includes('xml') ||
    ct.includes('svg')
  );
}

/**
 * URL -> 本地路径
 * 例子：
 *   https://site.com/                  -> index.html
 *   https://site.com/ai/login/         -> ai/login/index.html
 *   https://site.com/comments/123      -> comments/123.json
 */
function urlToLocalPath(urlStr, contentType = '') {
  const urlObj = new URL(urlStr);

  if (!isAllowedProtocol(urlObj)) {
    throw new Error(`Unsupported protocol: ${urlObj.protocol}`);
  }

  let pathname = decodeURIComponent(urlObj.pathname || '/');

  if (pathname === '/' || pathname === '') {
    pathname = '/index.html';
  } else if (pathname.endsWith('/')) {
    pathname += 'index.html';
  }

  // 某些站会把资源代理成 /https_/domain/xxx 或 /http_/domain/xxx
  pathname = pathname.replace(/^\/https?_\/[^/]+\//, '/');

  let ext = path.extname(pathname);
  if (!ext) {
    pathname += getExtFromContentType(contentType) || '.html';
  }

  return pathname
    .split('/')
    .map((segment) => sanitizeFilename(segment))
    .join('/')
    .replace(/^\/+/, '');
}

function writeTextFile(url, contentType, text) {
  const localPath = urlToLocalPath(url, contentType);
  const filePath = path.join(outputDir, localPath);

  ensureDir(filePath);
  fs.writeFileSync(filePath, text, 'utf8');

  logInfo('✔ text', localPath);
}

function writeBinaryFile(url, contentType, buffer) {
  const localPath = urlToLocalPath(url, contentType);
  const filePath = path.join(outputDir, localPath);

  ensureDir(filePath);
  fs.writeFileSync(filePath, buffer);

  logInfo('✔ bin ', localPath);
}

async function handleResponse(response) {
  const request = response.request();
  const method = request.method();
  const resourceType = request.resourceType();
  const responseUrl = response.url();
  const status = response.status();

  if (method !== 'GET') return;
  if (status < 200 || status >= 400) return;
  if (!shouldSaveUrl(responseUrl)) return;
  if (savedResources.has(responseUrl)) return;

  savedResources.add(responseUrl);

  const headers = response.headers();
  const contentType = headers['content-type'] || '';

  try {
    if (isTextLikeContent(contentType, resourceType)) {
      const text = await response.text();
      writeTextFile(responseUrl, contentType, text);
      return;
    }

    const buffer = await response.buffer();
    writeBinaryFile(responseUrl, contentType, buffer);
  } catch (err) {
    logError('✖ response save failed:', responseUrl, err.message);
  }
}

async function closeBrowserAndExit(browser, code = 0) {
  try {
    if (browser && browser.isConnected()) {
      await browser.close();
    }
  } catch {}
  process.exit(code);
}

async function main() {
  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: null,
  });

  const page = await browser.newPage({ 
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
  });

  page.on('close', async () => {
    logInfo('页签已关闭，脚本退出。');
    await closeBrowserAndExit(browser, 0);
  });

  page.on('response', (response) => {
    handleResponse(response).catch((err) => {
      logError('✖ unexpected response handler error:', err.message);
    });
  });
  
  logInfo('→ 打开入口页:', entry);

  await page.goto(entry, {
    waitUntil: 'domcontentloaded',
    timeout: 0,
  });

  logInfo('');
  logInfo('浏览器页签已打开。');
  logInfo('你现在可以手动切换页面，脚本会持续监听同域原始响应并实时落盘。');
  logInfo(`输出目录：${outputDir}`);
  logInfo('');
  logInfo('说明：');
  logInfo('- 只保存 http/https 同域响应');
  logInfo('- 自动跳过 blob: / data: / chrome-extension: 等特殊 URL');
  logInfo('- 主文档 HTML 使用 response.text()，更接近 DevTools 的原始响应');
  logInfo('- 用户关闭这个页签后，脚本自动退出');
  logInfo('');

  process.on('SIGINT', async () => {
    logInfo('\n收到退出信号，正在关闭浏览器...');
    await closeBrowserAndExit(browser, 0);
  });

  // 保持进程存活
  await new Promise(() => {});
}

main().catch((err) => {
  logError(err);
  process.exit(1);
});
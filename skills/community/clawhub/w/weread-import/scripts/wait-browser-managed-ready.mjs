#!/usr/bin/env node
import { extractCookieFromBrowser } from '../src/cookie.mjs';

function parseArgs(argv) {
  const args = { cdp: 'http://127.0.0.1:9222', timeoutMs: 8000, intervalMs: 1000 };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    const value = argv[i + 1];
    if (key === '--cdp' && value) {
      args.cdp = value;
      i += 1;
    } else if (key === '--timeout-ms' && value) {
      args.timeoutMs = Number(value) || args.timeoutMs;
      i += 1;
    } else if (key === '--interval-ms' && value) {
      args.intervalMs = Number(value) || args.intervalMs;
      i += 1;
    }
  }
  return args;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const RETRYABLE_MESSAGES = [
  '浏览器中未找到 weread.qq.com 的 cookie',
  '隔离浏览器中尚未登录微信读书',
  '浏览器中未找到',
];

function isRetryable(error) {
  const message = String(error?.message || error || '');
  return RETRYABLE_MESSAGES.some((pattern) => message.includes(pattern));
}

async function waitForManagedBrowserReady({ cdp, timeoutMs, intervalMs }) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      await extractCookieFromBrowser(cdp);
      console.error('微信读书登录态已就绪。');
      return;
    } catch (error) {
      if (!isRetryable(error)) {
        console.error(`微信读书登录态预热检查跳过：${String(error?.message || error)}`);
        return;
      }
      await sleep(intervalMs);
    }
  }
  console.error('微信读书登录态尚未就绪，继续尝试同步。');
}

await waitForManagedBrowserReady(parseArgs(process.argv));

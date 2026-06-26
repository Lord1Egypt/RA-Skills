import { chromium } from 'playwright';
import { isBrowserCookieMode, isManagedBrowserMode } from './browser-mode.mjs';

export const WEREAD_COOKIE_URLS = [
  'https://weread.qq.com/',
  'https://weread.qq.com/api/user/notebook',
  'https://weread.qq.com/web/book/bookmarklist?bookId=1',
  'https://weread.qq.com/web/review/list?bookId=1&listType=4&syncKey=0&mine=1',
];

export const CDP_CONNECT_OPTIONS = {
  acceptDownloads: 'internal-browser-default',
};

export function cookieMatchesHost(cookie, host = 'weread.qq.com') {
  const domain = String(cookie?.domain || '').replace(/^\./, '');
  return Boolean(domain) && (host === domain || host.endsWith(`.${domain}`));
}

export function buildCookieHeader(cookies, host = 'weread.qq.com') {
  return (cookies || [])
    .filter((cookie) => cookieMatchesHost(cookie, host) && cookie.name && cookie.value)
    .map((cookie) => `${cookie.name}=${cookie.value}`)
    .join('; ');
}

export function normalizeBrowserCookieError(error, { profileSyncMode = process.env.WEREAD_PROFILE_SYNC_MODE || 'isolated', cookieFrom = process.env.WEREAD_COOKIE_FROM || 'browser-managed' } = {}) {
  if (!isManagedBrowserMode(cookieFrom)) {
    return error;
  }
  const isolatedMode = profileSyncMode === 'isolated';
  if (isolatedMode && /未找到 weread\.qq\.com 的 cookie/.test(String(error?.message || ''))) {
    return new Error('隔离浏览器中尚未登录微信读书。请在自动打开的独立 Chrome 窗口中登录微信读书后再重试。');
  }
  return error;
}

async function closeBrowser(browser, primaryError) {
  if (!browser) return;
  try {
    if (typeof browser.close === 'function') {
      await browser.close();
    }
  } catch (closeError) {
    if (!primaryError) throw closeError;
  }
}

export async function extractCookieFromBrowserWithConnector(cdpUrl, connectOverCDP = chromium.connectOverCDP.bind(chromium)) {
  const browser = await connectOverCDP(cdpUrl, CDP_CONNECT_OPTIONS);
  let primaryError = null;
  try {
    const context = browser.contexts()[0];
    if (!context) throw new Error('无可用浏览器上下文，请确认已启动带远程调试的 Chrome');
    const cookieHeader = buildCookieHeader(await context.cookies(...WEREAD_COOKIE_URLS));
    if (!cookieHeader) throw new Error('浏览器中未找到 weread.qq.com 的 cookie，请先在该浏览器中登录微信读书');
    return cookieHeader;
  } catch (error) {
    primaryError = error;
    throw error;
  } finally {
    await closeBrowser(browser, primaryError);
  }
}

export async function extractCookieFromBrowser(cdpUrl) {
  return extractCookieFromBrowserWithConnector(cdpUrl);
}

export async function getCookieForApi(args) {
  if (args.cookie) return args.cookie;
  if (isBrowserCookieMode(args.cookieFrom)) {
    try {
      return extractCookieFromBrowser(args.cdp);
    } catch (error) {
      throw normalizeBrowserCookieError(error, { cookieFrom: args.cookieFrom });
    }
  }
  throw new Error('API 模式需要 cookie，请通过 --cookie、WEREAD_COOKIE 或 --cookie-from browser-live/browser-managed 提供');
}

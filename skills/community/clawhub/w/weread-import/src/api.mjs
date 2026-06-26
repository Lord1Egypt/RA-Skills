import { chromium } from 'playwright';
import { buildCookieHeader, CDP_CONNECT_OPTIONS, WEREAD_COOKIE_URLS } from './cookie.mjs';
import { cleanText } from './utils.mjs';
import { WereadApiError, WereadAuthError } from './errors.mjs';

const WEREAD_BASE = 'https://weread.qq.com';
const USER_AGENT = process.env.WEREAD_USER_AGENT || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36';

const AUTH_ERROR_CODES = [-1, -2, -100, -2010, -2012];

function appendCacheBuster(url) {
  const sep = url.includes('?') ? '&' : '?';
  return `${url}${sep}_=${Date.now()}`;
}

function extractBookIdFromUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.searchParams.get('bookId');
  } catch {
    return null;
  }
}

function parseWereadJsonResponse(url, status, text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new WereadApiError(`响应非合法 JSON: ${url}\n${text.slice(0, 500)}`);
  }
  if (status < 200 || status >= 300) {
    const code = data?.errcode ?? data?.errCode ?? data?.data?.errcode ?? data?.data?.errCode ?? 0;
    if (AUTH_ERROR_CODES.includes(Number(code)) || status === 401) {
      throw new WereadAuthError(`HTTP ${status} 错误: ${url}\n${text.slice(0, 500)}`);
    }
    throw new WereadApiError(`HTTP ${status} 错误: ${url}\n${text.slice(0, 500)}`);
  }
  const businessErrCode = data?.errCode ?? data?.errcode ?? 0;
  const businessErrMsg = data?.errMsg ?? data?.errmsg ?? '';
  if (businessErrCode && Number(businessErrCode) !== 0) {
    const isAuth = /login|auth|expire|token/i.test(businessErrMsg) || AUTH_ERROR_CODES.includes(Number(businessErrCode));
    const ErrClass = isAuth ? WereadAuthError : WereadApiError;
    throw new ErrClass(`业务错误 ${businessErrCode}: ${url}\n${businessErrMsg || text.slice(0, 500)}`);
  }
  return data;
}

export async function wereadFetchJson(url, cookie, { method = 'GET', body, extraHeaders = {} } = {}) {
  const finalUrl = method === 'GET' ? appendCacheBuster(url) : url;
  const headers = {
    'user-agent': USER_AGENT,
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    cookie,
    ...extraHeaders,
  };
  if (body) headers['content-type'] = 'application/json;charset=UTF-8';
  const res = await fetch(finalUrl, { method, headers, body });
  const text = await res.text();
  return parseWereadJsonResponse(url, res.status, text);
}

async function closeBrowserSession(browser, page, { closePage = true } = {}) {
  try {
    if (closePage && page && !page.isClosed()) await page.close();
  } catch {}
  try {
    if (!browser) return;
    if (typeof browser.close === 'function') await browser.close();
  } catch {}
}

export async function createWereadBrowserFetcher(cdpUrl, connectOverCDP = chromium.connectOverCDP.bind(chromium), options = {}) {
  if (typeof connectOverCDP === 'object' && connectOverCDP !== null) {
    options = connectOverCDP;
    connectOverCDP = chromium.connectOverCDP.bind(chromium);
  }
  const { reuseExistingPage = false, keepPageOnClose = false } = options;
  const browser = await connectOverCDP(cdpUrl, CDP_CONNECT_OPTIONS);
  const context = browser.contexts()[0];
  if (!context) {
    await closeBrowserSession(browser);
    throw new Error('无可用浏览器上下文，请确认已启动带远程调试的 Chrome');
  }

  const existingPage = reuseExistingPage
    ? context.pages().find((candidate) => typeof candidate?.isClosed !== 'function' || !candidate.isClosed())
    : null;
  const page = existingPage || await context.newPage();
  const ownsPage = !existingPage;
  if (ownsPage) {
    await page.goto(`${WEREAD_BASE}/`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  }
  let currentBookId = null;

  return {
    async getCookieHeader() {
      const cookieHeader = buildCookieHeader(await context.cookies(...WEREAD_COOKIE_URLS));
      if (!cookieHeader) throw new Error('浏览器中未找到 weread.qq.com 的 cookie，请先在该浏览器中登录微信读书');
      return cookieHeader;
    },
    async fetchJson(url, { method = 'GET', body, extraHeaders = {} } = {}) {
      const bookId = extractBookIdFromUrl(url);
      if (bookId && bookId !== currentBookId) {
        await page.goto(`${WEREAD_BASE}/web/reader/${encodeURIComponent(bookId)}`, {
          waitUntil: 'domcontentloaded',
          timeout: 60000,
        });
        currentBookId = bookId;
      }
      const finalUrl = method === 'GET' ? appendCacheBuster(url) : url;
      const headers = { ...extraHeaders };
      if (body && !headers['content-type']) headers['content-type'] = 'application/json;charset=UTF-8';
      const result = await page.evaluate(async ({ requestUrl, requestMethod, requestBody, requestHeaders }) => {
        const res = await fetch(requestUrl, {
          method: requestMethod,
          body: requestBody,
          headers: requestHeaders,
          credentials: 'include',
        });
        const text = await res.text();
        return { status: res.status, text };
      }, {
        requestUrl: finalUrl,
        requestMethod: method,
        requestBody: body ?? null,
        requestHeaders: headers,
      });
      return parseWereadJsonResponse(url, result.status, result.text);
    },
    async close(closeOptions = {}) {
      await closeBrowserSession(browser, page, {
        closePage: ownsPage && !(closeOptions.keepPage ?? keepPageOnClose),
      });
    },
  };
}

function normalizeBookshelfBooks(data) {
  return (data.books || []).map((item) => ({
    bookId: item.bookId || item.book?.bookId,
    title: item.book?.title || item.title,
    author: item.book?.author || item.author || '',
    sort: item.sort || 0,
    noteCount: item.noteCount || 0,
  })).filter((x) => x.bookId && x.title);
}

export async function getNotebookBooks(cookie) {
  return normalizeBookshelfBooks(await wereadFetchJson(`${WEREAD_BASE}/api/user/notebook`, cookie));
}

export async function getBookmarks(cookie, bookId, { fetchJson } = {}) {
  const loadJson = fetchJson || ((url, options) => wereadFetchJson(url, cookie, options));
  const data = await loadJson(`${WEREAD_BASE}/web/book/bookmarklist?bookId=${encodeURIComponent(bookId)}`);
  const chapters = Array.isArray(data.chapters) ? data.chapters : [];
  const chapterMap = new Map(chapters.map((item) => [
    String(item.chapterUid),
    {
      chapterName: cleanText(item.title || ''),
      chapterIdx: item.chapterIdx,
    },
  ]));
  const updated = Array.isArray(data.updated) ? data.updated : [];
  return updated.map((item) => ({
    ...item,
    chapterName: item.chapterName || item.chapterTitle || chapterMap.get(String(item.chapterUid))?.chapterName || '',
    chapterIdx: item.chapterIdx ?? chapterMap.get(String(item.chapterUid))?.chapterIdx ?? null,
  }));
}

export async function getReviews(cookie, bookId, { fetchJson } = {}) {
  const loadJson = fetchJson || ((url, options) => wereadFetchJson(url, cookie, options));
  const data = await loadJson(`${WEREAD_BASE}/web/review/list?bookId=${encodeURIComponent(bookId)}&listType=4&syncKey=0&mine=1`);
  return Array.isArray(data.reviews) ? data.reviews : [];
}

import {
  WereadApiError,
  WereadGatewayAuthError,
  WereadGatewayMissingKeyError,
  WereadGatewayUnavailableError,
  WereadGatewayUpgradeError,
} from './errors.mjs';

const GATEWAY_URL = 'https://i.weread.qq.com/api/agent/gateway';
const DEFAULT_GATEWAY_SKILL_VERSION = process.env.WEREAD_GATEWAY_SKILL_VERSION || '1.0.3';

function isUnsupportedApiError(code, message) {
  return /unsupported|unknown api|not found|not support|不存在|不支持|未找到/i.test(`${code} ${message}`);
}

function isAuthError(code, message) {
  return /auth|bearer|token|key|unauthor|forbidden|permission|鉴权|认证|权限|密钥|登录/i.test(`${code} ${message}`);
}

function normalizeBookItem(item) {
  const book = item.book || item.bookInfo || item;
  return {
    bookId: item.bookId || book.bookId,
    title: book.title || item.title,
    author: book.author || item.author || '',
    sort: item.sort || 0,
    noteCount: item.noteCount || 0,
    reviewCount: item.reviewCount || 0,
    bookmarkCount: item.bookmarkCount || 0,
  };
}

export function buildGatewayRequestBody(apiName, params = {}, skillVersion = DEFAULT_GATEWAY_SKILL_VERSION) {
  return {
    api_name: apiName,
    ...params,
    skill_version: skillVersion,
  };
}

export async function gatewayFetchJson(apiName, params = {}, options = {}) {
  const apiKey = options.apiKey || process.env.WEREAD_API_KEY || '';
  if (!apiKey) {
    throw new WereadGatewayMissingKeyError([
      '未配置 WEREAD_API_KEY，默认 Gateway 后端无法运行。',
      '请先设置：export WEREAD_API_KEY=<你的apikey>',
      '如果本次明确不使用官方 Gateway，可加 --no-gateway 走现有浏览器/Cookie 链路。',
    ].join('\n'));
  }

  const fetchImpl = options.fetchImpl || fetch;
  const skillVersion = options.skillVersion || DEFAULT_GATEWAY_SKILL_VERSION;
  const body = buildGatewayRequestBody(apiName, params, skillVersion);
  let res;
  try {
    res = await fetchImpl(GATEWAY_URL, {
      method: 'POST',
      headers: {
        authorization: `Bearer ${apiKey}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
    });
  } catch (error) {
    throw new WereadGatewayUnavailableError(`Gateway 网络不可用: ${error.message}`);
  }

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    if (res.status >= 500) throw new WereadGatewayUnavailableError(`Gateway HTTP ${res.status}: ${text.slice(0, 300)}`);
    throw new WereadApiError(`Gateway 响应非合法 JSON: ${text.slice(0, 300)}`);
  }

  if (data?.upgrade_info) {
    const message = data.upgrade_info.message || JSON.stringify(data.upgrade_info);
    throw new WereadGatewayUpgradeError(`官方 Gateway 要求升级 skill: ${message}`);
  }

  if (res.status === 401 || res.status === 403) {
    throw new WereadGatewayAuthError(`Gateway 鉴权失败，请检查 WEREAD_API_KEY: ${text.slice(0, 300)}`);
  }
  if (res.status >= 500) {
    throw new WereadGatewayUnavailableError(`Gateway HTTP ${res.status}: ${text.slice(0, 300)}`);
  }
  if (res.status < 200 || res.status >= 300) {
    throw new WereadApiError(`Gateway HTTP ${res.status}: ${text.slice(0, 300)}`);
  }

  const errcode = data.errcode ?? data.errCode ?? 0;
  const errmsg = data.errmsg ?? data.errMsg ?? data.message ?? '';
  if (Number(errcode) !== 0) {
    if (isUnsupportedApiError(errcode, errmsg)) {
      throw new WereadGatewayUnavailableError(`Gateway 接口不可用: ${errcode} ${errmsg}`);
    }
    if (isAuthError(errcode, errmsg)) {
      throw new WereadGatewayAuthError(`Gateway 鉴权失败，请检查 WEREAD_API_KEY: ${errcode} ${errmsg}`);
    }
    throw new WereadApiError(`Gateway 业务错误 ${errcode}: ${errmsg || text.slice(0, 300)}`);
  }

  return data.data ?? data;
}

export async function getGatewayNotebookBooks(options = {}) {
  const books = [];
  let lastSort = null;
  for (;;) {
    const params = { count: options.count || 100 };
    if (lastSort) params.lastSort = lastSort;
    const data = await gatewayFetchJson('/user/notebooks', params, options);
    const pageBooks = Array.isArray(data.books) ? data.books : [];
    books.push(...pageBooks.map(normalizeBookItem).filter((book) => book.bookId && book.title));
    if (!data.hasMore || !pageBooks.length) break;
    lastSort = pageBooks[pageBooks.length - 1]?.sort;
    if (!lastSort) break;
  }
  return books;
}

export async function getGatewayBookmarks(bookId, options = {}) {
  const data = await gatewayFetchJson('/book/bookmarklist', { bookId }, options);
  const chapters = Array.isArray(data.chapters) ? data.chapters : [];
  const chapterMap = new Map(chapters.map((item) => [
    String(item.chapterUid),
    {
      chapterName: item.title || '',
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

export async function getGatewayReviews(bookId, options = {}) {
  const reviews = [];
  let synckey = 0;
  for (;;) {
    const data = await gatewayFetchJson('/review/list/mine', {
      bookid: bookId,
      count: options.count || 100,
      synckey,
    }, options);
    const pageReviews = Array.isArray(data.reviews) ? data.reviews : [];
    reviews.push(...pageReviews);
    if (!data.hasMore || !pageReviews.length) break;
    const nextSynckey = data.synckey ?? data.syncKey;
    if (!nextSynckey || nextSynckey === synckey) break;
    synckey = nextSynckey;
  }
  return reviews;
}

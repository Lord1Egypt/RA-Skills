import { createWereadBrowserFetcher } from './api.mjs';
import { getCookieForApi, extractCookieFromBrowser } from './cookie.mjs';
import { WereadAuthError } from './errors.mjs';
import { isBrowserCookieMode, isManagedBrowserMode, isLiveBrowserMode } from './browser-mode.mjs';

const WEREAD_BASE = 'https://weread.qq.com';

function browserAuthFailureMessage(cookieFrom) {
  if (isLiveBrowserMode(cookieFrom)) {
    return '已连接的外部 Chrome 中微信读书尚未登录或登录已过期。请在该 Chrome 中登录微信读书后再重试。';
  }
  const isolatedMode = (process.env.WEREAD_PROFILE_SYNC_MODE || 'isolated') === 'isolated';
  if (isolatedMode) {
    return '隔离浏览器窗口中的微信读书尚未登录或登录已过期。请在自动打开的独立 Chrome 窗口中登录微信读书后再重试。';
  }
  return '浏览器中的微信读书登录已过期，请在 Chrome 中重新登录后重试';
}

export async function createApiSessionManager(args, deps = {}) {
  const getCookie = deps.getCookieForApi || getCookieForApi;
  const refreshCookie = deps.extractCookieFromBrowser || extractCookieFromBrowser;
  const createBrowserFetcher = deps.createWereadBrowserFetcher || createWereadBrowserFetcher;
  const managedBrowser = isManagedBrowserMode(args.cookieFrom);

  async function openBrowserFetcher() {
    return createBrowserFetcher(args.cdp, undefined, {
      reuseExistingPage: managedBrowser,
      keepPageOnClose: managedBrowser,
    });
  }

  let cookie = null;
  let browserFetcher = null;
  let state = 'idle';
  let invalidReason = null;
  let basicValidated = false;
  let detailReady = false;
  let detailBookId = null;

  async function closeFetcher() {
    if (!browserFetcher) return;
    const current = browserFetcher;
    browserFetcher = null;
    await current.close?.();
  }

  function resetValidation() {
    basicValidated = false;
    detailReady = false;
    detailBookId = null;
  }

  async function buildReadySession(nextCookie, nextBrowserFetcher = null) {
    cookie = nextCookie;
    resetValidation();
    browserFetcher = nextBrowserFetcher;
    state = 'ready';
    invalidReason = null;
    return getSnapshot();
  }

  function getSnapshot() {
    return {
      cookie,
      detailFetchJson: browserFetcher?.fetchJson.bind(browserFetcher),
      state,
      invalidReason,
      validation: {
        basicValidated,
        detailReady,
        detailBookId,
      },
    };
  }

  return {
    getState() {
      return state;
    },
    getSnapshot,
    invalidate(reason = 'unknown') {
      state = 'invalid';
      invalidReason = reason;
      resetValidation();
    },
    markBasicValidated() {
      basicValidated = true;
      invalidReason = null;
      if (state === 'validating_basic') state = 'ready';
      return getSnapshot();
    },
    async ensureDetailReady(bookId) {
      if (!bookId) return getSnapshot();
      if (detailReady && detailBookId === String(bookId)) return getSnapshot();
      if (!isBrowserCookieMode(args.cookieFrom)) {
        detailReady = true;
        detailBookId = String(bookId);
        return getSnapshot();
      }
      if (!browserFetcher || typeof browserFetcher.fetchJson !== 'function') {
        throw new Error('浏览器详情请求器不可用');
      }
      state = 'validating_detail';
      await browserFetcher.fetchJson(`${WEREAD_BASE}/web/book/bookmarklist?bookId=${encodeURIComponent(bookId)}`);
      state = 'ready';
      detailReady = true;
      detailBookId = String(bookId);
      invalidReason = null;
      return getSnapshot();
    },
    async acquire() {
      if (state === 'ready' && cookie) return getSnapshot();
      await closeFetcher();
      state = 'acquiring';
      if (isBrowserCookieMode(args.cookieFrom)) {
        const nextBrowserFetcher = await openBrowserFetcher();
        try {
          const nextCookie = typeof nextBrowserFetcher.getCookieHeader === 'function'
            ? await nextBrowserFetcher.getCookieHeader()
            : await getCookie(args);
          return buildReadySession(nextCookie, nextBrowserFetcher);
        } catch (error) {
          await nextBrowserFetcher.close?.();
          throw error;
        }
      }
      const nextCookie = await getCookie(args);
      return buildReadySession(nextCookie);
    },
    async refresh() {
      if (!isBrowserCookieMode(args.cookieFrom)) {
        throw new Error('仅浏览器模式支持刷新 session');
      }
      await closeFetcher();
      state = 'refreshing';
      const nextBrowserFetcher = await openBrowserFetcher();
      try {
        const nextCookie = typeof nextBrowserFetcher.getCookieHeader === 'function'
          ? await nextBrowserFetcher.getCookieHeader()
          : await refreshCookie(args.cdp);
        return buildReadySession(nextCookie, nextBrowserFetcher);
      } catch (error) {
        await nextBrowserFetcher.close?.();
        throw error;
      }
    },
    async close() {
      state = 'closed';
      invalidReason = null;
      resetValidation();
      await closeFetcher();
    },
  };
}

export async function runWithApiSessionRetry(args, run, deps = {}) {
  const warn = deps.warn || console.warn;
  const sessionManager = await createApiSessionManager(args, deps);
  try {
    const session = await sessionManager.acquire();
    return await run(session, sessionManager);
  } catch (err) {
    if (err instanceof WereadAuthError && isBrowserCookieMode(args.cookieFrom)) {
      const snapshot = sessionManager.getSnapshot();
      const reason = snapshot.validation?.basicValidated ? 'detail_auth_error' : 'basic_auth_error';
      sessionManager.invalidate(reason);
      warn('[warn] API cookie 已过期，需要浏览器中的微信读书会话恢复后再重试。');
      throw new Error(browserAuthFailureMessage(args.cookieFrom));
    }
    if (err instanceof WereadAuthError) {
      throw new Error('cookie 已过期，请更新 WEREAD_COOKIE 或使用 --cookie-from browser');
    }
    throw err;
  } finally {
    await sessionManager.close();
  }
}

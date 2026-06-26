import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { WereadAuthError } from '../src/errors.mjs';
import { createApiSessionManager, runWithApiSessionRetry } from '../src/session.mjs';

describe('createApiSessionManager', () => {
  it('acquires and closes a browser-backed session', async () => {
    const calls = [];
    const manager = await createApiSessionManager(
      { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
      {
        async createWereadBrowserFetcher(cdpUrl) {
          calls.push(`fetcher:${cdpUrl}`);
          return {
            async getCookieHeader() {
              calls.push('getCookieHeader');
              return 'cookie-1';
            },
            fetchJson() {},
            async close() {
              calls.push('closeFetcher');
            },
          };
        },
      },
    );

    const session = await manager.acquire();
    assert.equal(session.cookie, 'cookie-1');
    assert.equal(typeof session.detailFetchJson, 'function');
    assert.equal(manager.getState(), 'ready');
    assert.deepEqual(session.validation, {
      basicValidated: false,
      detailReady: false,
      detailBookId: null,
    });

    await manager.close();
    assert.deepEqual(calls, ['fetcher:http://127.0.0.1:9222', 'getCookieHeader', 'closeFetcher']);
    assert.equal(manager.getState(), 'closed');
  });

  it('refreshes a browser-backed session and closes the previous fetcher', async () => {
    const calls = [];
    let fetcherIndex = 0;
    const manager = await createApiSessionManager(
      { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
      {
        async createWereadBrowserFetcher() {
          fetcherIndex += 1;
          const label = `fetcher-${fetcherIndex}`;
          calls.push(label);
          return {
            async getCookieHeader() {
              calls.push(`cookie:${label}`);
              return label === 'fetcher-1' ? 'cookie-1' : 'cookie-2';
            },
            fetchJson() {},
            async close() {
              calls.push(`close:${label}`);
            },
          };
        },
      },
    );

    await manager.acquire();
    const refreshed = await manager.refresh();
    assert.equal(refreshed.cookie, 'cookie-2');
    assert.equal(manager.getState(), 'ready');
    await manager.close();

    assert.deepEqual(calls, [
      'fetcher-1',
      'cookie:fetcher-1',
      'close:fetcher-1',
      'fetcher-2',
      'cookie:fetcher-2',
      'close:fetcher-2',
    ]);
  });

  it('tracks basic validation and browser detail readiness separately', async () => {
    const calls = [];
    const manager = await createApiSessionManager(
      { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
      {
        async getCookieForApi() {
          return 'cookie-1';
        },
        async createWereadBrowserFetcher() {
          return {
            async fetchJson(url) {
              calls.push(url);
              return { updated: [] };
            },
            async close() {},
          };
        },
      },
    );

    await manager.acquire();
    const basicReady = manager.markBasicValidated();
    assert.deepEqual(basicReady.validation, {
      basicValidated: true,
      detailReady: false,
      detailBookId: null,
    });

    const detailReady = await manager.ensureDetailReady('33628204');
    assert.deepEqual(detailReady.validation, {
      basicValidated: true,
      detailReady: true,
      detailBookId: '33628204',
    });

    await manager.ensureDetailReady('33628204');
    assert.deepEqual(calls, ['https://weread.qq.com/web/book/bookmarklist?bookId=33628204']);
    await manager.close();
  });

  it('marks detail readiness for manual sessions without a browser fetcher', async () => {
    const manager = await createApiSessionManager(
      { cookieFrom: 'manual', cookie: 'manual-cookie' },
      {
        async getCookieForApi(args) {
          return args.cookie;
        },
      },
    );

    await manager.acquire();
    manager.markBasicValidated();
    const detailReady = await manager.ensureDetailReady('33628204');
    assert.deepEqual(detailReady.validation, {
      basicValidated: true,
      detailReady: true,
      detailBookId: '33628204',
    });
    await manager.close();
  });
});

describe('runWithApiSessionRetry', () => {
  it('surfaces a browser login message after browser auth failure without retrying immediately', async () => {
    const warnings = [];
    const calls = [];
    await assert.rejects(
      runWithApiSessionRetry(
        { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
        async (session) => {
          calls.push(`run:${session.cookie}`);
          throw new WereadAuthError('expired');
        },
        {
          warn(message) {
            warnings.push(message);
          },
          async createWereadBrowserFetcher() {
            calls.push('fetcher-1');
            return {
              async getCookieHeader() {
                calls.push('cookie:fetcher-1');
                return 'cookie-1';
              },
              fetchJson() {},
              async close() {
                calls.push('close:fetcher-1');
              },
            };
          },
        },
      ),
      /隔离浏览器窗口中的微信读书尚未登录或登录已过期/,
    );
    assert.deepEqual(warnings, ['[warn] API cookie 已过期，需要浏览器中的微信读书会话恢复后再重试。']);
    assert.deepEqual(calls, [
      'fetcher-1',
      'cookie:fetcher-1',
      'run:cookie-1',
      'close:fetcher-1',
    ]);
  });

  it('converts repeated browser auth failures into a user-facing login message', async () => {
    const previousMode = process.env.WEREAD_PROFILE_SYNC_MODE;
    process.env.WEREAD_PROFILE_SYNC_MODE = 'isolated';
    try {
      await assert.rejects(
        runWithApiSessionRetry(
          { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
          async () => {
            throw new WereadAuthError('expired');
          },
          {
            warn() {},
            async getCookieForApi() {
              return 'cookie-1';
            },
            async createWereadBrowserFetcher() {
              return {
                async getCookieHeader() {
                  return 'cookie-1';
                },
                fetchJson() {},
                async close() {},
              };
            },
          },
        ),
        /隔离浏览器窗口中的微信读书尚未登录或登录已过期/,
      );
    } finally {
      if (previousMode === undefined) delete process.env.WEREAD_PROFILE_SYNC_MODE;
      else process.env.WEREAD_PROFILE_SYNC_MODE = previousMode;
    }
  });

  it('preserves the legacy browser-auth message in legacy sync mode', async () => {
    const previousMode = process.env.WEREAD_PROFILE_SYNC_MODE;
    process.env.WEREAD_PROFILE_SYNC_MODE = 'legacy';
    try {
      await assert.rejects(
        runWithApiSessionRetry(
          { cookieFrom: 'browser', cdp: 'http://127.0.0.1:9222' },
          async () => {
            throw new WereadAuthError('expired');
          },
          {
            warn() {},
            async getCookieForApi() {
              return 'cookie-1';
            },
            async createWereadBrowserFetcher() {
              return {
                async getCookieHeader() {
                  return 'cookie-1';
                },
                fetchJson() {},
                async close() {},
              };
            },
          },
        ),
        /浏览器中的微信读书登录已过期/,
      );
    } finally {
      if (previousMode === undefined) delete process.env.WEREAD_PROFILE_SYNC_MODE;
      else process.env.WEREAD_PROFILE_SYNC_MODE = previousMode;
    }
  });

  it('uses an external-chrome message in browser-live mode', async () => {
    await assert.rejects(
      runWithApiSessionRetry(
        { cookieFrom: 'browser-live', cdp: 'http://127.0.0.1:9222' },
          async () => {
            throw new WereadAuthError('expired');
          },
          {
            warn() {},
            async getCookieForApi() {
              return 'cookie-1';
            },
            async createWereadBrowserFetcher() {
              return {
                async getCookieHeader() {
                  return 'cookie-1';
                },
                fetchJson() {},
                async close() {},
              };
          },
        },
      ),
      /已连接的外部 Chrome 中微信读书尚未登录或登录已过期/,
    );
  });

  it('converts manual auth failures into a cookie-expired message', async () => {
    await assert.rejects(
      runWithApiSessionRetry(
        { cookieFrom: 'manual', cookie: 'manual-cookie' },
        async () => {
          throw new WereadAuthError('expired');
        },
        {
          async getCookieForApi(args) {
            return args.cookie;
          },
        },
      ),
      /cookie 已过期，请更新 WEREAD_COOKIE 或使用 --cookie-from browser/,
    );
  });
});

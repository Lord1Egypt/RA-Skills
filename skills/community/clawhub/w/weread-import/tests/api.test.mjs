import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { WereadAuthError } from '../src/errors.mjs';
import { createWereadBrowserFetcher, getBookmarks, getReviews } from '../src/api.mjs';
import { CDP_CONNECT_OPTIONS } from '../src/cookie.mjs';

describe('getBookmarks', () => {
  it('supports injected browser fetchers for detail APIs', async () => {
    const calls = [];
    const bookmarks = await getBookmarks('cookie', '33628204', {
      async fetchJson(url) {
        calls.push(url);
        return {
          chapters: [{ chapterUid: 51, title: '第一章', chapterIdx: 2 }],
          updated: [{ bookmarkId: 'id-1', chapterUid: 51 }],
        };
      },
    });

    assert.deepEqual(calls, ['https://weread.qq.com/web/book/bookmarklist?bookId=33628204']);
    assert.deepEqual(bookmarks, [{
      bookmarkId: 'id-1',
      chapterUid: 51,
      chapterName: '第一章',
      chapterIdx: 2,
    }]);
  });
});

describe('getReviews', () => {
  it('supports injected browser fetchers for detail APIs', async () => {
    const calls = [];
    const reviews = await getReviews('cookie', '33628204', {
      async fetchJson(url) {
        calls.push(url);
        return { reviews: [{ reviewId: 'r-1' }] };
      },
    });

    assert.deepEqual(calls, ['https://weread.qq.com/web/review/list?bookId=33628204&listType=4&syncKey=0&mine=1']);
    assert.deepEqual(reviews, [{ reviewId: 'r-1' }]);
  });
});

describe('createWereadBrowserFetcher', () => {
  it('reuses one browser page and only enters the reader context once per book', async () => {
    const calls = [];
    const page = {
      async goto(url, options) {
        calls.push(['goto', url, options.waitUntil]);
      },
      async evaluate(_fn, payload) {
        calls.push(['evaluate', payload.requestUrl, payload.requestMethod]);
        return {
          status: 200,
          text: JSON.stringify({ ok: payload.requestUrl }),
        };
      },
      isClosed() {
        return false;
      },
      async close() {
        calls.push(['page.close']);
      },
    };
    const browser = {
      contexts() {
        return [{ async newPage() { calls.push(['newPage']); return page; } }];
      },
      async close() {
        calls.push(['browser.close']);
      },
    };

    const fetcher = await createWereadBrowserFetcher('http://127.0.0.1:9222', async (cdpUrl, options) => {
      calls.push(['connect', cdpUrl]);
      calls.push(['connectOptions', options]);
      return browser;
    });

    const first = await fetcher.fetchJson('https://weread.qq.com/web/book/bookmarklist?bookId=1');
    const second = await fetcher.fetchJson('https://weread.qq.com/web/review/list?bookId=1&listType=4&syncKey=0&mine=1');
    await fetcher.close();

    assert.match(first.ok, /^https:\/\/weread\.qq\.com\/web\/book\/bookmarklist\?bookId=1&_=\d+$/);
    assert.match(second.ok, /^https:\/\/weread\.qq\.com\/web\/review\/list\?bookId=1&listType=4&syncKey=0&mine=1&_=\d+$/);
    assert.deepEqual(calls.slice(0, 3), [
      ['connect', 'http://127.0.0.1:9222'],
      ['connectOptions', CDP_CONNECT_OPTIONS],
      ['newPage'],
    ]);
    assert.deepEqual(calls[3], ['goto', 'https://weread.qq.com/', 'domcontentloaded']);
    assert.deepEqual(calls[4], ['goto', 'https://weread.qq.com/web/reader/1', 'domcontentloaded']);
    assert.equal(calls[5][0], 'evaluate');
    assert.match(calls[5][1], /^https:\/\/weread\.qq\.com\/web\/book\/bookmarklist\?bookId=1&_=\d+$/);
    assert.equal(calls[5][2], 'GET');
    assert.equal(calls[6][0], 'evaluate');
    assert.match(calls[6][1], /^https:\/\/weread\.qq\.com\/web\/review\/list\?bookId=1&listType=4&syncKey=0&mine=1&_=\d+$/);
    assert.equal(calls[6][2], 'GET');
    assert.deepEqual(calls.slice(7), [
      ['page.close'],
      ['browser.close'],
    ]);
  });

  it('maps browser-side auth failures to WereadAuthError', async () => {
    let evaluateCalls = 0;
    const page = {
      async goto() {},
      async evaluate() {
        evaluateCalls += 1;
        return {
          status: 200,
          text: JSON.stringify({ errCode: -2012, errMsg: '登录超时' }),
        };
      },
      isClosed() {
        return false;
      },
      async close() {},
    };
    const browser = {
      contexts() {
        return [{ async newPage() { return page; } }];
      },
      async close() {},
    };

    const fetcher = await createWereadBrowserFetcher('http://127.0.0.1:9222', async () => browser);

    await assert.rejects(
      fetcher.fetchJson('https://weread.qq.com/web/book/bookmarklist?bookId=1'),
      WereadAuthError,
    );
    assert.equal(evaluateCalls, 1);
    await fetcher.close();
  });
});

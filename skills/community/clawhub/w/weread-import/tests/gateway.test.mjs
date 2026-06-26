import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  buildGatewayRequestBody,
  gatewayFetchJson,
  getGatewayNotebookBooks,
} from '../src/gateway.mjs';
import {
  WereadGatewayAuthError,
  WereadGatewayMissingKeyError,
  WereadGatewayUnavailableError,
  WereadGatewayUpgradeError,
} from '../src/errors.mjs';

function jsonResponse(data, status = 200) {
  return {
    status,
    async text() {
      return JSON.stringify(data);
    },
  };
}

describe('buildGatewayRequestBody', () => {
  it('flattens business params at the top level', () => {
    assert.deepEqual(
      buildGatewayRequestBody('/user/notebooks', { count: 100, lastSort: 123 }, '1.0.3'),
      {
        api_name: '/user/notebooks',
        count: 100,
        lastSort: 123,
        skill_version: '1.0.3',
      },
    );
  });
});

describe('gatewayFetchJson', () => {
  it('requires WEREAD_API_KEY', async () => {
    await assert.rejects(
      gatewayFetchJson('/user/notebooks', {}, { apiKey: '' }),
      WereadGatewayMissingKeyError,
    );
  });

  it('sends the gateway authorization header and JSON body', async () => {
    const calls = [];
    const result = await gatewayFetchJson('/book/bookmarklist', { bookId: '1' }, {
      apiKey: 'wrk-test',
      skillVersion: '1.0.3',
      async fetchImpl(url, options) {
        calls.push({ url, options });
        return jsonResponse({ errcode: 0, data: { updated: [] } });
      },
    });

    assert.deepEqual(result, { updated: [] });
    assert.equal(calls[0].url, 'https://i.weread.qq.com/api/agent/gateway');
    assert.equal(calls[0].options.headers.authorization, 'Bearer wrk-test');
    assert.deepEqual(JSON.parse(calls[0].options.body), {
      api_name: '/book/bookmarklist',
      bookId: '1',
      skill_version: '1.0.3',
    });
  });

  it('classifies auth failures as non-fallback errors', async () => {
    await assert.rejects(
      gatewayFetchJson('/user/notebooks', {}, {
        apiKey: 'bad',
        async fetchImpl() {
          return jsonResponse({ errcode: 401, errmsg: 'unauthorized' }, 401);
        },
      }),
      WereadGatewayAuthError,
    );
  });

  it('classifies upgrade_info as a non-fallback error', async () => {
    await assert.rejects(
      gatewayFetchJson('/user/notebooks', {}, {
        apiKey: 'wrk-test',
        async fetchImpl() {
          return jsonResponse({ upgrade_info: { message: 'please upgrade' } });
        },
      }),
      WereadGatewayUpgradeError,
    );
  });

  it('classifies unsupported APIs as fallback-eligible', async () => {
    await assert.rejects(
      gatewayFetchJson('/user/notebooks', {}, {
        apiKey: 'wrk-test',
        async fetchImpl() {
          return jsonResponse({ errcode: 4004, errmsg: 'api not supported' });
        },
      }),
      WereadGatewayUnavailableError,
    );
  });
});

describe('getGatewayNotebookBooks', () => {
  it('paginates by hasMore and the last book sort value', async () => {
    const bodies = [];
    const books = await getGatewayNotebookBooks({
      apiKey: 'wrk-test',
      skillVersion: '1.0.3',
      async fetchImpl(_url, options) {
        const body = JSON.parse(options.body);
        bodies.push(body);
        if (bodies.length === 1) {
          return jsonResponse({
            errcode: 0,
            data: {
              hasMore: 1,
              books: [
                { bookId: '1', book: { title: '第一本', author: '作者 A' }, sort: 20, noteCount: 2 },
                { bookId: '2', book: { title: '第二本', author: '作者 B' }, sort: 10, reviewCount: 1 },
              ],
            },
          });
        }
        return jsonResponse({
          errcode: 0,
          data: {
            hasMore: 0,
            books: [
              { bookId: '3', book: { title: '第三本', author: '作者 C' }, sort: 5, bookmarkCount: 1 },
            ],
          },
        });
      },
    });

    assert.deepEqual(bodies, [
      { api_name: '/user/notebooks', count: 100, skill_version: '1.0.3' },
      { api_name: '/user/notebooks', count: 100, lastSort: 10, skill_version: '1.0.3' },
    ]);
    assert.deepEqual(books, [
      { bookId: '1', title: '第一本', author: '作者 A', sort: 20, noteCount: 2, reviewCount: 0, bookmarkCount: 0 },
      { bookId: '2', title: '第二本', author: '作者 B', sort: 10, noteCount: 0, reviewCount: 1, bookmarkCount: 0 },
      { bookId: '3', title: '第三本', author: '作者 C', sort: 5, noteCount: 0, reviewCount: 0, bookmarkCount: 1 },
    ]);
  });
});

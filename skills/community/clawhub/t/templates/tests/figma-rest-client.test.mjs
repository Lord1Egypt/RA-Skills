import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { createFigmaRestClient } from '../scripts/lib/figma-rest-client.mjs';

function jsonResponse(body, init = {}) {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers ?? {}),
    },
  });
}

function binaryResponse(bytes, init = {}) {
  return new Response(bytes, {
    status: init.status ?? 200,
    headers: init.headers ?? {},
  });
}

function makeTokenProvider(tokens = ['token-1']) {
  const calls = [];
  return {
    calls,
    async withTokenRetry(operation) {
      calls.push(tokens[0]);
      const first = await operation({ accessToken: tokens[0], tokenType: 'Bearer' });
      if (first?.status === 401 && tokens[1]) {
        calls.push(tokens[1]);
        const second = await operation({ accessToken: tokens[1], tokenType: 'Bearer' });
        return second;
      }
      return first;
    },
  };
}

function makeClient(fetchImpl, options = {}) {
  return createFigmaRestClient({
    apiBaseUrl: 'https://api.test.figma.local',
    fetchImpl,
    tokenProvider: options.tokenProvider ?? makeTokenProvider(),
    retryDelayMs: 0,
    sleep: async () => {},
    imageFetchImpl: options.imageFetchImpl,
  });
}

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-rest-test-'));
}

describe('createFigmaRestClient', () => {
  it('reads /v1/me with an Authorization bearer token', async () => {
    const requests = [];
    const client = makeClient(async (url, init) => {
      requests.push({ url: new URL(url), init });
      return jsonResponse({ id: 'user-1', email: 'designer@example.com' });
    });

    const me = await client.getMe();

    assert.equal(me.email, 'designer@example.com');
    assert.equal(requests[0].url.pathname, '/v1/me');
    assert.equal(requests[0].init.headers.Authorization, 'Bearer token-1');
  });

  it('reads a target node and records the Figma file version', async () => {
    const client = makeClient(async (url) => {
      const parsed = new URL(url);
      assert.equal(parsed.pathname, '/v1/files/fileKey123/nodes');
      assert.equal(parsed.searchParams.get('ids'), '1:2');
      return jsonResponse({
        version: '123456',
        nodes: {
          '1:2': {
            document: { id: '1:2', name: 'Target', type: 'FRAME' },
          },
        },
      });
    });

    const node = await client.getNode({ fileKey: 'fileKey123', nodeId: '1:2' });

    assert.equal(node.fileVersion, '123456');
    assert.equal(node.document.name, 'Target');
  });

  it('treats HTTP 200 with a null node as a read failure', async () => {
    const client = makeClient(async () =>
      jsonResponse({
        version: '123456',
        nodes: {
          '1:2': null,
        },
      }),
    );

    await assert.rejects(client.getNode({ fileKey: 'fileKey123', nodeId: '1:2' }), {
      code: 'figma_node_not_found',
    });
  });

  it('refreshes once after a 401 and retries the original request once', async () => {
    const tokenProvider = makeTokenProvider(['expired-token', 'fresh-token']);
    const authorizations = [];
    const client = makeClient(
      async (_url, init) => {
        authorizations.push(init.headers.Authorization);
        if (authorizations.length === 1) {
          return jsonResponse({ err: 'expired' }, { status: 401 });
        }
        return jsonResponse({ id: 'user-1' });
      },
      { tokenProvider },
    );

    const me = await client.getMe();

    assert.equal(me.id, 'user-1');
    assert.deepEqual(authorizations, ['Bearer expired-token', 'Bearer fresh-token']);
    assert.deepEqual(tokenProvider.calls, ['expired-token', 'fresh-token']);
  });

  it('does not refresh for 403 or 404 responses', async () => {
    const forbiddenProvider = makeTokenProvider(['token-1', 'token-2']);
    const forbiddenClient = makeClient(async () => jsonResponse({ err: 'forbidden' }, { status: 403 }), {
      tokenProvider: forbiddenProvider,
    });
    await assert.rejects(forbiddenClient.getMe(), { code: 'figma_api_forbidden' });
    assert.deepEqual(forbiddenProvider.calls, ['token-1']);

    const notFoundProvider = makeTokenProvider(['token-1', 'token-2']);
    const notFoundClient = makeClient(async () => jsonResponse({ err: 'not found' }, { status: 404 }), {
      tokenProvider: notFoundProvider,
    });
    await assert.rejects(notFoundClient.getNode({ fileKey: 'fileKey123', nodeId: '1:2' }), {
      code: 'figma_api_not_found',
    });
    assert.deepEqual(notFoundProvider.calls, ['token-1']);
  });

  it('honors Retry-After for 429 with bounded retry', async () => {
    let calls = 0;
    const retryAfterValues = [];
    const client = createFigmaRestClient({
      apiBaseUrl: 'https://api.test.figma.local',
      tokenProvider: makeTokenProvider(),
      fetchImpl: async () => {
        calls += 1;
        if (calls === 1) {
          return jsonResponse({ err: 'rate limited' }, { status: 429, headers: { 'Retry-After': '2' } });
        }
        return jsonResponse({ id: 'user-1' });
      },
      retryDelayMs: 0,
      sleep: async (ms) => {
        retryAfterValues.push(ms);
      },
    });

    const me = await client.getMe();

    assert.equal(me.id, 'user-1');
    assert.equal(calls, 2);
    assert.deepEqual(retryAfterValues, [2000]);
  });

  it('retries finite 5xx and network failures', async () => {
    let calls = 0;
    const client = makeClient(async () => {
      calls += 1;
      if (calls === 1) {
        throw new Error('temporary network failure');
      }
      if (calls === 2) {
        return jsonResponse({ err: 'server error' }, { status: 503 });
      }
      return jsonResponse({ id: 'user-1' });
    });

    const me = await client.getMe();

    assert.equal(me.id, 'user-1');
    assert.equal(calls, 3);
  });

  it('exports an image through the Figma Images API and downloads only the returned https URL', async () => {
    const tempDir = await makeTempDir();
    const outPath = path.join(tempDir, 'target.png');
    const imageBytes = new Uint8Array([1, 2, 3, 4]);
    const apiRequests = [];
    const imageRequests = [];
    const client = makeClient(
      async (url) => {
        apiRequests.push(new URL(url));
        return jsonResponse({
          images: {
            '1:2': 'https://figma-image.example.com/tmp-render.png?sig=secret',
          },
        });
      },
      {
        imageFetchImpl: async (url) => {
          imageRequests.push(url);
          return binaryResponse(imageBytes, {
            headers: { 'Content-Length': String(imageBytes.byteLength) },
          });
        },
      },
    );

    const result = await client.exportNodeImage({
      fileKey: 'fileKey123',
      nodeId: '1:2',
      outPath,
      scale: 2,
    });

    assert.equal(apiRequests[0].pathname, '/v1/images/fileKey123');
    assert.equal(apiRequests[0].searchParams.get('ids'), '1:2');
    assert.equal(apiRequests[0].searchParams.get('format'), 'png');
    assert.equal(apiRequests[0].searchParams.get('scale'), '2');
    assert.deepEqual(imageRequests, ['https://figma-image.example.com/tmp-render.png?sig=secret']);
    assert.equal(result.path, outPath);
    assert.equal(result.byteLength, 4);
    assert.deepEqual(new Uint8Array(await fs.readFile(outPath)), imageBytes);
  });

  it('rejects unsafe image downloads and oversized images with screenshot_failed', async () => {
    const tempDir = await makeTempDir();
    const client = makeClient(async () => jsonResponse({ id: 'unused' }), {
      imageFetchImpl: async () =>
        binaryResponse(new Uint8Array([1]), {
          headers: { 'Content-Length': String(21 * 1024 * 1024) },
        }),
    });

    await assert.rejects(
      client.downloadImage({
        imageUrl: 'https://figma-image.example.com/tmp-render.png',
        allowedImageUrls: new Set(['https://other.example.com/render.png']),
        outPath: path.join(tempDir, 'not-allowed.png'),
      }),
      { code: 'image_url_not_allowed' },
    );

    await assert.rejects(
      client.downloadImage({
        imageUrl: 'http://figma-image.example.com/tmp-render.png',
        allowedImageUrls: new Set(['http://figma-image.example.com/tmp-render.png']),
        outPath: path.join(tempDir, 'http.png'),
      }),
      { code: 'image_url_invalid_protocol' },
    );

    await assert.rejects(
      client.downloadImage({
        imageUrl: 'https://figma-image.example.com/tmp-render.png',
        allowedImageUrls: new Set(['https://figma-image.example.com/tmp-render.png']),
        outPath: path.join(tempDir, 'too-large.png'),
      }),
      { code: 'screenshot_failed' },
    );
  });
});

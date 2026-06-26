import { describe, test, expect, mock, beforeEach, afterEach } from 'bun:test';
import { RobloxApiClient, parseRobloxApiKeyJwt } from '../lib/api.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe('parseRobloxApiKeyJwt', () => {
  test('parses valid JWT from API key', () => {
    const TEST_API_KEY = Buffer.from(
      'prefix_eyJhbGciOiJIUzI1NiJ9.eyJvd25lcklkIjoiMTIzNDU2Nzg5IiwiZXhwIjoxNzAwMDAwMDAwfQ.sig_suffix'
    ).toString('base64');

    const result = parseRobloxApiKeyJwt(TEST_API_KEY);

    expect(result.ownerId).toBe('123456789');
    expect(result.exp).toBe(1700000000);
  });

  test('returns null for invalid API key', () => {
    const result = parseRobloxApiKeyJwt('invalid_short_key');

    expect(result.ownerId).toBeNull();
    expect(result.exp).toBeNull();
  });

  test('returns null for malformed base64', () => {
    const result = parseRobloxApiKeyJwt('!!!not-base64!!!');

    expect(result.ownerId).toBeNull();
    expect(result.exp).toBeNull();
  });
});

describe('RobloxApiClient', () => {
  describe('listGamePasses', () => {
    test('uses v1 URL for game passes', async () => {
      const mockFetch = mock((url: string) => {
        expect(url).toContain('https://apis.roblox.com/game-passes/v1/');
        return Promise.resolve(new Response(JSON.stringify({
          gamePasses: [],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      await client.listGamePasses('12345');

      expect(mockFetch).toHaveBeenCalled();
    });

    test('includes x-api-key header', async () => {
      const mockFetch = mock((_url: string, options: RequestInit) => {
        const headers = options.headers as Record<string, string>;
        expect(headers['x-api-key']).toBe('test-api-key');
        return Promise.resolve(new Response(JSON.stringify({
          gamePasses: [],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      await client.listGamePasses('12345');

      expect(mockFetch).toHaveBeenCalled();
    });

    test('paginates through all results', async () => {
      let callCount = 0;
      const mockFetch = mock((url: string) => {
        callCount++;
        if (callCount === 1) {
          expect(url).not.toContain('pageToken');
          return Promise.resolve(new Response(JSON.stringify({
            gamePasses: [{ gamePassId: 1, name: 'Pass 1' }],
            nextPageToken: 'token123'
          })));
        } else {
          expect(url).toContain('pageToken=token123');
          return Promise.resolve(new Response(JSON.stringify({
            gamePasses: [{ gamePassId: 2, name: 'Pass 2' }],
            nextPageToken: null
          })));
        }
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listGamePasses('12345');

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(2);
        expect(result.data[0]?.gamePassId).toBe(1);
        expect(result.data[1]?.gamePassId).toBe(2);
      }
      expect(callCount).toBe(2);
    });
  });

  describe('listProducts', () => {
    test('uses v2 URL for developer products', async () => {
      const mockFetch = mock((url: string) => {
        expect(url).toContain('https://apis.roblox.com/developer-products/v2/');
        return Promise.resolve(new Response(JSON.stringify({
          developerProducts: [],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      await client.listProducts('12345');

      expect(mockFetch).toHaveBeenCalled();
    });

    test('includes x-api-key header', async () => {
      const mockFetch = mock((_url: string, options: RequestInit) => {
        const headers = options.headers as Record<string, string>;
        expect(headers['x-api-key']).toBe('my-secret-key');
        return Promise.resolve(new Response(JSON.stringify({
          developerProducts: [],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('my-secret-key');
      await client.listProducts('12345');

      expect(mockFetch).toHaveBeenCalled();
    });
  });

  describe('getProduct', () => {
    test('uses v2 URL with creator suffix', async () => {
      const mockFetch = mock((url: string) => {
        expect(url).toBe('https://apis.roblox.com/developer-products/v2/universes/12345/developer-products/67890/creator');
        return Promise.resolve(new Response(JSON.stringify({
          productId: 67890,
          name: 'Test Product'
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.getProduct('12345', '67890');

      expect(result.success).toBe(true);
      expect(mockFetch).toHaveBeenCalled();
    });
  });

  describe('createGamePass', () => {
    test('uses POST method with multipart body', async () => {
      const mockFetch = mock((url: string, options: RequestInit) => {
        expect(url).toContain('https://apis.roblox.com/game-passes/v1/');
        expect(options.method).toBe('POST');
        const contentType = (options.headers as Record<string, string>)['Content-Type'];
        expect(contentType).toContain('multipart/form-data');
        return Promise.resolve(new Response(JSON.stringify({
          gamePassId: 999,
          name: 'New Pass'
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      await client.createGamePass('12345', { name: 'New Pass', price: 100 });

      expect(mockFetch).toHaveBeenCalled();
    });
  });

  describe('updateGamePass', () => {
    test('uses PATCH method', async () => {
      const mockFetch = mock((_url: string, options: RequestInit) => {
        expect(options.method).toBe('PATCH');
        return Promise.resolve(new Response(JSON.stringify({
          gamePassId: 999,
          name: 'Updated Pass'
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      await client.updateGamePass('12345', '999', { name: 'Updated Pass' });

      expect(mockFetch).toHaveBeenCalled();
    });
  });

  describe('retry logic', () => {
    test('retries on 429 and succeeds', async () => {
      let callCount = 0;
      const mockFetch = mock(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve(new Response('Rate limited', { status: 429 }));
        }
        return Promise.resolve(new Response(JSON.stringify({
          developerProducts: [{ productId: 1, name: 'Product' }],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listProducts('12345');

      expect(result.success).toBe(true);
      expect(callCount).toBeGreaterThan(1);
    }, 10000);

    test('retries on 500 and succeeds', async () => {
      let callCount = 0;
      const mockFetch = mock(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve(new Response('Server error', { status: 500 }));
        }
        return Promise.resolve(new Response(JSON.stringify({
          gamePasses: [],
          nextPageToken: null
        })));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listGamePasses('12345');

      expect(result.success).toBe(true);
      expect(callCount).toBeGreaterThan(1);
    }, 10000);

    test('returns error after max retries', async () => {
      let callCount = 0;
      const mockFetch = mock(() => {
        callCount++;
        return Promise.resolve(new Response('Rate limited', { status: 429 }));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listProducts('12345');

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('RATE_LIMITED');
      }
      expect(callCount).toBe(4);
    }, 30000);

    test('does not retry on 401', async () => {
      let callCount = 0;
      const mockFetch = mock(() => {
        callCount++;
        return Promise.resolve(new Response('Unauthorized', { status: 401 }));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listProducts('12345');

      expect(result.success).toBe(false);
      expect(callCount).toBe(1);
    });

    test('does not retry on 404', async () => {
      let callCount = 0;
      const mockFetch = mock(() => {
        callCount++;
        return Promise.resolve(new Response('Not found', { status: 404 }));
      });
      globalThis.fetch = mockFetch;

      const client = new RobloxApiClient('test-api-key');
      const result = await client.getProduct('12345', '99999');

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('NOT_FOUND');
      }
      expect(callCount).toBe(1);
    });
  });

  describe('error handling', () => {
    test('returns API_ERROR for 401', async () => {
      globalThis.fetch = mock(() => Promise.resolve(new Response('Unauthorized', { status: 401 })));

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listProducts('12345');

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('API_ERROR');
        expect(result.error.message).toContain('Invalid or expired API key');
      }
    });

    test('returns API_ERROR for 403', async () => {
      globalThis.fetch = mock(() => Promise.resolve(new Response('Forbidden', { status: 403 })));

      const client = new RobloxApiClient('test-api-key');
      const result = await client.listProducts('12345');

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('API_ERROR');
        expect(result.error.message).toContain('lacks access');
      }
    });

    test('returns INVALID_ARGS for 400', async () => {
      globalThis.fetch = mock(() => Promise.resolve(new Response('Bad request', { status: 400 })));

      const client = new RobloxApiClient('test-api-key');
      const result = await client.createProduct('12345', { name: '', price: -1 });

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('INVALID_ARGS');
      }
    });
  });
});

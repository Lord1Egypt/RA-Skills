import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import {
  ensureFigmaAccessToken,
  readTokenStore,
  withFigmaTokenRetry,
  writeTokenStore,
} from '../scripts/lib/figma-token-store.mjs';

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-token-test-'));
}

async function writeEnvFile(filePath, values) {
  const lines = Object.entries(values).map(([key, value]) => `${key}=${value}`);
  await fs.writeFile(filePath, `${lines.join('\n')}\n`, { mode: 0o600 });
}

function makeRefreshFetch({
  accessToken = 'new-access-token',
  refreshToken,
  expiresIn = 3600,
  status = 200,
  body,
  calls,
} = {}) {
  return async (url, init) => {
    calls?.push({ url, init });
    return {
      ok: status >= 200 && status < 300,
      status,
      async json() {
        if (body) {
          return body;
        }
        return {
          access_token: accessToken,
          refresh_token: refreshToken,
          token_type: 'Bearer',
          expires_in: expiresIn,
        };
      },
      async text() {
        return JSON.stringify(body ?? {});
      },
    };
  };
}

describe('ensureFigmaAccessToken', () => {
  it('imports a first token store from an env file with secure permissions', async () => {
    const tempDir = await makeTempDir();
    const envFile = path.join(tempDir, '.env');
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeEnvFile(envFile, {
      FIGMA_CLIENT_ID: 'client-id-1',
      FIGMA_CLIENT_SECRET: 'client-secret-1',
      FIGMA_ACCESS_TOKEN: 'access-token-1',
      FIGMA_REFRESH_TOKEN: 'refresh-token-1',
      FIGMA_TOKEN_TYPE: 'Bearer',
      FIGMA_TOKEN_EXPIRES_AT: '2026-07-22T01:00:00.000Z',
    });

    const token = await ensureFigmaAccessToken({
      tokenStorePath,
      envFiles: [envFile],
      now: () => new Date('2026-07-22T00:00:00Z'),
      fetchImpl: makeRefreshFetch(),
    });

    assert.equal(token.accessToken, 'access-token-1');
    const dirMode = (await fs.stat(path.dirname(tokenStorePath))).mode & 0o777;
    const fileMode = (await fs.stat(tokenStorePath)).mode & 0o777;
    assert.equal(dirMode, 0o700);
    assert.equal(fileMode, 0o600);

    const stored = await readTokenStore(tokenStorePath);
    assert.equal(stored.clientId, 'client-id-1');
    assert.equal(stored.refreshToken, 'refresh-token-1');
  });

  it('does not fall back to env when an existing token store is corrupt', async () => {
    const tempDir = await makeTempDir();
    const envFile = path.join(tempDir, '.env');
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await fs.mkdir(path.dirname(tokenStorePath), { recursive: true, mode: 0o700 });
    await fs.writeFile(tokenStorePath, '{not-json', { mode: 0o600 });
    await writeEnvFile(envFile, {
      FIGMA_CLIENT_ID: 'client-id-1',
      FIGMA_CLIENT_SECRET: 'client-secret-1',
      FIGMA_ACCESS_TOKEN: 'access-token-1',
      FIGMA_REFRESH_TOKEN: 'refresh-token-1',
      FIGMA_TOKEN_TYPE: 'Bearer',
      FIGMA_TOKEN_EXPIRES_AT: '2026-07-22T01:00:00.000Z',
    });

    await assert.rejects(
      ensureFigmaAccessToken({
        tokenStorePath,
        envFiles: [envFile],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl: makeRefreshFetch(),
      }),
      (error) => {
        assert.equal(error.code, 'figma_token_store_invalid');
        assert.equal(String(error.message).includes('access-token-1'), false);
        return true;
      },
    );
  });

  it('fails with figma_env_missing when configured env files have no full Figma credential set', async () => {
    const tempDir = await makeTempDir();
    const envFile = path.join(tempDir, '.env');
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeEnvFile(envFile, {
      FIGMA_CLIENT_ID: 'client-id-1',
    });

    await assert.rejects(
      ensureFigmaAccessToken({
        tokenStorePath,
        envFiles: [envFile],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl: makeRefreshFetch(),
      }),
      { code: 'figma_env_missing' },
    );
  });

  it('accepts Figma env expires_at as Unix seconds and stores a normalized ISO timestamp', async () => {
    const tempDir = await makeTempDir();
    const envFile = path.join(tempDir, '.env');
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeEnvFile(envFile, {
      FIGMA_CLIENT_ID: 'client-id-1',
      FIGMA_CLIENT_SECRET: 'client-secret-1',
      FIGMA_ACCESS_TOKEN: 'access-token-1',
      FIGMA_REFRESH_TOKEN: 'refresh-token-1',
      FIGMA_TOKEN_TYPE: 'bearer',
      FIGMA_TOKEN_EXPIRES_AT: '1791912467',
    });

    const token = await ensureFigmaAccessToken({
      tokenStorePath,
      envFiles: [envFile],
      now: () => new Date('2026-07-22T00:00:00Z'),
      fetchImpl: makeRefreshFetch(),
    });

    assert.equal(token.accessToken, 'access-token-1');
    assert.equal(token.tokenType, 'Bearer');
    assert.equal(token.expiresAt, '2026-10-13T17:27:47.000Z');
    const stored = await readTokenStore(tokenStorePath);
    assert.equal(stored.tokenType, 'Bearer');
    assert.equal(stored.expiresAt, '2026-10-13T17:27:47.000Z');
  });

  it('rejects insecure token directory and file permissions', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await fs.mkdir(path.dirname(tokenStorePath), { recursive: true, mode: 0o755 });
    await fs.writeFile(
      tokenStorePath,
      JSON.stringify({
        schemaVersion: 'figma-oauth-token/v1',
        clientId: 'client-id-1',
        clientSecret: 'client-secret-1',
        accessToken: 'access-token-1',
        refreshToken: 'refresh-token-1',
        tokenType: 'Bearer',
        expiresAt: '2026-07-22T01:00:00.000Z',
      }),
      { mode: 0o644 },
    );

    await assert.rejects(readTokenStore(tokenStorePath), { code: 'figma_token_dir_insecure' });

    await fs.chmod(path.dirname(tokenStorePath), 0o700);
    await assert.rejects(readTokenStore(tokenStorePath), { code: 'figma_token_file_insecure' });
  });

  it('refreshes tokens that expire within five minutes and saves refresh-token rotation', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T00:04:00.000Z',
    });
    const calls = [];

    const token = await ensureFigmaAccessToken({
      tokenStorePath,
      envFiles: [],
      now: () => new Date('2026-07-22T00:00:00Z'),
      fetchImpl: makeRefreshFetch({
        accessToken: 'new-access-token',
        refreshToken: 'new-refresh-token',
        calls,
      }),
    });

    assert.equal(token.accessToken, 'new-access-token');
    assert.equal(calls.length, 1);
    const stored = await readTokenStore(tokenStorePath);
    assert.equal(stored.accessToken, 'new-access-token');
    assert.equal(stored.refreshToken, 'new-refresh-token');
    assert.equal(stored.expiresAt, '2026-07-22T01:00:00.000Z');
  });

  it('refreshes from a native Response body that can only be consumed once', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T00:04:00.000Z',
    });

    const token = await ensureFigmaAccessToken({
      tokenStorePath,
      envFiles: [],
      now: () => new Date('2026-07-22T00:00:00Z'),
      fetchImpl: async () =>
        new Response(
          JSON.stringify({
            access_token: 'native-response-access-token',
            refresh_token: 'native-response-refresh-token',
            token_type: 'Bearer',
            expires_in: 3600,
          }),
          {
            status: 200,
            headers: {
              'Content-Type': 'application/json',
            },
          },
        ),
    });

    assert.equal(token.accessToken, 'native-response-access-token');
    const stored = await readTokenStore(tokenStorePath);
    assert.equal(stored.accessToken, 'native-response-access-token');
    assert.equal(stored.refreshToken, 'native-response-refresh-token');
    assert.equal(stored.expiresAt, '2026-07-22T01:00:00.000Z');
  });

  it('preserves the old refresh token when Figma omits refresh_token', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T00:04:00.000Z',
    });

    await ensureFigmaAccessToken({
      tokenStorePath,
      envFiles: [],
      now: () => new Date('2026-07-22T00:00:00Z'),
      fetchImpl: makeRefreshFetch({
        accessToken: 'new-access-token',
      }),
    });

    const stored = await readTokenStore(tokenStorePath);
    assert.equal(stored.refreshToken, 'old-refresh-token');
  });

  it('uses a single lock so concurrent refresh writes one refreshed token', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T00:04:00.000Z',
    });
    const calls = [];
    const fetchImpl = async (...args) => {
      calls.push(args);
      await new Promise((resolve) => setTimeout(resolve, 25));
      return makeRefreshFetch({ accessToken: 'new-access-token' })(...args);
    };

    const [first, second] = await Promise.all([
      ensureFigmaAccessToken({
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl,
      }),
      ensureFigmaAccessToken({
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl,
      }),
    ]);

    assert.equal(first.accessToken, 'new-access-token');
    assert.equal(second.accessToken, 'new-access-token');
    assert.equal(calls.length, 1);
  });

  it('stops automatic retry on invalid_grant without leaking secret values', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T00:04:00.000Z',
    });

    await assert.rejects(
      ensureFigmaAccessToken({
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl: makeRefreshFetch({
          status: 400,
          body: {
            error: 'invalid_grant',
            error_description: 'old-refresh-token is not valid',
          },
        }),
      }),
      (error) => {
        assert.equal(error.code, 'figma_token_invalid_grant');
        assert.equal(String(error.message).includes('old-refresh-token'), false);
        return true;
      },
    );
  });
});

describe('withFigmaTokenRetry', () => {
  it('refreshes once after a 401 result and retries the original operation once', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T01:00:00.000Z',
    });
    const operationTokens = [];

    const result = await withFigmaTokenRetry(
      {
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        fetchImpl: makeRefreshFetch({ accessToken: 'new-access-token' }),
      },
      async (token) => {
        operationTokens.push(token.accessToken);
        if (operationTokens.length === 1) {
          return { ok: false, status: 401 };
        }
        return { ok: true, status: 200, body: 'done' };
      },
    );

    assert.deepEqual(operationTokens, ['old-access-token', 'new-access-token']);
    assert.deepEqual(result, { ok: true, status: 200, body: 'done' });
  });

  it('coalesces concurrent 401-triggered refreshes behind the token lock', async () => {
    const tempDir = await makeTempDir();
    const tokenStorePath = path.join(tempDir, 'secrets', 'figma-oauth.json');
    await writeTokenStore(tokenStorePath, {
      clientId: 'client-id-1',
      clientSecret: 'client-secret-1',
      accessToken: 'old-access-token',
      refreshToken: 'old-refresh-token',
      tokenType: 'Bearer',
      expiresAt: '2026-07-22T01:00:00.000Z',
    });
    const refreshCalls = [];
    const operationTokens = [];
    let firstOperationCount = 0;
    let releaseBothFirstOperations;
    const bothFirstOperationsSeen = new Promise((resolve) => {
      releaseBothFirstOperations = resolve;
    });
    const waitForBothFirstOperations = new Promise((resolve) => {
      const maybeResolve = () => {
        if (firstOperationCount === 2) {
          releaseBothFirstOperations();
          resolve();
        }
      };
      globalThis.__readFigmaMaybeResolve = maybeResolve;
    });

    const operation = async (token) => {
      operationTokens.push(token.accessToken);
      if (token.accessToken === 'old-access-token') {
        firstOperationCount += 1;
        globalThis.__readFigmaMaybeResolve();
        await bothFirstOperationsSeen;
        return { ok: false, status: 401 };
      }
      return { ok: true, status: 200, token: token.accessToken };
    };

    const first = withFigmaTokenRetry(
      {
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        lockRetryDelayMs: 1,
        fetchImpl: async (...args) => {
          refreshCalls.push(args);
          await new Promise((resolve) => setTimeout(resolve, 25));
          return makeRefreshFetch({ accessToken: 'new-access-token' })(...args);
        },
      },
      operation,
    );
    const second = withFigmaTokenRetry(
      {
        tokenStorePath,
        envFiles: [],
        now: () => new Date('2026-07-22T00:00:00Z'),
        lockRetryDelayMs: 1,
        fetchImpl: async (...args) => {
          refreshCalls.push(args);
          await new Promise((resolve) => setTimeout(resolve, 25));
          return makeRefreshFetch({ accessToken: 'new-access-token' })(...args);
        },
      },
      operation,
    );

    await waitForBothFirstOperations;
    const results = await Promise.all([first, second]);

    assert.deepEqual(results, [
      { ok: true, status: 200, token: 'new-access-token' },
      { ok: true, status: 200, token: 'new-access-token' },
    ]);
    assert.equal(refreshCalls.length, 1);
    assert.equal(operationTokens.filter((token) => token === 'old-access-token').length, 2);
    assert.equal(operationTokens.filter((token) => token === 'new-access-token').length, 2);
    delete globalThis.__readFigmaMaybeResolve;
  });
});
